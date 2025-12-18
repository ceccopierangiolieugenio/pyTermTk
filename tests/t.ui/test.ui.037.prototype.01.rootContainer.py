
#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk


class MovementContainer(ttk.TTkContainer):
    def __init__(self, *, widget=ttk.TTkWidget, **kwargs):
        super().__init__(**kwargs)
        self.layout().addWidget(widget=widget)
        widget.sizeChanged.connect(self._sizeChanged)
        # widget.positionChanged.connect(self._positionChanged)


    @ttk.pyTTkSlot(int,int)
    def _sizeChanged(self,w,h):
        self.resize(w,h)

    @ttk.pyTTkSlot(int,int)
    def _positionChanged(self,x,y):
        ox,oy = self.layout().offset()
        self.layout().setOffset(-x,-y)
        self.move(x,y)

    def paintEvent(self, canvas):
        canvas.fill(color=ttk.TTkColor.BG_RED)

root = ttk.TTk()

win = ttk.TTkWindow(size=(40,15))
frame = ttk.TTkResizableFrame(size=(40,15), border=True)

mcWin = MovementContainer(widget=win, parent=root, pos=(10,5),  size=(40,15))
mcFrame = MovementContainer(widget=frame, parent=root, pos=(5,2),  size=(40,15))


root.mainloop()
