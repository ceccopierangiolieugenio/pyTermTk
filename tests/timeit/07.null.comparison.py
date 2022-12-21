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

import timeit

a = 0
b = 1
c = None

def test1(x):
    if x: return 0
    else: return 1
def test2(x):
    if not x: return 10
    else: return 11
def test3(x):
    if x is None: return 110
    else: return 111
def test4(x):
    if x is not None: return 1110
    else: return 1111




loop = 1000000

result = timeit.timeit('test1(a)', globals=globals(), number=loop)
print(f"1a  {result / loop:.10f} - {result / loop} {test1(a)}")
result = timeit.timeit('test2(a)', globals=globals(), number=loop)
print(f"2a  {result / loop:.10f} - {result / loop} {test2(a)}")
result = timeit.timeit('test3(a)', globals=globals(), number=loop)
print(f"3a  {result / loop:.10f} - {result / loop} {test3(a)}")
result = timeit.timeit('test4(a)', globals=globals(), number=loop)
print(f"4a  {result / loop:.10f} - {result / loop} {test4(a)}")

result = timeit.timeit('test1(b)', globals=globals(), number=loop)
print(f"1b  {result / loop:.10f} - {result / loop} {test1(b)}")
result = timeit.timeit('test2(b)', globals=globals(), number=loop)
print(f"2b  {result / loop:.10f} - {result / loop} {test2(b)}")
result = timeit.timeit('test3(b)', globals=globals(), number=loop)
print(f"3b  {result / loop:.10f} - {result / loop} {test3(b)}")
result = timeit.timeit('test4(b)', globals=globals(), number=loop)
print(f"4b  {result / loop:.10f} - {result / loop} {test4(b)}")

result = timeit.timeit('test1(c)', globals=globals(), number=loop)
print(f"1c  {result / loop:.10f} - {result / loop} {test1(c)}")
result = timeit.timeit('test2(c)', globals=globals(), number=loop)
print(f"2c  {result / loop:.10f} - {result / loop} {test2(c)}")
result = timeit.timeit('test3(c)', globals=globals(), number=loop)
print(f"3c  {result / loop:.10f} - {result / loop} {test3(c)}")
result = timeit.timeit('test4(c)', globals=globals(), number=loop)
print(f"4c  {result / loop:.10f} - {result / loop} {test4(c)}")

