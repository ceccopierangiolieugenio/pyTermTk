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

import timeit

array1 = [[True            for _ in range(1000)] for _ in range(1000)]
array2 = [[False           for _ in range(1000)] for _ in range(1000)]
array3 = [[x==y==999       for x in range(1000)] for y in range(1000)]
array4 = [[not (x==y==999) for x in range(1000)] for y in range(1000)]
array5 = [[x==y==500       for x in range(1000)] for y in range(1000)]
array6 = [[not (x==y==500) for x in range(1000)] for y in range(1000)]

def test_ti_1_1():
    array1[500] = [True]*1000
    return True

def test_ti_1_2():
    array1[500][0:1000] = [True]*1000
    return True

def test_ti_2_1():
    for line in array1[400:600]:
        line[400:600] =   [True]*(600-400)
    return True

def test_ti_3_1():
    array1 = [[True]*1000 for _ in range(1000)]
    return True

def test_ti_4_1():
    array1 = [[True]*10000 for _ in range(10000)]
    return True

def test_ti_5_1():
    array1 = [[True]*100 for _ in range(100000)]
    return True

def test_ti_6_1():
    array1 = [[True]*11 for _ in range(2000000)]
    return True

loop = 10

a = {}
# while (testName := f'test{iii}') and (testName in globals()):
for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
