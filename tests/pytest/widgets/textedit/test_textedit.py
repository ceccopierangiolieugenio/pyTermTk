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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

import TermTk as ttk

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


# ---------------------------------------------------------------------------
# replaceText coverage
# ---------------------------------------------------------------------------

def test_replaceText_replaces_forward_characters():
    doc = ttk.TTkTextDocument(text='abcde')
    cur = ttk.TTkTextCursor(document=doc)
    cur.setPosition(line=0, pos=0)
    cur.replaceText('XY')
    assert doc.toPlainText() == 'XYcde'


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
    cur.removeSelectedText()
    assert doc.toPlainText() == 'hello'


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