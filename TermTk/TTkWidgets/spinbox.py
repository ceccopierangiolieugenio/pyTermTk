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

__all__ = ['TTkSpinBox']

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkLayouts import TTkGridLayout
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.lineedit import TTkLineEdit

class TTkSpinBox(TTkContainer):
    '''TTkSpinBox'''

    classStyle = {
                'default':     {'color': TTkColor.RST},
                'disabled':    {'color': TTkColor.fg('#888888')},
                'focus':       {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000044")+TTkColor.BOLD},
            }

    __slots__= (
        '_lineEdit', '_value', '_maximum', '_minimum',
        '_mouseDelta', '_valueDelta', '_draggable',
        # Signals
        'valueChanged')
    def __init__(self, *args, **kwargs):
        # Signals
        self.valueChanged=pyTTkSignal(int)
        super().__init__(*args, **kwargs)
        self._value = kwargs.get("value",0)
        self._maximum = kwargs.get("maximum",99)
        self._minimum = kwargs.get("minimum",0)
        self.setLayout(TTkGridLayout())
        self.setPadding(0,0,0,2)
        self.setMinimumSize(4,1)
        self._mouseDelta = 0
        self._valueDelta = 0
        self._draggable = False
        self._lineEdit = TTkLineEdit(parent=self, text=str(self._value), inputType=TTkK.Input_Number, enabled=self.isEnabled())
        self._lineEdit.keyEvent = self.keyEvent
        self.setFocusPolicy(TTkK.ClickFocus)
        self._lineEdit.textEdited.connect(self._textEdited)

    def value(self):
        '''value'''
        return self._value

    @pyTTkSlot(int)
    def setValue(self, value):
        '''setValue'''
        value = min(value,self._maximum)
        value = max(value,self._minimum)
        if self._value == value: return
        self._value = value
        self._lineEdit.setText(str(self._value))
        self.valueChanged.emit(value)

    def minimum(self):
        '''minimum'''
        return self._minimum

    @pyTTkSlot(int)
    def setMinimum(self, minimum):
        '''setMinimum'''
        if self._minimum == minimum:
            return
        self._minimum = minimum
        self.setValue(self._value)

    def maximum(self):
        '''maximum'''
        return self._maximum

    @pyTTkSlot(int)
    def setMaximum(self, maximum):
        '''setMaximum'''
        if self._maximum == maximum:
            return
        self._maximum = maximum
        self.setValue(self._value)

    @pyTTkSlot(str)
    def _textEdited(self, text):
        self.setValue(int(str(text)))
        self._lineEdit.setText(str(self._value))

    def wheelEvent(self, evt):
        if evt.evt == TTkK.WHEEL_Up:
            self.setValue(self._value+1)
        else:
            self.setValue(self._value-1)
        return True

    def keyEvent(self, evt):
        if evt.type == TTkK.SpecialKey:
            if evt.key == TTkK.Key_Up:
                self.setValue(self._value+1)
                return True
            elif evt.key == TTkK.Key_Down:
                self.setValue(self._value-1)
                return True
        return TTkLineEdit.keyEvent(self._lineEdit, evt)

    def mousePressEvent(self, evt):
        x,y = evt.x, evt.y
        w = self.width()
        value = self._value
        self._draggable = False
        if x==w-2:
            self._draggable = True
            value += 1
        if x==w-1:
            self._draggable = True
            value -= 1
        self.setValue(value)
        self._mouseDelta = y-x
        self._valueDelta = self._value
        return True

    def mouseDragEvent(self, evt):
        d = evt.y-evt.x
        if self._draggable:
            self.setValue(self._valueDelta + self._mouseDelta - d)
            return True

    def setEnabled(self, enabled=True):
        self._lineEdit.setEnabled(enabled)
        return super().setEnabled(enabled)

    def paintEvent(self, canvas):
        style = self.currentStyle()
        color = style['color']
        w = self.width()
        canvas.drawChar(pos=(w-2,0),char="▲", color=color)
        canvas.drawChar(pos=(w-1,0),char="▼", color=color)

    def focusOutEvent(self):
        self._draggable = False
        self._lineEdit.focusOutEvent()
        self._lineEdit.update()