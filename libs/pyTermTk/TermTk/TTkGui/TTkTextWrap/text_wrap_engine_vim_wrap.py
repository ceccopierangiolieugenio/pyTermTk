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

from dataclasses import dataclass
from typing import List, Optional, Tuple
from .text_wrap import _WrapEngine_Interface
from .text_wrap_data import _ReWrapData, _WrapLine, _WrapState

@dataclass
class _LastWindow():
    '''Cache of the last wrapped viewport window.

    :param y: first wrapped row of the cached viewport.
    :type y: int
    :param h: viewport height used to build the cache.
    :type h: int
    :param buffer: cached wrapped-row descriptors.
    :type buffer: List[:py:class:`_WrapLine`]
    '''
    y:int
    h:int
    buffer:List[_WrapLine]

class _WrapEngine_VimWrap(_WrapEngine_Interface):
    '''Lazy wrap engine optimized around the active viewport.'''
    __slots__ = ('_lastWindow')

    _lastWindow: _LastWindow

    def __init__(self, state):
        '''Initialize the viewport cache for lazy wrapping.

        :param state: shared wrap state.
        :type state: :py:class:`_WrapState`
        '''
        self._lastWindow = _LastWindow(y=0,h=0,buffer=[])
        super().__init__(state)

    def size(self) -> int:
        '''Return the number of source lines.

        :return: logical line count.
        :rtype: int
        '''
        return len(self._wrapState.textDocument._dataLines)

    def rewrap(self, data: Optional[_ReWrapData]=None) -> None:
        '''No-op; wrapping is generated on demand by viewport.

        :param data: optional change descriptor, ignored.
        :type data: Optional[:py:class:`_ReWrapData`]
        '''
        pass

    def dataToScreenPosition(self, line:int, pos:int) -> Tuple[int, int]:
        '''Map document coordinates using the cached window buffer.

        :param line: source line index.
        :type line: int
        :param pos: source position within line.
        :type pos: int

        :return: ``(x, y)`` position if present in cache, else ``(0, 0)``.
        :rtype: Tuple[int, int]
        '''
        if not (w := self._wrapState.size):
            return 0,0
        text_document = self._wrapState.textDocument
        buffer = self._lastWindow.buffer
        for i, row in enumerate(buffer):
            dt=row.line
            fr=row.start
            to=row.stop
            if dt == line and fr <= pos <= to:
                l = text_document.dataLine(dt).substring(fr,pos).tab2spaces(self._wrapState.tabSpaces)
                return l.termWidth(), i+self._lastWindow.y
        return 0,0

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Map screen coordinates back to source coordinates.

        :param x: horizontal coordinate.
        :type x: int
        :param y: vertical coordinate.
        :type y: int

        :return: ``(line, pos)`` from the cached viewport.
        :rtype: Tuple[int, int]
        '''
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
        '''Clamp a screen coordinate to a valid cached character cell.

        :param x: horizontal coordinate.
        :type x: int
        :param y: vertical coordinate.
        :type y: int

        :return: normalized ``(x, y)``.
        :rtype: Tuple[int, int]
        '''
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
        '''Wrap and cache enough rows to satisfy a viewport request.

        :param y: first viewport row.
        :type y: int
        :param h: viewport height.
        :type h: int

        :return: cached wrapped row descriptors.
        :rtype: List[:py:class:`_WrapLine`]
        '''
        if not (w := self._wrapState.size):
            return []

        self._lastWindow = _LastWindow(y=y, h=h, buffer=[])

        for _i,_line in enumerate(self._wrapState.textDocument._dataLines[y:y+h], start=y):
            self._lastWindow.buffer.extend(self._wrapLine(w,_i,_line))
            if len(self._lastWindow.buffer) >= h:
                break
        return self._lastWindow.buffer
