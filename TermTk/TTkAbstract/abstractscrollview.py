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

from TermTk.TTkCore.constant import TTkConstant, TTkK
from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget

class TTkAbstractScrollView(TTkWidget):
    __slots__ = (
        '_viewOffsetX', '_viewOffsetY',
        # Signals
         'viewMovedTo', 'viewSizeChanged', 'viewChanged')

    def __init__(self, *args, **kwargs):
        # Signals
        self.viewMovedTo = pyTTkSignal(int, int) # x, y
        self.viewSizeChanged = pyTTkSignal(int, int) # w, h
        self.viewChanged = pyTTkSignal()
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkAbstractScrollView')

        self._viewOffsetX = 0
        self._viewOffsetY = 0

    # Override this function
    def viewFullAreaSize(self) -> (int, int):
        raise NotImplementedError()

    # Override this function
    def viewDisplayedSize(self) -> (int, int):
        raise NotImplementedError()

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x, y):
        fw, fh  = self.viewFullAreaSize()
        dw, dh = self.viewDisplayedSize()
        rangex = fw - dw
        rangey = fh - dh
        # TTkLog.debug(f"x:{x},y:{y}, full:{fw,fh}, display:{dw,dh}, range:{rangex,rangey}")
        x = max(0,min(rangex,x))
        y = max(0,min(rangey,y))
        # TTkLog.debug(f"x:{x},y:{y}, wo:{self._viewOffsetX,self._viewOffsetY}")
        if self._viewOffsetX == x and \
           self._viewOffsetY == y: # Nothong to do
            return
        self._viewOffsetX = x
        self._viewOffsetY = y
        self.viewMovedTo.emit(x,y)
        self.viewChanged.emit()
        self.update()

    def wheelEvent(self, evt):
        delta = TTkCfg.scrollDelta
        offx, offy = self.getViewOffsets()
        if evt.evt == TTkK.WHEEL_Up:
            delta = -delta
        self.viewMoveTo(offx, offy + delta)
        return True

    def resizeEvent(self, w, h):
        self.viewMoveTo(self._viewOffsetX, self._viewOffsetY)
        self.viewSizeChanged.emit(w,h)
        self.viewChanged.emit()

    def getViewOffsets(self):
        return self._viewOffsetX, self._viewOffsetY

