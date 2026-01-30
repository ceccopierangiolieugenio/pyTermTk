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

__all__ = ['TTkAbstractScrollViewInterface', 'TTkAbstractScrollView', 'TTkAbstractScrollViewLayout', 'TTkAbstractScrollViewGridLayout']

from typing import Tuple

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

from TermTk.TTkWidgets.container import TTkContainer

from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout

class TTkAbstractScrollViewInterface():
    '''
    The :py:class:`TTkAbstractScrollViewInterface` provide the basic interface that can be used in :py:class:`TTkAbstractScrollArea` to enable on-demand scroll bars.

    When subclassing :py:class:`TTkAbstractScrollViewInterface`,
    you must implement :meth:`viewFullAreaSize`, :meth:`viewDisplayedSize`, :meth:`getViewOffsets`, and :meth:`viewMoveTo`.

    This interface is implemented in the following specialised classes:

    * :py:class:`TTkAbstractScrollView`
    * :py:class:`TTkAbstractScrollViewLayout`
    * :py:class:`TTkAbstractScrollViewGridLayout`
    '''

    viewMovedTo:pyTTkSignal
    '''
    This signal is emitted when the view content move to a new position (x,y),

    :param x: the new horizontal offset
    :type x: int
    :param y: the new vertical offset
    :type y: int
    '''
    viewSizeChanged:pyTTkSignal
    '''
    This signal is emitted when the view content size changed

    :param width: the new width
    :type width: int
    :param height: the new height
    :type height: int
    '''
    viewChanged:pyTTkSignal
    '''
    This signal is emitted whenever there is a change in the view content topology (size,pos)

    .. note:: This signal must be implemented in any implementation
              of :py:class:`TTkAbstractScrollView` to notify that the view content boudaries changed
    '''

    def __init__(self) -> None:
        pass

    # Override this function
    def viewFullAreaSize(self) -> Tuple[int,int]:
        '''
        This method returns the full widget area size of the :py:class:`TTkAbstractScrollViewInterface` implementation.

        This is required to `TTkAbstractScrollArea` implementation to handle the on-demand scroll bars.

        .. note:: Reimplement this function to handle this event

        :return: the full area size as a tuple of 2 int elements (width,height)
        :rtype: tuple[int,int]
        '''
        raise NotImplementedError()

    # Override this function
    def viewDisplayedSize(self) -> Tuple[int,int]:
        '''
        This method returns the displayed size of the :py:class:`TTkAbstractScrollViewInterface` implementation.

        .. note::

            Reimplement this function to handle this event

            This method is already implemented in the following classes:

            * :py:class:`TTkAbstractScrollView`
            * :py:class:`TTkAbstractScrollViewLayout`
            * :py:class:`TTkAbstractScrollViewGridLayout`

        Unless a different iplementation is required, by default it should return :py:meth:`TTkWidget.size`

        :return: the displayed size as a tuple of 2 int elements (width,height)
        :rtype: tuple[int,int]
        '''
        raise NotImplementedError()

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int) -> None:
        '''
        This method is used to set the vertical and horizontal offsets of the :py:class:`TTkAbstractScrollViewInterface`

        .. note::

            Reimplement this function to handle this event

            This method is already implemented in the following classes:
             * :py:class:`TTkAbstractScrollView`
             * :py:class:`TTkAbstractScrollViewLayout`
             * :py:class:`TTkAbstractScrollViewGridLayout`

        :param x: the horizontal position
        :type x: int
        :param y: the vertical position
        :type y: int
        '''
        raise NotImplementedError()

    def getViewOffsets(self) -> Tuple[int,int]:
        '''
        Retrieve the vertical and horizontal offsets of the :py:class:`TTkAbstractScrollViewInterface`

        .. note::

            Reimplement this function to handle this event

            This method is already implemented in the following classes:
             * :py:class:`TTkAbstractScrollView`
             * :py:class:`TTkAbstractScrollViewLayout`
             * :py:class:`TTkAbstractScrollViewGridLayout`

        :return: the (x,y) offset
        :rtype: tuple[int,int]
        '''
        raise NotImplementedError()

