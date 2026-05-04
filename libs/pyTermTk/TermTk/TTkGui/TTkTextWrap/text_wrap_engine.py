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
from typing import List, Tuple, Optional

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString

from .text_wrap_data import _RetScreenPosition, _RetScreenPositions, _RetScreenRows, _WrapLine, _WrapState, _ReWrapData

class _WrapEngine_Interface():
    '''Base interface for text wrap engines.

    Concrete subclasses implement different wrapping strategies:

    * :py:class:`_WrapEngine_NoWrap` -- no wrapping, one screen row per document line.
    * :py:class:`_WrapEngine_FullWrap` -- eagerly wraps every document line into a
      pre-computed buffer that is kept in sync via the
      :py:attr:`TTkTextDocument.contentsChange` signal.
    * :py:class:`_WrapEngine_VimWrap` -- lazily wraps only the visible window,
      caching the last viewport for coordinate conversions.
        * :py:class:`_WrapEngine_FastWrap` -- chunk-based lazy wrapping strategy
            for large documents.
    '''
    __slots__ = ('_wrapState')

    _wrapState: _WrapState

    def __init__(self, state:_WrapState):
        '''Initialise the engine with shared wrapping state.

        :param state: shared state holding the document reference,
                      wrap width, tab-stop size, and word-wrap mode.
        :type state: :py:class:`_WrapState`
        '''
        self._wrapState = state

    def size(self) -> int:
        '''Return the total number of wrapped screen rows.

        For engines that do not wrap (e.g. :py:class:`_WrapEngine_NoWrap`)
        this equals the document line count.  For full-wrap engines it
        equals the length of the internal buffer after wrapping.

        :return: total wrapped row count.
        :rtype: int
        '''
        raise NotImplementedError()

    def rewrap(self, data: Optional[_ReWrapData]=None) -> None:
        '''Recompute wrapping for the entire document.

        Called when the wrap width, word-wrap mode, or the underlying
        document changes.  Engines that maintain a buffer (e.g.
        :py:class:`_WrapEngine_FullWrap`) rebuild it here; engines
        that wrap lazily (e.g. :py:class:`_WrapEngine_NoWrap`,
        :py:class:`_WrapEngine_VimWrap`) may be a no-op.

        :param data: optional incremental change descriptor.
        :type data: Optional[:py:class:`_ReWrapData`]
        '''
        raise NotImplementedError()

    def dataToScreenPosition(self, line:int, pos:int) -> _RetScreenPositions:
        '''Map a document position to wrapped screen coordinates.

        Converts a logical ``(line, pos)`` pair in the source document
        into the ``(x, y)`` position on the wrapped screen, accounting
        for tab expansion and line fragmentation.

        :param line: zero-based document line index.
        :type line: int
        :param pos: character offset within the document line.
        :type pos: int

        :return: wrapped screen coordinates where *main.x* is the
             terminal-cell column and *main.y* is the wrapped row index.
        :rtype: :py:class:`_RetScreenPositions`
        '''
        raise NotImplementedError()

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Map wrapped screen coordinates to a document position.

        Inverse of :py:meth:`dataToScreenPosition`.  Given a screen
        ``(x, y)`` pair, returns the corresponding ``(line, pos)``
        in the source document.

        :param x: horizontal screen coordinate (terminal cells).
        :type x: int
        :param y: vertical screen coordinate (wrapped row index).
        :type y: int

        :return: ``(line, pos)`` document position.
        :rtype: Tuple[int, int]
        '''
        raise NotImplementedError()

    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Snap a screen position to the nearest valid character cell.

        Clamps *y* to the valid row range and adjusts *x* so that it
        lands on a real character boundary (respecting tab expansion
        and wide characters).

        :param x: horizontal screen coordinate.
        :type x: int
        :param y: vertical screen coordinate.
        :type y: int

        :return: normalized ``(x, y)`` screen position.
        :rtype: Tuple[int, int]
        '''
        raise NotImplementedError()

    def screenRows(self, y:int, h:int) -> _RetScreenRows:
        '''Return the wrapped row slices for a viewport.

        Each returned :py:class:`_WrapLine` carries the source document
        line index together with the *start* and *stop* character
        offsets that form the visible fragment.

        :param y: first screen row of the viewport.
        :type y: int
        :param h: number of rows to retrieve.
        :type h: int

        :return: wrapped row descriptors.
        :rtype: :py:class:`_RetScreenRows`
        '''
        raise NotImplementedError()

    def _clampLine(self, line:int) -> int:
        '''Clamp a line index to the valid document range.

        Ensures the given line index is within the valid range [0, lineCount-1].

        :param line: the line index to clamp.
        :type line: int

        :return: the clamped line index.
        :rtype: int
        '''
        return max(0,min(line, self._wrapState.textDocument.lineCount()-1))

    def _wrapLine(self, _w:int, _i:int, _l:TTkString) -> List[_WrapLine]:
        '''Split a single document line into wrapped fragments.

        The line is broken into chunks that each fit within *_w*
        terminal cells.  Tab characters are expanded according to
        :py:attr:`_WrapState.tabSpaces`.  When the word-wrap mode is
        :py:attr:`TTkK.WordWrap`, breaks are placed at the last
        whitespace that fits; otherwise the line is split at exact
        cell boundaries (:py:attr:`TTkK.WrapAnywhere`).

        :param _w: available width in terminal cells.
        :type _w: int
        :param _i: document line index (stored in each :py:class:`_WrapLine`).
        :type _i: int
        :param _l: the document line to wrap.
        :type _l: :py:class:`TTkString`

        :return: one or more :py:class:`_WrapLine` fragments covering
                 the entire source line.
        :rtype: List[:py:class:`_WrapLine`]
        '''
        ret:List[_WrapLine] = []
        tabSpaces = self._wrapState.tabSpaces
        wordWrapMode = self._wrapState.wordWrapMode
        fr = 0
        if not len(_l): # if the line is empty append it
            ret.append(_WrapLine(_i,0,0,True))
            return ret
        while len(_l):
            to = _l.tabCharPos(_w, tabSpaces)
            if to >= len(_l):
                ret.append(_WrapLine(_i,fr,fr+len(_l)+1,True))
                return ret
            to = max(1,to)
            if wordWrapMode == TTkK.WordWrap: # Find the index of the first white space
                s = str(_l)
                newTo = to
                while newTo and ( s[newTo] != ' ' and s[newTo] != '\t' ): newTo-=1
                if newTo: to = newTo

            ret.append(_WrapLine(_i,fr,fr+to,False))
            _l = _l.substring(to)
            fr += to
        if ret:
            ret[-1].last_slice=True
        return ret