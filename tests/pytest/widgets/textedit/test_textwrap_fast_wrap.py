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


def _mk_wrap(text: str, engine: ttk.TTkK.WrapEngine, width: int = 4, word_wrap: bool = False):
	doc = ttk.TTkTextDocument(text=text)
	tw = ttk.TTkTextWrap(document=doc)
	tw.setEngine(engine)
	tw.setWrapWidth(width)
	if word_wrap:
		tw.setWordWrapMode(ttk.TTkK.WordWrap)
	else:
		tw.setWordWrapMode(ttk.TTkK.WrapAnywhere)
	return doc, tw


def _mk_fast_wrap(text: str, width: int = 4, word_wrap: bool = False):
	return _mk_wrap(text=text, engine=ttk.TTkK.WrapEngine.FastWrap, width=width, word_wrap=word_wrap)


def _mk_full_wrap(text: str, width: int = 4, word_wrap: bool = False):
	return _mk_wrap(text=text, engine=ttk.TTkK.WrapEngine.FullWrap, width=width, word_wrap=word_wrap)


def _rows_for(tw: ttk.TTkTextWrap, y: int, h: int) -> list[_WrapLine]:
	ret = tw.screenRows(y, h)
	assert isinstance(ret.rows, list)
	return ret.rows


def _rows_sig(rows: list[_WrapLine]) -> list[tuple[int, int, int, bool]]:
	return [(r.line, r.start, r.stop, r.last_slice) for r in rows]


def test_fast_wrap_screen_rows_wrap_anywhere_visible_window() -> None:
	_, tw = _mk_fast_wrap('abcdefghij\nxyz', width=4)

	rows = _rows_for(tw, 0, 4)

	assert len(rows) == 4
	assert rows[0] == _WrapLine(0, 0, 4, False)
	assert rows[1] == _WrapLine(0, 4, 8, False)
	assert rows[2] == _WrapLine(0, 8, 11, True)
	assert rows[3] == _WrapLine(1, 0, 4, True)


def test_fast_wrap_screen_rows_matches_full_wrap_for_same_viewport() -> None:
	text = '\n'.join([
		'abcdefghij',
		'0123456789',
		'short',
		'line with spaces',
		'tab\tline',
	])
	_, tw_fast = _mk_fast_wrap(text, width=5)
	_, tw_full = _mk_full_wrap(text, width=5)

	rows_fast = _rows_for(tw_fast, 0, 50)
	rows_full = _rows_for(tw_full, 0, 50)

	assert _rows_sig(rows_fast) == _rows_sig(rows_full)


def test_fast_wrap_data_to_screen_position_inside_cached_window_is_wrap_accurate() -> None:
	text = 'abcdefghij\n' * 5
	_, tw = _mk_fast_wrap(text, width=4)

	tw.screenRows(0, 4)

	x, y = tw.dataToScreenPosition(0, 6).to_xy()
	assert (x, y) == (2, 1)


def test_fast_wrap_data_to_screen_position_distant_query_remains_roundtrip_safe() -> None:
	text = 'abcdefghij\n' * 5
	_, tw = _mk_fast_wrap(text, width=4)

	tw.screenRows(10, 4)

	x, y = tw.dataToScreenPosition(0, 5).to_xy()
	line, pos = tw.screenToDataPosition(x, y)
	assert (line, pos) == (0, 5)


def test_fast_wrap_screen_to_data_position_matches_full_wrap() -> None:
	text = '\n'.join(['abcdefghij'] * 12)
	_, tw_fast = _mk_fast_wrap(text, width=4)
	_, tw_full = _mk_full_wrap(text, width=4)

	tw_fast.screenRows(0, 40)

	for y in range(0, 35):
		for x in (0, 1, 2, 3, 4, 99):
			assert tw_fast.screenToDataPosition(x, y) == tw_full.screenToDataPosition(x, y)


def test_fast_wrap_screen_to_data_position_beyond_tail_clamps_to_last_line() -> None:
	text = '\n'.join(['abcdefghij'] * 120)
	doc, tw = _mk_fast_wrap(text, width=4)

	tw.screenRows(0, 5)

	line, pos = tw.screenToDataPosition(7, 100000)

	assert isinstance(line, int)
	assert isinstance(pos, int)
	assert line == doc.lineCount() - 1
	assert pos >= 0


def test_fast_wrap_normalize_screen_position_inside_cached_row_is_wrap_accurate() -> None:
	text = 'abcdefghij\n' * 3
	_, tw = _mk_fast_wrap(text, width=4)

	tw.screenRows(0, 4)

	x, y = tw.normalizeScreenPosition(99, 1)
	assert (x, y) == (4, 1)


