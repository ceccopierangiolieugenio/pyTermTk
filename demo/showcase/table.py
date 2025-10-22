#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os, argparse

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

sys.path.append(os.path.join(sys.path[0],'..'))
from showcase._showcasehelper import getUtfWord

def demoTTkTable(root= None):
    # Basic Table Demo

    # Setup a model using a 2d list of random values
    dataList = [[f"0x{i:04X}"] + [int(i*100),float(i*100),ttk.TTkString(getUtfWord(),ttk.TTkColor.YELLOW)] + [getUtfWord() for _ in range(10)] for i in range(101)]
    tableModel = ttk.TTkTableModelList(data=dataList)

    # Init the table with the model defilned
    retTable = ttk.TTkTable(parent=root, tableModel=tableModel)
    retTable.resizeRowsToContents()
    retTable.resizeColumnsToContents()

    return retTable


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
    demoTTkTable(rootTab)
    root.mainloop()

if __name__ == "__main__":
    main()