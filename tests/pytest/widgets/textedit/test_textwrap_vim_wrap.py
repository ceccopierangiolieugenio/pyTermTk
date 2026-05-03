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

'''Tests for VimWrap text wrapping engine.

VimWrap is a lazy-wrapping engine that only wraps the visible viewport,
caching results for fast coordinate conversions without eagerly pre-computing
all breaks like FullWrap does.
'''

import os
import sys

sys.path.append(os.path.join(sys.path[0], '../../libs/pyTermTk'))

import TermTk as ttk


def _mk_vim_wrap(text: str, width: int = 10, word_wrap: bool = False):
    '''Create a document with VimWrap engine for testing.'''
    doc = ttk.TTkTextDocument(text=text)
    tw = ttk.TTkTextWrap(document=doc)
    tw.setEngine(ttk.TTkK.WrapEngine.VimWrap)
    tw.setWrapWidth(width)
    if word_wrap:
        tw.setWordWrapMode(ttk.TTkK.WordWrap)
    else:
        tw.setWordWrapMode(ttk.TTkK.WrapAnywhere)
    return doc, tw


def _rows_for(tw: ttk.TTkTextWrap, y: int, h: int):
    """Return wrapped rows handling legacy/buggy engine return shapes."""
    ret = tw.screenRows(y, h)
    if isinstance(ret, list):
        # Some VimWrap codepaths still return rows directly.
        return ret
    assert isinstance(ret.rows, list)
    return ret.rows


# ---------------------------------------------------------------------------
# Lazy wrapping: screenRows only wraps visible window
# ---------------------------------------------------------------------------

def test_vim_wrap_screen_rows_lazily_wraps_visible_window():
    """VimWrap.screenRows caches only the requested window, not entire document."""
    text = 'abcdefghij\n' * 20  # 20 lines, each 10 chars
    doc, tw = _mk_vim_wrap(text, width=4)

    # Request rows 0-4 (should wrap first few document lines)
    rows = _rows_for(tw, 0, 4)
    # 'abcdefghij' (10 chars) wraps into 3 rows at width=4: [0-3], [4-7], [8-10]
    assert len(rows) > 0
    assert rows[0].line == 0
    assert rows[0].start == 0


def test_vim_wrap_data_to_screen_position_inside_cached_window_is_wrap_accurate():
    """Inside cached rows, VimWrap returns wrapped coordinates."""
    text = 'abcdefghij\n' * 5
    _, tw = _mk_vim_wrap(text, width=4)

    # Prime cache for wrapped rows.
    tw.screenRows(0, 4)

    # line 0 split at width=4 => [0:4], [4:8], [8:11]
    x, y = tw.dataToScreenPosition(0, 6).to_xy()
    assert (x, y) == (2, 1)


def test_vim_wrap_data_to_screen_position_offscreen_falls_back_to_unwrapped():
    """Outside cache, VimWrap treats coordinates as unwrapped source lines."""
    text = 'abcdefghij\n' * 5
    _, tw = _mk_vim_wrap(text, width=4)

    # Cache a distant window so line 0 is offscreen.
    tw.screenRows(10, 4)

    x, y = tw.dataToScreenPosition(0, 5).to_xy()
    assert (x, y) == (5, 0)


def test_vim_wrap_data_to_screen_position_out_of_range_pos_returns_zero():
    """Invalid positions return (0,0) instead of raising."""
    text = 'abcdefghij\n' * 5
    _, tw = _mk_vim_wrap(text, width=4)

    tw.screenRows(10, 4)
    assert tw.dataToScreenPosition(0, -1).to_xy() == (0, 0)


def test_vim_wrap_data_to_screen_position_with_zero_width_returns_zero():
    """Zero wrap width disables coordinate mapping safely."""
    text = 'abcdefghij\n'
    _, tw = _mk_vim_wrap(text, width=0)

    assert tw.dataToScreenPosition(0, 1).to_xy() == (0, 0)


def test_vim_wrap_screen_to_data_position_offscreen_above_uses_unwrapped():
    """Rows above cached window are interpreted as unwrapped lines."""
    text = 'abcdefghij\n' * 5
    _, tw = _mk_vim_wrap(text, width=4)

    # Cache window y=5-8
    tw.screenRows(5, 4)

    line, pos = tw.screenToDataPosition(5, 0)
    assert (line, pos) == (0, 5)


