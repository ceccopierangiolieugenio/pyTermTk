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

l3d = [[[random.randint(0,0xFFFFFFFF)]*100 for _ in range(100)] for _ in range(100)]
lll = [value for plane in l3d for line in plane for value in line]

def test_ti_1_00():
    return len([value for plane in l3d for line in plane for value in line])
# def test_ti_1_02():
#     return len(value for plane in l3d for line in plane for value in line)
def test_ti_1_03():
    return len(lll)

def test_ti_2_01():
    return min(value for plane in l3d for line in plane for value in line)
def test_ti_2_02():
    return min(lll)

def test_ti_3_01():
    v = l3d[0][0][0]
    for plane in l3d:
        for line in plane:
            for value in line:
                v = min(v,value)
    return v

def test_ti_3_02():
    for plane in l3d:
        for line in plane:
            for value in line:
                v = value
    return v

def test_ti_3_03():
    for val in (value for plane in l3d for line in plane for value in line):
                v = val
    return v
def test_ti_3_04():
    for val in [value for plane in l3d for line in plane for value in line]:
                v = val
    return v

def test_ti_4_01():
    global aaa
    aaa = 0
    def _proc(v):
        global aaa
        aaa += v
    [_proc(value) for plane in l3d for line in plane for value in line]
    return aaa

def test_ti_4_02():
    return sum(value for plane in l3d for line in plane for value in line)

def test_ti_4_03():
    global aaa
    aaa = 0
    def _proc(v):
        global aaa
        aaa += v
    for plane in l3d:
        for line in plane:
            for value in line:
                _proc(value)
    return aaa

loop = 50

a = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
