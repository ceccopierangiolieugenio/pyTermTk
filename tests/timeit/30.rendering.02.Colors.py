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

c01 = [ttk.TTkColor.fg(  f'#0000{x:02X}') for x in range(200)]
c02 = [ttk.TTkColor.bg(  f'#0000{x:02X}') for x in range(200)]
c03 = [ttk.TTkColor.fg(  f'#0000{x:02X}')+ttk.TTkColor.UNDERLINE for x in range(200)]
c04 = [ttk.TTkColor.bg(  f'#0000{x:02X}')+ttk.TTkColor.UNDERLINE for x in range(200)]
c10 = [ttk.TTkColor.fgbg(f'#0000{x:02X}',f'#0000{x:02X}') for x in range(200)]
c11 = [ttk.TTkColor.fgbg(f'#0000{x:02X}',f'#0000{x:02X}')+ttk.TTkColor.BOLD for x in range(200)]
c20 = [ttk.TTkColor.fgbg(f'#0000{x:02X}',f'#0000{x:02X}','http://www.example.com/{x:02X}')+ttk.TTkColor.UNDERLINE for x in range(200)]

def test_ti_01():  return len(''.join([str(x) for x in c01]))
def test_ti_02():  return len(''.join([str(x) for x in c02]))
def test_ti_03():  return len(''.join([str(x) for x in c03]))
def test_ti_04():  return len(''.join([str(x) for x in c04]))
def test_ti_10():  return len(''.join([str(x) for x in c10]))
def test_ti_11():  return len(''.join([str(x) for x in c11]))
def test_ti_20():  return len(''.join([str(x) for x in c20]))

loop = 10000

a = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
