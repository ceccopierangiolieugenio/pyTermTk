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

from typing import NamedTuple


class TTkPadding(NamedTuple):
    top    : int = 0
    bottom : int = 0
    left   : int = 0
    right  : int = 0

def test_ti_1_00():
    return len([[x,x,x,x] for x in range(1000)])

def test_ti_2_00():
    return len([(x,x,x,x) for x in range(1000)])

def test_ti_2_01():
    return len([(1,1,1,1) for x in range(1000)])

def test_ti_3_00():
    return len([TTkPadding(x,x,x,x) for x in range(1000)])


loop = 500

a = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
