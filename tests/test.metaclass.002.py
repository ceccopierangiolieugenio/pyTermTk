#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
    test = True
    def __new__(cls, *args, **kwargs):
        print(f"New:  {args=} {kwargs=} {cls=}")
        if kwargs.get('mod'):
            return super().__new__(A_Mod)
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        print(f"Init: {args=} {kwargs=}")

class A_Mod(A):
    test = False
    def __init__(self, *args, **kwargs):
        print(f"Init: Mod {args=} {kwargs=}")

a = A(1,2,3,aa=1,bb=2,cc=3)
print(f"A ---> {a=} {a.test=}")
b = A(1,2,3,aa=1,bb=2,cc=3,mod=4)
print(f"B ---> {b=} {b.test=}")

def test(x):
    print(f"Test {x=}")
    return x == 5

print(f"{any(test(x) for x in range(10))=}")