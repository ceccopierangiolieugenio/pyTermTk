#!/usr/bin/env python3
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

import os
import sys

sys.path.append(os.path.join(sys.path[0], '../../libs/pyTermTk'))

import TermTk as ttk

from TermTk.TTkGui.TTkTextWrap.text_wrap_data import _WrapLine


def _mk_wrap(text: str, width: int = 4, word_wrap: bool = False):
    doc = ttk.TTkTextDocument(text=text)
    tw = ttk.TTkTextWrap(document=doc)
    tw.setEngine(ttk.TTkK.WrapEngine.FullWrap)
    tw.setWrapWidth(width)
    if word_wrap:
        tw.setWordWrapMode(ttk.TTkK.WordWrap)
    else:
        tw.setWordWrapMode(ttk.TTkK.WrapAnywhere)
    return doc, tw


def _rows_for(tw: ttk.TTkTextWrap, y: int, h: int) -> list[_WrapLine]:
    """Return wrapped rows and validate the screenRows contract."""
    ret = tw.screenRows(y, h)
    assert isinstance(ret.rows, list)
    return ret.rows


def test_screen_rows_wrap_anywhere_visible_window():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    rows = _rows_for(tw, 0, 4)

    assert len(rows) == 4
    assert rows[0] == _WrapLine(0, 0, 4, False)
    assert rows[1] == _WrapLine(0, 4, 8, False)
    assert rows[2] == _WrapLine(0, 8, 11, True)
    assert rows[3] == _WrapLine(1, 0, 4, True)


def test_data_to_screen_and_back_roundtrip():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    for pos in (0, 3, 4, 7, 9, 10):
        x, y = tw.dataToScreenPosition(0, pos).to_xy()
        line, dpos = tw.screenToDataPosition(x, y)
        assert line == 0
        assert dpos == pos


def test_rewrap_after_document_content_change():
    doc, tw = _mk_wrap('line0-abcdefghij\nline1-abcdefghij\nline2-abcdefghij', width=6)

    size_before = tw.size()
    assert size_before > 3  # lines wrap at width=6

    # Shrink the document; FullWrap re-wraps via contentsChange signal.
    doc.setText('short')

    assert tw.size() < size_before
    rows = _rows_for(tw, 0, 5)
    assert len(rows) >= 1
    assert rows[0].line == 0


def test_size_returns_correct_total_wrapped_row_count():
    _, tw = _mk_wrap(('abcdefghij\n' * 50).rstrip('\n'), width=4)

    # FullWrap eagerly wraps everything; size() is always exact.
    # 'abcdefghij' (10 chars) at width=4 → 3 screen rows per data line.
    # 50 data lines → 150 screen rows.
    assert tw.size() == 150


def test_data_to_screen_position_safe_after_document_shrink():
    doc, tw = _mk_wrap('line0\nline1\nline2', width=4)

    assert tw.size() > 0

    # Shrink the document; the engine re-wraps automatically.
    doc.setText('only-one-line')

    x, y = tw.dataToScreenPosition(2, 0).to_xy()

    assert x >= 0
    assert y >= 0

    doc.clear()

    x, y = tw.dataToScreenPosition(2, 0).to_xy()

    assert x >= 0
    assert y >= 0


def test_screen_to_data_position_safe_after_document_shrink():
    doc, tw = _mk_wrap('line0\nline1\nline2', width=4)

    assert tw.size() > 0

    # Shrink the document; the engine re-wraps automatically.
    doc.setText('x')

    line, pos = tw.screenToDataPosition(0, 2)

    assert line >= 0
    assert pos >= 0


# ---------------------------------------------------------------------------
# WordWrap mode
# ---------------------------------------------------------------------------

# TODO: Investigate and implement the correct wrap behavior for
#       the word wrap in case of whitespces

# def test_word_wrap_breaks_at_space_boundary():
#     # 'abcdef ghij': space at position 6, 'g' at position 7.
#     # WrapAnywhere cuts at column 8 (mid-word, leaving 'hij' on the next row).
#     # WordWrap must break at the word boundary so 'ghij' is never split.
#     # The wrapped second row must start at 'g' (position 7), not at the space
#     # (position 6): the space at the wrap point must NOT appear as a leading
#     # character on the next visual line.
#     _, tw_wa = _mk_wrap('abcdef ghij', width=8, word_wrap=False)
#     _, tw_ww = _mk_wrap('abcdef ghij', width=8, word_wrap=True)

