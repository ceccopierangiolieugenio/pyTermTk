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

'''Multithreading safety tests for TTkTextDocument, TTkTextWrap and their interaction.

The suite exercises three concurrent access patterns that occur in a real TUI application:

* **Reader vs writer**: one thread repeatedly calls ``screenRows()`` /
  ``dataToScreenPosition()`` while another thread mutates the document via
  ``setText()`` / ``appendText()``.

* **Multiple concurrent readers**: several threads call ``screenRows()`` and
  ``screenToDataPosition()`` simultaneously on the same (TTkTextDocument,
  TTkTextWrap) pair.

* **Rewrap race**: one thread calls ``rewrap()`` while a rendering thread reads
  ``screenRows()`` at the same time.

A test passes if no exception is raised and the returned values satisfy basic
sanity checks (non-negative coordinates, slice indices within line boundaries,
etc.).
'''

import os
import sys
import threading
import random

sys.path.append(os.path.join(sys.path[0], '../../libs/pyTermTk'))

import TermTk as ttk

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_LINES = [
    'The quick brown fox jumps over the lazy dog',
    'Pack my box with five dozen liquor jugs',
    'How vexingly quick daft zebras jump',
    'The five boxing wizards jump quickly',
    '',
    'Sphinx of black quartz judge my vow',
]

_LONG_LINE = 'abcdefghijklmnopqrstuvwxyz' * 4   # 104 chars


def _mk_wrap(text: str, width: int = 20, word_wrap: bool = False) -> tuple[ttk.TTkTextDocument, ttk.TTkTextWrap]:
    doc = ttk.TTkTextDocument(text=text)
    tw = ttk.TTkTextWrap(document=doc)
    tw.setEngine(ttk.TTkK.WrapEngine.FullWrap)
    tw.setWrapWidth(width)
    if word_wrap:
        tw.setWordWrapMode(ttk.TTkK.WordWrap)
    else:
        tw.setWordWrapMode(ttk.TTkK.WrapAnywhere)
    return doc, tw


_THREAD_TIMEOUT = 10  # seconds; a still-alive thread after this is treated as a deadlock


def _collect_errors(threads: list[threading.Thread]) -> list[Exception]:
    '''Join all threads and return a list of exceptions or timeout errors.

    A thread that is still alive after ``_THREAD_TIMEOUT`` seconds is considered
    to have deadlocked or hung and is reported as a ``TimeoutError``.
    '''
    errors: list[Exception] = []
    for t in threads:
        t.join(timeout=_THREAD_TIMEOUT)
        if t.is_alive():
            errors.append(TimeoutError(
                f'Thread {t.name!r} did not finish within {_THREAD_TIMEOUT}s '
                f'(possible deadlock or infinite loop)'
            ))
        elif hasattr(t, '_exc') and t._exc is not None:
            errors.append(t._exc)
    return errors


def _safe_thread(target, *args, **kwargs) -> threading.Thread:
    '''Create a thread that stores any raised exception in ``t._exc``.'''
    exc_holder: list[Exception | None] = [None]

    def wrapper():
        try:
            target(*args, **kwargs)
        except Exception as e:
            exc_holder[0] = e

    t = threading.Thread(target=wrapper, daemon=True)
    t._exc = None  # type: ignore[attr-defined]
    # Patch join to propagate stored exception after base join.
    _orig_join = t.join
    def patched_join(timeout=None):
        _orig_join(timeout=timeout)
        t._exc = exc_holder[0]  # type: ignore[attr-defined]
    t.join = patched_join  # type: ignore[method-assign]
    return t

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_concurrent_readers_screenRows():
    '''Multiple threads calling screenRows() simultaneously must not raise.'''
    text = '\n'.join(_LINES * 10)
    doc, tw = _mk_wrap(text, width=20)

    errors: list[Exception] = []
    barrier = threading.Barrier(6)

    def reader(start_y: int) -> None:
        barrier.wait()
        for _ in range(50):
            rows = tw.screenRows(start_y, 10)
            for row in rows:
                assert row.line >= 0
                assert row.start >= 0
                assert row.start <= row.stop

    threads = [_safe_thread(reader, i * 5) for i in range(6)]
    for t in threads:
        t.start()
    errors = _collect_errors(threads)
    assert errors == [], f'Exceptions in reader threads: {errors}'


