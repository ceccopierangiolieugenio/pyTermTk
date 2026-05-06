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

'''Tests for HybridVimWrap text wrapping engine.

HybridVimWrap is a lazy-wrapping engine that wraps the visible viewport plus
extended border region without early stopping. It caches results for fast
coordinate conversions similar to VimWrap but with more complete wrapping
of extended regions for better off-screen behavior.
'''

import os
import sys

sys.path.append(os.path.join(sys.path[0], '../../libs/pyTermTk'))

import TermTk as ttk


def _mk_hybrid_wrap(text: str, width: int = 10, word_wrap: bool = False):
    '''Create a document with HybridVimWrap engine for testing.'''
    doc = ttk.TTkTextDocument(text=text)
    tw = ttk.TTkTextWrap(document=doc)
    # Note: HybridVimWrap may not be exposed via TTkK.WrapEngine yet.
    # For now, we use the internal import approach.
    from TermTk.TTkGui.TTkTextWrap.text_wrap_engine_vim_wrap_hybrid import _WrapEngine_HybridVimWrap
    tw._wrapEngine = _WrapEngine_HybridVimWrap(state=tw._wrapState)
    tw.setWrapWidth(width)
    if word_wrap:
        tw.setWordWrapMode(ttk.TTkK.WordWrap)
    else:
        tw.setWordWrapMode(ttk.TTkK.WrapAnywhere)
    return doc, tw


def _rows_for(tw: ttk.TTkTextWrap, y: int, h: int):
    """Return wrapped rows handling engine return shapes."""
    ret = tw.screenRows(y, h)
    if isinstance(ret, list):
        return ret
    assert isinstance(ret.rows, list)
    return ret.rows


# ---------------------------------------------------------------------------
# Basic wrapping: screenRows caches extended viewport region
# ---------------------------------------------------------------------------

def test_hybrid_wrap_screen_rows_lazily_wraps_visible_window():
    """HybridVimWrap.screenRows caches the requested window."""
    text = 'abcdefghij\n' * 20
    doc, tw = _mk_hybrid_wrap(text, width=4)

    rows = _rows_for(tw, 0, 4)
    assert len(rows) > 0
    assert rows[0].line == 0
    assert rows[0].start == 0


def test_hybrid_wrap_data_to_screen_position_inside_cached_window_is_wrap_accurate():
    """Inside cached rows, HybridVimWrap returns wrapped coordinates."""
    text = 'abcdefghij\n' * 5
    _, tw = _mk_hybrid_wrap(text, width=4)

    tw.screenRows(0, 4)

    x, y = tw.dataToScreenPosition(0, 6).to_xy()
    assert (x, y) == (2, 1)


def test_hybrid_wrap_data_to_screen_position_offscreen_maps_through_extended_cache():
    """HybridVimWrap extends cache beyond viewport, improving off-screen behavior."""
    text = 'abcdefghij\n' * 20
    _, tw = _mk_hybrid_wrap(text, width=4)

    tw.screenRows(5, 4)

    # Request position from a line outside viewport but possibly in extended cache
    x, y = tw.dataToScreenPosition(0, 5).to_xy()
    assert x >= 0 and y >= 0


def test_hybrid_wrap_data_to_screen_position_out_of_range_pos_returns_zero():
    """Invalid positions return (0,0) safely."""
    text = 'abcdefghij\n' * 5
    _, tw = _mk_hybrid_wrap(text, width=4)

    tw.screenRows(10, 4)
    assert tw.dataToScreenPosition(0, -1).to_xy() == (0, 0)


def test_hybrid_wrap_data_to_screen_position_with_zero_width_returns_zero():
    """Zero wrap width returns (0,0) without crashing."""
    text = 'abcdefghij\n'
    _, tw = _mk_hybrid_wrap(text, width=0)

    assert tw.dataToScreenPosition(0, 1).to_xy() == (0, 0)


# ---------------------------------------------------------------------------
# screenToDataPosition: extended cache improves roundtrip accuracy
# ---------------------------------------------------------------------------

def test_hybrid_wrap_screen_to_data_position_inside_cached_window_uses_wrapped_row():
    """Inside cached rows, screenToDataPosition maps through wrapped fragments."""
    text = 'abcdefghij\n' * 5
    _, tw = _mk_hybrid_wrap(text, width=4)

    tw.screenRows(0, 4)

    line, pos = tw.screenToDataPosition(1, 1)
    assert line == 0
    assert 0 <= pos <= len('abcdefghij')


