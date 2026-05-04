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

import sys, os, argparse, math, random
from typing import Tuple

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

class _Test_TTkTestAbstractScrollWidget(ttk.TTkTestAbstractScrollWidget):
    def __init__(self, *, name = None, areaSize = ..., areaPos = ..., **kwargs):
        super().__init__(name=name, areaSize=areaSize, areaPos=areaPos, **kwargs)
        ttk.TTkLabel(parent=self, pos=(1,10), text='Size:')
        ttk.TTkLabel(parent=self, pos=(1,11), text='Pos:')
        ttk.TTkLabel(parent=self, pos=(1,12), text='P/S:')

        self._sb_size = ttk.TTkSpinBox(parent=self, pos=(7,10), size=(10,1), value=40)
        self._sb_pos  = ttk.TTkSpinBox(parent=self, pos=(7,11), size=(10,1))
        self._sb_p_s  = ttk.TTkSpinBox(parent=self, pos=(7,12), size=(10,1))

        self._sb_size.valueChanged.connect(self._changed_size)
        self._sb_pos.valueChanged.connect(self._changed_pos)
        self._sb_p_s.valueChanged.connect(self._changed_pos_and_size)

    def viewFullAreaSize(self) -> Tuple[int, int]:
        w,h = self.size()
        new_h = self._sb_size.value()
        return w, new_h

    @ttk.pyTTkSlot(int)
    def _changed_size(self, size:int) -> None:
        self._realign()

    @ttk.pyTTkSlot(int)
    def _changed_pos(self, pos:int) -> None:
        self._realign()

    @ttk.pyTTkSlot(int)
    def _changed_pos_and_size(self, pos:int) -> None:
        self._sb_size.setValue(random.randint(30,150))
        self._sb_pos.setValue(pos)

    def _realign(self):
        ox, oy = self.getViewOffsets()
        w,h = self.size()
        new_h = self._sb_size.value()
        new_pos = self._sb_pos.value()
        self.viewMoveTo(ox, new_pos)

    def paintEvent(self, canvas:ttk.TTkCanvas):
        super().paintEvent(canvas)
        ox, oy = self.getViewOffsets()
        canvas.drawText(pos=(30-ox, 10-oy), text='<-1------>')
        canvas.drawText(pos=(30-ox, 20-oy), text='<-2---->')
        canvas.drawText(pos=(30-ox, 30-oy), text='<-3------>')
        canvas.drawText(pos=(30-ox, 40-oy), text='<-4---->')
        canvas.drawText(pos=(30-ox, 50-oy), text='<-5------>')



class ScrollAreaTest(ttk.TTkAbstractScrollArea):
    __slots__ = ('_areaView',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kwargs.pop('parent',None)
        kwargs.pop('visible',None)
        self.setFocusPolicy(ttk.TTkK.ClickFocus)
        self.setViewport(_Test_TTkTestAbstractScrollWidget(areaSize=(100,40), areaPos=(10,5)))

def demoScrollArea(root= None):
    scrollArea = ScrollAreaTest(parent=root)
    return scrollArea

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if args.f:
        rootGraph = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootGraph = ttk.TTkWindow(parent=root,pos=(1,1), size=(50,20), title="Test Graph", border=True, layout=ttk.TTkGridLayout())
    demoScrollArea(rootGraph)
    root.mainloop()

if __name__ == "__main__":
    main()