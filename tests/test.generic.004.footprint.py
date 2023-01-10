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

import sys

class A():
    def a(self): print(f"{self=}")
class B(A): pass
class C(B): pass

class Aa():
    _euVars = {'aa':1, 'ab':2}

class Bb(Aa):
    _euVars = {'ba':1, 'bb':2}

class Cc(Bb):
    _euVars = {'ca':1, 'cb':2}

c = C()
cc = Cc()

print(cc)
print(cc.__class__.__name__)
print(Cc.__mro__)

print(f"{sys.getsizeof(c)=}")
print(f"{sys.getsizeof(cc)=}")

print(f"{sys.getsizeof(A)=}")
print(f"{sys.getsizeof(B)=}")
print(f"{sys.getsizeof(C)=}")

print(f"{sys.getsizeof(Aa)=}")
print(f"{sys.getsizeof(Bb)=}")
print(f"{sys.getsizeof(Cc)=}")


for co in reversed(type(cc).__mro__):
    if hasattr(co,'_euVars'):
        print(f"{co} -> {co.__name__} -> {co.__class__} -> {co.__class__.__name__} -> {co._euVars}")