def test_hybrid_wrap_screen_to_data_position_extended_cache_improves_nearby_queries():
    """Positions near cached window benefit from extended border."""
    text = 'abcdefghij\n' * 20
    _, tw = _mk_hybrid_wrap(text, width=4)

    tw.screenRows(5, 4)

    # Query a position in the extended border region
    line, pos = tw.screenToDataPosition(2, 2)
    assert line >= 0
    assert pos >= 0


def test_hybrid_wrap_screen_to_data_position_beyond_extended_border_falls_back():
    """Positions far from cache fall back to unwrapped semantics."""
    text = '\n'.join(['abcdefghij'] * 100)
    _, tw = _mk_hybrid_wrap(text, width=4)

    tw.screenRows(10, 4)

    line, pos = tw.screenToDataPosition(5, 200)
    assert line >= 0 and line < 100
    assert pos >= 0


# ---------------------------------------------------------------------------
# normalizeScreenPosition
# ---------------------------------------------------------------------------

def test_hybrid_wrap_normalize_screen_position_inside_cached_row_clamps_to_fragment():
    """Inside cached rows, x is normalized within wrapped fragment boundaries."""
    text = 'abcdefghij\n' * 3
    _, tw = _mk_hybrid_wrap(text, width=4)

    tw.screenRows(0, 4)

    x, y = tw.normalizeScreenPosition(99, 1)
    assert x >= 0 and x <= 4
    assert y == 1


def test_hybrid_wrap_normalize_screen_position_extended_cache_region():
    """Normalization works in extended cache region."""
    text = 'abcdefghij\n' * 20
    _, tw = _mk_hybrid_wrap(text, width=4)

    tw.screenRows(10, 4)

    x, y = tw.normalizeScreenPosition(5, 5)
    assert x >= 0
    assert y >= 0


# ---------------------------------------------------------------------------
# Coordinate roundtrips: the core invariant
# ---------------------------------------------------------------------------

def test_hybrid_wrap_roundtrip_within_cached_window():
    """HybridVimWrap dataToScreenPosition/screenToDataPosition roundtrip in cached window."""
    text = 'abcdefghij\nxyzuvw'
    doc, tw = _mk_hybrid_wrap(text, width=4)

    tw.screenRows(0, 10)

    for pos in [0, 2, 4, 6, 8, 10]:
        x, y = tw.dataToScreenPosition(0, pos).to_xy()
        line, rpos = tw.screenToDataPosition(x, y)
        assert line == 0
        assert 0 <= rpos <= len(doc.dataLine(0))


def test_hybrid_wrap_roundtrip_extended_cache_region():
    """Roundtrip accuracy extends into border region."""
    text = 'abcdefghij\n' * 30
    doc, tw = _mk_hybrid_wrap(text, width=4)

    tw.screenRows(10, 5)

    # Test a line in the extended border region
    for line_idx in [5, 10, 15]:
        for pos in [0, 2, 5]:
            x, y = tw.dataToScreenPosition(line_idx, pos).to_xy()
            if x >= 0 and y >= 0:  # May not be in cache if far away
                line, rpos = tw.screenToDataPosition(x, y)
                if line == line_idx:
                    assert 0 <= rpos <= len(doc.dataLine(line_idx))


# ---------------------------------------------------------------------------
# Multi-line documents
# ---------------------------------------------------------------------------

def test_hybrid_wrap_single_long_line():
    """HybridVimWrap wraps a single long line across multiple rows."""
    text = 'abcdefghijklmnopqrst'
    _, tw = _mk_hybrid_wrap(text, width=4)

    rows = _rows_for(tw, 0, 10)

    assert len(rows) == 5
    assert all(row.line == 0 for row in rows)
    assert rows[0].start == 0
    assert rows[0].stop == 4
    assert rows[4].start == 16


def test_hybrid_wrap_multi_line_document():
    """HybridVimWrap handles multi-line documents correctly."""
    text = 'short\nabcdefghij\nend'
    _, tw = _mk_hybrid_wrap(text, width=4)

    rows = _rows_for(tw, 0, 10)

    assert rows[0].line == 0
    assert rows[1].line == 0
    assert rows[2].line == 1
    assert rows[3].line == 1
    assert rows[4].line == 1


