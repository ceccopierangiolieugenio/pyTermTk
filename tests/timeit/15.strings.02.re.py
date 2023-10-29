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
testString1 = "A[12;3H" + "abc"
testString2 = "A[123A"  + "abc"
testString3 = "A[;f"    + "abc"

# xterm escape sequences from:
# https://invisible-island.net/xterm/ctlseqs/ctlseqs.html
# https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-Functions-using-CSI-_-ordered-by-the-final-character_s_
re_CURSOR      = re.compile('^A\[(\d*);?(\d*)([ABCDEFGIJKLMPSTXZHf@])')
# https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-Functions-using-CSI-_-ordered-by-the-final-character_s_
# Basic Re for CSI Ps matches:
#   CSI : Control Sequence Introducer "<ESC>[" = '\033['
#   Ps  : A single (usually optional) numeric parameter, composed of one or more digits.
#   fu  : the single char defining the function
re_CSI_Ps_fu    = re.compile('^A\[(\d*)([ABCDEFGIJKLMPSTXZ@])')
re_CSI_Ps_Ps_fu = re.compile('^A\[(\d*);(\d*)([Hf])')

re_CSI_Mix    = re.compile('^A\[(\d*)([ABCDEFGIJKLMPSTXZ@])|A\[(\d*);(\d*)([Hf])')


re_DEC_SET_RST  = re.compile('A\[\?(\d+)([lh])')
# re_CURSOR_1    = re.compile(r'^(\d+)([ABCDEFGIJKLMPSTXZHf])')

def process1(txt):
    if m:=re_CURSOR.match(txt):
        return 1
    return 3

def process2(txt):
    if m:=re_CSI_Ps_fu.match(txt):
        return 1
    elif m:=re_CSI_Ps_Ps_fu.match(txt):
        return 2
    return 3

def process3(txt):
    if m:=re_CSI_Mix.match(txt):
        return 1
    return 3

def test1(): return process1(testString1)
def test2(): return process1(testString2)
def test3(): return process1(testString3)
def test4(): return process2(testString1)
def test5(): return process2(testString2)
def test6(): return process2(testString3)
def test7(): return process3(testString1)
def test8(): return process3(testString2)
def test9(): return process3(testString3)

loop = 100000

a={}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1

