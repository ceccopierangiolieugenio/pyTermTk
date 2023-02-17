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

class A(ttk.TTkString):pass
class B(A):pass
class C(B):pass

c = C("Eugenio")
s = ttk.TTkString("Eugenio")

signalA = ttk.pyTTkSignal(int)
signalB = ttk.pyTTkSignal(int)
signalC = ttk.pyTTkSignal(int)
signalD = ttk.pyTTkSignal(int)

@ttk.pyTTkSlot(int)
def processA(a): return a
@ttk.pyTTkSlot(int)
def processB(b): return b
@ttk.pyTTkSlot(int)
def processC(c): return c
@ttk.pyTTkSlot(int)
def processD(d): return d

signalA.connect(processA)

signalB.connect(processA)
signalB.connect(processB)

signalC.connect(processA)
signalC.connect(processB)
signalC.connect(processC)

signalD.connect(processA)
signalD.connect(processB)
signalD.connect(processC)
signalD.connect(processD)


def test1(v):
    signalA.emit(a)
    return 1
def test2(v):
    return processA(v)

def test3(v):
    signalB.emit(a)
    return 1
def test4(v):
    return processA(v),processB(v)

def test5(v):
    signalC.emit(a)
    return 1
def test6(v):
    return processA(v),processB(v),processC(v)

def test7(v):
    signalD.emit(a)
    return 1
def test8(v):
    return processA(v),processB(v),processC(v),processD(v)

loop = 20000


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
