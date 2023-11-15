#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

root = ttk.TTk(title="pyTermTk Demo", mouseTrack=True)


tdp = ttk.TTkTextDialogPicker(parent=root, pos=(0,0), size=(60,10))

# epw = ttk.emojiPicker(parent=root, pos=(60,5), size=(60,10))

w1 = ttk.TTkWindow(parent=root, pos=(60,0), size=(20,11))
w1.addWidget(tp := ttk.TTkTextPicker(pos=(0,0), size=(18,7)))

def _tpSizeChanged(w,h):
    w1.sizeChanged.disconnect(_wSizeChanged)
    ww,wh = w1.size()
    w1.resize(max(ww,w+2),h+4)
    w1.sizeChanged.connect(_wSizeChanged)

def _wSizeChanged(w,h):
    tp.documentViewChanged.disconnect(_tpSizeChanged)
    tp.resize(w-2,h-4)
    tp.documentViewChanged.connect(_tpSizeChanged)

w1.sizeChanged.connect(_wSizeChanged)
tp.documentViewChanged.connect(_tpSizeChanged)

w2 = ttk.TTkWindow(parent=root, pos=(10,10), size=(60,20), layout=ttk.TTkGridLayout())

tw = ttk.TTkTree(parent=w2)
tw.setHeaderLabels(["Column 1", "Column 2", "Column 3"])

l1   = ttk.TTkTreeWidgetItem(["String A\nNewLine\nNW", "String B", "String C"])
l2   = ttk.TTkTreeWidgetItem(["String AA", ttk.TTkTextPicker(size=(10,1)), "String CC"])
l3   = ttk.TTkTreeWidgetItem(["String AAA", "String BBB", "String CCC"])
l4   = ttk.TTkTreeWidgetItem(["String AAAA", "String BBBB", "String CCCC"])
l5   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB", "String CCCCC"])
l1.addChild(l2)
l2.addChild(l3)
l3.addChild(l4)
l4.addChild(l5)
tw.addTopLevelItem(l1)

l1.setExpanded(True)
l2.setExpanded(True)

root.mainloop()