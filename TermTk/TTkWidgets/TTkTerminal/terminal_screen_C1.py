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

# Note:
# This Class is supposed to be inherited by and only by
# terminal_screen.py : _TTkTerminalScreen
# Due to the huge amount of Escape commands required to be handled
# I decided to split tham in multiple files
class _TTkTerminalScreen_C1():
    # C1 (8-Bit) Control Characters
    #
    # The xterm program recognizes both 8-bit and 7-bit control characters.
    # It generates 7-bit controls (by default) or 8-bit if S8C1T is enabled.
    # The following pairs of 7-bit and 8-bit control characters are
    # equivalent:
    #
    # ESC D
    #      Index (IND  is 0x84).
    #      Move the cursor down and scroll at the edge
    def _C1_D(self):
        x,y = self._terminalCursor
        t,b = self._scrollingRegion
        h = self._h
        if y < b-1:
            self._terminalCursor = (x,y+1)
        else:
            self._CSI_S_SU(1)

    # ESC E
    #      Next Line (NEL  is 0x85).
    #
    # ESC H
    #      Tab Set (HTS  is 0x88).
    #
    # ESC M
    #      Reverse Index (RI  is 0x8d).
    #      Move the cursor Up and scroll at the edge
    def _C1_M(self):
        x,y = self._terminalCursor
        t,b = self._scrollingRegion
        h = self._h
        if y > t:
            self._terminalCursor = (x,y-1)
        else:
            self._CSI_T_SD(1)

    # ESC N
    #      Single Shift Select of G2 Character Set (SS2  is 0x8e), VT220.
    #      This affects next character only.
    #
    # ESC O
    #      Single Shift Select of G3 Character Set (SS3  is 0x8f), VT220.
    #      This affects next character only.
    #
    # ESC P
    #      Device Control String (DCS  is 0x90).
    #
    # ESC V
    #      Start of Guarded Area (SPA  is 0x96).
    #
    # ESC W
    #      End of Guarded Area (EPA  is 0x97).
    #
    # ESC X
    #      Start of String (SOS  is 0x98).
    #
    # ESC Z
    #      Return Terminal ID (DECID is 0x9a).  Obsolete form of CSI c  (DA).
    #
    # ESC [
    #      Control Sequence Introducer (CSI  is 0x9b).
    #
    # ESC \
    #      String Terminator (ST  is 0x9c).
    #
    # ESC ]
    #      Operating System Command (OSC  is 0x9d).
    #
    # ESC ^
    #      Privacy Message (PM  is 0x9e).
    #
    # ESC _
    #      Application Program Command (APC  is 0x9f).
    #
    #
    # These control characters are used in the vtXXX emulation.
    _C1_MAP = {
        'D' : _C1_D,
        'M' : _C1_M
    }
