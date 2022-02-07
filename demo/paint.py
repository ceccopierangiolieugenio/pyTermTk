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

import argparse
import os
import sys
import time

sys.path.append(os.path.join(sys.path[0],'..'))
from TermTk import TTk, TTkGridLayout, TTkK, TTkWidget, TTkWindow, TTkColor

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Full Screen', action='store_true')
args = parser.parse_args()

fullscreen = args.f

class PaintCanvas(TTkWidget):
    __slots__ = ('_pressPos', '_dragPos', '_boxes')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'PaintCanvas' )
        self._pressPos = None
        self._dragPos = None
        self._boxes = []
        self.setFocusPolicy(TTkK.ClickFocus)


    def mousePressEvent(self, evt):
        self._pressPos = (evt.x, evt.y)
        self.update()
        return True

    def mouseReleaseEvent(self, evt) -> bool:
        if self._pressPos and self._dragPos:
            x = min(self._pressPos[0], self._dragPos[0])
            y = min(self._pressPos[1], self._dragPos[1])
            w = max(self._pressPos[0]-x, self._dragPos[0]-x)
            h = max(self._pressPos[1]-y, self._dragPos[1]-y)
            if w>0 and h>0:
                self._boxes.append(((x,y),(w,h)))
        self._pressPos = None
        self._dragPos = None
        self.update()
        return True

    def mouseDragEvent(self, evt) -> bool:
        self._dragPos = (evt.x, evt.y)
        self.update()
        return True

    def paintEvent(self):
        for b in self._boxes:
            self._canvas.drawBox(pos=b[0],size=b[1])
        if self._pressPos and self._dragPos:
            x = min(self._pressPos[0], self._dragPos[0])
            y = min(self._pressPos[1], self._dragPos[1])
            w = max(self._pressPos[0]-x, self._dragPos[0]-x)
            h = max(self._pressPos[1]-y, self._dragPos[1]-y)
            if w>0 and h>0:
                self._canvas.drawBox(pos=(x,y),size=(w,h), color=TTkColor.fg('#ffff00'))

root = TTk()
if fullscreen:
    paint = root
    root.setLayout(TTkGridLayout())
else:
    root = TTk()
    paint = TTkWindow(parent=root,pos = (1,1), size=(100,30), title="Paint...", border=True, layout=TTkGridLayout())

PaintCanvas(parent=paint)

root.mainloop()
