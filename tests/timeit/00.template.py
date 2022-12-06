#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os

import timeit
import random

sys.path.append(os.path.join(sys.path[0],'../..'))
sys.path.append(os.path.join(sys.path[0],'.'))
import TermTk as ttk


def test1():
    return 1
def test2():
    return 1
def test3():
    return 1
def test4():
    return 1
def test5():
    return 1
def test6():
    return 1
def test7():
    return 1
def test8():
    return 1
def test9():
    return 1
def test10():
    return 1
def test11():
    return 1
def test12():
    return 1

loop = 100

result = timeit.timeit('test1()', globals=globals(), number=loop)
print(f"1  {result / loop:.10f} - {result / loop} {test1()}")
result = timeit.timeit('test2()', globals=globals(), number=loop)
print(f"2  {result / loop:.10f} - {result / loop} {test2()}")
result = timeit.timeit('test3()', globals=globals(), number=loop)
print(f"3  {result / loop:.10f} - {result / loop} {test3()}")
result = timeit.timeit('test4()', globals=globals(), number=loop)
print(f"4  {result / loop:.10f} - {result / loop} {test4()}")
result = timeit.timeit('test5()', globals=globals(), number=loop)
print(f"5  {result / loop:.10f} - {result / loop} {test5()}")
result = timeit.timeit('test6()', globals=globals(), number=loop)
print(f"6  {result / loop:.10f} - {result / loop} {test6()}")
result = timeit.timeit('test7()', globals=globals(), number=loop)
print(f"7  {result / loop:.10f} - {result / loop} {test7()}")
result = timeit.timeit('test8()', globals=globals(), number=loop)
print(f"8  {result / loop:.10f} - {result / loop} {test8()}")
result = timeit.timeit('test9()', globals=globals(), number=loop)
print(f"9  {result / loop:.10f} - {result / loop} {test9()}")
result = timeit.timeit('test10()', globals=globals(), number=loop)
print(f"10 {result / loop:.10f} - {result / loop} {test10()}")
result = timeit.timeit('test11()', globals=globals(), number=loop)
print(f"11 {result / loop:.10f} - {result / loop} {test11()}")
result = timeit.timeit('test12()', globals=globals(), number=loop)
print(f"12 {result / loop:.10f} - {result / loop} {test12()}")



