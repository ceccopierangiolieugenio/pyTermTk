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

from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.menubar import TTkMenuLayout

class TTkFrame(TTkWidget):
    __slots__ = (
        '_border','_title', '_titleColor', '_titleAlign','_borderColor',
        '_menubarTop', '_menubarTopPosition', '_menubarBottom')
    def __init__(self, *args, **kwargs):
        self._borderColor = kwargs.get('borderColor', TTkCfg.theme.frameBorderColor )
        self._titleColor = kwargs.get('titleColor', TTkCfg.theme.frameTitleColor )
        self._titleAlign = kwargs.get('titleAlign' , TTkK.CENTER_ALIGN )
        self._title = kwargs.get('title' , '' )
        self._border = kwargs.get('border', True )
        self._menubarTopPosition = 0
        self._menubarTop = None
        self._menubarBottom = None
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkFrame' )
        self.setBorder(self._border)


    def menubarTop(self):
        if not self._menubarTop:
            self._menubarTop = TTkMenuLayout(borderColor=self._borderColor)
            self.rootLayout().addItem(self._menubarTop)
            self._menubarTop.setGeometry(1,self._menubarTopPosition,self.width()-2,1)
            if not self._border and self._padt == 0:
                self.setPadding(1,0,0,0)
        return self._menubarTop

    def resizeEvent(self, w, h):
        if self._menubarTop:
            self._menubarTop.setGeometry(1,self._menubarTopPosition,w-2,1)

    def setBorder(self, border):
        self._border = border
        if border: self.setPadding(1,1,1,1)
        else:      self.setPadding(0,0,0,0)

    def border(self):
        return self._border

    def paintEvent(self):
        if self._border:
            self._canvas.drawBox(pos=(0,0),size=(self._width,self._height), color=self._borderColor)
            if self._title != '':
                self._canvas.drawBoxTitle(
                                pos=(0,0),
                                size=(self._width,self._height),
                                text=self._title,
                                align=self._titleAlign,
                                color=self._borderColor,
                                colorText=self._titleColor)
        elif self._menubarTop:
            self._canvas.drawMenuBarBg(pos=(0,0),size=self.width(),color=self._borderColor)

