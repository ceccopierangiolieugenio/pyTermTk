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

root = TermTk.TTk()

frame = ttk.TTkFrame(parent=root, border=True, pos=(2,1), size=(30,10))
frame.setPadding(2,2,2,2)

frame.layout().addWidget(ttk.TTkFrame(parent=frame, border=True, pos=(-4,-3), size=(20,15)))

frame.layout().addWidget(ttk.TTkLabel(text="A-123-A-4567890-A", pos=(-3,-2), size=(17,1)))
frame.layout().addWidget(ttk.TTkLabel(text="B-123-B-4567890-B", pos=(-3,-1), size=(17,1)))
frame.layout().addWidget(ttk.TTkLabel(text="C-123-C-4567890-C", pos=(-3, 0), size=(17,1)))
frame.layout().addWidget(ttk.TTkLabel(text="D-123-D-4567890-D-123-D-4567890-D", pos=(-3, 1), size=(33,1)))
frame.layout().addWidget(ttk.TTkLabel(text="E-123-E-4567890-E", pos=(-3, 2), size=(17,1)))
frame.layout().addWidget(ttk.TTkLabel(text="F-123-F-4567890-F", pos=(-3, 3), size=(17,1)))

def cb(_):
    ox = sbx.value()
    oy = sby.value()
    frame.layout().setOffset(ox,oy)
    frame.update(updateLayout=True)

sbx = ttk.TTkSpinBox(parent=root, pos=(20,11), size=(10,1), maximum=50, minimum=-50)
sby = ttk.TTkSpinBox(parent=root, pos=(20,12), size=(10,1), maximum=50, minimum=-50)

sbx.valueChanged.connect(cb)
sby.valueChanged.connect(cb)

root.mainloop()