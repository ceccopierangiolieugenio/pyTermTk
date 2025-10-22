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

import sys, os
import gc, weakref, time

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
sys.path.append(os.path.join(sys.path[0],'.'))
import TermTk as ttk

def pobjs():
    for i,o in enumerate(gc.get_objects()[-100:]):
        ss = str(o)
        if "Foo" in ss:
            print(f" * {i} - {ss}")

print(f"\nStart {gc.isenabled()=}")

def _gccb(phase,info):
    print(f" ---> {gc.garbage=}")
    print(f" ---> {phase=} {info=}")
# gc.callbacks.append(_gccb)

def _ref(o):
    print(f"\n### -> Referents - {o}")
    for i,r in enumerate(gc.get_referents(o)):
        print(f" - {i} ) {r}")
    print(f"\n### -> Referrers - {o}")
    for i,r in enumerate(gc.get_referrers(o)):
        print(f" - {i} ) {r}")
        for ii,rr in enumerate(gc.get_referrers(r)):
            print(f"   | {ii} ) {rr}")
        print("")
    print("")


class TestWid(ttk.TTkWidget):
    __slots__ = ('_a','_b')
    def __init__(self, *args, **kwargs):
        self.setDefaultSize(kwargs, 10, 10)
        super().__init__(*args, **kwargs)
        self._b = ttk.pyTTkSignal(bool)
        self.setFocusPolicy(ttk.TTkK.ClickFocus + ttk.TTkK.TabFocus)

    def mousePressEvent(self, evt):
        # TTkLog.debug(f"{self._text} Test Mouse {evt}")
        self.update()
        return True

    def paintEvent(self, canvas):
        canvas.fill(pos=(0,0), size=(2,2))

print("\n############# Phase 1 ##################")
# wid = ttk.TTkWidget()
wid = ttk.TTkButton()
# wid = ttk.TTkGraph()
# wid = ttk.TTkSpacer()
# wid = ttk.TTkSplitter()
# wid = TestWid()
# sizef = wid.size
sizef = []

wrwid    = weakref.ref(wid)
# wrsizef  = weakref.ref(sizef)
wrsizef  = wrwid
# wrsizef2 = weakref.WeakMethod(wid.size)
wrsizef2 = wrwid

_ref(wid)

print(f"{wrwid()=} {wrsizef()=} {wrsizef2()=}")
del wid
print(f"{gc.collect()=}")
# print(f"{sizef()}")
print(f"{wrwid()=} {wrsizef()=} {wrsizef2()=}")
sizef = None
print(f"{wrwid()=} {wrsizef()=} {wrsizef2()=}")
# time.sleep(4)
# print(f"{wrwid()=} {wrsizef()=} {wrsizef2()=}")
print(f"{gc.collect()=}")
print(f"{wrwid()=} {wrsizef()=} {wrsizef2()=}")

print(f"{gc.garbage=}")
print(f"End {gc.get_count()=}")
