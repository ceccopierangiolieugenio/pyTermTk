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
import re

sys.path.append(os.path.join(sys.path[0],'../..'))

# Testing a string contain different kind of matches
# Uppercase the matching pattern
# With the one mimic the VT100 escape codes "A...x"
testString1 = (
    "123456Aabcdef01" + "A[123A"  +
    "123456Babcdef02" + "A[123B"  +
    "123456Babcdef03" + "A[12C"   +
    "123456Babcdef04" + "A[1D"    +
    "123456Babcdef05" + "A[?123l" +
    "123456Babcdef06" + "A[?123h" +
    "123456Babcdef07" + "A[?4l"   +
    "123456Babcdef08" + "A[?5h"   +
    "123456Babcdef09" + "A[1E"    +
    "123456Cabcdef10" + "A[1;3H"  +
    "123456Cabcdef11" + "A[;f"    +
    "123456Dabcdef12" + "A[123F"  +
    "123456Eabcdef13" + "A[12;34f" )

testString2 = (
    "123456Aabcdef01" + "A[123A"  +
    "123456Cabcdef10" + "A[1;3H"  +
    "123456Eabcdef13" )

testString3 = (
    "123456Aabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef01" + "A[123A"  +
    "123456Eabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef13" )


re_P1_1 = re.compile(r'^(\d*);(\d*)([Hf])')
re_P1_2 = re.compile(r'^\?(\d+)([lh])')
re_P1_3 = re.compile(r'^(\d+)([ABCDEFGIJKLMPSTXZ])')

def process1_1(txt):
    _lines = []
    _cursor = (1,1)
    lines = txt.split('A')
    for i,l in enumerate(lines):
        if i:
            _lines.append("")
            _cursor = (0,len(_lines)-1)
        ls = l.split('B')
        for ii,ll in enumerate(ls):
            if ii:
                _cursor = (0,len(_lines)-1)
            lls = ll.split('C')
            for iii,lll in enumerate(lls):
                if iii:
                    x,y = _cursor
                    _cursor = (max(0,x-1),y)
                _lines.append(lll)
    return len(lines) +_cursor[0] + _cursor[1]

def process1(txt):
    r = 0
    tmp = []
    sout = txt.split('A[')
    r += process1_1(sout[0])
    for slice in sout[1:]:
        if m := re_P1_2.match(slice):
            l = len(m.group(0))
            ps = int(m.group(1))
            sr = m.group(2)
            tmp.append((ps,sr))
            slice = slice[l:]
        elif m := re_P1_1.match(slice):
            l = len(m.group(0))
            y = m.group(1)
            x = m.group(2)
            tp = m.group(3)
            tmp.append((y,x,tp))
            slice = slice[l:]
        elif m := re_P1_3.match(slice):
            l = len(m.group(0))
            ps = int(m.group(1))
            sr = m.group(2)
            tmp.append((ps,sr))
            slice = slice[l:]
        else:
            slice = '\033[' + slice.replace('\r','')
        r += process1_1(slice)
    return r + len(tmp)

re_P2_1 = re.compile(r'A\[(\d*);(\d*)([Hf])')
re_P2_2 = re.compile(r'A\[\?(\d+)([lh])')
re_P2_3 = re.compile(r'A\[(\d+)([ABCDEFGIJKLMPSTXZ])')
re_P2_4 = re.compile(r'[ABCD]')

def process2_2(txt):
    ret=0
    pos = 0
    prev = 0
    lll = len(txt)
    x,y = 0,0
    xxx = {
        "A":lambda :(x+1,y),
        "B":lambda :(x-1,y),
        "C":lambda :(x,y+1),
        "D":lambda :(x,y-1),
        }
    while pos < lll:
        if m := re_P2_4.search(txt,pos):
            gr = m.group()
            ln = 1
            st = m.start()
            en = pos = st+1
            _x = xxx.get(gr,lambda :(x,y))
            x,y = _x()
            ret += x+y
            ret += len(txt[prev:st])
            prev = en
        else:
            ret += len(txt[prev:])
            break
    return ret

def process2_1(txt):
    ret=0
    pos = 0
    prev = 0
    lll = len(txt)
    while pos < lll:
        if m := re_P2_1.search(txt,pos):
            gr = m.group()
            ln = len(gr)
            st = m.start()
            en = pos = m.end()
            y  = int(vv) if (vv:=m.group(1)) else 0
            x  = int(vv) if (vv:=m.group(2)) else 0
            ty = m.group(3)
            ret += x+y
            ret += process2_2(txt[prev:st])
            prev = en
        elif m := re_P2_3.search(txt,pos):
            gr = m.group()
            ln = len(gr)
            st = m.start()
            ps = int(m.group(1))
            sr = m.group(2)
            en = pos = m.end()
            ret += ps
            ret += process2_2(txt[prev:st])
            prev = en
        else:
            ret += process2_2(txt[prev:])
            break
    return ret

def process2(txt):
    ret=0
    pos = 0
    prev = 0
    lll = len(txt)
    xxx = {
       "A[123l":lambda x:len(x)+1,
       "A[123l":lambda x:len(x)+2,
       }
    while pos < lll:
        if m := re_P2_2.search(txt,pos):
            gr = m.group()
            ln = len(gr)
            st = m.start()
            en = pos = m.end()
            _x = xxx.get(gr,lambda x:len(x)+3)
            ret += _x(txt[st:en])
            ret += process2_1(txt[prev:st])
            prev = en
        else:
            ret += process2_1(txt[prev:])
            break
    return ret


def test1(): return process1(testString1)
def test2(): return process1(testString2)
def test3(): return process1(testString3)
def test4(): return process2(testString1)
def test5(): return process2(testString2)
def test6(): return process2(testString3)
def test7(): return 7
def test8(): return 8
def test9(): return 9

loop = 10000

a={}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1

