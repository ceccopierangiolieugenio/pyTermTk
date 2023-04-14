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

import sys, os

import timeit
import random


sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

lll = [(ttk.TTkButton(), random.randint(0,10000)) for _ in range(100)]
lll += lll

def sort1():
    l = []
    for b in lll:
        if b not in l:
            l.append(b)
    return len(l)

def sort2():
    l = set()
    for b in lll:
        l.add(b)
    return len(l)

def sort3():
    l = []
    for b in lll:
        if b not in l:
            l.append(b)
    sl = sorted(l, key=lambda w: -w[1])
    return len(sl)

def sort4():
    l = set()
    for b in lll:
        l.add(b)
    sl = sorted(l, key=lambda w: -w[1])
    return len(sl)

def test1(): return sort1()
def test2(): return sort2()
def test3(): return sort3()
def test4(): return sort4()
def test5(): return sort1()
def test6(): return sort1()
def test7(): return sort1()
def test8(): return sort1()
def test9(): return sort1()

loop = 1000

a={}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    iii+=1