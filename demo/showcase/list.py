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

from showcase._showcasehelper import getUtfWord

def demoList(root= None):
    # Define the main Layout
    splitter = ttk.TTkSplitter(parent=root, orientation=ttk.TTkK.HORIZONTAL)
    frame2 = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())
    frame1 = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())
    frame3 = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())

    # Multi Selection List
    ttk.TTkLabel(parent=frame1, text="[ MultiSelect ]",maxHeight=2)
    listWidgetMulti = ttk.TTkList(parent=frame1, maxWidth=40, minWidth=10, selectionMode=ttk.TTkK.MultiSelection)

    # Single Selection List
    ttk.TTkLabel(parent=frame2, text="[ SingleSelect ]",maxHeight=2)
    listWidgetSingle = ttk.TTkList(parent=frame2, maxWidth=40, minWidth=10)

    # Log Viewer
    label1 = ttk.TTkLabel(parent=frame3, text="[ list1 ]",maxHeight=2)
    label2 = ttk.TTkLabel(parent=frame3, text="[ list2 ]",maxHeight=2)
    ttk.TTkLogViewer(parent=frame3)#, border=True)

    @ttk.pyTTkSlot(str)
    def _listCallback1(label):
        ttk.TTkLog.info(f"Clicked label1: {label}")
        label1.text = f"[ list1 ] clicked {label}"

    @ttk.pyTTkSlot(str)
    def _listCallback2(label):
        ttk.TTkLog.info(f"Clicked label2: {label} - selected: {listWidgetMulti.selectedLabels()}")
        label2.text = f"[ list2 ] {listWidgetMulti.selectedLabels()}"

    # Connect the signals to the 2 slots defines
    listWidgetSingle.textClicked.connect(_listCallback1)
    listWidgetMulti.textClicked.connect(_listCallback2)

    # populate the lists with random entries
    for i in range(100):
        listWidgetSingle.addItem(f"{i}) {getUtfWord()} {getUtfWord()}")
        listWidgetMulti.addItem(f"{getUtfWord()} {getUtfWord()}")

    return splitter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if args.f:
        rootGraph = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootGraph = ttk.TTkWindow(parent=root,pos=(1,1), size=(100,40), title="Test List", border=True, layout=ttk.TTkGridLayout())
    demoList(rootGraph)
    root.mainloop()

if __name__ == "__main__":
    main()