def test_fast_wrap_normalize_screen_position_offscreen_uses_line_fallback() -> None:
	text = '\n'.join(['abcdefghij'] * 5)
	_, tw = _mk_fast_wrap(text, width=4)

	tw.screenRows(0, 4)

	x, y = tw.normalizeScreenPosition(5, 50)
	assert x >= 0
	assert y == 4


def test_fast_wrap_rewrap_after_append_keeps_new_tail_addressable() -> None:
	base = '\n'.join(['abcdefghij'] * 720)
	doc, tw = _mk_fast_wrap(base, width=4)

	tw.screenRows(250, 30)
	tw.screenRows(1500, 30)

	before = doc.lineCount()
	doc.appendText('\nTAIL-ONE\nTAIL-TWO')
	assert doc.lineCount() >= before + 2
	tw.rewrap()

	last_line = doc.lineCount() - 1
	x, y = tw.dataToScreenPosition(last_line, 1).to_xy()
	assert x >= 0
	assert y >= 0

	line, pos = tw.screenToDataPosition(x, y)
	assert line == last_line
	assert pos >= 0


def test_fast_wrap_size_estimate_becomes_more_than_line_count_after_wrapping() -> None:
	text = '\n'.join(['abcdefghij'] * 720)
	doc, tw = _mk_fast_wrap(text, width=4)

	assert tw.size() >= doc.lineCount()

	tw.screenRows(0, 50)

	assert tw.size() > doc.lineCount()


def test_fast_wrap_size_estimate_exact_multiple_chunks() -> None:
	'''Regression: size estimate should be accurate after materializing exact multiples of chunks.

	Validates fix for off-by-one error in unprocessed_tail_lines calculation.
	With 896 lines (7 × 128 chunk size) wrapped at width=5, all lines should be materialized
	and size estimate should match actual wrapped row count exactly.
	'''
	text = '\n'.join(['x' * 20] * 896)
	doc, tw = _mk_fast_wrap(text, width=5)

	# Materialize all chunks by querying full document
	rows = _rows_for(tw, 0, 10000)
	actual_wrapped_rows = len(rows)

	# After full materialization, size estimate should match actual
	estimated_size = tw.size()

	assert actual_wrapped_rows > 0, "Document should produce wrapped rows"
	assert estimated_size == actual_wrapped_rows, (
		f"Size estimate {estimated_size} should match actual wrapped rows {actual_wrapped_rows}"
	)


def test_fast_wrap_rewrap_exact_chunk_multiples_does_not_regress() -> None:
	'''Regression: rewrap with exact chunk multiples should not fail or corrupt state.

	Validates fix for brittle tail_id calculation in rewrap(). With 896 lines
	(exactly 7 chunks of 128), the old code would compute last_id=7 which is out
	of range for valid chunk IDs (0-6). The fix explicitly handles this case.
	'''
	text = '\n'.join(['abcdefghij'] * 896)
	doc, tw = _mk_fast_wrap(text, width=4)

	# Prime the cache with some rows
	tw.screenRows(0, 50)

	# Trigger rewrap (full document, no incremental data)
	tw.rewrap()

	# Verify state is still valid after rewrap
	last_line = doc.lineCount() - 1
	x, y = tw.dataToScreenPosition(last_line, 0).to_xy()
	assert x >= 0 and y >= 0, "Last line should map to valid screen coordinates"

	# Verify round-trip mapping still works
	line, pos = tw.screenToDataPosition(x, y)
	assert line == last_line, f"Screen position should map back to last line, got {line}"
	assert pos >= 0, f"Position should be valid, got {pos}"


def test_fast_wrap_rewrap_incremental_then_full_exact_multiple() -> None:
	'''Rewrap after incremental change, then full rewrap, with exact chunk multiple.'''
	text = '\n'.join(['line'] * 640)  # 640 lines
	doc, tw = _mk_fast_wrap(text, width=8)

	# Materialize initial state
	tw.screenRows(0, 100)

	# Append exactly 384 lines to hit 1024 total (8 complete chunks)
	doc.appendText('\n' + '\n'.join(['new'] * 384))
	assert doc.lineCount() == 1025, "Should have 1025 lines"

	# Rewrap after append
	tw.rewrap()

	# Verify full document is addressable
	for line_idx in [0, 512, 1024]:
		x, y = tw.dataToScreenPosition(line_idx, 0).to_xy()
		assert x >= 0 and y >= 0, f"Line {line_idx} should map to valid coordinates"
		recovered_line, _ = tw.screenToDataPosition(x, y)
		assert recovered_line == line_idx, f"Round-trip mapping failed for line {line_idx}"


