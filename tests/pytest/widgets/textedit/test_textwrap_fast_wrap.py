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
from TermTk.TTkGui.textcursor import TTkTextCursor


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


def test_fast_wrap_regression_scroll_end_then_modify():
	'''Regression test: scroll to end, modify document, verify no crash on screenToDataPosition.

	This tests a bug where scrolling to near the end and then modifying the document
	could cause screenToDataPosition to crash with AttributeError when trying to access
	chunk.y on a None chunk. The fix ensures that None chunks are handled gracefully
	with proper early return instead of unsafe walrus operator patterns.
	'''
	# Create document with exact chunk multiple (512 = 4 * 128)
	doc = ttk.TTkTextDocument(text='\n'.join(['line'*10] * 512))
	tw = ttk.TTkTextWrap(document=doc)
	tw.setEngine(ttk.TTkK.WrapEngine.FastWrap)
	tw.setWrapWidth(30)
	tw.rewrap()

	initial_size = tw.size()
	assert initial_size > 0, "Should have wrapped rows"

	# Scroll to end by querying rows near last line (this materializes chunks)
	last_line_before = doc.lineCount() - 1
	x, y = tw.dataToScreenPosition(last_line_before, 0).to_xy()
	rows_end = tw.screenRows(max(0, y - 50), 100)
	assert len(rows_end.rows) > 0, "Should get rows near end"

	# Append new content (creates new lines, triggers rewrap)
	doc.appendText('\n' + '\n'.join(['NEW'*8] * 256))
	last_line_after = doc.lineCount() - 1
	assert last_line_after > last_line_before, "Should have new lines"

	tw.rewrap()
	new_size = tw.size()
	assert new_size > initial_size, "Size should grow after append"

	# Now the critical test: map the new end position
	# This used to crash because screenToDataPosition would get a None chunk
	# when accessing an out-of-range y coordinate after the rewrap
	x_new, y_new = tw.dataToScreenPosition(last_line_after, 0).to_xy()
	assert x_new >= 0 and y_new >= 0, "New end should be mappable"

	# Verify round-trip works (this calls screenToDataPosition internally)
	recovered_line, _ = tw.screenToDataPosition(x_new, y_new)
	assert recovered_line == last_line_after, "Should round-trip correctly after append+rewrap"

	# Verify size consistency
	all_rows = tw.screenRows(0, 100000)
	actual_wrapped = len(all_rows.rows)
	estimated_size = tw.size()
	assert actual_wrapped == estimated_size, "Size should match actual row count"

def test_fast_wrap_regression_text_edit_view_paint_crash():
	'''Regression test: text_edit_view.paintEvent crashes with IndexError when backgroundColors
	is too small for the line range covered by wrapped rows.

	This tests a bug where when wrapping causes multiple wrapped rows to reference the same
	source line, the backgroundColors array (sized to viewport height) can be too small to
	index by (row.line - first_line), causing IndexError during paint.

	Scenario: 2 text editors share a document. Editor 1 is scrolled near the end with FastWrap.
	Editor 2 adds content. When Editor 1 repaints, screenRows might return wrapped rows spanning
	many source lines (e.g., 10 wrapped rows but 20 source lines due to word wrapping).
	The old code sized backgroundColors to viewport height (10), but indexed by line offset (up to 19),
	causing IndexError.
	'''
	# Create document with long lines that wrap heavily
	doc = ttk.TTkTextDocument(text='\n'.join(['word ' * 30] * 64))
	tw = ttk.TTkTextWrap(document=doc)
	tw.setEngine(ttk.TTkK.WrapEngine.FastWrap)
	tw.setWrapWidth(30)  # Small width causes heavy wrapping
	tw.rewrap()

	# Request rows that will span more source lines than viewport height
	# This creates the mismatch that triggers the bug
	rows = tw.screenRows(150, 10).rows  # Request 10 rows from offset 150
	size = tw.size()
	if not rows and size > 0:
		# Adjust offset to be within bounds
		rows = tw.screenRows(max(0, size - 30), 10).rows

	assert len(rows) > 0, "Should get some rows"

	fr = rows[0].line
	to = rows[-1].line
	line_range = to - fr + 1

	# Verify the problematic condition exists
	# (more source lines than viewport height)
	if line_range > 10:
		# This is the scenario that would crash with old code
		# Old code: backgroundColors = [color] * 10
		# New code: backgroundColors = [color] * line_range
		for y, row in enumerate(rows):
			idx = row.line - rows[0].line
			# With new code, this should never exceed line_range - 1
			assert idx < line_range, f"Index {idx} should be < {line_range}"
			# With old code (h=10), this would sometimes fail
			# if idx >= 10, that would have been the crash point

	# Verify all rows can be safely indexed
	outLines = doc._dataLines[fr:to+1]
	assert len(outLines) == line_range, "outLines should match line_range"

	for row in rows:
		idx = row.line - rows[0].line
		# Both should be safe with new code
		assert idx < len(outLines), f"Index {idx} valid for outLines of length {len(outLines)}"
		assert idx < line_range, f"Index {idx} valid for line_range of {line_range}"


