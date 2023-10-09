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

import sys, os, argparse, math, random


sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

sys.path.append(os.path.join(sys.path[0],'..'))
from showcase._showcasehelper import getUtfWord

def demoList(root= None):
    # Define the main Layout
    retFrame = ttk.TTkFrame(parent=root, layout=(rootLayout:=ttk.TTkGridLayout()))

    # Define the main Layout
    win1    = ttk.TTkWindow(title="Single List",      layout=ttk.TTkVBoxLayout())
    win2    = ttk.TTkWindow(title="Multi List",       layout=ttk.TTkVBoxLayout())
    win3    = ttk.TTkWindow(title="Log",              layout=ttk.TTkVBoxLayout())
    win4    = ttk.TTkWindow(title="Oly Drag Allowed", layout=ttk.TTkVBoxLayout())
    win5    = ttk.TTkWindow(title="Oly Drop Allowed", layout=ttk.TTkVBoxLayout())
    layout1 = ttk.TTkLayout()

    # Place the widgets in the root layout
    rootLayout.addWidget(win1,0,0)
    rootLayout.addWidget(win2,0,1)
    rootLayout.addWidget(win3,0,2,1,3)
    rootLayout.addItem(layout1,1,0,1,3)
    rootLayout.addWidget(win4,1,3)
    rootLayout.addWidget(win5,1,4)

    # Single Selection List
    listWidgetSingle = ttk.TTkList(parent=win1, maxWidth=40, minWidth=10)

    # Multi Selection List
    listWidgetMulti = ttk.TTkList(parent=win2, maxWidth=40, minWidth=10, selectionMode=ttk.TTkK.MultiSelection)

    # Multi Selection List - Drag Allowed
    listWidgetDrag = ttk.TTkList(parent=win4, maxWidth=40, minWidth=10, dragDropMode=ttk.TTkK.DragDropMode.AllowDrag)
    listWidgetDrop = ttk.TTkList(parent=win5, maxWidth=40, minWidth=10, dragDropMode=ttk.TTkK.DragDropMode.AllowDrop)

    # Log Viewer
    label1 = ttk.TTkLabel(pos=(10,0), text="[ list1 ]",maxHeight=2)
    label2 = ttk.TTkLabel(pos=(10,1), text="[ list2 ]",maxHeight=2)
    ttk.TTkLogViewer(parent=win3)

    btn_mv1 = ttk.TTkButton(pos=(0,0), text=" >> ")
    btn_mv2 = ttk.TTkButton(pos=(0,1), text=" << ")
    btn_del = ttk.TTkButton(pos=(0,2), text="Delete")
    layout1.addWidgets([label1,label2,btn_mv1,btn_mv2,btn_del])

    @ttk.pyTTkSlot(str)
    def _listCallback1(label):
        ttk.TTkLog.info(f'Clicked label1: "{label}"')
        label1.setText(f'[ list1 ] clicked "{label}" - Selected: {[str(s) for s in listWidgetSingle.selectedLabels()]}')

    @ttk.pyTTkSlot(str)
    def _listCallback2(label):
        ttk.TTkLog.info(f'Clicked label2: "{label}" - selected: {[str(s) for s in listWidgetMulti.selectedLabels()]}')
        label2.setText(f'[ list2 ] clicked "{label}" - {[str(s) for s in listWidgetMulti.selectedLabels()]}')

    @ttk.pyTTkSlot()
    def _moveToRight2():
        for i in listWidgetSingle.selectedItems().copy():
            listWidgetSingle.removeItem(i)
            listWidgetMulti.addItemAt(i,0)

    @ttk.pyTTkSlot()
    def _moveToLeft1():
        for i in listWidgetMulti.selectedItems().copy():
            listWidgetMulti.removeItem(i)
            listWidgetSingle.addItemAt(i,0)

    @ttk.pyTTkSlot()
    def _delSelected():
        items = listWidgetMulti.selectedItems()
        listWidgetMulti.removeItems(items)
        items = listWidgetSingle.selectedItems()
        listWidgetSingle.removeItems(items)


    btn_mv1.clicked.connect(_moveToRight2)
    btn_mv2.clicked.connect(_moveToLeft1)
    btn_del.clicked.connect(_delSelected)


    # Connect the signals to the 2 slots defines
    listWidgetSingle.textClicked.connect(_listCallback1)
    listWidgetMulti.textClicked.connect(_listCallback2)

    # populate the lists with random entries
    for i in range(50):
        listWidgetSingle.addItem(f"S-{i}) {getUtfWord()} {getUtfWord()}")
        listWidgetMulti.addItem( f"M-{i}){getUtfWord()} {getUtfWord()}")
        listWidgetDrag.addItem( f"D-{i}){getUtfWord()} {getUtfWord()}")

    return retFrame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen (default)', action='store_true')
    parser.add_argument('-w', help='Windowed',    action='store_true')
    parser.add_argument('-t', help='Track Mouse', action='store_true')
    args = parser.parse_args()
    windowed = args.w
    mouseTrack = args.t

    root = ttk.TTk(title="pyTermTk List Demo", mouseTrack=mouseTrack)
    if windowed:
        rootTab = ttk.TTkWindow(parent=root,pos=(1,1), size=(100,40), title="Test Tab", border=True, layout=ttk.TTkGridLayout())
    else:
        rootTab = root
        root.setLayout(ttk.TTkGridLayout())
    demoList(rootTab)
    root.mainloop()

if __name__ == "__main__":
    main()