#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os
import argparse
import queue
import pickle
import threading
import pytest

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

import TermTk as ttk

_WRAP_ENGINES = ttk.TTkK.WrapEngine

txt = '''xxxxxxxxxx
xxxxxxxxxx
xxxxxxxxxx
xxxxxxxxxx
xxxxxxxxxx
xxxxxxxxxx
xxxxxxxxxx
xxxxxxxxxx
'''

def _setCursor(cur, prop):
    cur._properties = []
    for p in prop:
        cur._properties.append(
            ttk.TTkGui.textcursor._Prop(
                ttk.TTkGui.textcursor._CP(p[0][0], p[0][1]),
                ttk.TTkGui.textcursor._CP(p[1][0], p[1][1])))
    cur._checkCursors()

def test_demo1():
    doc = ttk.TTkTextDocument(text=txt)
    cur = ttk.TTkTextCursor(document=doc)

    _setCursor(cur, [((0,0),(0,5))])
    cbLine, cbRem, cbAdd = -1,-1,-1

    def _cb(a,b,c):
        nonlocal cbLine, cbRem, cbAdd
        cbLine, cbRem, cbAdd = a,b,c

    doc.contentsChange.connect(_cb)
    cur.removeSelectedText()
    print(f"{cbLine=}, {cbRem=}, {cbAdd=}")

    assert cbLine == 0
    assert cbRem  == 1
    assert cbAdd  == 1




# __..__..__
# __..______
# __........
# ..........
# ..__......
# ..........
# ....______
# __........
# rem=8 add=5

def test_demo2():
    doc = ttk.TTkTextDocument(text=txt)
    cur = ttk.TTkTextCursor(document=doc)

    _setCursor(cur, [
        ((0,0),(0,2)),
        ((0,4),(0,6)),
        ((0,8),(1,2)),
        ((1,4),(2,2)),
        ((4,2),(4,4)),
        ((6,4),(7,2))])
    cbLine, cbRem, cbAdd = -1,-1,-1

    def _cb(a,b,c):
        nonlocal cbLine, cbRem, cbAdd
        cbLine, cbRem, cbAdd = a,b,c

    doc.contentsChange.connect(_cb)
    cur.removeSelectedText()
    print(f"{cbLine=}, {cbRem=}, {cbAdd=}")

    assert cbLine == 0
    assert cbRem  == 8
    assert cbAdd  == 5

# ..........
# __..__..__
# __..______
# __........
# ..........
# ..__......
# ..........
# rem=5 add=3

def test_demo3():
    doc = ttk.TTkTextDocument(text=txt)
    cur = ttk.TTkTextCursor(document=doc)

    _setCursor(cur, [
        ((1,0),(1,2)),
        ((1,4),(1,6)),
        ((1,8),(2,2)),
        ((2,4),(3,2)),
        ((5,2),(5,4))])
    cbLine, cbRem, cbAdd = -1,-1,-1

    def _cb(a,b,c):
        nonlocal cbLine, cbRem, cbAdd
        cbLine, cbRem, cbAdd = a,b,c

    doc.contentsChange.connect(_cb)
    cur.removeSelectedText()
    print(f"{cbLine=}, {cbRem=}, {cbAdd=}")

    assert cbLine == 1
    assert cbRem  == 5
    assert cbAdd  == 3


# ---------------------------------------------------------------------------
# insertText coverage
# ---------------------------------------------------------------------------

def test_insertText_appends_to_cursor_position():
    doc = ttk.TTkTextDocument(text='hello\nworld')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=5)
    cur.insertText(' there')
    assert doc.toPlainText() == 'hello there\nworld'


def test_insertText_with_newline_splits_line():
    doc = ttk.TTkTextDocument(text='hello\nworld')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=5)
    cur.insertText('\nthere')
    assert doc.lineCount() == 3
    assert doc.toPlainText() == 'hello\nthere\nworld'


def test_insertText_with_newline_emits_correct_contentsChange_signal():
    doc = ttk.TTkTextDocument(text='hello\nworld')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=5)
    cbLine, cbRem, cbAdd = -1, -1, -1

    def _cb(a, b, c):
        nonlocal cbLine, cbRem, cbAdd
        cbLine, cbRem, cbAdd = a, b, c

    doc.contentsChange.connect(_cb)
    cur.insertText('\nthere')

    assert cbLine == 0
    assert cbRem == 1
    assert cbAdd == 2