class TTkAbstractScrollView(TTkContainer, TTkAbstractScrollViewInterface):
    '''
    The :py:class:`TTkAbstractScrollView` is a :py:class:`TTkContainer` widget that incude :py:class:`TTkAbstractScrollViewInterface` api.

    The placement of any widget inside this container will change accordingly to the offset of this view.

    This class is used in the convenience widget :py:class:`TTkScrollArea`
    '''

    viewMovedTo:pyTTkSignal
    '''
    This signal is emitted when the view content move to a new position (x,y),

    :param x: the new horizontal offset
    :type x: int
    :param y: the new vertical offset
    :type y: int
    '''
    viewSizeChanged:pyTTkSignal
    '''
    This signal is emitted when the view content size changed

    :param width: the new width
    :type width: int
    :param height: the new height
    :type height: int
    '''
    viewChanged:pyTTkSignal
    '''
    This signal is emitted whenever there is a change in the view content topology (size,pos)

    .. note:: This signal must be implemented in any implementation
              of :py:class:`TTkAbstractScrollView` to notify that the view content boudaries changed
    '''

    __slots__ = (
        '_viewOffsetX', '_viewOffsetY',
        # Signals
         'viewMovedTo', 'viewSizeChanged', 'viewChanged')

    def __init__(self, **kwargs) -> None:
        # Signals
        self.viewMovedTo = pyTTkSignal(int, int) # x, y
        self.viewSizeChanged = pyTTkSignal(int, int) # w, h
        self.viewChanged = pyTTkSignal()
        self._viewOffsetX = 0
        self._viewOffsetY = 0
        # Do NOT use super()
        TTkContainer.__init__(self, **kwargs)

    def viewDisplayedSize(self) -> Tuple[int,int]:
        ''' Return the displayed size of this view

        :return: the (width, height) of the view
        :rtype: tuple[int,int]
        '''
        return self.size()

    def viewFullAreaSize(self) -> Tuple[int,int]:
        ''' Return the full area size including padding

        :return: the (width, height) of the full area
        :rtype: tuple[int,int]
        '''
        t,b,l,r = self.getPadding()
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w+l+r, h+t+b

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int) -> None:
        ''' Move the view to the specified offset position

        :param x: the horizontal offset
        :type x: int
        :param y: the vertical offset
        :type y: int
        '''
        fw, fh = self.viewFullAreaSize()
        dw, dh = self.viewDisplayedSize()
        rangex = fw - dw
        rangey = fh - dh
        # TTkLog.debug(f"x:{x},y:{y}, full:{fw,fh}, display:{dw,dh}, range:{rangex,rangey}")
        x = max(0,min(rangex,x))
        y = max(0,min(rangey,y))
        # TTkLog.debug(f"x:{x},y:{y}, wo:{self._viewOffsetX,self._viewOffsetY}")
        if ( self._viewOffsetX == x and
             self._viewOffsetY == y ): # Nothing to do
            return
        self._viewOffsetX = x
        self._viewOffsetY = y
        self.viewMovedTo.emit(x,y)
        self.viewChanged.emit()
        self.update()

    def wheelEvent(self, evt: TTkMouseEvent) -> bool:
        ''' Handle mouse wheel events for scrolling

        :param evt: the mouse event
        :type evt: :py:class:`TTkMouseEvent`

        :return: True if the event was handled
        :rtype: bool
        '''
        delta = TTkCfg.scrollDelta
        offx, offy = self.getViewOffsets()
        if evt.evt == TTkK.WHEEL_Up:
            self.viewMoveTo(offx, offy - delta)
        elif evt.evt == TTkK.WHEEL_Down:
            self.viewMoveTo(offx, offy + delta)
        elif evt.evt == TTkK.WHEEL_Left:
            self.viewMoveTo(offx - delta, offy)
        elif evt.evt == TTkK.WHEEL_Right:
            self.viewMoveTo(offx + delta, offy)
        return True

    def resizeEvent(self, w: int, h: int) -> None:
        ''' Handle resize events

        :param w: the new width
        :type w: int
        :param h: the new height
        :type h: int
        '''
        self.viewMoveTo(self._viewOffsetX, self._viewOffsetY)
        self.viewSizeChanged.emit(w,h)
        self.viewChanged.emit()

    def update(self, repaint: bool = True, updateLayout: bool = False, updateParent: bool = False) -> None:
        ''' Update the widget and emit viewChanged signal if layout is updated

        :param repaint: trigger a repaint, defaults to True
        :type repaint: bool, optional
        :param updateLayout: trigger a layout update, defaults to False
        :type updateLayout: bool, optional
        :param updateParent: trigger a parent update, defaults to False
        :type updateParent: bool, optional
        '''
        if updateLayout:
            self.viewChanged.emit()
        return super().update(repaint, updateLayout, updateParent)

    def setPadding(self, top: int, bottom: int, left: int, right: int) -> None:
        ''' Set the padding and emit viewChanged signal

        :param top: the top padding
        :type top: int
        :param bottom: the bottom padding
        :type bottom: int
        :param left: the left padding
        :type left: int
        :param right: the right padding
        :type right: int
        '''
        super().setPadding(top, bottom, left, right)
        self.viewChanged.emit()

    def getViewOffsets(self) -> Tuple[int,int]:
        '''
        Retrieve the vertical and horizontal offsets of the :py:class:`TTkAbstractScrollViewInterface`

        .. note::

            Reimplement this function to handle this event

            This method is already implemented in the following classes:
             * :py:class:`TTkAbstractScrollView`
             * :py:class:`TTkAbstractScrollViewLayout`
             * :py:class:`TTkAbstractScrollViewGridLayout`

        :return: the (x,y) offset
        :rtype: tuple[int,int]
        '''
        return self._viewOffsetX, self._viewOffsetY

