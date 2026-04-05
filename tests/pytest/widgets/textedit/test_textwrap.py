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


def _mk_wrap(text: str, width: int = 4, word_wrap: bool = False):
    doc = ttk.TTkTextDocument(text=text)
    tw = ttk.TTkTextWrap(document=doc)
    tw.enable()
    tw.setWrapWidth(width)
    if word_wrap:
        tw.setWordWrapMode(ttk.TTkK.WordWrap)
    else:
        tw.setWordWrapMode(ttk.TTkK.WrapAnywhere)
    return doc, tw


def test_screen_rows_wrap_anywhere_visible_window():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    rows = tw.screenRows(0, 4)

    assert len(rows) == 4
    assert rows[0] == (0, (0, 4))
    assert rows[1] == (0, (4, 8))
    assert rows[2] == (0, (8, 11))
    assert rows[3] == (1, (0, 4))


def test_data_to_screen_and_back_roundtrip():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    for pos in (0, 3, 4, 7, 9, 10):
        x, y = tw.dataToScreenPosition(0, pos)
        line, dpos = tw.screenToDataPosition(x, y)
        assert line == 0
        assert dpos == pos


def test_invalidate_from_data_line_drops_tail_prefix_cache():
    _, tw = _mk_wrap('line0-abcdefghij\nline1-abcdefghij\nline2-abcdefghij', width=6)

    tw.ensureScreenRows(0, 30)
    assert tw._processedLines == 3
    before_rows = tw._lineStartY[-1]

    tw.invalidateFromDataLine(1)

    assert tw._processedLines == 1
    assert len(tw._lineStartY) == 2
    assert tw._lineStartY[-1] < before_rows
    assert tw._checkpoints[-1][0] == 1
    assert tw._checkpoints[-1][1] == tw._lineStartY[-1]


def test_size_estimate_grows_with_partial_materialization():
    _, tw = _mk_wrap(('abcdefghij\n' * 50).rstrip('\n'), width=4)

    initial = tw.size()
    tw.ensureScreenRows(0, 6)
    after_first = tw.size()
    tw.ensureScreenRows(40, 6)
    after_more = tw.size()

    assert initial >= 50
    assert after_first >= 50
    assert after_more >= after_first


def test_data_to_screen_position_safe_after_document_shrink_before_invalidate():
    doc, tw = _mk_wrap('line0\nline1\nline2', width=4)

    tw.ensureScreenRows(0, 30)
    assert tw._processedLines == 3

    # Simulate signal ordering where the document shrinks before wrap invalidation runs.
    doc.setText('only-one-line')

    x, y = tw.dataToScreenPosition(2, 0)

    assert x >= 0
    assert y >= 0

    doc.clear()

    x, y = tw.dataToScreenPosition(2, 0)

    assert x >= 0
    assert y >= 0


def test_screen_to_data_position_safe_after_document_shrink_with_stale_cache():
    doc, tw = _mk_wrap('line0\nline1\nline2', width=4)

    tw.ensureScreenRows(0, 30)
    assert tw._processedLines == 3

    # Shrink the document while wrap cache still contains stale processed lines.
    doc.setText('x')

    line, pos = tw.screenToDataPosition(0, 2)

    assert line >= 0
    assert pos >= 0


# ---------------------------------------------------------------------------
# WordWrap mode
# ---------------------------------------------------------------------------

# TODO: Investigate and implement the correct wrap behavior for the word wrap in case of whitespces
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
    # When wrapping is *not* enabled each data line is one screen row regardless
    # of width.
    doc = ttk.TTkTextDocument(text='abcdefghij\nxyz')
    tw = ttk.TTkTextWrap(document=doc)
    tw.setWrapWidth(4)   # narrow width — would create many rows if enabled
    # tw.enable() is intentionally NOT called

    rows = tw.screenRows(0, 2)

    assert len(rows) == 2
    assert rows[0] == (0, (0, 11))   # 'abcdefghij' → len=10, +1 sentinel
    assert rows[1] == (1, (0, 4))    # 'xyz'        → len=3,  +1 sentinel


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


def test_wrap_changed_emitted_on_invalidateFromDataLine():
    _, tw = _mk_wrap('hello world', width=5)
    tw.ensureScreenRows(0, 10)
    count = [0]

    def _inc():
        count[0] += 1

    tw.wrapChanged.connect(_inc)
    tw.invalidateFromDataLine(0)
    assert count[0] == 1


# ---------------------------------------------------------------------------
# Tab handling
# ---------------------------------------------------------------------------

