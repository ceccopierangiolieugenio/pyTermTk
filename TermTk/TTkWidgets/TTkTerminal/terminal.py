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

from dataclasses import dataclass

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
from TermTk.TTkWidgets.TTkTerminal.mode            import TTkTerminalModes

from TermTk.TTkWidgets.TTkTerminal.vt102 import TTkVT102

from TermTk.TTkCore.TTkTerm.colors import TTkTermColor
from TermTk.TTkCore.TTkTerm.colors_ansi_map import ansiMap16, ansiMap256

__all__ = ['TTkTerminal']

class TTkTerminal(TTkWidget):
    @dataclass
    class _Terminal():
        bracketedMode: bool = False
        DCSstring: str = ""
        IRM: bool = False

    @dataclass
    class _Keyboard():
        flags: int = 0

    @dataclass
    class _Mouse():
        reportPress: bool = False
        reportDrag:  bool = False
        reportMove:  bool = False
        sgrMode:     bool = False

    __slots__ = ('_shell', '_fd', '_inout', '_proc', '_quit_pipe', '_mode_normal'
                 '_clipboard',
                 '_buffer_lines', '_buffer_screen',
                 '_keyboard', '_mouse', '_terminal',
                 '_screen_current', '_screen_normal', '_screen_alt')
    def __init__(self, *args, **kwargs):
        self._shell = os.environ.get('SHELL', 'sh')
        self._fd = None
        self._proc = None
        self._mode_normal = True
        self._quit_pipe = None
        self._terminal = TTkTerminal._Terminal()
        self._keyboard = TTkTerminal._Keyboard()
        self._mouse = TTkTerminal._Mouse()
        self._buffer_lines = [TTkString()]
        # self._screen_normal  = _TTkTerminalNormalScreen()
        self._screen_normal  = _TTkTerminalAltScreen()
        self._screen_alt     = _TTkTerminalAltScreen()
        self._screen_current = self._screen_normal
        self._clipboard = TTkClipboard()

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
        TTkLog.info(f"Resize Terminal: {w=} {h=}")
        return super().resizeEvent(w, h)

    def runShell(self, program=None):
        self._shell = program if program else self._shell

        pid, self._fd = pty.fork()

        if pid == 0:
            def _spawnTerminal(argv=[self._shell], env=os.environ):
                os.execvpe(argv[0], argv, env)
            threading.Thread(target=_spawnTerminal).start()
            TTkHelper.quit()
            import sys
            sys.exit()
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
            w,h = self.size()
            self.resizeEvent(w,h)

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

    re_DEC_SET_RST  = re.compile('^\[(\??)(\d+)([lh])')
    # re_CURSOR_1    = re.compile(r'^(\d+)([ABCDEFGIJKLMPSTXZHf])')

    @pyTTkSlot()
    def _quit(self):
        if self._quit_pipe:
            os.write(self._quit_pipe[1], b'quit')

    def _inputGenerator(self):
        while rs := select( [self._inout,self._quit_pipe[0]], [], [])[0]:
            if self._quit_pipe[0] in rs:
                return

            # TTkLog.debug(f"Select - {rs=}")
            for r in rs:
                if r is not self._inout:
                    continue

                try:
                    _fl = fcntl.fcntl(self._inout, fcntl.F_GETFL)
                    fcntl.fcntl(self._inout, fcntl.F_SETFL, _fl | os.O_NONBLOCK) # Set the input as NONBLOCK to read the full sequence
                    out = b""
                    while _out := self._inout.read():
                        out += _out
                    fcntl.fcntl(self._inout, fcntl.F_SETFL, _fl)
                except Exception as e:
                    TTkLog.error(f"Error: {e=}")
                    return

                # out = out.decode('utf-8','ignore')
                try:
                    out = out.decode()
                except Exception as e:
                    TTkLog.error(f"{e=}")
                    TTkLog.error(f"Failed to decode {out}")
                    out = out.decode('utf-8','ignore')

                yield out

    def loop(self, _):
        inputgenerator = self._inputGenerator()
        for out in inputgenerator:
            sout = out.split('\033')
            TTkLog.debug(f"{sout[0]=}")

            # The first element is not an escaped sequence
            if sout[0]:
                self._screen_current.pushLine(sout[0],irm=self._terminal.IRM)

            escapeGenerator = (i for i in sout[1:])
            for slice in escapeGenerator:
                ssss = slice.replace('\033','<ESC>').replace('\n','\\n').replace('\r','\\r')
                TTkLog.debug(f"slice: {ssss}")

                ################################################
                # CSI Modes
                #   CSI Pm h
                #       Set Mode (SM).
                #   CSI Pm l
                #       Reset Mode (RM).
                #   CSI ? Pm h
                #      DEC Private Mode Set (DECSET).
                #   CSI ? Pm l
                #      DEC Private Mode Reset (DECRST).
                ################################################
                if m := TTkTerminal.re_DEC_SET_RST.match(slice):
                    en = m.end()
                    qm = m.group(1) == '?'
                    ps = int(m.group(2))
                    sr = (m.group(3) == 'h')
                    if qm:
                        self._CSI_DEC_SET_RST(ps,sr)
                    else:
                        self._CSI_SM_RM(ps,sr)
                    slice = slice[en:]

                ################################################
                # CSI Color Functions
                #   CSI Pm ; Pm ; ... m
                ################################################
                elif ((m      := TTkTerminal.re_CURSOR.match(slice)) and
                      (mg     := m.groups()) and
                       mg[-1] == 'm' ):
                    # TTkLog.debug(f"Handle color {mg[0]=}")
                    en = m.end()

                    color=TTkColor.RST

                    if mg[0] not in ['0','']:
                        values = mg[0].split(';')
                        color = self._screen_current.color()
                        fg = color._fg
                        bg = color._bg
                        mod = color._mod
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
                            elif s==1: mod |= TTkTermColor.BOLD
                            elif s==3: mod |= TTkTermColor.ITALIC
                            elif s==4: mod |= TTkTermColor.UNDERLINE
                            elif s==9: mod |= TTkTermColor.STRIKETROUGH
                            elif s==5: mod |= TTkTermColor.BLINKING
                            elif s==7: mod |= TTkTermColor.REVERSED
                        color = TTkColor(fg=fg, bg=bg, mod=mod, clean=clean)

                    self._screen_alt.setColor(color)
                    self._screen_normal.setColor(color)

                    # TTkLog.debug(TTkString(f"color - <ESC>[{mg[0]}",color).toAnsi())
                    slice = slice[en:]

                ################################################
                # CSI Common Functions
                #   CSI Pm ; Pm ; ... X
                ################################################
                elif m:
                    en = m.end()
                    fn = m.group(5)
                    defval = self._CSI_Default_MAP.get(fn,(1,1))
                    y  = ps = int(y) if (y:=m.group(2)) else defval[0]
                    sep = m.group(3)
                    x =       int(x) if (x:=m.group(4)) else defval[1]
                    TTkLog.debug(f"{mg[0]}{fn} = ps:{y=} {sep=} {x=} {fn=}")
                    if fn in ['n']:
                        # Handle the non screen related functions
                        _ex = self._CSI_MAP.get(
                                fn,
                                lambda a,b,c: TTkLog.error(f"Unhandled <ESC>[{mg[0]}{fn} = ps:{y=} {sep=} {x=} {fn=}"))
                        _ex(self,y,x)
                    else:
                        # Handle the screen related functions
                        _ex = self._screen_current._CSI_MAP.get(
                                fn,
                                lambda a,b,c: TTkLog.error(f"Unhandled <ESC>[{mg[0]}{fn} = ps:{y=} {sep=} {x=} {fn=}"))
                        _ex(self._screen_current,y,x)
                    slice = slice[en:]

                ################################################
                # ESC =     Application Keypad (DECKPAM).
                ################################################
                elif slice and slice[0] in ['=','>']:
                    # ESC =     Application Keypad (DECKPAM).
                    if slice[0] == '=':
                        self._keyboard.flags |= TTkTerminalModes.MODE_DECKPAM
                        TTkLog.warn("Unhandled <ESC> = (DECKPAM)")
                    # ESC >     Normal Keypad (DECKPNM), VT100.
                    elif slice[0] == '>':
                        self._keyboard.flags &= ~TTkTerminalModes.MODE_DECKPAM
                        TTkLog.warn("Unhandled <ESC> > (DECKPNM)")
                    slice = slice[1:]

                ################################################
                # ESC P
                #   Device Control String (DCS  is 0x90).
                # ESC \
                #   String Terminator (ST  is 0x9c).
                #
                #   ESC P Pt ESC \
                #     Device Control String (DCS) xterm implements no DCS functions; Pt is ignored. Pt need not be printable characters.
                #
                # NOTE:
                #    DCS is an escape sequence that does not happen often
                #    So far I saw it only during vim initialization and
                #    only to check if the TERM=screen is capable to handle DCS
                #    I try to keep everything related in a self contained place
                ################################################
                elif slice and slice[0] == 'P':
                    # Sarting DCS (ESC P) and wait for ST (ESC \)
                    self._terminal.DCSstring = slice[1:]
                    slice = ""

                    # I am using a closure in order to exit the routine at the end
                    def __processDCSEscapeGenerator():
                        for dcs in escapeGenerator:
                            if dcs[0] == '\\':
                                TTkLog.warn(f"DCS: {self._terminal.DCSstring} - Not Handled")
                                self._terminal.DCSstring = ""
                                return True, dcs[1:]
                            self._terminal.DCSstring += dcs
                        return False, ""

                    def __processDCSInputGenerator(slice):
                        # If the terminator is not in the current escaped slices
                        # I need to fetch from the input until I got all of them
                        # This is not the nicest thing but it save a bunch of extra
                        # hcecks at any input just to find if we are in DCS mode or not
                        for out in inputgenerator:
                            sout = out.split('\033')
                            self._terminal.DCSstring += sout[0]
                            escapeGenerator = (i for i in sout[1:])
                            ret, slice =  __processDCSEscapeGenerator()
                            if not ret:
                                return escapeGenerator, slice

                    ret, slice =  __processDCSEscapeGenerator()

                    if not ret:
                        escapeGenerator, slice = __processDCSInputGenerator()

                    if not slice:
                        continue

                ################################################
                # Everything else
                ################################################
                else:
                    TTkLog.warn(f"Unhandled Slice:'<ESC>{slice}'".replace('\n','\\n'))
                    continue

                self._screen_current.pushLine(slice,irm=self._terminal.IRM)

            self.update()
            self.setWidgetCursor(pos=self._screen_current.getCursor())
            TTkLog.debug(f"wc:{self._screen_current.getCursor()} {self._proc=}")

    def pasteEvent(self, txt:str):
        if self._terminal.bracketedMode:
            txt = "\033[200~"+txt+"\033[201~"
        self._inout.write(txt.encode())
        return True

    def keyEvent(self, evt):
        # TTkLog.debug(f"Key: {evt.code=}")
        TTkLog.debug(f"Key: {str(evt)=}")
        if evt.type == TTkK.SpecialKey:
            if evt.mod == TTkK.ControlModifier and evt.key == TTkK.Key_V:
                txt = self._clipboard.text()
                self.pasteEvent(str(txt))
                return True
            if self._keyboard.flags & TTkTerminalModes.MODE_DECCKM:
                if code := {TTkK.Key_Up:    b"\033OA",
                            TTkK.Key_Down:  b"\033OB",
                            TTkK.Key_Right: b"\033OC",
                            TTkK.Key_Left:  b"\033OD"}.get(evt.key):
                    self._inout.write(code)
                    return True
            if evt.key == TTkK.Key_Enter:
                TTkLog.debug(f"Key: Enter")
                # self._inout.write(b'\n')
                # self._inout.write(evt.code.encode())
        else: # Input char
            TTkLog.debug(f"Key: {evt.key=}")
            # self._inout.write(evt.key.encode())
        self._inout.write(evt.code.encode())
        return True

    # Extended coordinates
    # The original X10 mouse protocol limits the Cx and Cy ordinates to 223
    # (=255 - 32).  XTerm supports more than one scheme for extending this
    # range, by changing the protocol encoding:
    #
    # UTF-8 (1005)
    #           This enables UTF-8 encoding for Cx and Cy under all tracking
    #           modes, expanding the maximum encodable position from 223 to
    #           2015.  For positions less than 95, the resulting output is
    #           identical under both modes.  Under extended mouse mode,
    #           positions greater than 95 generate "extra" bytes which will
    #           confuse applications which do not treat their input as a UTF-8
    #           stream.  Likewise, Cb will be UTF-8 encoded, to reduce
    #           confusion with wheel mouse events.
    #
    #           Under normal mouse mode, positions outside (160,94) result in
    #           byte pairs which can be interpreted as a single UTF-8
    #           character; applications which do treat their input as UTF-8
    #           will almost certainly be confused unless extended mouse mode
    #           is active.
    #
    #           This scheme has the drawback that the encoded coordinates will
    #           not pass through luit(1) unchanged, e.g., for locales using
    #           non-UTF-8 encoding.
    #
    # SGR (1006)
    #           The normal mouse response is altered to use
    #
    #           o   CSI < followed by semicolon-separated
    #
    #           o   encoded button value,
    #
    #           o   Px and Py ordinates and
    #
    #           o   a final character which is M  for button press and m  for
    #               button release.
    #
    #           The encoded button value in this case does not add 32 since
    #           that was useful only in the X10 scheme for ensuring that the
    #           byte containing the button value is a printable code.
    #
    #           o   The modifiers are encoded in the same way.
    #
    #           o   A different final character is used for button release to
    #               resolve the X10 ambiguity regarding which button was
    #               released.
    #
    #           The highlight tracking responses are also modified to an SGR-
    #           like format, using the same SGR-style scheme and button-
    #           encodings.
    #
    # URXVT (1015)
    #           The normal mouse response is altered to use
    #
    #           o   CSI followed by semicolon-separated
    #
    #           o   encoded button value,
    #
    #           o   the Px and Py ordinates and final character M .
    #
    #           This uses the same button encoding as X10, but printing it as
    #           a decimal integer rather than as a single byte.
    #
    #           However, CSI M  can be mistaken for DL (delete lines), while
    #           the highlight tracking CSI T  can be mistaken for SD (scroll
    #           down), and the Window manipulation controls.  For these
    #           reasons, the 1015 control is not recommended; it is not an
    #           improvement over 1006.
    #
    # SGR-Pixels (1016)
    #           Use the same mouse response format as the 1006 control, but
    #           report position in pixels rather than character cells.

    def _sendMouse(self, evt):
        if   not self._mouse.reportPress:
            return True
        if ( not self._mouse.reportDrag and
            evt.evt in (TTkK.Drag, TTkK.Move)):
            return True

        x,y = evt.x+1, evt.y+1
        if self._mouse.sgrMode:
            k = {
                TTkK.NoButton     : 3,
                TTkK.AllButtons   : 0,
                TTkK.LeftButton   : 0,
                TTkK.RightButton  : 2,
                TTkK.MidButton    : 1,
                TTkK.MiddleButton : 1,
                TTkK.Wheel        : 64,
            }.get(evt.key, 0)

            km,pr = {
                TTkK.Press:     ( 0,'M'),
                TTkK.Release:   ( 0,'m'),
                TTkK.Move:      ( 0,'M'),
                TTkK.Drag:      (32,'M'),
                TTkK.WHEEL_Up:  ( 0,'M'),
                TTkK.WHEEL_Down:( 1,'M')}.get(
                    evt.evt,(0,'M'))

            self._inout.write(f'\033[<{k+km};{x};{y}{pr}'.encode())
        else:
            head = {
                TTkK.Press:     b'\033[M ',
                TTkK.Release:   b'\033[M#',
                # TTkK.Move:      b'\033[M@',
                TTkK.Drag:      b'\033[M@',
                TTkK.WHEEL_Up:  b'\033[M`',
                TTkK.WHEEL_Down:b'\033[Ma'}.get(
                    evt.evt,
                    b'')
            bah = bytearray(head)
            bah.append((x+32)%0xff)
            bah.append((y+32)%0xff)
            self._inout.write(bah)
        return True

    def mousePressEvent(self, evt):   return self._sendMouse(evt)
    def mouseReleaseEvent(self, evt): return self._sendMouse(evt)
    def mouseDragEvent(self, evt):    return self._sendMouse(evt)
    def mouseMoveEvent(self, evt):    return self._sendMouse(evt)
    def wheelEvent(self, evt):        return self._sendMouse(evt)
    def mouseTapEvent(self, evt):     return self._sendMouse(evt)
    def mouseDoubleClickEvent(self, evt): return self._sendMouse(evt)

    def paintEvent(self, canvas: TTkCanvas):
        w,h = self.size()
        self._screen_current.paintEvent(canvas,w,h)



    # This map include the default values in case Ps or Row/Col are empty
    # Since almost all the CSI use 1 as default, I am including here only
    # the ones that are different
    _CSI_Default_MAP = {
        'J' : (0,None),
        'K' : (0,None)
    }


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

    # CSI Pm h  Set Mode (SM).
    #             Ps = 2  ⇒  Keyboard Action Mode (KAM).
    #             Ps = 4  ⇒  Insert Mode (IRM).
    #             Ps = 1 2  ⇒  Send/receive (SRM).
    #             Ps = 2 0  ⇒  Automatic Newline (LNM).
    #             Ps = 3 4  ⇒  Normal Cursor Visibility
    # CSI Pm l  Reset Mode (RM).
    #             Ps = 2  ⇒  Keyboard Action Mode (KAM).
    #             Ps = 4  ⇒  Replace Mode (IRM).
    #             Ps = 1 2  ⇒  Send/receive (SRM).
    #             Ps = 2 0  ⇒  Normal Linefeed (LNM).
    #             Ps = 3 4  ⇒  Normal Cursor Visibility
    def _CSI_SM_RM(self, ps, s):
        if ps == 4: # Insert/Replace Mode
            self._terminal.IRM = s
        elif ps == 34:
            TTkLog.warn(f"Unhandled (SM) <ESC>{ps}{'h' if s else 'l'} Normal Cursor Visibility")
        else:
            TTkLog.error(f"Unhandled (SM) <ESC>{ps}{'h' if s else 'l'}")

    def _CSI_DEC_SET_RST(self, ps, s):
        _dec = self._CSI_DEC_SET_RST_MAP.get(
                ps,
                lambda a,b: TTkLog.error(f"Unhandled (DEC) <ESC>[{ps}{'h' if s else 'l'}"))
        _dec(self, s)



    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1  ⇒  Application Cursor Keys (MODE_DECCKM), VT100.
    #                UP    = \0330A
    #                DOWN  = \0330B
    #                LEFT  = \0330C
    #                RIGHT = \0330D
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1  ⇒  Normal Cursor Keys (MODE_DECCKM), VT100.
    #                UP    = \033[A
    #                DOWN  = \033[B
    #                LEFT  = \033[C
    #                RIGHT = \033[D
    def _CSI_DEC_SR_1_MODE_DECCKM(self, s):
        if s:
            self._keyboard.flags |= TTkTerminalModes.MODE_DECCKM
        else:
            self._keyboard.flags &= ~TTkTerminalModes.MODE_DECCKM

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 2 5  ⇒  Show cursor (DECTCEM), VT220.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 2 5  ⇒  Hide cursor (DECTCEM), VT220.
    def _CSI_DEC_SR_25_DECTCEM(self, s):
        self.enableWidgetCursor(enable=s)

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1 0 0 0  ⇒  Send Mouse X & Y on button press and
    #           release.  See the section Mouse Tracking.  This is the X11
    #           xterm mouse protocol.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1 0 0 0  ⇒  Don't send Mouse X & Y on button press and
    #           release.  See the section Mouse Tracking.
    def _CSI_DEC_SR_1000(self, s):
        self._mouse.reportPress = s
        self._mouse.reportDrag  = False
        self._mouse.reportMove  = False
        TTkLog.info(f"1002 Mouse Tracking {s=}")

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1 0 0 2  ⇒  Use Cell Motion Mouse Tracking, xterm.  See
    #           the section Button-event tracking.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1 0 0 2  ⇒  Don't use Cell Motion Mouse Tracking,
    #           xterm.  See the section Button-event tracking.
    def _CSI_DEC_SR_1002(self, s):
        self._mouse.reportPress = s
        self._mouse.reportDrag  = s
        self._mouse.reportMove  = False
        TTkLog.info(f"1002 Mouse Tracking {s=}")

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1 0 0 6  ⇒  Enable SGR Mouse Mode, xterm.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1 0 0 6  ⇒  Disable SGR Mouse Mode, xterm.
    def _CSI_DEC_SR_1006(self, s):
        self._mouse.sgrMode = s
        TTkLog.info(f"1006 SGR Mouse Mode {s=}")

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1 0 1 5  ⇒  Enable urxvt Mouse Mode.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1 0 1 5  ⇒  Disable urxvt Mouse Mode.
    def _CSI_DEC_SR_1015(self, s):
        TTkLog.warn(f"1015 {s=} Unimplemented: _CSI_DEC_SR_1015 urxvt Mouse Mode.")

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1 0 4 7  ⇒  Use Alternate Screen Buffer, xterm.  This
    #           may be disabled by the titeInhibit resource.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1 0 4 7  ⇒  Use Normal Screen Buffer, xterm.  Clear the
    #           screen first if in the Alternate Screen Buffer.  This may be
    #           disabled by the titeInhibit resource.
    def _CSI_DEC_SR_1047(self, s):
        if s:
            self._screen_current = self._screen_alt
        else:
            self._screen_current = self._screen_normal

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1 0 4 8  ⇒  Save cursor as in DECSC, xterm.  This may
    #           be disabled by the titeInhibit resource.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1 0 4 8  ⇒  Restore cursor as in DECRC, xterm.  This
    #           may be disabled by the titeInhibit resource.
    def _CSI_DEC_SR_1048(self, s):
            pass

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
        self._CSI_DEC_SR_1047(s)
        self._CSI_DEC_SR_1048(s)

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 2 0 0 4  ⇒  Set bracketed paste mode, xterm.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 2 0 0 4  ⇒  Reset bracketed paste mode, xterm.
    def _CSI_DEC_SR_2004(self, s):
        self._terminal.bracketedMode = s

    _CSI_DEC_SET_RST_MAP = {
        1   : _CSI_DEC_SR_1_MODE_DECCKM,
        25  : _CSI_DEC_SR_25_DECTCEM,
        1000: _CSI_DEC_SR_1000,
        1002: _CSI_DEC_SR_1002,
        1006: _CSI_DEC_SR_1006,
        1015: _CSI_DEC_SR_1015,
        1047: _CSI_DEC_SR_1047,
        1049: _CSI_DEC_SR_1049,
        2004: _CSI_DEC_SR_2004
    }