def test_insertText_emits_contentsChange_signal():
    doc = ttk.TTkTextDocument(text='hello')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=5)
    cbLine, cbRem, cbAdd = -1, -1, -1

    def _cb(a, b, c):
        nonlocal cbLine, cbRem, cbAdd
        cbLine, cbRem, cbAdd = a, b, c

    doc.contentsChange.connect(_cb)
    cur.insertText(' world')
    assert cbLine == 0
    assert cbRem  == 1
    assert cbAdd  == 1


def test_insertText_multi_cursor_emits_merged_contentsChange_signal():
    doc = ttk.TTkTextDocument(text='aa\nbb\ncc')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=1)
    cur.addCursor(line=2, pos=1)
    cbLine, cbRem, cbAdd = -1, -1, -1

    def _cb(a, b, c):
        nonlocal cbLine, cbRem, cbAdd
        cbLine, cbRem, cbAdd = a, b, c

    doc.contentsChange.connect(_cb)
    cur.insertText('X')

    assert doc.toPlainText() == 'aXa\nbb\ncXc'
    assert cbLine == 0
    assert cbRem == 3
    assert cbAdd == 3


def test_insertText_multiline_multi_cursor_emits_merged_contentsChange_signal():
    doc = ttk.TTkTextDocument(text='aa\nbb\ncc')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=1)
    cur.addCursor(line=2, pos=1)
    cbLine, cbRem, cbAdd = -1, -1, -1

    def _cb(a, b, c):
        nonlocal cbLine, cbRem, cbAdd
        cbLine, cbRem, cbAdd = a, b, c

    doc.contentsChange.connect(_cb)
    cur.insertText('X\nY\nZ')

    assert doc.toPlainText() == 'aX\nY\nZa\nbb\ncX\nY\nZc'
    assert cbLine == 0
    assert cbRem == 3
    assert cbAdd == 7


# ---------------------------------------------------------------------------
# replaceText coverage
# ---------------------------------------------------------------------------

def test_replaceText_replaces_forward_characters():
    doc = ttk.TTkTextDocument(text='abcde')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=0)
    cur.replaceText('XY')
    assert doc.toPlainText() == 'XYcde'


def test_replaceText_emits_correct_contentsChange_signal_without_selection():
    doc = ttk.TTkTextDocument(text='abcde')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=0)
    cbLine, cbRem, cbAdd = -1, -1, -1

    def _cb(a, b, c):
        nonlocal cbLine, cbRem, cbAdd
        cbLine, cbRem, cbAdd = a, b, c

    doc.contentsChange.connect(_cb)
    cur.replaceText('XY')

    assert cbLine == 0
    assert cbRem == 1
    assert cbAdd == 1


def test_replaceText_emits_correct_contentsChange_signal_with_selection():
    doc = ttk.TTkTextDocument(text='abcdef')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=1)
    cur.setPosition(line=0, pos=4, moveMode=ttk.TTkTextCursor.KeepAnchor)
    cbLine, cbRem, cbAdd = -1, -1, -1

    def _cb(a, b, c):
        nonlocal cbLine, cbRem, cbAdd
        cbLine, cbRem, cbAdd = a, b, c

    doc.contentsChange.connect(_cb)
    cur.replaceText('XY')

    assert doc.toPlainText() == 'aXYef'
    assert cbLine == 0
    assert cbRem == 1
    assert cbAdd == 1


# ---------------------------------------------------------------------------
# Selection coverage
# ---------------------------------------------------------------------------

def test_hasSelection_is_false_without_selection():
    doc = ttk.TTkTextDocument(text='hello world')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=3)
    assert not cur.hasSelection()


def test_hasSelection_and_clearSelection():
    doc = ttk.TTkTextDocument(text='hello world')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=0)
    cur.setPosition(line=0, pos=5, moveMode=ttk.TTkTextCursor.KeepAnchor)
    assert cur.hasSelection()
    cur.clearSelection()
    assert not cur.hasSelection()


def test_selectedText_returns_correct_slice():
    doc = ttk.TTkTextDocument(text='hello world')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=0)
    cur.setPosition(line=0, pos=5, moveMode=ttk.TTkTextCursor.KeepAnchor)
    assert str(cur.selectedText()) == 'hello'


