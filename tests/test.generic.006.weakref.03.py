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

import weakref
import gc

class Obj():
    def __init__(self, v=None) -> None:
        self._v = v
        self._k = None
        if v: v.setK(self)

    def setK(self,k):
        self._k = k

    def __del__(self):
        print(f"Delete {self=} -> {self._v} {self._k}")

k1 = Obj()
k2 = Obj()
k3 = Obj()

k4 = Obj()
k5 = Obj(k4)

d = weakref.WeakKeyDictionary()

def ppp(n):
    print(f"Dump: {n=}")
    print(f"{gc.get_count()}, {gc.get_stats()}, {gc.garbage}")
    for i in d:
        print(f"<*> - {i=} {d[i]=}")

d[Obj(k1)] = "k1"
d[Obj(k2)] = "k2"
d[Obj(k3)] = "k3"

ppp(1)
del k2
k4 = k5 = None
gc.collect()
ppp(2)
k3 = None
gc.collect()
ppp(3)

print("------> Inizio della seconda parte")

k1 = Obj()
k2 = Obj()
k3 = Obj()
d[k1] = weakref.ref(Obj(k1))
d[k2] = weakref.ref(Obj(k2))
d[k3] = weakref.ref(Obj(k3))

print(f"{k1 in d=}")

ppp(4)
del k2
gc.collect()
ppp(5)
k3 = k1 = None
gc.collect()
ppp(6)