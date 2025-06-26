#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

from dataclasses import dataclass
import timeit

@dataclass
class Data():
    a:int
    b:str

class A():
    p1 = Data(1,'a')
    p2 = Data(2,'b')
    p3 = Data(3,'c')
    p4 = Data(4,'d')
    p5 = Data(5,'e')

class B():
    p1:Data
    p2:Data
    p3:Data
    p4:Data
    p5:Data

B.p1 = Data(1,'a')
B.p2 = Data(2,'b')
B.p3 = Data(3,'c')
B.p4 = Data(4,'d')
B.p5 = Data(5,'e')

def test_ti_01():
    return len([A.p1.b, A.p1.a, A.p2.b, A.p2.a, A.p3.b, A.p3.a, A.p4.b, A.p4.a, A.p5.b, A.p5.a])
def test_ti_02():
    return len([B.p1.b, B.p1.a, B.p2.b, B.p2.a, B.p3.b, B.p3.a, B.p4.b, B.p4.a, B.p5.b, B.p5.a])
def test_ti_03():
    return len([A.p1.b, A.p1.a, A.p2.b, A.p2.a, A.p3.b, A.p3.a, A.p4.b, A.p4.a, A.p5.b, A.p5.a])
def test_ti_04():
    return len([B.p1.b, B.p1.a, B.p2.b, B.p2.a, B.p3.b, B.p3.a, B.p4.b, B.p4.a, B.p5.b, B.p5.a])
def test_ti_05():
    return len([A.p1.b, A.p1.a, A.p2.b, A.p2.a, A.p3.b, A.p3.a, A.p4.b, A.p4.a, A.p5.b, A.p5.a])
def test_ti_06():
    return len([B.p1.b, B.p1.a, B.p2.b, B.p2.a, B.p3.b, B.p3.a, B.p4.b, B.p4.a, B.p5.b, B.p5.a])

loop = 10000

a:dict = {}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
