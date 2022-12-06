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

class A():
    def test(self):
        return 1

class B(A):
    def test(self):
        return 2

class C(B):
    def test(self):
        return 3

class D():
    __slots__ = ('test')
    def __init__(self, sw=True):
        if sw:
            self.test = self._testA
        else:
            self.test = self._testB
    def _testA(self):
        return 11
    def _testB(self):
        return 12

class E():
    __slots__ = ('_sw')
    def __init__(self, sw=True):
        self._sw = sw
    def test(self):
        if self._sw:
            return 21
        else:
            return 22

class F():
    __slots__ = ('_sw')
    def __init__(self, sw=True):
        self._sw = sw
    def test(self):
        if self._sw:
            return self._testA()
        else:
            return self._testB()
    def _testA(self):
        return 31
    def _testB(self):
        return 32

a  = A()
b  = B()
c  = C()
da = D(sw=True)
db = D(sw=False)
ea = E(sw=True)
eb = E(sw=False)
fa = F(sw=True)
fb = F(sw=False)

def test1():
    return a.test()
def test2():
    return b.test()
def test3():
    return c.test()
def test4():
    return da.test()
def test5():
    return db.test()
def test6():
    return ea.test()
def test7():
    return eb.test()
def test8():
    return fa.test()
def test9():
    return fb.test()

def test10(): return None
def test11(): return None
def test12(): return None

loop = 100000

result = timeit.timeit('test1()', globals=globals(), number=loop)
print(f"1a  {result / loop:.10f} - {result / loop} {test1()}")
result = timeit.timeit('test2()', globals=globals(), number=loop)
print(f"2b  {result / loop:.10f} - {result / loop} {test2()}")
result = timeit.timeit('test3()', globals=globals(), number=loop)
print(f"3c  {result / loop:.10f} - {result / loop} {test3()}")
result = timeit.timeit('test4()', globals=globals(), number=loop)
print(f"4da {result / loop:.10f} - {result / loop} {test4()}")
result = timeit.timeit('test5()', globals=globals(), number=loop)
print(f"5db {result / loop:.10f} - {result / loop} {test5()}")
result = timeit.timeit('test6()', globals=globals(), number=loop)
print(f"6ea {result / loop:.10f} - {result / loop} {test6()}")
result = timeit.timeit('test7()', globals=globals(), number=loop)
print(f"7eb {result / loop:.10f} - {result / loop} {test7()}")
result = timeit.timeit('test8()', globals=globals(), number=loop)
print(f"8fa {result / loop:.10f} - {result / loop} {test8()}")
result = timeit.timeit('test9()', globals=globals(), number=loop)
print(f"9fb {result / loop:.10f} - {result / loop} {test9()}")
result = timeit.timeit('test10()', globals=globals(), number=loop)
print(f"10 {result / loop:.10f} - {result / loop} {test10()}")
result = timeit.timeit('test11()', globals=globals(), number=loop)
print(f"11 {result / loop:.10f} - {result / loop} {test11()}")
result = timeit.timeit('test12()', globals=globals(), number=loop)
print(f"12 {result / loop:.10f} - {result / loop} {test12()}")



