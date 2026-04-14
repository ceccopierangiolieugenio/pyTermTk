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

from typing import List, Optional, Tuple

from .text_wrap import _WrapEngine_Interface
from .text_wrap_data import _ReWrapData, _WrapLine, _WrapState


class _WrapEngine_NoWrap(_WrapEngine_Interface):
    '''Wrapping engine that keeps one screen row per document line.'''
    def size(self) -> int:
        '''Return the number of logical lines in the document.

        :return: total visible rows.
        :rtype: int
        '''
        return self._wrapState.textDocument.lineCount()

    def rewrap(self, data: Optional[_ReWrapData]=None) -> None:
        '''No-op for no-wrap mode.

        :param data: optional change descriptor, ignored.
        :type data: Optional[:py:class:`_ReWrapData`]
        '''
        pass

    def dataToScreenPosition(self, line:int, pos:int) -> Tuple[int, int]:
        '''Convert ``(line, pos)`` into no-wrap screen coordinates.

        :param line: source line index.
        :type line: int
        :param pos: source character offset.
        :type pos: int

        :return: ``(x, y)`` screen coordinates.
        :rtype: Tuple[int, int]
        '''
        text_document = self._wrapState.textDocument
        data_line = text_document.dataLine(line)
        if 0 <= pos <= len(data_line) + 1:
            l = data_line.substring(0,pos).tab2spaces(self._wrapState.tabSpaces)
            return l.termWidth(), line
        return 0,0

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Convert no-wrap screen coordinates back to document position.

        :param x: horizontal terminal-cell coordinate.
        :type x: int
        :param y: line index on screen.
        :type y: int

        :return: ``(line, pos)`` document coordinates.
        :rtype: Tuple[int, int]
        '''
        line = self._wrapState.textDocument.dataLine(y)
        pos = line.tabCharPos(x,self._wrapState.tabSpaces)
        return y, pos

    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Clamp and normalize a screen position to valid character cells.

        :param x: horizontal coordinate.
        :type x: int
        :param y: vertical coordinate.
        :type y: int

        :return: normalized ``(x, y)``.
        :rtype: Tuple[int, int]
        '''
        x = max(0,x)
        y = max(0,min(y,self.size()-1))
        line = self._wrapState.textDocument.dataLine(y)
        x = line.tabCharPos(x, self._wrapState.tabSpaces)
        x = line.substring(0,x).tab2spaces(self._wrapState.tabSpaces).termWidth()
        return x, y

    def screenRows(self, y:int, h:int) -> List[_WrapLine]:
        '''Return contiguous source lines as viewport row descriptors.

        :param y: first row.
        :type y: int
        :param h: number of rows.
        :type h: int

        :return: row descriptors covering the requested viewport.
        :rtype: List[:py:class:`_WrapLine`]
        '''
        return [
            _WrapLine(_i, 0, len(_line)+1)
            for _i,_line in enumerate(self._wrapState.textDocument.dataLines(slice(y,y+h)), start=y)
        ]