def test_concurrent_readers_dataToScreenPosition():
    '''Multiple threads calling dataToScreenPosition() simultaneously must not raise.'''
    text = '\n'.join(_LINES)
    doc, tw = _mk_wrap(text, width=15)

    barrier = threading.Barrier(4)

    def reader(line_idx: int) -> None:
        barrier.wait()
        for pos in range(0, 40, 2):
            x, y = tw.dataToScreenPosition(line_idx % tw.documentLineCount(), pos)
            assert x >= 0
            assert y >= 0

    threads = [_safe_thread(reader, i) for i in range(4)]
    for t in threads:
        t.start()
    errors = _collect_errors(threads)
    assert errors == [], f'Exceptions in reader threads: {errors}'


def test_reader_writer_setText():
    '''One reader thread and one writer thread using setText() must not crash.'''
    initial_text = '\n'.join(_LINES)
    doc, tw = _mk_wrap(initial_text, width=20)

    barrier = threading.Barrier(2)

    def writer() -> None:
        barrier.wait()
        texts = [
            '\n'.join(_LINES[:3]),
            _LONG_LINE,
            '\n'.join(_LINES * 2),
            'single line',
        ]
        for txt in texts:
            doc.setText(txt)

    def reader() -> None:
        barrier.wait()
        for _ in range(100):
            rows = tw.screenRows(0, 10)
            for row in rows:
                assert row.line >= 0
                assert row.start >= 0
                assert row.start <= row.stop

    t_w = _safe_thread(writer)
    t_r = _safe_thread(reader)
    t_w.start()
    t_r.start()
    errors = _collect_errors([t_w, t_r])
    assert errors == [], f'Exceptions in threads: {errors}'


def test_reader_writer_appendText():
    '''One reader thread and one writer thread using appendText() must not crash.'''
    doc, tw = _mk_wrap('\n'.join(_LINES[:2]), width=20)

    barrier = threading.Barrier(2)

    def writer() -> None:
        barrier.wait()
        for line in _LINES * 3:
            doc.appendText(line + '\n')

    def reader() -> None:
        barrier.wait()
        for _ in range(100):
            rows = tw.screenRows(0, 8)
            for row in rows:
                assert row.line >= 0
                assert row.start >= 0
                assert row.start <= row.stop

    t_w = _safe_thread(writer)
    t_r = _safe_thread(reader)
    t_w.start()
    t_r.start()
    errors = _collect_errors([t_w, t_r])
    assert errors == [], f'Exceptions in threads: {errors}'


def test_rewrap_race():
    '''rewrap() called from one thread while another reads screenRows().'''
    text = '\n'.join(_LINES * 5)
    doc, tw = _mk_wrap(text, width=15)

    barrier = threading.Barrier(2)

    def rewrapper() -> None:
        barrier.wait()
        for _ in range(10):
            tw.rewrap()

    def reader() -> None:
        barrier.wait()
        for y in range(0, 60, 4):
            rows = tw.screenRows(y, 4)
            for row in rows:
                assert row.line >= 0
                assert row.start >= 0
                assert row.start <= row.stop

    t_i = _safe_thread(rewrapper)
    t_r = _safe_thread(reader)
    t_i.start()
    t_r.start()
    errors = _collect_errors([t_i, t_r])
    assert errors == [], f'Exceptions in threads: {errors}'


