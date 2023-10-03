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

import gc, weakref

class Foo(object):
    __slots__ = ('a','b')
    def __init__(self, a=1234) -> None:
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

v1 = {'b':2345}

print(f"\nStart {gc.isenabled()=}")
# print(f"{gc.set_debug(gc.DEBUG_LEAK)=}")

print("\n############# Phase 1 ##################")
foo = Foo(v1)
print(f"{gc.get_referents(foo)=}")
print(f"{gc.get_count()=}")
print(f"{foo.a=} - {foo.b=} - {foo.f()=}")
del foo
print(f"{gc.collect()=}")

print("\n############# Phase 2 ##################")
foo = Foo(v1)
bar = foo.a
print(f"{gc.get_referents(foo)=}")
print(f"{gc.get_count()=}")
print(f"{foo.a=} - {foo.b=} - {foo.f()=} - {bar=}")
del foo
print(f"{gc.collect()=}")
print(f"{bar=}")

print("\n############# Phase 3 ##################")
foo = Foo(v1)
bar = foo.b
print(f"{gc.get_referents(foo)=}")
print(f"{gc.get_count()=}")
print(f"{foo.a=} - {foo.b=} - {foo.f()=} - {bar()=}")
del foo
print(f"{gc.collect()=}")
print(f"{bar()=}")

print("\n############# Phase 4 ##################")
foo = Foo(v1)
bar = foo.b
print(f"{gc.get_referents(foo)=}")
print(f"{gc.get_referents(v1)=}")
print(f"{gc.get_count()=}")
print(f"{foo.a=} - {foo.b=} - {foo.f()=} - {bar()=}")
del foo
pobjs()
print(f"{gc.collect()=}")
print(f"{bar()=}")
del bar
pobjs()
print(f"{gc.collect()=}")
pobjs()

print("\n############# Phase 5 ##################")
foo = Foo(v1)
bar = weakref.ref(foo.b)
xx = foo.f
baz = weakref.ref(xx)
print(f"{gc.get_referents(foo)=}")
print(f"{gc.get_referents(v1)=}")
print(f"{gc.get_count()=}")
print(f"{foo.a=} - {foo.b=} - {foo.f()=} - {bar()()=}")
del foo
pobjs()
print(f"{gc.collect()=}")
print(f"{bar()() if bar() else None=}")
del bar
pobjs()
print(f"{gc.collect()=}")
pobjs()

print(f"{gc.garbage=}")
print(f"End {gc.get_count()=}")