def test_select_document_selects_all_content():
    doc = ttk.TTkTextDocument(text='hello\nworld')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=0)
    cur.select(ttk.TTkTextCursor.Document)
    assert cur.hasSelection()
    assert str(cur.selectedText()) == 'hello\nworld'


def test_select_line_under_cursor():
    doc = ttk.TTkTextDocument(text='hello\nworld')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=2)
    cur.select(ttk.TTkTextCursor.LineUnderCursor)
    assert str(cur.selectedText()) == 'hello'


def test_select_word_under_cursor():
    doc = ttk.TTkTextDocument(text='hello world')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=2)
    cur.select(ttk.TTkTextCursor.WordUnderCursor)
    assert str(cur.selectedText()) == 'hello'


# ---------------------------------------------------------------------------
# removeSelectedText edge cases
# ---------------------------------------------------------------------------

def test_removeSelectedText_noop_without_selection():
    doc = ttk.TTkTextDocument(text='hello')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=2)
    calls = []

    def _cb(a, b, c):
        calls.append((a, b, c))

    doc.contentsChange.connect(_cb)
    cur.removeSelectedText()

    assert doc.toPlainText() == 'hello'
    assert calls == []


def test_removeSelectedText_updates_document_content():
    doc = ttk.TTkTextDocument(text='hello world')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=6)
    cur.setPosition(line=0, pos=11, moveMode=ttk.TTkTextCursor.KeepAnchor)
    cur.removeSelectedText()
    assert doc.toPlainText() == 'hello '


# ---------------------------------------------------------------------------
# movePosition coverage
# ---------------------------------------------------------------------------

def test_movePosition_right_and_left():
    doc = ttk.TTkTextDocument(text='hello')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=0)
    cur.movePosition(ttk.TTkTextCursor.Right)
    cur.movePosition(ttk.TTkTextCursor.Right)
    assert cur.position().pos == 2
    cur.movePosition(ttk.TTkTextCursor.Left)
    assert cur.position().pos == 1


def test_movePosition_end_of_line():
    doc = ttk.TTkTextDocument(text='hello')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=0)
    cur.movePosition(ttk.TTkTextCursor.EndOfLine)
    assert cur.position().pos == 5


def test_movePosition_start_and_end_of_document():
    doc = ttk.TTkTextDocument(text='hello\nworld')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=1, pos=2)
    cur.movePosition(ttk.TTkTextCursor.Start)
    assert cur.position().line == 0
    assert cur.position().pos  == 0
    cur.setPosition(line=0, pos=0)
    cur.movePosition(ttk.TTkTextCursor.End)
    assert cur.position().line == 1
    assert cur.position().pos  == 5


# ---------------------------------------------------------------------------
# Multi-cursor coverage
# ---------------------------------------------------------------------------

def test_addCursor_and_clearCursors():
    doc = ttk.TTkTextDocument(text='hello\nworld')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=0)
    cur.addCursor(line=1, pos=0)
    assert len(cur.cursors()) == 2
    cur.clearCursors()
    assert len(cur.cursors()) == 1


# ---------------------------------------------------------------------------
# TTkTextEditView clear / setText cursor-reset regression tests
# ---------------------------------------------------------------------------

def test_clear_resets_cursor_to_origin():
    """Regression: clear() must move cursor back to (0,0)."""
    tev = ttk.TTkTextEditView()
    tev.setText('hello\nworld\nfoo')
    cur = tev.textCursor()
    cur.setPosition(line=2, pos=3)
    assert cur.position().line == 2
    assert cur.position().pos  == 3
    tev.clear()
    cur = tev.textCursor()
    assert cur.position().line == 0
    assert cur.position().pos  == 0


def test_clear_clears_selection():
    """clear() must leave no selection on the cursor."""
    tev = ttk.TTkTextEditView()
    tev.setText('hello\nworld')
    cur = tev.textCursor()
    cur.setPosition(line=0, pos=0)
    cur.setPosition(line=1, pos=5, moveMode=ttk.TTkTextCursor.KeepAnchor)
    assert cur.hasSelection()
    tev.clear()
    cur = tev.textCursor()
    assert not cur.hasSelection()


