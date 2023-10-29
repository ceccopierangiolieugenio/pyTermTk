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

__all__ = []

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkWidgets.TTkTerminal.mode            import TTkTerminalModes

class _termLog():
    # debug = TTkLog.debug
    # info  = TTkLog.info
    error = TTkLog.error
    warn  = TTkLog.warn
    fatal = TTkLog.fatal
    # mouse = TTkLog.error

    debug = lambda _:None
    info  = lambda _:None
    # error = lambda _:None
    # warn  = lambda _:None
    # fatal = lambda _:None
    mouse = lambda _:None

# Note:
# This Class is supposed to be inherited by and only by
# terminal.py : TTkTerminal
# Due to the huge amount of Escape commands required to be handled
# I decided to split tham in multiple files
class _TTkTerminal_CSI_DEC():
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
        _termLog.info(f"1000 Mouse Tracking {s=}")

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
        _termLog.info(f"1002 Mouse Tracking {s=}")

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1 0 0 3  ⇒  Use All Motion Mouse Tracking, xterm.  See
    #           the section Any-event tracking.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1 0 0 3  ⇒  Don't use All Motion Mouse Tracking, xterm.
    #           See the section Any-event tracking.
    def _CSI_DEC_SR_1003(self, s):
        self._mouse.reportPress = s
        self._mouse.reportDrag  = s
        self._mouse.reportMove  = s
        _termLog.info(f"1003 Mouse Tracking {s=}")

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1 0 0 4  ⇒  Send FocusIn/FocusOut events, xterm.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1 0 0 4  ⇒  Don't send FocusIn/FocusOut events, xterm.
    def _CSI_DEC_SR_1004(self, s):
        _termLog.warn(f"Unhandled 1004 Focus In/Out event {s=}")


    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1 0 0 6  ⇒  Enable SGR Mouse Mode, xterm.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1 0 0 6  ⇒  Disable SGR Mouse Mode, xterm.
    def _CSI_DEC_SR_1006(self, s):
        self._mouse.sgrMode = s
        _termLog.info(f"1006 SGR Mouse Mode {s=}")

    # CSI ? Pm h
    #           DEC Private Mode Set (DECSET).
    #             Ps = 1 0 1 5  ⇒  Enable urxvt Mouse Mode.
    # CSI ? Pm l
    #           DEC Private Mode Reset (DECRST).
    #             Ps = 1 0 1 5  ⇒  Disable urxvt Mouse Mode.
    def _CSI_DEC_SR_1015(self, s):
        _termLog.warn(f"1015 {s=} Unimplemented: _CSI_DEC_SR_1015 urxvt Mouse Mode.")

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
        self._screen_current.resize(*(self.size()))
        self._screenChanged()

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
        1003: _CSI_DEC_SR_1003,
        1004: _CSI_DEC_SR_1004,
        1006: _CSI_DEC_SR_1006,
        1015: _CSI_DEC_SR_1015,
        1047: _CSI_DEC_SR_1047,
        1049: _CSI_DEC_SR_1049,
        2004: _CSI_DEC_SR_2004
    }