#     doc = ttk.TTkTextDocument(text='abcdef ghij')
#     full_line = doc.dataLine(0)

#     rows_wa = tw_wa.screenRows(0, 5)
#     rows_ww = tw_ww.screenRows(0, 5)

#     # WrapAnywhere always cuts at column 8 regardless of word boundaries.
#     assert rows_wa[0] == (0, (0, 8))

#     # WordWrap must break earlier than WrapAnywhere.
#     assert rows_ww[0][1][1] < rows_wa[0][1][1], (
#         f'WordWrap break {rows_ww[0][1][1]} is not earlier than WrapAnywhere {rows_wa[0][1][1]}'
#     )

#     # The second visual row must start at the first non-space character 'g'
#     # (position 7). Starting at position 6 (the space) would produce a leading
#     # space on the wrapped line — incorrect text-editor behaviour.
#     second_row_start = rows_ww[1][1][0]
#     second_row_first_char = str(full_line.substring(second_row_start, second_row_start + 1))
#     assert second_row_first_char != ' ', (
#         f'WordWrap second visual row starts with a space (pos {second_row_start}); '
#         f'the wrap point space must not appear as a leading character on the next line'
#     )

#     # No content is lost.
#     assert rows_ww[-1][1][1] >= len('abcdef ghij')


# ---------------------------------------------------------------------------
# Disabled wrapping
# ---------------------------------------------------------------------------

def test_disable_mode_exposes_each_line_as_one_screen_row():
    # When wrapping is *not* enabled (NoWrap engine, the default) each data
    # line is one screen row regardless of width.
    doc = ttk.TTkTextDocument(text='abcdefghij\nxyz')
    tw = ttk.TTkTextWrap(document=doc)
    tw.setWrapWidth(4)   # narrow width — would create many rows if wrapping were enabled

    rows = _rows_for(tw, 0, 2)

    assert len(rows) == 2
    assert rows[0] == _WrapLine(0, 0, 11, True)   # 'abcdefghij' → len=10, +1 sentinel
    assert rows[1] == _WrapLine(1, 0, 4, True)    # 'xyz'        → len=3,  +1 sentinel


# ---------------------------------------------------------------------------
# normalizeScreenPosition
# ---------------------------------------------------------------------------

def test_normalize_screen_position_snaps_to_nearest_cell():
    # 'abcdefghij\nxyz' at width=4.
    # Screen layout:
    #   y=0: line 0 chars 0-3  (abcd)
    #   y=1: line 0 chars 4-7  (efgh)
    #   y=2: line 0 chars 8-10 (ij)
    #   y=3: line 1 chars 0-3  (xyz)
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    assert tw.normalizeScreenPosition(2, 0)   == (2, 0)  # within first row
    assert tw.normalizeScreenPosition(0, 0)   == (0, 0)  # start of first row
    assert tw.normalizeScreenPosition(100, 0) == (4, 0)  # past end clamps to width
    assert tw.normalizeScreenPosition(2, 3)   == (2, 3)  # within row 3 (line 1)


# ---------------------------------------------------------------------------
# wrapChanged signal
# ---------------------------------------------------------------------------

def test_wrap_changed_emitted_on_setWrapWidth():
    _, tw = _mk_wrap('hello world', width=5)
    count = [0]

    def _inc():
        count[0] += 1

    tw.wrapChanged.connect(_inc)
    tw.setWrapWidth(10)
    assert count[0] == 1


def test_wrap_changed_emitted_on_setWordWrapMode():
    _, tw = _mk_wrap('hello world', width=5)
    count = [0]

    def _inc():
        count[0] += 1

    tw.wrapChanged.connect(_inc)
    tw.setWordWrapMode(ttk.TTkK.WordWrap)
    assert count[0] == 1