def test_tab_handling_advances_x_by_tab_width():
    # A leading tab expands to 4 spaces (default tabSpaces=4).
    # Data positions: 0='\t', 1='a', 2='b', 3='c'
    # Screen columns:   0      4     5     6
    _, tw = _mk_wrap('\tabc', width=6)

    x0, y0 = tw.dataToScreenPosition(0, 0)  # at the tab
    x1, y1 = tw.dataToScreenPosition(0, 1)  # at 'a', after the tab

    assert x0 == 0 and y0 == 0
    assert x1 == 4 and y1 == 0   # tab consumed 4 terminal cells


# ---------------------------------------------------------------------------
# Empty document
# ---------------------------------------------------------------------------

def test_empty_document_exposes_one_row():
    _, tw = _mk_wrap('', width=10)

    rows = tw.screenRows(0, 2)

    assert len(rows) == 1
    assert rows[0] == (0, (0, 0))


# ---------------------------------------------------------------------------
# Degenerate wrap width
# ---------------------------------------------------------------------------

def test_width_one_wraps_each_character_onto_its_own_row():
    _, tw = _mk_wrap('abc', width=1)

    rows = tw.screenRows(0, 5)

    assert len(rows) == 3
    assert rows[0] == (0, (0, 1))
    assert rows[1] == (0, (1, 2))


# ---------------------------------------------------------------------------
# screenRows h=0 guard
# ---------------------------------------------------------------------------

def test_screen_rows_zero_height_returns_empty_list():
    _, tw = _mk_wrap('hello', width=10)
    assert tw.screenRows(0, 0) == []


# ---------------------------------------------------------------------------
# Multi-line position mapping
# ---------------------------------------------------------------------------

def test_data_to_screen_position_for_second_data_line():
    # 'abcdefghij' wraps into 3 rows at y=0,1,2; 'xyz' starts at y=3.
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    x, y = tw.dataToScreenPosition(1, 0)

    assert y == 3
    assert x == 0


def test_roundtrip_data_to_screen_for_second_data_line():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)

    for pos in (0, 1, 2):
        x, y = tw.dataToScreenPosition(1, pos)
        line, dpos = tw.screenToDataPosition(x, y)
        assert line == 1
        assert dpos == pos


# ---------------------------------------------------------------------------
# setWrapWidth resets the wrap cache
# ---------------------------------------------------------------------------

def test_setWrapWidth_resets_processed_lines_cache():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)
    tw.ensureScreenRows(0, 10)
    assert tw._processedLines == 2

    tw.setWrapWidth(10)

    assert tw._processedLines == 0


# ---------------------------------------------------------------------------
# _wrapCache behaviour
# ---------------------------------------------------------------------------

def test_wrapLine_cache_returns_same_object_on_second_call():
    doc, tw = _mk_wrap('abcdefghij\nxyz', width=4)
    tw.ensureScreenRows(0, 10)

    line0 = doc.dataLine(0)
    first = tw._wrapLine(0, line0)
    second = tw._wrapLine(0, line0)

    assert first is second


def test_invalidateAll_clears_wrap_cache():
    _, tw = _mk_wrap('abcdefghij\nxyz', width=4)
    tw.ensureScreenRows(0, 10)
    assert len(tw._wrapCache) > 0

    tw._invalidateAll()

    assert tw._wrapCache == {}


def test_invalidateFromDataLine_evicts_lines_ge_threshold():
    _, tw = _mk_wrap('line0-abcdefghij\nline1-abcdefghij\nline2-abcdefghij', width=6)
    tw.ensureScreenRows(0, 30)
    assert 0 in tw._wrapCache
    assert 1 in tw._wrapCache
    assert 2 in tw._wrapCache

    tw._invalidateFromDataLine(1)

    assert 0 in tw._wrapCache
    assert 1 not in tw._wrapCache
    assert 2 not in tw._wrapCache


def test_rewrap_clears_wrap_cache():
    _, tw = _mk_wrap('abcdefghij', width=4)
    tw.ensureScreenRows(0, 10)
    assert len(tw._wrapCache) > 0

    tw.rewrap()

    assert tw._wrapCache == {}


def test_screenRows_reuses_cached_wrapLine_results():
    doc, tw = _mk_wrap('abcdefghij\nxyz', width=4)
    tw.ensureScreenRows(0, 10)

    cached_line0 = tw._wrapCache.get(0)
    assert cached_line0 is not None

    rows = tw.screenRows(0, 4)

    assert tw._wrapCache[0] is cached_line0
    assert rows[0] == (0, (0, 4))
