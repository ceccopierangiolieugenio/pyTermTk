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
from TermTk.TTkWidgets.widget import TTkWidget

'''
    ref: https://doc.qt.io/qt-5/qscrollbar.html
'''
class TTkScrollBar(TTkWidget):
    __slots__ = (
        '_orientation',
        '_minimum', '_maximum',
        '_singlestep', '_pagestep',
        '_value', '_color')

    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkScrollBar' )
        self._orientation = kwargs.get('orientation' , TTkK.VERTICAL )
        if self._orientation == TTkK.VERTICAL:
            self.setMaximumWidth(1)
            self.setMinimumSize(1,3)
        else:
            self.setMaximumHeight(1)
            self.setMinimumSize(3,1)
        self._minimum = kwargs.get('minimum' , 0 )
        self._maximum = kwargs.get('maximum' , 99 )
        self._singlestep = kwargs.get('singlestep' , 1 )
        self._pagestep = kwargs.get('pagestep' , 10 )
        self._value = kwargs.get('value' , 0 )
        self._color = kwargs.get('color', TTkColor.RST )
        self.update()

    '''
         | min        | max
        <-----XXXXX-------->   scrollbar
        |------------------|   size = widt or height
         |----------------|   size2 = widt or height - 2 (removed the ending arrows)
         |------------|     workingSize = max - min
         |----------------| drawingSize = max - min + pagestep
              a---b            slider = [a=value-min, b=a+pagestep]
              |---|            pagestep

    '''
    def paintEvent(self):
        if self._orientation == TTkK.VERTICAL:
            size=self._height
        else:
            size=self._width
        size2 = size-2
        drawingSize = self._maximum - self._minimum + self._pagestep
        a = self._value - self._minimum
        b = a + self._pagestep
        # covert i screen coordinates
        aa = 1+a*size2//drawingSize
        bb = 1+b*size2//drawingSize
        self._canvas.drawScroll(pos=(0,0),size=size,slider=(aa,bb),orientation=self._orientation, color=self.color)

    @property
    def minimum(self): return self._minimum
    @minimum.setter
    def minimum(self, v): self._minimum = v; self.update()

    @property
    def maximum(self): return self._maximum
    @minimum.setter
    def minimum(self, v): self._maximum = v; self.update()

    @property
    def singlestep(self): return self._singlestep
    @singlestep.setter
    def singlestep(self, v): self._singlestep = v; self.update()

    @property
    def pagestep(self): return self._pagestep
    @pagestep.setter
    def pagestep(self, v): self._pagestep = v; self.update()

    @property
    def value(self): return self._value
    @value.setter
    def value(self, v):
        if v > self._maximum: v = self._maximum
        if v < self._minimum: v = self._minimum
        self._value = v
        self.update()

    def wheelEvent(self, evt):
        if evt.evt == TTkK.WHEEL_Up:
            self.value = self._value - self._pagestep
        else:
            self.value = self._value + self._pagestep

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, color):
        if self.color != color:
            self._color = color
            self.update()