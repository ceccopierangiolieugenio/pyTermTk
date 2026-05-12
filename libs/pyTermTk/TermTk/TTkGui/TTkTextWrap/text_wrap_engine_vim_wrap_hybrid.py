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

from dataclasses import dataclass
from threading import RLock
from typing import Final, List, Optional, Tuple

from .text_wrap import _WrapEngine_Interface
from .text_wrap_data import _ReWrapData, _RetScreenPosition, _RetScreenPositions, _RetScreenRows, _WrapLine, _WrapState

_WINDOW_BORDER : Final[int] = 32


@dataclass
class _getBufferSignature():
    '''Viewport signature for caching.

    :param y: first viewport row.
    :type y: int
    :param h: viewport height.
    :type h: int
    '''
    y: int
    h: int


@dataclass
class _LastWindow():
    '''Cache of the last wrapped viewport window.

    :param buffer: cached wrapped-row descriptors.
    :type buffer: List[:py:class:`_WrapLine`]
    :param signature: viewport signature used to build the cache.
    :type signature: Optional[:py:class:`_getBufferSignature`]
    '''
    buffer: List[_WrapLine]
    signature: Optional[_getBufferSignature] = None

    @property
    def y(self) -> int:
        if not self.buffer:
            return 0
        return self.buffer[0].line

    @property
    def h(self) -> int:
        return len(self.buffer)

    @property
    def lines(self) -> int:
        if not self.buffer:
            return 0
        return self.buffer[-1].line - self.buffer[0].line + 1

    @property
    def first_line(self) -> int:
        if not self.buffer:
            return 0
        return self.buffer[0].line

    def hasSlice(self, y:int, h:int) -> bool:
        return self.y <= y < y+h <= self.y+self.h

    def slice(self, y:int, h:int) -> List[_WrapLine]:
        by = self.y
        return self.buffer[y-by:y-by+h+1]



