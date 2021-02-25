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
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import *

class TTkButton(TTkWidget):
    __slots__ = ('_text', '_border', '_pressed', 'clicked')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        # Define Signals
        self.clicked = pyTTkSignal()

        self._name = kwargs.get('name' , 'TTkButton' )
        self.text = kwargs.get('text', "" )
        self._border = kwargs.get('border', True )
        if self._border:
            self.setMinimumSize(2+len(self.text), 3)
        else:
            self.setMinimumSize(len(self.text), 1)
        self._pressed = False
        self.setFocusPolicy(TTkWidget.ClickFocus)

    def paintEvent(self):
        if self._pressed:
            borderColor = TTkColor.RST
            textColor   = TTkColor.RST
            grid = 0
        else:
            borderColor = TTkColor.RST+TTkColor.BOLD
            textColor   = TTkColor.RST+TTkColor.BOLD
            grid = 1
        self._canvas.drawText(pos=(1,1), color=textColor ,text=self.text)
        if self._border:
            self._canvas.drawButtonBox(pos=(0,0),size=(self._width,self._height),color=borderColor, grid=grid)

    def mousePressEvent(self, evt):
        TTkLog.debug(f"{self._text} Test Mouse {evt}")
        self._pressed = True
        self.update()
        return True

    def mouseReleaseEvent(self, evt):
        TTkLog.debug(f"{self._text} Test Mouse {evt}")
        self._pressed = False
        self.update()
        self.clicked.emit()
        return True

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.setMinimumSize(len(text), 1)
        self.update()