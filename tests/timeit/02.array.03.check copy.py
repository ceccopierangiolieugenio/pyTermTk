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

def test1():  return all(all(r) for r in array1)
def test2():  return all(all(r) for r in array2)
def test3():  return all(all(r) for r in array3)
def test4():  return all(all(r) for r in array4)
def test5():  return all(all(r) for r in array5)
def test6():  return all(all(r) for r in array6)

def test7():  return any(any(r) for r in array1)
def test8():  return any(any(r) for r in array2)
def test9():  return any(any(r) for r in array3)
def test10(): return any(any(r) for r in array4)
def test11(): return any(any(r) for r in array5)
def test12(): return any(any(r) for r in array6)

loop = 100

a = {}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1
