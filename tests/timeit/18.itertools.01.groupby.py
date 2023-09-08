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

# This test is bases on the example in:
#   https://www.geeksforgeeks.org/python-consecutive-characters-frequency/

import sys, os

import timeit

from itertools import groupby

sys.path.append(os.path.join(sys.path[0],'../..'))

testString1 = "EugenioXXXXXXXXXXXXXXXXXXParodiYYYYYYmalleoloZZZZsassso_______________122333444455555666666777777888888889999999990000000000"

def process1(txt):
    ret = ""
    for ch in txt:
        ret += ch
    return ret

def process2(txt):
    # return ''.join([ch*l if (l:=len(list(j)))>4 else f"[{l}b{ch}" for ch, j in groupby(txt)])
    return ''.join([ch*l if (l:=len(list(j)))<=4 else f"[{l}b{ch}" for ch, j in groupby(txt)])

def process3(txt):
    chBk = txt[0]
    count = 0
    ret = ""
    for ch in txt:
        if ch == chBk:
            count +=1
        else:
            if count>4:
                ret += f"[{count}b{chBk}"
            else:
                ret += chBk*count
            chBk = ch
            count = 1
    if count>4:
        ret += f"[{count}b{chBk}"
    else:
        ret += chBk*count
    return ret

def process4(txt):
    chBk = txt[0]
    count = 0
    ret = ""
    # genStr = (c for c in txt)
    genStr = iter(txt)
    ch = next(genStr)
    while ch:
        count = 1
        while ch == (_ch:=next(genStr,None)):
            count +=1
        if count>4:
            ret += f"[{count}b{ch}"
        else:
            ret += ch*count
        ch = _ch
    # if count>4:
    #     ret += f"[{count}b{ch}"
    # else:
    #     ret += ch*count
    return ret


def test1(): return process1(testString1)
def test2(): return process2(testString1)
def test3(): return process3(testString1)
def test4(): return process4(testString1)

loop = 100000

a={}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1

