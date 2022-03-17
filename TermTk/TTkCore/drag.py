#!/usr/bin/env python3

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

from TermTk.TTkCore.string    import TTkString
from TermTk.TTkCore.helper    import TTkHelper
from TermTk.TTkCore.canvas    import TTkCanvas
from TermTk.TTkWidgets.widget import TTkWidget

class _TTkDragDisplayWidget(TTkWidget):
    __slots__ = ('_pixmap')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkDragDisplayWidget' )
        self._x, self._y = TTkHelper.mousePos()

    def setPixmap(self, pixmap):
        w,h = pixmap.size()
        self._pixmap = pixmap
        self.resize(w,h)

    def paintEvent(self):
        _,_,w,h = self.geometry()
        self._canvas.paintCanvas(self._pixmap, (0,0,w,h), (0,0,w,h), (0,0,w,h))

class TTkDrag():
    __slots__ = ('_data', '_pixmap', '_showPixmap')
    def __init__(self):
        self._data = None
        self._showPixmap = True
        self._pixmap = _TTkDragDisplayWidget(size=(5,1))
        pixmap = TTkCanvas(width=5, height=1)
        pixmap.drawText(pos=(0,0), text='[...]')
        self._pixmap.setPixmap(pixmap)

    def setData(self, data):
        self._data = data

    def data(self):
        return self._data

    def setPixmap(self, pixmap):
        if issubclass(type(pixmap),TTkWidget):
            pixmap.getCanvas().updateSize()
            pixmap.paintEvent()
            pixmap = pixmap.getCanvas()
        if type(pixmap) is TTkCanvas:
            pixmap.updateSize()
            self._pixmap.setPixmap(pixmap)

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
