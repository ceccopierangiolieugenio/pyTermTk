# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__:dict = []

from bisect import bisect_right
from dataclasses import dataclass
from typing import List, Optional, Tuple

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.string import TTkString
from TermTk.TTkGui.textdocument import TTkTextDocument

from .text_wrap import _WrapEngine_Interface
from .text_wrap_data import _WrapLine, _WrapState

@dataclass
class _LastWindow():
    y:int
    h:int
    buffer:List[_WrapLine]

class _WrapEngine_VimWrap(_WrapEngine_Interface):
    __slots__ = ('_lastWindow')

    _lastWindow: _LastWindow

    def __init__(self, state):
        self._lastWindow = _LastWindow(y=0,h=0,buffer=[])
        super().__init__(state)

    def size(self) -> int:
        return len(self._wrapState.textDocument._dataLines)

    def rewrap(self) -> None:
        pass

    def dataToScreenPosition(self, line:int, pos:int) -> Tuple[int, int]:
        if not (w := self._wrapState.size):
            return 0,0
        text_document = self._wrapState.textDocument
        # documentLine = text_document._dataLines[line]
        buffer = self._lastWindow.buffer # + [_WrapLine(line,0,len(documentLine)+1)]
        for i, row in enumerate(buffer):
            dt=row.line
            fr=row.start
            to=row.stop
            if dt == line and fr <= pos <= to:
                l = text_document.dataLine(dt).substring(fr,pos).tab2spaces(self._wrapState.tabSpaces)
                return l.termWidth(), i+self._lastWindow.y
        return 0,0

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        dy = y - self._lastWindow.y
        if not (0 <= dy < self._lastWindow.h):
            return 0,0
        text_document = self._wrapState.textDocument
        row = self._lastWindow.buffer[dy]
        dt=row.line
        fr=row.start
        to=row.stop
        pos = fr+text_document.dataLine(dt).substring(fr,to).tabCharPos(x,self._wrapState.tabSpaces)
        return dt, pos

    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        y = max(0,min(y,self.size()-1))
        dy = y - self._lastWindow.y
        if not (0 <= dy < self._lastWindow.h):
            return 0,0
        text_document = self._wrapState.textDocument
        row = self._lastWindow.buffer[dy]
        dt=row.line
        fr=row.start
        to=row.stop
        x = max(0,x)
        s = text_document.dataLine(dt).substring(fr,to)
        x = s.tabCharPos(x, self._wrapState.tabSpaces)
        x = s.substring(0,x).tab2spaces(self._wrapState.tabSpaces).termWidth()
        return x, y

    def screenRows(self, y:int, h:int) -> List[_WrapLine]:
        if not (w := self._wrapState.size):
            return []

        self._lastWindow = _LastWindow(y=y, h=h, buffer=[])

        for _i,_line in enumerate(self._wrapState.textDocument._dataLines[y:y+h], start=y):
            self._lastWindow.buffer.extend(self._wrapLine(w,_i,_line))
            if len(self._lastWindow.buffer) >= h:
                break
        return self._lastWindow.buffer
