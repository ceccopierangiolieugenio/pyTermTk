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

__all__ = ['TTkAbstractScrollViewInterface', 'TTkAbstractScrollView', 'TTkAbstractScrollViewGridLayout']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout

class TTkAbstractScrollViewInterface():
    # Override this function
    def viewFullAreaSize(self) -> (int, int):
        raise NotImplementedError()

    # Override this function
    def viewDisplayedSize(self) -> (int, int):
        raise NotImplementedError()

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int):
        raise NotImplementedError()

    def getViewOffsets(self):
        return self._viewOffsetX, self._viewOffsetY

class TTkAbstractScrollView(TTkContainer, TTkAbstractScrollViewInterface):
    __slots__ = (
        '_viewOffsetX', '_viewOffsetY',
        # Signals
         'viewMovedTo', 'viewSizeChanged', 'viewChanged')

    def __init__(self, *args, **kwargs):
        # Signals
        self.viewMovedTo = pyTTkSignal(int, int) # x, y
        self.viewSizeChanged = pyTTkSignal(int, int) # w, h
        self.viewChanged = pyTTkSignal()
        self._viewOffsetX = 0
        self._viewOffsetY = 0
        TTkContainer.__init__(self, *args, **kwargs)

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int):
        fw, fh = self.viewFullAreaSize()
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

    def update(self, repaint=True, updateLayout=False, updateParent=False):
        if updateLayout:
            self.viewChanged.emit()
        return super().update(repaint, updateLayout, updateParent)

class TTkAbstractScrollViewLayout(TTkLayout, TTkAbstractScrollViewInterface):
    __slots__ = (
        '_viewOffsetX', '_viewOffsetY',
        # Signals
         'viewMovedTo', 'viewSizeChanged', 'viewChanged', '_excludeEvent')

    def __init__(self, *args, **kwargs):
        # Signals
        self.viewMovedTo = pyTTkSignal(int, int) # x, y
        self.viewSizeChanged = pyTTkSignal(int, int) # w, h
        self.viewChanged = pyTTkSignal()
        self._viewOffsetX = 0
        self._viewOffsetY = 0
        self._excludeEvent = False
        TTkLayout.__init__(self, *args, **kwargs)

    def viewFullAreaSize(self) -> (int, int):
        _,_,w,h = self.fullWidgetAreaGeometry()
        return w,h

    def viewDisplayedSize(self) -> (int, int):
        _,_,w,h = self.geometry()
        return w,h

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int):
        self.setOffset(-x,-y)

    def setGeometry(self, x, y, w, h):
        TTkLayout.setGeometry(self, x, y, w, h)
        self.viewChanged.emit()

class TTkAbstractScrollViewGridLayout(TTkGridLayout, TTkAbstractScrollViewInterface):
    __slots__ = (
        '_viewOffsetX', '_viewOffsetY',
        # Signals
         'viewMovedTo', 'viewSizeChanged', 'viewChanged', '_excludeEvent')

    def __init__(self, *args, **kwargs):
        # Signals
        self.viewMovedTo = pyTTkSignal(int, int) # x, y
        self.viewSizeChanged = pyTTkSignal(int, int) # w, h
        self.viewChanged = pyTTkSignal()
        self._viewOffsetX = 0
        self._viewOffsetY = 0
        self._excludeEvent = False
        TTkGridLayout.__init__(self, *args, **kwargs)

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int):
        fw, fh = self.viewFullAreaSize()
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
        self._excludeEvent = True
        for widget in self.iterWidgets(recurse=False):
            widget.viewMoveTo(x,y)
        self._excludeEvent = False
        self._viewOffsetX = x
        self._viewOffsetY = y
        self.viewMovedTo.emit(x,y)
        self.viewChanged.emit()
        self.update()

    def setGeometry(self, x, y, w, h):
        TTkGridLayout.setGeometry(self, x, y, w, h)
        self.viewChanged.emit()

    @pyTTkSlot()
    def _viewChanged(self):
        if self._excludeEvent: return
        self.viewChanged.emit()

    @pyTTkSlot(int,int)
    def _viewMovedTo(self, x, y):
        if self._excludeEvent: return
        self.viewMoveTo(x, y)

    def addWidget(self, widget, row=None, col=None, rowspan=1, colspan=1):
        if not issubclass(type(widget),TTkAbstractScrollViewInterface):
            raise TypeError("TTkAbstractScrollViewInterface is required in TTkAbstractScrollViewGridLayout.addWidget(...)")
        widget.viewChanged.connect(self._viewChanged)
        widget.viewMovedTo.connect(self._viewMovedTo)
        return TTkGridLayout.addWidget(self, widget, row, col, rowspan, colspan)

    def addItem(self, item, row=None, col=None, rowspan=1, colspan=1):
        if not issubclass(type(item),TTkAbstractScrollViewInterface):
            raise TypeError("TTkAbstractScrollViewInterface is required in TTkAbstractScrollViewGridLayout.addItem(...)")
        return TTkGridLayout.addItem(self, item, row, col, rowspan, colspan)

    # Override this function
    def viewFullAreaSize(self) -> (int, int):
        w,h=0,0
        for widget in self.iterWidgets(recurse=False):
            ww,wh = widget.viewFullAreaSize()
            w = max(w,ww)
            h = max(h,wh)
        return w,h

    # Override this function
    def viewDisplayedSize(self) -> (int, int):
        w,h=0,0
        for widget in self.iterWidgets(recurse=False):
            ww,wh = widget.viewDisplayedSize()
            w = max(w,ww)
            h = max(h,wh)
        return w,h

