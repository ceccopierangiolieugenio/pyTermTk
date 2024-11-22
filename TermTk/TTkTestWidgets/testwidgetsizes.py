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

__all__ = ['TTkTestWidgetSizes']

from TermTk.TTkWidgets.frame import TTkFrame

class TTkTestWidgetSizes(TTkFrame):
    ID = 1
    def __init__(self, *,
                 name:str=None,
                 **kwargs) -> None:
        name = name if name else f"TestWidgetSizes-{TTkTestWidgetSizes.ID}"
        super().__init__(name=name, **kwargs)
        TTkTestWidgetSizes.ID+=1

    def paintEvent(self, canvas):
        t,_,l,_ = self.getPadding()
        w,h = self.size()
        style = self.currentStyle()
        color = style['color']
        if color.hasBackground():
            canvas.fill(pos=(0,0), size=(w,h), color=color)
        borderColor = style['borderColor']
        canvas.drawText(pos=(l,t+0), color=color, text=f"Test Widget [{self._name}]")
        canvas.drawText(pos=(l,t+1), color=color, text=f"x,y ({self._x},{self._y})")
        canvas.drawText(pos=(l,t+2), color=color, text=f"w,h ({self._width},{self._height})")
        canvas.drawText(pos=(l,t+3), color=color, text=f"max w,h ({self._maxw},{self._maxh})")
        canvas.drawText(pos=(l,t+4), color=color, text=f"min w,h ({self._minw},{self._minh})")
        TTkFrame.paintEvent(self, canvas)