def test_screenToDataPosition_concurrent_with_setText():
    '''screenToDataPosition() must not raise while another thread calls setText().'''
    doc, tw = _mk_wrap('\n'.join(_LINES), width=20)

    barrier = threading.Barrier(2)

    def writer() -> None:
        barrier.wait()
        for i in range(5):
            doc.setText('\n'.join(_LINES[i % len(_LINES):] + _LINES[:i % len(_LINES)]))

    def reader() -> None:
        barrier.wait()
        for y in range(0, 30):
            line, pos = tw.screenToDataPosition(0, y)
            assert line >= 0
            assert pos >= 0

    t_w = _safe_thread(writer)
    t_r = _safe_thread(reader)
    t_w.start()
    t_r.start()
    errors = _collect_errors([t_w, t_r])
    assert errors == [], f'Exceptions in threads: {errors}'


def test_many_threads_mixed_operations():
    '''Stress test: many threads doing mixed reads and document mutations.'''
    rng = random.Random(42)
    text = '\n'.join(_LINES * 4)
    doc, tw = _mk_wrap(text, width=20)

    NUM_THREADS = 10
    ITERATIONS  = 30
    barrier = threading.Barrier(NUM_THREADS)

    def worker(thread_id: int) -> None:
        barrier.wait()
        for i in range(ITERATIONS):
            op = (thread_id + i) % 5
            if op == 0:
                # Read screen rows at a random position
                y = rng.randint(0, 20)
                rows = tw.screenRows(y, 5)
                for row in rows:
                    assert row.line >= 0 and row.start >= 0 and row.start <= row.stop
            elif op == 1:
                # Map data position to screen
                lc = tw.documentLineCount()
                if lc > 0:
                    ln = rng.randint(0, lc - 1)
                    x, y = tw.dataToScreenPosition(ln, 0)
                    assert x >= 0 and y >= 0
            elif op == 2:
                # Map screen position to data
                line, pos = tw.screenToDataPosition(0, rng.randint(0, 10))
                assert line >= 0 and pos >= 0
            elif op == 3:
                # Trigger a full rewrap
                tw.rewrap()
            else:
                # Overwrite document text (rare: only thread 0 does this)
                if thread_id == 0:
                    doc.setText('\n'.join(_LINES[i % len(_LINES):i % len(_LINES) + 3]))

    threads = [_safe_thread(worker, i) for i in range(NUM_THREADS)]
    for t in threads:
        t.start()
    errors = _collect_errors(threads)
    assert errors == [], f'Exceptions in stress threads: {errors}'


# ---------------------------------------------------------------------------
# Cursor tests
# ---------------------------------------------------------------------------

def test_cursor_insertText_concurrent_with_screenRows():
    '''One cursor doing insertText() while another thread reads screenRows().'''
    doc, tw = _mk_wrap('\n'.join(_LINES), width=20)

    from TermTk.TTkGui.textcursor import TTkTextCursor
    cursor = TTkTextCursor(document=doc)
    cursor.setPosition(line=0, pos=0)

    barrier = threading.Barrier(2)

    def editor() -> None:
        barrier.wait()
        for i in range(10):
            cursor.setPosition(line=0, pos=0)
            cursor.insertText(f'[{i}]')

    def reader() -> None:
        barrier.wait()
        for _ in range(80):
            rows = tw.screenRows(0, 8)
            for row in rows:
                assert row.line >= 0 and row.start >= 0 and row.start <= row.stop

    t_e = _safe_thread(editor)
    t_r = _safe_thread(reader)
    t_e.start()
    t_r.start()
    errors = _collect_errors([t_e, t_r])
    assert errors == [], f'Exceptions in threads: {errors}'


