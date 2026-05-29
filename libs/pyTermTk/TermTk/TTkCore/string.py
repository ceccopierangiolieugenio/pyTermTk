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

from __future__ import annotations

__all__ = ['TTkString','TTkStringType']

import os
import re
import unicodedata
from types import GeneratorType
from typing import Any, Optional, Union, List, Tuple

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor

class TTkString():
    ''' TermTk String Helper

    The TTkString constructor creates a terminal String object.

    :param text: text of the string, defaults to ""
    :type text: str, optional
    :param color: the color of the string, defaults to :py:class:`TTkColor.RST`
    :type color: :py:class:`TTkColor`, optional

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
    '''
    mnemonicColor = TTkColor.fg("#dddddd") + TTkColor.UNDERLINE
    unicodeWideOverflowColor = TTkColor.fg("#888888")+TTkColor.bg("#000088")

    __slots__ = ('_text','_colors','_baseColor','_hasTab','_hasSpecialWidth')
    _text:str
    _colors:List[TTkColor]
    _baseColor:TTkColor
    def __init__(self,
                 text:Union[str,TTkString]="",
                 color:Optional[TTkColor]=None) -> None:
        if isinstance(text, TTkString):
            self._text      = text._text
            self._colors    = text._colors if color is None else [color]*len(self._text)
            self._baseColor = text._baseColor
        else:
            self._baseColor = TTkColor.RST if color is None else color
            self._text, self._colors = TTkString._parseAnsi(str(text), self._baseColor)
        self._hasTab = '\t' in self._text
        self._checkWidth()
        # raise AttributeError(f"{type(text)} not supported in TTkString")

    @staticmethod
    def _importString1(text, colors:List[TTkColor]):
        ret = TTkString()
        if text and colors:
            ret._text = text
            ret._colors = colors
            ret._baseColor = colors[-1] if colors else TTkColor.RST
            ret._hasTab = '\t' in text
            ret._checkWidth()
        return ret

    @staticmethod
    def _parseAnsi(text, color:TTkColor = TTkColor.RST):
        pos = 0
        txtret = ""
        colret = []
        for m in re.findall('\033[^m]*m', text):
            index = text.index(m,pos)
            txt = text[pos:index]
            txtret += txt
            colret += [color]*len(txt)
            color+=TTkColor.ansi(m)
            pos = index+len(m)
        txtret += text[pos:]
        colret += [color]*(len(text)-pos)
        return txtret, colret

    def termWidth(self) -> int:
        '''Return the rendered terminal width of this string.

        :return: rendered width accounting for tabs and wide/combining chars
        :rtype: int
        '''
        return self._hasSpecialWidth if self._hasSpecialWidth is not None else len(self)

    def __len__(self) -> int:
        return len(self._text)

    def __str__(self) -> str:
        return self._text

    def __add__(self, other:Union[TTkStringType,TTkColor]) -> TTkString:
        ret = TTkString()
        ret._baseColor = self._baseColor
        if   isinstance(other, TTkString):
            ret._text   = self._text   + other._text
            ret._colors = self._colors + other._colors
            ret._hasTab = '\t' in ret._text
            ret._fastCheckWidth(self._hasSpecialWidth, other._hasSpecialWidth)
        elif isinstance(other, str):
            atxt, acol = TTkString._parseAnsi(other, self._baseColor)
            ret._text   = self._text   + atxt
            ret._colors = self._colors + acol
            ret._hasTab = '\t' in ret._text
            ret._checkWidth()
        elif isinstance(other, TTkColor):
            ret._text   = self._text
            ret._colors = self._colors
            ret._hasSpecialWidth = self._hasSpecialWidth
            ret._hasTab = self._hasTab
            ret._baseColor = other
        return ret

    def __radd__(self, other:TTkStringType) -> TTkString:
        ret = TTkString()
        ret._baseColor = self._baseColor
        if  isinstance(other, TTkString):
            ret._text   = other._text   + self._text
            ret._colors = other._colors + self._colors
            ret._hasTab = '\t' in ret._text
            ret._fastCheckWidth(self._hasSpecialWidth, other._hasSpecialWidth)
        elif isinstance(other, str):
            ret._text   = other + self._text
            ret._colors = [self._baseColor]*len(other) + self._colors
            ret._hasTab = '\t' in ret._text
            ret._checkWidth()
        return ret

    def __setitem__(self, index:int, value:Any) -> None:
        raise NotImplementedError()

    def __getitem__(self, index:int) -> Any:
        raise NotImplementedError()

    def __bool__(self) -> bool:
        return bool(self._text)
    def __int__(self) -> int:
        return int(self._text)
    def __float__(self) -> float:
        return float(self._text)
    def __complex__(self) -> complex:
        return complex(self._text)

    # Operators
    def __lt__(self, other:TTkStringType) -> bool:
        return self._text < other._text if isinstance(other, TTkString) else self._text < other

    def __le__(self, other:TTkStringType) -> bool:
        return self._text <= other._text if isinstance(other, TTkString) else self._text <= other

    def __eq__(self, other:object) -> bool:
        if isinstance(other, TTkString):
            return self._text == other._text
        return self._text == other

    def __ne__(self, other:object) -> bool:
        if isinstance(other, TTkString):
            return self._text != other._text
        return self._text != other

    def __gt__(self, other:TTkStringType) -> bool:
        return self._text > other._text if isinstance(other, TTkString) else self._text > other

    def __ge__(self, other:TTkStringType) -> bool:
        return self._text >= other._text if isinstance(other, TTkString) else self._text >= other

    def sameAs(self, other:TTkStringType) -> bool:
        '''Check whether text and per-character colors are identical.

        :param other: string to compare against
        :type other: :py:class:`TTkString` | str

        :return: True when text and colors match exactly
        :rtype: bool
        '''
        if not isinstance(other,TTkString): return False
        return (
            self==other and
            len(self._colors) == len(other._colors) and
            all(s==o for s,o in zip(self._colors,other._colors)) )

    def isdigit(self) -> bool:
        '''Check whether the string contains only digit characters.

        :return: True if all characters are digits and the string is non-empty
        :rtype: bool
        '''
        return self._text.isdigit()

    def lstrip(self, ch:str) -> TTkString:
        '''Return a copy with leading characters removed.

        :param ch: characters to strip from the left side
        :type ch: str

        :return: left-stripped string preserving color alignment
        :rtype: :py:class:`TTkString`
        '''
        ret = TTkString()
        ret._text = self._text.lstrip(ch)
        ret._colors = self._colors[-len(ret._text):]
        ret._checkWidth()
        return ret

    def charAt(self, pos:int) -> str:
        '''Return the character at the given position.

        :param pos: character index
        :type pos: int

        :return: character at ``pos``
        :rtype: str
        '''
        return self._text[pos]

    def setCharAt(self, pos:int, char:str) -> TTkString:
        '''Return a copy with one character replaced.

        :param pos: character index to replace
        :type pos: int
        :param char: replacement character
        :type char: str

        :return: updated string
        :rtype: :py:class:`TTkString`

        :raises IndexError: if ``pos`` is out of range
        '''
        if not (0 <= pos < len(self._text)):
            raise IndexError()
        ret = TTkString()
        ret._text = self._text[:pos]+char+self._text[pos+1:]
        ret._colors = self._colors
        ret._checkWidth()
        return ret

    def colorAt(self, pos:int) -> TTkColor:
        '''Return the color assigned to the character at ``pos``.

        :param pos: character index
        :type pos: int

        :return: color at ``pos`` or :py:class:`TTkColor.RST` when out of range
        :rtype: :py:class:`TTkColor`
        '''
        if pos >= len(self._colors):
            return TTkColor.RST
        return self._colors[pos]

    def setColorAt(self, pos:int, color:TTkColor) -> TTkString:
        '''Return a copy with one character color replaced.

        :param pos: character index to recolor
        :type pos: int
        :param color: replacement color
        :type color: :py:class:`TTkColor`

        :return: recolored string
        :rtype: :py:class:`TTkString`

        :raises IndexError: if ``pos`` is out of range
        '''
        if not (0 <= pos < len(self._colors)):
            raise IndexError()
        ret = TTkString()
        ret._text = self._text
        ret._colors = [*self._colors[:pos], color, *self._colors[pos+1:]]
        ret._hasSpecialWidth = self._hasSpecialWidth
        return ret

    def tab2spaces(self, tabSpaces:int=4) -> TTkString:
        '''Expand tab characters into aligned spaces.

        :param tabSpaces: tab stop size
        :type tabSpaces: int

        :return: string with tabs replaced by spaces
        :rtype: :py:class:`TTkString`
        '''
        if not self._hasTab: return self
        ret = TTkString()
        slices = self._text.split("\t")
        ret._text += slices[0]
        pos = len(slices[0])
        ret._colors += self._colors[0:pos]
        for s in slices[1:]:
            c  = self._colors[pos]
            lentxt = ret.termWidth()
            spaces = tabSpaces - (lentxt+tabSpaces)%tabSpaces
            ret._text   += " "*spaces + s
            ret._colors += [c]*spaces + self._colors[pos+1:pos+1+len(s)]
            ret._fastCheckWidth(self._hasSpecialWidth)
            pos+=len(s)+1
        return ret

    def tabCharPos(self, pos:int, tabSpaces:int=4, alignTabRight:bool=False) -> int:
        '''Map a rendered column position to the internal character index.

        Tabs and variable-width characters are resolved against the visual
        terminal representation.

        :param pos: target visual column
        :type pos: int
        :param tabSpaces: tab stop size
        :type tabSpaces: int
        :param alignTabRight: map positions inside a tab to the tab right edge
        :type alignTabRight: bool

        :return: character index in ``_text``
        :rtype: int

        i.e.

        ::

            pos                   X = 11
            tab2Spaces |----------|---------------------|
            Tabs             |-|  |  |-|     |-|   |
            _text      L😁rem   ipsum   dolor   sit amet,
            chars      .. ...t  .....t  .....t  ...t.....
            ret                   x = 7 (tab is a char)

        '''
        if not self._hasTab and self._hasSpecialWidth is None: return max(0,min(pos,len(self._text)))
        if self._hasSpecialWidth is not None:
            return self._tabCharPosWideChar(pos, tabSpaces, alignTabRight)
        slices = self._text.split("\t")
        postxt = 0 # position of the text
        lentxt = 0 # length of the text with resolved tabs
        for s in slices:
            lens   = len(s)
            lentxt += lens
            postxt += lens
            if pos<=postxt:
                return pos
            spaces = tabSpaces - (lentxt+tabSpaces)%tabSpaces
            if pos < postxt+spaces:
                if alignTabRight:
                    return postxt+1
                else:
                    return postxt
            pos += 1-spaces
            lentxt += spaces
            postxt += 1
        return len(self._text)

    def _tabCharPosWideChar(self, pos:int, tabSpaces:int=4, alignTabRight:bool=False) -> int:
        '''Wide-char aware implementation for :py:meth:`tabCharPos`.

        i.e.

        ::

            pos                   X = 11
            tab2Spaces |----------|---------------------|
            Tabs             |-|  |  |-|     |-|   |
            _text      L😁rem   ipsum   dolor   sit amet,
            chars      .. ...t  .....t  .....t  ...t.....
            ret                   x = 7 (tab is a char)

        :param pos: target visual column
        :type pos: int
        :param tabSpaces: tab stop size
        :type tabSpaces: int
        :param alignTabRight: unused in this implementation
        :type alignTabRight: bool

        :return: character index in ``_text``
        :rtype: int
        '''
        # get pos in the slice:
        dx = pos
        pp = 0
        for i,ch in enumerate(self._text):
            if ch=='\t':
                pp += tabSpaces - (pp+tabSpaces)%tabSpaces
            elif unicodedata.east_asian_width(ch) == 'W':
                pp += 2
            elif unicodedata.category(ch) in ('Me','Mn'):
                pass
            else:
                pp += 1
            if dx < pp:
                return i
        return len(self._text)

    def isPlainText(self) -> bool:
        '''Return True if the string has no color/style information.

        :return: True when all chars use :py:class:`TTkColor.RST`
        :rtype: bool
        '''
        return all(TTkColor.RST == c for c in self._colors)

    def toAscii(self) -> str:
        '''Return the plain-text content.

        :return: raw text without terminal escapes
        :rtype: str
        '''
        return self._text

    def toAnsi(self, strip:bool=False) -> str:
        '''Return the ANSI escaped representation of the string.

        :param strip: remove leading/trailing reset sequences
        :type strip: bool

        :return: ANSI escaped text
        :rtype: str
        '''
        out   = ""
        color = None
        for ch, col in zip(self._text, self._colors):
            if col != color:
                color = col
                out += str(TTkColor.RST) + str(color)
            out += ch
        if strip:
            rstCh  = "\u001b[0m"
            lenRst = len(rstCh)
            while out.startswith(rstCh):
                out = out[lenRst:]
            while out.endswith(rstCh):
                out = out[:-lenRst]
            return out
        return out+str(TTkColor.RST)

    def align(self, width:int=0, color:TTkColor=TTkColor.RST, alignment:TTkK.Alignment=TTkK.Alignment.NONE) -> TTkString:
        ''' Align the string

        :param width: the new width
        :type width: int, optional
        :param color: the color of the padding, defaults to :py:class:`TTkColor.RST`
        :type color: :py:class:`TTkColor`, optional
        :param alignment: text alignment within the requested width
        :type alignment: :py:class:`TTkK.Alignment`, optional

        :return: aligned string with preserved styling
        :rtype: :py:class:`TTkString`
        '''
        lentxt = self.termWidth()
        if not width or width == lentxt: return self

        ret = TTkString()

        if lentxt < width:
            pad = width-lentxt
            if alignment in [TTkK.Alignment.NONE, TTkK.LEFT_ALIGN]:
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
                if not (_slices := [_t for _t in self.split(" ") if _t._text]) or len(_slices) < 2:
                    return self
                _avg_spaces = width - sum(_slice.termWidth() for _slice in _slices)
                _avg_space = _avg_spaces // (len(_slices)-1)
                _left_part = TTkString(' '*_avg_space).join(_slices[:-1])
                _last_space = width - _left_part.termWidth() - _slices[-1].termWidth()
                return _left_part + TTkString(' '*_last_space) + _slices[-1]
        elif self._hasSpecialWidth is not None:
            # Trim the string to a fixed size taking care of the variable width unicode chars
            rt = ""
            sz = 0
            for ch in self._text:
                rt += ch
                if unicodedata.category(ch) in ('Me','Mn'):
                    continue

                sz += 2 if unicodedata.east_asian_width(ch) == 'W' else 1

                if sz == width:
                    ret._text   =  rt
                    ret._colors =  self._colors[:len(rt)]
                    break
                elif sz > width:
                    ret._text   =  rt[:-1]+TTkCfg.theme.unicodeWideOverflowCh[1]
                    ret._colors =  self._colors[:len(ret._text)]
                    ret._colors[-1] = TTkString.unicodeWideOverflowColor
                    break
        else:
            # Legacy, trim the string
            ret._text   =  self._text[:width]
            ret._colors =  self._colors[:width]

        ret._hasTab = '\t' in ret._text
        ret._fastCheckWidth(self._hasSpecialWidth)

        return ret

    def extractShortcuts(self) -> Tuple[TTkString,List[str]]:
        '''Extract ``&`` shortcuts and underline the mnemonic characters.

        :return: tuple of processed string and extracted shortcut characters
        :rtype: tuple[:py:class:`TTkString`, list[str]]
        '''
        def _chGenerator():
            for ch,color in zip(self._text,self._colors):
                yield ch,color
        _newText   = ""
        _newColors = []
        _ret = []
        _gen = _chGenerator()
        _found = False
        for ch,color in _gen:
            if ch == '&':
                _found =  True
                continue
            if _found:
                _found = False
                _ret.append(ch)
                color += self.mnemonicColor  # UNDERLINE
            _newText += ch
            _newColors.append(color)
        return TTkString._importString1(_newText,_newColors), _ret

    def replace(self, *args, **kwargs) -> TTkString:
        ''' **replace** (*old*, *new*, *count*)

        Replace "**old**" match with "**new**" string for "**count**" times

        :param old: substring to be replaced
        :type old: str
        :param new: replacement substring
        :type new: str, optional
        :param count: maximum number of replacements
        :type count: int, optional

        :return: updated string preserving color spans
        :rtype: :py:class:`TTkString`
        '''
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
            while (pos := (self._text.index(old, start) if old in self._text[start:] else None)) is not None:
                ret._colors += self._colors[start:pos+newLen]
                start = pos+oldLen
                count -= 1
                if count == 0: break
            ret._colors += self._colors[start:]
            ret._text   = self._text.replace(*args, **kwargs)
        else:
            start = 0
            while (pos := (self._text.index(old, start) if old in self._text[start:] else None)) is not None:
                ret._colors += self._colors[start:pos+oldLen] + [self._colors[pos+oldLen-1]]*(newLen-oldLen)
                start = pos+oldLen
                if count == 0: break
            ret._colors += self._colors[start:]
            ret._text   = self._text.replace(*args, **kwargs)

        ret._hasTab = '\t' in ret._text
        ret._checkWidth()

        return ret

    def completeColor(self, color:TTkColor, match:Optional[str]=None, posFrom:Optional[int]=None, posTo:Optional[int]=None) -> TTkString:
        ''' Complete the color of the entire string or a slice of it

        The Fg and/or Bg of the string is replaced with the selected Fg/Bg color only if missing

        If only the color is specified, the entire string is colorized

        :param color: the color to be used, defaults to :py:class:`TTkColor.RST`
        :type color: :py:class:`TTkColor`
        :param match: the match to colorize
        :type match: str, optional
        :param posFrom: the initial position of the color
        :type posFrom: int, optional
        :param posTo: the final position of the color
        :type posTo: int, optional

        :return: recolored string
        :rtype: :py:class:`TTkString`
        '''
        ret = TTkString()
        ret._text = self._text
        ret._hasTab = self._hasTab
        ret._hasSpecialWidth = self._hasSpecialWidth
        if match:
            ret._colors = self._colors.copy()
            start=0
            lenMatch = len(match)
            while (pos := self._text.index(match, start) if match in self._text[start:] else None) is not None:
                start = pos+lenMatch
                for i in range(pos, pos+lenMatch):
                    ret._colors[i] |= color
        elif isinstance(posFrom,int) and isinstance(posTo, int) and posFrom < posTo:
            ret._colors = self._colors.copy()
            posFrom = min(len(self._text),posFrom)
            posTo   = min(len(self._text),posTo)
            for i in range(posFrom, posTo):
                ret._colors[i] |= color
        else:
            ret._colors = [c|color for c in self._colors]
        return ret


    def setColor(self, color:TTkColor, match:Optional[str]=None, posFrom:Optional[int]=None, posTo:Optional[int]=None) -> TTkString:
        ''' Set the color of the entire string or a slice of it

        If only the color is specified, the entire string is colorized

        :param color: the color to be used, defaults to :py:class:`TTkColor.RST`
        :type color: :py:class:`TTkColor`
        :param match: the match to colorize
        :type match: str, optional
        :param posFrom: the initial position of the color
        :type posFrom: int, optional
        :param posTo: the final position of the color
        :type posTo: int, optional

        :return: recolored string
        :rtype: :py:class:`TTkString`
        '''
        ret = TTkString()
        ret._text  += self._text
        ret._hasTab = self._hasTab
        ret._hasSpecialWidth = self._hasSpecialWidth
        if match:
            ret._colors += self._colors
            start=0
            lenMatch = len(match)
            while None != (pos := self._text.index(match, start) if match in self._text[start:] else None):
                start = pos+lenMatch
                ret._colors[pos: pos+lenMatch] = [color]*lenMatch
        elif posFrom is posTo is None:
            ret._colors = [color]*len(self._text)
        elif isinstance(posFrom,int) and isinstance(posTo, int) and posFrom < posTo:
            ret._colors += self._colors
            posFrom = min(len(self._text),posFrom)
            posTo   = min(len(self._text),posTo)
            ret._colors[posFrom:posTo] = [color]*(posTo-posFrom)
        else:
            ret._colors += self._colors
        return ret

    def substring(self, fr:Optional[int]=None, to:Optional[int]=None) -> TTkString:
        ''' Return the substring

        :param fr: the starting of the slice, defaults to 0
        :type fr: int, optional
        :param to: the ending of the slice, defaults to the end of the string
        :type to: int, optional

        :return: sliced string
        :rtype: :py:class:`TTkString`
        '''
        ret = TTkString()
        ret._text   = self._text[fr:to]
        ret._colors = self._colors[fr:to]
        ret._hasTab = '\t' in ret._text
        ret._fastCheckWidth(self._hasSpecialWidth)
        return ret

    def split(self, separator:str) -> list[TTkString]:
        ''' Split the string using a separator

        .. note:: Only a one char separator is currently supported

        :param separator: the "**char**" separator to be used
        :type separator: str

        :return: list of split chunks
        :rtype: list[:py:class:`TTkString`]
        '''
        ret = []
        pos = 0
        if len(separator)==1:
            for i,c in enumerate(self._text):
                if c == separator:
                    ret.append(self.substring(pos,i))
                    pos = i+1
        else:
            raise NotImplementedError("Not yet implemented separators bigger than one char")
        ret.append(self.substring(pos,len(self)))

        return ret

    def getData(self) -> Tuple[Union[Tuple[str,...],List[str]],List[TTkColor]]:
        '''Return text and color data in terminal-rendered form.

        :return: tuple of characters and colors
        :rtype: tuple
        '''
        if self._hasSpecialWidth is not None:
            return self._getDataW()
        else:
            return (tuple(self._text), self._colors)

    def search(self, regexp:str, ignoreCase:bool=False) -> Optional[re.Match[str]]:
        ''' Return the **re.match** of the **regexp**

        :param regexp: the regular expression to be matched
        :type regexp: str
        :param ignoreCase: Ignore case, defaults to **False**
        :type ignoreCase: bool

        :return: first regular-expression match or None
        :rtype: re.Match | None
        '''
        return re.search(regexp, self._text, re.IGNORECASE if ignoreCase else 0)

    def find(self, *args, **kwargs) -> int:
        '''Return the first index of a substring using ``str.find`` semantics.

        :return: start index of the first match, or ``-1`` if not found
        :rtype: int
        '''
        return self._text.find(*args, **kwargs)

    def findall(self, regexp:str, ignoreCase:bool=False) -> List[Any]:
        ''' FindAll the **regexp** matches in the string

        :param regexp: the regular expression to be matched
        :type regexp: str
        :param ignoreCase: Ignore case, defaults to **False**
        :type ignoreCase: bool

        :return: list of all matches
        :rtype: list[str] | list[tuple]
        '''
        return re.findall(regexp, self._text, re.IGNORECASE if ignoreCase else 0)

    def getIndexes(self, char:str) -> List[int]:
        '''Return indexes where ``char`` appears.

        :param char: target character
        :type char: str

        :return: matching character positions
        :rtype: list[int]
        '''
        return [i for i,c in enumerate(self._text) if c==char]

    def join(self, strings:Union[GeneratorType[TTkStringType,None,None],List[TTkStringType],List[TTkString],List[str]]) -> TTkString:
        ''' Join the input strings using the current as separator

        :param strings: the list of strings to be joined
        :type strings: list

        :return: joined string
        :rtype: :py:class:`TTkString`
        '''
        if not strings:
            return TTkString()
        if isinstance(strings, GeneratorType):
            strings = [s for s in strings]
        ret = TTkString(strings[0])
        for s in strings[1:]:
            ret += self + s
        return ret

    # Unicode Zero/Half/Normal sized chars helpers:
    @staticmethod
    def _isWideCharData(ch:str) -> bool:
        '''Check whether ``ch`` starts with a wide character.

        :param ch: input text chunk
        :type ch: str

        :return: True when first character is wide
        :rtype: bool
        '''
        if len(ch) == 1:
            return unicodedata.east_asian_width(ch)=='W'
        if len(ch) > 1:
            return unicodedata.east_asian_width(ch[0])=='W'
        return False

    @staticmethod
    def _isSpecialWidthChar(ch:str) -> bool:
        '''Check whether a character has non-standard display width.

        :param ch: input character
        :type ch: str

        :return: True for wide or combining characters
        :rtype: bool
        '''
        return ( unicodedata.east_asian_width(ch) == 'W' or
                 unicodedata.category(ch) in ('Me','Mn') )

    @staticmethod
    def _getWidthText(txt:str) -> int:
        '''Compute rendered width for a text snippet.

        :param txt: input text
        :type txt: str

        :return: rendered width
        :rtype: int
        '''
        return ( len(txt) +
            sum(unicodedata.east_asian_width(ch) == 'W' for ch in txt) -
            sum(unicodedata.category(ch) in ('Me','Mn') for ch in txt) )

    @staticmethod
    def _getLenTextWoZero(txt:str) -> int:
        '''Count text length excluding zero-width combining marks.

        :param txt: input text
        :type txt: str

        :return: logical length without combining marks
        :rtype: int
        '''
        return ( len(txt) -
            sum(unicodedata.category(ch) in ('Me','Mn') for ch in txt) )

    def nextPos(self, pos:int) -> int:
        '''Return next editable character position.

        :param pos: current position
        :type pos: int

        :return: next non-combining character index
        :rtype: int
        '''
        pos += 1
        for i,ch in enumerate(self._text[pos:]):
            if unicodedata.category(ch) not in ('Me','Mn'):
                return pos+i
        return len(self._text)

    def prevPos(self, pos:int) -> int:
        '''Return previous editable character position.

        :param pos: current position
        :type pos: int

        :return: previous non-combining character index
        :rtype: int
        '''
        # from TermTk.TTkCore.log import TTkLog
        # TTkLog.debug(f"->{self._text[:pos]}<- {pos=}")
        # TTkLog.debug(f"{str(reversed(self._text[:pos]))} {pos=}")
        for i,ch in enumerate(reversed(self._text[:pos])):
            # TTkLog.debug(f"{i}---> {ch}    ")
            if unicodedata.category(ch) not in ('Me','Mn'):
                return pos-i-1
        return 0

    def _fastCheckWidth(self, a:Optional[int], b:Optional[int]=None) -> None:
        self._hasSpecialWidth = None if (
                a is None and b is None ) else self._termWidthW()

    def _checkWidth(self):
        # from: tests/timeit/09.widechar.check.py
        # the first not halfsize char is 0x300
        # this check is ~3 times faster than the 2 combined unicode checks
        # and will quickly filter out the (more common) simple ascii text
        tw = self._termWidthW() if any(ord(ch)>=0x300 for ch in self._text) else None
        self._hasSpecialWidth = tw if tw != len(self._text) else None

    def _termWidthW(self) -> int:
        ''' String displayed length

        This value consider the displayed size (Zero, Half, Full) of each character.

        :return: rendered width
        :rtype: int
        '''
        return ( len(self._text) +
             sum(unicodedata.east_asian_width(ch) == 'W' for ch in self._text) -
             sum(unicodedata.category(ch) in ('Me','Mn') for ch in self._text) )

    def _getDataW_pts(self) -> Tuple[List[str],List[TTkColor]]:
        retTxt = []  # type: List[str]
        retCol = []  # type: List[TTkColor]
        for ch,color in zip(self._text,self._colors):
            if unicodedata.east_asian_width(ch) == 'W':
                retTxt += (ch,'')
                retCol += (color,color)
            elif unicodedata.category(ch) in ('Me','Mn'):
                if retTxt:
                    if len(retTxt)>1 and retTxt[-1] == '':
                        retTxt[-2]+=ch
                    else:
                        retTxt[-1]+=ch
                #else:
                #    retTxt = [f"{ch}"]
                #    retCol = [TTkColor.RST]
            else:
                retTxt.append(ch)
                retCol.append(color)
        return (retTxt, retCol)

    def _getDataW_tty(self) -> Tuple[List[str],List[TTkColor]]:
        retTxt = []  # type: List[str]
        retCol = []  # type: List[TTkColor]
        for ch,color in zip(self._text,self._colors):
            if unicodedata.east_asian_width(ch) == 'W':
                retTxt += ('■','■')
                retCol += (color,color)
            elif unicodedata.category(ch) not in ('Me','Mn'):
                retTxt.append(ch)
                retCol.append(color)
        return (retTxt, retCol)

    if os.environ.get("TERMTK_GPM",False):
        _getDataW = _getDataW_tty
    else:
        _getDataW = _getDataW_pts

TTkStringType = Union[str, TTkString]