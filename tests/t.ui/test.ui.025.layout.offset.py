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

import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk
from math import sin, cos

import TermTk

class TestWidget(ttk.TTkWidget):
    def __init__(self, cc, *args, **kwargs):
        self._cc = cc
        super().__init__(*args, **kwargs)

    def paintEvent(self, canvas):
        for y in range(self.height()):
            canvas.drawText(pos=(0,y), text=self._cc*self.width())

root = TermTk.TTk()

frame = ttk.TTkFrame(parent=root, border=True, pos=(2,1), size=(15,8))
frame.setPadding(2,2,2,2)

frame.layout().addWidget(TestWidget(cc="X",pos=(0,0),size=(15,8)))

frame.layout().addItem(l2 := ttk.TTkLayout())
l2.setGeometry(2,4,5,3)
l2.addWidget(TestWidget(cc="+",pos=(0,0),size=(15,8)))

def cb(_):
    ox = sbx.value()
    oy = sby.value()
    frame.layout().setOffset(ox,oy)
    frame.update(updateLayout=True)

sbx = ttk.TTkSpinBox(parent=root, pos=(20,10), size=(10,1), maximum=50, minimum=-50)
sby = ttk.TTkSpinBox(parent=root, pos=(20,11), size=(10,1), maximum=50, minimum=-50)

sbx.valueChanged.connect(cb)
sby.valueChanged.connect(cb)

root.mainloop()