def test_clear_resets_multi_cursors():
    """clear() must collapse multiple cursors back to a single cursor at (0,0)."""
    tev = ttk.TTkTextEditView()
    tev.setText('aaa\nbbb\nccc')
    cur = tev.textCursor()
    cur.setPosition(line=0, pos=1)
    cur.addCursor(line=2, pos=2)
    assert len(cur.cursors()) == 2
    tev.clear()
    cur = tev.textCursor()
    assert len(cur.cursors()) == 1
    assert cur.position().line == 0
    assert cur.position().pos  == 0


def test_clear_then_insert_text():
    """After clear(), inserting text must work starting at (0,0)."""
    tev = ttk.TTkTextEditView()
    tev.setText('hello\nworld')
    cur = tev.textCursor()
    cur.setPosition(line=1, pos=5)
    tev.clear()
    cur = tev.textCursor()
    assert cur.position().line == 0
    assert cur.position().pos  == 0
    tev.setText('new text')
    assert tev.toPlainText() == 'new text'


def test_clear_document_has_default_content():
    """After clear(), document should contain the default init text (a space)."""
    tev = ttk.TTkTextEditView()
    tev.setText('hello\nworld\nfoo\nbar')
    tev.clear()
    # Default init text is a single space
    assert tev.toPlainText() == ' '
    assert tev.document().lineCount() == 1


def test_setText_over_shorter_content():
    """setText() with shorter content should leave cursor valid."""
    tev = ttk.TTkTextEditView()
    tev.setText('line0\nline1')
    cur = tev.textCursor()
    # Place cursor within bounds of the first line
    cur.setPosition(line=0, pos=3)
    tev.setText('short')
    doc = tev.document()
    assert doc.lineCount() == 1
    assert doc.toPlainText() == 'short'


def test_clear_and_set_text_roundtrip():
    """clear() followed by setText() must produce the expected document."""
    tev = ttk.TTkTextEditView()
    tev.setText('aaa\nbbb')
    cur = tev.textCursor()
    cur.setPosition(line=1, pos=3)
    tev.clear()
    tev.setText('xxx\nyyy\nzzz')
    assert tev.toPlainText() == 'xxx\nyyy\nzzz'
    cur = tev.textCursor()
    # Cursor should be valid (not pointing beyond the new content)
    assert cur.position().line < 3


def test_clear_undo_redo_not_available():
    """After clear(), undo/redo history is wiped."""
    tev = ttk.TTkTextEditView()
    tev.setText('hello')
    cur = tev.textCursor()
    cur.setPosition(line=0, pos=5)
    cur.insertText(' world')
    tev.clear()
    assert not tev.isUndoAvailable()
    assert not tev.isRedoAvailable()


def test_TTkTextEdit_clear_resets_cursor():
    """TTkTextEdit (scroll-area wrapper) clear() must also reset cursor."""
    te = ttk.TTkTextEdit()
    te.setText('hello\nworld\nfoo')
    cur = te.textCursor()
    cur.setPosition(line=2, pos=3)
    assert cur.position().line == 2
    te.clear()
    cur = te.textCursor()
    assert cur.position().line == 0
    assert cur.position().pos  == 0
    assert not cur.hasSelection()


# ---------------------------------------------------------------------------
# TTkTextEditView scrolling/follow-bottom API coverage
# ---------------------------------------------------------------------------

def test_textedit_view_scroll_to_top_and_bottom():
    tev = ttk.TTkTextEditView(size=(10, 3))
    tev.setText('\n'.join(f'line-{i}' for i in range(12)))

    tev.scrollTo(ttk.TTkK.TextEditEdge.BOTTOM)
    _, oy = tev.getViewOffsets()
    _, fh = tev.viewFullAreaSize()
    _, dh = tev.viewDisplayedSize()
    assert oy == max(0, fh - dh)

    tev.scrollTo(ttk.TTkK.TextEditEdge.TOP)
    _, oy = tev.getViewOffsets()
    assert oy == 0


def test_textedit_view_follow_mode_default_is_never():
    tev = ttk.TTkTextEditView(size=(10, 3))
    assert tev.followMode() == ttk.TTkK.TextEditFollow.NEVER


