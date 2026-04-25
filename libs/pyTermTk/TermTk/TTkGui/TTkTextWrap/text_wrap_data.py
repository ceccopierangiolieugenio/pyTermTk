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
from typing import List

from TermTk.TTkCore.constant import TTkK

from TermTk.TTkGui.textdocument import TTkTextDocument

@dataclass
class _ReWrapData():
    '''Incremental rewrap change descriptor.

    :param line: first changed line in the source document.
    :type line: int
    :param added: number of lines inserted at ``line``.
    :type added: int
    :param removed: number of lines removed at ``line``.
    :type removed: int
    '''
    line:int
    added:int
    removed:int

@dataclass
class _WrapLine():
    '''A wrapped row fragment mapped to the source document line.

    :param line: zero-based source line index.
    :type line: int
    :param start: inclusive start character offset in the source line.
    :type start: int
    :param stop: exclusive stop character offset in the source line.
    :type stop: int
    '''
    __slots__ = ('line', 'start', 'stop')
    line:int
    start: int
    stop:int


@dataclass
class _WrapState():
    '''Shared mutable state used by wrap engine implementations.

    :param size: wrapping width in terminal cells.
    :type size: int
    :param tabSpaces: tab expansion width.
    :type tabSpaces: int
    :param textDocument: source text document.
    :type textDocument: :py:class:`TTkTextDocument`
    :param wordWrapMode: wrapping mode selector.
    :type wordWrapMode: :py:class:`TTkK.WrapMode`
    '''
    __slots__ = ('textDocument', 'tabSpaces', 'size', 'wordWrapMode')
    size: int
    tabSpaces: int
    textDocument: TTkTextDocument
    wordWrapMode: TTkK.WrapMode

@dataclass
class _RetScreenRows():
    y:int
    rows: List[_WrapLine]
