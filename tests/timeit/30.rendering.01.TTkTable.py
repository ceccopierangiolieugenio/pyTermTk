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


import os
import sys
import argparse
import operator
import json
import timeit

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

imagesFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../ansi.images.json')
with open(imagesFile) as f:
    d = json.load(f)
    # Image exported by the Dumb Paint Tool
    pepper   = ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['pepper'])
    python   = ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['python'])
    fire     = ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['fire'])
    fireMini = ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['fireMini'])
    img_pepper   = ttk.TTkString(pepper)
    img_python   = ttk.TTkString(python)
    img_fire     = ttk.TTkString(fire)
    img_fireMini = ttk.TTkString(fireMini)

class MyTableModel(ttk.TTkAbstractTableModel):
    def __init__(self, mylist, *args):
        super().__init__(*args)
        self.mylist = mylist

    def rowCount(self):        return len(self.mylist)
    def columnCount(self):     return len(self.mylist[0])
    def data(self, row, col):  return self.mylist[row][col]
    def headerData(self, num, orientation):
        prefix = ['aa','bb','cc','dd','ee','ff','gg','Euge']
        return f"{prefix[num%len(prefix)]}:{num:03}"

# use numbers for numeric data to sort properly
txt1 = "Text"
txt2 = txt1*10
txt3 = '\n'.join([txt1*2]*5)
txt4 = '\n'.join([txt1*5]*10)
txt5 = ttk.TTkString(txt4, ttk.TTkColor.RED + ttk.TTkColor.BG_BLUE)

data_lists = [
    [[txt1           for y in range(100)] for x in range(1000)],
    [[txt2           for y in range(100)] for x in range(1000)],
    [[txt3           for y in range(100)] for x in range(1000)],
    [[txt4           for y in range(100)] for x in range(1000)],
    [[txt5           for y in range(100)] for x in range(1000)],
    [[1234567        for y in range(100)] for x in range(1000)],
    [[1234567.123456 for y in range(100)] for x in range(1000)],
    [[img_fireMini   for y in range(100)] for x in range(1000)],
    [[img_python     for y in range(100)] for x in range(1000)],
    [[fireMini       for y in range(100)] for x in range(1000)],
    [[python         for y in range(100)] for x in range(1000)]]

table_models = [MyTableModel(dl) for dl in data_lists]
tables = [ttk.TTkTableWidget(tableModel=tm) for tm in table_models]

def paint(table):
    canvas = table.getCanvas()
    return table.paintEvent(canvas)

def resize1():
    [t.resize(200,50)  for t in tables]
def resize2():
    [t.resize(500,200) for t in tables]

tests = [
    lambda : [t.resize(200,50)  for t in tables],
    lambda : paint(tables[0]),
    lambda : paint(tables[1]),
    lambda : paint(tables[2]),
    lambda : paint(tables[3]),
    lambda : paint(tables[4]),
    lambda : paint(tables[5]),
    lambda : paint(tables[6]),
    lambda : paint(tables[7]),
    lambda : paint(tables[8]),
    lambda : paint(tables[9]),
    lambda : paint(tables[10]),

    lambda : [t.resize(500,200)  for t in tables],
    lambda : paint(tables[0]),
    lambda : paint(tables[1]),
    lambda : paint(tables[2]),
    lambda : paint(tables[3]),
    lambda : paint(tables[4]),
    lambda : paint(tables[5]),
    lambda : paint(tables[6]),
    lambda : paint(tables[7]),
    lambda : paint(tables[8]),
    lambda : paint(tables[9]),
    lambda : paint(tables[10]) ]

def test_ti_01():  return tests[0]()
def test_ti_02():  return tests[1]()
def test_ti_03():  return tests[2]()
def test_ti_04():  return tests[3]()
def test_ti_05():  return tests[4]()
def test_ti_06():  return tests[5]()
def test_ti_07():  return tests[6]()
def test_ti_08():  return tests[7]()
def test_ti_09():  return tests[8]()
def test_ti_10():  return tests[9]()
def test_ti_11():  return tests[10]()
def test_ti_12():  return tests[11]()
def test_ti_13():  return tests[12]()
def test_ti_14():  return tests[13]()
def test_ti_15():  return tests[14]()
def test_ti_16():  return tests[15]()
def test_ti_17():  return tests[16]()
def test_ti_18():  return tests[17]()
def test_ti_19():  return tests[18]()
def test_ti_20():  return tests[19]()
def test_ti_21():  return tests[20]()
def test_ti_22():  return tests[21]()

for t in tables: t.resize(500,200)

loop = 10

a = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
