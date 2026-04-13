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

from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from typing import List, Optional, Tuple

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.string import TTkString
from TermTk.TTkGui.textdocument import TTkTextDocument

from .text_wrap import _WrapEngine_Interface
from .text_wrap_data import _WrapLine, _WrapState

class _BisectKeyLine:
    '''Helper to bisect _WrapLine list by the .line attribute.'''
    __slots__ = ('_buf',)
    _buf:List[_WrapLine]
    def __init__(self, buf:List[_WrapLine]):
        self._buf = buf
    def __len__(self) -> int:
        return len(self._buf)
    def __getitem__(self, i) -> int:
        return self._buf[i].line

class _WrapEngine_FullWrap(_WrapEngine_Interface):
    __slots__ = ('_buffer')

    _buffer: List[_WrapLine]

    def __init__(self, state):
        self._buffer = []
        super().__init__(state)
        self._wrapState.textDocument.contentsChange.connect(self.rewrap)

    def clean(self):
        self._wrapState.textDocument.contentsChange.disconnect(self.rewrap)

    def size(self) -> int:
        return len(self._buffer)

    @pyTTkSlot()
    def rewrap(self) -> None:
        self._buffer = []

        if not (w := self._wrapState.size):
            return

        for i,l in enumerate(self._wrapState.textDocument._dataLines):
            self._buffer.extend(self._wrapLine(w,i,l))

    def dataToScreenPosition(self, line:int, pos:int) -> Tuple[int, int]:
        text_document = self._wrapState.textDocument
        keys = _BisectKeyLine(self._buffer)
        lo = bisect_left(keys, line)
        hi = bisect_right(keys, line, lo)
        for i in range(lo, hi):
            row = self._buffer[i]
            if row.start <= pos <= row.stop:
                l = text_document.dataLine(line).substring(row.start, pos).tab2spaces(self._wrapState.tabSpaces)
                return l.termWidth(), i
        return 0, 0

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        y = max(0,min(y,len(self._buffer)-1))
        text_document = self._wrapState.textDocument
        row = self._buffer[y]
        dt=row.line
        fr=row.start
        to=row.stop
        pos = fr+text_document.dataLine(dt).substring(fr,to).tabCharPos(x,self._wrapState.tabSpaces)
        return dt, pos

    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        text_document = self._wrapState.textDocument
        y = max(0,min(y,self.size()-1))
        row = self._buffer[y]
        dt=row.line
        fr=row.start
        to=row.stop
        x = max(0,x)
        s = text_document.dataLine(dt).substring(fr,to)
        x = s.tabCharPos(x, self._wrapState.tabSpaces)
        x = s.substring(0,x).tab2spaces(self._wrapState.tabSpaces).termWidth()
        return x, y

    def screenRows(self, y:int, h:int) -> List[_WrapLine]:
        return self._buffer[y:y+h]