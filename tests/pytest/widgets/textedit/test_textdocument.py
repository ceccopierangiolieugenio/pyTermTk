#!/usr/bin/env python3
# MIT License

import os
import sys

sys.path.append(os.path.join(sys.path[0], '../../libs/pyTermTk'))

import TermTk as ttk


def _mk_doc(text: str = ' ') -> ttk.TTkTextDocument:
    return ttk.TTkTextDocument(text=text)


def test_set_text_emits_change_and_resets_modified_flag() -> None:
    doc = _mk_doc('a\nb')
    contents_change_calls: list[tuple[int, int, int]] = []
    contents_changed_count = [0]

    def _on_change(line: int, removed: int, added: int) -> None:
        contents_change_calls.append((line, removed, added))

    def _on_changed() -> None:
        contents_changed_count[0] += 1

    doc.contentsChange.connect(_on_change)
    doc.contentsChanged.connect(_on_changed)

    doc.setText('x\ny\nz')

    assert doc.toPlainText() == 'x\ny\nz'
    assert contents_changed_count[0] == 1
    assert contents_change_calls[-1] == (0, 2, 3)
    assert not doc.changed()


def test_append_text_replaces_default_placeholder() -> None:
    doc = _mk_doc()

    doc.appendText('abc')

    assert doc.toPlainText() == 'abc'
    assert doc.lineCount() == 1


def test_append_text_adds_lines_and_emits_change() -> None:
    doc = _mk_doc('a')
    calls: list[tuple[int, int, int]] = []

    def _on_change(line: int, removed: int, added: int) -> None:
        calls.append((line, removed, added))

    doc.contentsChange.connect(_on_change)
    doc.appendText('b\nc')

    assert doc.toPlainText() == 'a\nb\nc'
    assert calls[-1] == (1, 0, 2)


def test_line_and_character_count_and_safe_data_line_access() -> None:
    doc = _mk_doc('ab\nc')

    assert doc.lineCount() == 2
    assert doc.characterCount() == 5
    assert str(doc.dataLine(0)) == 'ab'
    assert doc.dataLine(-1) is None
    assert doc.dataLine(10) is None


def test_find_returns_selected_cursor_when_match_exists() -> None:
    doc = _mk_doc('hello\nworld')

    cur = doc.find('orl')

    assert cur is not None
    assert str(cur.selectedText()) == 'orl'
    assert cur.position().line == 1
    assert cur.anchor().line == 1


def test_find_returns_none_when_no_match_exists() -> None:
    doc = _mk_doc('hello')

    assert doc.find('xyz') is None


def test_snapshot_restore_prev_and_next_roundtrip_document_content() -> None:
    doc = _mk_doc('abc')
    cur = ttk.TTkTextCursor(document=doc)

    doc.saveSnapshot(cur.copy())
    sid_before = doc.snapshootId()

    cur.setPosition(line=0, pos=3)
    cur.insertText('X')
    doc.saveSnapshot(cur.copy())

    assert doc.toPlainText() == 'abcX'
    assert doc.isUndoAvailable()
    assert not doc.isRedoAvailable()
    assert doc.snapshootId() != sid_before

    prev_cursor = doc.restoreSnapshotPrev()
    assert prev_cursor is not None
    assert doc.toPlainText() == 'abc'
    assert doc.isRedoAvailable()

    next_cursor = doc.restoreSnapshotNext()
    assert next_cursor is not None
    assert doc.toPlainText() == 'abcX'


def test_restore_snapshot_returns_none_when_no_history_available() -> None:
    doc = _mk_doc('abc')

    assert doc.restoreSnapshotPrev() is None
    assert doc.restoreSnapshotNext() is None


def test_set_modified_true_clears_redo_chain() -> None:
    doc = _mk_doc('abc')
    cur = ttk.TTkTextCursor(document=doc)
    modification_calls: list[bool] = []

    def _on_modification_changed(modified: bool) -> None:
        modification_calls.append(modified)

    doc.modificationChanged.connect(_on_modification_changed)

    cur.setPosition(line=0, pos=3)
    cur.insertText('!')
    doc.saveSnapshot(cur.copy())

    doc.restoreSnapshotPrev()
    assert doc.isRedoAvailable()

    doc.setModified(True)

    assert not doc.isRedoAvailable()
    assert modification_calls[-1] is True


def test_set_changed_true_clears_redo_chain_without_signal() -> None:
    doc = _mk_doc('abc')
    cur = ttk.TTkTextCursor(document=doc)

    cur.setPosition(line=0, pos=3)
    cur.insertText('!')
    doc.saveSnapshot(cur.copy())

    doc.restoreSnapshotPrev()
    assert doc.isRedoAvailable()

    doc.setChanged(True)

    assert not doc.isRedoAvailable()
    assert doc.changed() is True


def test_merge_changes_slices_combines_overlapping_ranges() -> None:
    merged = ttk.TTkTextDocument._mergeChangesSlices((1, 2, 1), (2, 1, 3))

    assert merged == (1, 3, 4)


def test_clear_and_text_converters() -> None:
    doc = _mk_doc('hello\nworld')

    assert doc.toPlainText() == 'hello\nworld'
    ansi = doc.toAnsi()
    assert 'hello' in ansi
    assert 'world' in ansi
    assert '\n' in ansi
    assert str(doc.toRawText()) == 'hello\nworld'

    doc.clear()

    assert doc.toPlainText() == ' '