class TTkAbstractScrollViewLayout(TTkLayout, TTkAbstractScrollViewInterface):
    '''
    :py:class:`TTkAbstractScrollViewLayout`
    '''

    viewMovedTo:pyTTkSignal
    '''
    This signal is emitted when the view content move to a new position (x,y),

    :param x: the new horizontal offset
    :type x: int
    :param y: the new vertical offset
    :type y: int
    '''
    viewSizeChanged:pyTTkSignal
    '''
    This signal is emitted when the view content size changed

    :param width: the new width
    :type width: int
    :param height: the new height
    :type height: int
    '''
    viewChanged:pyTTkSignal
    '''
    This signal is emitted whenever there is a change in the view content topology (size,pos)

    .. note:: This signal must be implemented in any implementation
              of :py:class:`TTkAbstractScrollView` to notify that the view content boudaries changed
    '''

    __slots__ = (
        '_viewOffsetX', '_viewOffsetY',
        # Signals
         'viewMovedTo', 'viewSizeChanged', 'viewChanged', '_excludeEvent')

    def __init__(self, *args, **kwargs) -> None:
        # Signals
        self.viewMovedTo = pyTTkSignal(int, int) # x, y
        self.viewSizeChanged = pyTTkSignal(int, int) # w, h
        self.viewChanged = pyTTkSignal()
        self._viewOffsetX = 0
        self._viewOffsetY = 0
        self._excludeEvent = False
        TTkLayout.__init__(self, *args, **kwargs)

    def viewFullAreaSize(self) -> Tuple[int,int]:
        ''' Return the full area size of the layout

        :return: the (width, height) of the full area
        :rtype: tuple[int,int]
        '''
        _,_,w,h = self.fullWidgetAreaGeometry()
        return w,h

    def viewDisplayedSize(self) -> Tuple[int,int]:
        ''' Return the displayed size of the layout

        :return: the (width, height) of the displayed area
        :rtype: tuple[int,int]
        '''
        _,_,w,h = self.geometry()
        return w,h

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int) -> None:
        ''' Move the view to the specified offset position

        :param x: the horizontal offset
        :type x: int
        :param y: the vertical offset
        :type y: int
        '''
        self.setOffset(-x,-y)

    def setGeometry(self, x: int, y: int, w: int, h: int) -> None:
        ''' Set the geometry and emit viewChanged signal

        :param x: the horizontal position
        :type x: int
        :param y: the vertical position
        :type y: int
        :param w: the width
        :type w: int
        :param h: the height
        :type h: int
        '''
        TTkLayout.setGeometry(self, x, y, w, h)
        self.viewChanged.emit()

    def getViewOffsets(self) -> Tuple[int,int]:
        '''
        Retrieve the vertical and horizontal offsets of the :py:class:`TTkAbstractScrollViewInterface`

        .. note::

            Reimplement this function to handle this event

            This method is already implemented in the following classes:
             * :py:class:`TTkAbstractScrollView`
             * :py:class:`TTkAbstractScrollViewLayout`
             * :py:class:`TTkAbstractScrollViewGridLayout`

        :return: the (x,y) offset
        :rtype: tuple[int,int]
        '''
        return self._viewOffsetX, self._viewOffsetY

