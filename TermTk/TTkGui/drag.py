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

__all__ = ['TTkDrag', 'TTkDropEvent']

from TermTk.TTkCore.helper    import TTkHelper
from TermTk.TTkCore.canvas    import TTkCanvas
from TermTk.TTkWidgets.widget import TTkWidget

class _TTkDragDisplayWidget(TTkWidget):
    __slots__ = ('_pixmap')

    def setPixmap(self, pixmap, hotSpot):
        self.getCanvas().setTransparent(True)
        w,h = pixmap.size()
        hsx, hsy= hotSpot
        x, y = TTkHelper.mousePos()
        self._pixmap = pixmap
        self.setGeometry(x-hsx,y-hsy,w,h)

    def paintEvent(self, canvas):
        _,_,w,h = self.geometry()
        canvas.paintCanvas(self._pixmap, (0,0,w,h), (0,0,w,h), (0,0,w,h))

class TTkDrag():
    __slots__ = ('_data', '_pixmap', '_showPixmap', '_hotSpot')
    def __init__(self):
        self._data = None
        self._showPixmap = True
        self._hotSpot = (0,0)
        self._pixmap = _TTkDragDisplayWidget(size=(5,1))
        pixmap = TTkCanvas(width=5, height=1)
        pixmap.drawText(pos=(0,0), text='[...]')
        self._pixmap.setPixmap(pixmap, self._hotSpot)

    def setData(self, data):
        self._data = data

    def data(self):
        return self._data

    def setHotSpot(self, x,y):
        self._hotSpot = (x,y)

    def hotSpot(self):
        return self._hotSpot

    def setPixmap(self, pixmap):
        if issubclass(type(pixmap),TTkWidget):
            canvas = pixmap.getCanvas()
            canvas.updateSize()
            pixmap.paintEvent(canvas)
            pixmap = canvas
        if type(pixmap) is TTkCanvas:
            pixmap.updateSize()
            self._pixmap.setPixmap(pixmap, self._hotSpot)

    def pixmap(self):
        return self._pixmap

    def visible(self):
        return self._showPixmap

    def showPixmap(self):
        self._showPixmap = True

    def hidePixmap(self):
        self._showPixmap = False

    def exec(self):
        TTkHelper.dndInit(self)

    @staticmethod
    def copy(drag):
        ret = TTkDropEvent()
        ret._data = drag._data
        ret._pixmap = drag._pixmap
        ret._hotSpot = drag._hotSpot
        return ret

    def getDragEnterEvent(self, evt):
        ret = TTkDropEvent.copy(self)
        ret._pos = (evt.x, evt.y)
        ret.x = evt.x
        ret.y = evt.y
        return ret

    def getDragLeaveEvent(self, evt):
        return self.getDragEnterEvent(evt)

    def getDragMoveEvent(self, evt):
        return self.getDragEnterEvent(evt)

    def getDropEvent(self, evt):
        return self.getDragEnterEvent(evt)


class TTkDropEvent(TTkDrag):
    __slots__ = ('_pos', 'x', 'y')

    def pos(self): return self._pos
