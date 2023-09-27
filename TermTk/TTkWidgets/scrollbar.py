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

__all__ = ['TTkScrollBar']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget

'''
    ref: https://doc.qt.io/qt-5/qscrollbar.html
'''
class TTkScrollBar(TTkWidget):
    '''TTkScrollBar'''

    classStyle = {
                'default':     {'color': TTkColor.RST},
                'disabled':    {'color': TTkColor.fg('#888888')},
                'focus':       {'color': TTkColor.fg('#cccc00')},
            }

    __slots__ = (
        '_orientation',
        '_minimum', '_maximum',
        '_singleStep', '_pageStep',
        '_value',
        '_draggable', '_mouseDelta',
        # Those Vars are required to handle the mouseclick
        #  |-----|           Screen Pg Down
        #        |---|       Screen Scroller
        #            |-----| Screen Pg Up
        # <------|XXX|----->
        '_screenPgDown','_screenPgUp','_screenScroller',
        # Signals
        'valueChanged', 'rangeChanged', 'sliderMoved'
        )

    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        # Define Signals
        self.valueChanged = pyTTkSignal(int) #  Value
        self.rangeChanged = pyTTkSignal(int, int) # Min, Max
        self.sliderMoved  = pyTTkSignal(int) # Value

        self._orientation = kwargs.get('orientation' , TTkK.VERTICAL )
        if self._orientation == TTkK.VERTICAL:
            self.setMaximumWidth(1)
            self.setMinimumSize(1,3)
        else:
            self.setMaximumHeight(1)
            self.setMinimumSize(3,1)
        self._minimum = kwargs.get('minimum' , 0 )
        self._maximum = kwargs.get('maximum' , 99 )
        self._singleStep = kwargs.get('singleStep' , 1 )
        self._pageStep = kwargs.get('pageStep' , 10 )
        self._value = kwargs.get('value' , 0 )
        self._screenPgDown = (0,0)
        self._screenPgUp = (0,0)
        self._screenScroller = (0,0)
        self._draggable = False
        self._mouseDelta = 0
        self.setFocusPolicy(TTkK.ClickFocus)

    def orientation(self):
        return self._orientation

    '''
         | min        | max
        <-----XXXXX-------->   scrollbar
        |------------------|   size = widt or height
         |----------------|   size2 = widt or height - 2 (removed the ending arrows)
         |------------|     workingSize = max - min
         |----------------| drawingSize = max - min + pageStep
              a---b            slider = [a=value-min, b=a+pageStep]
              |---|            pageStep, asciiStep (step size in ascii)

    '''
    def paintEvent(self, canvas):
        style = self.currentStyle()
        color   = style['color']

        if self._orientation == TTkK.VERTICAL:
            size=self._height
        else:
            size=self._width

        if self._maximum == self._minimum:
            # Special case where no scroll is needed
            aa=0
            bb=size-2
        else:
            size2 = size-2
            asciiStep = size2 * self._pageStep // (self._maximum - self._minimum + self._pageStep)
            if asciiStep==0: asciiStep=1 # Force the slider to be at least one char wide
            asciiDrawingSize = size2 - asciiStep
            a = self._value - self._minimum
            # convert i screen coordinates
            aa = asciiDrawingSize * a // (self._maximum - self._minimum)
            bb = aa + asciiStep
        canvas.drawScroll(pos=(0,0),size=size,slider=(aa+1,bb+1),orientation=self._orientation, color=color)
        # Update the screen position coordinates
        self._screenPgDown =   ( 1 ,    aa+1     )
        self._screenScroller = ( aa+1 , bb+1)
        self._screenPgUp =     ( bb+1 , size-1 )
        # TTkLog.debug(f"aa:{aa} bb:{bb}, a:{a}, size2:{size2}")

    def wheelEvent(self, evt):
        if evt.evt == TTkK.WHEEL_Up:
            value = self._value-self._pageStep
        else:
            value = self._value+self._pageStep
        self.setValue(max(self._minimum,min(self._maximum,value)))
        self.sliderMoved.emit(self._value)
        return True

    def mousePressEvent(self, evt):
        if self._orientation == TTkK.VERTICAL:
            size=self._height
            mouse = evt.y
        else:
            size=self._width
            mouse = evt.x

        if mouse == 0: # left/up arrow pressed
            self.setValue(self._value - self._singleStep)
        elif mouse == size-1: # right/down arrow pressed
            self.setValue(self._value + self._singleStep)
        elif self._screenPgDown[0] <= mouse < self._screenPgDown[1]:
            self.setValue(self._value - self._pageStep)
        elif self._screenPgUp[0] <= mouse < self._screenPgUp[1]:
            self.setValue(self._value + self._pageStep)
        elif self._screenScroller[0] <= mouse < self._screenScroller[1]:
            self._mouseDelta = mouse-self._screenScroller[0]
            self._draggable = True
        else:
            return False
        self.setValue(max(self._minimum,min(self._maximum,self._value)))
        self.sliderMoved.emit(self._value)
        # TTkLog.debug(f"m={mouse}, md:{self._mouseDelta}, d:{self._screenPgDown},u:{self._screenPgUp},s:{self._screenScroller}")
        return True

    def mouseDragEvent(self, evt):
        if not self._draggable: return False
        if self._orientation == TTkK.VERTICAL:
            size=self._height
            mouse = evt.y
        else:
            size=self._width
            mouse = evt.x
        aa = mouse-self._mouseDelta

        size2 = size-2
        asciiStep = self._screenScroller[1] - self._screenScroller[0]
        asciiDrawingSize = size2 - asciiStep

        a =  aa * (self._maximum - self._minimum) // asciiDrawingSize

        self.setValue(max(self._minimum,min(self._maximum,a+self._minimum)))
        self.sliderMoved.emit(self._value)
        # TTkLog.debug(f"m={mouse}, md:{self._mouseDelta}, aa:{aa}")
        return True


    def focusInEvent(self):
        self.update()

    def focusOutEvent(self):
        self.update()

    def singleStep(self):
        '''singleStep'''
        return self._singleStep

    @pyTTkSlot(int)
    def setSingleStep(self, v):
        '''setSingleStep'''
        self._singleStep = v
        self.update()

    def pageStep(self):
        '''pageStep'''
        return self._pageStep

    @pyTTkSlot(int)
    def setPageStep(self, pageStep):
        '''setPageStep'''
        self._pageStep = pageStep
        self.update()

    @pyTTkSlot(int)
    def setRangeTo(self, max):
        '''setRangeTo'''
        self.setRange(0,max)

    @pyTTkSlot(int, int)
    def setRange(self, min, max):
        '''setRange'''
        if self._minimum == min and \
           self._maximum == max :
            return
        self._minimum = min
        self._maximum = max
        self.rangeChanged.emit(min, max)

    def minimum(self):
        return self._minimum

    def setMinimum(self, v):
        if v == self._minimum:
            return
        if v > self._maximum:
            v = self._maximum
        self._minimum = v
        self.update()

    def maximum(self):
        return self._maximum

    def setMaximum(self, v):
        if v == self._maximum:
            return
        if v < self._minimum:
            v = self._minimum
        self._maximum = v
        self.update()

    def value(self):
        return self._value

    @pyTTkSlot(int)
    def setValue(self, v):
        v = max(self._minimum,min(self._maximum,v))
        if self._value == v: return
        self._value = v
        self.valueChanged.emit(v)
        self.update()

    def color(self):
        return self._color

    def setColor(self, color):
        if self._color != color:
            self._color = color
            self.update()

    def focusColor(self):
        return self._focusColor

    def setFocusColor(self, color):
        if self._focusColor != color:
            self._focusColor = color
            self.update()