def test_textedit_view_follow_mode_always_tracks_document_changes():
    tev = ttk.TTkTextEditView(size=(10, 3))
    tev.setText('\n'.join(f'line-{i}' for i in range(10)))
    tev.viewMoveTo(0, 0)

    tev.setFollowMode(ttk.TTkK.TextEditFollow.ALWAYS)
    assert tev.followMode() == ttk.TTkK.TextEditFollow.ALWAYS

    _, oy = tev.getViewOffsets()
    _, fh = tev.viewFullAreaSize()
    _, dh = tev.viewDisplayedSize()
    assert oy == max(0, fh - dh)

    tev.viewMoveTo(0, 0)
    tev.append('new-tail')
    _, oy = tev.getViewOffsets()
    _, fh = tev.viewFullAreaSize()
    _, dh = tev.viewDisplayedSize()
    assert oy == max(0, fh - dh)


def test_textedit_view_follow_mode_smart_tracks_only_while_at_bottom():
    tev = ttk.TTkTextEditView(size=(10, 3))
    tev.setText('\n'.join(f'line-{i}' for i in range(10)))
    tev.setFollowMode(ttk.TTkK.TextEditFollow.SMART)

    tev.scrollTo(ttk.TTkK.TextEditEdge.BOTTOM)
    tev.append('smart-tail-1')
    _, oy = tev.getViewOffsets()
    _, fh = tev.viewFullAreaSize()
    _, dh = tev.viewDisplayedSize()
    assert oy == max(0, fh - dh)

    tev.viewMoveTo(0, 1)
    _, oy_before = tev.getViewOffsets()
    tev.append('smart-tail-2')
    _, oy_after = tev.getViewOffsets()
    assert oy_after == oy_before


@pytest.mark.parametrize('initial_text', ['', 'line-0'])
def test_textedit_view_follow_mode_smart_from_underfilled_document_starts_following_when_full(initial_text):
    tev_1 = ttk.TTkTextEditView(size=(10, 3))
    tev_1.setText(initial_text)
    tev_1.setFollowMode(ttk.TTkK.TextEditFollow.SMART)

    for i in range(1, 7):
        tev_1.append(f'line-{i}')

    _, oy = tev_1.getViewOffsets()
    _, fh = tev_1.viewFullAreaSize()
    _, dh = tev_1.viewDisplayedSize()
    assert oy == max(0, fh - dh)

    tev_2 = ttk.TTkTextEditView(size=(10, 3),followMode=ttk.TTkK.TextEditFollow.SMART)
    tev_2.setText(initial_text)

    for i in range(1, 7):
        tev_2.append(f'line-{i}')

    _, oy = tev_2.getViewOffsets()
    _, fh = tev_2.viewFullAreaSize()
    _, dh = tev_2.viewDisplayedSize()
    assert oy == max(0, fh - dh)


def test_textedit_view_follow_mode_smart_nowrap_starts_following_after_initial_zero_height():
    tev = ttk.TTkTextEditView(size=(10, 0), visible=False)
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.NoWrap)
    tev.setText('line-0')

    # Simulate enabling SMART before geometry is realized.
    tev.setFollowMode(ttk.TTkK.TextEditFollow.SMART)

    # Grow the document while still unrealized.
    for i in range(1, 5):
        tev.append(f'line-{i}')

    # Realize final view height and keep appending.
    tev.resize(10, 3)
    tev.append('line-5')

    _, oy = tev.getViewOffsets()
    _, fh = tev.viewFullAreaSize()
    _, dh = tev.viewDisplayedSize()
    assert oy == max(0, fh - dh)

def test_textedit_view_follow_mode_never_does_not_force_scroll():
    tev = ttk.TTkTextEditView(size=(10, 3))
    tev.setText('\n'.join(f'line-{i}' for i in range(10)))
    tev.scrollTo(ttk.TTkK.TextEditEdge.BOTTOM)
    tev.viewMoveTo(0, 1)
    _, oy_before = tev.getViewOffsets()

    tev.setFollowMode(ttk.TTkK.TextEditFollow.NEVER)
    assert tev.followMode() == ttk.TTkK.TextEditFollow.NEVER
    tev.append('still-not-following')
    _, oy_after = tev.getViewOffsets()

    assert oy_after == oy_before