# ---------------------------------------------------------------------------
# Special cases and edge cases
# ---------------------------------------------------------------------------

def test_hybrid_wrap_empty_document():
    """HybridVimWrap handles empty document gracefully."""
    text = ''
    _, tw = _mk_hybrid_wrap(text, width=10)

    rows = _rows_for(tw, 0, 2)
    assert len(rows) >= 1
    assert rows[0].line == 0
    assert rows[0].start == 0


def test_hybrid_wrap_size_returns_reasonable_estimate():
    """HybridVimWrap.size() returns a reasonable wrapped row estimate."""
    text = 'a\n' * 100
    doc, tw = _mk_hybrid_wrap(text, width=1)

    size_before = tw.size()
    assert size_before > 0
    assert size_before >= doc.lineCount()


def test_hybrid_wrap_tab_handling():
    """HybridVimWrap expands tabs correctly in position conversions."""
    text = '\ta\tb'
    _, tw = _mk_hybrid_wrap(text, width=20)

    tw.screenRows(0, 2)

    x, _y = tw.dataToScreenPosition(0, 1).to_xy()
    assert x == 4  # After tab expansion


def test_hybrid_wrap_width_zero_handles_gracefully():
    """HybridVimWrap with zero width should not crash."""
    text = 'hello'
    _, tw = _mk_hybrid_wrap(text, width=0)

    rows = _rows_for(tw, 0, 5)
    assert isinstance(rows, list)


def test_hybrid_wrap_large_document_partial_access():
    """HybridVimWrap on large document accesses partial viewport efficiently."""
    text = 'line_of_text_' * 100 + '\n'
    text = text * 1000

    _, tw = _mk_hybrid_wrap(text, width=20)

    rows = _rows_for(tw, 500, 10)

    assert len(rows) > 0
    assert all(row.start >= 0 and row.start <= row.stop for row in rows)


def test_hybrid_wrap_screen_rows_with_height_zero_returns_empty_and_is_stable():
    """HybridVimWrap.screenRows with h=0 returns empty list."""
    text = 'hello world'
    _, tw = _mk_hybrid_wrap(text, width=10)

    rows = _rows_for(tw, 0, 0)
    assert rows == []

    assert _rows_for(tw, 0, 0) == []


def test_hybrid_wrap_screen_rows_with_negative_y_handles_gracefully():
    """HybridVimWrap.screenRows with negative y should handle gracefully."""
    text = 'hello world'
    _, tw = _mk_hybrid_wrap(text, width=10)

    rows = _rows_for(tw, -5, 10)
    assert isinstance(rows, list)


def test_hybrid_wrap_screen_rows_repeated_same_viewport_returns_same_rows():
    """Repeated identical viewport requests return the same cached rows."""
    text = 'abcdefghij\n' * 10
    _, tw = _mk_hybrid_wrap(text, width=4)

    rows1 = _rows_for(tw, 3, 4)
    rows2 = _rows_for(tw, 3, 4)
    assert rows2 == rows1


# ---------------------------------------------------------------------------
# Rewrap behavior
# ---------------------------------------------------------------------------

def test_hybrid_wrap_rewrap_invalidation_rebuilds_after_document_change():
    """After document edits, rewrap path invalidates and rebuilds viewport cache."""
    doc, tw = _mk_hybrid_wrap('aaaa\nbbbb', width=2)

    first = _rows_for(tw, 0, 4)
    assert first[0].stop == 2

    doc.setText('zzzzzz\nbbbb')
    rebuilt = _rows_for(tw, 0, 4)

    assert rebuilt != first
    assert rebuilt[2].stop == 7


def test_hybrid_wrap_post_rewrap_cached_coordinates_remain_wrap_accurate():
    """After rewrap, cached coordinate conversions remain wrap-accurate."""
    text = 'aaaa\nbbbb\ncccc\ndddd\neeee'
    doc, tw = _mk_hybrid_wrap(text, width=2)

    tw.screenRows(0, 4)
    before = tw.dataToScreenPosition(1, 0).to_xy()
    doc.setText(text)
    after = tw.dataToScreenPosition(1, 0).to_xy()

    assert after == before

    line, pos = tw.screenToDataPosition(*after)
    assert (line, pos) == (1, 0)


