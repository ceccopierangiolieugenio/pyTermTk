#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys,os

import timeit

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk/'))
import TermTk as ttk
from TermTk.TTkLayouts.layout import TTkWidgetItem, TTkLayout

layouts = [
    TTkLayout() if i%4 else TTkWidgetItem(widget=ttk.TTkWidget())
    for i in range(400)
]

def test_ti_1_Bisect_01_01():
    return sum(i._layoutItemType == ttk.TTkK.LayoutItemTypes.LayoutItem for i in layouts)

def test_ti_1_Bisect_01_02():
    return sum(isinstance(i, TTkLayout) for i in layouts)

def test_ti_1_Bisect_01_03():
    return sum(i._layoutItemType == ttk.TTkK.LayoutItemTypes.WidgetItem for i in layouts)

def test_ti_1_Bisect_01_04():
    return sum(isinstance(i, TTkWidgetItem) for i in layouts)

def test_ti_1_Bisect_01_05():
    return sum(isinstance(i, ttk.TTkWidget) for i in layouts)

def test_ti_1_Bisect_01_06():
    return sum(i._layoutItemType is ttk.TTkK.LayoutItemTypes.LayoutItem for i in layouts)

def test_ti_1_Bisect_01_07():
    return sum(i._layoutItemType is ttk.TTkK.LayoutItemTypes.WidgetItem for i in layouts)

loop = 10000

a:dict = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
