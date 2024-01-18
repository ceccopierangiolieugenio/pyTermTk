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
import os,sys

sys.path.append(os.path.join(sys.path[0],'../..'))
sys.path.append(os.path.join(sys.path[0],'.'))
import TermTk as ttk

ttk.TTkLog.use_default_stdout_logging()

class testClass():
    pass

def pobjs():
    for i,o in enumerate(gc.get_objects()[-100:]):
        ss = str(o)
        if "Foo" in ss:
            print(f" * {i} - {ss}")

def _ref(o,ch="*"):
    # print(f"\n### -> Referents - {o}")
    # for i,r in enumerate(gc.get_referents(o)):
    #     print(f" - {i} ) {r}")
    print(f"\n### -> Referrers - {o}")
    for i,r in enumerate(gc.get_referrers(o)):
        print(f" {ch} {i} ) ({type(r)})-> {r}")
    print("")

v1 = {'b':2345}

print(f"\nStart {gc.isenabled()=}")
# print(f"{gc.set_debug(gc.DEBUG_LEAK)=}")

def _gccb(phase,info):
    print(f" ---> {gc.garbage=}")
    print(f" ---> {phase=} {info=}")

# gc.callbacks.append(_gccb)

print("\n############# Phase 1 ##################")
foo = ttk.TTkAbout()
bar1 = ttk.TTkButton()
bar2 = ttk.TTkWidget()
pep = testClass()

ttk.TTkHelper._updateWidget.clear()
ttk.TTkHelper._updateBuffer.clear()

print(f"{gc.collect()=}")
print(f"Mid {gc.get_count()=}")

_ref(foo)
_ref(foo)
_ref(foo, "-Active-")

foo.close()
ttk.TTkHelper._updateWidget.clear()
ttk.TTkHelper._updateBuffer.clear()

_ref(foo, "-Closed-")
del foo
# _ref(bar1)
# _ref(pep)

print(f"{gc.collect()=}")
print(f"End {gc.get_count()=}")
# time.sleep(3)

