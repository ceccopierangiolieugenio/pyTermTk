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

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.ttk import *
from TermTk.TTkWidgets.widget import *
from TermTk.TTkWidgets.frame import *

class TTkSplitter(TTkFrame):
    __slots__ = ('_splitterInitialized', '_orientation','_separators', '_separatorSelected', '_mouseDelta')
    def __init__(self, *args, **kwargs):
        self._splitterInitialized = False
        # self._splitterInitialized = True
        self._separators = []
        self._separatorSelected = None
        self._orientation = TTkK.HORIZONTAL
        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkSpacer')
        self._orientation = kwargs.get('orientation', TTkK.HORIZONTAL)
        self.setBorder(False)
        self.setFocusPolicy(TTkK.ClickFocus)
        self._splitterInitialized = True

    def addWidget(self, widget, size=None):
        TTkFrame.addWidget(self, widget)
        _,_,w,h = self.geometry()

        if self._orientation == TTkK.HORIZONTAL:
            fullSize = w
        else:
            fullSize = h

        if self._separators:
            newSep = (self._separators[-1] + fullSize)  // 2
        else:
            newSep = -1
        self._separators.append(newSep)
        self._updateGeometries()

        #widgetsNum = self.layout().count()
        #lastId = widgetsNum - 2
        #newId = widgetsNum - 1
        #lastSep = -1
        #if self._separators:
        #    lastSep = self._separators[-1]
        #self._separators.append(newSep)
        #if self._orientation == TTkK.HORIZONTAL:
        #    self.layout().itemAt(oldId).setGeometry(lastSep+1, 0, newSep-lastSep-1, h)
        #    self.layout().itemAt(newId).setGeometry(newSep+1,  0, w-newSep-1,       h)
        #else:
        #    self.layout().itemAt(oldId).setGeometry(0, lastSep+1, w, newSep-lastSep-1)
        #    self.layout().itemAt(newId).setGeometry(0, newSep+1,  w, h-newSep-1)

    def _updateGeometries(self):
        _,_,w,h = self.geometry()
        forward = True
        sep = self._separators
        for i in range(len(sep)):
            item = self.layout().itemAt(i)
            if self._orientation == TTkK.HORIZONTAL:
                y = 0
                x  = sep[i]+1
                if i>len(sep)-2: # this is the last widget
                    ww = w-x
                else:
                    ww = sep[i+1]-x
                    maxw = item.maxDimension(self._orientation)
                    minw = item.minDimension(self._orientation)
                    if   ww > maxw: ww = maxw
                    elif ww < minw: ww = minw
                    sep[i+1]=ww+x
                item.setGeometry(x,y,ww,h)
            else:
                x = 0
                y  = sep[i]+1
                if i>len(sep)-2: # this is the last widget
                    hh = h-y
                else:
                    hh = sep[i+1]-y
                    maxh = item.maxDimension(self._orientation)
                    minh = item.minDimension(self._orientation)
                    if   hh > maxh: hh = maxh
                    elif hh < minh: hh = minh
                    sep[i+1]=hh+y
                item.setGeometry(x,y,w,hh)

    def resizeEvent(self, w, h):
        self._updateGeometries()

    def paintEvent(self):
        w,h = self.size()
        if self._orientation == TTkK.HORIZONTAL:
            for i in self._separators:
                self._canvas.drawVLine(pos=(i,0), size=h)
        else:
            for i in self._separators:
                self._canvas.drawHLine(pos=(0,i), size=w)

    def mousePressEvent(self, evt):
        self._separatorSelected = None
        self._mouseDelta = (evt.x, evt.y)
        x,y = evt.x, evt.y
        TTkLog.debug(f"{self._separators} {evt}")
        for i in range(len(self._separators)):
            val = self._separators[i]
            if self._orientation == TTkK.HORIZONTAL:
                if x == val:
                    self._separatorSelected = i
                    self.update()
                    self._updateGeometries()
                    return True
            else:
                if y == val:
                    self._separatorSelected = i
                    self.update()
                    self._updateGeometries()
                    return True

    def mouseDragEvent(self, evt):
        if self._separatorSelected is not None:
            # TTkLog.debug(f"{self._resizable}")
            x,y,w,h = self.geometry()
            maxw, maxh = self.maximumSize()
            minw, minh = self.minimumSize()
            dx = evt.x-self._mouseDelta[0]
            dy = evt.y-self._mouseDelta[1]
            if self._orientation == TTkK.HORIZONTAL:
                self._separators[self._separatorSelected] = evt.x
            else:
                self._separators[self._separatorSelected] = evt.y
            self._updateGeometries()
            self.update()
            return True
        return False


    def minimumHeight(self) -> int:
        if not self._splitterInitialized: return 0
        min = 0
        if self._orientation == TTkK.VERTICAL:
            for item in self.layout().children():
                min+=item.minimumHeight()
        else:
            for item in self.layout().children():
                if min < item.minimumHeight():
                    min = item.minimumHeight()
        return min

    def minimumWidth(self)  -> int:
        if not self._splitterInitialized: return 0
        min = 0
        if self._orientation == TTkK.HORIZONTAL:
            for item in self.layout().children():
                min+=item.minimumWidth()
        else:
            for item in self.layout().children():
                if min < item.minimumWidth():
                    min = item.minimumWidth()
        return min

    def maximumHeight(self) -> int:
        if not self._splitterInitialized: return 0x10000
        if self._orientation == TTkK.VERTICAL:
            max = 0
            for item in self.layout().children():
                max+=item.maximumHeight()
        else:
            max = 0x10000
            for item in self.layout().children():
                if max > item.maximumHeight():
                    max = item.maximumHeight()
        return max

    def maximumWidth(self)  -> int:
        if not self._splitterInitialized: return 0x10000
        if self._orientation == TTkK.HORIZONTAL:
            max = 0
            for item in self.layout().children():
                max+=item.maximumHeight()
        else:
            max = 0x10000
            for item in self.layout().children():
                if max > item.maximumWidth():
                    max = item.maximumWidth()
        return max
