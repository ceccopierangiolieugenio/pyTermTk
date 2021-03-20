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

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.resizableframe import TTkResizableFrame
from TermTk.TTkWidgets.widget import TTkWidget


class TTkWindow(TTkResizableFrame):
    __slots__ = ('_title', '_mouseDelta', '_draggable')
    def __init__(self, *args, **kwargs):
        TTkResizableFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkWindow' )
        self._title = kwargs.get('title' , 0 )
        self.setPadding(3,1,1,1)
        self._mouseDelta = (0,0)
        self.setFocusPolicy(TTkK.ClickFocus)
        self._draggable = False
        self._menubarTopPosition = 2

    def paintEvent(self):
        if self.hasFocus():
            color = TTkCfg.theme.windowBorderColorFocus
        else:
            color = TTkCfg.theme.windowBorderColor
        self._canvas.drawText(pos=(2,1),text=self._title)
        self._canvas.drawGrid(
                    color=color,
                    pos=(0,0), size=self.size(),
                    hlines=[2], grid=2)

    def mousePressEvent(self, evt):
        self._mouseDelta = (evt.x, evt.y)
        self._draggable = False
        w,_ = self.size()
        x,y = evt.x, evt.y
        # If the mouse position is inside the header box enable the dragging feature
        if x >= 1 and y>=1 and x<w-1 and y<3:
            self._draggable = True
            return True
        return TTkResizableFrame.mousePressEvent(self, evt)

    def mouseDragEvent(self, evt):
        if self._draggable:
            x,y = self.pos()
            dx = evt.x-self._mouseDelta[0]
            dy = evt.y-self._mouseDelta[1]
            self.move(x+dx, y+dy)
            return True
        return TTkResizableFrame.mouseDragEvent(self, evt)

    def focusInEvent(self):
        if self._menubarTop:
            self._menubarTop.setBorderColor(TTkColor.fg("#ffff55"))
        self.update()

    def focusOutEvent(self):
        self._draggable = False
        if self._menubarTop:
            self._menubarTop.setBorderColor(TTkColor.RST)
        self.update()