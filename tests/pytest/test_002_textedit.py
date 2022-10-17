#!/usr/bin/env python3
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

sys.path.append(os.path.join(sys.path[0],'../..'))

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
            ttk.TTkTextCursor._prop(
                ttk.TTkTextCursor._CP(p[0][0], p[0][1]),
                ttk.TTkTextCursor._CP(p[1][0], p[1][1])))
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