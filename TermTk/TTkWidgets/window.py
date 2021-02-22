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

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkWidgets.widget import TTkWidget


class TTkWindow(TTkWidget):
    __slots__ = ('_title', '_mouseDelta', '_draggable', '_resizable')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._title = kwargs.get('title' , 0 )
        self.setPadding(3,1,1,1)
        self._mouseDelta = (0,0)
        self.setFocusPolicy(TTkWidget.ClickFocus)
        self._draggable = False
        self._resizable = TTkWidget.NONE

    def paintEvent(self):
        if self.hasFocus():
            color = TTkColor.fg("#ffff55")
        else:
            color = TTkColor.RST
        self._canvas.drawBox(pos=(0,0),  color=color, size=(self._width,3))
        self._canvas.drawBox(pos=(0,2),  color=color, size=(self._width,self._height-2))
        self._canvas.drawText(pos=(0,2), color=color, text="╟"+("─"*(self._width-2))+"╢")
        self._canvas.drawText(pos=(2,1),text=self._title)

    def mousePressEvent(self, evt):
        self._mouseDelta = (evt.x, evt.y)
        w,h = self.size()
        x,y = evt.x, evt.y
        # If the mouse position is inside the header box enable the dragging feature
        if x >= 1 and y>=1 and x<w-1 and y<3:
            self._draggable = True
        else:
            # check if the ckick is on any norder to enable the resize feature
            if x==0:
                self._resizable |= TTkWidget.LEFT
            elif x==w-1:
                self._resizable |= TTkWidget.RIGHT
            if y==0:
                self._resizable |= TTkWidget.TOP
            elif y==h-1:
                self._resizable |= TTkWidget.BOTTOM
            # TTkLog.debug(f"{(x,y)} - {self._resizable}")


    def mouseDragEvent(self, evt):
        # TTkLog.debug(f"{self._resizable}")
        if self._draggable:
            x,y = self.pos()
            dx = evt.x-self._mouseDelta[0]
            dy = evt.y-self._mouseDelta[1]
            self.move(x+dx, y+dy)
        elif self._resizable:
            # TTkLog.debug(f"{self._resizable}")
            x,y,w,h = self.geometry()
            maxw, maxh = self.maximumSize()
            minw, minh = self.minimumSize()
            dx = evt.x-self._mouseDelta[0]
            dy = evt.y-self._mouseDelta[1]
            if self._resizable & TTkWidget.LEFT:
                tmpw = w-dx
                if minw < tmpw < maxw:
                    x += dx ; w -= tmpw
            elif self._resizable & TTkWidget.RIGHT:
                if minw < evt.x < maxw:
                    w = evt.x
            if self._resizable & TTkWidget.TOP:
                tmph = h-dy
                if minh < tmph < maxh:
                    y += dy ; h = tmph
            elif self._resizable & TTkWidget.BOTTOM:
                if minh < evt.y < maxh:
                    h = evt.y
            self.move(x,y)
            self.resize(w,h)



    def focusInEvent(self):
        self.update()

    def focusOutEvent(self):
        self._draggable = False
        self._resizable = TTkWidget.NONE
        self.update()