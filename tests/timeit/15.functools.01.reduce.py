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
from functools import reduce

txt = "akjhakjhakjhakjhakjhakjahkjahkjahakjhalkhjalkahjlkahjadd"
txt += "1111111111111111111111111111111111111111111111111111111"
txt += "skljhdlhjdlkhjslkfhjdsljhfdlkjshfldkjshdflkjhfdsljhdslj"
txt += "skljhdlhjdlkhjslkfhjdsljhfdlkjshfldkjshdflkjhfdsljhdslj"
txt += "skljhdlhjdlkhjslkfhjdsljhfdlkjshfldkjshdflkjhfdsljhdslj"
txt += "skljhdlhjdlkhjslkfhjdsljhfdlkjshfldkjshdflkjhfdsljhdslj"

def test1(t=txt):
    ret = 0
    cbk = None
    for ch in t:
        if ch == cbk:
            ret += 1
        cbk = ch
    return ret

def _fr2(val, it):
    if val[1] == it:
        val[0] += 1
    val[1] = it
    return val

def test2(t=txt):
    return reduce(_fr2, t, [0,None])[0]

_fr3Ret = 0
def _fr3(val, it):
    global _fr3Ret
    if _fr3Ret == it:
        val += 1
    _fr3Ret = it
    return val

def test3(t=txt):
    global _fr3Ret
    _fr3Ret = None
    return reduce(_fr3, t, 0)

def test4(t=txt):
    val = [0,None]
    for ch in t:
        val = _fr2(val, ch)
    return val[0]

def test5(t=txt):
    global _fr3Ret
    _fr3Ret = None
    val = 0
    for ch in t:
        val = _fr3(val, ch)
    return val

def test6(t=txt):
    it = iter(t)
    ret = 0
    cbk = None
    for ch in it:
        if ch == cbk:
            ret += 1
        cbk = ch
    return ret

# def test7(): return 7
# def test8(): return 8
# def test9(): return 9

loop = 10000

a={}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1

