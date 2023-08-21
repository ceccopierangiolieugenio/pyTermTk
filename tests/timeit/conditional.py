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

sys.path.append(os.path.join(sys.path[0],'../..'))

testString1 = "1234567890ABCDEFGHI"

def process1(txt):
    ret = 0
    for ch in txt:
        if ord(ch)<=0x39:
            continue
        ret += ord(ch)
    return ret

def process2(txt):
    ret = 0
    for ch in [c for c in  txt if ord(c)>0x39]:
        ret += ord(ch)
    return ret

def process3(txt):
    ret = 0
    for ch in txt:
        ret += ord(ch)
    return ret

def test1(): return process1(testString1)
def test2(): return process1(testString1)
def test3(): return process1(testString1)
def test4(): return process2(testString1)
def test5(): return process2(testString1)
def test6(): return process2(testString1)
def test7(): return process3(testString1)
def test8(): return process3(testString1)
def test9(): return process3(testString1)

loop = 100000

a={}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1

