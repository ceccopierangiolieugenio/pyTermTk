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

import sys, os, re

import timeit
import random
import unicodedata

sys.path.append(os.path.join(sys.path[0],'../..'))
sys.path.append(os.path.join(sys.path[0],'.'))
import TermTk as ttk

stra = '\033Eugenio\033Parodi'
strb = 'print([m.start() for m in rm.finditer(stra)]),print([m.start() for m in rm.finditer(stra)]),print([m.start() for m in rm.finditer(stra)]),print([m.start() for m in rm.finditer(stra)]),Eugenio\033Parodi\033Parodi\033Parodi\033Parodi\033Parodiprint([m.start() for m in rm.finditer(stra)]),print([m.start() for m in rm.finditer(stra)]),print([m.start() for m in rm.finditer(stra)]),print([m.start() for m in rm.finditer(stra)]),Eugenio\033Parodi\033Parodi\033Parodi\033Parodi\033Parodiprint([m.start() for m in rm.finditer(stra)]),print([m.start() for m in rm.finditer(stra)]),print([m.start() for m in rm.finditer(stra)]),print([m.start() for m in rm.finditer(stra)]),Eugenio\033Parodi\033Parodi\033Parodi\033Parodi\033Parodi'
strc = 'Eugenio'
strd = '\033Eugenio'

rm = re.compile('(\033?[^\033]+)')

print(stra.split('\033'))
print(strb.split('\033'))
print(strc.split('\033'))

print(rm.match(stra))
print(rm.findall(stra))
print(rm.findall(strb))
print(rm.findall(strc))
print(rm.findall(strd))
print([m.start() for m in rm.finditer(stra)])
print([m.start() for m in rm.finditer(strb)])
print([m.start() for m in rm.finditer(strc)])


def _re(s):
    rm.findall(s)
def _old(s):
    ss = s.split('\033')
    rs=''
    for sss in ss[1:]:
        rs += '\033'+sss
    return len(rs)

def test1(v): return _re(v)
def test2(v): return _old(v)
def test3(v): return _re(v)
def test4(v): return _old(v)
def test5(v): return _re(v)
def test6(v): return _old(v)
def test7(v): return _re(v)
def test8(v): return _old(v)

loop = 20000


a=stra
result = timeit.timeit('test1(a)', globals=globals(), number=loop)
print(f"1a s {result / loop:.10f} - {result / loop} {test1(a)}")
result = timeit.timeit('test2(a)', globals=globals(), number=loop)
print(f"2a   {result / loop:.10f} - {result / loop} {test2(a)}")
a=strb
result = timeit.timeit('test3(a)', globals=globals(), number=loop)
print(f"3b s {result / loop:.10f} - {result / loop} {test3(a)}")
result = timeit.timeit('test4(a)', globals=globals(), number=loop)
print(f"4b   {result / loop:.10f} - {result / loop} {test4(a)}")
a=strc
result = timeit.timeit('test5(a)', globals=globals(), number=loop)
print(f"5c s {result / loop:.10f} - {result / loop} {test5(a)}")
result = timeit.timeit('test6(a)', globals=globals(), number=loop)
print(f"6c   {result / loop:.10f} - {result / loop} {test6(a)}")
a=strd
result = timeit.timeit('test7(a)', globals=globals(), number=loop)
print(f"7d s {result / loop:.10f} - {result / loop} {test7(a)}")
result = timeit.timeit('test8(a)', globals=globals(), number=loop)
print(f"8d   {result / loop:.10f} - {result / loop} {test8(a)}")
