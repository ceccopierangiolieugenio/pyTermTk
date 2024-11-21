#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

class A():
    def __init__(self,a,b) -> None:
        self.a = a
        self.b = b

    def __eq__(self, value: object) -> bool:
        print(f"A.eq - {self=},{value=}")
        return self.a==value.a and self.b==value.b

class B():
    def __init__(self,a,b) -> None:
        self.a = a
        self.b = b

    def __eq__(self, value: object) -> bool:
        print(f"B.eq - {self=},{value=}")
        return self.a==value.a and self.b==value.b

class C(A):
    def __eq__(self, value: object) -> bool:
        print(f"C(A).eq - {self=},{value=}")
        return self.a==value.a and self.b==value.b

class D():
    def __init__(self,a,b) -> None:
        self.a = a
        self.b = b

a = A(1,2)
aa = a
b = B(1,2)
bb = b
c = C(1,2)
cc = c
d = D(1,2)


print(f"{(a==aa)=}")
print(f"{(aa==a)=}")
print(f"{(a==c )=}")
print(f"{(c==a )=}")
print(f"{(a==b )=}")
print(f"{(b==a )=}")
print(f"{(b==c )=}")
print(f"{(c==b )=}")
print(f"{(c==d )=}")
print(f"{(d==c )=}")