def test_two_cursors_insertText_on_different_lines():
    '''Two independent cursors each inserting on different lines concurrently.'''
    text = '\n'.join(_LINES)
    doc, tw = _mk_wrap(text, width=30)

    from TermTk.TTkGui.textcursor import TTkTextCursor
    cursor_a = TTkTextCursor(document=doc)
    cursor_b = TTkTextCursor(document=doc)
    cursor_a.setPosition(line=0, pos=0)
    cursor_b.setPosition(line=3, pos=0)

    barrier = threading.Barrier(2)

    def editor_a() -> None:
        barrier.wait()
        for i in range(8):
            cursor_a.setPosition(line=0, pos=0)
            cursor_a.insertText(f'A{i}')

    def editor_b() -> None:
        barrier.wait()
        for i in range(8):
            cursor_b.setPosition(line=min(3, doc.lineCount() - 1), pos=0)
            cursor_b.insertText(f'B{i}')

    t_a = _safe_thread(editor_a)
    t_b = _safe_thread(editor_b)
    t_a.start()
    t_b.start()
    errors = _collect_errors([t_a, t_b])
    assert errors == [], f'Exceptions in threads: {errors}'
    # Document must still be coherent after concurrent edits.
    assert doc.lineCount() >= 1


def test_cursor_removeSelectedText_concurrent_with_screenRows():
    '''Cursor selecting and removing text while a render thread reads screenRows().'''
    text = '\n'.join(_LINES * 3)
    doc, tw = _mk_wrap(text, width=20)

    from TermTk.TTkGui.textcursor import TTkTextCursor
    cursor = TTkTextCursor(document=doc)
    barrier = threading.Barrier(2)

    def editor() -> None:
        barrier.wait()
        for _ in range(10):
            lc = doc.lineCount()
            if lc < 2:
                break
            target_line = min(1, lc - 1)
            line_data = doc.dataLine(target_line)
            if line_data and len(line_data) >= 4:
                cursor.setPosition(line=target_line, pos=0)
                cursor.setPosition(
                    line=target_line, pos=4,
                    moveMode=TTkTextCursor.MoveMode.KeepAnchor
                )
                if cursor.hasSelection():
                    cursor.removeSelectedText()

    def reader() -> None:
        barrier.wait()
        for y in range(0, 40, 2):
            rows = tw.screenRows(y, 4)
            for row in rows:
                assert row.line >= 0 and row.start >= 0 and row.start <= row.stop

    t_e = _safe_thread(editor)
    t_r = _safe_thread(reader)
    t_e.start()
    t_r.start()
    errors = _collect_errors([t_e, t_r])
    assert errors == [], f'Exceptions in threads: {errors}'


def test_cursor_movePosition_updown_concurrent_with_rewrap():
    '''Cursor using Up/Down movePosition (via textWrap) while rewrap runs concurrently.'''
    text = '\n'.join(_LINES * 4)
    doc, tw = _mk_wrap(text, width=20)

    from TermTk.TTkGui.textcursor import TTkTextCursor
    cursor = TTkTextCursor(document=doc)
    cursor.setPosition(line=0, pos=0)

    barrier = threading.Barrier(2)

    def mover() -> None:
        barrier.wait()
        for _ in range(20):
            cursor.movePosition(TTkTextCursor.Down, textWrap=tw)
        for _ in range(20):
            cursor.movePosition(TTkTextCursor.Up, textWrap=tw)

    def rewrapper() -> None:
        barrier.wait()
        for _ in range(10):
            tw.rewrap()

    t_m = _safe_thread(mover)
    t_i = _safe_thread(rewrapper)
    t_m.start()
    t_i.start()
    errors = _collect_errors([t_m, t_i])
    assert errors == [], f'Exceptions in threads: {errors}'


def test_cursor_insertText_concurrent_with_dataLine_reads():
    '''Cursor inserting text while another thread reads dataLine() directly.'''
    doc, tw = _mk_wrap('\n'.join(_LINES), width=20)

    from TermTk.TTkGui.textcursor import TTkTextCursor
    cursor = TTkTextCursor(document=doc)
    barrier = threading.Barrier(2)

    def editor() -> None:
        barrier.wait()
        for i in range(15):
            cursor.setPosition(line=0, pos=0)
            cursor.insertText(f'X{i}X')

    def reader() -> None:
        barrier.wait()
        for _ in range(60):
            for ln in range(doc.lineCount()):
                line_data = doc.dataLine(ln)
                if line_data is not None:
                    assert len(line_data) >= 0

    t_e = _safe_thread(editor)
    t_r = _safe_thread(reader)
    t_e.start()
    t_r.start()
    errors = _collect_errors([t_e, t_r])
    assert errors == [], f'Exceptions in threads: {errors}'


