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

__all__ = ['TTkLabel']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSlot
from TermTk.TTkWidgets.widget import TTkWidget

class TTkLabel(TTkWidget):
    '''TTkLabel'''

    classStyle = {
                'default':  {'color': TTkColor.RST          },
                'disabled': {'color': TTkColor.fg('#888888')},
            }

    __slots__ = ('_text', '_alignment')
    def __init__(self, *,
                 text:TTkString="",
                 color:TTkColor=None,
                 alignment:TTkK.Alignment=TTkK.LEFT_ALIGN,
                 **kwargs) -> None:
        if issubclass(type(text), TTkString):
            self._text = text.split('\n')
        else:
            self._text = TTkString(text).split('\n')
        self._alignment = alignment

        self.setDefaultSize(kwargs, max(t.termWidth() for t in  self._text), len(self._text))
        super().__init__(**kwargs)
        if color:
            self.setColor(color)
        self._textUpdated()

    def alignment(self):
        return self._alignment

    @pyTTkSlot(TTkK.Alignment)
    def setAlignment(self, alignment: TTkK.Alignment) -> None:
        if self._alignment == alignment:
            return
        self._alignment = alignment
        self.update()

    def color(self) ->TTkColor:
        '''color'''
        return self.style()['default']['color']

    @pyTTkSlot(TTkColor)
    def setColor(self, color:TTkColor):
        '''setColor'''
        self.mergeStyle({'default':{'color':color}})

    def text(self) -> TTkString:
        '''text'''
        return TTkString('\n').join(self._text)

    @pyTTkSlot(str)
    def setText(self, text:TTkString):
        '''setText'''
        if self.text().sameAs(text): return
        if issubclass(type(text), TTkString):
            self._text  = text.split('\n')
        else:
            self._text  = TTkString(text).split('\n')
        self._textUpdated()

    def paintEvent(self, canvas: TTkCanvas) -> None:
        style = self.currentStyle()
        color = style['color']

        forceColor = color!=TTkColor.RST

        w = self.width()
        for y,text in enumerate(self._text):
            canvas.drawText(pos=(0,y), text=' '*w, color=color, forceColor=forceColor)
            canvas.drawText(pos=(0,y), text=text, width=w, alignment=self._alignment, color=color, forceColor=forceColor)

    def _textUpdated(self):
        w, h = self.size()
        textWidth = max(t.termWidth() for t in  self._text)
        if w<textWidth or h<len(self._text):
            self.resize(textWidth,len(self._text))
        self.setMinimumSize(textWidth, 1)
        self.update()

