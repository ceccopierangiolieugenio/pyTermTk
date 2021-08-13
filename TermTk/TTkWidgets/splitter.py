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
from TermTk.TTkWidgets.widget import *
from TermTk.TTkWidgets.frame import *

class TTkSplitter(TTkFrame):
    __slots__ = (
        '_splitterInitialized', '_orientation',
        '_separators', '_separatorsRef', '_sizeRef', '_initSizes',
        '_separatorSelected', '_mouseDelta')
    def __init__(self, *args, **kwargs):
        self._splitterInitialized = False
        # self._splitterInitialized = True
        self._separators = []
        self._separatorsRef = []
        self._sizeRef = 0
        self._initSizes = []
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
        numW = self.layout().count()

        if self._orientation == TTkK.HORIZONTAL:
            fullSize = w
        else:
            fullSize = h
        # assign the same slice to all the widgets
        self._initSizes.append(size)
        self._separators = [fullSize*i//numW for i in range(1,numW+1)]
        self._updateGeometries()
        self._separatorsRef = self._separators
        self._sizeRef = fullSize

    def _minMaxSizeBefore(self, index):
        if self._separatorSelected is None:
            return 0, 0x1000
        # this is because there is a hidden splitter at position -1
        minsize = -1
        maxsize = -1
        for i in range(self._separatorSelected+1):
            item = self.layout().itemAt(i)
            minsize += item.minDimension(self._orientation)+1
            maxsize += item.maxDimension(self._orientation)+1
        return minsize, maxsize

    def _minMaxSizeAfter(self, index):
        if self._separatorSelected is None:
            return 0, 0x1000
        minsize = 0x0
        maxsize = 0x0
        for i in range(self._separatorSelected+1, len(self._separators)):
            item = self.layout().itemAt(i)
            minsize += item.minDimension(self._orientation)+1
            maxsize += item.maxDimension(self._orientation)+1
        return minsize, maxsize

    def _updateGeometries(self, resized=False):
        if not self.isVisible(): return
        _,_,w,h = self.geometry()
        sep = self._separators
        x,y=0,0

        def _processGeometry(index, forward):
            item = self.layout().itemAt(i)
            pa = -1 if i==0 else sep[i-1]
            pb = sep[i]

            if self._orientation == TTkK.HORIZONTAL:
                newPos = pa+1
                size = w-newPos
            else:
                newPos = pa+1
                size = h-newPos

            if i<=len(sep)-2: # this is not the last widget
                size = pb-newPos
                maxsize = item.maxDimension(self._orientation)
                minsize = item.minDimension(self._orientation)
                if   size > maxsize: size = maxsize
                elif size < minsize: size = minsize
                if forward:
                    sep[i]=pa+size+1
                elif i>0 :
                    sep[i-1]=pa=pb-size-1

            if self._orientation == TTkK.HORIZONTAL:
                item.setGeometry(pa+1,0,size,h)
            else:
                item.setGeometry(0,pa+1,w,size)
            pass


        selected = 0
        if self._orientation == TTkK.HORIZONTAL:
            size = w
        else:
            size = h
        if self._separatorSelected is not None:
            selected = self._separatorSelected
            sepPos = sep[selected]
            minsize,maxsize = self._minMaxSizeBefore(selected)
            # TTkLog.debug(f"before:{minsize,maxsize}")
            if sepPos > maxsize: sep[selected] = maxsize
            if sepPos < minsize: sep[selected] = minsize
            minsize,maxsize = self._minMaxSizeAfter(selected)
            # TTkLog.debug(f"after:{minsize,maxsize}")
            if sepPos < size-maxsize: sep[selected] = size-maxsize
            if sepPos > size-minsize: sep[selected] = size-minsize

        if resized:
            l = len(sep)
            for i in reversed(range(l)):
                _processGeometry(i, False)
            for i in range(l):
                _processGeometry(i, True)
        else:
            for i in reversed(range(selected+1)):
                _processGeometry(i, False)
            for i in range(selected+1, len(sep)):
                _processGeometry(i, True)

        if self._separatorSelected is not None or self._sizeRef==0:
            self._separatorsRef = self._separators
            self._sizeRef = size

    def resizeEvent(self, w, h):
        if w==h==0: return
        if not self._sizeRef:
            # This is the first resize (w,h != 0 and previous reference size was 0)
            # I need to define the initial position of all the widgets
            if self._orientation == TTkK.HORIZONTAL:
                self._sizeRef = w
            else:
                self._sizeRef = h
            # get the sum of the fixed sizes
            fixSize = sum(filter(None, self._initSizes))
            numVarSizes = len([x for x in self._initSizes if x is None])
            avalSize = self._sizeRef-fixSize
            sizes = [avalSize//numVarSizes if s is None else s for s in self._initSizes]
            self._separatorsRef = [sum(sizes[:i+1]) for i in range(len(sizes))]

        # Adjust separators to the new size;
        self._separatorSelected = None
        if self._sizeRef > 0:
            if self._orientation == TTkK.HORIZONTAL:
                diff = w/self._sizeRef
            else:
                diff = h/self._sizeRef
            self._separators = [int(i*diff) for i in self._separatorsRef]
        self._updateGeometries(resized=True)

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
        # TTkLog.debug(f"{self._separators} {evt}")
        for i in range(len(self._separators)):
            val = self._separators[i]
            if self._orientation == TTkK.HORIZONTAL:
                if x == val:
                    self._separatorSelected = i
                    self.update()
                    self._updateGeometries()
            else:
                if y == val:
                    self._separatorSelected = i
                    self.update()
                    self._updateGeometries()
        return self._separatorSelected is not None

    def mouseDragEvent(self, evt):
        if self._separatorSelected is not None:
            if self._orientation == TTkK.HORIZONTAL:
                self._separators[self._separatorSelected] = evt.x
            else:
                self._separators[self._separatorSelected] = evt.y
            self._updateGeometries()
            self.update()
            return True
        return False

    def focusOutEvent(self):
        self._separatorSelected = None

    def minimumHeight(self) -> int:
        if not self._splitterInitialized: return 0
        ret = 0
        if self._orientation == TTkK.VERTICAL:
            for item in self.layout().children():
                ret+=item.minimumHeight()+1
            ret = max(0,ret-1)
        else:
            for item in self.layout().children():
                if ret < item.minimumHeight():
                    ret = item.minimumHeight()
        return ret

    def minimumWidth(self)  -> int:
        if not self._splitterInitialized: return 0
        ret = 0
        if self._orientation == TTkK.HORIZONTAL:
            for item in self.layout().children():
                ret+=item.minimumWidth()+1
            ret = max(0,ret-1)
        else:
            for item in self.layout().children():
                if ret < item.minimumWidth():
                    ret = item.minimumWidth()
        return ret

    def maximumHeight(self) -> int:
        if not self._splitterInitialized: return 0x10000
        if self._orientation == TTkK.VERTICAL:
            ret = 0
            for item in self.layout().children():
                ret+=item.maximumHeight()+1
            ret = max(0,ret-1)
        else:
            ret = 0x10000
            for item in self.layout().children():
                if ret > item.maximumHeight():
                    ret = item.maximumHeight()
        return ret

    def maximumWidth(self)  -> int:
        if not self._splitterInitialized: return 0x10000
        if self._orientation == TTkK.HORIZONTAL:
            ret = 0
            for item in self.layout().children():
                ret+=item.maximumHeight()+1
            ret = max(0,ret-1)
        else:
            ret = 0x10000
            for item in self.layout().children():
                if ret > item.maximumWidth():
                    ret = item.maximumWidth()
        return ret
