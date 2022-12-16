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

import math

from TermTk.TTkCore.cfg       import TTkCfg
from TermTk.TTkCore.constant  import TTkK
from TermTk.TTkCore.string    import TTkString
from TermTk.TTkCore.signal    import pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkTemplates.lookandfeel import TTkLookAndFeel

class TTkLookAndFeelPBar(TTkLookAndFeel):
    def color(self, value, minimum, maximum):
        return TTkCfg.theme.progresssBarColor
    def text(self, value, minimum, maximum):
        percent = round(100*(value-minimum)/(maximum-minimum))
        return TTkString(f"{percent:3}%", color=TTkCfg.theme.progressBarTextColor)

'''
     Progressbar:  |████████▌      |
        rest block          ^
        full blocks ^^^^^^^^
'''
class TTkProgressBar(TTkWidget):
    __slots__ = (
        '_value', '_value_min', '_value_max', '_textWidth',
        # Signals
        'valueChanged')

    def __init__(self, *args, **kwargs):
        self.valueChanged = pyTTkSignal(float)
        TTkWidget.__init__(self, *args, **kwargs)
        self.setLookAndFeel(TTkLookAndFeelPBar())
        self._textWidth = kwargs.get('textWidth', 4)
        self._value_min, self._value_max, self._value = 0.0, 1.0, 0.0
        self.setMinimumMaximum(
            kwargs.get('minimum', 0.0), kwargs.get('maximum', 1.0))
        self.setValue(kwargs.get('value', 0.0))
        self.setMaximumHeight(1)
        self.setMinimumSize(3, 1)

    def value(self):
        return self._value

    def setValue(self, new_value):
        new_value = min(max(float(new_value), self._value_min), self._value_max)
        if new_value == self._value:
            return
        self._value = new_value
        self.valueChanged.emit(self._value)
        self.update()

    def minimum(self):
        return self._value_min

    def setMinimum(self, new_value):
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
        return self._value_max

    def setMaximum(self, new_value):
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
        return self._textWidth

    def setTextWidth(self, new_width):
        self._textWidth = max(0, new_width)

    def paintEvent(self):
        width, height = self.size()
        laf = self.lookAndFeel()
        text = laf.text(self._value, self._value_min, self._value_max)
        color_bar = laf.color(self._value, self._value_min, self._value_max)
        blocks = TTkCfg.theme.progressbarBlocks
        canvas = self._canvas
        show_text = (
            text is not None  and  self._textWidth > 0  and 
            width > 3 + self._textWidth)

        if show_text:
            width -= self._textWidth

        virt_width = 8 * width * (self._value - self._value_min)/(self._value_max - self._value_min)
        full = math.floor(virt_width // 8)
        rest = math.floor(virt_width - 8*full)

        canvas.drawText(pos=(0, 0), text='',   width=width, color=color_bar)
        if full:
            canvas.drawText(pos=(0, 0), text=blocks[8]*full, color=color_bar)
        if full < width:
            canvas.drawText(pos=(full, 0), text=blocks[rest], color=color_bar)
        if show_text:
            canvas.drawText(
                pos=(width, 0), text=text, width=self._textWidth,
                alignment=TTkK.RIGHT_ALIGN)