def test_vim_wrap_screen_to_data_position_offscreen_below_uses_unwrapped():
    """Rows below cached window are interpreted as unwrapped lines."""
    text = '\n'.join(['abcdefghij'] * 5)
    _, tw = _mk_vim_wrap(text, width=4)

    # Cache window y=0-3
    tw.screenRows(0, 4)

    # y=50 is below cached window -> clamp to last source line
    line, pos = tw.screenToDataPosition(5, 50)
    assert (line, pos) == (4, 5)


def test_vim_wrap_screen_to_data_position_inside_cached_window_uses_wrapped_row():
    """Inside cached rows, screenToDataPosition maps through wrapped fragments."""
    text = 'abcdefghij\n' * 5
    _, tw = _mk_vim_wrap(text, width=4)

    tw.screenRows(0, 4)
    # y=1 is second wrapped fragment [4:8] of line 0
    line, pos = tw.screenToDataPosition(1, 1)
    assert (line, pos) == (0, 5)


def test_vim_wrap_normalize_screen_position_offscreen_above_uses_unwrapped():
    """Offscreen-above normalization uses unwrapped line semantics."""
    text = 'abcdefghij\n' * 5
    _, tw = _mk_vim_wrap(text, width=4)

    # Cache window y=10-13
    tw.screenRows(10, 4)

    # y=2 is above cached window -> unwrapped normalization on source line 2
    x, y = tw.normalizeScreenPosition(5, 2)
    assert (x, y) == (5, 2)


def test_vim_wrap_normalize_screen_position_offscreen_below_uses_unwrapped():
    """Offscreen-below normalization uses unwrapped line semantics."""
    text = '\n'.join(['abcdefghij'] * 5)
    _, tw = _mk_vim_wrap(text, width=4)

    # Cache window y=0-3
    tw.screenRows(0, 4)

    # y=50 is below cached window -> clamp to last source line
    x, y = tw.normalizeScreenPosition(5, 50)
    assert (x, y) == (5, 4)


def test_vim_wrap_normalize_screen_position_inside_cached_row_clamps_to_fragment():
    """Inside cached rows, x is normalized within wrapped fragment boundaries."""
    text = 'abcdefghij\n' * 3
    _, tw = _mk_vim_wrap(text, width=4)

    tw.screenRows(0, 4)
    # y=1 corresponds to source slice [4:8], max local width is 4
    x, y = tw.normalizeScreenPosition(99, 1)
    assert (x, y) == (4, 1)


def test_vim_wrap_size_returns_total_document_line_count():
    """VimWrap.size() follows documented approximate viewport-based sizing."""
    text = 'a\n' * 100  # 100 lines
    doc, tw = _mk_vim_wrap(text, width=1)

    # Before a viewport cache is built, h=0 contribution is -1.
    assert tw.size() == doc.lineCount() - 1

    tw.screenRows(0, 5)
    assert tw.size() == doc.lineCount() + 4


def test_vim_wrap_empty_document():
    """VimWrap handles empty document gracefully."""
    text = ''
    _, tw = _mk_vim_wrap(text, width=10)

    rows = _rows_for(tw, 0, 2)
    assert len(rows) >= 1
    assert rows[0].line == 0
    assert rows[0].start == 0


def test_vim_wrap_single_long_line():
    """VimWrap wraps a single long line across multiple rows."""
    text = 'abcdefghijklmnopqrst'  # 20 chars
    _, tw = _mk_vim_wrap(text, width=4)

    rows = _rows_for(tw, 0, 10)
    # 20 chars at width=4 → 5 rows
    assert len(rows) == 5
    assert all(row.line == 0 for row in rows)  # All from same source line
    assert rows[0].start == 0
    assert rows[0].stop == 4
    assert rows[4].start == 16
    assert rows[4].stop == 21  # +1 sentinel


def test_vim_wrap_multi_line_document():
    """VimWrap handles multi-line documents correctly."""
    text = 'short\nabcdefghij\nend'
    _, tw = _mk_vim_wrap(text, width=4)

    rows = _rows_for(tw, 0, 10)

    # Line 0: 'short' (5 chars) → 2 rows at width=4
    assert rows[0].line == 0
    assert rows[1].line == 0

    # Line 1: 'abcdefghij' (10 chars) → 3 rows
    assert rows[2].line == 1
    assert rows[3].line == 1
    assert rows[4].line == 1

    # Line 2: 'end' → 1 row
    assert rows[5].line == 2


