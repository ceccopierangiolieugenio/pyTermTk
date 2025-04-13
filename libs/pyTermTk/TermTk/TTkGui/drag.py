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

__all__ = ['TTkDrag', 'TTkDnDEvent', 'TTkDnD']

from typing import Any

from TermTk.TTkCore.helper    import TTkHelper
from TermTk.TTkCore.canvas    import TTkCanvas
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

class _TTkDragDisplayWidget(TTkWidget):
    __slots__ = ('_pixmap')
    def __init__(self, **kwargs) -> None:
        self._pixmap = TTkCanvas(width=5, height=1)
        self._pixmap.drawText(pos=(0,0), text='[...]')
        super().__init__(**kwargs)
        self.setPixmap(self._pixmap, (0,0))

    def setPixmap(self, pixmap:TTkCanvas, hotSpot:tuple[int,int]) -> None:
        self.getCanvas().setTransparent(True)
        w,h = pixmap.size()
        hsx, hsy= hotSpot
        x, y = TTkHelper.mousePos()
        self._pixmap = pixmap
        self.setGeometry(x-hsx,y-hsy,w,h)

    def paintEvent(self, canvas:TTkCanvas) -> None:
        _,_,w,h = self.geometry()
        canvas.paintCanvas(self._pixmap, (0,0,w,h), (0,0,w,h), (0,0,w,h))

class TTkDnD():
    '''
    Base class for drag and drop operations.
    '''
    __slots__ = ('_data', '_hotSpot')
    def __init__(self, data:Any=None, hotspot:tuple[int,int]=(0,0)) -> None:
        '''
        :param data: The data attached to this Drag object, defaults to 0.
        :type data: Any
        :param hotSpot: The offset coordinates of the visual overlay relative to the mouse drag position.
        :type hotSpot: tuple[int,int]
        '''
        self._data = data
        self._hotSpot = hotspot

    def setData(self, data:Any) -> None:
        '''
        The data attached to this Drag object

        :param data: The data attached to this Drag object
        :type data: Any
        '''
        self._data = data

    def data(self) -> Any:
        '''
        Returns the data attached to this Drag object

        :return: The data attached to this Drag object
        :rtype:  Any
        '''
        return self._data

    def setHotSpot(self, pos:tuple[int,int]) -> None:
        '''
        Sets the position of the hot spot relative to the top-left corner of the pixmap used to the point specified by hotspot.

        :param pos: the hotspot position
        :type pos:  tuple[int,int]
        '''
        self._hotSpot = pos

    def hotSpot(self) -> tuple[int,int]:
        '''
        Returns the position of the hot spot relative to the top-left corner of the cursor.

        :return: the hotspot position
        :rtype:  tuple[int,int]
        '''
        return self._hotSpot

    def clone(self):
        '''
        Clone this event

        :return: the cloned event
        :rtype:  :py:class:`TTkDnD`
        '''
        return TTkDnD(data=self._data, hotspot=self._hotSpot)

class TTkDnDEvent(TTkDnD):
    '''
    Drag and Drop event class.
    '''
    __slots__ = ('_pos', 'x', 'y')
    def __init__(self, *, pos:tuple[int,int]=(0,0), **kwargs) -> None:
        '''
        :param pos: The position of the mouse cursor relative to the current widget.
        :type pos: tuple[int,int]
        '''
        self._pos = pos
        self.x, self.y = pos
        super().__init__(**kwargs)

    def pos(self) -> tuple[int,int]:
        '''
        Returns the position of the mouse cursor relative to the current widget.

        :return: the position.
        :rtype:  tuple[int,int]
        '''
        return self._pos

    def clone(self):
        '''
        Clone this event

        :return: the cloned event
        :rtype:  :py:class:`TTkDnDEvent`
        '''
        return TTkDnDEvent(data=self._data, hotspot=self._hotSpot, pos=self._pos)

