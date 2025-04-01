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

__all__ = ['TTkTestAbstractScrollWidget']

from TermTk.TTkCore.signal import pyTTkSlot
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class TTkTestAbstractScrollWidget(TTkAbstractScrollView):
    ID = 1
    __slots__ = ('_areaPos','_areaSize')
    def __init__(self, *,
                 name:str=None,
                 areaSize:tuple=(10,10),
                 areaPos:tuple=(0,0),
                 **kwargs) -> None:
        name = name if name else f"TTkTestAbstractScrollWidget-{TTkTestAbstractScrollWidget.ID}"
        self._areaSize = areaSize
        self._areaPos = areaPos
        super().__init__(name=name, **kwargs)
        TTkTestAbstractScrollWidget.ID+=1
        self.viewChanged.connect(self._viewChangedHandler)

    @pyTTkSlot()
    def _viewChangedHandler(self):
        self._areaPos = self.getViewOffsets()
        self.update()

    def paintEvent(self, canvas):
        canvas.drawBox(pos=(0,0),size=(self._width,self._height))
        t,_,l,_ = self.getPadding()
        canvas.drawText(pos=(l+1,t+1+0), text=f"Test Widget [{self._name}]")
        canvas.drawText(pos=(l+1,t+1+1), text=f"x,y ({self._x},{self._y})")
        canvas.drawText(pos=(l+1,t+1+2), text=f"w,h ({self._width},{self._height})")
        canvas.drawText(pos=(l+1,t+1+3), text=f"max w,h ({self._maxw},{self._maxh})")
        canvas.drawText(pos=(l+1,t+1+4), text=f"min w,h ({self._minw},{self._minh})")
        canvas.drawText(pos=(l+1,t+1+5), text=f"areaSize {self._areaSize}")
        canvas.drawText(pos=(l+1,t+1+6), text=f"areaPos1  {self._areaPos}")
        canvas.drawText(pos=(l+1,t+1+7), text=f"areaPos2  ({self._areaPos[0]+self._width},{self._areaPos[1]+self._height})")

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        return True

    def mouseReleaseEvent(self, evt:TTkMouseEvent) -> bool:
        return True

    def viewFullAreaSize(self) -> tuple[int,int]:
        return self._areaSize



