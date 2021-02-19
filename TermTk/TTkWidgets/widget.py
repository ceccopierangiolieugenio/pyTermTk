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

from TermTk.TTkCore.canvas import *
from TermTk.TTkCore.cfg import *
from .layout import *

class TTkWidget:
    def __init__(self, *args, **kwargs):
        self._childs = []
        self._parent = kwargs.get('parent', None )
        self._x = kwargs.get('x', 0 )
        self._y = kwargs.get('y', 0 )
        self._width  = kwargs.get('width' , 0 )
        self._height = kwargs.get('height', 0 )
        self._maxw = 0x80000000
        self._maxh = 0x80000000
        self._minw = 0x00000000
        self._minh = 0x00000000
        self._layout = TTkLayout()
        self._canvas = TTkCanvas(
                            widget = self,
                            width  = self._width  ,
                            height = self._height )
        if self._parent is not None and \
           self._parent._layout is not None:
            self._parent._layout.addWidget(self)

    def getX(self): return self._x
    def getY(self): return self._y
    def getWidth(self):  return self._width
    def getHeight(self): return self._height

    def pos(self):
        return (self._x, self._y)

    def addLayout(self, l):
        self._layout = l

    def paintEvent(self): pass

    def move(self, x, y):
        self._x = x
        self._y = y
        self._canvas.move(self._x, self._y)
        if self._layout is not None:
            self._layout.setGeometry(self._x, self._y, self._width, self._height)
        self.update()

    def resize(self, w, h):
        self._width  = w
        self._height = h
        self._canvas.resize(self._width, self._height)
        if self._layout is not None:
            self._layout.setGeometry(self._x, self._y, self._width, self._height)
        self.update()

    def setGeometry(self, x, y, w, h):
        self.resize(w, h)
        self.move(x, y)

    def mouseDoubleClickEvent(self, evt): pass
    def mouseMoveEvent(self, evt): pass
    def mousePressEvent(self, evt): pass
    def mouseReleaseEvent(self, evt): pass
    def wheelEvent(self, evt): pass
    def enterEvent(self, evt): pass
    def leaveEvent(self, evt): pass
    def keyPressEvent(self, evt): pass
    def keyReleaseEvent(self, evt): pass

    def event(self, evt):
        pass
#        # handle own events
#        if evt.type() == CuEvent.MouseMove:
#            if evt.button() == CuT.NoButton:
#                self.mouseMoveEvent(evt)
#        elif   evt.type() == CuEvent.MouseButtonRelease:
#            self.mouseReleaseEvent(evt)
#        elif evt.type() == CuEvent.MouseButtonPress:
#            self.mousePressEvent(evt)
#            if self.focusPolicy() & CuT.ClickFocus == CuT.ClickFocus:
#                self.setFocus()
#        elif evt.type() == CuEvent.Wheel:
#            self.wheelEvent(evt)
#            if self.focusPolicy() & CuT.WheelFocus == CuT.WheelFocus:
#                self.setFocus()
#        elif evt.type() == CuEvent.KeyPress:
#            self.keyPressEvent(evt)
#        elif evt.type() == CuEvent.KeyRelease:
#            self.keyReleaseEvent(evt)
#        # Trigger this event to the childs
#        if self._layout is not None:
#            return CuWidget._eventLayoutHandle(evt, self._layout)
    def maximumSize(self):
        return self.maximumWidth(), self.maximumHeight()
    def maximumHeight(self):
        wMaxH = self._maxh
        if self._layout is not None:
            lMaxH = self._layout.maximumHeight()
            if lMaxH < wMaxH:
                return lMaxH
        return wMaxH
    def maximumWidth(self):
        wMaxW = self._maxw
        if self._layout is not None:
            lMaxW = self._layout.maximumWidth()
            if lMaxW < wMaxW:
                return lMaxW
        return wMaxW

    def minimumSize(self):
        return self.minimumWidth(), self.minimumHeight()
    def minimumHeight(self):
        wMinH = self._minh
        if self._layout is not None:
            lMinH = self._layout.minimumHeight()
            if lMinH > wMinH:
                return lMinH
        return wMinH
    def minimumWidth(self):
        wMinW = self._minw
        if self._layout is not None:
            lMinW = self._layout.minimumWidth()
            if lMinW > wMinW:
                return lMinW
        return wMinW

    def setMaximumSize(self, maxw, maxh): self._maxw = maxw; self._maxh = maxh
    def setMaximumHeight(self, maxh):     self._maxh = maxh
    def setMaximumWidth(self, maxw):      self._maxw = maxw

    def setMinimumSize(self, minw, minh): self._minw = minw; self._minh = minh
    def setMinimumHeight(self, minh):     self._minh = minh
    def setMinimumWidth(self, minw):      self._minw = minw

    def update(self):
        TTkHelper.addUpdateWidget(self)
        if self._layout is not None:
            self._layout.update()

    def getCanvas(self):
        return self._canvas

    def layout(self):
        return self._layout

    def setParent(self, parent):
        self._parent = parent
    def parentWidget(self):
        return self._parent