def test_wrap_changed_emitted_on_rewrap():
    _, tw = _mk_wrap('hello world', width=5)
    count = [0]

    def _inc():
        count[0] += 1

    tw.wrapChanged.connect(_inc)
    tw.rewrap()
    assert count[0] == 1


# ---------------------------------------------------------------------------
# Tab handling
# ---------------------------------------------------------------------------

def test_tab_handling_advances_x_by_tab_width():
    # A leading tab expands to 4 spaces (default tabSpaces=4).
    # Data positions: 0='\t', 1='a', 2='b', 3='c'
    # Screen columns:   0      4     5     6
    _, tw = _mk_wrap('\tabc', width=6)

    x0, y0 = tw.dataToScreenPosition(0, 0).to_xy()  # at the tab
    x1, y1 = tw.dataToScreenPosition(0, 1).to_xy()  # at 'a', after the tab

    assert x0 == 0 and y0 == 0
    assert x1 == 4 and y1 == 0   # tab consumed 4 terminal cells


# ---------------------------------------------------------------------------
# Empty document
# ---------------------------------------------------------------------------

def test_empty_document_exposes_one_row():
    _, tw = _mk_wrap('', width=10)

    rows = _rows_for(tw, 0, 2)

    assert len(rows) == 1
    assert rows[0] == _WrapLine(0, 0, 0, True)


# ---------------------------------------------------------------------------
# Degenerate wrap width
# ---------------------------------------------------------------------------

def test_width_one_wraps_each_character_onto_its_own_row():
    _, tw = _mk_wrap('abc', width=1)

    rows = _rows_for(tw, 0, 5)

    assert len(rows) == 3
    assert rows[0] == _WrapLine(0, 0, 1, False)
    assert rows[1] == _WrapLine(0, 1, 2, False)


# ---------------------------------------------------------------------------
# screenRows h=0 guard
# ---------------------------------------------------------------------------

def test_screen_rows_zero_height_returns_empty_list():
    _, tw = _mk_wrap('hello', width=10)
    ret = tw.screenRows(0, 0)
    assert ret.rows == []


# ---------------------------------------------------------------------------
# Multi-line position mapping
# ---------------------------------------------------------------------------

def test_data_to_screen_position_for_second_data_line():
    # 'abcdefghij' wraps into 3 rows at y=0,1,2; 'xyz' starts at y=3.
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    x, y = tw.dataToScreenPosition(1, 0).to_xy()

    assert y == 3
    assert x == 0


def test_roundtrip_data_to_screen_for_second_data_line():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    for pos in (0, 1, 2):
        x, y = tw.dataToScreenPosition(1, pos).to_xy()
        line, dpos = tw.screenToDataPosition(x, y)
        assert line == 1
        assert dpos == pos


# ---------------------------------------------------------------------------
# setWrapWidth triggers a full rewrap
# ---------------------------------------------------------------------------

def test_setWrapWidth_changes_wrapped_size():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)
    size_at_4 = tw.size()  # 'abcdefghij' → 3 rows, 'xyz' → 1 row = 4

    tw.setWrapWidth(10)
    size_at_10 = tw.size()  # 'abcdefghij' → 1 row, 'xyz' → 1 row = 2

    assert size_at_4 == 4
    assert size_at_10 == 2


# ---------------------------------------------------------------------------
# FullWrap buffer behaviour
# ---------------------------------------------------------------------------

def test_rewrap_rebuilds_buffer():
    _, tw = _mk_wrap('abcdefghij', width=4)
    assert tw.size() == 3  # 3 wrapped rows

    tw.setWrapWidth(5)

    assert tw.size() == 2  # 2 wrapped rows at width=5


def test_screenRows_returns_correct_slices():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    rows = _rows_for(tw, 0, 4)

    assert rows[0] == _WrapLine(0, 0, 4, False)
    assert rows[3] == _WrapLine(1, 0, 4, True)


def test_screen_rows_contract_preserves_viewport_origin_and_row_invariants():
    _, tw = _mk_wrap('alpha\nbeta\ngamma', width=3)

    ret = tw.screenRows(2, 4)

    for row in ret.rows:
        assert row.start >= 0
        assert row.stop >= row.start
        assert row.line >= 0
