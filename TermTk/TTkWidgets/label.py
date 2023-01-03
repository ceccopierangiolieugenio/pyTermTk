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

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSlot
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkTemplates.color import TColor

class TTkLabel(TTkWidget, TColor):
    __slots__ = ('_text')
    def __init__(self, *args, **kwargs):
        TColor.__init__(self, *args, **kwargs)

        text = kwargs.get('text', TTkString() )
        if issubclass(type(text), TTkString):
            self._text = text
        else:
            self._text = TTkString(text)

        self.setDefaultSize(kwargs, self._text.termWidth(), 1)
        TTkWidget.__init__(self, *args, **kwargs)
        self._textUpdated()

    def text(self):
        return self._text

    @pyTTkSlot(str)
    def setText(self, text):
        if self._text != text:
            if issubclass(type(text), TTkString):
                self._text  = text
            else:
                self._text  = TTkString(text)
            self._textUpdated()

    def paintEvent(self):
        forceColor = self.color!=TTkColor.RST
        self._canvas.drawText(pos=(0,0), text=' '*self.width(), color=self.color, forceColor=forceColor)
        self._canvas.drawText(pos=(0,0), text=self._text, color=self.color, forceColor=forceColor)

    def _textUpdated(self):
        w, h = self.size()
        textWidth = self._text.termWidth()
        if w<textWidth or h<1:
            self.resize(textWidth,1)
        self.setMinimumSize(textWidth, 1)
        self.update()

    def colorUpdated(self, color):
        self.update()

    _ttkProperties = {
        'Text' : {
                'init': {'name':'text',  'type':TTkString },
                'get':  {'cb':text,      'type':TTkString } ,
                'set':  {'cb':setText,   'type':TTkString } },
    }