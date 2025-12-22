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

# match statement requires Python 3.10+
if sys.version_info < (3, 10):
    print("This test requires Python 3.10 or higher (match statement not available)")
    sys.exit(0)

def test_ti_01_01_ma():
    ret = 0
    for i in range(1000):
        match i:
            case 0:
                ret += 1
            case 10:
                ret += 10
            case 100:
                ret += 100
    return ret

def test_ti_01_01_if():
    ret = 0
    for i in range(1000):
        if i == 0:
            ret += 1
        elif i == 10:
            ret += 10
        elif i == 100:
            ret += 100
    return ret

def test_ti_01_02_ma():
    ret = 0
    for i in range(1000):
        match i:
            case 0 | 5:
                ret += 1
            case 10 | 20 | 30:
                ret += 10
            case 100 | 200 | 500:
                ret += 100
    return ret

def test_ti_01_02_if():
    ret = 0
    for i in range(1000):
        if i in (0,5):
            ret += 1
        elif i in (10,20,30):
            ret += 10
        elif i in (100,200,500):
            ret += 100
    return ret

# Test with tuple destructuring - match should be faster
def test_ti_02_01_ma():
    ret = 0
    data = [(1, 2), (3, 4, 5), (6,), "string", (7, 8), None, (9, 10, 11)]
    for _ in range(1000):
        for item in data:
            match item:
                case (x, y):
                    ret += x + y
                case (x, y, z):
                    ret += x + y + z
                case (x,):
                    ret += x
                case str():
                    ret += 0
                case None:
                    ret += 0
    return ret

def test_ti_02_01_if():
    ret = 0
    data = [(1, 2), (3, 4, 5), (6,), "string", (7, 8), None, (9, 10, 11)]
    for _ in range(1000):
        for item in data:
            if isinstance(item, tuple):
                if len(item) == 2:
                    x, y = item
                    ret += x + y
                elif len(item) == 3:
                    x, y, z = item
                    ret += x + y + z
                elif len(item) == 1:
                    x = item[0]
                    ret += x
            elif isinstance(item, str):
                ret += 0
            elif item is None:
                ret += 0
    return ret

# Test with complex nested patterns - match should be faster
def test_ti_02_02_ma():
    ret = 0
    data = [
        ("add", 10, 20),
        ("mul", 5, 6),
        ("sub", 100, 50),
        ("div", 200, 4),
        ("unknown", 1, 2),
        ("add", 1, 1),
        ("mul", 3, 3),
    ]
    for _ in range(1000):
        for item in data:
            match item:
                case ("add", x, y):
                    ret += x + y
                case ("sub", x, y):
                    ret += x - y
                case ("mul", x, y):
                    ret += x * y
                case ("div", x, y):
                    ret += x // y
                case _:
                    ret += 0
    return ret

def test_ti_02_02_if():
    ret = 0
    data = [
        ("add", 10, 20),
        ("mul", 5, 6),
        ("sub", 100, 50),
        ("div", 200, 4),
        ("unknown", 1, 2),
        ("add", 1, 1),
        ("mul", 3, 3),
    ]
    for _ in range(1000):
        for item in data:
            if isinstance(item, tuple) and len(item) == 3:
                op, x, y = item
                if op == "add":
                    ret += x + y
                elif op == "sub":
                    ret += x - y
                elif op == "mul":
                    ret += x * y
                elif op == "div":
                    ret += x // y
                else:
                    ret += 0
            else:
                ret += 0
    return ret

loop = 1000

a:dict = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
