# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkSlider']

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

from TermTk.TTkWidgets.scrollbar import TTkScrollBar

'''
    ref: https://doc.qt.io/qt-5/qslider.html
'''
class TTkSlider(TTkScrollBar):
    '''TtkSlider'''

    classStyle = {
                'default':     {
                        'color': TTkColor.RST,
                        'sliderColor': TTkColor.fg('#6666bb')},
                'disabled':    {
                        'color': TTkColor.fg('#666666'),
                        'sliderColor': TTkColor.fg('#888888')},
                'focus':       {
                        'color': TTkColor.fg('#cccc00'),
                        'sliderColor': TTkColor.fg('#8888ff')},
            }

    def wheelEvent(self, evt:TTkMouseEvent) -> bool:
        if self._orientation == TTkK.VERTICAL:
            if evt.evt == TTkK.WHEEL_Up: value = self._value+self._pageStep
            else:                        value = self._value-self._pageStep
        else:
            if evt.evt == TTkK.WHEEL_Up: value = self._value-self._pageStep
            else:                        value = self._value+self._pageStep
        self.setValue(max(self._minimum,min(self._maximum,value)))
        self.sliderMoved.emit(self._value)
        return True

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        if self._orientation == TTkK.VERTICAL:
            size=self._height-1
            mouse = max(0,min(size,size-evt.y))
        else:
            size=self._width-1
            mouse = max(0,min(size,evt.x))

        self._draggable = False
        if self._maximum > self._minimum:
            smin = self._minimum
            smax = self._maximum
            sval = self._value
            sliderPos = int(0.5+size*(sval-smin)/(smax-smin))
            if mouse < sliderPos:
                self.setValue(self._value - self._pageStep)
            elif mouse > sliderPos:
                self.setValue(self._value + self._pageStep)
            else:
                self._draggable = True

        self.sliderMoved.emit(self._value)
        return True

    def mouseDragEvent(self, evt:TTkMouseEvent) -> bool:
        if not self._draggable: return False
        if self._orientation == TTkK.VERTICAL:
            size=self._height-1
            mouse = max(0,min(size,size-evt.y))
        else:
            size=self._width-1
            mouse = max(0,min(size,evt.x))

        if self._maximum > self._minimum:
            smin = self._minimum
            smax = self._maximum
            val  = int(0.5+smin+(smax-smin)*mouse/size)
            if val != self._value:
                self.setValue(val)
                self.sliderMoved.emit(self._value)
        return True


    '''
        ╞═══════════╬═════╡

    '''
    def paintEvent(self, canvas:TTkCanvas):
        style = self.currentStyle()
        color   = style['color']
        sliderColor   = style['sliderColor']

        if self._orientation == TTkK.VERTICAL:
            size=self._height-1
        else:
            size=self._width-1

        if self._maximum > self._minimum:
            smin = self._minimum
            smax = self._maximum
            sval = self._value
            sliderPos = int(0.5+size*(sval-smin)/(smax-smin))
        else:
            # Special case where no scroll is needed
            sliderPos = size//2

        if self._orientation == TTkK.VERTICAL:
            canvas.drawChar(pos=(0,0),char='┬',color=color)
            for y in range(1,size-sliderPos):
                canvas.drawChar(pos=(0,y),char='┊',color=color)
            if sliderPos>0:
                canvas.drawChar(pos=(0,size-sliderPos),char='╦',color=sliderColor)
                for y in range(size-sliderPos+1,size):
                    canvas.drawChar(pos=(0,y),char='║',color=sliderColor)
                canvas.drawChar(pos=(0,size),char='╨',color=sliderColor)
            else:
                canvas.drawTTkString(pos=(0,size),text=TTkString(f"╧",sliderColor))
        else:
            canvas.drawTTkString(pos=(0,0),text=TTkString(f"{'┄'*(size)}┤",color))
            if sliderPos>0:
                canvas.drawTTkString(pos=(0,0),text=TTkString(f"╞{'═'*(sliderPos-1)}╣",sliderColor))
            else:
                canvas.drawTTkString(pos=(0,0),text=TTkString(f"║",sliderColor))
