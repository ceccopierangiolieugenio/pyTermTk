# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys
from threading import RLock
from typing import List, Tuple, Optional

from .text_wrap import _WrapEngine_Interface
from .text_wrap_data import _WrapLine, _ReWrapData

# TODO: remove Python 3.9 compatibility routine once dropped support
# Python 3.9 compatibility: key parameter was added in Python 3.10
if sys.version_info >= (3, 10):
    from bisect import bisect_left, bisect_right
else:
    from bisect import bisect_left as _bisect_left, bisect_right as _bisect_right
    class _BisectKeyLine:
        __slots__ = ('_buf', '_key')
        _buf:List[_WrapLine]
        def __init__(self, buf:List[_WrapLine], key):
            self._buf = buf
            self._key = key
        def __len__(self) -> int:
            return len(self._buf)
        def __getitem__(self, i) -> int:
            return self._key(self._buf[i])
    def bisect_left(a, x, lo=0, hi=None, *, key=None):
        '''Compatibility wrapper for bisect_left with key parameter support.'''
        if key is None:
            return _bisect_left(a, x, lo, hi if hi is not None else len(a))
        keys = _BisectKeyLine(a, key)
        return _bisect_left(keys, x, lo, hi if hi is not None else len(a))

    def bisect_right(a, x, lo=0, hi=None, *, key=None):
        '''Compatibility wrapper for bisect_right with key parameter support.'''
        if key is None:
            return _bisect_right(a, x, lo, hi if hi is not None else len(a))
        keys = _BisectKeyLine(a, key)
        return _bisect_right(keys, x, lo, hi if hi is not None else len(a))

class _WrapEngine_FullWrap(_WrapEngine_Interface):
    '''Eager wrap engine that maintains a full wrapped-row buffer.

    Thread Safety: All buffer operations are protected with an RLock mutex.
    '''
    __slots__ = ('_buffer', '_bufferLock')

    _buffer: List[_WrapLine]

    def __init__(self, state):
        '''Initialize the internal wrapped-row buffer.

        :param state: shared wrap state.
        :type state: :py:class:`_WrapState`
        '''
        self._buffer = []
        self._bufferLock = RLock()
        super().__init__(state)

    def size(self) -> int:
        '''Return the number of wrapped rows currently cached.

        :return: wrapped row count.
        :rtype: int
        '''
        with self._bufferLock:
            return len(self._buffer)

    def rewrap(self, data: Optional[_ReWrapData]=None) -> None:
        '''Update wrapped rows for a full or incremental document change.

        :param data: optional incremental change descriptor. If omitted,
                     the full wrapped buffer is rebuilt.
        :type data: Optional[:py:class:`_ReWrapData`]
        '''
        if not (w := self._wrapState.size):
            return

        with self._bufferLock:
            if isinstance(data, _ReWrapData):
                line = data.line
                added = data.added
                removed = data.removed
                changed:List[_WrapLine] = []

                lo = bisect_left(self._buffer, line, key=lambda _wl:_wl.line)
                hi = bisect_right(self._buffer, line+removed-1, lo, key=lambda _wl:_wl.line)

                for i,l in enumerate(self._wrapState.textDocument.dataLines(slice(line,line+added)), start=line):
                    changed.extend(self._wrapLine(w,i,l))
                for row in self._buffer[hi:]:
                    row.line += added - removed
                self._buffer[lo:hi] = changed
            else:
                self._buffer = []
                for i,l in enumerate(self._wrapState.textDocument.dataLines()):
                    self._buffer.extend(self._wrapLine(w,i,l))

    def dataToScreenPosition(self, line:int, pos:int) -> Tuple[int, int]:
        '''Map source coordinates to screen coordinates using the full buffer.

        :param line: source line index.
        :type line: int
        :param pos: source character offset.
        :type pos: int

        :return: ``(x, y)`` wrapped coordinates.
        :rtype: Tuple[int, int]
        '''
        text_document = self._wrapState.textDocument
        with self._bufferLock:
            lo = bisect_left(self._buffer, line, key=lambda _wl:_wl.line)
            hi = bisect_right(self._buffer, line, lo, key=lambda _wl:_wl.line)
            for i in range(lo, hi):
                row = self._buffer[i]
                if row.start <= pos <= row.stop:
                    data_line = text_document.dataLine(line)
                    if data_line is None:
                        return 0, 0
                    l = data_line.substring(row.start, pos).tab2spaces(self._wrapState.tabSpaces)
                    return l.termWidth(), i
        return 0, 0

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Map wrapped screen coordinates back to source coordinates.

        :param x: horizontal screen coordinate.
        :type x: int
        :param y: vertical wrapped-row coordinate.
        :type y: int

        :return: ``(line, pos)`` source coordinates.
        :rtype: Tuple[int, int]
        '''
        text_document = self._wrapState.textDocument
        with self._bufferLock:
            y = max(0, min(y, len(self._buffer)-1))
            row = self._buffer[y]
            dt = row.line
            fr = row.start
            to = row.stop
        data_line = text_document.dataLine(dt)
        if data_line is None:
            return 0, 0
        pos = fr + data_line.substring(fr, to).tabCharPos(x, self._wrapState.tabSpaces)
        return dt, pos

    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Clamp coordinates to a valid character position in the buffer.

        :param x: horizontal coordinate.
        :type x: int
        :param y: vertical coordinate.
        :type y: int

        :return: normalized ``(x, y)``.
        :rtype: Tuple[int, int]
        '''
        text_document = self._wrapState.textDocument
        with self._bufferLock:
            y = max(0, min(y, self.size()-1))
            row = self._buffer[y]
            dt = row.line
            fr = row.start
            to = row.stop
        x = max(0, x)
        data_line = text_document.dataLine(dt)
        if data_line is None:
            return 0, 0
        s = data_line.substring(fr, to)
        x = s.tabCharPos(x, self._wrapState.tabSpaces)
        x = s.substring(0, x).tab2spaces(self._wrapState.tabSpaces).termWidth()
        return x, y

    def screenRows(self, y:int, h:int) -> List[_WrapLine]:
        '''Return a viewport slice from the precomputed wrapped buffer.

        :param y: first wrapped row.
        :type y: int
        :param h: number of rows.
        :type h: int

        :return: wrapped row descriptors for the viewport.
        :rtype: List[:py:class:`_WrapLine`]
        '''
        with self._bufferLock:
            return self._buffer[y:y+h].copy()