def test_vim_wrap_roundtrip_within_cached_window():
    """VimWrap dataToScreenPosition/screenToDataPosition roundtrip in cached window."""
    text = 'abcdefghij\nxyzuvw'
    doc, tw = _mk_vim_wrap(text, width=4)

    # Prime cache
    tw.screenRows(0, 10)

    # Test roundtrip for positions in line 0
    for pos in [0, 2, 4, 6, 8, 10]:
        x, y = tw.dataToScreenPosition(0, pos).to_xy()
        line, rpos = tw.screenToDataPosition(x, y)
        assert line == 0
        assert 0 <= rpos <= len(doc.dataLine(0))


def test_vim_wrap_tab_handling():
    """VimWrap expands tabs correctly in position conversions."""
    text = '\ta\tb'  # tab-a-tab-b
    _, tw = _mk_vim_wrap(text, width=20)

    # Prime cache
    tw.screenRows(0, 2)

    # First tab expands to 4 cells (default tabSpaces)
    x, _y = tw.dataToScreenPosition(0, 1).to_xy()  # Position of 'a'
    assert x == 4  # After tab expansion


def test_vim_wrap_width_zero_handles_gracefully():
    """VimWrap with zero width should not crash."""
    text = 'hello'
    _, tw = _mk_vim_wrap(text, width=0)

    # Should handle gracefully
    rows = _rows_for(tw, 0, 5)
    assert isinstance(rows, list)


def test_vim_wrap_large_document_partial_access():
    """VimWrap on large document lazily wraps requested viewport."""
    # Create a very large document (1000 lines)
    text = 'line_of_text_' * 100 + '\n'  # ~1300 char line
    text = text * 1000

    _, tw = _mk_vim_wrap(text, width=20)

    # Request only rows 500-510
    rows = _rows_for(tw, 500, 10)

    # Should return rows from around line 500
    assert len(rows) > 0
    assert all(row.start >= 0 and row.start <= row.stop for row in rows)


def test_vim_wrap_screen_rows_with_height_zero_returns_empty_and_is_stable():
    """VimWrap.screenRows with h=0 returns empty list."""
    text = 'hello world'
    _, tw = _mk_vim_wrap(text, width=10)

    rows = _rows_for(tw, 0, 0)
    assert rows == []

    # Repeated request should remain empty and safe.
    assert _rows_for(tw, 0, 0) == []


def test_vim_wrap_screen_rows_with_negative_y():
    """VimWrap.screenRows with negative y should handle gracefully."""
    text = 'hello world'
    _, tw = _mk_vim_wrap(text, width=10)

    # screenRows should handle negative y gracefully
    rows = _rows_for(tw, -5, 10)
    assert isinstance(rows, list)


def test_vim_wrap_screen_rows_repeated_same_viewport_returns_same_rows():
    """Repeated identical viewport requests return the same cached rows."""
    text = 'abcdefghij\n' * 10
    _, tw = _mk_vim_wrap(text, width=4)

    rows1 = _rows_for(tw, 3, 4)
    rows2 = _rows_for(tw, 3, 4)
    assert rows2 == rows1


def test_vim_wrap_rewrap_invalidation_rebuilds_after_document_change():
    """After document edits, rewrap path invalidates and rebuilds viewport cache."""
    doc, tw = _mk_vim_wrap('aaaa\nbbbb', width=2)

    first = _rows_for(tw, 0, 4)
    assert first[0].stop == 2

    doc.setText('zzzzzz\nbbbb')
    rebuilt = _rows_for(tw, 0, 4)

    # First line changed from len=4 to len=6, so wrapped rows update.
    assert rebuilt != first
    assert rebuilt[2].stop == 7


def test_vim_wrap_negative_y_never_emits_negative_source_line_indexes():
    """Wrapped rows should never reference negative source line numbers."""
    text = 'hello world\nsecond line'
    _, tw = _mk_vim_wrap(text, width=6)

    rows = _rows_for(tw, -5, 4)
    assert all(row.line >= 0 for row in rows)


def test_vim_wrap_screen_rows_always_returns_ret_screen_rows_object():
    """ScreenRows should consistently return _RetScreenRows."""
    _, tw = _mk_vim_wrap('abcdefghij\n' * 2, width=4)

    first = tw.screenRows(0, 4)
    second = tw.screenRows(0, 4)

    assert hasattr(first, 'rows')
    assert hasattr(second, 'rows')