class TTkAbstractScrollViewGridLayout(TTkGridLayout, TTkAbstractScrollViewInterface):
    '''
    :py:class:`TTkAbstractScrollViewGridLayout`
    '''

    viewMovedTo:pyTTkSignal
    '''
    This signal is emitted when the view content move to a new position (x,y),

    :param x: the new horizontal offset
    :type x: int
    :param y: the new vertical offset
    :type y: int
    '''
    viewSizeChanged:pyTTkSignal
    '''
    This signal is emitted when the view content size changed

    :param width: the new width
    :type width: int
    :param height: the new height
    :type height: int
    '''
    viewChanged:pyTTkSignal
    '''
    This signal is emitted whenever there is a change in the view content topology (size,pos)

    .. note:: This signal is normally emitted from any implementation
              of :py:class:`TTkAbstractScrollView` to notify that the view content boudaries changed
    '''

    __slots__ = (
        '_viewOffsetX', '_viewOffsetY',
        '_excludeEvent',
        # Signals
         'viewMovedTo', 'viewSizeChanged', 'viewChanged')

    def __init__(self, *args, **kwargs) -> None:
        # Signals
        self.viewMovedTo = pyTTkSignal(int, int) # x, y
        self.viewSizeChanged = pyTTkSignal(int, int) # w, h
        self.viewChanged = pyTTkSignal()
        self._viewOffsetX = 0
        self._viewOffsetY = 0
        self._excludeEvent = False
        TTkGridLayout.__init__(self, *args, **kwargs)

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int) -> None:
        ''' Move the view to the specified offset position and propagate to child widgets

        :param x: the horizontal offset
        :type x: int
        :param y: the vertical offset
        :type y: int
        '''
        fw, fh = self.viewFullAreaSize()
        dw, dh = self.viewDisplayedSize()
        rangex = fw - dw
        rangey = fh - dh
        # TTkLog.debug(f"x:{x},y:{y}, full:{fw,fh}, display:{dw,dh}, range:{rangex,rangey}")
        x = max(0,min(rangex,x))
        y = max(0,min(rangey,y))
        # TTkLog.debug(f"x:{x},y:{y}, wo:{self._viewOffsetX,self._viewOffsetY}")
        if self._viewOffsetX == x and \
           self._viewOffsetY == y: # Nothing to do
            return
        self._excludeEvent = True
        for widget in self.iterWidgets():
            if isinstance(widget, TTkAbstractScrollViewInterface):
                widget.viewMoveTo(x,y)
        self._excludeEvent = False
        self._viewOffsetX = x
        self._viewOffsetY = y
        self.viewMovedTo.emit(x,y)
        self.viewChanged.emit()
        self.update()

    def setGeometry(self, x: int, y: int, w: int, h: int) -> None:
        ''' Set the geometry and emit viewChanged signal

        :param x: the horizontal position
        :type x: int
        :param y: the vertical position
        :type y: int
        :param w: the width
        :type w: int
        :param h: the height
        :type h: int
        '''
        TTkGridLayout.setGeometry(self, x, y, w, h)
        self.viewChanged.emit()

    @pyTTkSlot()
    def _viewChanged(self) -> None:
        ''' Internal slot to handle viewChanged signal from child widgets '''
        if self._excludeEvent: return
        self.viewChanged.emit()

    @pyTTkSlot(int,int)
    def _viewMovedTo(self, x: int, y: int) -> None:
        ''' Internal slot to handle viewMovedTo signal from child widgets

        :param x: the horizontal offset
        :type x: int
        :param y: the vertical offset
        :type y: int
        '''
        if self._excludeEvent: return
        self.viewMoveTo(x, y)

    def addWidget(self, widget, row=None, col=None, rowspan=1, colspan=1):
        ''' Add a widget that implements :py:class:`TTkAbstractScrollViewInterface` to the grid layout

        :param widget: the widget to be added (must implement TTkAbstractScrollViewInterface)
        :type widget: :py:class:`TTkWidget`
        :param row: the row position, optional, defaults to None
        :type row: int, optional
        :param col: the column position, optional, defaults to None
        :type col: int, optional
        :param rowspan: number of rows to span, defaults to 1
        :type rowspan: int, optional
        :param colspan: number of columns to span, defaults to 1
        :type colspan: int, optional

        :raises TypeError: if widget does not implement TTkAbstractScrollViewInterface
        '''
        if not issubclass(type(widget),TTkAbstractScrollViewInterface):
            raise TypeError("TTkAbstractScrollViewInterface is required in TTkAbstractScrollViewGridLayout.addWidget(...)")
        widget.viewChanged.connect(self._viewChanged)
        widget.viewMovedTo.connect(self._viewMovedTo)
        return TTkGridLayout.addWidget(self, widget, row, col, rowspan, colspan)

    def addItem(self, item, row=None, col=None, rowspan=1, colspan=1):
        ''' Add a layout item that implements :py:class:`TTkAbstractScrollViewInterface` to the grid layout

        :param item: the layout item to be added (must implement TTkAbstractScrollViewInterface)
        :type item: :py:class:`TTkLayoutItem`
        :param row: the row position, optional, defaults to None
        :type row: int, optional
        :param col: the column position, optional, defaults to None
        :type col: int, optional
        :param rowspan: number of rows to span, defaults to 1
        :type rowspan: int, optional
        :param colspan: number of columns to span, defaults to 1
        :type colspan: int, optional

        :raises TypeError: if item does not implement TTkAbstractScrollViewInterface
        '''
        if not issubclass(type(item),TTkAbstractScrollViewInterface):
            raise TypeError("TTkAbstractScrollViewInterface is required in TTkAbstractScrollViewGridLayout.addItem(...)")
        return TTkGridLayout.addItem(self, item, row, col, rowspan, colspan)

    # Override this function
    def viewFullAreaSize(self) -> Tuple[int,int]:
        ''' Return the full area size by computing the maximum size from all child widgets

        :return: the (width, height) of the full area
        :rtype: tuple[int,int]
        '''
        w,h=0,0
        for widget in self.iterWidgets():
            if isinstance(widget, TTkAbstractScrollViewInterface):
                ww,wh = widget.viewFullAreaSize()
                w = max(w,ww)
                h = max(h,wh)
        return w,h

    # Override this function
    def viewDisplayedSize(self) -> Tuple[int,int]:
        ''' Return the displayed size by computing the maximum displayed size from all child widgets

        :return: the (width, height) of the displayed area
        :rtype: tuple[int,int]
        '''
        w,h=0,0
        for widget in self.iterWidgets():
            if isinstance(widget, TTkAbstractScrollViewInterface):
                ww,wh = widget.viewDisplayedSize()
                w = max(w,ww)
                h = max(h,wh)
        return w,h

    def getViewOffsets(self) -> Tuple[int,int]:
        '''
        Retrieve the vertical and horizontal offsets of the :py:class:`TTkAbstractScrollViewInterface`

        .. note::

            Reimplement this function to handle this event

            This method is already implemented in the following classes:
             * :py:class:`TTkAbstractScrollView`
             * :py:class:`TTkAbstractScrollViewLayout`
             * :py:class:`TTkAbstractScrollViewGridLayout`

        :return: the (x,y) offset
        :rtype: tuple[int,int]
        '''
        return self._viewOffsetX, self._viewOffsetY