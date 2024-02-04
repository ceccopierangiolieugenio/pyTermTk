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

import timeit, pickle

class ObjA():
    __slots__ = ('a','b','c','d')
    def __init__(self,a,b,c,d) -> None:
        self.a=a
        self.b=b
        self.c=c
        self.d=d

class ObjA1(ObjA):
    def __eq__(self, other):
        if other is None: return False
        return (
            self.a == other.a and
            self.b == other.b and
            self.c == other.c and
            self.d == other.d )

class ObjA2(ObjA):
    def __eq__(self, other):
        if other is None: return False
        return (
            (self.a, self.b, self.c, self.d ) ==
            (other.a,other.b,other.c,other.d) )

class ObjA3(ObjA):
    __slots__ = ('rec')
    def __init__(self, a, b, c, d) -> None:
        super().__init__(a, b, c, d)
        self.rec = (self.a, self.b, self.c, self.d )
    def __eq__(self, other):
        if other is None: return False
        return self.rec == other.rec

oa1_1 = ObjA1(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')
oa1_2 = ObjA1(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')
oa1_3 = ObjA1(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')
oa1_4 = ObjA1(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')
oa2_1 = ObjA2(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')
oa2_2 = ObjA2(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')
oa2_3 = ObjA2(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')
oa2_4 = ObjA2(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')
oa3_1 = ObjA3(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')
oa3_2 = ObjA3(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')
oa3_3 = ObjA3(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')
oa3_4 = ObjA3(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'123456789123456789123456789123456789')

oa1_1d = ObjA1(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567891')
oa1_2d = ObjA1(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567892')
oa1_3d = ObjA1(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567893')
oa1_4d = ObjA1(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567894')
oa2_1d = ObjA2(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567895')
oa2_2d = ObjA2(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567896')
oa2_3d = ObjA2(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567897')
oa2_4d = ObjA2(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567898')
oa3_1d = ObjA3(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567895')
oa3_2d = ObjA3(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567896')
oa3_3d = ObjA3(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567897')
oa3_4d = ObjA3(1,'asd123456789abcdefghijklmnopqrstuvwxyz',3.123456,'1234567891234567891234567891234567898')

print(f"{len(pickle.dumps(oa1_1))=}")
print(f"{len(pickle.dumps(oa2_1))=}")
print(f"{len(pickle.dumps(oa3_1))=}")
print(f"diff: {len(pickle.dumps(oa3_1))-len(pickle.dumps(oa1_1))}")

def test1():  return oa1_1==oa1_1==oa1_1==oa1_1
def test2():  return oa1_1==oa1_2==oa1_3==oa1_4
def test3():  return oa2_1==oa2_1==oa2_1==oa2_1
def test4():  return oa2_1==oa2_2==oa2_3==oa2_4
def test5():  return oa3_1==oa3_1==oa3_1==oa3_1
def test6():  return oa3_1==oa3_2==oa3_3==oa3_4

def test7():  return oa1_1==oa1_1==oa1_1==oa1_1d
def test8():  return oa1_1==oa1_2==oa1_3==oa1_4d
def test9():  return oa2_1==oa2_1==oa2_1==oa2_1d
def test10(): return oa2_1==oa2_2==oa2_3==oa2_4d
def test11(): return oa3_1==oa3_1==oa3_1==oa3_1d
def test12(): return oa3_1==oa3_2==oa3_3==oa3_4d

def test13(): return oa1_1d==oa1_1==oa1_1==oa1_1
def test14(): return oa1_1d==oa1_2==oa1_3==oa1_4
def test15(): return oa2_1d==oa2_1==oa2_1==oa2_1
def test16(): return oa2_1d==oa2_2==oa2_3==oa2_4
def test17(): return oa3_1d==oa3_1==oa3_1==oa3_1
def test18(): return oa3_1d==oa3_2==oa3_3==oa3_4


loop = 300000

a = {}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1