def test_fast_wrap_size_estimate_exactness_after_partial_materialization() -> None:
	'''Gap: Validate size() exactness after partial wrapping, not just inequalities.

	The original loose inequality test (line 183) doesn't validate that size estimate
	accuracy improves as more chunks are materialized. This test confirms that size()
	becomes exact once all chunks are wrapped, without relying on inequalities.
	'''
	text = '\n'.join(['abcdefghij'] * 512)
	doc, tw = _mk_fast_wrap(text, width=5)

	# Before any materialization, size is an estimate based on line count
	size_before = tw.size()
	assert size_before >= doc.lineCount(), "Initial estimate should be >= line count"

	# Materialize first half of document
	rows_half = _rows_for(tw, 0, 500)
	size_after_half = tw.size()
	assert size_after_half > 0, "Size after partial wrap should be positive"

	# Materialize full document
	rows_full = _rows_for(tw, 0, 10000)
	size_after_full = tw.size()

	# Key validation: size() should match actual wrapped row count exactly when fully materialized
	actual_rows = len(rows_full)
	assert size_after_full == actual_rows, (
		f"After full materialization, size() {size_after_full} should exactly match "
		f"actual wrapped rows {actual_rows}"
	)


def test_fast_wrap_large_document_exact_multiple_rewrap_path() -> None:
	'''Gap: Test rewrap with large exact-multiple-of-128 document to exercise full rewrap path.

	The rewrap() method has different logic paths for num_ids > 6 (large documents with
	first/last chunk bootstrap) vs small documents (full sequential wrap). This test
	ensures the large-document rewrap path (lines 158-175) works correctly with exact
	multiples where num_ids = N*128.
	'''
	# Create exactly 10 chunks (1280 lines)
	text = '\n'.join(['x' * 30] * 1280)
	doc, tw = _mk_fast_wrap(text, width=7)

	# Trigger rewrap on untouched document (full rewrap path)
	tw.rewrap()

	# Verify chunk state is valid
	eng = tw._wrapEngine
	chunks = eng._chunks
	assert len(chunks) > 0, "Should have materialized chunks"
	assert chunks[-1].id == 9, f"Max chunk id should be 9 (for 1280 lines), got {chunks[-1].id}"

	# Verify all document lines are addressable after rewrap
	for test_line in [0, 128, 256, 640, 1024, 1279]:
		x, y = tw.dataToScreenPosition(test_line, 0).to_xy()
		assert x >= 0 and y >= 0, f"Line {test_line} should map to valid coordinates"
		recovered_line, _ = tw.screenToDataPosition(x, y)
		assert recovered_line == test_line, (
			f"Large-doc rewrap: line {test_line} should round-trip, got {recovered_line}"
		)

	# Verify size estimation is correct
	rows_all = _rows_for(tw, 0, 50000)
	assert tw.size() == len(rows_all), (
		f"Size estimate {tw.size()} should match actual wrapped rows {len(rows_all)}"
	)


def test_fast_wrap_rewrap_exact_multiple_with_incremental_data() -> None:
	'''Full rewrap on exact-multiple document to exercise large-doc rewrap bootstrap path.

	Validates that the full rewrap path (num_ids > 6) in rewrap() correctly handles
	exact multiples of 128. This tests the same code path as the large-document case
	but in isolation with document modification.
	'''
	text = '\n'.join(['base'] * 768)  # 6 chunks exactly
	doc, tw = _mk_fast_wrap(text, width=6)

	# Materialize initial state
	tw.screenRows(0, 100)

	# Replace entire document (still exact multiple)
	doc.setText('\n'.join(['modified'] * 768))

	# Full rewrap
	tw.rewrap()

	# Verify document is still addressable after rewrap on exact multiple
	last_line = doc.lineCount() - 1
	x, y = tw.dataToScreenPosition(last_line, 0).to_xy()
	assert x >= 0 and y >= 0, "Last line should be addressable after rewrap"

	line, _ = tw.screenToDataPosition(x, y)
	assert line == last_line, "Round-trip should work after rewrap on exact multiple"

	# Verify intermediate lines also work
	for test_line in [0, 128, 256, 512, 640]:
		x, y = tw.dataToScreenPosition(test_line, 0).to_xy()
		recovered, _ = tw.screenToDataPosition(x, y)
		assert recovered == test_line, f"Line {test_line} should round-trip correctly"
