#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import os
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkWidgets.widget import *
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.scrollbar import TTkScrollBar
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView


class _TTkTextEditView(TTkAbstractScrollView):
    __slots__ = ('_lines')
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTextEditView' )
        self._lines = []

    @pyTTkSlot(str)
    def setText(self, text):
        self._lines = [line for line in text.split('\n')]
        self.viewMoveTo(0, 0)
        self.viewChanged.emit()
        self.update()

    @pyTTkSlot(str)
    def setLines(self, lines):
        self._lines = lines
        self.viewMoveTo(0, 0)
        self.viewChanged.emit()
        self.update()

    def viewFullAreaSize(self) -> (int, int):
        return self.width(), len(self._lines)

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def paintEvent(self):
        _, oy = self.getViewOffsets()
        for y, t in enumerate(self._lines[oy:]):
            self._canvas.drawText(pos=(0,y), text=t)

class TTkTextEdit(TTkAbstractScrollArea):
    __slots__ = ('_textEditView', 'setText', 'setColoredLines')
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTextEdit' )
        self._textEditView = _TTkTextEditView()
        self.setViewport(self._textEditView)
        self.setText = self._textEditView.setText
        self.setLines = self._textEditView.setLines
