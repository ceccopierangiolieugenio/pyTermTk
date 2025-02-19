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

__all__ = ['TTkAbstractScrollViewInterface', 'TTkAbstractScrollView', 'TTkAbstractScrollViewGridLayout']

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

    def __init__(self) -> None: pass

    # Override this function
    def viewFullAreaSize(self) -> tuple[int,int]:
        '''
        This method returns the full widget area size of the :py:class:`TTkAbstractScrollViewInterface` implementation.

        This is required to `TTkAbstractScrollArea` implementation to handle the on-demand scroll bars.

        .. note:: Reimplement this function to handle this event

        :return: the full area size as a tuple of 2 int elements (width,height)
        :rtype: tuple[int,int]
        '''
        raise NotImplementedError()

    # Override this function
    def viewDisplayedSize(self) -> tuple[int,int]:
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
    def viewMoveTo(self, x: int, y: int):
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

    def getViewOffsets(self) -> tuple:
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
    :param height: the new heighht
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

    def viewDisplayedSize(self) -> tuple[int,int]:
        return self.size()

    def viewFullAreaSize(self) -> tuple[int,int]:
        t,b,l,r = self.getPadding()
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w+l+r, h+t+b

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int):
        fw, fh = self.viewFullAreaSize()
        dw, dh = self.viewDisplayedSize()
        rangex = fw - dw
        rangey = fh - dh
        # TTkLog.debug(f"x:{x},y:{y}, full:{fw,fh}, display:{dw,dh}, range:{rangex,rangey}")
        x = max(0,min(rangex,x))
        y = max(0,min(rangey,y))
        # TTkLog.debug(f"x:{x},y:{y}, wo:{self._viewOffsetX,self._viewOffsetY}")
        if self._viewOffsetX == x and \
           self._viewOffsetY == y: # Nothong to do
            return
        self._viewOffsetX = x
        self._viewOffsetY = y
        self.viewMovedTo.emit(x,y)
        self.viewChanged.emit()
        self.update()

    def getViewOffsets(self) -> tuple:
        return self._viewOffsetX, self._viewOffsetY

    def wheelEvent(self, evt:TTkMouseEvent) -> bool:
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

    def resizeEvent(self, w, h):
        self.viewMoveTo(self._viewOffsetX, self._viewOffsetY)
        self.viewSizeChanged.emit(w,h)
        self.viewChanged.emit()

    def update(self, repaint=True, updateLayout=False, updateParent=False):
        if updateLayout:
            self.viewChanged.emit()
        return super().update(repaint, updateLayout, updateParent)

    def setPadding(self, top, bottom, left, right) -> None:
        super().setPadding(top, bottom, left, right)
        self.viewChanged.emit()

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
    :param height: the new heighht
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

    def viewFullAreaSize(self) -> tuple[int,int]:
        _,_,w,h = self.fullWidgetAreaGeometry()
        return w,h

    def viewDisplayedSize(self) -> tuple[int,int]:
        _,_,w,h = self.geometry()
        return w,h

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int):
        self.setOffset(-x,-y)

    def getViewOffsets(self) -> tuple:
        return self._viewOffsetX, self._viewOffsetY

    def setGeometry(self, x, y, w, h):
        TTkLayout.setGeometry(self, x, y, w, h)
        self.viewChanged.emit()

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
    :param height: the new heighht
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
    def viewMoveTo(self, x: int, y: int):
        fw, fh = self.viewFullAreaSize()
        dw, dh = self.viewDisplayedSize()
        rangex = fw - dw
        rangey = fh - dh
        # TTkLog.debug(f"x:{x},y:{y}, full:{fw,fh}, display:{dw,dh}, range:{rangex,rangey}")
        x = max(0,min(rangex,x))
        y = max(0,min(rangey,y))
        # TTkLog.debug(f"x:{x},y:{y}, wo:{self._viewOffsetX,self._viewOffsetY}")
        if self._viewOffsetX == x and \
           self._viewOffsetY == y: # Nothong to do
            return
        self._excludeEvent = True
        for widget in self.iterWidgets(recurse=False):
            widget.viewMoveTo(x,y)
        self._excludeEvent = False
        self._viewOffsetX = x
        self._viewOffsetY = y
        self.viewMovedTo.emit(x,y)
        self.viewChanged.emit()
        self.update()

    def getViewOffsets(self) -> tuple:
        return self._viewOffsetX, self._viewOffsetY

    def setGeometry(self, x, y, w, h):
        TTkGridLayout.setGeometry(self, x, y, w, h)
        self.viewChanged.emit()

    @pyTTkSlot()
    def _viewChanged(self):
        if self._excludeEvent: return
        self.viewChanged.emit()

    @pyTTkSlot(int,int)
    def _viewMovedTo(self, x, y):
        if self._excludeEvent: return
        self.viewMoveTo(x, y)

    def addWidget(self, widget, row=None, col=None, rowspan=1, colspan=1):
        if not issubclass(type(widget),TTkAbstractScrollViewInterface):
            raise TypeError("TTkAbstractScrollViewInterface is required in TTkAbstractScrollViewGridLayout.addWidget(...)")
        widget.viewChanged.connect(self._viewChanged)
        widget.viewMovedTo.connect(self._viewMovedTo)
        return TTkGridLayout.addWidget(self, widget, row, col, rowspan, colspan)

    def addItem(self, item, row=None, col=None, rowspan=1, colspan=1):
        if not issubclass(type(item),TTkAbstractScrollViewInterface):
            raise TypeError("TTkAbstractScrollViewInterface is required in TTkAbstractScrollViewGridLayout.addItem(...)")
        return TTkGridLayout.addItem(self, item, row, col, rowspan, colspan)

    # Override this function
    def viewFullAreaSize(self) -> tuple[int,int]:
        w,h=0,0
        for widget in self.iterWidgets(recurse=False):
            ww,wh = widget.viewFullAreaSize()
            w = max(w,ww)
            h = max(h,wh)
        return w,h

    # Override this function
    def viewDisplayedSize(self) -> tuple[int,int]:
        w,h=0,0
        for widget in self.iterWidgets(recurse=False):
            ww,wh = widget.viewDisplayedSize()
            w = max(w,ww)
            h = max(h,wh)
        return w,h

