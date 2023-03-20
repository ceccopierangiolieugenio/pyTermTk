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
import unicodedata

sys.path.append(os.path.join(sys.path[0],'../..'))
sys.path.append(os.path.join(sys.path[0],'.'))
import TermTk as ttk


def f1(a):       return a
def f2(a,b):     return a+b
def f3(a,b,c):   return a+b+c
def f4(a,b,c,d): return a+b+c+d

def c1(*args,**argv): return f1(*args[:1])
def c2(*args,**argv): return f2(*args[:2])
def c3(*args,**argv): return f3(*args[:3])
def c4(*args,**argv): return f4(*args[:4])

def d1(*args,**argv): return f1(*args)
def d2(*args,**argv): return f2(*args)
def d3(*args,**argv): return f3(*args)
def d4(*args,**argv): return f4(*args)


def test1(v): return d1(1)
def test2(v): return d2(1,2)
def test3(v): return d3(1,2,3)
def test4(v): return d4(1,2,3,4)
def test5(v): return c1(1,2,3,4)
def test6(v): return c2(1,2,3,4)
def test7(v): return c3(1,2,3,4)
def test8(v): return c4(1,2,3,4)


loop = 200000


a=1
result = timeit.timeit('test1(a)', globals=globals(), number=loop)
print(f"1a s {result / loop:.10f} - {result / loop} {test1(a)}")
result = timeit.timeit('test2(a)', globals=globals(), number=loop)
print(f"2a   {result / loop:.10f} - {result / loop} {test2(a)}")
result = timeit.timeit('test3(a)', globals=globals(), number=loop)
print(f"3a s {result / loop:.10f} - {result / loop} {test3(a)}")
result = timeit.timeit('test4(a)', globals=globals(), number=loop)
print(f"4a   {result / loop:.10f} - {result / loop} {test4(a)}")
result = timeit.timeit('test5(a)', globals=globals(), number=loop)
print(f"5a s {result / loop:.10f} - {result / loop} {test5(a)}")
result = timeit.timeit('test6(a)', globals=globals(), number=loop)
print(f"6a   {result / loop:.10f} - {result / loop} {test6(a)}")
result = timeit.timeit('test7(a)', globals=globals(), number=loop)
print(f"7a s {result / loop:.10f} - {result / loop} {test7(a)}")
result = timeit.timeit('test8(a)', globals=globals(), number=loop)
print(f"8a   {result / loop:.10f} - {result / loop} {test8(a)}")