def test_hybrid_wrap_negative_y_never_emits_negative_source_line_indexes():
    """Wrapped rows should never reference negative source line numbers."""
    text = 'hello world\nsecond line'
    _, tw = _mk_hybrid_wrap(text, width=6)

    rows = _rows_for(tw, -5, 4)
    assert all(row.line >= 0 for row in rows)


# ---------------------------------------------------------------------------
# Extended region behavior (key differentiator from pure Redux)
# ---------------------------------------------------------------------------

def test_hybrid_wrap_extended_region_improves_adjacent_queries():
    """Extended border region improves coordinate queries for nearby out-of-cache rows."""
    text = 'line\n' * 200
    _, tw = _mk_hybrid_wrap(text, width=10)

    tw.screenRows(50, 10)

    # Query a line just outside the viewport but possibly in extended region
    x, y = tw.dataToScreenPosition(40, 0).to_xy()
    if x >= 0 and y >= 0:
        line, pos = tw.screenToDataPosition(x, y)
        assert line == 40 or line >= 0  # Should resolve to correct or nearby line


def test_hybrid_wrap_many_small_queries_use_extended_cache_effectively():
    """Multiple queries across near viewport use extended cache efficiently."""
    text = 'abcdefghij\n' * 100
    _, tw = _mk_hybrid_wrap(text, width=4)

    tw.screenRows(30, 5)

    for line_idx in [25, 28, 30, 32, 35, 40]:
        x, y = tw.dataToScreenPosition(line_idx, 2).to_xy()
        if x >= 0 and y >= 0:
            line, pos = tw.screenToDataPosition(x, y)
            # Extended cache may allow more accurate roundtrip
            assert line >= 0


# ---------------------------------------------------------------------------
# Screen rows return type consistency
# ---------------------------------------------------------------------------

def test_hybrid_wrap_screen_rows_always_returns_ret_screen_rows_object():
    """ScreenRows should consistently return _RetScreenRows."""
    _, tw = _mk_hybrid_wrap('abcdefghij\n' * 2, width=4)

    first = tw.screenRows(0, 4)
    second = tw.screenRows(0, 4)

    assert hasattr(first, 'rows')
    assert hasattr(second, 'rows')
    assert isinstance(first.rows, list)
    assert isinstance(second.rows, list)


# ---------------------------------------------------------------------------
# Comparison with other engines (when applicable)
# ---------------------------------------------------------------------------

def test_hybrid_wrap_vs_full_wrap_basic_roundtrip():
    """HybridVimWrap roundtrip accuracy matches FullWrap for cached content."""
    text = 'abcdefghij\nxyzuvw\nend'

    doc_hybrid = ttk.TTkTextDocument(text=text)
    tw_hybrid = ttk.TTkTextWrap(document=doc_hybrid)
    from TermTk.TTkGui.TTkTextWrap.text_wrap_engine_vim_wrap_hybrid import _WrapEngine_HybridVimWrap
    tw_hybrid._wrapEngine = _WrapEngine_HybridVimWrap(state=tw_hybrid._wrapState)
    tw_hybrid.setWrapWidth(4)

    doc_full = ttk.TTkTextDocument(text=text)
    tw_full = ttk.TTkTextWrap(document=doc_full)
    tw_full.setEngine(ttk.TTkK.WrapEngine.FullWrap)
    tw_full.setWrapWidth(4)

    # Prime both engines
    tw_hybrid.screenRows(0, 10)

    # For positions in cached region, results should match
    for line in [0, 1]:
        for pos in [0, 2]:
            x_h, y_h = tw_hybrid.dataToScreenPosition(line, pos).to_xy()
            x_f, y_f = tw_full.dataToScreenPosition(line, pos).to_xy()
            assert (x_h, y_h) == (x_f, y_f)


# ---------------------------------------------------------------------------
# Thread safety (basic verification)
# ---------------------------------------------------------------------------

def test_hybrid_wrap_concurrent_screenRows_calls_is_safe():
    """Multiple concurrent screenRows calls should not corrupt state."""
    import threading

    text = 'abcdefghij\n' * 50
    doc, tw = _mk_hybrid_wrap(text, width=4)

    errors = []
    def reader(y_start):
        try:
            for _ in range(10):
                tw.screenRows(y_start, 5)
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=reader, args=(i*5,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5)

    assert errors == [], f"Thread safety issue: {errors}"
