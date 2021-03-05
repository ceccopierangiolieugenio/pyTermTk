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
from TermTk.TTkWidgets.frame import TTkFrame

class TTkResizableFrame(TTkFrame):
    __slots__ = ('_mouseDelta', '_resizable')
    def __init__(self, *args, **kwargs):
        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkResizableFrame' )
        self.setBorder(True)
        self._mouseDelta = (0,0)
        self._resizable = TTkK.NONE
        self.setFocusPolicy(TTkK.ClickFocus)


    def mousePressEvent(self, evt):
        self._resizable = TTkK.NONE
        self._mouseDelta = (evt.x, evt.y)
        w,h = self.size()
        x,y = evt.x, evt.y

        # check if the ckick is on any norder to enable the resize feature
        if x==0:
            self._resizable |= TTkK.LEFT
        elif x==w-1:
            self._resizable |= TTkK.RIGHT
        if y==0:
            self._resizable |= TTkK.TOP
        elif y==h-1:
            self._resizable |= TTkK.BOTTOM
        # TTkLog.debug(f"{(x,y)} - {self._resizable}")
        #return self._resizable != TTkK.NONE
        return True

    def mouseDragEvent(self, evt):
        if self._resizable:
            # TTkLog.debug(f"{self._resizable}")
            x,y,w,h = self.geometry()
            maxw, maxh = self.maximumSize()
            minw, minh = self.minimumSize()
            dx = evt.x-self._mouseDelta[0]
            dy = evt.y-self._mouseDelta[1]
            if self._resizable & TTkK.LEFT:
                tmpw = w-dx
                if   minw > tmpw: tmpw=minw; dx= w-tmpw
                elif maxw < tmpw: tmpw=maxw; dx= w-tmpw
                x += dx ; w = tmpw
            elif self._resizable & TTkK.RIGHT:
                if   minw > evt.x: w = minw
                elif maxw < evt.x: w = maxw
                else: w = evt.x+1
            if self._resizable & TTkK.TOP:
                tmph = h-dy
                if   minh > tmph: tmph=minh; dy= h-tmph
                elif maxh < tmph: tmph=maxh; dy= h-tmph
                y += dy ; h = tmph
            elif self._resizable & TTkK.BOTTOM:
                if   minh > evt.y: h = minh
                elif maxh < evt.y: h = maxh
                else: h = evt.y+1
            self.move(x,y)
            self.resize(w,h)
            return True
        return False
