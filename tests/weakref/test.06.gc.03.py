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

# ttk.TTkLog.use_default_stdout_logging()

class testClass():
    pass

def pobjs():
    for i,o in enumerate(gc.get_objects()[-100:]):
        ss = str(o)
        if "Foo" in ss:
            ttk.TTkLog.info(f" * {i} - {ss}")

def _ref(o,ch="*"):
    # ttk.TTkLog.info(f"\n### -> Referents - {o}")
    # for i,r in enumerate(gc.get_referents(o)):
    #     ttk.TTkLog.info(f" - {i} ) {r}")
    ttk.TTkLog.info(f"### -> Referrers - {o}")
    for i,r in enumerate(gc.get_referrers(o)):
        ttk.TTkLog.info(f" {ch} {i} ) ({type(r)})-> {r}")
    ttk.TTkLog.info("")

def _gccb(phase,info):
    ttk.TTkLog.info(f" ---> {gc.garbage=}")
    ttk.TTkLog.info(f" ---> {phase=} {info=}")

class Button2(ttk.TTkButton):pass

root = ttk.TTk()

ttk.TTkLog.info(f"Start {gc.isenabled()=}")
# ttk.TTkLog.info(f"{gc.set_debug(gc.DEBUG_LEAK)=}")

# gc.callbacks.append(_gccb)

ttk.TTkLog.info("############# Phase 1 ##################")

foo = ttk.TTkAbout(parent=root)

bar1 = Button2(parent=root, border=True, text="Do it")
bar2 = ttk.TTkWidget()
pep = testClass()

win = ttk.TTkWindow(parent=root,pos = (0,10), size=(50,30), title="Test Window 1")
win.setLayout(ttk.TTkHBoxLayout())
ttk.TTkTestWidget(parent=win, border=False)

win = ttk.TTkWindow(parent=root,pos=(20,0), size=(150,30), title="Log Window", flags=ttk.TTkK.WindowFlag.WindowCloseButtonHint)
win.setLayout(ttk.TTkHBoxLayout())
ttk.TTkLogViewer(parent=win, follow=True )

win = ttk.TTkWindow(parent=root,pos = (5,35), size=(85,7), title="Captured Input")
win.setLayout(ttk.TTkHBoxLayout())
ttk.TTkKeyPressView(parent=win)

del win

ttk.TTkAbout(parent=root, pos=(5,17))



ttk.TTkLog.info(f"{gc.collect()=}")
ttk.TTkLog.info(f"Mid {gc.get_count()=}")


@ttk.pyTTkSlot()
def _doit():
    ttk.TTkLog.info(f"{gc.collect()=}")
    ttk.TTkLog.info(f"End {gc.get_count()=}")
bar1.clicked.connect(_doit)
bar1.clicked.connect(foo.close)

foo.closed.connect(lambda _x: _ref(_x, "-Closed-"))

_ref(foo, "-Active-")
del foo

root.mainloop()

foo.close()

_ref(foo, "-Closed-")
