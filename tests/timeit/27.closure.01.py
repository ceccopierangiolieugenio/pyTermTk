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


def _processOut1(loop,a,b,c,d,e,f):
    ret = loop
    for x in range(a,b):
        for y in range(c,d):
            for z in range(e,f):
                ret += x+y+z
    return ret

_internals = {'a':1,'b':1,'c':1,'d':1,'e':1,'f':1}
def _processOut2(loop):
    a,b,c,d,e,f = _internals.values()
    ret = loop
    for x in range(a,b):
        for y in range(c,d):
            for z in range(e,f):
                ret += x+y+z
    return ret

def test1():
    a,b,c,d,e,f = 1,3,1,3,1,3
    ret = 0
    for loop in range(100):
        ret += loop
        for x in range(a,b):
            for y in range(c,d):
                for z in range(e,f):
                    ret += x+y+z
    return ret

def test2():
    def _processIn(loop,a,b,c,d,e,f):
        ret = loop
        for x in range(a,b):
            for y in range(c,d):
                for z in range(e,f):
                    ret += x+y+z
        return ret
    a,b,c,d,e,f = 1,3,1,3,1,3
    ret = 0
    for loop in range(100):
        ret += _processIn(loop,a,b,c,d,e,f)
    return ret

def test3():
    a,b,c,d,e,f = 1,3,1,3,1,3
    ret = 0
    for loop in range(100):
        ret += _processOut1(loop,a,b,c,d,e,f)
    return ret

def test4():
    def _processIn(loop):
        ret = loop
        for x in range(a,b):
            for y in range(c,d):
                for z in range(e,f):
                    ret += x+y+z
        return ret
    a,b,c,d,e,f = 1,3,1,3,1,3
    ret = 0
    for loop in range(100):
        ret += _processIn(loop)
    return ret

def test5():  return 1


loop = 10000

a = {}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1
