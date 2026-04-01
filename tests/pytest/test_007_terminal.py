# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
import pytest

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.TTkTerminal.terminal_screen import _TTkTerminalScreen


def _get_screen_text(screen, row):
    '''Get the text content of a screen row as a string (trimmed of trailing spaces).'''
    data = screen._canvas._data[row]
    return ''.join(data).rstrip()


def _get_screen_row(screen, row):
    '''Get the full raw text content of a screen row.'''
    return ''.join(screen._canvas._data[row])


class TestTerminalScreenBasic:
    '''Tests for basic _TTkTerminalScreen operations.'''

    def test_init_default(self):
        screen = _TTkTerminalScreen()
        assert screen._w == 80
        assert screen._h == 24
        assert screen._terminalCursor == (0, 0)
        assert screen._scrollingRegion == (0, 24)

    def test_init_custom_size(self):
        screen = _TTkTerminalScreen(w=40, h=10)
        assert screen._w == 40
        assert screen._h == 10
        assert screen._terminalCursor == (0, 0)
        assert screen._scrollingRegion == (0, 10)

    def test_push_simple_text(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        screen.pushLine("Hello")
        assert _get_screen_text(screen, 0) == "Hello"
        assert screen._terminalCursor == (5, 0)

    def test_push_text_with_newline(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        # \n (LF) moves cursor down but preserves x position
        screen.pushLine("Line1\nLine2")
        assert _get_screen_text(screen, 0) == "Line1"
        assert _get_screen_text(screen, 1) == "     Line2"

    def test_push_text_with_cr_lf(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        # \r\n resets x to 0 then moves down
        screen.pushLine("Line1\r\nLine2")
        assert _get_screen_text(screen, 0) == "Line1"
        assert _get_screen_text(screen, 1) == "Line2"

    def test_push_text_with_carriage_return(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        screen.pushLine("Hello\rWorld")
        assert _get_screen_text(screen, 0) == "World"

    def test_push_text_with_backspace(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        # Backspace moves cursor back 1, then 'd' overwrites position 2
        screen.pushLine("abc\bd")
        assert _get_screen_text(screen, 0) == "abd"

    def test_cursor_get(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        assert screen.getCursor() == (0, 0)
        screen.pushLine("AB")
        assert screen.getCursor() == (2, 0)

    def test_resize(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        screen.pushLine("Hello")
        screen.resize(40, 10)
        assert screen._w == 40
        assert screen._h == 10
        assert screen._scrollingRegion == (0, 10)
        assert _get_screen_text(screen, 0) == "Hello"

    def test_resize_minimum_bounds(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        screen.resize(1, 1)
        assert screen._w == 3  # min width
        assert screen._h == 1  # min height

    def test_get_buffer_simple(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        screen.pushLine("Line1\r\nLine2\r\nLine3")
        buf = screen.getBuffer()
        assert len(buf) == 3
        assert str(buf[0]) == "Line1"
        assert str(buf[1]) == "Line2"
        assert str(buf[2]) == "Line3"

    def test_get_buffer_empty(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        buf = screen.getBuffer()
        assert len(buf) == 0


class TestTerminalCSICursorMovement:
    '''Tests for CSI cursor movement escape sequences.'''

    def setup_method(self):
        self.screen = _TTkTerminalScreen(w=20, h=10)

    # CSI Ps A - Cursor Up (CUU)
    def test_cursor_up(self):
        self.screen._terminalCursor = (5, 5)
        self.screen._CSI_A_CUU(3, None)
        assert self.screen._terminalCursor == (5, 2)

    def test_cursor_up_clamped(self):
        self.screen._terminalCursor = (5, 2)
        self.screen._CSI_A_CUU(10, None)
        assert self.screen._terminalCursor == (5, 0)

    # CSI Ps B - Cursor Down (CUD)
    def test_cursor_down(self):
        self.screen._terminalCursor = (5, 3)
        self.screen._CSI_B_CUD(4, None)
        assert self.screen._terminalCursor == (5, 7)

    def test_cursor_down_clamped(self):
        self.screen._terminalCursor = (5, 8)
        self.screen._CSI_B_CUD(10, None)
        assert self.screen._terminalCursor == (5, 9)

    # CSI Ps C - Cursor Forward (CUF)
    def test_cursor_forward(self):
        self.screen._terminalCursor = (3, 5)
        self.screen._CSI_C_CUF(5, None)
        assert self.screen._terminalCursor == (8, 5)

    def test_cursor_forward_clamped(self):
        self.screen._terminalCursor = (15, 5)
        self.screen._CSI_C_CUF(10, None)
        assert self.screen._terminalCursor == (19, 5)

    # CSI Ps D - Cursor Backward (CUB)
    def test_cursor_backward(self):
        self.screen._terminalCursor = (10, 5)
        self.screen._CSI_D_CUB(3, None)
        assert self.screen._terminalCursor == (7, 5)

    def test_cursor_backward_clamped(self):
        self.screen._terminalCursor = (2, 5)
        self.screen._CSI_D_CUB(10, None)
        assert self.screen._terminalCursor == (0, 5)

    # CSI Ps E - Cursor Next Line (CNL)
    def test_cursor_next_line(self):
        self.screen._terminalCursor = (5, 3)
        self.screen._CSI_E_CNL(2, None)
        assert self.screen._terminalCursor == (0, 5)

    def test_cursor_next_line_clamped(self):
        self.screen._terminalCursor = (5, 8)
        self.screen._CSI_E_CNL(5, None)
        assert self.screen._terminalCursor == (0, 9)

    # CSI Ps F - Cursor Preceding Line (CPL)
    def test_cursor_preceding_line(self):
        self.screen._terminalCursor = (5, 5)
        self.screen._CSI_F_CPL(2, None)
        assert self.screen._terminalCursor == (0, 3)

    def test_cursor_preceding_line_clamped(self):
        self.screen._terminalCursor = (5, 1)
        self.screen._CSI_F_CPL(10, None)
        assert self.screen._terminalCursor == (0, 0)

    # CSI Ps G - Cursor Character Absolute (CHA)
    def test_cursor_character_absolute(self):
        self.screen._terminalCursor = (0, 5)
        self.screen._CSI_G_CHA(10, None)
        assert self.screen._terminalCursor == (9, 5)  # 1-based → 0-based

    def test_cursor_character_absolute_clamped(self):
        self.screen._terminalCursor = (0, 5)
        self.screen._CSI_G_CHA(100, None)
        assert self.screen._terminalCursor == (19, 5)

    # CSI Ps ; Ps H - Cursor Position (CUP)
    def test_cursor_position(self):
        self.screen._CSI_H_CUP(5, 10)
        assert self.screen._terminalCursor == (9, 4)  # 1-based → 0-based

    def test_cursor_position_origin(self):
        self.screen._terminalCursor = (5, 5)
        self.screen._CSI_H_CUP(1, 1)
        assert self.screen._terminalCursor == (0, 0)

    def test_cursor_position_clamped(self):
        self.screen._CSI_H_CUP(100, 100)
        assert self.screen._terminalCursor == (19, 9)

    # CSI Ps d - Line Position Absolute (VPA)
    def test_line_position_absolute(self):
        self.screen._terminalCursor = (5, 0)
        self.screen._CSI_d_VPA(7, None)
        assert self.screen._terminalCursor == (5, 6)  # 1-based → 0-based

    def test_line_position_absolute_clamped(self):
        self.screen._terminalCursor = (5, 0)
        self.screen._CSI_d_VPA(100, None)
        assert self.screen._terminalCursor == (5, 9)

    # CSI Ps ; Ps f - Horizontal and Vertical Position (HVP)
    def test_horizontal_vertical_position(self):
        self.screen._CSI_f_HVP(3, 7)
        assert self.screen._terminalCursor == (6, 2)  # 1-based → 0-based


class TestTerminalCSIErase:
    '''Tests for CSI erase escape sequences.'''

    def setup_method(self):
        self.screen = _TTkTerminalScreen(w=10, h=5)

    def _fill_screen(self):
        '''Fill screen with predictable content.'''
        for row in range(5):
            self.screen._terminalCursor = (0, row)
            self.screen._pushTxt(f"Row{row:05d}!")

    # CSI Ps J - Erase in Display (ED)
    def test_erase_below(self):
        self._fill_screen()
        self.screen._terminalCursor = (3, 2)
        self.screen._CSI_J_ED(0, None)
        # Row 0 and 1 untouched
        assert _get_screen_text(self.screen, 0) == "Row00000!"
        assert _get_screen_text(self.screen, 1) == "Row00001!"
        # Row 2 from pos 3 onward erased
        row2 = _get_screen_row(self.screen, 2)
        assert row2[:3] == "Row"
        # Rows 3-4 fully erased
        assert _get_screen_text(self.screen, 3) == ""
        assert _get_screen_text(self.screen, 4) == ""

    def test_erase_all(self):
        self._fill_screen()
        self.screen._terminalCursor = (0, 0)
        self.screen._CSI_J_ED(2, None)
        for row in range(5):
            assert _get_screen_text(self.screen, row) == ""

    # CSI Ps K - Erase in Line (EL)
    def test_erase_to_right(self):
        self.screen._terminalCursor = (0, 0)
        self.screen._pushTxt("ABCDEFGHIJ")
        self.screen._terminalCursor = (5, 0)
        self.screen._CSI_K_EL(0, None)
        row = _get_screen_row(self.screen, 0)
        assert row[:5] == "ABCDE"
        assert row[5:] == "     "

    def test_erase_to_left(self):
        self.screen._terminalCursor = (0, 0)
        self.screen._pushTxt("ABCDEFGHIJ")
        self.screen._terminalCursor = (5, 0)
        self.screen._CSI_K_EL(1, None)
        row = _get_screen_row(self.screen, 0)
        assert row[:5] == "     "
        assert row[5:] == "FGHIJ"

    def test_erase_entire_line(self):
        self.screen._terminalCursor = (0, 0)
        self.screen._pushTxt("ABCDEFGHIJ")
        self.screen._terminalCursor = (5, 0)
        self.screen._CSI_K_EL(2, None)
        assert _get_screen_text(self.screen, 0) == ""

    def test_erase_to_right_preserves_fg_bg_but_removes_modifiers(self):
        self.screen._terminalCursor = (0, 0)
        self.screen._pushTxt("ABCDEFGHIJ")

        styled = TTkColor.fg('#112233') + TTkColor.bg('#445566') + TTkColor.UNDERLINE + TTkColor.BOLD
        self.screen.setColor(styled)
        self.screen._terminalCursor = (5, 0)
        self.screen._CSI_K_EL(0, None)

        erased_color = self.screen._canvas._colors[0][5]
        assert erased_color.fgToRGB() == (0x11, 0x22, 0x33)
        assert erased_color.bgToRGB() == (0x44, 0x55, 0x66)
        assert not erased_color.underline()
        assert not erased_color.bold()

    def test_erase_to_left_preserves_fg_bg_but_removes_modifiers(self):
        self.screen._terminalCursor = (0, 0)
        self.screen._pushTxt("ABCDEFGHIJ")

        styled = TTkColor.fg('#aabbcc') + TTkColor.bg('#010203') + TTkColor.UNDERLINE + TTkColor.ITALIC
        self.screen.setColor(styled)
        self.screen._terminalCursor = (5, 0)
        self.screen._CSI_K_EL(1, None)

        erased_color = self.screen._canvas._colors[0][0]
        assert erased_color.fgToRGB() == (0xaa, 0xbb, 0xcc)
        assert erased_color.bgToRGB() == (0x01, 0x02, 0x03)
        assert not erased_color.underline()
        assert not erased_color.italic()


class TestTerminalCSICharManipulation:
    '''Tests for CSI character insertion/deletion escape sequences.'''

    def setup_method(self):
        self.screen = _TTkTerminalScreen(w=10, h=5)

    # CSI Ps @ - Insert Blank Characters (ICH)
    # ICH inserts empty-string entries (zero-width blanks), shifting content right
    def test_insert_blank_chars(self):
        self.screen._terminalCursor = (0, 0)
        self.screen._pushTxt("ABCDEFGHIJ")
        self.screen._terminalCursor = (3, 0)
        self.screen._CSI___ICH(2, None)
        data = self.screen._canvas._data[0]
        # 2 empty strings inserted at position 3, content shifted right, truncated to width
        assert data[:5] == ['A', 'B', 'C', '', '']
        assert data[5:10] == ['D', 'E', 'F', 'G', 'H']

    # CSI Ps P - Delete Characters (DCH)
    def test_delete_chars(self):
        self.screen._terminalCursor = (0, 0)
        self.screen._pushTxt("ABCDEFGHIJ")
        self.screen._terminalCursor = (3, 0)
        self.screen._CSI_P_DCH(2, None)
        row = _get_screen_row(self.screen, 0)
        assert row == "ABCFGHIJ  "

    def test_delete_chars_clamped(self):
        self.screen._terminalCursor = (0, 0)
        self.screen._pushTxt("ABCDEFGHIJ")
        self.screen._terminalCursor = (8, 0)
        self.screen._CSI_P_DCH(5, None)
        row = _get_screen_row(self.screen, 0)
        assert row == "ABCDEFGH  "

    # CSI Ps X - Erase Characters (ECH)
    def test_erase_chars(self):
        self.screen._terminalCursor = (0, 0)
        self.screen._pushTxt("ABCDEFGHIJ")
        self.screen._terminalCursor = (3, 0)
        self.screen._CSI_X_ECH(4, None)
        row = _get_screen_row(self.screen, 0)
        assert row == "ABC    HIJ"

    # CSI Ps b - Repeat Preceding Character (REP)
    def test_repeat_character(self):
        self.screen._terminalCursor = (0, 0)
        self.screen._pushTxt("X")
        self.screen._CSI_b_REP(4, None)
        assert _get_screen_text(self.screen, 0) == "XXXXX"


class TestTerminalCSILineManipulation:
    '''Tests for CSI line insertion/deletion escape sequences.'''

    def setup_method(self):
        self.screen = _TTkTerminalScreen(w=10, h=5)
        for row in range(5):
            self.screen._terminalCursor = (0, row)
            self.screen._pushTxt(chr(ord('A') + row) * 5)

    # CSI Ps L - Insert Lines (IL)
    def test_insert_lines(self):
        self.screen._terminalCursor = (0, 2)
        self.screen._CSI_L_IL(1, None)
        assert _get_screen_text(self.screen, 0) == "AAAAA"
        assert _get_screen_text(self.screen, 1) == "BBBBB"
        assert _get_screen_text(self.screen, 2) == ""       # inserted
        assert _get_screen_text(self.screen, 3) == "CCCCC"  # shifted down
        assert _get_screen_text(self.screen, 4) == "DDDDD"  # shifted down
        # "EEEEE" is pushed off screen

    # CSI Ps M - Delete Lines (DL)
    def test_delete_lines(self):
        self.screen._terminalCursor = (0, 1)
        self.screen._CSI_M_DL(1, None)
        assert _get_screen_text(self.screen, 0) == "AAAAA"
        assert _get_screen_text(self.screen, 1) == "CCCCC"  # shifted up
        assert _get_screen_text(self.screen, 2) == "DDDDD"  # shifted up
        assert _get_screen_text(self.screen, 3) == "EEEEE"  # shifted up
        assert _get_screen_text(self.screen, 4) == ""        # blank


class TestTerminalCSIScrolling:
    '''Tests for CSI scroll escape sequences.'''

    def setup_method(self):
        self.screen = _TTkTerminalScreen(w=10, h=5)
        for row in range(5):
            self.screen._terminalCursor = (0, row)
            self.screen._pushTxt(chr(ord('A') + row) * 5)

    # CSI Ps S - Scroll Up (SU)
    def test_scroll_up(self):
        self.screen._CSI_S_SU(1)
        assert _get_screen_text(self.screen, 0) == "BBBBB"
        assert _get_screen_text(self.screen, 1) == "CCCCC"
        assert _get_screen_text(self.screen, 2) == "DDDDD"
        assert _get_screen_text(self.screen, 3) == "EEEEE"
        assert _get_screen_text(self.screen, 4) == ""  # new blank line

    def test_scroll_up_multiple(self):
        self.screen._CSI_S_SU(2)
        assert _get_screen_text(self.screen, 0) == "CCCCC"
        assert _get_screen_text(self.screen, 1) == "DDDDD"
        assert _get_screen_text(self.screen, 2) == "EEEEE"
        assert _get_screen_text(self.screen, 3) == ""
        assert _get_screen_text(self.screen, 4) == ""

    def test_scroll_up_adds_to_buffer(self):
        self.screen._CSI_S_SU(1)
        assert len(self.screen._bufferedLines) == 1
        assert str(self.screen._bufferedLines[0]) == "AAAAA"

    # CSI Ps T - Scroll Down (SD)
    def test_scroll_down(self):
        self.screen._CSI_T_SD(1)
        assert _get_screen_text(self.screen, 0) == ""       # new blank line
        assert _get_screen_text(self.screen, 1) == "AAAAA"
        assert _get_screen_text(self.screen, 2) == "BBBBB"
        assert _get_screen_text(self.screen, 3) == "CCCCC"
        assert _get_screen_text(self.screen, 4) == "DDDDD"
        # "EEEEE" pushed off bottom


class TestTerminalCSIScrollingRegion:
    '''Tests for CSI scrolling region (DECSTBM) and scrolling within regions.'''

    def setup_method(self):
        self.screen = _TTkTerminalScreen(w=10, h=6)
        for row in range(6):
            self.screen._terminalCursor = (0, row)
            self.screen._pushTxt(chr(ord('A') + row) * 5)

    # CSI Ps ; Ps r - Set Scrolling Region (DECSTBM)
    def test_set_scrolling_region(self):
        self.screen._CSI_r_DECSTBM(2, 5)
        assert self.screen._scrollingRegion == (1, 5)

    def test_scroll_up_within_region(self):
        self.screen._CSI_r_DECSTBM(2, 5)  # region: rows 1-4 (0-based)
        self.screen._CSI_S_SU(1)
        # Row 0 and row 5 should be untouched
        assert _get_screen_text(self.screen, 0) == "AAAAA"
        assert _get_screen_text(self.screen, 5) == "FFFFF"
        # Within region: scrolled up
        assert _get_screen_text(self.screen, 1) == "CCCCC"
        assert _get_screen_text(self.screen, 2) == "DDDDD"
        assert _get_screen_text(self.screen, 3) == "EEEEE"
        assert _get_screen_text(self.screen, 4) == ""   # new blank

    def test_scroll_down_within_region(self):
        self.screen._CSI_r_DECSTBM(2, 5)  # region: rows 1-4 (0-based)
        self.screen._CSI_T_SD(1)
        assert _get_screen_text(self.screen, 0) == "AAAAA"
        assert _get_screen_text(self.screen, 5) == "FFFFF"
        # Within region: scrolled down
        assert _get_screen_text(self.screen, 1) == ""       # new blank
        assert _get_screen_text(self.screen, 2) == "BBBBB"
        assert _get_screen_text(self.screen, 3) == "CCCCC"
        assert _get_screen_text(self.screen, 4) == "DDDDD"
        # "EEEEE" pushed off region bottom


class TestTerminalC1:
    '''Tests for C1 (ESC ...) escape sequences handled by _TTkTerminalScreen_C1.'''

    def setup_method(self):
        self.screen = _TTkTerminalScreen(w=10, h=5)
        for row in range(5):
            self.screen._terminalCursor = (0, row)
            self.screen._pushTxt(chr(ord('A') + row) * 5)

    # ESC D - Index (IND): move cursor down, scroll at bottom
    def test_c1_index_move_down(self):
        self.screen._terminalCursor = (3, 2)
        self.screen._C1_D()
        assert self.screen._terminalCursor == (3, 3)

    def test_c1_index_at_bottom_scrolls(self):
        self.screen._terminalCursor = (3, 4)
        self.screen._C1_D()
        # Should have scrolled up, cursor stays at bottom row
        assert self.screen._terminalCursor[1] == 4
        assert _get_screen_text(self.screen, 0) == "BBBBB"

    # ESC M - Reverse Index (RI): move cursor up, scroll at top
    def test_c1_reverse_index_move_up(self):
        self.screen._terminalCursor = (3, 3)
        self.screen._C1_M()
        assert self.screen._terminalCursor == (3, 2)

    def test_c1_reverse_index_at_top_scrolls(self):
        self.screen._terminalCursor = (3, 0)
        self.screen._C1_M()
        # Should have scrolled down, cursor stays at top
        assert self.screen._terminalCursor[1] == 0
        assert _get_screen_text(self.screen, 0) == ""
        assert _get_screen_text(self.screen, 1) == "AAAAA"


class TestTerminalTextWrapping:
    '''Tests for text wrapping at the right edge.'''

    def test_text_wraps_at_edge(self):
        screen = _TTkTerminalScreen(w=5, h=3)
        screen.pushLine("ABCDEFGH")
        # "ABCDE" on row 0, "FGH" wraps to row 1
        assert _get_screen_text(screen, 0) == "ABCDE"
        assert _get_screen_text(screen, 1) == "FGH"

    def test_text_wrap_scrolls_at_bottom(self):
        screen = _TTkTerminalScreen(w=5, h=2)
        screen.pushLine("ABCDEFGHIJKLMNO")
        # Should have scrolled; "KLMNO" on last row
        assert _get_screen_text(screen, 1) == "KLMNO"

    def test_newline_preserves_x(self):
        screen = _TTkTerminalScreen(w=10, h=5)
        # \n preserves x position (LF only moves down)
        screen.pushLine("AAA\nBBB\nCCC")
        assert _get_screen_text(screen, 0) == "AAA"
        assert _get_screen_text(screen, 1) == "   BBB"
        assert _get_screen_text(screen, 2) == "      CCC"

    def test_crlf_resets_x(self):
        screen = _TTkTerminalScreen(w=10, h=5)
        screen.pushLine("AAA\r\nBBB\r\nCCC")
        assert _get_screen_text(screen, 0) == "AAA"
        assert _get_screen_text(screen, 1) == "BBB"
        assert _get_screen_text(screen, 2) == "CCC"


class TestTerminalScrollbackBuffer:
    '''Tests for the scrollback buffer behavior.'''

    def test_scrollback_on_scroll_up(self):
        screen = _TTkTerminalScreen(w=10, h=3, bufferSize=100)
        for row in range(3):
            screen._terminalCursor = (0, row)
            screen._pushTxt(f"Line{row}")
        screen._CSI_S_SU(1)
        assert len(screen._bufferedLines) == 1
        assert str(screen._bufferedLines[0]) == "Line0"

    def test_scrollback_accumulates(self):
        screen = _TTkTerminalScreen(w=10, h=3, bufferSize=100)
        for row in range(3):
            screen._terminalCursor = (0, row)
            screen._pushTxt(chr(ord('A') + row) * 3)
        screen._CSI_S_SU(2)
        assert len(screen._bufferedLines) == 2
        assert str(screen._bufferedLines[0]) == "AAA"
        assert str(screen._bufferedLines[1]) == "BBB"

    def test_scrollback_buffer_limit(self):
        screen = _TTkTerminalScreen(w=10, h=2, bufferSize=5)
        for i in range(10):
            screen._terminalCursor = (0, 0)
            screen._pushTxt(f"L{i}")
            screen._CSI_S_SU(1)
        assert len(screen._bufferedLines) <= 5

    def test_get_buffer_includes_scrollback(self):
        screen = _TTkTerminalScreen(w=10, h=3, bufferSize=100)
        for row in range(3):
            screen._terminalCursor = (0, row)
            screen._pushTxt(chr(ord('A') + row) * 3)
        screen._CSI_S_SU(1)
        buf = screen.getBuffer()
        # Buffer should include scrollback ("AAA") + visible ("BBB", "CCC")
        texts = [str(line) for line in buf]
        assert "AAA" in texts
        assert "BBB" in texts
        assert "CCC" in texts


class TestTerminalCSIMap:
    '''Tests that the CSI and C1 dispatch maps are correctly populated.'''

    def test_csi_map_contains_expected_entries(self):
        expected_keys = {'@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                         'J', 'K', 'L', 'M', 'P', 'S', 'T', 'X',
                         'b', 'd', 'f', 'r'}
        actual_keys = set(_TTkTerminalScreen._CSI_MAP.keys())
        assert expected_keys == actual_keys

    def test_c1_map_contains_expected_entries(self):
        expected_keys = {'D', 'M'}
        actual_keys = set(_TTkTerminalScreen._C1_MAP.keys())
        assert expected_keys == actual_keys

    def test_csi_map_values_are_callable(self):
        for key, handler in _TTkTerminalScreen._CSI_MAP.items():
            assert callable(handler), f"Handler for CSI '{key}' is not callable"

    def test_c1_map_values_are_callable(self):
        for key, handler in _TTkTerminalScreen._C1_MAP.items():
            assert callable(handler), f"Handler for C1 '{key}' is not callable"


class TestTerminalCSIIntegration:
    '''Integration tests combining multiple CSI operations.'''

    def test_move_and_write(self):
        screen = _TTkTerminalScreen(w=20, h=5)
        screen.pushLine("Hello World")
        screen._CSI_H_CUP(1, 7)  # Move to col 7, row 1
        screen._pushTxt("There")
        assert _get_screen_text(screen, 0) == "Hello There"

    def test_clear_screen_and_write(self):
        screen = _TTkTerminalScreen(w=10, h=3)
        screen.pushLine("AAAAAAAAAA\nBBBBBBBBBB\nCCCCCCCCCC")
        screen._CSI_J_ED(2, None)  # Erase all
        for row in range(3):
            assert _get_screen_text(screen, row) == ""
        screen._CSI_H_CUP(1, 1)
        screen._pushTxt("New")
        assert _get_screen_text(screen, 0) == "New"

    def test_insert_and_delete_chars(self):
        screen = _TTkTerminalScreen(w=10, h=1)
        screen.pushLine("ABCDEFGHIJ")
        # Insert 2 blank entries at position 3 (ICH inserts empty strings)
        screen._terminalCursor = (3, 0)
        screen._CSI___ICH(2, None)
        data = screen._canvas._data[0]
        assert data == ['A', 'B', 'C', '', '', 'D', 'E', 'F', 'G', 'H']
        # Delete those 2 blank entries
        screen._terminalCursor = (3, 0)
        screen._CSI_P_DCH(2, None)
        assert _get_screen_row(screen, 0) == "ABCDEFGH  "

    def test_scroll_region_insert_delete_lines(self):
        screen = _TTkTerminalScreen(w=5, h=5)
        for row in range(5):
            screen._terminalCursor = (0, row)
            screen._pushTxt(chr(ord('A') + row) * 3)
        # Set scrolling region to rows 2-4 (1-based: 2;4)
        screen._CSI_r_DECSTBM(2, 4)
        # Delete 1 line at row 1 (within region)
        screen._terminalCursor = (0, 1)
        screen._CSI_M_DL(1, None)
        assert _get_screen_text(screen, 0) == "AAA"
        assert _get_screen_text(screen, 1) == "CCC"  # shifted up
        assert _get_screen_text(screen, 2) == "DDD"  # shifted up
        assert _get_screen_text(screen, 3) == ""      # new blank
        assert _get_screen_text(screen, 4) == "EEE"   # outside region, unchanged

    def test_multiple_newlines_and_cursor_moves(self):
        screen = _TTkTerminalScreen(w=20, h=10)
        # Use \r\n so each line starts at column 0
        screen.pushLine("Line0\r\nLine1\r\nLine2")
        assert screen.getCursor() == (5, 2)
        screen._CSI_A_CUU(1, None)
        assert screen.getCursor() == (5, 1)
        screen._pushTxt("!")
        row1 = _get_screen_text(screen, 1)
        assert row1 == "Line1!"

    def test_cursor_home_then_overwrite(self):
        screen = _TTkTerminalScreen(w=10, h=3)
        screen.pushLine("OLD TEXT")
        screen._CSI_H_CUP(1, 1)  # Home
        screen._pushTxt("NEW")
        assert _get_screen_text(screen, 0) == "NEW TEXT"

    def test_erase_to_right_then_write(self):
        screen = _TTkTerminalScreen(w=10, h=1)
        screen.pushLine("ABCDEFGHIJ")
        screen._terminalCursor = (5, 0)
        screen._CSI_K_EL(0, None)  # Erase to right
        screen._pushTxt("XY")
        assert _get_screen_text(screen, 0) == "ABCDEXY"


class TestTerminalColor:
    '''Tests for color state management on the terminal screen.'''

    def test_default_color(self):
        screen = _TTkTerminalScreen()
        assert screen.color() == TTkColor.RST

    def test_set_and_get_color(self):
        screen = _TTkTerminalScreen()
        color = TTkColor.fg("#ff0000")
        screen.setColor(color)
        assert screen.color() == color

    def test_color_applied_to_pushed_text(self):
        screen = _TTkTerminalScreen(w=10, h=3)
        color = TTkColor.fg("#00ff00")
        screen.setColor(color)
        screen.pushLine("Hi")
        assert screen._canvas._colors[0][0] == color
        assert screen._canvas._colors[0][1] == color


class TestTerminalBell:
    '''Tests for the bell signal.'''

    def test_bell_emitted(self):
        screen = _TTkTerminalScreen(w=10, h=3)
        bell_count = [0]
        screen.bell.connect(lambda: bell_count.__setitem__(0, bell_count[0] + 1))
        screen._pushTxt("Hello\aWorld")
        assert bell_count[0] == 1

    def test_multiple_bells(self):
        screen = _TTkTerminalScreen(w=10, h=3)
        bell_count = [0]
        screen.bell.connect(lambda: bell_count.__setitem__(0, bell_count[0] + 1))
        screen._pushTxt("A\aB\aC")
        assert bell_count[0] == 2