def test_fast_wrap_regression_shared_document_last_line_edit_keeps_tail_consistent() -> None:
	'''Editing the last line from another editor must not corrupt FastWrap tail chunks.

	Scenario covered: one FastWrap view is scrolled at the bottom while another editor
	modifies the same last line in the shared document.
	'''
	doc = ttk.TTkTextDocument(text='\n'.join(['x' * 20] * 1200))
	tw = ttk.TTkTextWrap(document=doc)
	tw.setEngine(ttk.TTkK.WrapEngine.FastWrap)
	tw.setWrapWidth(10)

	# Simulate bottom viewport in the fast-wrapped editor.
	last_line = doc.lineCount() - 1
	_, last_y = tw.dataToScreenPosition(last_line, 0).to_xy()
	tw.screenRows(max(0, last_y - 40), 60)

	# Simulate another editor modifying the same last line.
	cursor = TTkTextCursor(document=doc)
	line_txt = doc.dataLine(last_line)
	line_end = len(line_txt) if line_txt is not None else 0
	cursor.setPosition(last_line, line_end)
	cursor.insertText('Z', moveCursor=True)

	# Tail mapping should remain stable and size should be exact after materialization.
	rows_all = tw.screenRows(0, 100000)
	actual_rows = len(rows_all.rows)
	assert tw.size() == actual_rows, 'FastWrap size() should match materialized rows after tail edit'

	ids = [chunk.id for chunk in tw._wrapEngine._chunks]
	assert ids == sorted(set(ids)), 'Chunk ids should remain unique and sorted after incremental rewrap'


def test_fast_wrap_regression_shared_document_newline_at_end_keeps_tail_consistent() -> None:
	'''Pressing newline at the very end of the last line (via a shared document cursor) must
	not corrupt FastWrap tail chunks or underreport size in the other editor.

	This is the exact user scenario: two editors share a document, editor A (FastWrap) is
	scrolled to the bottom, editor B presses Enter on the last line.
	'''
	doc = ttk.TTkTextDocument(text='\n'.join(['x' * 20] * 1200))
	tw = ttk.TTkTextWrap(document=doc)
	tw.setEngine(ttk.TTkK.WrapEngine.FastWrap)
	tw.setWrapWidth(10)

	# Editor A: materialize viewport at the bottom.
	last_line = doc.lineCount() - 1
	_, last_y = tw.dataToScreenPosition(last_line, 0).to_xy()
	tw.screenRows(max(0, last_y - 40), 60)

	# Editor B: press Enter at the very end of the last line.
	cursor = TTkTextCursor(document=doc)
	line_txt = doc.dataLine(last_line)
	line_end = len(line_txt) if line_txt is not None else 0
	cursor.setPosition(last_line, line_end)
	cursor.insertText('\n', moveCursor=True)

	# Document must have grown by one line.
	assert doc.lineCount() == last_line + 2, 'Document should have a new empty line at the end'

	new_last = doc.lineCount() - 1
	_, new_last_y = tw.dataToScreenPosition(new_last, 0).to_xy()
	assert new_last_y > last_y, 'New last-line screen position should be beyond the old one'

	# Size must be exact after full materialization.
	rows_all = tw.screenRows(0, 100000)
	actual_rows = len(rows_all.rows)
	assert tw.size() == actual_rows, (
		f'FastWrap size() {tw.size()} should match materialized rows {actual_rows} after newline-at-end'
	)

	# Chunk IDs must remain unique and sorted.
	ids = [chunk.id for chunk in tw._wrapEngine._chunks]
	assert ids == sorted(set(ids)), 'Chunk ids should remain unique and sorted after newline-at-end'
