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
import random

sys.path.append(os.path.join(sys.path[0],'../..'))

l1 =[ random.randint(0x100,0x20000) for _ in range(10000) ]
l2 =[ random.randint(0x100,0x20000) for _ in range(10000) ] + ['b']

def _k1(x): return x
def _k2(x): return str(x)

def test_ti_1_01(): sorted(l1)
def test_ti_1_02(): sorted(l1, key=lambda x: x)
def test_ti_1_03(): sorted(l1, key=lambda x:str(x))
def test_ti_1_04(): sorted(l1, key=_k1)
def test_ti_1_05(): sorted(l1, key=_k2)

def test_ti_1_06():
    try:
        sorted(l1)
    except TypeError as _:
        sorted(l1, key=lambda x:str(x))

def test_ti_1_07():
    try:
        sorted(l1)
    except TypeError as _:
        sorted(l1, key=_k2)

def test_ti_2_01():  sorted(l2, key=lambda x:str(x))
def test_ti_2_02():  sorted(l2, key=_k2)

def test_ti_2_03():
    try:
        sorted(l2)
    except TypeError as _:
        sorted(l2, key=lambda x:str(x))

def test_ti_2_04():
    try:
        sorted(l2)
    except TypeError as _:
        sorted(l2, key=_k2)

loop = 300

a = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
