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
from TermTk import TTkTermColor

testInput = [0,1,2,3,4,5,6,7,8,9,10,20,21,22,23,24,25,26,27,28,29,30,31]

def test1(ttt=testInput):
    mod = 0
    for s in ttt:
        if s==1: mod |= TTkTermColor.BOLD
        elif s==2: mod += TTkTermColor.FAINT
        elif s==3: mod += TTkTermColor.ITALIC
        elif s==4: mod += TTkTermColor.UNDERLINE
        elif s==5: mod += TTkTermColor.BLINKING
        elif s==7: mod += TTkTermColor.REVERSED
        elif s==8: mod += TTkTermColor.HIDDEN
        elif s==9: mod += TTkTermColor.STRIKETROUGH
        elif s==22: mod += ~(TTkTermColor.BOLD|TTkTermColor.FAINT)
        elif s==23: mod += ~TTkTermColor.ITALIC
        elif s==24: mod += ~TTkTermColor.UNDERLINE
        elif s==25: mod += ~TTkTermColor.BLINKING
        elif s==27: mod += ~TTkTermColor.REVERSED
        elif s==28: mod += ~TTkTermColor.HIDDEN
        elif s==29: mod += ~TTkTermColor.STRIKETROUGH
    return mod

def test2(ttt=testInput):
    mod = 0
    for s in ttt:
        if mm := {
                    1: TTkTermColor.BOLD ,
                    2: TTkTermColor.FAINT ,
                    3: TTkTermColor.ITALIC ,
                    4: TTkTermColor.UNDERLINE ,
                    5: TTkTermColor.BLINKING ,
                    7: TTkTermColor.REVERSED ,
                    8: TTkTermColor.HIDDEN ,
                    9: TTkTermColor.STRIKETROUGH
                }.get(s,None):
            mod += mm
        elif mm := {
                    22: ~(TTkTermColor.BOLD|TTkTermColor.FAINT),
                    23: ~TTkTermColor.ITALIC,
                    24: ~TTkTermColor.UNDERLINE,
                    25: ~TTkTermColor.BLINKING,
                    27: ~TTkTermColor.REVERSED,
                    28: ~TTkTermColor.HIDDEN,
                    29: ~TTkTermColor.STRIKETROUGH,
                }.get(s,None):
            mod += mm
    return mod

t3_or = {
    1: TTkTermColor.BOLD ,
    2: TTkTermColor.FAINT ,
    3: TTkTermColor.ITALIC ,
    4: TTkTermColor.UNDERLINE ,
    5: TTkTermColor.BLINKING ,
    7: TTkTermColor.REVERSED ,
    8: TTkTermColor.HIDDEN ,
    9: TTkTermColor.STRIKETROUGH }
t3_and = {
    22: ~(TTkTermColor.BOLD|TTkTermColor.FAINT),
    23: ~TTkTermColor.ITALIC,
    24: ~TTkTermColor.UNDERLINE,
    25: ~TTkTermColor.BLINKING,
    27: ~TTkTermColor.REVERSED,
    28: ~TTkTermColor.HIDDEN,
    29: ~TTkTermColor.STRIKETROUGH }

def test3(ttt=testInput):
    mod = 0
    for s in ttt:
        if mm := t3_or.get(s,None):
            mod += mm
        elif mm := t3_and.get(s,None):
            mod += mm
    return mod

class t4():
    t4_or = {
        1: TTkTermColor.BOLD ,
        2: TTkTermColor.FAINT ,
        3: TTkTermColor.ITALIC ,
        4: TTkTermColor.UNDERLINE ,
        5: TTkTermColor.BLINKING ,
        7: TTkTermColor.REVERSED ,
        8: TTkTermColor.HIDDEN ,
        9: TTkTermColor.STRIKETROUGH }
    t4_and = {
        22: ~(TTkTermColor.BOLD|TTkTermColor.FAINT),
        23: ~TTkTermColor.ITALIC,
        24: ~TTkTermColor.UNDERLINE,
        25: ~TTkTermColor.BLINKING,
        27: ~TTkTermColor.REVERSED,
        28: ~TTkTermColor.HIDDEN,
        29: ~TTkTermColor.STRIKETROUGH }

def test4(ttt=testInput):
    mod = 0
    for s in ttt:
        if mm := t4.t4_or.get(s,None):
            mod += mm
        elif mm := t4.t4_and.get(s,None):
            mod += mm
    return mod

def test5(ttt=testInput):
    mod = 0
    t5_or  = t4.t4_or
    t5_and = t4.t4_and
    for s in ttt:
        if mm := t5_or.get(s,None):
            mod += mm
        elif mm := t5_and.get(s,None):
            mod += mm
    return mod

def test6(): return 1
def test7(): return 1
def test8(): return 1
def test9(): return 1

loop = 150000

a={}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1

