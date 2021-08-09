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
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor

class TTkString():
    __slots__ = ('_text','_colors')
    def __init__(self):
        self._text = ""
        self._colors = [TTkColor.RST]

    def __str__(self):
        return self._text

    def __add__(self, other):
        ret = TTkString()
        if   isinstance(other, TTkString):
            ret._text   += other._text
            ret._colors += other._colors
        elif isinstance(other, TTkColor):
            ret._colors[-1] = other
        elif isinstance(other, str):
            ret._text   += other
            ret._colors += [TTkColor.RST]*len(other)
        return ret

    def __radd__(self, other):
        ret = TTkString()
        if  isinstance(other, TTkString):
            ret._text   = other._text   + ret._text
            ret._colors = other._colors + ret._colors
        elif isinstance(other, str):
            ret._text   = other + ret._text
            ret._colors = [TTkColor.RST]*len(other) + ret._colors
        return ret

    def ansiString(self):
        out   = ""
        color = none
        for ch, col in zip(self._text, self._color):
            if col != color
                color = col
                out += str(color)
            out += ch
        return out
