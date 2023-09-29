#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os, weakref

import timeit
from threading import Lock

class Foo():
    def a(self,v):
        return v+v*v

f1 = Foo()
f21 = Foo()
f22 = Foo()

a1  = f1.a
a21 = weakref.WeakMethod(f21.a)
a22 = weakref.WeakMethod(f22.a)
a31 = weakref.ref(_a31:=f21.a)
a32 = weakref.ref(_a32:=f22.a)

del f22,_a32

def test1(v=a1,ff=f1):    return sum([  v(x)                     for x in range(100)])

def test2(v=a21,ff=f21):  return sum([v()(x) if      v()  else 0 for x in range(100)])
def test3(v=a22,ff=f21):  return sum([v()(x) if      v()  else 0 for x in range(100)])
def test4(v=a21,ff=f21):  return sum([ _v(x) if (_v:=v()) else 0 for x in range(100)])
def test5(v=a22,ff=f21):  return sum([ _v(x) if (_v:=v()) else 0 for x in range(100)])

def test6(v=a31,ff=f21):  return sum([v()(x) if      v()  else 0 for x in range(100)])
def test7(v=a32,ff=f21):  return sum([v()(x) if      v()  else 0 for x in range(100)])
def test8(v=a31,ff=f21):  return sum([ _v(x) if (_v:=v()) else 0 for x in range(100)])
def test9(v=a32,ff=f21):  return sum([ _v(x) if (_v:=v()) else 0 for x in range(100)])

loop = 10000

a = {}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1

