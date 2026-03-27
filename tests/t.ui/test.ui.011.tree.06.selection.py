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

import os
import sys
import argparse

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Full Screen', action='store_true')
args = parser.parse_args()

root = ttk.TTk(mouseTrack=True)

if args.f:
    rootWidget = root
    root.setLayout(ttk.TTkGridLayout())
else:
    rootWidget = ttk.TTkWindow(parent=root, pos=(0,0), size=(120,40), title="Test Tree Selection", layout=ttk.TTkGridLayout(), border=True)

# Left panel: tree
tw = ttk.TTkTree()
tw.setHeaderLabels(["Name", "Type", "Value"])

# Populate tree items
items = []
for i in range(5):
    item = ttk.TTkTreeWidgetItem([f"Item {i}", f"Type {chr(65+i)}", f"Val {i*10}"])
    for j in range(3):
        child = ttk.TTkTreeWidgetItem([f"Child {i}.{j}", f"Sub {chr(65+i)}", f"{i*10+j}"])
        item.addChild(child)
    tw.addTopLevelItem(item)
    items.append(item)
items[0].setExpanded(True)
items[2].setExpanded(True)

# Right panel: controls
controlLayout = ttk.TTkGridLayout()
controlFrame = ttk.TTkFrame(border=True, title="Controls", layout=controlLayout)

# Selection mode radio buttons
row = 0
controlLayout.addWidget(ttk.TTkLabel(text="Selection Mode:", maxHeight=1), row, 0, 1, 2)
row += 1
rbNoSel    = ttk.TTkRadioButton(text="NoSelection",     radiogroup="selMode", maxHeight=1)
rbSingle   = ttk.TTkRadioButton(text="SingleSelection", radiogroup="selMode", maxHeight=1, checked=True)
rbMulti    = ttk.TTkRadioButton(text="MultiSelection",  radiogroup="selMode", maxHeight=1)
controlLayout.addWidget(rbNoSel,  row, 0, 1, 2) ; row += 1
controlLayout.addWidget(rbSingle, row, 0, 1, 2) ; row += 1
controlLayout.addWidget(rbMulti,  row, 0, 1, 2) ; row += 1

@ttk.pyTTkSlot()
def _setNoSel():
    tw.setSelectionMode(ttk.TTkK.SelectionMode.NoSelection)
    ttk.TTkLog.debug("Selection mode: NoSelection")

@ttk.pyTTkSlot()
def _setSingle():
    tw.setSelectionMode(ttk.TTkK.SelectionMode.SingleSelection)
    ttk.TTkLog.debug("Selection mode: SingleSelection")

@ttk.pyTTkSlot()
def _setMulti():
    tw.setSelectionMode(ttk.TTkK.SelectionMode.MultiSelection)
    ttk.TTkLog.debug("Selection mode: MultiSelection")

rbNoSel.clicked.connect(_setNoSel)
rbSingle.clicked.connect(_setSingle)
rbMulti.clicked.connect(_setMulti)

# Selection API buttons
controlLayout.addWidget(ttk.TTkLabel(text="Selection API:", maxHeight=1), row, 0, 1, 2) ; row += 1

btnSelectItem0   = ttk.TTkButton(text="selectItem(Item 0)",      maxHeight=3, border=True)
btnSelectItem2   = ttk.TTkButton(text="selectItem(Item 2)",      maxHeight=3, border=True)
btnDeselectItem0 = ttk.TTkButton(text="deselectItem(Item 0)",    maxHeight=3, border=True)
btnDeselectItem2 = ttk.TTkButton(text="deselectItem(Item 2)",    maxHeight=3, border=True)
btnSetCurrent1   = ttk.TTkButton(text="setCurrentItem(Item 1)",  maxHeight=3, border=True)
btnSetCurrentNone= ttk.TTkButton(text="setCurrentItem(None)",    maxHeight=3, border=True)
btnClearSel      = ttk.TTkButton(text="clearSelection()",        maxHeight=3, border=True)
btnShowSel       = ttk.TTkButton(text="Show selectedItems()",    maxHeight=3, border=True)

controlLayout.addWidget(btnSelectItem0,   row, 0) ; controlLayout.addWidget(btnSelectItem2,   row, 1) ; row += 1
controlLayout.addWidget(btnDeselectItem0, row, 0) ; controlLayout.addWidget(btnDeselectItem2, row, 1) ; row += 1
controlLayout.addWidget(btnSetCurrent1,   row, 0) ; controlLayout.addWidget(btnSetCurrentNone,row, 1) ; row += 1
controlLayout.addWidget(btnClearSel,      row, 0) ; controlLayout.addWidget(btnShowSel,       row, 1) ; row += 1

btnSelectItem0.clicked.connect(  lambda: (tw.selectItem(items[0]),   ttk.TTkLog.debug(f"selectItem: {items[0].data(0)}")))
btnSelectItem2.clicked.connect(  lambda: (tw.selectItem(items[2]),   ttk.TTkLog.debug(f"selectItem: {items[2].data(0)}")))
btnDeselectItem0.clicked.connect(lambda: (tw.deselectItem(items[0]), ttk.TTkLog.debug(f"deselectItem: {items[0].data(0)}")))
btnDeselectItem2.clicked.connect(lambda: (tw.deselectItem(items[2]), ttk.TTkLog.debug(f"deselectItem: {items[2].data(0)}")))
btnSetCurrent1.clicked.connect(  lambda: (tw.setCurrentItem(items[1]), ttk.TTkLog.debug(f"setCurrentItem: {items[1].data(0)}")))
btnSetCurrentNone.clicked.connect(lambda: (tw.setCurrentItem(None),  ttk.TTkLog.debug("setCurrentItem: None")))
btnClearSel.clicked.connect(     lambda: (tw.clearSelection(),       ttk.TTkLog.debug("clearSelection")))
btnShowSel.clicked.connect(      lambda: ttk.TTkLog.debug(f"selectedItems: {[i.data(0) for i in tw.selectedItems()]}"))

controlLayout.addWidget(ttk.TTkSpacer(), row, 0, 1, 2)

# Log viewer at the bottom
logViewer = ttk.TTkLogViewer()

# Layout: tree left, controls right, log bottom
splitterH = ttk.TTkSplitter()
splitterH.addWidget(tw)
splitterH.addWidget(controlFrame)

splitterV = ttk.TTkSplitter(orientation=ttk.TTkK.VERTICAL)
splitterV.addWidget(splitterH)
splitterV.addWidget(logViewer)

rootWidget.layout().addWidget(splitterV)

root.mainloop()
