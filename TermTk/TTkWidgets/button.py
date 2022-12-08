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
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkWidgets.widget import *

class TTkButton(TTkWidget):
    ''' TTkButton:

    Border = True
    ::

         ┌────────┐
         │  Text  │
         ╘════════╛

    Border = False
    ::

         [  Text  ]

    Demo: `formwidgets.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/formwidgets.py>`_

    :param str text: the text shown on the button, defaults to ""
    :type text: str, optional

    :param bool border: the border of the button, defaults to "False"
    :type border: bool, optional

    :param bool checked: checked status if the button is checkable, defaults to "False"
    :type checked: bool, optional
    :param bool checkable: define if the burtton is checkable, defaults to "False"
    :type checkable: bool, optional

    :param TTkColor color: the color of the border of the button, defaults to :class:`~TermTk.TTkTheme.theme.TTkTheme.buttonTextColor`
    :type color: :class:`~TermTk.TTkCore.color.TTkColor`, optional
    :param TTkColor borderColor: the color of the border of the button, defaults to :class:`~TermTk.TTkTheme.theme.TTkTheme.buttonBorderColor`
    :type borderColor: :class:`~TermTk.TTkCore.color.TTkColor`, optional

    +-----------------------------------------------------------------------------------------------+
    | `Signals <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/003-signalslots.html>`_ |
    +-----------------------------------------------------------------------------------------------+

        .. py:method:: clicked()
            :signal:

            This signal is emitted when the button is activated

        .. py:method:: toggled(checked)
            :signal:

            This signal is emitted whenever the button state changes if checkeable, i.e., whenever the user checks or unchecks it.

            :param checked: True if checked otherwise False
            :type checked: bool

    '''

    __slots__ = (
        '_text', '_border', '_pressed', '_keyPressed',
        '_checkable', '_checked',
        '_borderColor',        '_textColor',
        '_borderColorClicked', '_textColorClicked',
        '_borderColorFocus',   '_textColorFocus'
        '_borderColorDisabled','_textColorDisabled',
        # Signals
        'clicked', 'toggled'
        )
    def __init__(self, *args, **kwargs):
        self._text = TTkString(kwargs.get('text', ""))
        textWidth = self._text.termWidth()
        self._border = kwargs.get('border', False )
        self.setDefaultSize(kwargs, 2 + textWidth, 3 if self._border else 1 )

        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkButton' )
        # Define Signals
        self.clicked = pyTTkSignal()
        self.toggled = pyTTkSignal(bool)

        self._checked = kwargs.get('checked', False )
        self._checkable = kwargs.get('checkable', False )
        self._borderColor = kwargs.get('borderColor', TTkCfg.theme.buttonBorderColor )
        self._textColor   = kwargs.get('color',       TTkCfg.theme.buttonTextColor )
        self._borderColorClicked = TTkCfg.theme.buttonBorderColorClicked
        self._textColorClicked   = TTkCfg.theme.buttonTextColorClicked
        self._borderColorFocus   = TTkCfg.theme.buttonBorderColorFocus
        self._textColorFocus     = TTkCfg.theme.buttonTextColorFocus
        self._borderColorDisabled= TTkCfg.theme.buttonBorderColorDisabled
        self._textColorDisabled  = TTkCfg.theme.buttonTextColorDisabled

        self._pressed = False
        self._keyPressed = False
        if self._border:
            self.setMinimumSize(2+textWidth, 3)
        else:
            self.setMinimumSize(textWidth+2, 1)
            self.setMaximumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def isCheckable(self):
        return self._checkable

    def setCheckable(self, ch):
        self._checkable = ch
        self.update()

    def isChecked(self):
        return self._checked

    def setChecked(self, ch):
        self._checked = ch
        self.toggled.emit(self._checked)
        self.update()

    def color(self):
        return self._textColor

    def setColor(self, color):
        self._textColor = color
        self.update()

    def borderColor(self):
        return self._borderColor

    def setBorderColor(self, color):
        self._borderColor = color
        self.update()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = TTkString(text)
        self.setMinimumSize(self._text.termWidth()+2, 1)
        self.update()

    def mousePressEvent(self, evt):
        # TTkLog.debug(f"{self._text} Test Mouse {evt}")
        self._pressed = True
        self.update()
        return True

    def mouseReleaseEvent(self, evt):
        # TTkLog.debug(f"{self._text} Test Mouse {evt}")
        self._pressed = False
        if self._checkable:
            self._checked = not self._checked
            self.toggled.emit(self._checked)
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

    def paintEvent(self):
        if not self.isEnabled():
            borderColor = self._borderColorDisabled
            textColor   = self._textColorDisabled
            grid = TTkCfg.theme.buttonBoxGridDisabled
        elif self._pressed:
            borderColor = self._borderColorClicked
            textColor   = self._textColorClicked
            grid = TTkCfg.theme.buttonBoxGridClicked
        else:
            if self._checkable:
                if self._checked:
                    grid = TTkCfg.theme.buttonBoxGridChecked
                    borderColor = TTkCfg.theme.buttonBorderColorChecked
                    textColor = TTkCfg.theme.buttonTextColorChecked
                else:
                    grid = TTkCfg.theme.buttonBoxGridUnchecked
                    borderColor = TTkCfg.theme.buttonBorderColorUnchecked
                    textColor = TTkCfg.theme.buttonTextColorUnchecked
            else:
                grid = TTkCfg.theme.buttonBoxGrid
                borderColor = self._borderColor
                if self.hasFocus():
                    textColor   = self._textColorFocus
                else:
                    textColor   = self._textColor
            if self.hasFocus():
                borderColor = self._borderColorFocus
        text = self._text
        w = self.width()-2
        h = self.height()
        y = (h-1)//2
        text = text.align(width=w, alignment=TTkK.CENTER_ALIGN).addColor(textColor)
        if self._border:
            if self._border:
                self._canvas.drawButtonBox(pos=(0,0),size=(self._width,self._height),color=borderColor, grid=grid)
                for i in range(1,h-1):
                    self._canvas.drawText(pos=(1,i) ,text=TTkString(" "*w, textColor))
                self._canvas.drawText(pos=(1,y) ,text=text)
            else:
                self._canvas.drawText(pos=(1,1) ,text=text)
        else:
            self._canvas.drawText(pos=(0,y), color=borderColor ,text='[')
            self._canvas.drawText(pos=(1+text.termWidth(),y), color=borderColor ,text=']')
            self._canvas.drawText(pos=(1,y) ,text=text)

