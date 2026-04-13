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

__all__ = ['TTkTextWrap']


from typing import List, Optional, Tuple

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.string import TTkString
from TermTk.TTkGui.textdocument import TTkTextDocument

from .text_wrap_data import _WrapLine, _WrapState
from .text_wrap_engine import _WrapEngine_Interface
from .text_wrap_engine_no_wrap import _WrapEngine_NoWrap
from .text_wrap_engine_vim_wrap import _WrapEngine_VimWrap
from .text_wrap_engine_fast_wrap import _WrapEngine_FastWrap
from .text_wrap_engine_full_wrap import _WrapEngine_FullWrap

class TTkTextWrap():
    '''TTkTextWrap:

    Incremental text wrapping helper for :py:class:`TTkTextDocument`.
    It maps document positions to wrapped screen rows and vice versa.
    '''
    __slots__ = (
        '_wrapState',
        '_wrapEngine',

        # Signals
        'wrapChanged'
        )

    _wrapState: _WrapState
    _wrapEngine: _WrapEngine_Interface

    def __init__(self, document:TTkTextDocument) -> None:
        '''Create a wrap manager bound to a text document.

        :param document: optional source document; when omitted a new
                         :py:class:`TTkTextDocument` is created.
        :type document: Optional[:py:class:`TTkTextDocument`]
        '''
        # signals
        self.wrapChanged = pyTTkSignal()

        self._wrapState = _WrapState(
            size=80,
            tabSpaces=4,
            textDocument=document,
            wordWrapMode=TTkK.WrapAnywhere,
        )
        self._wrapEngine = _WrapEngine_NoWrap(state=self._wrapState)

    def setDocument(self, document:TTkTextDocument) -> None:
        '''Attach a new document and reset wrapping caches.

        :param document: source text document.
        :type document: :py:class:`TTkTextDocument`
        '''
        self._wrapState.textDocument = document
        self.rewrap()

    def setEngine(self, engine:TTkK.WrapEngine):
        engine_class = {
            TTkK.WrapEngine.FastWrap : _WrapEngine_FastWrap,
            TTkK.WrapEngine.FullWrap : _WrapEngine_FullWrap,
            TTkK.WrapEngine.VimWrap : _WrapEngine_VimWrap,
            TTkK.WrapEngine.NoWrap : _WrapEngine_NoWrap,
        }.get(engine, _WrapEngine_NoWrap)
        if isinstance(self._wrapEngine, engine_class):
            return
        self._wrapEngine.clean()
        self._wrapEngine = engine_class(state=self._wrapState)
        self.rewrap()

    def size(self) -> int:
        '''Return the estimated wrapped row count.

        :return: wrapped size in screen rows.
        :rtype: int
        '''
        return self._wrapEngine.size()

    def documentLineCount(self) -> int:
        '''Return the number of logical data lines in the document.

        :return: document line count.
        :rtype: int
        '''
        return self._wrapState.textDocument.lineCount()

    def _documentDataLine(self, line:int) -> Optional[TTkString]:
        '''Get one document line through the document thread-safe API.'''
        return self._wrapState.textDocument.dataLine(line)

    def wrapWidth(self) -> int:
        '''Return the current wrap width in terminal cells.

        :return: wrap width.
        :rtype: int
        '''
        return self._wrapState.size

    def setWrapWidth(self, width:int) -> None:
        '''Set wrap width and trigger a full rewrap.

        :param width: target width in terminal cells.
        :type width: int
        '''
        self._wrapState.size = width
        self.rewrap()

    def wordWrapMode(self) -> TTkK.WrapMode:
        '''Return the active word-wrap mode.

        :return: current wrap mode.
        :rtype: :py:class:`TTkK.WrapMode`
        '''
        return self._wrapState.wordWrapMode

    def setWordWrapMode(self, mode:TTkK.WrapMode) -> None:
        '''Set the word-wrap mode and invalidate cached wrapping.

        :param mode: new wrap mode.
        :type mode: :py:class:`TTkK.WrapMode`
        '''
        self._wrapState.wordWrapMode = mode
        self.rewrap()

    def screenRows(self, y:int, h:int) -> List[_WrapLine]:
        '''Return wrapped slices visible in the requested viewport.

        :param y: first screen row.
        :type y: int
        :param h: number of rows to extract.
        :type h: int

        :return: wrapped row slices.
        :rtype: List[:py:class:`_WrapLine`]
        '''
        if h <= 0:
            return []
        return self._wrapEngine.screenRows(y=y,h=h)

    def rewrap(self) -> None:
        self._wrapEngine.rewrap()
        self.wrapChanged.emit()

    def dataToScreenPosition(self, line:int, pos:int) -> Tuple[int, int]:
        '''Map a document position to wrapped screen coordinates.

        :param line: logical line index.
        :type line: int
        :param pos: character position in the logical line.
        :type pos: int
        :return: ``(x, y)`` wrapped screen coordinates.
        :rtype: Tuple[int, int]
        '''
        return self._wrapEngine.dataToScreenPosition(line=line, pos=pos)

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Map wrapped screen coordinates to a document position.

        :param x: horizontal screen coordinate.
        :type x: int
        :param y: vertical screen coordinate.
        :type y: int
        :return: ``(line, pos)`` document position.
        :rtype: Tuple[int, int]
        '''
        return self._wrapEngine.screenToDataPosition(x=x, y=y)

    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Snap a screen position to the nearest editable character cell.

        :param x: horizontal widget-relative coordinate.
        :type x: int
        :param y: vertical widget-relative coordinate.
        :type y: int
        :return: normalized ``(x, y)`` screen position.
        :rtype: Tuple[int, int]
        '''
        return self._wrapEngine.normalizeScreenPosition(x=x, y=y)
