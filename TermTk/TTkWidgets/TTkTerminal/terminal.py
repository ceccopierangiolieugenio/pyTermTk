# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, pty, threading
import struct, fcntl, termios

import re
from select import select
from TermTk.TTkCore.canvas import TTkCanvas


from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkGui.clipboard import TTkClipboard
from TermTk.TTkGui.textwrap1 import TTkTextWrap
from TermTk.TTkGui.textcursor import TTkTextCursor
from TermTk.TTkGui.textdocument import TTkTextDocument
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView, TTkAbstractScrollViewGridLayout
from TermTk.TTkWidgets.widget import TTkWidget

from TermTk.TTkWidgets.TTkTerminal.terminal_alt    import _TTkTerminalAltScreen
from TermTk.TTkWidgets.TTkTerminal.terminal_normal import _TTkTerminalNormalScreen

from TermTk.TTkWidgets.TTkTerminal.vt102 import TTkVT102

from TermTk.TTkCore.TTkTerm.colors import TTkTermColor
from TermTk.TTkCore.TTkTerm.colors_ansi_map import ansiMap16, ansiMap256

__all__ = ['TTkTerminal']

class TTkTerminal(TTkWidget):
    __slots__ = ('_shell', '_fd', '_inout', '_proc', '_quit_pipe', '_mode_normal'
                 '_buffer_lines', '_buffer_screen',
                 '_screen_current', '_screen_normal', '_screen_alt')
    def __init__(self, *args, **kwargs):
        self._shell = os.environ.get('SHELL', 'sh')
        self._fd = None
        self._proc = None
        self._mode_normal = True
        self._quit_pipe = None
        self._buffer_lines = [TTkString()]
        self._screen_normal  = _TTkTerminalNormalScreen()
        self._screen_alt     = _TTkTerminalAltScreen()
        self._screen_current = self._screen_normal

        super().__init__(*args, **kwargs)

        # self._screen_alt._CSI_MAP     |= self._CSI_MAP
        # self._screen_current._CSI_MAP |= self._CSI_MAP

        w,h = self.size()
        self._screen_alt.resize(w,h)
        self._screen_normal.resize(w,h)

        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)
        self.enableWidgetCursor()
        TTkHelper.quitEvent.connect(self._quit)

    def resizeEvent(self, w: int, h: int):
        if self._fd:
            # s = struct.pack('HHHH', 0, 0, 0, 0)
            # t = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s)
            # print(struct.unpack('HHHH', t))
            s = struct.pack('HHHH', h, w, 0, 0)
            t = fcntl.ioctl(self._fd, termios.TIOCSWINSZ, s)

            # termios.tcsetwinsize(self._fd,(h,w))
        self._screen_alt.resize(w,h)
        self._screen_normal.resize(w,h)
        return super().resizeEvent(w, h)

    def runShell(self, program=None):
        self._shell = program if program else self._shell

        pid, self._fd = pty.fork()

        if pid == 0:
            def _spawnTerminal(argv=[self._shell], env=os.environ):
                os.execvpe(argv[0], argv, env)
            threading.Thread(target=_spawnTerminal).start()
            TTkHelper.quit()
            # os.execvpe(argv[0], argv, env)
            # os.execvpe(argv[0], argv, env)
            # self._proc = subprocess.Popen(self._shell)
            # TTkLog.debug(f"Terminal PID={self._proc.pid=}")
            # self._proc.wait()
        else:
            self._inout = os.fdopen(self._fd, "w+b", 0)
            name = os.ttyname(self._fd)
            TTkLog.debug(f"{pid=} {self._fd=} {name}")

            self._quit_pipe = os.pipe()

            threading.Thread(target=self.loop,args=[self]).start()

    # xterm escape sequences from:
    # https://invisible-island.net/xterm/ctlseqs/ctlseqs.html
    # https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-Functions-using-CSI-_-ordered-by-the-final-character_s_
    re_CURSOR      = re.compile('^\[((\d*)(;(\d*))*)([@^`A-Za-z])')
    # https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-Functions-using-CSI-_-ordered-by-the-final-character_s_
    # Basic Re for CSI Ps matches:
    #   CSI : Control Sequence Introducer "<ESC>[" = '\033['
    #   Ps  : A single (usually optional) numeric parameter, composed of one or more digits.
    #   fn  : the single char defining the function
    re_CSI_Ps_fu    = re.compile('^\[(\d*)([@ABCDEFGIJKLMPSTXZ^`abcdeghinqx])')
    re_CSI_Ps_Ps_fu = re.compile('^\[(\d*);(\d*)([Hf])')

    re_DEC_SET_RST  = re.compile('^\[\?(\d+)([lh])')
    # re_CURSOR_1    = re.compile(r'^(\d+)([ABCDEFGIJKLMPSTXZHf])')

    @pyTTkSlot()
    def _quit(self):
        if self._quit_pipe:
            os.write(self._quit_pipe[1], b'quit')

    def loop(self, _):
        while rs := select( [self._inout,self._quit_pipe[0]], [], [])[0]:
            if self._quit_pipe[0] in rs:
                break
            # TTkLog.debug(f"Select - {rs=}")
            for r in rs:
                if r is not self._inout:
                    continue
                try:
                    out = self._inout.read(10240)
                except Exception as e:
                    TTkLog.error(f"Error: {e=}")
                    return
                # out = out.decode('utf-8','ignore')
                out = out.decode()
                for bi, bout in enumerate(out.split('\a')): # grab the bells
                    # TTkLog.debug(f'Eugenio->{out}')
                    # sout = bout.decode('utf-8','ignore')
                    if bi:
                        TTkLog.debug("BELL!!! 🔔🔔🔔")
                    sout = bout.split('\033')
                    TTkLog.debug(f"{sout[0]=}")
                    self._screen_current.pushLine(sout[0])
                    for slice in sout[1:]:
                        ssss = slice.replace('\033','<ESC>').replace('\n','\\n').replace('\r','\\r')
                        TTkLog.debug(f"slice: {ssss}")
                        if m := TTkTerminal.re_DEC_SET_RST.match(slice):
                            en = m.end()
                            ps = int(m.group(1))
                            sr = (m.group(2) == 'h')
                            self._CSI_DEC_SET_RST(ps,sr)
                            slice = slice[en:]
                        elif ( (m      := TTkTerminal.re_CURSOR.match(slice)) and
                                (mg     := m.groups()) and
                                mg[-1] == 'm' ):
                            # TTkLog.debug(f"Handle color {mg[0]=}")
                            en = m.end()

                            color=TTkColor.RST

                            if mg[0] not in ['0','']:
                                values = mg[0].split(';')

                                fg = None
                                bg = None
                                mod = 0
                                clean = False

                                while values:
                                    s = int(values.pop(0))
                                    if s==0: # Reset Color/Format
                                        fg = None
                                        bg = None
                                        mod = 0
                                        clean = True
                                    elif ( # Ansi 16 colors
                                        30  <= s <= 37 or   # fg [ 30 -  37]
                                        90  <= s <= 97 ):   # fg [ 90 -  97] Bright
                                        fg = ansiMap16.get(s)
                                    elif ( # Ansi 16 colors
                                        40  <= s <= 47 or   # bg [ 40 -  47]
                                        100 <= s <= 107 ) : # bg [100 - 107] Bright
                                        bg = ansiMap16.get(s)
                                    elif s == 38:
                                        t =  int(values.pop(0))
                                        if t == 5:# 256 fg
                                            fg = ansiMap256.get(int(values.pop(0)))
                                        if t == 2:# 24 bit fg
                                            fg = (int(values.pop(0)),int(values.pop(0)),int(values.pop(0)))
                                    elif s == 48:
                                        t =  int(values.pop(0))
                                        if t == 5:# 256 bg
                                            bg = ansiMap256.get(int(values.pop(0)))
                                        if t == 2:# 24 bit bg
                                            bg = (int(values.pop(0)),int(values.pop(0)),int(values.pop(0)))
                                    elif s==1: mod += TTkTermColor.BOLD
                                    elif s==3: mod += TTkTermColor.ITALIC
                                    elif s==4: mod += TTkTermColor.UNDERLINE
                                    elif s==9: mod += TTkTermColor.STRIKETROUGH
                                    elif s==5: mod += TTkTermColor.BLINKING
                                color = TTkColor(fg=fg, bg=bg, mod=mod, clean=clean)

                            self._screen_alt.setColor(color)
                            self._screen_normal.setColor(color)

                            # TTkLog.debug(TTkString(f"color - <ESC>[{mg[0]}",color).toAnsi())

                            slice = slice[en:]
                        elif m:
                            en = m.end()
                            y  = ps = int(y) if (y:=m.group(2)) else 1
                            sep = m.group(3)
                            x =       int(x) if (x:=m.group(4)) else 1
                            fn = m.group(5)
                            TTkLog.debug(f"{mg[0]}{fn} = ps:{y=} {sep=} {x=} {fn=}")
                            if fn in ['n']:
                                _ex = self._CSI_MAP.get(
                                        fn,
                                        lambda a,b,c: TTkLog.warn(f"Unhandled <ESC>[{mg[0]}{fn} = ps:{y=} {sep=} {x=} {fn=}"))
                                _ex(self,y,x)
                            else:
                                _ex = self._screen_current._CSI_MAP.get(
                                        fn,
                                        lambda a,b,c: TTkLog.warn(f"Unhandled <ESC>[{mg[0]}{fn} = ps:{y=} {sep=} {x=} {fn=}"))
                                _ex(self._screen_current,y,x)
                            slice = slice[en:]
                        else:
                            slice = '\033' + slice.replace('\r','')
                            ssss = slice.replace('\033','<ESC>').replace('\n','\\n')
                            TTkLog.warn(f"Unhandled Slice:{ssss}")

                        # TTkLog.debug(f'Eugenio->{slice}')
                        if '\033' in slice:
                            # import time
                            # ssss = slice.replace('\033','<ESC>').replace('\n','\\n')
                            # TTkLog.warn(f"WAIT FOR Unhandled Slice:{ssss}")
                            # time.sleep(0.5)
                            # self._screen_current.pushLine(slice)
                            # TTkLog.warn(f"DONE!!!! Unhandled Slice:{ssss}")
                            slice = slice.replace('\033','<ESC>').replace('\n','\\n')
                            TTkLog.warn(f"Unhandled slice: {slice=}")
                            # time.sleep(1.5)
                        else:
                            self._screen_current.pushLine(slice)
                            slice = slice.replace('\033','<ESC>').replace('\n','\\n')
                            # TTkLog.debug(f"{slice=}")
                    self.update()
                    self.setWidgetCursor(pos=self._screen_current.getCursor())
                    TTkLog.debug(f"wc:{self._screen_current.getCursor()} {self._proc=}")

    def mousePressEvent(self, evt):
        return True

    def keyEvent(self, evt):
        # TTkLog.debug(f"Key: {evt.code=}")
        TTkLog.debug(f"Key: {str(evt)=}")
        if evt.type == TTkK.SpecialKey:
            if evt.key == TTkK.Key_Enter:
                TTkLog.debug(f"Key: Enter")
                # self._inout.write(b'\n')
                # self._inout.write(evt.code.encode())
        else: # Input char
            TTkLog.debug(f"Key: {evt.key=}")
            # self._inout.write(evt.key.encode())
        self._inout.write(evt.code.encode())
        return True

    def paintEvent(self, canvas: TTkCanvas):
        w,h = self.size()
        self._screen_current.paintEvent(canvas,w,h)

    # CSI Ps n  Device Status Report (DSR).
    #             Ps = 5  ⇒  Status Report.
    #           Result ("OK") is CSI 0 n
    #             Ps = 6  ⇒  Report Cursor Position (CPR) [row;column].
    #           Result is CSI r ; c R
    #
    #           Note: it is possible for this sequence to be sent by a
    #           function key.  For example, with the default keyboard
    #           configuration the shifted F1 key may send (with shift-,
    #           control-, alt-modifiers)
    #
    #             CSI 1 ; 2  R , or
    #             CSI 1 ; 5  R , or
    #             CSI 1 ; 6  R , etc.
    #
    #           The second parameter encodes the modifiers; values range from
    #           2 to 16.  See the section PC-Style Function Keys for the
    #           codes.  The modifyFunctionKeys and modifyKeyboard resources
    #           can change the form of the string sent from the modified F1
    #           key.
    def _CSI_n_DSR(self, ps, _):
        x,y = self._screen_current.getCursor()
        if ps==6:
            self._inout.write(f"\033[{y+1};{x+1}R".encode())
        elif ps==5:
            self._inout.write(f"\033[0n".encode())

    _CSI_MAP = {
        'n': _CSI_n_DSR,
    }

    def _CSI_DEC_SET_RST(self, ps, s):
        _dec = self._CSI_DEC_SET_RST_MAP.get(
                ps,
                lambda a,b: TTkLog.warn(f"Unhandled DEC <ESC>[{ps}{'h' if s else 'l'}"))
        _dec(self, s)
    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 2 5  ⇒  Show cursor (DECTCEM), VT220.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 2 5  ⇒  Hide cursor (DECTCEM), VT220.
    def _CSI_DEC_SR_25(self, s):
        self.enableWidgetCursor(enable=s)

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1 0 4 9  ⇒  Save cursor as in DECSC, xterm.  After
    #           saving the cursor, switch to the Alternate Screen Buffer,
    #           clearing it first.  This may be disabled by the titeInhibit
    #           resource.  This control combines the effects of the 1 0 4 7
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1 0 4 9  ⇒  Use Normal Screen Buffer and restore cursor
    #           as in DECRC, xterm.  This may be disabled by the titeInhibit
    #           resource.  This combines the effects of the 1 0 4 7  and 1 0 4
    #           8  modes.  Use this with terminfo-based applications rather
    #           than the 4 7  mode.
    def _CSI_DEC_SR_1049(self, s):
        if s:
            self._screen_current = self._screen_alt
        else:
            self._screen_current = self._screen_normal


    _CSI_DEC_SET_RST_MAP = {
        25  : _CSI_DEC_SR_25,
        1049: _CSI_DEC_SR_1049
    }