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

import re

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor, _TTkColor


class TTkString:
    """TermTk String Helper

    The TTkString constructor creates a terminal String object.

    :param text: text of the string, defaults to ""
    :type text: str, optional
    :param color: the color of the string, defaults to :class:`~TermTk.TTkCore.color.TTkColor.RST`
    :type color: :class:`~TermTk.TTkCore.color.TTkColor`, optional

    Example:

    .. code:: python

        # No params Constructor
        str1 = TTkString() + "test 1"
        str2 = TTkString() + TTkColor.BOLD + "test 2"

        # Indexed params constructor
        str3 = TTkString("test 3")
        str4 = TTkString("test 4", TTkColor.ITALIC)

        # Named params constructor
        str5 = TTkString(text="test 5")
        str6 = TTkString(text="test 6", color=TTkColor.ITALIC+TTkColor.bg("000044"))

        # Combination of constructors (Highly Unrecommended)
        str7 = TTkString("test 7", color=TTkColor.fg('#FF0000'))
    """

    __slots__ = ("_text", "_colors", "_baseColor")

    def __init__(self, text="", color=TTkColor.RST):
        self._text = text
        self._baseColor = color
        self._colors = [self._baseColor] * len(self._text)

    def __len__(self):
        return len(self._text)

    def __str__(self):
        return self._text

    def __add__(self, other):
        ret = TTkString()
        ret._baseColor = self._baseColor
        if isinstance(other, TTkString):
            ret._text = self._text + other._text
            ret._colors = self._colors + other._colors
        elif isinstance(other, str):
            ret._text = self._text + other
            ret._colors = self._colors + [self._baseColor] * len(other)
        elif isinstance(other, _TTkColor):
            ret._text = self._text
            ret._colors = self._colors
            ret._baseColor = other
        return ret

    def __radd__(self, other):
        ret = TTkString()
        ret._baseColor = self._baseColor
        if isinstance(other, TTkString):
            ret._text = other._text + self._text
            ret._colors = other._colors + self._colors
        elif isinstance(other, str):
            ret._text = other + self._text
            ret._colors = [self._baseColor] * len(other) + self._colors
        return ret

    def __setitem__(self, index, value):
        raise NotImplementedError()

    def __getitem__(self, index):
        raise NotImplementedError()

    # Operators
    def __lt__(self, other):
        return self._text < other._text

    def __le__(self, other):
        return self._text <= other._text

    def __eq__(self, other):
        return self._text == other._text

    def __ne__(self, other):
        return self._text != other._text

    def __gt__(self, other):
        return self._text > other._text

    def __ge__(self, other):
        return self._text >= other._text

    def toAscii(self):
        """Return the ascii representation of the string"""
        return self._text

    def toAansi(self):
        """Return the ansii (terminal colors/events) representation of the string"""
        out = ""
        color = None
        for ch, col in zip(self._text, self._colors):
            if col != color:
                color = col
                out += str(TTkColor.RST) + str(color)
            out += ch
        return out

    def align(self, width=None, color=TTkColor.RST, alignment=TTkK.NONE):
        """Align the string

        :param width: the new width
        :type width: int, optional
        :param color: the color of the padding, defaults to :class:`~TermTk.TTkCore.color.TTkColor.RST`
        :type color: :class:`~TermTk.TTkCore.color.TTkColor`, optional
        :param alignment: the alignment of the text to the full width :class:`~TermTk.TTkCore.constant.TTkConstant.Alignment.NONE`
        :type alignment: :class:`~TermTk.TTkCore.constant.TTkConstant.Alignment`, optional
        """
        lentxt = len(self._text)
        if not width or width == lentxt:
            return self

        ret = TTkString()

        if lentxt < width:
            pad = width - lentxt
            if alignment in [TTkK.NONE, TTkK.LEFT_ALIGN]:
                ret._text = self._text + " " * pad
                ret._colors = self._colors + [color] * pad
            elif alignment == TTkK.RIGHT_ALIGN:
                ret._text = " " * pad + self._text
                ret._colors = [color] * pad + self._colors
            elif alignment == TTkK.CENTER_ALIGN:
                p1 = pad // 2
                p2 = pad - p1
                ret._text = " " * p1 + self._text + " " * p2
                ret._colors = [color] * p1 + self._colors + [color] * p2
            elif alignment == TTkK.JUSTIFY:
                # TODO: Text Justification
                ret._text = self._text + " " * pad
                ret._colors = self._colors + [color] * pad
        else:
            ret._text = self._text[:width]
            ret._colors = self._colors[:width]

        return ret

    def replace(self, *args, **kwargs):
        """**replace** (*old*, *new*, *count*)

        Replace "**old**" match with "**new**" string for "**count**" times

        :param old: the match to be placed
        :type old: str
        :param new: the match to replace
        :type new: str, optional
        :param count: the number of occurrences
        :type count: int, optional
        """
        old = args[0]
        new = args[1]
        count = args[2] if len(args) == 3 else 0x1000000

        if old not in self._text:
            return self

        oldLen = len(old)
        newLen = len(new)

        ret = TTkString()
        if oldLen == newLen:
            ret._colors += self._colors
            ret._text = self._text.replace(*args, **kwargs)
        elif oldLen > newLen:
            start = 0
            while (
                pos := self._text.index(old, start)
                if old in self._text[start:]
                else None
            ):
                ret._colors += self._colors[start : pos + newLen]
                start = pos + oldLen
                count -= 1
                if count == 0:
                    break
            ret._colors += self._colors[start:]
            ret._text = self._text.replace(*args, **kwargs)
        else:
            start = 0
            oldPos = 0
            while (
                pos := self._text.index(old, start)
                if old in self._text[start:]
                else None
            ):
                ret._colors += self._colors[start : pos + oldLen] + [
                    self._colors[pos + oldLen - 1]
                ] * (newLen - oldLen)
                start = pos + oldLen
                if count == 0:
                    break
            ret._colors += self._colors[start:]
            ret._text = self._text.replace(*args, **kwargs)

        return ret

    def setColor(self, color, match=None, posFrom=None, posTo=None):
        """Set the color of the entire string or a slice of it

        If only the color is specified, the entore sting is colorized

        :param color: the color to be used, defaults to :class:`~TermTk.TTkCore.color.TTkColor.RST`
        :type color: :class:`~TermTk.TTkCore.color.TTkColor`
        :param match: the match to colorize
        :type match: str, optional
        :param posFrom: the initial position of the color
        :type posFrom: int, optional
        :param posTo: the final position of the color
        :type posTo: int, optional
        """
        ret = TTkString()
        ret._text += self._text
        if match:
            ret._colors += self._colors
            start = 0
            lenMatch = len(match)
            while (
                pos := self._text.index(match, start)
                if match in self._text[start:]
                else None
            ):
                start = pos + lenMatch
                for i in range(pos, pos + lenMatch):
                    ret._colors[i] = color
        elif posFrom == posTo == None:
            ret._colors = [color] * len(self._text)
        elif posFrom < posTo:
            ret._colors += self._colors
            for i in range(posFrom, posTo):
                ret._colors[i] = color
        else:
            ret._colors += self._colors
        return ret

    def substring(self, fr=None, to=None):
        """Return the substring

        :param fr: the starting of the slice, defaults to 0
        :type fr: int, optional
        :param to: the ending of the slice, defaults to the end of the string
        :type to: int, optional
        """
        ret = TTkString()
        ret._text = self._text[fr:to]
        ret._colors = self._colors[fr:to]
        return ret

    def split(self, separator):
        """Split the string using a separator

        .. note:: Only a one char separator is currently supported

        :param separator: the "**char**" separator to be used
        :type separator: str
        """
        ret = []
        pos = 0
        if len(separator) == 1:
            for i, c in enumerate(self._text):
                if c == separator:
                    ret.append(self.substring(pos, i))
                    pos = i + 1
        else:
            raise NotImplementedError(
                "Not yet implemented separators bigger than one char"
            )
        ret.append(self.substring(pos, len(self)))

        return ret

    def getData(self):
        return (self._text, self._colors)

    def search(self, regexp, ignoreCase=False):
        """Return the **re.match** of the **regexp**

        :param regexp: the regular expression to be matched
        :type regexp: str
        :param ignoreCase: Ignore case, defaults to **False**
        :type ignoreCase: bool
        """
        return re.search(regexp, self._text, re.IGNORECASE if ignoreCase else 0)

    def findall(self, regexp, ignoreCase=False):
        """FindAll the **regexp** matches in the string

        :param regexp: the regular expression to be matched
        :type regexp: str
        :param ignoreCase: Ignore case, defaults to **False**
        :type ignoreCase: bool
        """
        return re.findall(regexp, self._text, re.IGNORECASE if ignoreCase else 0)

    def getIndexes(self, char):
        return [i for i, c in enumerate(self._text) if c == char]

    def join(self, strings):
        """Join the input strings using the current as separator

        :param strings: the list of strings to be joined
        :type strings: list
        """
        if not strings:
            return TTkString()
        ret = TTkString() + strings[0]
        for s in strings[1:]:
            ret += self + s
        return ret
