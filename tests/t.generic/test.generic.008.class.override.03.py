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

    def __str__(self):        return f"a={self.a} {type(self).__name__} {type(other).__name__}, b={self.b}"
    def __sub__(self, other): return f"A( ).  sub {type(self).__name__} {type(other).__name__}"
    def __or__( self, other): return f"A( ).  or  {type(self).__name__} {type(other).__name__}"
    def __ror__(self, other): return f"A( ).R-or  {type(self).__name__} {type(other).__name__}"

class B():
    def __init__(self,a,b) -> None:
        self.a = a
        self.b = b

    def __sub__(self, other): return f"B( ).  sub {type(self).__name__} {type(other).__name__}"

class C(A):
    def __sub__(self, other): return f"C(A).  sub {type(self).__name__} {type(other).__name__}"
    def __or__( self, other): return f"C(C).  or  {type(self).__name__} {type(other).__name__}"

class D(C):
    def __init__(self,a,b) -> None:
        self.a = a
        self.b = b
    def __sub__( self, other): return f"D(C).  sub {type(self).__name__} {type(other).__name__}"
    def __rsub__(self, other): return f"D(C).R-sub {type(self).__name__} {type(other).__name__}"
    def __or__(  self, other): return f"D(C).  or  {type(self).__name__} {type(other).__name__}"
    def __ror__( self, other): return f"D(C).R-or  {type(self).__name__} {type(other).__name__}"
a = A(1,2)
aa = a
b = B(1,2)
bb = b
c = C(1,2)
cc = c
d = D(1,2)


print(f"{(a-aa)=} | {(a|aa)=}")
print(f"{(aa-a)=} | {(aa|a)=}")
print(f"{(a-c )=} | {(a|c )=}")
print(f"{(c-a )=} | {(c|a )=}")
print(f"{(a-b )=} | {(a|b )=}")
print(f"{(b-a )=} | {(b|a )=}")
print(f"{(b-c )=} | {(b|c )=}")
print(f"{(c-b )=} | {(c|b )=}")
print(f"{(c-d )=} | {(c|d )=}")
print(f"{(d-c )=} | {(d|c )=}")
print(f"{(d-d )=} | {(d|d )=}")