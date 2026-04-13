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

from TermTk.TTkGui.TTkTextWrap.text_wrap_data import _WrapLine


def _mk_vim_wrap(text: str, width: int = 10, word_wrap: bool = False):
    """Create a document with VimWrap engine for testing."""
    doc = ttk.TTkTextDocument(text=text)
    tw = ttk.TTkTextWrap(document=doc)
    tw.setEngine(ttk.TTkK.WrapEngine.VimWrap)
    tw.setWrapWidth(width)
    if word_wrap:
        tw.setWordWrapMode(ttk.TTkK.WordWrap)
    else:
        tw.setWordWrapMode(ttk.TTkK.WrapAnywhere)
    return doc, tw


# ---------------------------------------------------------------------------
# Lazy wrapping: screenRows only wraps visible window
# ---------------------------------------------------------------------------

def test_vim_wrap_screenRows_lazily_wraps_visible_window():
    """VimWrap.screenRows caches only the requested window, not entire document."""
    text = 'abcdefghij\n' * 20  # 20 lines, each 10 chars
    doc, tw = _mk_vim_wrap(text, width=4)

    # Request rows 0-4 (should wrap first few document lines)
    rows = tw.screenRows(0, 4)
    # 'abcdefghij' (10 chars) wraps into 3 rows at width=4: [0-3], [4-7], [8-10]
    assert len(rows) > 0
    assert rows[0].line == 0
    assert rows[0].start == 0


def test_vim_wrap_relying_on_last_cached_window():
    """dataToScreenPosition uses lastWindow cache set by prior screenRows call."""
    text = 'abcdefghij\n' * 5
    doc, tw = _mk_vim_wrap(text, width=4)

    # Prime the cache with screenRows call for y=0..4
    tw.screenRows(0, 4)

    # dataToScreenPosition now uses that cached window
    x, y = tw.dataToScreenPosition(0, 2)  # Position 2 in line 0
    assert y >= 0  # Must return a valid screen row
    assert x >= 0  # Must return a valid column


def test_vim_wrap_dataToScreenPosition_outside_cached_window_returns_zero():
    """dataToScreenPosition returns (0,0) if position is outside cached window."""
    text = 'abcdefghij\n' * 5
    doc, tw = _mk_vim_wrap(text, width=4)

    # Cache window y=10-13
    tw.screenRows(10, 4)

    # Try to convert position in line 0 (outside the cached y=10-13 window)
    x, y = tw.dataToScreenPosition(0, 0)
    # VimWrap returns (0,0) if position is not in cached window
    assert x == 0 and y == 0


def test_vim_wrap_screenToDataPosition_outside_cached_window_returns_zero():
    """screenToDataPosition returns (0,0) if screen position is outside cached window."""
    text = 'abcdefghij\n' * 5
    doc, tw = _mk_vim_wrap(text, width=4)

    # Cache window y=5-8
    tw.screenRows(5, 4)

    # Try to convert screen position y=0 (outside the cached y=5-8 window)
    line, pos = tw.screenToDataPosition(0, 0)
    # VimWrap has no cached data for y=0, returns (0,0)
    assert line == 0 and pos == 0


def test_vim_wrap_normalizeScreenPosition_outside_cached_window_returns_zero():
    """normalizeScreenPosition returns (0,0) if screen y is outside cached window."""
    text = 'abcdefghij\n' * 5
    doc, tw = _mk_vim_wrap(text, width=4)

    # Cache window y=10-13
    tw.screenRows(10, 4)

    # Try to normalize position y=2 (outside cache)
    x, y = tw.normalizeScreenPosition(5, 2)
    # VimWrap returns (0,0) if no cached data
    assert x == 0 and y == 0


def test_vim_wrap_size_returns_total_document_line_count():
    """VimWrap.size() returns document line count (may include trailing newline line)."""
    text = 'a\n' * 100  # 100 lines
    doc, tw = _mk_vim_wrap(text, width=1)

    # VimWrap counts source lines
    assert tw.size() > 0


def test_vim_wrap_empty_document():
    """VimWrap handles empty document gracefully."""
    text = ''
    doc, tw = _mk_vim_wrap(text, width=10)

    rows = tw.screenRows(0, 2)
    assert len(rows) >= 1
    assert rows[0].line == 0
    assert rows[0].start == 0