def test_textedit_wrapper_forwards_scroll_and_follow_mode_api():
    te = ttk.TTkTextEdit(size=(10, 3))
    te.setText('\n'.join(f'line-{i}' for i in range(8)))

    te.setFollowMode(ttk.TTkK.TextEditFollow.ALWAYS)
    assert te.followMode() == ttk.TTkK.TextEditFollow.ALWAYS

    te.append('tail')
    te.scrollTo(ttk.TTkK.TextEditEdge.BOTTOM)

    _, oy = te.textEditView().getViewOffsets()
    _, fh = te.textEditView().viewFullAreaSize()
    _, dh = te.textEditView().viewDisplayedSize()
    assert oy == max(0, fh - dh)

    te.scrollTo(ttk.TTkK.TextEditEdge.TOP)
    _, oy = te.textEditView().getViewOffsets()
    assert oy == 0


@pytest.mark.parametrize('wrap_engine', _WRAP_ENGINES)
def test_textedit_view_scroll_to_top_and_bottom_with_all_wrap_engines(wrap_engine):
    tev = ttk.TTkTextEditView(size=(10, 3))
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.WidgetWidth, wrapEngine=wrap_engine)
    tev.setText('\n'.join('word ' * 8 for _ in range(18)))

    tev.scrollTo(ttk.TTkK.TextEditEdge.BOTTOM)
    _, oy = tev.getViewOffsets()
    _, fh = tev.viewFullAreaSize()
    _, dh = tev.viewDisplayedSize()
    assert oy > 0
    assert 0 <= oy <= max(0, fh - dh)

    tev.scrollTo(ttk.TTkK.TextEditEdge.TOP)
    _, oy = tev.getViewOffsets()
    assert oy == 0


@pytest.mark.parametrize('wrap_engine', _WRAP_ENGINES)
def test_textedit_view_follow_mode_always_with_all_wrap_engines(wrap_engine):
    tev = ttk.TTkTextEditView(size=(10, 3))
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.WidgetWidth, wrapEngine=wrap_engine)
    tev.setText('\n'.join('word ' * 8 for _ in range(14)))
    tev.viewMoveTo(0, 0)
    _, oy_before = tev.getViewOffsets()

    tev.setFollowMode(ttk.TTkK.TextEditFollow.ALWAYS)
    tev.append('tail ' * 8)

    _, oy = tev.getViewOffsets()
    _, fh = tev.viewFullAreaSize()
    _, dh = tev.viewDisplayedSize()
    assert oy >= oy_before
    assert oy > 0
    assert 0 <= oy <= max(0, fh - dh)


@pytest.mark.parametrize('wrap_engine', _WRAP_ENGINES)
def test_textedit_view_follow_mode_smart_and_never_with_all_wrap_engines(wrap_engine):
    tev = ttk.TTkTextEditView(size=(10, 3))
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.WidgetWidth, wrapEngine=wrap_engine)
    tev.setText('\n'.join('word ' * 8 for _ in range(14)))

    tev.setFollowMode(ttk.TTkK.TextEditFollow.SMART)
    tev.scrollTo(ttk.TTkK.TextEditEdge.BOTTOM)
    _, oy_bottom = tev.getViewOffsets()
    tev.append('smart-follow-tail') # split in 2 lines if wrapped
    _, oy_after_smart_bottom = tev.getViewOffsets()
    assert 0 < abs(oy_after_smart_bottom - oy_bottom) <= (2 if not wrap_engine==_WRAP_ENGINES.VimWrap else 14)
    
    tev.viewMoveTo(0, 1)
    _, oy_before = tev.getViewOffsets()
    tev.append('smart-do-not-follow') # split in 2 lines if wrapped
    _, oy_after = tev.getViewOffsets()
    assert oy_after == oy_before

    tev.setFollowMode(ttk.TTkK.TextEditFollow.NEVER)
    tev.append('never-do-not-follow') # split in 2 lines if wrapped
    _, oy_never = tev.getViewOffsets()
    assert oy_never == oy_after


@pytest.mark.parametrize('wrap_engine', _WRAP_ENGINES)
def test_textedit_view_follow_mode_keeps_following_while_hidden(wrap_engine, fake_canvas):
    canvas = fake_canvas(10, 3)
    tev = ttk.TTkTextEditView(size=(10, 3), followMode=ttk.TTkK.TextEditFollow.SMART, visible=False)
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.WidgetWidth, wrapEngine=wrap_engine)
    tev.setText('\n'.join('word ' * 8 for _ in range(8)))

    tev.scrollTo(ttk.TTkK.TextEditEdge.BOTTOM)
    for _ in range(4):
        tev.append('tail ' * 20)
    
    tev.append('Last Line')
    tev.paintEvent(canvas=canvas)

    assert canvas.text_in_line(line=2, text='Last Line')


