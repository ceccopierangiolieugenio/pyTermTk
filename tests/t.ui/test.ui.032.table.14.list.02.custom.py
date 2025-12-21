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
TTkTable with Custom Enum Types Example
========================================

This example demonstrates displaying Python Enum types in table cells.

Key Features:
- Custom Enum classes with auto() values
- Enum display using __str__() method
- Boolean Enum (MyEnumYesNo) with True/False values
- Mixed Enum types in different columns
- Automatic enum value rendering
- Random enum selection for variety

The table automatically displays enum values by calling their __str__() method,
making it easy to show meaningful names instead of raw enum values.

Useful for displaying categorical data, status fields, or any predefined
set of options in a human-readable format.
'''

import os
import sys
import argparse
import random
from enum import Enum

from random import choice
from enum import Enum, auto
from typing import Tuple

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Full Screen (default)', action='store_true')
parser.add_argument('-w', help='Windowed',    action='store_true')

args = parser.parse_args()

fullScreen = not args.w
mouseTrack = True

# Custom Enum for demonstrating enum display in tables
class MyEnum(Enum):
    Foo=auto()  # auto() generates sequential values automatically
    Bar=auto()
    Baz=auto()

    # Override __str__ to display the enum name instead of the full value
    def __str__(self):
        return self.name

# Boolean-like Enum that maps to True/False values
class MyEnumYesNo(Enum):
    Yes=True   # Maps to boolean True
    No=False   # Maps to boolean False

    # Display as "Yes" or "No" instead of "MyEnumYesNo.Yes"
    def __str__(self):
        return self.name

    # Allow the enum to be used in boolean contexts
    def __bool__(self):
        return self.value

data = [
    [
        bool(random.randint(0,1)),
        MyEnum.Foo,
        MyEnum.Bar,
        MyEnum.Baz,
        MyEnumYesNo.Yes,
        MyEnumYesNo.No,
        random.choice(list(MyEnum)),
        random.choice(list(MyEnumYesNo)),
    ] for y in range(20)
]

root = ttk.TTk(
    title="pyTermTk Table Demo",
    mouseTrack=mouseTrack)

if fullScreen:
    rootTable = root
    root.setLayout(ttk.TTkGridLayout())
else:
    rootTable = ttk.TTkWindow(parent=root,pos = (0,0), size=(150,40), title="Test Table 1", layout=ttk.TTkGridLayout(), border=True)

table_model = ttk.TTkTableModelList(data=data)
table = ttk.TTkTable(parent=rootTable, tableModel=table_model)

table.resizeRowsToContents()
table.resizeColumnsToContents()

root.mainloop()