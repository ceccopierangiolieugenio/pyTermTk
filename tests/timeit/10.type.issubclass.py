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

def test1(text): return 1 if type(c) is str else 0
def test2(text): return 1 if type(c) == str else 0
def test3(text): return 1 if issubclass(type(c), ttk.TTkString) else 0
def test4(text): return 1 if c==s else 0
def test5(text): return 1 if s==c else 0
def test6(text): return 1 if c=='Eugenio' else 0

loop = 20000


a="123"
result = timeit.timeit('test1(a)', globals=globals(), number=loop)
print(f"1a  {result / loop:.10f} - {result / loop} {test1(a)}")
result = timeit.timeit('test2(a)', globals=globals(), number=loop)
print(f"2a  {result / loop:.10f} - {result / loop} {test2(a)}")
result = timeit.timeit('test3(a)', globals=globals(), number=loop)
print(f"3a  {result / loop:.10f} - {result / loop} {test3(a)}")
result = timeit.timeit('test4(a)', globals=globals(), number=loop)
print(f"4a  {result / loop:.10f} - {result / loop} {test4(a)}")
result = timeit.timeit('test5(a)', globals=globals(), number=loop)
print(f"5a  {result / loop:.10f} - {result / loop} {test5(a)}")
result = timeit.timeit('test6(a)', globals=globals(), number=loop)
print(f"6a  {result / loop:.10f} - {result / loop} {test6(a)}")

a="456"
result = timeit.timeit('test1(a)', globals=globals(), number=loop)
print(f"1b  {result / loop:.10f} - {result / loop} {test1(a)}")
result = timeit.timeit('test2(a)', globals=globals(), number=loop)
print(f"2b  {result / loop:.10f} - {result / loop} {test2(a)}")
result = timeit.timeit('test3(a)', globals=globals(), number=loop)
print(f"3b  {result / loop:.10f} - {result / loop} {test3(a)}")
result = timeit.timeit('test4(a)', globals=globals(), number=loop)
print(f"4b  {result / loop:.10f} - {result / loop} {test4(a)}")
result = timeit.timeit('test5(a)', globals=globals(), number=loop)
print(f"5b  {result / loop:.10f} - {result / loop} {test5(a)}")
result = timeit.timeit('test6(a)', globals=globals(), number=loop)
print(f"6b  {result / loop:.10f} - {result / loop} {test6(a)}")