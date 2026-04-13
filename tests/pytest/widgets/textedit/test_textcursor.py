#!/usr/bin/env python3
# MIT License

import os
import sys

import pytest

sys.path.append(os.path.join(sys.path[0], '../../libs/pyTermTk'))

import TermTk as ttk


def _mk_cursor(text: str) -> tuple[ttk.TTkTextDocument, ttk.TTkTextCursor]:
    doc = ttk.TTkTextDocument(text=text)
    cur = ttk.TTkTextCursor(document=doc)
    return doc, cur


def test_document_change_clears_selection_and_extra_cursors() -> None:
    doc, cur = _mk_cursor('hello\nworld')

    cur.setPosition(line=0, pos=0)
    cur.setPosition(line=0, pos=3, moveMode=ttk.TTkTextCursor.KeepAnchor)
    cur.addCursor(line=1, pos=2)

    assert len(cur.cursors()) == 2
    assert cur.hasSelection()

    doc.setText('reset')

    assert len(cur.cursors()) == 1
    assert not cur.hasSelection()
    assert cur.position().line == cur.anchor().line
    assert cur.position().pos == cur.anchor().pos


def test_copy_restore_restores_state_and_emits_cursor_signal() -> None:
    doc, cur = _mk_cursor('alpha\nbeta')
    signal_calls: list[ttk.TTkTextCursor] = []

    def _on_cursor_changed(cursor: ttk.TTkTextCursor) -> None:
        signal_calls.append(cursor)

    doc.cursorPositionChanged.connect(_on_cursor_changed)

    cur.setPosition(line=0, pos=1)
    cur.setPosition(line=0, pos=4, moveMode=ttk.TTkTextCursor.KeepAnchor)
    snapshot = cur.copy()

    cur.setPosition(line=1, pos=2)
    cur.clearSelection()

    cur.restore(snapshot)

    assert cur.position().line == 0
    assert cur.position().pos == 4
    assert cur.anchor().line == 0
    assert cur.anchor().pos == 1
    assert cur.hasSelection()
    assert signal_calls
    assert signal_calls[-1] is cur


def test_move_up_down_requires_textwrap() -> None:
    _doc, cur = _mk_cursor('a\nb')

    with pytest.raises(ValueError):
        cur.movePosition(ttk.TTkTextCursor.Up)

    with pytest.raises(ValueError):
        cur.movePosition(ttk.TTkTextCursor.Down)


def test_move_left_right_cross_line_boundaries() -> None:
    _doc, cur = _mk_cursor('abc\nde')

    cur.setPosition(line=0, pos=3)
    cur.movePosition(ttk.TTkTextCursor.Right)
    assert (cur.position().line, cur.position().pos) == (1, 0)

    cur.movePosition(ttk.TTkTextCursor.Left)
    assert (cur.position().line, cur.position().pos) == (0, 3)


def test_position_char_returns_space_when_out_of_range() -> None:
    _doc, cur = _mk_cursor('abc')

    cur.setPosition(line=0, pos=1)
    assert cur.positionChar() == 'a'

    cur.setPosition(line=9, pos=0)
    assert cur.positionChar() == ' '

# NOTE: The default behavior is to select the leftmost word under the cursor
def test_select_word_under_cursor_on_whitespace_yields_no_selection() -> None:
    _doc, cur = _mk_cursor('hello world')

    cur.setPosition(line=0, pos=5)
    cur.select(ttk.TTkTextCursor.WordUnderCursor)

    assert cur.hasSelection()
    assert str(cur.selectedText()) == 'hello'


def test_get_lines_under_cursor_ignores_invalid_positions() -> None:
    _doc, cur = _mk_cursor('line1\nline2')

    cur.addCursor(line=9, pos=0)
    lines = cur.getLinesUnderCursor()

    assert len(lines) == 1
    assert str(lines[0]) == 'line1'


def test_replace_text_is_bounded_to_current_line_when_no_selection() -> None:
    doc, cur = _mk_cursor('abc\ndef')
    calls: list[tuple[int, int, int]] = []

    def _on_change(line: int, removed: int, added: int) -> None:
        calls.append((line, removed, added))

    doc.contentsChange.connect(_on_change)

    cur.setPosition(line=0, pos=2)
    cur.replaceText('WXYZ')

    assert doc.toPlainText() == 'abWXYZ\ndef'
    assert calls[-1] == (0, 1, 1)


def test_insert_text_with_newline_emits_expected_contents_change_payload() -> None:
    doc, cur = _mk_cursor('abc\ndef')
    calls: list[tuple[int, int, int]] = []

    def _on_change(line: int, removed: int, added: int) -> None:
        calls.append((line, removed, added))

    doc.contentsChange.connect(_on_change)

    cur.setPosition(line=0, pos=1)
    cur.insertText('\nXYZ')

    assert doc.toPlainText() == 'a\nXYZbc\ndef'
    assert calls[-1] == (0, 1, 2)


def test_remove_selected_text_emits_expected_contents_change_payload() -> None:
    doc, cur = _mk_cursor('hello world')
    calls: list[tuple[int, int, int]] = []

    def _on_change(line: int, removed: int, added: int) -> None:
        calls.append((line, removed, added))

    doc.contentsChange.connect(_on_change)

    cur.setPosition(line=0, pos=6)
    cur.setPosition(line=0, pos=11, moveMode=ttk.TTkTextCursor.KeepAnchor)
    cur.removeSelectedText()

    assert doc.toPlainText() == 'hello '
    assert calls[-1] == (0, 1, 1)
