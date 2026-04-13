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

import sys

from dataclasses import dataclass
from enum import Enum,Flag,auto
from typing import NamedTuple
import timeit

from typing import List, Tuple, Iterator

class _C():
    a:int
    b:int
    c:int
    def __init__(self, a:int,b:int,c:int):
        self.a = a
        self.b = b
        self.c = c

class _CS():
    __slots__ = ('a','b','c')
    a:int
    b:int
    c:int
    def __init__(self, a:int,b:int,c:int):
        self.a = a
        self.b = b
        self.c = c

@dataclass
class _DC1():
    a:int
    b:int
    c:int

@dataclass
class _DC1S():
    __slots__ = ('a','b','c')
    a:int
    b:int
    c:int

@dataclass()
class _DC2():
    a:int
    b:int
    c:int

@dataclass()
class _DC2S():
    __slots__ = ('a','b','c')
    a:int
    b:int
    c:int

@dataclass(frozen=True)
class _DC3():
    a:int
    b:int
    c:int

@dataclass(frozen=True, slots=True)
class _DC3S():
    a:int
    b:int
    c:int

# Optimization approaches for keyword argument overhead

# 1. Factory function (pre-baked positional)
def _DC1S_factory(a: int, b: int, c: int) -> _DC1S:
    return _DC1S(a, b, c)

# 2. Direct object creation + setattr bypass
def _DC1S_direct(a: int, b: int, c: int) -> _DC1S:
    obj = object.__new__(_DC1S)
    object.__setattr__(obj, 'a', a)
    object.__setattr__(obj, 'b', b)
    object.__setattr__(obj, 'c', c)
    return obj

# 3. Pre-cached init method
_DC1S_init_method = _DC1S.__init__
def _DC1S_cached(a: int, b: int, c: int) -> _DC1S:
    obj = object.__new__(_DC1S)
    _DC1S_init_method(obj, a, b, c)
    return obj

class _NT(NamedTuple):
    a:int
    b:int
    c:int


t1 = [(i,i,i)    for i in range(1000)]
l1 = [[i,i,i]    for i in range(1000)]
d1 = [{'a':i,'b':i,'c':i} for i in range(1000)]
c = [_C(i,i,i)    for i in range(1000)]
cs = [_CS(i,i,i)   for i in range(1000)]
dc1 = [_DC1(i,i,i)  for i in range(1000)]
dc1s = [_DC1S(i,i,i) for i in range(1000)]
dc2 = [_DC2(i,i,i)  for i in range(1000)]
dc2s = [_DC2S(i,i,i) for i in range(1000)]
dc3 = [_DC3(i,i,i)  for i in range(1000)]
dc3s = [_DC3S(i,i,i) for i in range(1000)]
nt = [_NT(i,i,i)  for i in range(1000)]


lists = {
    'tuple': t1,
    'list': l1,
    'dict': d1,
    '_C': c,
    '_CS': cs,
    '_DC1': dc1,
    '_DC1S': dc1s,
    '_DC2': dc2,
    '_DC2S': dc2s,
    '_DC3': dc3,
    '_NT': nt,
}

for name, lst in lists.items():
    total = sum(sys.getsizeof(item) for item in lst)
    avg = total / len(lst) if lst else 0
    print(f"{name:10} - Total: {total:8} bytes, Avg per instance: {avg:6.1f} bytes")

def test_ti_1_Init_01_0(): return len([{'a':i,'b':i,'c':i}      for i in range(100)])
def test_ti_1_Init_02_0(): return len([[i,i,i]      for i in range(100)])
def test_ti_1_Init_03_0(): return len([(i,i,i)      for i in range(100)])
def test_ti_1_Init_04_0(): return len([_C(i,i,i)    for i in range(100)])
def test_ti_1_Init_05_0(): return len([_CS(i,i,i)   for i in range(100)])
def test_ti_1_Init_06_1(): return len([_DC1(i,i,i)  for i in range(100)])
def test_ti_1_Init_06_2(): return len([_DC1S(i,i,i) for i in range(100)])
def test_ti_1_Init_06_3(): return len([_DC1S(a=i,b=i,c=i) for i in range(100)])
def test_ti_1_Init_07_1(): return len([_DC2(i,i,i)  for i in range(100)])
def test_ti_1_Init_07_2(): return len([_DC2S(i,i,i) for i in range(100)])
def test_ti_1_Init_08_1(): return len([_DC3(i,i,i)  for i in range(100)])
def test_ti_1_Init_08_2(): return len([_DC3S(i,i,i) for i in range(100)])
def test_ti_1_Init_09_1(): return len([_DC1S_factory(i,i,i) for i in range(100)])
def test_ti_1_Init_09_2(): return len([_DC1S_direct(i,i,i) for i in range(100)])
def test_ti_1_Init_09_3(): return len([_DC1S_cached(i,i,i) for i in range(100)])
def test_ti_1_Init_10_1(): return len([_NT(i,i,i)  for i in range(100)])
def test_ti_1_Init_10_2(): return len([_NT(a=i,b=i,c=i)  for i in range(100)])

def test_ti_2_Access_01_0(): return sum(i['a']+i['b']+i['c'] for i in d1)
def test_ti_2_Access_02_1(): return sum(sum(i) for i in l1)
def test_ti_2_Access_02_2(): return sum(i[0]+i[1]+i[2] for i in l1)
def test_ti_2_Access_03_1(): return sum(sum(i) for i in t1)
def test_ti_2_Access_03_2(): return sum(i[0]+i[1]+i[2] for i in t1)
def test_ti_2_Access_05_0(): return sum(i.a+i.b+i.c for i in c)
def test_ti_2_Access_06_0(): return sum(i.a+i.b+i.c for i in cs)
def test_ti_2_Access_07_1(): return sum(i.a+i.b+i.c for i in dc1)
def test_ti_2_Access_07_2(): return sum(i.a+i.b+i.c for i in dc1s)
def test_ti_2_Access_08_1(): return sum(i.a+i.b+i.c for i in dc2)
def test_ti_2_Access_08_2(): return sum(i.a+i.b+i.c for i in dc2s)
def test_ti_2_Access_09_1(): return sum(i.a+i.b+i.c for i in dc3)
def test_ti_2_Access_09_2(): return sum(i.a+i.b+i.c for i in dc3s)
def test_ti_2_Access_10_1(): return sum(i.a+i.b+i.c for i in nt)

loop = 10000

a:dict = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
