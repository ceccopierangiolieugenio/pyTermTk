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

t1 = [(i,i,i)    for i in range(1000)]
d1 = [{'a':i,'b':i,'c':i} for i in range(1000)]
c = [_C(i,i,i)    for i in range(1000)]
cs = [_CS(i,i,i)   for i in range(1000)]
dc1 = [_DC1(i,i,i)  for i in range(1000)]
dc1s = [_DC1S(i,i,i) for i in range(1000)]
dc2 = [_DC2(i,i,i)  for i in range(1000)]
dc2s = [_DC2S(i,i,i) for i in range(1000)]
dc3 = [_DC3(i,i,i)  for i in range(1000)]
dc3s = [_DC3S(i,i,i) for i in range(1000)]

def test_ti_1_Init_1(): return len([{'a':i,'b':i,'c':i}      for i in range(100)])
def test_ti_1_Init_3(): return len([(i,i,i)      for i in range(100)])
def test_ti_1_Init_4(): return len([_C(i,i,i)    for i in range(100)])
def test_ti_1_Init_5(): return len([_CS(i,i,i)   for i in range(100)])
def test_ti_1_Init_6_1(): return len([_DC1(i,i,i)  for i in range(100)])
def test_ti_1_Init_6_2(): return len([_DC1S(i,i,i) for i in range(100)])
def test_ti_1_Init_7_1(): return len([_DC2(i,i,i)  for i in range(100)])
def test_ti_1_Init_7_2(): return len([_DC2S(i,i,i) for i in range(100)])
def test_ti_1_Init_8_1(): return len([_DC3(i,i,i)  for i in range(100)])
def test_ti_1_Init_8_2(): return len([_DC3S(i,i,i) for i in range(100)])

def test_ti_2_Access_1(): return sum(i['a']+i['b']+i['c'] for i in d1)
def test_ti_2_Access_2(): return sum(sum(i) for i in t1)
def test_ti_2_Access_3(): return sum(i[0]+i[1]+i[2] for i in t1)
def test_ti_2_Access_4(): return sum(i.a+i.b+i.c for i in c)
def test_ti_2_Access_5(): return sum(i.a+i.b+i.c for i in cs)
def test_ti_2_Access_6_1(): return sum(i.a+i.b+i.c for i in dc1)
def test_ti_2_Access_6_2(): return sum(i.a+i.b+i.c for i in dc1s)
def test_ti_2_Access_7_1(): return sum(i.a+i.b+i.c for i in dc2)
def test_ti_2_Access_7_2(): return sum(i.a+i.b+i.c for i in dc2s)
def test_ti_2_Access_8_1(): return sum(i.a+i.b+i.c for i in dc3)
def test_ti_2_Access_8_2(): return sum(i.a+i.b+i.c for i in dc3s)

loop = 10000

a:dict = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
