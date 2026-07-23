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

from typing import Any

from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

from .terminal_screen import _TTkTerminalScreen

class _TTkTerminalViewBase(TTkAbstractScrollView):
    __slots__ = (
        '_termLoop', '_newSize',
        '_clipboard', '_selecting',
        '_buffer_lines', '_buffer_screen',
        '_keyboard', '_mouse', '_terminal',
        '_screen_current', '_screen_normal', '_screen_alt',
        # Signals
        '_bell',
        '_titleChanged', '_terminalClosed', '_textSelected',
        '_termData','_termResized'
    )

    _newSize: tuple[int,int] | None
    _keyboard: Any
    _mouse: Any
    _terminal: Any
    _screen_current: _TTkTerminalScreen
    _screen_normal: _TTkTerminalScreen
    _screen_alt: _TTkTerminalScreen

    def _screenChanged(self) -> None: ...

