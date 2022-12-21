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

class A():
    __slots__ = ('_value')
    def __init__(self):
        self._value = 123
    @property
    def value(self):return self._value
    @value.setter
    def value(self, value): self._value = value

class B():
    __slots__ = ('_value')
    def __init__(self):
        self._value = 123

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = value

a = A()
b = B()

def test1(x):
    ret = 0
    for v in range(10,100):
        a.value = v
        ret += a.value
    return ret

def test2(x):
    ret = 0
    for v in range(10,100):
        b.setValue(v)
        ret += b.value()
    return ret

def test3(x):
    ret = 0
    for v in range(10,100):
        a.value = v
    return ret

def test4(x):
    ret = 0
    for v in range(10,100):
        b.setValue(v)
    return ret

def test5(x):
    ret = 0
    for v in range(10,100):
        ret += a.value
    return ret

def test6(x):
    ret = 0
    for v in range(10,100):
        ret += b.value()
    return ret


loop = 10000

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


