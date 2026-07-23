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

__all__:list[str] = []

from abc import abstractmethod
import collections
from typing import Any

from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.signal import pyTTkSignal

class _TTkTerminalScreenBase():
    __slots__ = (
        '_lines',
        '_terminalCursor', '_terminalCursor_save',
        '_selectCursor',
        '_scrollingRegion',
        '_bufferSize', '_bufferedLines',
        '_w', '_h', '_color', '_canvas',
        '_canvasNewLine', '_canvasLineSize',
        '_last',
        'bell', 'bufferedLinesChanged',
    )

    _w: int
    _h: int
    _color: TTkColor
    _canvas: TTkCanvas
    _canvasNewLine: list[bool]
    _canvasLineSize: list[int]
    _terminalCursor: tuple[int, int]
    _terminalCursor_save: tuple[int, int]
    _scrollingRegion: tuple[int, int]
    _bufferedLines: collections.deque
    _bufferSize: int
    _last: 'str | None'
    _selectCursor: Any
    _lines: Any
    bell: pyTTkSignal
    bufferedLinesChanged: pyTTkSignal

    @abstractmethod
    def restoreCursor(self) -> None: ...

    @abstractmethod
    def saveCursor(self) -> None: ...

    @abstractmethod
    def _pushTxt(self, txt: str, irm: bool = False) -> None: ...

    @abstractmethod
    def _CSI_S_SU(self, ps: int, _: Any = None) -> None: ...

    @abstractmethod
    def _CSI_T_SD(self, ps: int, _: Any = None) -> None: ...
