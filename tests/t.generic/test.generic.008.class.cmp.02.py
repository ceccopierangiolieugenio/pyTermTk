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

class A():
    def __init__(self,a:int,b:int) -> None:
        self.a = a
        self.b = b

    def __hash__(self) -> int:
        print('HASH:',self)
        return hash(self.a)

    def __str__(self) -> str:
        return f"{(self.a,self.b)}"

    def __eq__(self, value: object) -> bool:
        # print(f"{self=},{value=}")
        if not isinstance(value, A):
            return False
        return self.a==value.a and self.b==value.b


a = A(1,2)
b = a
c = A(1,2)
d = A(1,3)

print(f"{(a==b)=}")
print(f"{(a==c)=}")
print(f"{(a==d)=}")
print(f"{(a is b)=}")
print(f"{(a is c)=}")
print(f"{(a is d)=}")
print(a,hash(a),b,hash(b),c,hash(c),d,hash(d))

d = {a:1, b:2, c:3, d:4}
print(d)