def test_cursor_replaceText_concurrent_with_screenRows():
    '''Cursor using replaceText() while a render thread calls screenRows().'''
    doc, tw = _mk_wrap('\n'.join(_LINES), width=20)

    from TermTk.TTkGui.textcursor import TTkTextCursor
    cursor = TTkTextCursor(document=doc)
    barrier = threading.Barrier(2)

    def editor() -> None:
        barrier.wait()
        replacements = ['REPLACED', 'hi', 'longer replacement text here', '!']
        for txt in replacements * 3:
            lc = doc.lineCount()
            if lc > 0:
                cursor.setPosition(line=0, pos=0)
                cursor.replaceText(txt)

    def reader() -> None:
        barrier.wait()
        for _ in range(80):
            rows = tw.screenRows(0, 8)
            for row in rows:
                assert row.line >= 0 and row.start >= 0 and row.start <= row.stop

    t_e = _safe_thread(editor)
    t_r = _safe_thread(reader)
    t_e.start()
    t_r.start()
    errors = _collect_errors([t_e, t_r])
    assert errors == [], f'Exceptions in threads: {errors}'


def test_cursor_editing_stress_with_mixed_readers():
    '''Stress: one editor cursor + multiple readers all running concurrently.'''
    rng = random.Random(7)
    text = '\n'.join(_LINES)
    doc, tw = _mk_wrap(text, width=20)

    from TermTk.TTkGui.textcursor import TTkTextCursor
    cursor = TTkTextCursor(document=doc)
    cursor.setPosition(line=0, pos=0)

    NUM_READERS = 5
    barrier = threading.Barrier(NUM_READERS + 1)  # readers + editor

    def editor() -> None:
        barrier.wait()
        ops = ['insert', 'move_right', 'move_left', 'move_down', 'move_up']
        for i in range(30):
            op = ops[i % len(ops)]
            if op == 'insert':
                cursor.setPosition(line=0, pos=0)
                cursor.insertText(f'{i}|')
            elif op == 'move_right':
                cursor.movePosition(TTkTextCursor.Right)
            elif op == 'move_left':
                cursor.movePosition(TTkTextCursor.Left)
            elif op == 'move_down':
                cursor.movePosition(TTkTextCursor.Down, textWrap=tw)
            elif op == 'move_up':
                cursor.movePosition(TTkTextCursor.Up, textWrap=tw)

    def reader(reader_id: int) -> None:
        barrier.wait()
        for j in range(40):
            op = (reader_id + j) % 3
            if op == 0:
                rows = tw.screenRows(rng.randint(0, 10), 5)
                for row in rows:
                    assert row.line >= 0 and row.start >= 0 and row.start <= row.stop
            elif op == 1:
                lc = doc.lineCount()
                if lc > 0:
                    x, y = tw.dataToScreenPosition(rng.randint(0, lc - 1), 0)
                    assert x >= 0 and y >= 0
            else:
                line, pos = tw.screenToDataPosition(0, rng.randint(0, 8))
                assert line >= 0 and pos >= 0

    t_editor = _safe_thread(editor)
    t_readers = [_safe_thread(reader, i) for i in range(NUM_READERS)]
    t_editor.start()
    for t in t_readers:
        t.start()
    errors = _collect_errors([t_editor] + t_readers)
    assert errors == [], f'Exceptions in stress threads: {errors}'


# ---------------------------------------------------------------------------
# Missing coverage tests
# ---------------------------------------------------------------------------

