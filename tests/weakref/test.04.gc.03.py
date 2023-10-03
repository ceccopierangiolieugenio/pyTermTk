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

# Example inspired by
# https://stackoverflow.com/questions/39838793/python-object-is-being-referenced-by-an-object-i-cannot-find

import gc, weakref, time

class Bar():
    __slots__ = ('_foo')
    def __init__(self, foo) -> None:
        self._foo = foo

class Foo():
    __slots__ = ('__weakref__','a','b','_bar')
    def __init__(self, a=1234) -> None:
        self._bar = Bar(self)
        self.a = a
        self.b = lambda : self.a

    def f(self):
        return self.a

    # def __del__(self):
    #     print(f"Deleted {self}")

def pobjs():
    for i,o in enumerate(gc.get_objects()[-100:]):
        ss = str(o)
        if "Foo" in ss:
            print(f" * {i} - {ss}")

def _ref(o):
    print(f"\n### -> Referents - {o}")
    for i,r in enumerate(gc.get_referents(o)):
        print(f" - {i} ) {r}")
    print(f"\n### -> Referrers - {o}")
    for i,r in enumerate(gc.get_referrers(o)):
        print(f" - {i} ) {r}")
    print("")

v1 = {'b':2345}

print(f"\nStart {gc.isenabled()=}")
# print(f"{gc.set_debug(gc.DEBUG_LEAK)=}")

def _gccb(phase,info):
    print(f" ---> {gc.garbage=}")
    print(f" ---> {phase=} {info=}")

# gc.callbacks.append(_gccb)

print("\n############# Phase 1 ##################")
foo = Foo(v1)
bar =foo.b

wrfoo = weakref.ref(foo)
wrbar = weakref.ref(bar)
wrf   = weakref.WeakMethod(foo.f)

# print(f"{gc.get_referents(foo)=}")
# print(f"{gc.get_referrers(foo)=}")
# print(f"{gc.get_referents(v1)=}")
# print(f"{gc.get_referrers(v1)=}")
# print(f"{gc.get_count()=}")
_ref(foo)

print(f"{foo.a=} - {foo.b=} - {foo.f()=} - {bar()=}")
print(f"{wrfoo()=} {wrbar()=} {wrf()=}")
del foo
print(f"{gc.collect()=}")
print(f"{bar()}")
# print(f"{gc.get_referents(v1)=}")
# print(f"{gc.get_referrers(v1)=}")
print(f"{wrfoo()=} {wrbar()=} {wrf()=}")
bar = None
print(f"{wrfoo()=} {wrbar()=} {wrf()=}")
time.sleep(4)
print(f"{wrfoo()=} {wrbar()=} {wrf()=}")
print(f"{gc.collect()=}")
print(f"{wrfoo()=} {wrbar()=} {wrf()=}")

print(f"{gc.garbage=}")
print(f"End {gc.get_count()=}")
