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
from TermTk.TTkWidgets.scrollbar import TTkScrollBar


class _TTkTextEditView(TTkWidget):
    __slots__ = ('_lines','_moveTo')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTextEditView' )
        self._lines = []
        self._moveTo = 0

    @pyTTkSlot(str)
    def setText(self, text):
        self._lines = text.split('\n')
        self.update()

    def paintEvent(self):
        y = 0
        for t in self._lines[self._moveTo:]:
            self._canvas.drawText(pos=(0,y), text=t)
            y+=1

    def wheelEvent(self, evt):
        delta = TTkCfg.scrollDelta
        if evt.evt == TTkK.WHEEL_Up:
            delta = -delta
        self.scrollTo(self._moveTo + delta)
        self.update()
        return True

    @pyTTkSlot(int)
    def scrollTo(self, to):
        # TTkLog.debug(f"to:{to},h{self._height},size:{len(self._tableData)}")
        max = len(self._lines) - self.height()
        if to>max: to=max
        if to<0: to=0
        self._moveTo = to
        self.update()

class TTkTextEdit(TTkWidget):
    __slots__ = ('_textEdit', '_vscroller', '_hscroller')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTextEdit' )
        self._textEdit = _TTkTextEditView()
        self._vscroller = TTkScrollBar(orientation=TTkK.VERTICAL)
        self._hscroller = TTkScrollBar(orientation=TTkK.HORIZONTAL)
        self.setLayout(TTkGridLayout())
        self.layout().addWidget(self._textEdit,0,0)
        self.layout().addWidget(self._vscroller,0,1)

    @pyTTkSlot(str)
    def setText(self, text):
        self._textEdit.setText(text)
