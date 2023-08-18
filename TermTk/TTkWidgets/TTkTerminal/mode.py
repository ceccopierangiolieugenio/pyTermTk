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

class TTkTerminalModes(int):
    # define masks for keyboard flags
    MODE_KAM     = 0x01 # mode 2: keyboard action mode
    MODE_DECKPAM = 0x02 # keypad application mode
    MODE_DECCKM  = 0x04 # private mode 1: cursor keys
    MODE_SRM     = 0x08 # mode 12: send-receive mode
    MODE_DECBKM  = 0x10 # private mode 67: backarrow
    MODE_DECSDM  = 0x20 # private mode 80: sixel DISPLAY mode -- note, when SDM is off, the terminal is in sixel SCROLLING mode

    #             Ps = 1  ⇒  Application Cursor Keys (DECCKM), VT100.
    #             Ps = 1  ⇒  Normal Cursor Keys (DECCKM), VT100.

    #             Ps = 2  ⇒  Designate VT52 mode (DECANM), VT100.
    #             Ps = 3  ⇒  80 Column Mode (DECCOLM), VT100.
    #             Ps = 4  ⇒  Jump (Fast) Scroll (DECSCLM), VT100.
    #             Ps = 5  ⇒  Normal Video (DECSCNM), VT100.
    #             Ps = 6  ⇒  Normal Cursor Mode (DECOM), VT100.
    #             Ps = 7  ⇒  No Auto-Wrap Mode (DECAWM), VT100.
    #             Ps = 8  ⇒  No Auto-Repeat Keys (DECARM), VT100.
    #             Ps = 9  ⇒  Don't send Mouse X & Y on button press, xterm.
    #             Ps = 1 0  ⇒  Hide toolbar (rxvt).
    #             Ps = 1 2  ⇒  Stop blinking cursor (AT&T 610).
    #             Ps = 1 3  ⇒  Disable blinking cursor (reset only via
    #           resource or menu).
    #             Ps = 1 4  ⇒  Disable XOR of blinking cursor control sequence
    #           and menu.
    #             Ps = 1 8  ⇒  Don't Print Form Feed (DECPFF), VT220.
    #             Ps = 1 9  ⇒  Limit print to scrolling region (DECPEX),
    #           VT220.
    #             Ps = 2 5  ⇒  Hide cursor (DECTCEM), VT220.
    #             Ps = 3 0  ⇒  Don't show scrollbar (rxvt).
    #             Ps = 3 5  ⇒  Disable font-shifting functions (rxvt).
    #             Ps = 4 0  ⇒  Disallow 80 ⇒  132 mode, xterm.
    #             Ps = 4 1  ⇒  No more(1) fix (see curses resource).
    #             Ps = 4 2  ⇒  Disable National Replacement Character sets
    #           (DECNRCM), VT220.
    #             Ps = 4 3  ⇒  Disable Graphic Expanded Print Mode (DECGEPM),
    #           VT340.
    #             Ps = 4 4  ⇒  Turn off margin bell, xterm.
    #             Ps = 4 4  ⇒  Disable Graphic Print Color Mode (DECGPCM),
    #           VT340.
    #             Ps = 4 5  ⇒  No Reverse-wraparound mode (XTREVWRAP), xterm.
    #             Ps = 4 5  ⇒  Disable Graphic Print Color Syntax (DECGPCS),
    #           VT340.
    #             Ps = 4 6  ⇒  Stop logging (XTLOGGING), xterm.  This is
    #           normally disabled by a compile-time option.
    #             Ps = 4 7  ⇒  Use Normal Screen Buffer, xterm.
    #             Ps = 4 7  ⇒  Disable Graphic Rotated Print Mode (DECGRPM),
    #           VT340.
    #             Ps = 6 6  ⇒  Numeric keypad mode (DECNKM), VT320.
    #             Ps = 6 7  ⇒  Backarrow key sends delete (DECBKM), VT340,
    #           VT420.  This sets the backarrowKey resource to "false".
    #             Ps = 6 9  ⇒  Disable left and right margin mode (DECLRMM),
    #           VT420 and up.
    #             Ps = 8 0  ⇒  Disable Sixel Display Mode (DECSDM), VT330,
    #           VT340, VT382.  Turns on "Sixel Scrolling".  See the section
    #           Sixel Graphics and mode 8 4 5 2 .
    #             Ps = 9 5  ⇒  Clear screen when DECCOLM is set/reset
    #           (DECNCSM), VT510 and up.
    #             Ps = 1 0 0 0  ⇒  Don't send Mouse X & Y on button press and
    #           release.  See the section Mouse Tracking.
    #             Ps = 1 0 0 1  ⇒  Don't use Hilite Mouse Tracking, xterm.
    #             Ps = 1 0 0 2  ⇒  Don't use Cell Motion Mouse Tracking,
    #           xterm.  See the section Button-event tracking.
    #             Ps = 1 0 0 3  ⇒  Don't use All Motion Mouse Tracking, xterm.
    #           See the section Any-event tracking.
    #             Ps = 1 0 0 4  ⇒  Don't send FocusIn/FocusOut events, xterm.
    #             Ps = 1 0 0 5  ⇒  Disable UTF-8 Mouse Mode, xterm.
    #             Ps = 1 0 0 6  ⇒  Disable SGR Mouse Mode, xterm.
    #             Ps = 1 0 0 7  ⇒  Disable Alternate Scroll Mode, xterm.  This
    #           corresponds to the alternateScroll resource.
    #             Ps = 1 0 1 0  ⇒  Don't scroll to bottom on tty output
    #           (rxvt).  This sets the scrollTtyOutput resource to "false".
    #             Ps = 1 0 1 1  ⇒  Don't scroll to bottom on key press (rxvt).
    #           This sets the scrollKey resource to "false".
    #             Ps = 1 0 1 5  ⇒  Disable urxvt Mouse Mode.
    #             Ps = 1 0 1 6  ⇒  Disable SGR Mouse Pixel-Mode, xterm.
    #             Ps = 1 0 3 4  ⇒  Don't interpret "meta" key, xterm.  This
    #           disables the eightBitInput resource.
    #             Ps = 1 0 3 5  ⇒  Disable special modifiers for Alt and
    #           NumLock keys, xterm.  This disables the numLock resource.
    #             Ps = 1 0 3 6  ⇒  Don't send ESC  when Meta modifies a key,
    #           xterm.  This disables the metaSendsEscape resource.
    #             Ps = 1 0 3 7  ⇒  Send VT220 Remove from the editing-keypad
    #           Delete key, xterm.
    #             Ps = 1 0 3 9  ⇒  Don't send ESC when Alt modifies a key,
    #           xterm.  This disables the altSendsEscape resource.
    #             Ps = 1 0 4 0  ⇒  Do not keep selection when not highlighted,
    #           xterm.  This disables the keepSelection resource.
    #             Ps = 1 0 4 1  ⇒  Use the PRIMARY selection, xterm.  This
    #           disables the selectToClipboard resource.
    #             Ps = 1 0 4 2  ⇒  Disable Urgency window manager hint when
    #           Control-G is received, xterm.  This disables the bellIsUrgent
    #           resource.
    #             Ps = 1 0 4 3  ⇒  Disable raising of the window when Control-
    #           G is received, xterm.  This disables the popOnBell resource.
    #             Ps = 1 0 4 5  ⇒  No Extended Reverse-wraparound mode
    #           (XTREVWRAP2), xterm.
    #             Ps = 1 0 4 6  ⇒  Disable switching to/from Alternate Screen
    #           Buffer, xterm.  This works for terminfo-based systems,
    #           updating the titeInhibit resource.  If currently using the
    #           Alternate Screen Buffer, xterm switches to the Normal Screen
    #           Buffer.
    #             Ps = 1 0 4 7  ⇒  Use Normal Screen Buffer, xterm.  Clear the
    #           screen first if in the Alternate Screen Buffer.  This may be
    #           disabled by the titeInhibit resource.
    #             Ps = 1 0 4 8  ⇒  Restore cursor as in DECRC, xterm.  This
    #           may be disabled by the titeInhibit resource.
    #             Ps = 1 0 4 9  ⇒  Use Normal Screen Buffer and restore cursor
    #           as in DECRC, xterm.  This may be disabled by the titeInhibit
    #           resource.  This combines the effects of the 1 0 4 7  and 1 0 4
    #           8  modes.  Use this with terminfo-based applications rather
    #           than the 4 7  mode.
    #             Ps = 1 0 5 0  ⇒  Reset terminfo/termcap function-key mode,
    #           xterm.
    #             Ps = 1 0 5 1  ⇒  Reset Sun function-key mode, xterm.
    #             Ps = 1 0 5 2  ⇒  Reset HP function-key mode, xterm.
    #             Ps = 1 0 5 3  ⇒  Reset SCO function-key mode, xterm.
    #             Ps = 1 0 6 0  ⇒  Reset legacy keyboard emulation, i.e,
    #           X11R6, xterm.
    #             Ps = 1 0 6 1  ⇒  Reset keyboard emulation to Sun/PC style,
    #           xterm.
    #             Ps = 2 0 0 1  ⇒  Disable readline mouse button-1, xterm.
    #             Ps = 2 0 0 2  ⇒  Disable readline mouse button-2, xterm.
    #             Ps = 2 0 0 3  ⇒  Disable readline mouse button-3, xterm.
    #             Ps = 2 0 0 4  ⇒  Reset bracketed paste mode, xterm.
    #             Ps = 2 0 0 5  ⇒  Disable readline character-quoting, xterm.
    #             Ps = 2 0 0 6  ⇒  Disable readline newline pasting, xterm.
