#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

# Demo inspired from:
# https://stackoverflow.com/questions/41204234/python-pyqt5-qtreewidget-sub-item

import os
import sys
from threading import Thread

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()


root = ttk.TTk()

base_btn = ttk.TTkButton(parent=root, text="Test Base", pos=(0,0), size=(20,3), border=True)
enough_btn = ttk.TTkButton(parent=root, text="Test Enough", pos=(20,0), size=(20,3), border=True)
many_btn = ttk.TTkButton(parent=root, text="Test Many", pos=(40,0), size=(20,3), border=True)
winTree = ttk.TTkWindow(parent=root,pos = (0,3), size=(80,30), title="Test Tree 1", layout=ttk.TTkGridLayout(), border=True)

winLog = ttk.TTkWindow(parent=root,pos = (5,10), size=(100,30), title="Logs", layout=ttk.TTkGridLayout(), border=True)
ttk.TTkLogViewer(parent=winLog)

tw = ttk.TTkTree(parent=winTree)
tw.setHeaderLabels(["Column 1", "Column 2", "Column 3"])

@ttk.pyTTkSlot()
def _add_base():
    tw.clear()
    l1   = ttk.TTkTreeWidgetItem(["String A", "String B\nxyz\nabc\n123", "String C"])
    l2   = ttk.TTkTreeWidgetItem(["String AA", "String BB", "String CC"])
    l3   = ttk.TTkTreeWidgetItem(["String AAA", "String BBB", "String CCC\nxyz\nabc\n123"])
    l4   = ttk.TTkTreeWidgetItem(["String AAAA", "String BBBB", "String CCCC"])
    l5   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB\nxyz\nabc\n123", "String CCCCC"])
    l2.addChild(l5)


    for i in range(3):
        l1_child = ttk.TTkTreeWidgetItem(["Child A" + str(i), "Child B" + str(i), "Child C" + str(i)])
        l1.addChild(l1_child)

    for j in range(2):
        l2_child = ttk.TTkTreeWidgetItem(["Child AA\nxyz\nabc\n123" + str(j), "Child BB" + str(j), "Child CC" + str(j)])
        l2.addChild(l2_child)

    for j in range(2):
        l3_child = ttk.TTkTreeWidgetItem(["Child AAA" + str(j), "Child BBB" + str(j), "Child CCC" + str(j)])
        l3.addChild(l3_child)

    for j in range(2):
        l4_child = ttk.TTkTreeWidgetItem(["Child AAAA" + str(j), "Child BBBB\nxyz\nabc\n123" + str(j), "Child CCCC" + str(j)])
        l4.addChild(l4_child)

    for j in range(2):
        l5_child = ttk.TTkTreeWidgetItem(["Child AAAAA" + str(j), "Child BBBBB\nxyz\nabc\n123" + str(j), "Child CCCCC" + str(j)])
        l5.addChild(l5_child)


    tw.addTopLevelItem(l1)
    tw.addTopLevelItem(l2)
    tw.addTopLevelItem(l3)
    tw.addTopLevelItem(l4)
    l1.setExpanded(True)
    l3.setExpanded(True)


@ttk.pyTTkSlot()
def _add_many():
    _add_base()

    def _many_loop():
        ttk.TTkLog.debug('Many Loop START!!!')
        num = 1
        for i in range(10):
            ttk.TTkLog.debug(f"Loop: {i}")
            _entries = []
            num = num<<1
            for ii in range(num):
                _e   = ttk.TTkTreeWidgetItem([f"({i}-{ii}) String A", "String B", "String C"])
                _e.addChildren([
                    ttk.TTkTreeWidgetItem(["Child A" + str(ii) + (f"\nl:{ii}"*ii), "Child B" + str(ii), "Child C" + str(ii)])
                    for i in range(3)
                    ])
                _entries.append(_e)
                if not ii%3:
                    _e.setExpanded(True)
            tw.addTopLevelItems(_entries)
        ttk.TTkLog.debug('DONE!!!')
    Thread(target=_many_loop).start()

@ttk.pyTTkSlot()
def _add_enough():
    _add_base()

    def _many_loop():
        ttk.TTkLog.debug('Many Loop START!!!')
        num = 1
        for i in range(4):
            _entries = []
            num = num<<1
            for ii in range(num):
                _e   = ttk.TTkTreeWidgetItem([f"({i}-{ii}) String A", "String B", "String C"])
                _e.addChildren([
                    ttk.TTkTreeWidgetItem(["Child A" + str(ii) + (f"\nl:{ii}"*ii), "Child B" + str(ii), "Child C" + str(ii)])
                    for i in range(3)
                    ])
                _entries.append(_e)
                if not ii%3:
                    _e.setExpanded(True)
            tw.addTopLevelItems(_entries)
        ttk.TTkLog.debug('DONE!!!')
    Thread(target=_many_loop).start()

base_btn.clicked.connect(_add_base)
enough_btn.clicked.connect(_add_enough)
many_btn.clicked.connect(_add_many)

root.mainloop()