class _WrapEngine_HybridVimWrap(_WrapEngine_Interface):
    '''Lazy wrap engine optimized around the active viewport.

    This engine is intentionally *viewport-accurate* only:

        * rows inside the cached window are wrapped with full accuracy;
        * coordinates outside the cached window are treated as unwrapped
            document lines to keep lookups and navigation fast on large files.

    This trade-off is deliberate and favors responsiveness while preserving
    precise behavior on visible content.

    Thread Safety: All cache operations are protected with an RLock mutex.
    '''
    __slots__ = ('_lastWindow', '_cacheLock')

    _lastWindow: _LastWindow

    def __init__(self, state):
        '''Initialize the viewport cache for lazy wrapping.

        :param state: shared wrap state.
        :type state: :py:class:`_WrapState`
        '''
        self._lastWindow = _LastWindow(buffer=[])
        self._cacheLock = RLock()
        super().__init__(state)

    def size(self) -> int:
        '''Return an approximate number of addressable screen rows.

        For visible rows this behaves like wrapped coordinates. Outside the
        cached viewport, this engine falls back to unwrapped line semantics,
        so the returned value is intentionally an approximation suitable for
        scrolling/navigation bounds.

        :return: logical line count.
        :rtype: int
        '''
        document = self._wrapState.textDocument
        document_size = document.lineCount()

        with self._cacheLock:
            lastWindow = self._lastWindow
            return max(0,document_size - lastWindow.lines + len(lastWindow.buffer))

    def rewrap(self, data: Optional[_ReWrapData]=None) -> None:
        '''Invalidate cached viewport data.

        Wrapping is generated on demand by :py:meth:`screenRows`. This method
        clears the last-window cache so subsequent calls rebuild from the
        current document/wrap settings.

        :param data: optional change descriptor, ignored.
        :type data: Optional[:py:class:`_ReWrapData`]
        '''
        with self._cacheLock:
            if signature := self._lastWindow.signature:
                self._getBuffer(signature.y, signature.h, force=True)
            else:
                self._lastWindow = _LastWindow(buffer=[])

    def dataToScreenPosition(self, line:int, pos:int) -> _RetScreenPositions:
        '''Map document coordinates to screen coordinates.

        Behavior depends on whether the target position is in the cached
        viewport window:

        * in-window: return fully wrapped ``(x, y)`` coordinates;
        * offscreen: return unwrapped-style coordinates where ``y`` matches
          the source line index.

        :param line: source line index.
        :type line: int
        :param pos: source position within line.
        :type pos: int

        :return: wrapped or fallback unwrapped-style screen coordinates.
        :rtype: :py:class:`_RetScreenPositions`
        '''
        if not self._wrapState.size:
            return _RetScreenPositions(main=_RetScreenPosition(x=0,y=0))
        text_document = self._wrapState.textDocument
        with self._cacheLock:
            buffer = self._lastWindow.buffer
            for i, row in enumerate(buffer, self._lastWindow.y):
                dt=row.line
                fr=row.start
                to=row.stop
                if dt == line and fr <= pos <= to:
                    data_line = text_document.dataLine(dt)
                    if data_line is None:
                        return _RetScreenPositions(main=_RetScreenPosition(x=0,y=0))
                    l = data_line.substring(fr,pos).tab2spaces(self._wrapState.tabSpaces)
                    x, y = l.termWidth(), i
                    extra = None
                    # Check if this is the end of the line and the beginning of the next one
                    if pos == row.stop and not row.last_slice:
                        extra = _RetScreenPosition(x=0,y=y+1)
                    return _RetScreenPositions(main=_RetScreenPosition(x=x,y=y), extra=extra)
                elif dt == line and row.last_slice and pos > row.stop:
                    data_line = text_document.dataLine(dt)
                    l = data_line.substring(row.start, row.stop).tab2spaces(self._wrapState.tabSpaces)
                    x, y = l.termWidth(), i
                    return _RetScreenPositions(main=_RetScreenPosition(x=x,y=y))
            line = self._clampLine(line)
            data_line = text_document.dataLine(line)
            if data_line is None:
                return _RetScreenPositions(main=_RetScreenPosition(x=0,y=0))
            if 0 <= pos <= len(data_line) + 1:
                l = data_line.substring(0,pos).tab2spaces(self._wrapState.tabSpaces)
                x, y = l.termWidth(), line
                return _RetScreenPositions(main=_RetScreenPosition(x=x,y=y))
        return _RetScreenPositions(main=_RetScreenPosition(x=0,y=0))

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Map screen coordinates back to source coordinates.

        For rows inside the cached viewport the mapping is wrap-accurate.
        For rows above/below the cached window, ``y`` is interpreted as an
        unwrapped source line index.

        :param x: horizontal coordinate.
        :type x: int
        :param y: vertical coordinate.
        :type y: int

        :return: ``(line, pos)`` from the cached viewport.
        :rtype: Tuple[int, int]
        '''
        with self._cacheLock:
            dy = y - self._lastWindow.y
            if dy < 0 or dy >= self._lastWindow.h:
                y = self._clampLine(y)
                line = self._wrapState.textDocument.dataLine(y)
                if line is None:
                    return 0, 0
                pos = line.tabCharPos(x,self._wrapState.tabSpaces)
                return y, pos
            dy = min(dy, len(self._lastWindow.buffer)-1)
            row = self._lastWindow.buffer[dy]
            dt=row.line
            fr=row.start
            to=row.stop
        text_document = self._wrapState.textDocument
        data_line = text_document.dataLine(dt)
        if data_line is None:
            return 0, 0
        pos = fr+data_line.substring(fr,to).tabCharPos(x,self._wrapState.tabSpaces)
        return dt, pos

    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Clamp a screen coordinate to a valid character cell.

        For rows inside the cached viewport this normalizes within the wrapped
        row fragment. For rows outside the cached viewport this normalizes as
        an unwrapped line coordinate.

        :param x: horizontal coordinate.
        :type x: int
        :param y: vertical coordinate.
        :type y: int

        :return: normalized ``(x, y)``.
        :rtype: Tuple[int, int]
        '''
        x = max(0,x)
        with self._cacheLock:
            dy = y - self._lastWindow.y
            if dy < 0 or dy >= self._lastWindow.h:
                y = self._clampLine(y)
                line = self._wrapState.textDocument.dataLine(y)
                if line is None:
                    return 0, 0
                x = line.tabCharPos(x, self._wrapState.tabSpaces)
                x = line.substring(0,x).tab2spaces(self._wrapState.tabSpaces).termWidth()
                return x, y
            dy = min(dy, len(self._lastWindow.buffer)-1)
            row = self._lastWindow.buffer[dy]
            dt=row.line
            fr=row.start
            to=row.stop
        x = max(0,x)
        text_document = self._wrapState.textDocument
        data_line = text_document.dataLine(dt)
        if data_line is None:
            return 0, 0
        s = data_line.substring(fr,to)
        x = s.tabCharPos(x, self._wrapState.tabSpaces)
        x = s.substring(0,x).tab2spaces(self._wrapState.tabSpaces).termWidth()
        return x, y

    def screenRows(self, y:int, h:int) -> _RetScreenRows:
        '''Wrap and cache enough rows to satisfy a viewport request.

        The engine caches only the last requested viewport window. If the same
        ``(y, h)`` pair is requested repeatedly and the cache is still valid,
        rows are returned directly without re-wrapping.

        :param y: first viewport row.
        :type y: int
        :param h: viewport height.
        :type h: int

        :return: cached wrapped row descriptors.
        :rtype: :py:class:`_RetScreenRows`
        '''
        buffer = self._getBuffer(y=y, h=h)
        return _RetScreenRows(rows=buffer)

    def _getBuffer(self, y:int, h:int, force:bool=False) -> List[_WrapLine]:
        '''Build or retrieve cached wrapped rows for a viewport window.

        :param y: first viewport row.
        :type y: int
        :param h: viewport height.
        :type h: int
        :param force: force re-wrapping even if cached slice is available.
        :type force: bool

        :return: list of wrapped row descriptors.
        :rtype: List[:py:class:`_WrapLine`]
        '''
        if not (w := self._wrapState.size):
            return []

        with self._cacheLock:
            if not force and self._lastWindow.hasSlice(y,h):
                return self._lastWindow.slice(y,h)
            else:
                buffer:List[_WrapLine] = []

                document = self._wrapState.textDocument
                document_size = document.lineCount()

                first_line = min(document_size, y+h) - h
                first_line = max(0,first_line-_WINDOW_BORDER)
                slice_size = min(document_size, first_line+_WINDOW_BORDER+h) - first_line

                for _i,_line in enumerate(document.dataLines(slice(first_line,first_line+slice_size)), start=max(0,first_line)):
                    buffer.extend(self._wrapLine(w,_i,_line))
                    # if len(buffer) >= h:
                    #     break
                self._lastWindow = _LastWindow(buffer=buffer, signature=_getBufferSignature(y=y, h=h))
                return self._lastWindow.slice(y,h)

        return []