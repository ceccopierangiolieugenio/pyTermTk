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
from TermTk.TTkCore.signal    import pyTTkSignal, pyTTkSlot
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkTemplates.lookandfeel import TTkLookAndFeel

class TTkLookAndFeelPBar(TTkLookAndFeel):
    def color(self, value, min, max):
        return TTkCfg.theme.progresssBarColor
    def text(self, value, min, max):
        percent = round(100*(value-min)/(max-min))
        return TTkString(f"{percent}%", color=TTkCfg.theme.progressBarTextColor)

'''
     Progressbar:  |████████▌      |
        rest block          ^
        full blocks ^^^^^^^^
'''
class TTkProgressBar(TTkWidget):
    __slots__ = (
        '_value', '_minimum', '_maximum',
        # Signals
        'valueChanged')

    def __init__(self, *args, **kwargs):
        self.valueChanged = pyTTkSignal(float)
        TTkWidget.__init__(self, *args, **kwargs)
        self.setLookAndFeel(TTkLookAndFeelPBar())
        self._minimum = float(kwargs.get('minimum', 0.0))
        self._maximum = float(kwargs.get('maximum', 1.0))
        self._value = float(kwargs.get('value', 0.0))
        self._value = min(max(self._value, self._minimum), self._maximum)
        self.setMaximumHeight(1)
        self.setMinimumSize(3, 1)

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum

    def value(self):
        return self._value

    @pyTTkSlot(int)
    def setValue(self, value):
        self._value = min(max(float(value), self._minimum), self._maximum)
        self.valueChanged.emit(self._value)
        self.update()

    def paintEvent(self):
        width, height = self.size()
        text = self.lookAndFeel().text(self._value, self._minimum, self._maximum)
        color_bar = self.lookAndFeel().color(self._value, self._minimum, self._maximum)
        blocks = TTkCfg.theme.progressbarBlocks
        canvas = self._canvas

        virt_width = 8 * width * (self._value - self._minimum)/(self._maximum - self._minimum)
        full = math.floor(virt_width // 8)
        rest = math.floor(virt_width - 8*full)

        canvas.drawText(pos=(0, 0), text='',   width=width, color=color_bar)
        if full:
            canvas.drawText(pos=(0, 0), text=text, width=full,color=color_bar.invertFgBg(), alignment=TTkK.CENTER_ALIGN)
        if full < width:
            canvas.drawText(pos=(full, 0), text=blocks[rest], color=color_bar)