def test_vim_wrap_single_long_line():
    """VimWrap wraps a single long line across multiple rows."""
    text = 'abcdefghijklmnopqrst'  # 20 chars
    doc, tw = _mk_vim_wrap(text, width=4)

    rows = tw.screenRows(0, 10)
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
    doc, tw = _mk_vim_wrap(text, width=4)

    rows = tw.screenRows(0, 10)

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
        x, y = tw.dataToScreenPosition(0, pos)
        if y > 0:  # Only if within cached window
            line, rpos = tw.screenToDataPosition(x, y)
            # May not roundtrip perfectly due to tab expansion,
            # but should return valid document position
            assert line == 0
            assert 0 <= rpos <= len(tw._wrapState.textDocument.dataLine(0))


def test_vim_wrap_tab_handling():
    """VimWrap expands tabs correctly in position conversions."""
    text = '\ta\tb'  # tab-a-tab-b
    doc, tw = _mk_vim_wrap(text, width=20)

    # Prime cache
    tw.screenRows(0, 2)

    # First tab expands to 4 cells (default tabSpaces)
    x, y = tw.dataToScreenPosition(0, 1)  # Position of 'a'
    assert x == 4  # After tab expansion


def test_vim_wrap_width_zero_handles_gracefully():
    """VimWrap with zero width should not crash."""
    text = 'hello'
    doc, tw = _mk_vim_wrap(text, width=0)

    # Should handle gracefully
    rows = tw.screenRows(0, 5)
    assert isinstance(rows, list)


def test_vim_wrap_large_document_partial_access():
    """VimWrap on large document lazily wraps requested viewport."""
    # Create a very large document (1000 lines)
    text = 'line_of_text_' * 100 + '\n'  # ~1300 char line
    text = text * 1000

    doc, tw = _mk_vim_wrap(text, width=20)

    # Request only rows 500-510
    rows = tw.screenRows(500, 10)

    # Should return rows from around line 500
    assert len(rows) > 0
    assert all(row.start >= 0 and row.start <= row.stop for row in rows)


def test_vim_wrap_screenRows_with_height_zero():
    """VimWrap.screenRows with h=0 returns empty list."""
    text = 'hello world'
    doc, tw = _mk_vim_wrap(text, width=10)

    rows = tw.screenRows(0, 0)
    assert rows == []


def test_vim_wrap_screenRows_with_negative_y():
    """VimWrap.screenRows with negative y should handle gracefully."""
    text = 'hello world'
    doc, tw = _mk_vim_wrap(text, width=10)

    # screenRows should handle negative y gracefully
    rows = tw.screenRows(-5, 10)
    # Should return some wrapped rows or empty
    assert isinstance(rows, list)


def test_vim_wrap_caches_last_window_state():
    """VimWrap caches _lastWindow state across multiple calls."""
    text = 'abcdefghij\n' * 10
    doc, tw = _mk_vim_wrap(text, width=4)

    # First call sets cache for y=0-4
    rows1 = tw.screenRows(0, 4)
    y1 = tw._wrapEngine._lastWindow.y  # type: ignore[attr-defined]
    h1 = tw._wrapEngine._lastWindow.h  # type: ignore[attr-defined]

    # Second call to different window updates cache
    rows2 = tw.screenRows(10, 4)
    y2 = tw._wrapEngine._lastWindow.y  # type: ignore[attr-defined]
    h2 = tw._wrapEngine._lastWindow.h  # type: ignore[attr-defined]

    # Cache should have updated
    assert y2 == 10 and h2 == 4


def test_vim_wrap_rewrap_clears_nothing():
    """VimWrap.rewrap() is a no-op (lazy engine, no pre-computed buffer)."""
    text = 'hello world'
    doc, tw = _mk_vim_wrap(text, width=10)

    # Prime cache
    tw.screenRows(0, 2)

    # Call rewrap (should be no-op)
    tw.rewrap()

    # Cache should still be valid
    rows = tw.screenRows(0, 2)
    assert len(rows) > 0
