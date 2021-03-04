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

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkWidgets.widget import *
from TermTk.TTkTemplates.color import TColor
from TermTk.TTkTemplates.text  import TText

class TTkLabel(TTkWidget, TColor, TText):
    __slots__ = ('_color', '_text')
    def __init__(self, *args, **kwargs):
        TColor.__init__(self, *args, **kwargs)
        TText.__init__(self, *args, **kwargs)
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkLabel' )
        # self.setMinimumSize(len(self.text), 1)
        self.textUpdated(self.text)

    def paintEvent(self):
        self._canvas.drawText(pos=(0,0), text=' '*self.width(), color=self.color)
        self._canvas.drawText(pos=(0,0), text=self.text, color=self.color)

    def textUpdated(self, text):
        w, h = self.size()
        if w<len(text) or h<1:
            self.resize(len(text),1)
        self.setMinimumSize(len(text), 1)
        self.update()

    def colorUpdated(self, color):
        self.update()