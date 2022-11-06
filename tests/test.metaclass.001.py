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

class A_Meta(type):
    def __new__(mcs, name, bases, d):
        print(f"{mcs=}")
        print(f"{name=}")
        print(f"{bases=}")
        print(f"{d=}")
        return type.__new__(mcs, name, bases, d)

class A(metaclass=A_Meta):
    def __init__(self, *args, **kwargs):
        pass
    def test(self):
        pass

print(f"{A=}")

a = A(1,2,3,4)

print(f"{a=}\n")

class B(A_Meta):
    def __init__(self, *args, **kwargs):
        pass
    def test(self):
        pass

b = B("NB",(),{})

print(f"{b=}\n")

class C():
    def __init__(self) -> None:
        print(f"C {type(self)=}")
class D():
    def __init__(self) -> None:
        print(f"D {type(self)=}")
class E(C,D):
    def __init__(self) -> None:
        print(f"{super()=}")
        super().__init__()
    def pippo(self):
        print(f"{super()=}")

e = E()
e.pippo()

print(f"{issubclass(E,D)=} {issubclass(E,C)=}")