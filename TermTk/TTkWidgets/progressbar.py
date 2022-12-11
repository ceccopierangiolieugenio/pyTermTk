#!/usr/bin/env python3

import math

from TermTk.TTkCore.cfg       import TTkCfg
from TermTk.TTkCore.constant  import TTkK
from TermTk.TTkCore.string    import TTkString
from TermTk.TTkCore.signal    import pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget

def default_look_and_feel(bar):
    '''return (text, color_bar) for progressbar's state.'''

    vmin, vmax, value = bar.value_min, bar.value_max, bar.value
    percent = round(100*(value-vmin)/(vmax-vmin))
    text = TTkString(f"{percent}%", color=TTkCfg.theme.progressBarTextColor)
    return (text, TTkCfg.theme.progresssBarColor)


'''
     Progressbar:  |████████▌      |
        rest block          ^
        full blocks ^^^^^^^^
'''
class TTkProgressBar(TTkWidget):
    __slots__ = (
        '_value', '_value_min', '_value_max',
        '_look_and_feel',
        # Signals
        'valueChanged')

    def __init__(self, *args, **kwargs):
        self.valueChanged = pyTTkSignal(float)
        TTkWidget.__init__(self, *args, **kwargs)
        self._value_min = float(kwargs.get('value_min', 0.0))
        self._value_max = float(kwargs.get('value_max', 1.0))
        self._value = float(kwargs.get('value', 0.0))
        if not (self._value_min <= self._value <= self._value_max):
            self._value = self._value_min
        self._look_and_feel = kwargs.get('look_and_feel', None)
        if self._look_and_feel is None:
            self._look_and_feel = default_look_and_feel
        self.setMaximumHeight(1)
        self.setMinimumSize(3, 1)

    @property
    def value_min(self):
        return self._value_min

    @property
    def value_max(self):
        return self._value_max

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = min(max(float(value), self._value_min), self._value_max)
        self.valueChanged.emit(self._value)
        self.update()

    def paintEvent(self):
        width, height = self.size()
        text, color_bar = self._look_and_feel(self)
        blocks = TTkCfg.theme.progressbarBlocks
        canvas = self._canvas

        virt_width = 8 * width * (self._value - self._value_min)/(self._value_max - self._value_min)
        full = math.floor(virt_width // 8)
        rest = math.floor(virt_width - 8*full)

        if text is not None and text.termWidth() <= full:
            pad = full - text.termWidth()
            pad1 = pad//2
            full_part = (
                TTkString(blocks[8]*pad1, color=color_bar) + text +
                TTkString(blocks[8]*(pad-pad1), color=color_bar))
        else:
            full_part = TTkString(blocks[8]*full, color=color_bar)

        canvas.drawText(pos=(0, 0), text=full_part)
        if full < width:
            canvas.drawText(pos=(full, 0), text=blocks[rest], color=color_bar)
        if full + 1 < width:
            canvas.drawText(pos=(full+1, 0), text=' '*(width-full-1), color=color_bar)




