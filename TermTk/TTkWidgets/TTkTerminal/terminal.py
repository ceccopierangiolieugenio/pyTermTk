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
    __slots__ = ('_shell', '_fd', '_inout', '_mode_normal'
                 '_buffer_lines', '_buffer_screen',
                 '_screen_current', '_screen_normal', '_screen_alt')
    def __init__(self, *args, **kwargs):
        self._shell = os.environ.get('SHELL', 'sh')
        self._fd = None
        self._mode_normal = True
        self._buffer_lines = [TTkString()]
        self._screen_normal  = _TTkTerminalNormalScreen()
        self._screen_alt     = _TTkTerminalAltScreen()
        self._screen_current = self._screen_normal

        super().__init__(*args, **kwargs)

        w,h = self.size()
        self._screen_alt.resize(w,h)
        self._screen_normal.resize(w,h)

        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)
        self.enableWidgetCursor()

    def resizeEvent(self, w: int, h: int):
        self._screen_alt.resize(w,h)
        self._screen_normal.resize(w,h)
        return super().resizeEvent(w, h)

    def runShell(self, program=None):
        self._shell = program if program else self._shell

        pid, self._fd = pty.fork()

        if pid == 0:
            argv = [self._shell]
            env = dict(TERM="screen", DISPLAY=":1")
            os.execvpe(argv[0], argv, env)
        else:
            self._inout = os.fdopen(self._fd, "w+b", 0)
            name = os.ttyname(self._fd)
            TTkLog.debug(f"{self._fd=} {name}")

            threading.Thread(target=self.loop,args=[self]).start()

    # xterm escape sequences from:
    # https://invisible-island.net/xterm/ctlseqs/ctlseqs.html
    # https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-Functions-using-CSI-_-ordered-by-the-final-character_s_
    re_CURSOR      = re.compile('^((\d*)(;(\d*))*)([@ABCDEFGIJKLMPSTXZ^`abcdeginmqxHf])')
    # https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-Functions-using-CSI-_-ordered-by-the-final-character_s_
    # Basic Re for CSI Ps matches:
    #   CSI : Control Sequence Introducer "<ESC>[" = '\033['
    #   Ps  : A single (usually optional) numeric parameter, composed of one or more digits.
    #   fn  : the single char defining the function
    re_CSI_Ps_fu    = re.compile('^(\d*)([@ABCDEFGIJKLMPSTXZ^`abcdeginqx])')
    re_CSI_Ps_Ps_fu = re.compile('^(\d*);(\d*)([Hf])')
    re_DEC_SET_RST  = re.compile('^\?(\d+)([lh])')
    # re_CURSOR_1    = re.compile(r'^(\d+)([ABCDEFGIJKLMPSTXZHf])')

    def loop(self, _):
        while rs := select( [self._inout], [], [])[0]:
            TTkLog.debug(f"Select - {rs=}")
            for r in rs:
                if r is self._inout:
                    try:
                        out = self._inout.read(10240)
                    except Exception as e:
                        TTkLog.error(f"Error: {e=}")
                        return
                    out = out.decode('utf-8','ignore')
                    for bi, bout in enumerate(out.split('\a')): # grab the bells
                        # TTkLog.debug(f'Eugenio->{out}')
                        # sout = bout.decode('utf-8','ignore')
                        if bi:
                            TTkLog.debug("BELL!!! 🔔🔔🔔")
                        sout = bout.split('\033[')
                        self._screen_current.pushLine(sout[0])
                        TTkLog.debug(f"{sout[0]=}")
                        for slice in sout[1:]:
                            if m := TTkTerminal.re_DEC_SET_RST.match(slice):
                                # l = len(m.group(0))
                                en = m.end()
                                ps = int(m.group(1))
                                sr = m.group(2)
                                if ps == 1049 and sr == 'l': # NORMAL SCREEN
                                    self._screen_current = self._screen_normal
                                elif ps == 1049 and sr == 'h': # ALT SCREEN
                                    self._screen_current = self._screen_alt
                                elif ps == 2004:
                                    # Bracketedpaste ON
                                    # Bracketedpaste OFF
                                    pass
                                slice = slice[en:]
                            elif ( (m      := TTkTerminal.re_CURSOR.match(slice)) and
                                   (mg     := m.groups()) and
                                    mg[-1] == 'm' ):
                                TTkLog.debug(f"Handle color {mg[0]=}")
                                en = m.end()

                                color=TTkColor.RST

                                if mg[0] != '0m':
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

                                TTkLog.debug(TTkString(f"color - <ESC>[{mg[0]}",color).toAnsi())

                                slice = slice[en:]
                            elif m:
                                en = m.end()
                                y  = ps = int(y) if (y:=m.group(1)) else 1
                                sep = m.group(2)
                                x =       int(x) if (x:=m.group(3)) else 1
                                fn = m.group(4)
                                TTkLog.debug(f"ps:{y=} {sep=} {x=} {fn=}")
                                _ex = self._screen_current._CSI_MAP.get(
                                        fn,
                                        lambda a,b,c: TTkLog.warn(f"Unhandled <ESC> {y=} {sep=} {x=} {fn=}"))
                                _ex(self._screen_current,y,x)
                                slice = slice[en:]
                            else:
                                slice = '\033[' + slice.replace('\r','')

                            # TTkLog.debug(f'Eugenio->{slice}')
                            self._screen_current.pushLine(slice)
                            slice = slice.replace('\033','<ESC>').replace('\n','\\n')
                            TTkLog.debug(f"{slice=}")
                        self.update()
                        self.setWidgetCursor(pos=self._screen_current.getCursor())
                        TTkLog.debug(f"wc:{self._screen_current.getCursor()}")

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
