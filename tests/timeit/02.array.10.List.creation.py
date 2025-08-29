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

from __future__ import annotations

import sys, os

from dataclasses import dataclass
from enum import Enum,Flag,auto
import timeit

from typing import List, Tuple, Iterator

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

import TermTk as ttk

txt = "Eugenio"

l = [txt] * 1000000
l1 = [txt] * 1000000
l2 = [txt] * 1000000
l3 = [txt] * 1000000
l4 = [txt] * 1000000

def test_ti_01_append():
    _ret = []
    for i in l:
        _ret.append(i)
    return len(_ret)

def test_ti_02_copy():
    _ret = []
    _ret[:] = l
    return len(_ret)

def test_ti_03_copy_2():
    _ret = [None]*len(l)
    for i,ii in enumerate(l):
        _ret[i] = ii
    return len(_ret)

def test_ti_03_copy_3():
    _ret = []
    for i in range(len(l) // 256):
        _ret.extend(l[i:i+256])
    return len(_ret)

def test_ti_03_copy_4():
    _ret = []
    _ret.extend(l)
    return len(_ret)

def test_ti_03_copy_5():
    _ret = l.copy()
    return len(_ret)

def test_ti_04_reduce_01():
    _ret = l4[:5000]
    return len(_ret)

loop = 100

a:dict = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
