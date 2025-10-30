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
import argparse

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Full Screen', action='store_true')
args = parser.parse_args()

root = ttk.TTk()
if args.f:
    rootTree1 = root
    root.setLayout(ttk.TTkGridLayout())
else:
    rootTree1 = ttk.TTkWindow(parent=root,pos = (0,0), size=(150,40), title="Test Tree 1", layout=ttk.TTkGridLayout(), border=True)

tw = ttk.TTkTree(parent=rootTree1)
tw.setHeaderLabels(["Column 1", "Column 2", "Column 3"])

l1   = ttk.TTkTreeWidgetItem(["String A", "String B", "String C"])
l2   = ttk.TTkTreeWidgetItem(["String AA", "String BB", "String CC"])
l3   = ttk.TTkTreeWidgetItem(["String AAA", "String BBB", "String CCC"])
l4   = ttk.TTkTreeWidgetItem(["String AAAA", "String BBBB", "String CCCC"])
l5   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB", "String CCCCC"])
l2.addChild(l5)


for i in range(3):
    l1_child = ttk.TTkTreeWidgetItem(["Child A" + str(i), "Child B" + str(i), "Child C" + str(i)])
    l1.addChild(l1_child)

for j in range(2):
    l2_child = ttk.TTkTreeWidgetItem(["Child AA" + str(j), "Child BB" + str(j), "Child CC" + str(j)])
    l2.addChild(l2_child)

for j in range(2):
    l3_child = ttk.TTkTreeWidgetItem(["Child AAA" + str(j), "Child BBB" + str(j), "Child CCC" + str(j)])
    l3.addChild(l3_child)

for j in range(2):
    l4_child = ttk.TTkTreeWidgetItem(["Child AAAA" + str(j), "Child BBBB" + str(j), "Child CCCC" + str(j)])
    l4.addChild(l4_child)

for j in range(2):
    l5_child = ttk.TTkTreeWidgetItem(["Child AAAAA" + str(j), "Child BBBBB" + str(j), "Child CCCCC" + str(j)])
    l5.addChild(l5_child)


tw.addTopLevelItem(l1)
tw.addTopLevelItem(l2)
tw.addTopLevelItem(l3)
tw.addTopLevelItem(l4)
l1.setExpanded(True)
l3.setExpanded(True)

root.mainloop()