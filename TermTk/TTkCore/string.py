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

from hashlib import new
import re

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor, _TTkColor

class TTkString():
    __slots__ = ('_text','_colors','_baseColor')
    def __init__(self):
        self._baseColor = TTkColor.RST
        self._text = ""
        self._colors = []

    def __len__(self):
        return len(self._text)

    def __str__(self):
        return self._text

    def __add__(self, other):
        ret = TTkString()
        ret._baseColor = self._baseColor
        if   isinstance(other, TTkString):
            ret._text   = self._text   + other._text
            ret._colors = self._colors + other._colors
        elif isinstance(other, str):
            ret._text   = self._text   + other
            ret._colors = self._colors + [self._baseColor]*len(other)
        elif isinstance(other, _TTkColor):
            ret._text   = self._text
            ret._colors = self._colors
            ret._baseColor = other
        return ret

    def __radd__(self, other):
        ret = TTkString()
        ret._baseColor = self._baseColor
        if  isinstance(other, TTkString):
            ret._text   = other._text   + self._text
            ret._colors = other._colors + self._colors
        elif isinstance(other, str):
            ret._text   = other + self._text
            ret._colors = [self._baseColor]*len(other) + self._colors
        return ret

    def __setitem__(self, index, value):
        raise NotImplementedError()

    def __getitem__(self, index):
        raise NotImplementedError()

    # Operators
    def __lt__(self, other): return self._text <  other._text
    def __le__(self, other): return self._text <= other._text
    def __eq__(self, other): return self._text == other._text
    def __ne__(self, other): return self._text != other._text
    def __gt__(self, other): return self._text >  other._text
    def __ge__(self, other): return self._text >= other._text

    def toAscii(self):
        return self._text

    def toAansi(self):
        out   = ""
        color = None
        for ch, col in zip(self._text, self._colors):
            if col != color:
                color = col
                out += str(TTkColor.RST) + str(color)
            out += ch
        return out

    def align(self, width=None, color=TTkColor.RST, alignment=TTkK.NONE):
        lentxt = len(self._text)
        if not width or width == lentxt: return self

        ret = TTkString()

        if lentxt < width:
            pad = width-lentxt
            if alignment in [TTkK.NONE, TTkK.LEFT_ALIGN]:
                ret._text   = self._text   + " "    *pad
                ret._colors = self._colors + [color]*pad
            elif alignment == TTkK.RIGHT_ALIGN:
                ret._text   = " "    *pad + self._text
                ret._colors = [color]*pad + self._colors
            elif alignment == TTkK.CENTER_ALIGN:
                p1 = pad//2
                p2 = pad-p1
                ret._text   = " "    *p1 + self._text   + " "    *p2
                ret._colors = [color]*p1 + self._colors + [color]*p2
            elif alignment == TTkK.JUSTIFY:
                # TODO: Text Justification
                ret._text   = self._text   + " "    *pad
                ret._colors = self._colors + [color]*pad
        else:
            ret._text   =  self._text[:width]
            ret._colors =  self._colors[:width]

        return ret

    def replace(self, *args, **kwargs):
        old = args[0]
        new = args[1]
        count = args[2] if len(args)==3 else 0x1000000

        if old not in self._text: return self

        oldLen = len(old)
        newLen = len(new)

        ret = TTkString()
        if oldLen == newLen:
            ret._colors += self._colors
            ret._text   = self._text.replace(*args, **kwargs)
        elif oldLen > newLen:
            start = 0
            while pos := self._text.index(old, start) if old in self._text[start:] else None:
                ret._colors += self._colors[start:pos+newLen]
                start = pos+oldLen
                count -= 1
                if count == 0: break
            ret._colors += self._colors[start:]
            ret._text   = self._text.replace(*args, **kwargs)
        else:
            start = 0
            oldPos=0
            while pos := self._text.index(old, start) if old in self._text[start:] else None:
                ret._colors += self._colors[start:pos+oldLen] + [self._colors[pos+oldLen-1]]*(newLen-oldLen)
                start = pos+oldLen
                if count == 0: break
            ret._colors += self._colors[start:]
            ret._text   = self._text.replace(*args, **kwargs)

        return ret

    def setColor(self, color, match=None, posFrom=0, posTo=0):
        ret = TTkString()
        ret._text   += self._text
        if match:
            ret._colors += self._colors
            start=0
            lenMatch = len(match)
            while pos := self._text.index(match, start) if match in self._text[start:] else None:
                start = pos+lenMatch
                for i in range(pos, pos+lenMatch):
                    ret._colors[i] = color
        elif posFrom < posTo:
            ret._colors += self._colors
            for i in range(posFrom, posTo):
                ret._colors[i] = color
        else:
            ret._colors = [color]*len(self._text)
        return ret

    def substring(self, fr=None, to=None):
        ret = TTkString()
        ret._text   = self._text[fr:to]
        ret._colors = self._colors[fr:to]
        return ret



    def getData(self):
        return (self._text,self._colors)

    def search(self, regexp, ignoreCase=False):
        return re.search(regexp, self._text, re.IGNORECASE if ignoreCase else 0)

    def findall(self, regexp, ignoreCase=False):
        return re.findall(regexp, self._text, re.IGNORECASE if ignoreCase else 0)