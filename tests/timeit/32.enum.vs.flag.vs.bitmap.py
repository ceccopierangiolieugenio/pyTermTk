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

from dataclasses import dataclass
from enum import Enum,Flag,auto
import timeit

class PermBm(int):
    READ = 0x01
    WRITE = 0x02
    EXECUTE = 0x04

class PermEn(Enum):
    READ = 0x01
    WRITE = 0x02
    EXECUTE = 0x04

class PermFl(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()

class PermCFl():
    READ:PermCFl
    WRITE:PermCFl
    EXECUTE:PermCFl
    __slots__= ('_v')
    _v:int
    def __init__(self,v:int):
        self._v = v
    def __or__(self, other:PermCFl):
        return PermCFl(self._v|other._v)
    def __and__(self, other:PermCFl):
        return PermCFl(self._v&other._v)
    def __str__(self):
        return f"PermCFL({self._v})"
PermCFl.READ = PermCFl(0x01)
PermCFl.WRITE = PermCFl(0x02)
PermCFl.EXECUTE = PermCFl(0x04)

fff = PermFl.READ | PermFl.WRITE

print(fff)

def test_ti_0_01():
    f1 = PermFl.READ  | PermFl.WRITE
    f2 = PermFl.READ  | PermFl.EXECUTE
    f3 = PermFl.WRITE | PermFl.EXECUTE
    return f1 | f2 | f3
def test_ti_0_02():
    f1 = PermCFl.READ  | PermCFl.WRITE
    f2 = PermCFl.READ  | PermCFl.EXECUTE
    f3 = PermCFl.WRITE | PermCFl.EXECUTE
    return f1 | f2 | f3
def test_ti_0_03():
    f1 = PermBm.READ  | PermBm.WRITE
    f2 = PermBm.READ  | PermBm.EXECUTE
    f3 = PermBm.WRITE | PermBm.EXECUTE
    return f1 | f2 | f3
def test_ti_1_01():
    f1 = PermFl.READ  | PermFl.WRITE
    f2 = PermFl.READ  | PermFl.EXECUTE
    f3 = PermFl.WRITE | PermFl.EXECUTE
    return 123
def test_ti_1_02():
    f1 = PermCFl.READ  | PermCFl.WRITE
    f2 = PermCFl.READ  | PermCFl.EXECUTE
    f3 = PermCFl.WRITE | PermCFl.EXECUTE
    return 123
def test_ti_1_03():
    f1 = PermBm.READ  | PermBm.WRITE
    f2 = PermBm.READ  | PermBm.EXECUTE
    f3 = PermBm.WRITE | PermBm.EXECUTE
    return 123
def test_ti_2_03():
    f1 = PermEn.READ
    f2 = PermEn.READ
    f3 = PermEn.WRITE
    return f1 , f2 , f3
def test_ti_2_04():
    f1 = PermFl.READ
    f2 = PermFl.READ
    f3 = PermFl.WRITE
    return f1 , f2 , f3
def test_ti_2_05():
    f1 = PermCFl.READ
    f2 = PermCFl.READ
    f3 = PermCFl.WRITE
    return f1 , f2 , f3
def test_ti_2_06():
    f1 = PermBm.READ
    f2 = PermBm.READ
    f3 = PermBm.WRITE
    return f1 , f2 , f3


loop = 100000

a:dict = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
