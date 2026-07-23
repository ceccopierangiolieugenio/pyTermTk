# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.TTkTerminal.terminal_screen import _TTkTerminalScreen
from TermTk.TTkWidgets.TTkTerminal.terminalview import TTkTerminalView
from TermTk.TTkWidgets.TTkTerminal.mode import TTkTerminalModes


def _get_screen_text(screen, row):
    data = screen._canvas._data[row]
    return ''.join(data).rstrip()


def _get_screen_row(screen, row):
    return ''.join(screen._canvas._data[row])


def _make_terminal_view(w=20, h=10):
    tv = TTkTerminalView.__new__(TTkTerminalView)
    from TermTk.TTkCore.signal import pyTTkSignal
    from TermTk.TTkCore.string import TTkString
    from TermTk.TTkGui.clipboard import TTkClipboard

    tv._bell = pyTTkSignal()
    tv._terminalClosed = pyTTkSignal()
    tv._titleChanged = pyTTkSignal(str)
    tv._textSelected = pyTTkSignal(TTkString)
    tv._termData = pyTTkSignal(bytes)
    tv._termResized = pyTTkSignal(int, int)
    tv._newSize = None
    tv._terminal = TTkTerminalView._Terminal()
    tv._keyboard = TTkTerminalView._Keyboard()
    tv._mouse = TTkTerminalView._Mouse()
    tv._buffer_lines = [TTkString()]
    tv._screen_normal = _TTkTerminalScreen(w=w, h=h)
    tv._screen_alt = _TTkTerminalScreen(w=w, h=h)
    tv._screen_current = tv._screen_normal
    tv._clipboard = TTkClipboard()
    tv._selecting = False

    tv._screen_normal.bell.connect(tv._bell.emit)
    tv._screen_alt.bell.connect(tv._bell.emit)

    tv._termLoop = tv._loopGenerator()
    next(tv._termLoop)
    tv._termLoop.send("")

    # Stub methods that depend on widget hierarchy
    tv._widgetCursorEnabled = True
    tv.enableWidgetCursor = lambda enable=True: setattr(tv, '_widgetCursorEnabled', enable)
    tv.size = lambda: (w, h)
    tv.viewMoveTo = lambda *a, **k: None
    tv.update = lambda *a, **k: None
    tv.setWidgetCursor = lambda *a, **k: None

    # Stub viewChanged signal
    class FakeSignal:
        def connect(self, *a): pass
        def emit(self, *a): pass
    tv.viewChanged = FakeSignal()
    tv._screen_normal.bufferedLinesChanged = FakeSignal()
    tv._screen_alt.bufferedLinesChanged = FakeSignal()

    return tv


