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
import TermTk as ttk

w=0x1000
h=0x1000

c1 = [[0x1234]*w           for _ in range(h)]
c2 = [[0x4321,None]*(w//2) for _ in range(h//2)]+[[0x5678]*w for _ in range(h//2)]
c3 = [[0x5678]*((w)-1)+[None] for _ in range(h)]



def paintCanvasNew1():
    d1,d2 = [c.copy() for c in c1], [c.copy() for c in c2]
    a,b = 0x10,w-0x10
    for iy in range(0x10,h-0x10):
            d1[iy][a:b] = [x if x else y for x,y in zip(d2[iy][a:b],d1[iy][a:b])]

def paintCanvasNew2():
    d1,d2 = [c.copy() for c in c1], [c.copy() for c in c2]
    a,b = 0x10,w-0x10
    for iy in range(0x10,h-0x10):
        if None in d2[iy]:
            d1[iy][a:b] = [x if x else y for x,y in zip(d2[iy][a:b],d1[iy][a:b])]
        else:
            d1[iy][a:b] = d2[iy][a:b]

def paintCanvasNew3():
    d1,d2 = [c.copy() for c in c1], [c.copy() for c in c1]
    a,b = 0x10,w-0x10
    for iy in range(0x10,h-0x10):
        if None in d2[iy]:
            d1[iy][a:b] = [x if x else y for x,y in zip(d2[iy][a:b],d1[iy][a:b])]
        else:
            d1[iy][a:b] = d2[iy][a:b]

def paintCanvasNew4():
    d1,d2 = [c.copy() for c in c1], [c.copy() for c in c3]
    a,b = 0x10,w-0x10
    for iy in range(0x10,h-0x10):
        if None in d2[iy]:
            d1[iy][a:b] = [x if x else y for x,y in zip(d2[iy][a:b],d1[iy][a:b])]
        else:
            d1[iy][a:b] = d2[iy][a:b]

def paintCanvasOld():
    d1,d2 = [c.copy() for c in c1], [c.copy() for c in c2]
    a,b = 0x10,w-0x10
    for iy in range(0x10,h-0x10):
        d1[iy][a:b] = d2[iy][a:b]

def _re(s):
    paintCanvasOld()
def _old(s):
    paintCanvasNew1()

def test1(v): return paintCanvasOld()
def test2(v): return paintCanvasNew1()
def test3(v): return paintCanvasNew2()
def test4(v): return paintCanvasNew3()
def test5(v): return paintCanvasNew4()
def test6(v): return _old(v)
def test7(v): return _re(v)
def test8(v): return _old(v)

loop=10

a=1
result = timeit.timeit('test1(a)', globals=globals(), number=loop)
print(f"1a s {result / loop:.10f} - {result / loop} {test1(a)}")
result = timeit.timeit('test2(a)', globals=globals(), number=loop)
print(f"2a   {result / loop:.10f} - {result / loop} {test2(a)}")
result = timeit.timeit('test3(a)', globals=globals(), number=loop)
print(f"3b s {result / loop:.10f} - {result / loop} {test3(a)}")
result = timeit.timeit('test4(a)', globals=globals(), number=loop)
print(f"4b   {result / loop:.10f} - {result / loop} {test4(a)}")
result = timeit.timeit('test5(a)', globals=globals(), number=loop)
print(f"5c s {result / loop:.10f} - {result / loop} {test5(a)}")
result = timeit.timeit('test6(a)', globals=globals(), number=loop)
print(f"6c   {result / loop:.10f} - {result / loop} {test6(a)}")
result = timeit.timeit('test7(a)', globals=globals(), number=loop)
print(f"7d s {result / loop:.10f} - {result / loop} {test7(a)}")
result = timeit.timeit('test8(a)', globals=globals(), number=loop)
print(f"8d   {result / loop:.10f} - {result / loop} {test8(a)}")
