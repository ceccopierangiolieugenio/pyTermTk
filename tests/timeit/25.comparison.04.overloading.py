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

class A():
    def __init__(self,a,b) -> None:
        self.a = a
        self.b = b

    def __eq__(self, value: object) -> bool:
        # print(f"A.eq - {self=},{value=}")
        return self.a==value.a and self.b==value.b

class B():
    def __init__(self,a,b) -> None:
        self.a = a
        self.b = b

    def __eq__(self, value: object) -> bool:
        # print(f"B.eq - {self=},{value=}")
        return self.a==value.a and self.b==value.b

class C(A):
    def __eq__(self, value: object) -> bool:
        # print(f"C(A).eq - {self=},{value=}")
        return self.a==value.a and self.b==value.b


a = A(1,2)
aa = a
b = B(1,2)
bb = b
c = C(1,2)
cc = c

print(f"{(a==aa)=}")
print(f"{(aa==a)=}")
print(f"{(a==c )=}")
print(f"{(c==a )=}")
print(f"{(a==b )=}")
print(f"{(b==a )=}")
print(f"{(b==c )=}")
print(f"{(c==b )=}")

def test_ti_00_x000(a,aa,b,c):  return len([a==aa for _ in range(1000)])
def test_ti_00_x001(a,aa,b,c):  return len([a==aa for _ in range(1000)])
def test_ti_00_x002(a,aa,b,c):  return len([a==aa for _ in range(1000)])
def test_ti_00_x003(a,aa,b,c):  return len([a==aa for _ in range(1000)])
def test_ti_00_x004(a,aa,b,c):  return len([a==aa for _ in range(100)])
def test_ti_01_A_AA(a,aa,b,c):  return len([a==aa for _ in range(1000)])
def test_ti_01_AA_A(a,aa,b,c):  return len([aa==a for _ in range(1000)])
def test_ti_02_A_B_(a,aa,b,c):  return len([a==b  for _ in range(1000)])
def test_ti_02_B_A_(a,aa,b,c):  return len([b==a  for _ in range(1000)])
def test_ti_03_A_C_(a,aa,b,c):  return len([a==c  for _ in range(1000)])
def test_ti_03_C_A_(a,aa,b,c):  return len([c==a  for _ in range(1000)])
def test_ti_04_B_C_(a,aa,b,c):  return len([b==c  for _ in range(1000)])
def test_ti_04_C_B_(a,aa,b,c):  return len([c==b  for _ in range(1000)])

loop = 1000

a = {'a':a,'aa':aa,'b':b,'c':c}

for testName in sorted([tn for tn in globals() if tn.startswith('test_ti_')]):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"{testName} | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