# ---------------------------------------------------------------------------
# TTkTextEditView horizontal scrolling (LEFT/RIGHT) coverage
# ---------------------------------------------------------------------------

def test_textedit_view_scroll_to_left():
    '''Test scrollTo(LEFT) scrolls the horizontal offset to the beginning (ox=0)'''
    # Create a text view with width 20 and add wide text (longer lines)
    tev = ttk.TTkTextEditView(size=(20, 5))
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.NoWrap)
    # Create lines that are longer than the 20-char width
    wide_text = '\n'.join('x' * 50 for _ in range(4))
    tev.setText(wide_text)

    # First scroll right to see if we can move the horizontal offset
    tev.viewMoveTo(10, 0)  # Move right by 10 chars
    ox, _ = tev.getViewOffsets()
    assert ox == 10  # Verify horizontal scroll worked

    # Now scroll to LEFT
    tev.scrollTo(ttk.TTkK.TextEditEdge.LEFT)
    ox, _ = tev.getViewOffsets()
    assert ox == 0


def test_textedit_view_scroll_to_right():
    '''Test scrollTo(RIGHT) scrolls to the rightmost position (ox=max(0, fw-dw))'''
    tev = ttk.TTkTextEditView(size=(20, 5))
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.NoWrap)
    # Create lines that are longer than the 20-char width
    wide_text = '\n'.join('x' * 50 for _ in range(4))
    tev.setText(wide_text)

    # First move to the left
    tev.viewMoveTo(0, 0)
    ox, _ = tev.getViewOffsets()
    assert ox == 0

    # Now scroll to RIGHT
    tev.scrollTo(ttk.TTkK.TextEditEdge.RIGHT)
    ox, _ = tev.getViewOffsets()
    fw, _ = tev.viewFullAreaSize()
    dw, _ = tev.viewDisplayedSize()
    assert ox == max(0, fw - dw)


def test_textedit_view_scroll_to_top_and_left():
    '''Test scrollTo(TOP | LEFT) scrolls to the top-left corner'''
    tev = ttk.TTkTextEditView(size=(20, 5))
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.NoWrap)
    # Create a grid of wide text lines
    wide_text = '\n'.join('line-' + str(i).ljust(40) for i in range(15))
    tev.setText(wide_text)

    # Move to a random position
    tev.viewMoveTo(15, 8)
    ox, oy = tev.getViewOffsets()
    assert ox > 0 and oy > 0

    # Scroll to top-left
    tev.scrollTo(ttk.TTkK.TextEditEdge.TOP | ttk.TTkK.TextEditEdge.LEFT)
    ox, oy = tev.getViewOffsets()
    assert ox == 0
    assert oy == 0


def test_textedit_view_scroll_to_bottom_and_right():
    '''Test scrollTo(BOTTOM | RIGHT) scrolls to the bottom-right corner'''
    tev = ttk.TTkTextEditView(size=(20, 5))
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.NoWrap)
    # Create a grid of wide text lines
    wide_text = '\n'.join('line-' + str(i).ljust(40) for i in range(15))
    tev.setText(wide_text)

    # Move to the top-left first
    tev.viewMoveTo(0, 0)
    ox, oy = tev.getViewOffsets()
    assert ox == 0 and oy == 0

    # Scroll to bottom-right
    tev.scrollTo(ttk.TTkK.TextEditEdge.BOTTOM | ttk.TTkK.TextEditEdge.RIGHT)
    ox, oy = tev.getViewOffsets()
    fw, fh = tev.viewFullAreaSize()
    dw, dh = tev.viewDisplayedSize()
    assert ox == max(0, fw - dw)
    assert oy == max(0, fh - dh)