class TTkDrag(TTkDnD):
    __slots__ = ('_pixmap', '_showPixmap')
    def __init__(self, **kwargs) -> None:
        self._showPixmap = True
        self._pixmap = _TTkDragDisplayWidget(size=(5,1))
        super().__init__(**kwargs)

    # def setPixmap(self, pixmap:TTkWidget|TTkCanvas) -> None:
    def setPixmap(self, pixmap:TTkWidget) -> None:
        '''
        Sets the pixmap used to represent the data in a drag and drop operation.
        If a :py:class:`TTkWidget` is provided as pixmap, its default rendering will be used in the pixmap :py:class:`TTkCanvas`.

        :param pixmap: the pixmap
        :type  pixmap: :py:class:`TTkWidget` or :py:class:`TTkCanvas`
        '''
        if issubclass(type(pixmap),TTkWidget):
            canvas = pixmap.getCanvas()
            canvas.updateSize()
            pixmap.paintEvent(canvas)
            pixmap = canvas
        if type(pixmap) is TTkCanvas:
            pixmap.updateSize()
            self._pixmap.setPixmap(pixmap, self._hotSpot)

    def pixmap(self) -> TTkCanvas:
        '''
        Returns the pixmap used to represent the data in a drag and drop operation.

        :return: the pixmap used to represent the data in a drag and drop operation.
        :rtype:  :py:class:`TTkCanvas`
        '''
        return self._pixmap

    def visible(self) -> bool:
        '''
        Returns pixmap's visibility status.

        :return: True if the pixmap is visible, False otherwise.
        :rtype:  bool
        '''
        return self._showPixmap

    def showPixmap(self) -> None:
        '''
        Shows the pixmap used to represent the data in a drag and drop operation.
        '''
        self._showPixmap = True

    def hidePixmap(self) -> None:
        '''
        Hides the pixmap used to represent the data in a drag and drop operation.
        '''
        self._showPixmap = False

    def exec(self) -> None:
        '''
        Starts the drag operation.
        '''
        TTkHelper.dndInit(self)

    def _toDropEvent(self, pos:tuple[int,int]) -> TTkDnDEvent:
        ret = TTkDnDEvent(data=self._data, hotspot=self._hotSpot, pos=pos)
        return ret

    def getDragEnterEvent(self, evt:TTkMouseEvent) -> TTkDnDEvent:
        '''
        Returns a Drag and Drop event for the DragEnter event.

        :param evt: The mouse event
        :type evt: :py:class:`TTkMouseEvent`

        :return: The Drag and Drop event
        :rtype:  :py:class:`TTkDnDEvent`
        '''
        return self._toDropEvent((evt.x, evt.y))

    def getDragLeaveEvent(self, evt:TTkMouseEvent) -> TTkDnDEvent:
        '''
        Returns a Drag and Drop event for the DragLeave event.

        :param evt: The mouse event
        :type evt: :py:class:`TTkMouseEvent`

        :return: The Drag and Drop event
        :rtype:  :py:class:`TTkDnDEvent`
        '''
        return self._toDropEvent((evt.x, evt.y))

    def getDragMoveEvent(self, evt:TTkMouseEvent) -> TTkDnDEvent:
        '''
        Returns a Drag and Drop event for the DragMove event.

        :param evt: The mouse event
        :type evt: :py:class:`TTkMouseEvent`

        :return: The Drag and Drop event
        :rtype:  :py:class:`TTkDnDEvent`
        '''
        return self._toDropEvent((evt.x, evt.y))

    def getDropEvent(self, evt:TTkMouseEvent) -> TTkDnDEvent:
        '''
        Returns a Drag and Drop event for the Drop event.

        :param evt: The mouse event
        :type evt: :py:class:`TTkMouseEvent`

        :return: The Drag and Drop event
        :rtype:  :py:class:`TTkDnDEvent`
        '''
        return self._toDropEvent((evt.x, evt.y))
