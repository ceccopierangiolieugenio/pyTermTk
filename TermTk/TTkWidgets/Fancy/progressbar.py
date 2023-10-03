# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#                    Luchr          <https://github.com/luchr>
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

__all__ = ['TTkFancyProgressBar', 'TTkLookAndFeelFPBar']

import math

from TermTk.TTkCore.cfg       import TTkCfg
from TermTk.TTkCore.color     import TTkColor
from TermTk.TTkCore.constant  import TTkK
from TermTk.TTkCore.string    import TTkString
from TermTk.TTkCore.signal    import pyTTkSignal, pyTTkSlot
from TermTk.TTkWidgets.widget import TTkWidget

class TTkLookAndFeel():
    __slots__ = ('modified')
    def __init__(self, *args, **kwargs):
        self.modified = pyTTkSignal()

class TTkLookAndFeelFPBar(TTkLookAndFeel):
    progresssBarColor = TTkColor.fg('#0000aa')+TTkColor.bg("#000044")
    progressBarTextColor = TTkColor.fg('#ffffff')

    __slots__ = ('_textWidth', '_showText')
    def __init__(self, showText=True, textWidth=4):
        super().__init__()
        self._textWidth = textWidth
        self._showText = showText

    def showText(self):
        return self._showText

    @pyTTkSlot(bool)
    def setShowText(self, st):
        if st == self._showText: return
        self._showText = st
        self.modified.emit()

    def textWidth(self):
        return self._textWidth

    @pyTTkSlot(int)
    def setTextWidth(self, tw):
        if tw == self._textWidth: return
        self._textWidth = tw
        self.modified.emit()

    def color(self, value, minimum, maximum):
        return self.progresssBarColor

    def text(self, value, minimum, maximum):
        percent = round(100*(value-minimum)/(maximum-minimum))
        return TTkString(f"{percent:3}%", color=self.progressBarTextColor)

'''
     Progressbar:  |████████▌      |
        rest block          ^
        full blocks ^^^^^^^^
'''
class TTkFancyProgressBar(TTkWidget):
    '''TTkFancyProgressBar'''

    __slots__ = (
        '_lookAndFeel',
        '_value', '_minimum', '_maximum',
        # Signals
        'valueChanged')

    def __init__(self, *args, **kwargs):
        self.valueChanged = pyTTkSignal(float)
        TTkWidget.__init__(self, *args, **kwargs)
        self._lookAndFeel = kwargs.get('lookAndFeel',TTkLookAndFeelFPBar())
        self._lookAndFeel.modified.connect(self.update)
        self._value_min, self._value_max, self._value = 0.0, 1.0, 0.0
        self.setValue(kwargs.get('value', 0.0))
        self.setMinimumSize(3, 1)

    def value(self):
        '''value'''
        return self._value

    @pyTTkSlot(float)
    def setValue(self, new_value):
        '''setValue'''
        new_value = min(max(float(new_value), self._value_min), self._value_max)
        if new_value == self._value:
            return
        self._value = new_value
        self.valueChanged.emit(self._value)
        self.update()

    def minimum(self):
        '''minimum'''
        return self._value_min

    def setMinimum(self, new_value):
        '''setMinimum'''
        if not math.isfinite(new_value):
            raise ValueError(f'minimum must be finite, but value was {new_value}')
        if not new_value < self._value_max:
            raise ValueError(
                f'new minimum {new_value} was not smaller '
                f'than maximum {self._value_max}')
        self._value_min = float(new_value)
        if self._value < self._value_min:
            self.setValue(self._value_min)

    def maximum(self):
        '''maximum'''
        return self._value_max

    def setMaximum(self, new_value):
        '''setMaximum'''
        if not math.isfinite(new_value):
            raise ValueError(f'maximum must be finite, but value was {new_value}')
        if not new_value > self._value_min:
            raise ValueError(
                f'new maximum {new_value} was not larger '
                f'than minimum {self._value_min}')
        self._value_max = float(new_value)
        if self._value > self._value_max:
            self.setValue(self._value_max)

    def setMinimumMaximum(self, new_min, new_max):
        '''setMinimumMaximum'''
        if not math.isfinite(new_min) or not math.isfinite(new_max):
            raise ValueError(
                f'minimum and maximum must be finite, but '
                f'found {new_min} and {new_max}')
        if not new_min < new_max:
            raise ValueError(
                f'minimum must be smaller thatn maximum, but '
                f'found {new_min} and {new_max}')
        self._value_min, self._value_max = new_min, new_max
        if not self._value_min <= self._value <= self._value_max:
            self.setValue(self._value) # setValue takes care for min/max-constraint

    def textWidth(self):
        '''textWidth'''
        return self._textWidth

    def setTextWidth(self, new_width):
        '''setTextWidth'''
        self._textWidth = max(0, new_width)

    def paintEvent(self, canvas):
        width, height = self.size()
        laf = self._lookAndFeel
        text = laf.text(self._value, self._value_min, self._value_max)
        color_bar = laf.color(self._value, self._value_min, self._value_max)
        blocks = TTkCfg.theme.progressbarBlocks
        show_text = laf.showText()

        if show_text:
            width -= laf.textWidth()
            width = max(width, 0)

        virt_width = 8 * width * (self._value - self._value_min)/(self._value_max - self._value_min)
        full = math.floor(virt_width // 8)
        rest = math.floor(virt_width - 8*full)

        for y in range(height):
            color_bar = color_bar.modParam(step=width)
            bar = TTkString((blocks[8]*full)+blocks[rest], color_bar)
            canvas.drawText(pos=(0, y), text=bar, width=width, color=color_bar)
        if show_text:
            canvas.drawText(
                pos=(width, (height-1)//2), text=text, width=laf.textWidth(),
                alignment=TTkK.RIGHT_ALIGN)