def test_textedit_view_scroll_to_top_and_right():
    '''Test scrollTo(TOP | RIGHT) scrolls to the top-right corner'''
    tev = ttk.TTkTextEditView(size=(20, 5))
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.NoWrap)
    wide_text = '\n'.join('x' * 50 for _ in range(10))
    tev.setText(wide_text)

    # Move to bottom-left
    tev.viewMoveTo(0, 5)
    ox, oy = tev.getViewOffsets()
    assert oy > 0

    # Scroll to top-right
    tev.scrollTo(ttk.TTkK.TextEditEdge.TOP | ttk.TTkK.TextEditEdge.RIGHT)
    ox, oy = tev.getViewOffsets()
    fw, _ = tev.viewFullAreaSize()
    dw, _ = tev.viewDisplayedSize()
    assert oy == 0
    assert ox == max(0, fw - dw)


def test_textedit_view_scroll_to_bottom_and_left():
    '''Test scrollTo(BOTTOM | LEFT) scrolls to the bottom-left corner'''
    tev = ttk.TTkTextEditView(size=(20, 5))
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.NoWrap)
    wide_text = '\n'.join('x' * 50 for _ in range(10))
    tev.setText(wide_text)

    # Move to top-right
    tev.viewMoveTo(20, 0)
    ox, oy = tev.getViewOffsets()
    assert ox > 0

    # Scroll to bottom-left
    tev.scrollTo(ttk.TTkK.TextEditEdge.BOTTOM | ttk.TTkK.TextEditEdge.LEFT)
    ox, oy = tev.getViewOffsets()
    _, fh = tev.viewFullAreaSize()
    _, dh = tev.viewDisplayedSize()
    assert ox == 0
    assert oy == max(0, fh - dh)


def test_textedit_wrapper_forwards_scroll_left_and_right_api():
    '''Test that TTkTextEdit properly forwards scrollTo LEFT and RIGHT to the view'''
    te = ttk.TTkTextEdit(size=(20, 5))
    te.setLineWrapMode(ttk.TTkK.LineWrapMode.NoWrap)
    wide_text = '\n'.join('y' * 60 for _ in range(8))
    te.setText(wide_text)

    # Test scrollTo(LEFT)
    te.textEditView().viewMoveTo(15, 0)
    ox_before, _ = te.textEditView().getViewOffsets()
    assert ox_before == 15

    te.scrollTo(ttk.TTkK.TextEditEdge.LEFT)
    ox, _ = te.textEditView().getViewOffsets()
    assert ox == 0

    # Test scrollTo(RIGHT)
    te.scrollTo(ttk.TTkK.TextEditEdge.RIGHT)
    ox, _ = te.textEditView().getViewOffsets()
    fw, _ = te.textEditView().viewFullAreaSize()
    dw, _ = te.textEditView().viewDisplayedSize()
    assert ox == max(0, fw - dw)


def test_textedit_view_scroll_left_does_not_affect_vertical_offset():
    '''Test that scrolling left/right doesn't affect vertical scroll position'''
    tev = ttk.TTkTextEditView(size=(20, 5))
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.NoWrap)
    tall_wide_text = '\n'.join('z' * 50 for _ in range(15))
    tev.setText(tall_wide_text)

    # Set a specific vertical position
    _, oy = 0, 7
    tev.viewMoveTo(0, oy)
    _, oy_before = tev.getViewOffsets()
    assert oy_before == 7

    # Scroll LEFT
    tev.scrollTo(ttk.TTkK.TextEditEdge.LEFT)
    _, oy_after = tev.getViewOffsets()
    assert oy_after == oy_before  # Vertical position unchanged

    # Scroll RIGHT
    tev.scrollTo(ttk.TTkK.TextEditEdge.RIGHT)
    _, oy_after = tev.getViewOffsets()
    assert oy_after == oy_before  # Vertical position unchanged


def test_textedit_view_scroll_right_does_not_affect_vertical_offset():
    '''Test that scrolling right doesn't affect vertical scroll position'''
    tev = ttk.TTkTextEditView(size=(20, 5))
    tev.setLineWrapMode(ttk.TTkK.LineWrapMode.NoWrap)
    tall_wide_text = '\n'.join('a' * 50 for _ in range(15))
    tev.setText(tall_wide_text)

    # Set a specific vertical position
    oy = 10
    tev.viewMoveTo(0, oy)
    _, oy_before = tev.getViewOffsets()
    assert oy_before == oy

    # Scroll RIGHT
    tev.scrollTo(ttk.TTkK.TextEditEdge.RIGHT)
    _, oy_after = tev.getViewOffsets()
    assert oy_after == oy_before  # Vertical position unchanged