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

a1 = (x for x in range(1000))
a2 = [x for x in range(1000)]

def test1(): return sum(a1)
def test2(): return sum(a2)
def test3():
    r = 0
    for i in a1:
        r+=i
    return r

def test4():
    r = 0
    for i in a2:
        r+=i
    return r

def test5(): return sum([x for x in range(300)])
def test6(): return sum((x for x in range(300)))
def test7(): return sum(x for x in range(300))

def test8():  return ".".join([f"{x:x}" for x in range(30)])
def test9():  return ".".join((f"{x:x}" for x in range(30)))
def test10(): return ".".join( f"{x:x}" for x in range(30) )

loop = 100000

a={}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    print(f"test{iii:02}) sec. {result / loop:.10f} - fps {loop / result : 15.3f} - {globals()[testName](*a)}")
    iii+=1