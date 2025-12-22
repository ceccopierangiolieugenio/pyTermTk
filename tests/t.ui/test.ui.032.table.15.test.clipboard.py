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

'''
TTkTable Clipboard Operations Example
======================================

This example demonstrates table clipboard functionality and complex data types.

Key Features:
- Clipboard operations (copy/paste) with Ctrl+C/Ctrl+Z signals enabled
- Mixed data types in cells:
  * Hex numbers (formatted strings)
  * TTkString with colors
  * Boolean values
  * TTkCellListType (dropdown lists)
  * Custom Enum types
  * datetime.time objects
  * datetime.date objects
  * datetime.datetime objects
- Random data generation for dates and times
- Signal mask configuration for clipboard shortcuts

Usage:
- Select cells and press Ctrl+C to copy
- Use Ctrl+Z for undo (if enabled in application)

This example shows how TTkTable handles various Python data types
and provides built-in clipboard support.
'''

import os
import sys
import argparse
import random
import datetime
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

# Helper function to generate random dates within a range
def random_date(start_date, end_date):
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + datetime.timedelta(days=random_days)

# Helper function to generate random times
def random_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime.time(hour, minute, second)

# Helper function to generate random datetimes within a range
def random_datetime(start_datetime, end_datetime):
    time_between = end_datetime - start_datetime
    total_seconds = int(time_between.total_seconds())
    random_seconds = random.randrange(total_seconds)
    return start_datetime + datetime.timedelta(seconds=random_seconds)


class MyEnum(Enum):
    Foo=auto()
    Bar=auto()
    Baz=auto()

    def __str__(self):
        return self.name

class MyEnumYesNo(Enum):
    Yes=True
    No=False

    def __str__(self):
        return self.name
    def __bool__(self):
        return self.value

data_list = [
    'Pippo', 'Pluto', 'Paperino',
    'Qui', 'Quo', 'Qua', # L'accento non ci va
    'Minnie', 'Topolino'
]

data = [
    [
        bool(random.randint(0,1)),
        'Pippo',
        'Pluto',
        ttk.TTkCellListType(value=random.choice(data_list), items=data_list)
    ] for y in range(20)
]

data = [
    [
        f"0x{random.randint(0,0xFFFF):04X}",
        ttk.TTkString(f"0x{random.randint(0,0xFFFF):04X}", ttk.TTkColor.YELLOW),
        bool(random.randint(0,1)),
        ttk.TTkCellListType(value=random.choice(data_list), items=data_list),
        random.choice(list(MyEnum)),
        random.choice(list(MyEnumYesNo)),
        random_time(),
        random_date(datetime.date(2020,1,1), datetime.date(2025,12,31)),
        random_datetime(datetime.datetime(2020,1,1), datetime.datetime(2025,12,31)),

    ] for y in range(20)
]

root = ttk.TTk(
    title="pyTermTk Table Demo",
    mouseTrack=mouseTrack,
    sigmask=(
        ttk.TTkTerm.Sigmask.CTRL_Z |
        ttk.TTkTerm.Sigmask.CTRL_C ))

if fullScreen:
    rootContainer = root
    root.setLayout(ttk.TTkGridLayout())
else:
    rootContainer = ttk.TTkWindow(parent=root,pos = (0,0), size=(150,40), title="Test Table 1", layout=ttk.TTkGridLayout(), border=True)

table_model = ttk.TTkTableModelList(data=data)
table = ttk.TTkTable(tableModel=table_model)
btn_quit = ttk.TTkButton(text='quit', maxSize=(8,3), border=True)
rootContainer.layout().addWidget(table,1,0,1,2)
rootContainer.layout().addWidget(btn_quit,0,0)

table.resizeRowsToContents()
table.resizeColumnsToContents()

btn_quit.clicked.connect(root.quit)

root.mainloop()