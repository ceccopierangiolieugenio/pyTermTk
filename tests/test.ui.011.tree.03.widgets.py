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

import os
import sys
import argparse

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Full Screen', action='store_true')
args = parser.parse_args()

root = ttk.TTk()

rootTree1 = ttk.TTkWindow(parent=root,pos = (0,1), size=(100,20), title="Test Tree 1", layout=ttk.TTkGridLayout(), border=True)

tw = ttk.TTkTree(parent=rootTree1)
tw.setHeaderLabels(["Column 1", "Column 2", "Column 3"])

l1   = ttk.TTkTreeWidgetItem(["String A\nNewLine\nNW", "String B", "String C"])
l2   = ttk.TTkTreeWidgetItem(["String AA", "String BB\nNewLine\nNW", "String CC"])
l3   = ttk.TTkTreeWidgetItem(["String AAA", "String BBB", "String CCC"])
l4   = ttk.TTkTreeWidgetItem(["String AAAA", "String BBBB", "String CCCC"])
l5   = ttk.TTkTreeWidgetItem(["String AAAAA", "String BBBBB", "String CCCCC"])
l2.addChild(l5)


for i in range(3):
    l1_child = ttk.TTkTreeWidgetItem(["Child A" + str(i), "Child B" + str(i), "Child C\nNewLine\nNW\nNW\nNW" + str(i)])
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


lw1   = ttk.TTkTreeWidgetItem(["WA1\nNewLine\nNewLine",                           "WB1",   btn1 := ttk.TTkButton(text="WC1\nNewLine", border=True)])
lw11  = ttk.TTkTreeWidgetItem(["WA11",                          "WB11",  ttk.TTkButton(text="WC11\nNewLine")])
lw111 = ttk.TTkTreeWidgetItem(["WA111",                         "WB111", ttk.TTkButton(text="WC111")])
lw2   = ttk.TTkTreeWidgetItem(["WA2",        ttk.TTkButton(text="WB2"),                     "WC2"])
lw3   = ttk.TTkTreeWidgetItem([btn2 := ttk.TTkButton(text="WA3\nNewLine\nNL"),      "WB3",                      "WC3"])
lw4   = ttk.TTkTreeWidgetItem(["WA4",   ttk.TTkCheckbox(   size=(10,1),text="WB4"),   "WC4"])
lw41  = ttk.TTkTreeWidgetItem(["WA41",  ttk.TTkCheckbox(   size=(10,1),text="WB41"),  "WC41"])
lw411 = ttk.TTkTreeWidgetItem(["WA411", ttk.TTkCheckbox(   size=(10,1),text="WB411"), "WC411"])
lw5   = ttk.TTkTreeWidgetItem(["WA5",   ttk.TTkRadioButton(size=(10,1),text="WB5"),   "WC5"])
lw51  = ttk.TTkTreeWidgetItem(["WA51",  ttk.TTkRadioButton(size=(10,1),text="WB51"),  "WC51"])
lw511 = ttk.TTkTreeWidgetItem(["WA511", ttk.TTkRadioButton(size=(10,1),text="WB511"), "WC511"])
lw6   = ttk.TTkTreeWidgetItem(["WA6",   ttk.TTkLineEdit(   size=(10,1),text="WB6"),   "WC6"])
lw61  = ttk.TTkTreeWidgetItem(["WA61",  ttk.TTkLineEdit(   size=(10,1),text="WB61"),  "WC61"])
lw611 = ttk.TTkTreeWidgetItem(["WA611", ttk.TTkLineEdit(   size=(10,1),text="WB611"), "WC611"])
lw7   = ttk.TTkTreeWidgetItem([ttk.TTkRadioButton(text="WA7"),   "WB7",   "WC7"])
lw71  = ttk.TTkTreeWidgetItem([ttk.TTkRadioButton(text="WA71"),  "WB71",  "WC71"])
lw711 = ttk.TTkTreeWidgetItem([ttk.TTkRadioButton(text="WA711"), "WB711", "WC711"])

lw1.addChild(lw11)
lw11.addChild(lw111)

lw4.addChild(lw41)
lw41.addChild(lw411)

tw.addTopLevelItem(l1)
tw.addTopLevelItem(lw1)
tw.addTopLevelItem(l2)
tw.addTopLevelItem(lw2)
tw.addTopLevelItem(l3)
tw.addTopLevelItem(lw3)
tw.addTopLevelItem(l4)
tw.addTopLevelItem(lw4)
tw.addTopLevelItem(lw5)
tw.addTopLevelItem(lw6)
tw.addTopLevelItem(lw7)
l1.setExpanded(True)
l3.setExpanded(True)

# test Adding child after
lw5.addChild(lw51)
lw51.addChild(lw511)
lw6.addChild(lw61)
lw61.addChild(lw611)
lw7.addChild(lw71)
lw71.addChild(lw711)

sb1 = ttk.TTkSpinBox(parent=root, pos=(0,0), size=(10,1), value=4)

def _changeSize1(v):
    w,h = btn1.size()
    btn1.resize(w,v)

sb1.valueChanged.connect(_changeSize1)

sb2 = ttk.TTkSpinBox(parent=root, pos=(15,0), size=(10,1), value=3)

def _changeSize2(v):
    w,h = btn2.size()
    btn2.resize(w,v)

sb2.valueChanged.connect(_changeSize2)

root.mainloop()
