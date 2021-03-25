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
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import *

class TTkButton(TTkWidget):
    __slots__ = (
        '_text', '_border', '_pressed', 'clicked', '_keyPressed',
        '_borderColor',        '_textColor',
        '_borderColorClicked', '_textColorClicked',
        '_borderColorFocus',   '_textColorFocus'
        )
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkButton' )
        # Define Signals
        self.clicked = pyTTkSignal()

        self._text = kwargs.get('text', "" )
        self._border = kwargs.get('border', False )
        self._borderColor = kwargs.get('borderColor', TTkCfg.theme.buttonBorderColor )
        self._textColor   = kwargs.get('color',       TTkCfg.theme.buttonTextColor )
        self._borderColorClicked = TTkCfg.theme.buttonBorderColorClicked
        self._textColorClicked   = TTkCfg.theme.buttonTextColorClicked
        self._borderColorFocus   = TTkCfg.theme.buttonBorderColorFocus
        self._textColorFocus     = TTkCfg.theme.buttonTextColorFocus

        self._pressed = False
        self._keyPressed = False
        if self._border:
            self.setMinimumSize(2+len(self._text), 3)
        else:
            self.setMinimumSize(len(self._text)+2, 1)
            self.setMaximumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def paintEvent(self):
        if self._pressed:
            borderColor = self._borderColorClicked
            textColor   = self._textColorClicked
            grid = TTkCfg.theme.buttonBoxGridClicked
        elif self.hasFocus():
            borderColor = self._borderColorFocus
            textColor   = self._textColorFocus
            grid = TTkCfg.theme.buttonBoxGrid
        else:
            borderColor = self._borderColor
            textColor   = self._textColor
            grid = TTkCfg.theme.buttonBoxGrid
        text = self._text
        w = self.width()-2
        h = self.height()
        y = (h-1)//2
        l = len(text)
        text = (" "*((w-l)//2)+text).ljust(w)
        if self._border:
            if self._border:
                self._canvas.drawButtonBox(pos=(0,0),size=(self._width,self._height),color=borderColor, grid=grid)
                for i in range(1,h-1):
                    self._canvas.drawText(pos=(1,i), color=textColor ,text=" "*w)
                self._canvas.drawText(pos=(1,y), color=textColor ,text=text)
            else:
                self._canvas.drawText(pos=(1,1), color=textColor ,text=text)
        else:
            self._canvas.drawText(pos=(0,y), color=borderColor ,text='[')
            self._canvas.drawText(pos=(1+len(text),y), color=borderColor ,text=']')
            self._canvas.drawText(pos=(1,y), color=textColor ,text=text)
        if self._keyPressed:
            self._keyPressed = False
            self._pressed = False
            self.update()

    def mousePressEvent(self, evt):
        # TTkLog.debug(f"{self._text} Test Mouse {evt}")
        self._pressed = True
        self.update()
        return True

    def mouseReleaseEvent(self, evt):
        # TTkLog.debug(f"{self._text} Test Mouse {evt}")
        self._pressed = False
        self.update()
        self.clicked.emit()
        return True

    def keyEvent(self, evt):
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            self._keyPressed = True
            self._pressed = True
            self.update()
            self.clicked.emit()
            return True
        return False

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.setMinimumSize(len(text), 1)
        self.update()