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

'''
TTkTable Alignment Example (Mixin Pattern)

This example demonstrates using a mixin class to control text alignment in table cells.
The mixin pattern allows reusing alignment logic across multiple table models by inheriting
from both the mixin class and the base table model class.

Key features:
- Mixin class (MyTableMixin) containing reusable alignment logic
- Custom alignment per column using modulo arithmetic
- Multiple inheritance combining mixin with TTkTableModelList
- Preserves parent class functionality using super() calls
- Column-specific edit flags (column 0: selectable only, column 1: editable)
- Multi-line cell content demonstrating alignment effects
'''

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

# Mixin class containing reusable alignment logic
# This can be combined with any table model class via multiple inheritance
class MyTableMixin():
    # Override headerData() to label each column with its alignment type
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

    # Override displayData() to apply custom alignment
    # Note: Uses super() to get data from parent class, then modifies alignment
    def displayData(self:ttk.TTkTableModelList, row:int, col:int) -> Tuple[ttk.TTkString, ttk.TTkK.Alignment]:
        data, legacy_align = super().displayData(row,col)
        # Cycle through alignment types based on column number
        if 0 == col%4:
            return data, ttk.TTkK.Alignment.LEFT_ALIGN
        if 1 == col%4:
            return data, ttk.TTkK.Alignment.CENTER_ALIGN
        if 2 == col%4:
            return data, ttk.TTkK.Alignment.RIGHT_ALIGN
        if 3 == col%4:
            return data, ttk.TTkK.Alignment.JUSTIFY
        return data, legacy_align

# Final table model using multiple inheritance (mixin + base model)
# Order matters: MyTableMixin is checked first for method resolution
class MyTableModel(MyTableMixin, ttk.TTkTableModelList):
    # Override flags() to control which cells are editable
    def flags(self, row: int, col: int) -> ttk.TTkConstant.ItemFlag:
        if col==0:
            # Column 0: Selectable but not editable
            return (
                ttk.TTkK.ItemFlag.ItemIsEnabled  |
                ttk.TTkK.ItemFlag.ItemIsSelectable )
        if col==1:
            # Column 1: Fully editable
            return (
                ttk.TTkK.ItemFlag.ItemIsEnabled  |
                ttk.TTkK.ItemFlag.ItemIsEditable )
        return super().flags(row, col)

# Create sample data with multi-line content in first column
data_list1 = [[f"{y:03}\npippo\npeppo-ooo"]+[str(x) for x in range(10) ] for y in range(20)]

# Add long multi-line text to specific cells to demonstrate alignment
data_list1[1][1] = "abc def ghi\ndef ghi\nghi\njkl - pippo"
data_list1[2][2] = "abc def ghi\ndef ghi\nghi\njkl - pippo"
data_list1[3][3] = "abc def ghi\ndef ghi a b c de fgh s\nghi\njkl - pippo"
data_list1[4][4] = "abc def ghi\ndef ghi\nghi\njkl - pippo"
data_list1[5][5] = "abc def ghi\ndef ghi\nghi\njkl - pippo"

# Initialize the main application
root = ttk.TTk(title="pyTermTk Table Demo",
               mouseTrack=mouseTrack)

# Setup layout - either fullscreen or windowed
if fullScreen:
    rootTable = root
    root.setLayout(ttk.TTkGridLayout())
else:
    rootTable = ttk.TTkWindow(parent=root,pos = (0,0), size=(150,40), title="Test Table 1", layout=ttk.TTkGridLayout(), border=True)

# Create table with custom model using mixin pattern
table_model1 = MyTableModel(data=data_list1)
table = ttk.TTkTable(parent=rootTable, tableModel=table_model1)
table.resizeRowsToContents()    # Adjust row heights for multi-line content
table.resizeColumnsToContents() # Adjust column widths for content

root.mainloop()