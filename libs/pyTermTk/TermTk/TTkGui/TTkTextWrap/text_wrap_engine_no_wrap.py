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

__all__:list = []

from typing import List, Tuple

from .text_wrap import _WrapEngine_Interface
from .text_wrap_data import _WrapLine, _WrapState


class _WrapEngine_NoWrap(_WrapEngine_Interface):
    def size(self) -> int:
        return len(self._wrapState.textDocument._dataLines)

    def rewrap(self) -> None:
        pass

    def dataToScreenPosition(self, line:int, pos:int) -> Tuple[int, int]:
        text_document = self._wrapState.textDocument
        data_line = text_document.dataLine(line)
        if 0 <= pos <= len(data_line) + 1:
            l = data_line.substring(0,pos).tab2spaces(self._wrapState.tabSpaces)
            return l.termWidth(), line
        return 0,0

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        line = self._wrapState.textDocument.dataLine(y)
        pos = line.tabCharPos(x,self._wrapState.tabSpaces)
        return y, pos

    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        x = max(0,x)
        y = max(0,min(y,self.size()-1))
        line = self._wrapState.textDocument.dataLine(y)
        x = line.tabCharPos(x, self._wrapState.tabSpaces)
        x = line.substring(0,x).tab2spaces(self._wrapState.tabSpaces).termWidth()
        return x, y

    def screenRows(self, y:int, h:int) -> List[_WrapLine]:
        return [
            _WrapLine(_i, 0, len(_line)+1)
            for _i,_line in enumerate(self._wrapState.textDocument._dataLines[y:y+h], start=y)
        ]
