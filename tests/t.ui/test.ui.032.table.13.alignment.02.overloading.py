#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
# https://www.daniweb.com/programming/software-development/code/447834/applying-pyside-s-qabstracttablemodel

import os
import sys
import csv
import re
import argparse
import operator
import json
import random
from typing import Tuple

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Full Screen (default)', action='store_true')
parser.add_argument('-w', help='Windowed',    action='store_true')

args = parser.parse_args()

fullScreen = not args.w
mouseTrack = True

class MyTableModel(ttk.TTkTableModelList):
    def headerData(self, num, orientation):
        if orientation == ttk.TTkK.HORIZONTAL:
            if 0 == num%4:
                return f"{num} Left"
            if 1 == num%4:
                return f"{num} Center"
            if 2 == num%4:
                return f"{num} Right"
            if 3 == num%4:
                return f"{num} Justified"
        return super().headerData(num, orientation)

    def displayData(self:ttk.TTkTableModelList, row:int, col:int) -> Tuple[ttk.TTkString, ttk.TTkK.Alignment]:
        if 0 == col%4:
            return self.ttkStringData(row, col), ttk.TTkK.Alignment.LEFT_ALIGN
        if 1 == col%4:
            return self.ttkStringData(row, col), ttk.TTkK.Alignment.CENTER_ALIGN
        if 2 == col%4:
            return self.ttkStringData(row, col), ttk.TTkK.Alignment.RIGHT_ALIGN
        if 3 == col%4:
            return self.ttkStringData(row, col), ttk.TTkK.Alignment.JUSTIFY
        return super().displayData(row,col)

data_list1 = [[f"{y:03}\npippo\npeppo-ooo"]+[str(x) for x in range(10) ] for y in range(20)]
data_list1[1][1] = "abc def ghi\ndef ghi\nghi\njkl - pippo"
data_list1[2][2] = "abc def ghi\ndef ghi\nghi\njkl - pippo"
data_list1[3][3] = "abc def ghi\ndef ghi a b c de fgh s\nghi\njkl - pippo"
data_list1[4][4] = "abc def ghi\ndef ghi\nghi\njkl - pippo"
data_list1[5][5] = "abc def ghi\ndef ghi\nghi\njkl - pippo"

root = ttk.TTk(title="pyTermTk Table Demo",
               mouseTrack=mouseTrack)

if fullScreen:
    rootTable = root
    root.setLayout(ttk.TTkGridLayout())
else:
    rootTable = ttk.TTkWindow(parent=root,pos = (0,0), size=(150,40), title="Test Table 1", layout=ttk.TTkGridLayout(), border=True)

table_model1 = MyTableModel(data=data_list1)
table = ttk.TTkTable(parent=rootTable, tableModel=table_model1)
table.resizeRowsToContents()
table.resizeColumnsToContents()

root.mainloop()