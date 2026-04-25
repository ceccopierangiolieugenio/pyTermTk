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

import sys

from dataclasses import dataclass
from bisect import bisect_left, bisect_right
import timeit

from typing import List, Tuple, Iterator

@dataclass
class _WrapLine():
    __slots__ = ('line', 'start', 'stop')
    line:int
    start: int
    stop:int

class _BisectKeyLine:
    __slots__ = ('_buf',)
    _buf:List[_WrapLine]
    def __init__(self, buf:List[_WrapLine]):
        self._buf = buf
    def __len__(self) -> int:
        return len(self._buf)
    def __getitem__(self, i) -> int:
        return self._buf[i].line

buffer = [_WrapLine(i,i,i) for i in range(10000)]
keys = _BisectKeyLine(buffer)

def test_ti_1_Bisect_01_01():
    a = bisect_left(keys, 9999)
    b = bisect_right(keys, 9999)
    return a+b

def test_ti_1_Bisect_01_02():
    a = bisect_left(buffer, 9999, key=lambda x:x.line)
    b = bisect_right(buffer, 9999, key=lambda x:x.line)
    return a+b

loop = 10000

a:dict = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