class TestSGRColorParsing:
    '''Tests for SGR (CSI m) escape sequences parsed in the view loop.'''

    def setup_method(self):
        self.tv = _make_terminal_view(w=20, h=5)

    def test_sgr_reset(self):
        self.tv.termWrite("\033[1mBold\033[0mNormal")
        color_at_4 = self.tv._screen_current._canvas._colors[0][4]
        assert color_at_4 == TTkColor.RST

    def test_sgr_bold(self):
        self.tv.termWrite("\033[1mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        assert color.bold()

    def test_sgr_italic(self):
        self.tv.termWrite("\033[3mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        assert color.italic()

    def test_sgr_underline(self):
        self.tv.termWrite("\033[4mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        assert color.underline()

    def test_sgr_fg_ansi_16(self):
        self.tv.termWrite("\033[31mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        r, g, b = color.fgToRGB()
        assert r > 0 and g == 0 and b == 0

    def test_sgr_bg_ansi_16(self):
        self.tv.termWrite("\033[42mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        r, g, b = color.bgToRGB()
        assert g > 0

    def test_sgr_fg_256(self):
        self.tv.termWrite("\033[38;5;196mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        r, g, b = color.fgToRGB()
        assert r == 255 and g == 0 and b == 0

    def test_sgr_bg_256(self):
        self.tv.termWrite("\033[48;5;21mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        r, g, b = color.bgToRGB()
        assert b > 0

    def test_sgr_fg_24bit(self):
        self.tv.termWrite("\033[38;2;100;150;200mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        assert color.fgToRGB() == (100, 150, 200)

    def test_sgr_bg_24bit(self):
        self.tv.termWrite("\033[48;2;10;20;30mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        assert color.bgToRGB() == (10, 20, 30)

    def test_sgr_fg_default_39(self):
        self.tv.termWrite("\033[31mA\033[39mX")
        color_a = self.tv._screen_current._canvas._colors[0][0]
        color_x = self.tv._screen_current._canvas._colors[0][1]
        # 'A' should have red fg
        r, g, b = color_a.fgToRGB()
        assert r > 0 and g == 0 and b == 0
        # 'X' after SGR 39 should have default fg (same as RST)
        assert color_x == TTkColor.RST, \
            f"SGR 39 should produce a color equivalent to RST, got {color_x}"

    def test_sgr_bg_default_49(self):
        self.tv.termWrite("\033[42mA\033[49mX")
        color_a = self.tv._screen_current._canvas._colors[0][0]
        color_x = self.tv._screen_current._canvas._colors[0][1]
        # 'A' should have green bg
        r, g, b = color_a.bgToRGB()
        assert g > 0
        # 'X' after SGR 49 should have default bg (same as RST)
        assert color_x == TTkColor.RST, \
            f"SGR 49 should produce a color equivalent to RST, got {color_x}"

    def test_sgr_multiple_attrs_combined(self):
        self.tv.termWrite("\033[1;3;4mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        assert color.bold()
        assert color.italic()
        assert color.underline()

    def test_sgr_reset_bold_22(self):
        self.tv.termWrite("\033[1mA\033[22mB")
        color_b = self.tv._screen_current._canvas._colors[0][1]
        assert not color_b.bold()

    def test_sgr_reset_italic_23(self):
        self.tv.termWrite("\033[3mA\033[23mB")
        color_b = self.tv._screen_current._canvas._colors[0][1]
        assert not color_b.italic()

    def test_sgr_reset_underline_24(self):
        self.tv.termWrite("\033[4mA\033[24mB")
        color_b = self.tv._screen_current._canvas._colors[0][1]
        assert not color_b.underline()

    def test_sgr_bright_fg(self):
        self.tv.termWrite("\033[91mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        r, g, b = color.fgToRGB()
        assert r > 0

    def test_sgr_bright_bg(self):
        self.tv.termWrite("\033[101mX")
        color = self.tv._screen_current._canvas._colors[0][0]
        r, g, b = color.bgToRGB()
        assert r > 0

    def test_sgr_empty_is_reset(self):
        self.tv.termWrite("\033[1mA\033[mB")
        color_b = self.tv._screen_current._canvas._colors[0][1]
        assert color_b == TTkColor.RST


class TestDECModes:
    '''Tests for DEC private mode set/reset.'''

    def setup_method(self):
        self.tv = _make_terminal_view(w=20, h=5)

    def test_alternate_screen_buffer_switch(self):
        self.tv.termWrite("NormalText")
        assert _get_screen_text(self.tv._screen_normal, 0).startswith("NormalText")
        self.tv.termWrite("\033[?1047h")
        assert self.tv._screen_current is self.tv._screen_alt
        self.tv.termWrite("AltText")
        assert _get_screen_text(self.tv._screen_alt, 0).startswith("AltText")
        self.tv.termWrite("\033[?1047l")
        assert self.tv._screen_current is self.tv._screen_normal
        assert _get_screen_text(self.tv._screen_normal, 0).startswith("NormalText")

    def test_1049_combines_1047_and_1048(self):
        self.tv.termWrite("Before")
        self.tv.termWrite("\033[?1049h")
        assert self.tv._screen_current is self.tv._screen_alt
        self.tv.termWrite("\033[?1049l")
        assert self.tv._screen_current is self.tv._screen_normal

    def test_cursor_show_hide_dectcem(self):
        assert self.tv._widgetCursorEnabled == True
        self.tv.termWrite("\033[?25l")
        assert self.tv._widgetCursorEnabled == False
        self.tv.termWrite("\033[?25h")
        assert self.tv._widgetCursorEnabled == True

    def test_decckm_application_cursor_keys(self):
        assert not (self.tv._keyboard.flags & TTkTerminalModes.MODE_DECCKM)
        self.tv.termWrite("\033[?1h")
        assert self.tv._keyboard.flags & TTkTerminalModes.MODE_DECCKM
        self.tv.termWrite("\033[?1l")
        assert not (self.tv._keyboard.flags & TTkTerminalModes.MODE_DECCKM)

    def test_mouse_tracking_1000(self):
        self.tv.termWrite("\033[?1000h")
        assert self.tv._mouse.reportPress == True
        assert self.tv._mouse.reportDrag == False
        assert self.tv._mouse.reportMove == False
        self.tv.termWrite("\033[?1000l")
        assert self.tv._mouse.reportPress == False

    def test_mouse_tracking_1002_cell_motion(self):
        self.tv.termWrite("\033[?1002h")
        assert self.tv._mouse.reportPress == True
        assert self.tv._mouse.reportDrag == True
        assert self.tv._mouse.reportMove == False

    def test_mouse_tracking_1003_all_motion(self):
        self.tv.termWrite("\033[?1003h")
        assert self.tv._mouse.reportPress == True
        assert self.tv._mouse.reportDrag == True
        assert self.tv._mouse.reportMove == True

    def test_sgr_mouse_mode_1006(self):
        assert self.tv._mouse.sgrMode == False
        self.tv.termWrite("\033[?1006h")
        assert self.tv._mouse.sgrMode == True
        self.tv.termWrite("\033[?1006l")
        assert self.tv._mouse.sgrMode == False

    def test_bracketed_paste_mode_2004(self):
        assert self.tv._terminal.bracketedMode == False
        self.tv.termWrite("\033[?2004h")
        assert self.tv._terminal.bracketedMode == True
        self.tv.termWrite("\033[?2004l")
        assert self.tv._terminal.bracketedMode == False

    def test_bracketed_paste_wraps_content(self):
        self.tv._terminal.bracketedMode = True
        emitted = []
        self.tv._termData.connect(lambda d: emitted.append(d))
        self.tv.pasteEvent("hello")
        assert len(emitted) == 1
        assert emitted[0] == b"\033[200~hello\033[201~"

    def test_bracketed_paste_no_wrap_when_disabled(self):
        self.tv._terminal.bracketedMode = False
        emitted = []
        self.tv._termData.connect(lambda d: emitted.append(d))
        self.tv.pasteEvent("hello")
        assert emitted[0] == b"hello"


class TestOSCTitleChange:
    '''Tests for OSC escape sequences (title changes).'''

    def setup_method(self):
        self.tv = _make_terminal_view(w=20, h=5)
        self.titles = []
        self.tv._titleChanged.connect(lambda t: self.titles.append(t))

    def test_osc_0_title_with_bel(self):
        self.tv.termWrite("\033]0;MyTitle\a")
        assert self.titles == ["MyTitle"]

    def test_osc_0_title_with_st(self):
        self.tv.termWrite("\033]0;MyTitle\033\\")
        assert self.titles == ["MyTitle"]

    def test_osc_2_title(self):
        self.tv.termWrite("\033]2;WindowTitle\a")
        assert self.titles == ["WindowTitle"]

    def test_osc_1_icon_name(self):
        self.tv.termWrite("\033]1;IconName\a")
        assert self.titles == ["IconName"]

    def test_osc_title_with_special_chars(self):
        self.tv.termWrite("\033]0;path/to/dir ~ user@host\a")
        assert self.titles == ["path/to/dir ~ user@host"]

    def test_osc_title_split_across_writes(self):
        # OSC without terminator waits for next input via generator yield
        # The second write must provide the BEL terminator
        self.tv.termWrite("\033]0;First")
        assert self.titles == [], "Title should not emit until terminator received"
        self.tv.termWrite("Second")
        assert self.titles == [], "Title should not emit until terminator received"
        self.tv.termWrite("Third")
        assert self.titles == [], "Title should not emit until terminator received"
        self.tv.termWrite("Part\a")
        # Expected: OSC completes with "FirstPart"
        assert self.titles == ["FirstSecondThirdPart"]

    def test_osc_followed_by_text(self):
        self.tv.termWrite("\033]0;Title\aHello")
        assert self.titles == ["Title"]
        assert _get_screen_text(self.tv._screen_current, 0).startswith("Hello")


class TestEscapeSequenceDispatch:
    '''Tests for the escape sequence parser/dispatch in the view loop.'''

    def setup_method(self):
        self.tv = _make_terminal_view(w=20, h=5)

    def test_plain_text_no_escape(self):
        self.tv.termWrite("Hello World")
        assert _get_screen_text(self.tv._screen_current, 0) == "Hello World"

    def test_csi_cursor_movement_via_termwrite(self):
        self.tv.termWrite("ABCDE\033[3D")
        assert self.tv._screen_current.getCursor() == (2, 0)

    def test_csi_erase_display_via_termwrite(self):
        self.tv.termWrite("ABCDE\033[2J")
        assert _get_screen_text(self.tv._screen_current, 0) == ""

    def test_csi_cursor_position_via_termwrite(self):
        self.tv.termWrite("\033[3;5H")
        assert self.tv._screen_current.getCursor() == (4, 2)

    def test_multiple_escapes_in_one_write(self):
        self.tv.termWrite("\033[31mRed\033[0m Normal")
        text = _get_screen_text(self.tv._screen_current, 0)
        assert "Red" in text
        assert "Normal" in text

    def test_split_escape_across_writes(self):
        self.tv.termWrite("\033[")
        self.tv.termWrite("5A")
        # cursor should have moved up (or stay at 0 since we start at row 0)
        assert self.tv._screen_current.getCursor()[1] == 0

    def test_c1_esc_d_index(self):
        self.tv.termWrite("Line0\033D")
        # ESC D = Index = move cursor down
        assert self.tv._screen_current.getCursor()[1] == 1

    def test_c1_esc_m_reverse_index(self):
        self.tv.termWrite("\033[3;1H")  # move to row 3
        self.tv.termWrite("\033M")       # ESC M = Reverse Index
        assert self.tv._screen_current.getCursor()[1] == 1

    def test_deckpam_deckpnm(self):
        self.tv.termWrite("\033=")
        assert self.tv._keyboard.flags & TTkTerminalModes.MODE_DECKPAM
        self.tv.termWrite("\033>")
        assert not (self.tv._keyboard.flags & TTkTerminalModes.MODE_DECKPAM)

    def test_dcs_sequence_ignored(self):
        self.tv.termWrite("\033Psome;data\033\\After")
        assert _get_screen_text(self.tv._screen_current, 0).startswith("After")


class TestCursorSaveRestore:
    '''Tests for cursor save/restore (DECSC/DECRC via DEC 1048).'''

    def test_dec_1048_save_restore_cursor(self):
        self.tv = _make_terminal_view(w=20, h=5)
        self.tv.termWrite("ABC")
        saved_cursor = self.tv._screen_current.getCursor()  # (3, 0)
        self.tv.termWrite("\033[?1048h")  # save
        self.tv.termWrite("\033[5;5H")    # move to (4, 4)
        self.tv.termWrite("\033[?1048l")  # restore
        cursor_after = self.tv._screen_current.getCursor()
        assert cursor_after == saved_cursor, \
            f"DECSC/DECRC (1048) should restore cursor to {saved_cursor}, got {cursor_after}"

    def test_scosc_scorc_save_restore_cursor(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        screen.pushLine("ABC")
        saved_cursor = screen.getCursor()  # (3, 0)
        screen._CSI_s_SCOSC(0, None)
        screen._terminalCursor = (10, 3)
        screen._CSI_u_SCORC(0, None)
        cursor_after = screen.getCursor()
        assert cursor_after == saved_cursor, \
            f"SCOSC/SCORC should restore cursor to {saved_cursor}, got {cursor_after}"


class TestIRMInsertReplaceMode:
    '''Tests for Insert/Replace mode (CSI 4 h / CSI 4 l).'''

    def setup_method(self):
        self.tv = _make_terminal_view(w=10, h=3)

    def test_irm_default_is_replace(self):
        assert self.tv._terminal.IRM == False

    def test_irm_set_insert_mode(self):
        self.tv.termWrite("\033[4h")
        assert self.tv._terminal.IRM == True

    def test_irm_reset_replace_mode(self):
        self.tv.termWrite("\033[4h")
        self.tv.termWrite("\033[4l")
        assert self.tv._terminal.IRM == False

    def test_irm_insert_shifts_text(self):
        self.tv.termWrite("ABCDEFGHIJ")
        self.tv.termWrite("\033[4h")       # insert mode
        self.tv.termWrite("\033[1;4H")     # cursor to col 4
        self.tv.termWrite("XY")
        row = _get_screen_row(self.tv._screen_current, 0)
        # In insert mode, XY inserted at position 3 shifts DEFGHIJ right, truncating to width
        assert row == "ABCXYDEFGH", \
            f"IRM insert mode should shift existing text right, got '{row}'"


class TestDSRDeviceStatusReport:
    '''Tests for CSI n (Device Status Report).'''

    def setup_method(self):
        self.tv = _make_terminal_view(w=20, h=10)
        self.responses = []
        self.tv._termData.connect(lambda d: self.responses.append(d))

    def test_dsr_5_status_ok(self):
        self.tv.termWrite("\033[5n")
        assert b"\033[0n" in self.responses

    def test_dsr_6_cursor_position(self):
        self.tv.termWrite("\033[3;7H")  # move to row 3, col 7
        self.tv.termWrite("\033[6n")
        assert b"\033[3;7R" in self.responses

    def test_dsr_6_at_home(self):
        self.tv.termWrite("\033[6n")
        assert b"\033[1;1R" in self.responses


class TestWideCharacters:
    '''Tests for wide (CJK) character handling in terminal screen.'''

    def test_wide_char_occupies_two_cells(self):
        screen = _TTkTerminalScreen(w=10, h=3)
        screen.pushLine("A\u4e2d")  # 'A' + Chinese char (width 2)
        data = screen._canvas._data[0]
        # Wide char should occupy 2 cells: the char + empty continuation
        assert data[0] == 'A'
        assert data[1] == '\u4e2d'
        # The next cell should be empty (continuation of wide char)
        assert data[2] == ''

    def test_wide_char_cursor_advance(self):
        screen = _TTkTerminalScreen(w=10, h=3)
        screen.pushLine("\u4e2d")
        assert screen.getCursor() == (2, 0)

    def test_wide_char_at_edge_wraps(self):
        screen = _TTkTerminalScreen(w=4, h=3)
        screen.pushLine("ABC\u4e2d")
        # 'ABC' fills cols 0-2, wide char needs 2 cells but only 1 remains
        # Wide char should wrap to row 1, cols 0-1
        data_row0 = screen._canvas._data[0]
        data_row1 = screen._canvas._data[1]
        assert data_row0[0] == 'A'
        assert data_row0[1] == 'B'
        assert data_row0[2] == 'C'
        assert data_row1[0] == '\u4e2d', \
            f"Wide char should wrap to row 1 col 0, got row1={data_row1}"
        assert data_row1[1] == '', \
            "Wide char continuation cell should be empty"

    def test_multiple_wide_chars(self):
        screen = _TTkTerminalScreen(w=10, h=3)
        screen.pushLine("\u4e2d\u6587")  # Two Chinese chars
        assert screen.getCursor() == (4, 0)
        data = screen._canvas._data[0]
        assert data[0] == '\u4e2d'
        assert data[1] == ''
        assert data[2] == '\u6587'
        assert data[3] == ''

    def test_overwrite_wide_char_with_narrow(self):
        screen = _TTkTerminalScreen(w=10, h=3)
        screen.pushLine("\u4e2d\u6587AB")
        # Now overwrite position 0 with narrow char
        screen._terminalCursor = (0, 0)
        screen._pushTxt("X")
        data = screen._canvas._data[0]
        assert data[0] == 'X'


class TestScrollingRegionEdgeCases:
    '''Additional edge case tests for scrolling region behavior.'''

    def test_scrolling_region_reset_on_resize(self):
        screen = _TTkTerminalScreen(w=10, h=10)
        screen._CSI_r_DECSTBM(3, 7)
        assert screen._scrollingRegion == (2, 7)
        screen.resize(10, 5)
        assert screen._scrollingRegion == (0, 5)

    def test_newline_at_bottom_of_region_scrolls(self):
        screen = _TTkTerminalScreen(w=10, h=5)
        screen._CSI_r_DECSTBM(1, 3)  # region rows 0-2
        screen._terminalCursor = (0, 0)
        screen._pushTxt("AAA")
        screen._terminalCursor = (0, 1)
        screen._pushTxt("BBB")
        screen._terminalCursor = (0, 2)
        screen._pushTxt("CCC")
        # Index at bottom of region should scroll region
        screen._terminalCursor = (0, 2)
        screen._C1_D()
        assert _get_screen_text(screen, 0) == "BBB"
        assert _get_screen_text(screen, 1) == "CCC"
        assert _get_screen_text(screen, 2) == ""


class TestMultipleModesInteraction:
    '''Tests for interactions between multiple DEC modes.'''

    def setup_method(self):
        self.tv = _make_terminal_view(w=20, h=5)

    def test_multiple_modes_in_single_sequence(self):
        self.tv.termWrite("\033[?25l")
        self.tv.termWrite("\033[?1000h")
        assert self.tv._widgetCursorEnabled == False
        assert self.tv._mouse.reportPress == True

    def test_alt_screen_preserves_normal_content(self):
        self.tv.termWrite("LineOnNormal")
        self.tv.termWrite("\033[?1049h")
        self.tv.termWrite("LineOnAlt")
        assert _get_screen_text(self.tv._screen_alt, 0).startswith("LineOnAlt")
        assert _get_screen_text(self.tv._screen_normal, 0).startswith("LineOnNormal")
        self.tv.termWrite("\033[?1049l")
        assert _get_screen_text(self.tv._screen_current, 0).startswith("LineOnNormal")

    def test_color_persists_across_screens(self):
        self.tv.termWrite("\033[31m")
        self.tv.termWrite("\033[?1047h")
        self.tv.termWrite("X")
        color = self.tv._screen_alt._canvas._colors[0][0]
        r, g, b = color.fgToRGB()
        assert r > 0 and g == 0 and b == 0


class TestTerminalScreenTabStops:
    '''Tests for tab stop behavior (ESC H = HTS, CSI g = TBC).
    These are currently stubbed - tests document what happens.'''

    def test_tab_character_default_stops(self):
        screen = _TTkTerminalScreen(w=20, h=3)
        screen.pushLine("\tX")
        # Default VT100 tab stops are at every 8th column
        # After tab, cursor should be at column 8, then X at column 8
        row = _get_screen_text(screen, 0)
        x_pos = row.find('X')
        assert x_pos == 8, \
            f"Tab should advance to column 8 (default tab stop), X found at {x_pos}"