def test_normalizeScreenPosition_concurrent_with_setText():
    '''normalizeScreenPosition() must not raise while another thread calls setText().'''
    doc, tw = _mk_wrap('\n'.join(_LINES), width=20)

    barrier = threading.Barrier(2)

    def writer() -> None:
        barrier.wait()
        texts = [
            '\n'.join(_LINES[:2]),
            _LONG_LINE,
            '\n'.join(_LINES * 2),
            'x',
        ]
        for txt in texts:
            doc.setText(txt)

    def reader() -> None:
        barrier.wait()
        for y in range(0, 20):
            for x in range(0, 20, 4):
                nx, ny = tw.normalizeScreenPosition(x, y)
                assert nx >= 0
                assert ny >= 0

    t_w = _safe_thread(writer)
    t_r = _safe_thread(reader)
    t_w.start()
    t_r.start()
    errors = _collect_errors([t_w, t_r])
    assert errors == [], f'Exceptions in threads: {errors}'


def test_setWrapWidth_concurrent_with_screenRows():
    '''setWrapWidth() (full rewrap) called from one thread must not crash a concurrent reader.'''
    text = '\n'.join(_LINES * 5)
    doc, tw = _mk_wrap(text, width=20)

    barrier = threading.Barrier(2)

    def width_changer() -> None:
        barrier.wait()
        for w in [10, 40, 5, 80, 20]:
            tw.setWrapWidth(w)

    def reader() -> None:
        barrier.wait()
        for _ in range(80):
            rows = tw.screenRows(0, 10)
            for row in rows:
                assert row.line >= 0
                assert row.start >= 0
                assert row.start <= row.stop

    t_c = _safe_thread(width_changer)
    t_r = _safe_thread(reader)
    t_c.start()
    t_r.start()
    errors = _collect_errors([t_c, t_r])
    assert errors == [], f'Exceptions in threads: {errors}'


def test_concurrent_readers_from_different_positions():
    '''Multiple threads reading screenRows() from different positions simultaneously
    must not raise (FullWrap buffer is pre-computed so all reads are valid).'''
    text = '\n'.join(_LINES * 30)          # ~180 logical lines
    doc, tw = _mk_wrap(text, width=20)

    NUM_THREADS = 6
    barrier = threading.Barrier(NUM_THREADS)

    def reader(start_y: int) -> None:
        barrier.wait()
        for _ in range(20):
            rows = tw.screenRows(start_y, 8)
            for row in rows:
                assert row.line >= 0
                assert row.start >= 0
                assert row.start <= row.stop

    # Spread threads across different positions.
    threads = [_safe_thread(reader, i * 30) for i in range(NUM_THREADS)]
    for t in threads:
        t.start()
    errors = _collect_errors(threads)
    assert errors == [], f'Exceptions in concurrent reader threads: {errors}'


def test_wrapChanged_listener_safe_during_concurrent_rewrap():
    '''A wrapChanged listener that calls screenRows() must not deadlock or raise
    when rewrap() is fired concurrently from another thread.'''
    text = '\n'.join(_LINES * 5)
    doc, tw = _mk_wrap(text, width=15)

    listener_errors: list[Exception] = []

    def on_wrap_changed() -> None:
        try:
            rows = tw.screenRows(0, 5)
            for row in rows:
                assert row.line >= 0 and row.start >= 0 and row.start <= row.stop
        except Exception as e:
            listener_errors.append(e)

    tw.wrapChanged.connect(on_wrap_changed)

    barrier = threading.Barrier(2)

    def rewrapper() -> None:
        barrier.wait()
        for _ in range(10):
            tw.rewrap()

    def reader() -> None:
        barrier.wait()
        for y in range(0, 50, 3):
            rows = tw.screenRows(y, 4)
            for row in rows:
                assert row.line >= 0 and row.start >= 0 and row.start <= row.stop

    t_i = _safe_thread(rewrapper)
    t_r = _safe_thread(reader)
    t_i.start()
    t_r.start()
    errors = _collect_errors([t_i, t_r])
    assert errors == [], f'Exceptions in threads: {errors}'
    assert listener_errors == [], f'Exceptions inside wrapChanged listener: {listener_errors}'
