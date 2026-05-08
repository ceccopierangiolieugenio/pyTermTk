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

from __future__ import annotations

__all__ = ['TTkWidget']

from typing import ( TYPE_CHECKING, Callable, Any, List, Optional, Tuple, Union, Dict )

from TermTk.TTkCore.cfg       import TTkCfg, TTkGlbl
from TermTk.TTkCore.constant  import TTkK
from TermTk.TTkCore.log       import TTkLog
from TermTk.TTkCore.helper    import TTkHelper
from TermTk.TTkCore.color     import TTkColor
from TermTk.TTkCore.string    import TTkString
from TermTk.TTkCore.canvas    import TTkCanvas
from TermTk.TTkCore.signal    import pyTTkSignal, pyTTkSlot
from TermTk.TTkTemplates.dragevents import TDragEvents
from TermTk.TTkTemplates.mouseevents import TMouseEvents
from TermTk.TTkTemplates.keyevents import TKeyEvents
from TermTk.TTkLayouts.layout import TTkWidgetItem
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

if TYPE_CHECKING:
    from TermTk import TTkContainer

class TTkWidget(TMouseEvents, TKeyEvents, TDragEvents):
    ''' Widget sizes:

    ::

        Terminal area (i.e. XTerm) = TTk
        ┌─────────────────────────────────────────┐
        │                                         │
        │    TTkWidget     width                  │
        │ (x,y)┌─────────────────────────┐        │
        │      │                         │        │
        │      │                         │ height │
        │      │                         │        │
        │      │                         │        │
        │      │                         │        │
        │      └─────────────────────────┘        │
        └─────────────────────────────────────────┘

    The TTkWidget class is the base class of all user interface objects

    '''

    focusChanged:pyTTkSignal
    '''
    This signal is emitted whenever the focus status change
    i.e. with the :meth:`setFocus` or :meth:`clearFocus` methods

    :param status: the curent focus status
    :type status: bool
    '''
    sizeChanged:pyTTkSignal
    '''
    This signal is emitted whenever the widget size change

    :param width: the new widget width
    :type width: int
    :param height: the new widget height
    :type height: int
    '''
    currentStyleChanged:pyTTkSignal
    '''
    This signal is emitted whenever the widget stye change

    :param style: the new style applied
    :type style: dict
    '''
    closed:pyTTkSignal
    '''
    This signal is emitted whenever the widget is closed

    :param widget: the widget closed (=self)
    :type widget: TTkWidget
    '''

    classStyle = {
                'default':     {'color': TTkColor.RST,           'borderColor': TTkColor.RST},
                'disabled':    {'color': TTkColor.fg('#888888'), 'borderColor': TTkColor.fg('#888888')},
                # 'hover':       {'color': TTkColor.fg('#00FF00')+TTkColor.bg('#0077FF')},
                # 'checked':     {'color': TTkColor.fg('#00FF00')+TTkColor.bg('#00FFFF')},
                # 'clicked':     {'color': TTkColor.fg('#FFFF00')},
                # 'focus':       {'color': TTkColor.fg('#FFFF88')},
            }

    __slots__ = (
        '_name', '_parent',
        '_x', '_y', '_width', '_height',
        '_maxw', '_maxh', '_minw', '_minh',
        '_focus_policy',
        '_canvas', '_widgetItem',
        '_visible',
        '_enabled',
        '_style', '_currentStyle',
        '_toolTip',
        '_dropEventProxy',
        '_widgetCursor', '_widgetCursorEnabled', '_widgetCursorType',
        #Signals
        'focusChanged', 'sizeChanged', 'currentStyleChanged', 'closed')

    _name:str
    _parent:Optional[TTkContainer]
    _x:int
    _y:int
    _width:int
    _height:int
    _maxw:int
    _maxh:int
    _minw:int
    _minh:int
    _focus_policy:TTkK.FocusPolicy
    _canvas:TTkCanvas
    _widgetItem:TTkWidgetItem
    _visible:bool
    _enabled:bool
    _style:Dict
    _currentStyle:Dict
    _toolTip:TTkString
    _dropEventProxy:Any
    _widgetCursor:Tuple[int,int]
    _widgetCursorEnabled:bool
    _widgetCursorType:int

    def __init__(
            self,
            parent:Optional[TTkContainer] = None,
            x:int=0,     y:int=0,
            width:int=0, height:int=0,
            pos  : Optional[Tuple[int,int]] = None,
            size : Optional[Tuple[int,int]] = None,
            maxSize  : Optional[Tuple[int,int]] = None,
            maxWidth : int   = 0x10000,
            maxHeight: int   = 0x10000,
            minSize  : Optional[Tuple[int,int]] = None,
            minWidth : int   = 0x00000,
            minHeight: int   = 0x00000,
            name     : Optional[str] = None,
            visible  : bool = True,
            enabled  : bool = True,
            toolTip  : Union[TTkString,str] = '',
            style    : Optional[Dict] = None,
            addStyle : Optional[Dict] = None,
            **kwargs) -> None:
        '''
        :param name: the name of the widget, defaults to ""
        :type name: str, optional
        :param parent: the parent widget, defaults to None
        :type parent: :py:class:`TTkWidget`, optional

        :param x: the x position, defaults to 0
        :type x: int, optional
        :param y: the y position, defaults to 0
        :type y: int, optional
        :param pos: the [x,y] position (override the previously defined x, y), defaults to (x,y)
        :type pos: (int,int), optional

        :param width: the width of the widget, defaults to 0
        :type width: int, optional
        :param height: the height of the widget, defaults to 0
        :type height: int, optional
        :param size: the size [width, height] of the widget (override the previously defined sizes), defaults to (width,height)
        :type size: (int,int), optional

        :param maxWidth: the maxWidth of the widget, defaults to 0x10000
        :type maxWidth: int, optional
        :param maxHeight: the maxHeight of the widget, defaults to 0x10000
        :type maxHeight: int, optional
        :param maxSize: the max [width,height] of the widget, optional, defaults to (maxWidth,maxHeight)
        :type maxSize: (int,int), optional
        :param minWidth: the minWidth of the widget, defaults to 0
        :type minWidth: int, optional
        :param minHeight: the minHeight of the widget, defaults to 0
        :type minHeight: int, optional
        :param minSize: the minSize [width,height] of the widget, optional, defaults to (minWidth,minHeight)
        :type minSize: (int,int), optional

        :param toolTip: This property holds the widget's tooltip, defaults to ''
        :type toolTip: :py:class:`TTkString`, optional

        :param style: this field hold the custom style to be used by this widget
        :type style: dict, optional
        :param addStyle: this field is required to override/merge the new style on top of the current one, useful if only few params need to be changed
        :type addStyle: dict, optional

        :param visible: the visibility, optional, defaults to True
        :type visible: bool, optional
        :param enabled: the ability to handle input events, optional, defaults to True
        :type enabled: bool, optional
        '''
        if kwargs:
            TTkLog.warn(f"Unhandled init params {self.__class__.__name__} -> {kwargs}")

        #Signals
        self.focusChanged = pyTTkSignal(bool)
        self.sizeChanged = pyTTkSignal(int,int)
        self.currentStyleChanged = pyTTkSignal(dict)
        self.closed = pyTTkSignal(TTkWidget)
        # self.sizeChanged.connect(self.resizeEvent)

        self._dropEventProxy = lambda x:x
        self._widgetCursor = (0,0)
        self._widgetCursorEnabled = False
        self._widgetCursorType = TTkK.Cursor_Blinking_Bar

        self._name = name if name else self.__class__.__name__
        self._parent = parent


        self._x, self._y = pos if pos else (x,y)
        self._width, self._height = size if size else (width,height)

        self._maxw, self._maxh = maxSize if maxSize else (maxWidth,maxHeight)
        self._minw, self._minh = minSize if minSize else (minWidth,minHeight)

        self._focus_policy = TTkK.NoFocus

        self._visible = visible
        self._enabled = enabled

        self._toolTip = TTkString(toolTip)

        self._widgetItem = TTkWidgetItem(widget=self)

        self._currentStyle = TTkWidget.classStyle['default']
        self.setStyle(self.classStyle)
        self._processStyleEvent(TTkWidget._S_DEFAULT)
        if style:
            self.setStyle(style)
        if addStyle:
            self.mergeStyle(addStyle)

        self._canvas = TTkCanvas(
                            width  = self._width  ,
                            height = self._height )

        # TODO: Check this,
        # The parent should always have a layout
        if self._parent:
            if not hasattr(self._parent,'layout'):
                TTkLog.warn(f"The parent={self._parent} is not a container")
            else:
                if self._parent.layout():
                    self._parent.layout().addWidget(self)
                    self._parent.update(repaint=True, updateLayout=True)

    def __del__(self):
        '''
        Widget destructor

        Performs cleanup including removal from parent layout and signal cleanup.

        .. caution:: This is an internal method, do not call it directly
        '''
        # TTkLog.debug("DESTRUCTOR")

        # clean all the signals, slots
        #for an in dir(self):
        #    att = self.__getattribute__(an)
        #    # TODO: TBD, I need to find the time to do this

        if hasattr(self._parent,'layout') and self._parent.layout():
            self._parent.layout().removeWidget(self)
            self._parent = None

    def name(self) -> str:
        '''
        Retrieve the name of this widget

        :return: the widget name
        :rtype: str
        '''
        return self._name

    def setName(self, name:str) -> None:
        '''
        Set the name of this Instance

        :param name: the name to be set
        :type name: str
        '''
        self._name = name

    def setDropEventProxy(self, proxy:Callable) -> None:
        '''
        .. warning::
            This is an alpha Method to prototype the Drag and Drop proxy feature and may change in the future
        '''
        self._dropEventProxy = proxy

    def widgetItem(self) -> TTkWidgetItem:
        '''
        Retrieve the widget item (layout item wrapper)

        :return: the layout item for this widget
        :rtype: :py:class:`TTkWidgetItem`
        '''
        return self._widgetItem

    def paintEvent(self, canvas:TTkCanvas) -> None:
        '''
        Paint Event callback,
        this need to be overridden in the widget.

        .. note:: Override this method to handle this event

        :param canvas: the canvas where the content need to be drawn
        :type canvas: :py:class:`TTkCanvas`
        '''
        pass

    def getPixmap(self) -> TTkCanvas:
        '''
        Convenience function which return a pixmap representing the current widget status

        :return: :py:class:`TTkCanvas`
        '''
        self.paintEvent(self._canvas)
        self.paintChildCanvas()
        return self._canvas.copy()

    @staticmethod
    def _paintChildCanvas(canvas, item, geometry, offset) -> None:
        '''
        Internal static method for painting child widgets on the canvas

        .. note:: This is an internal method

        :param canvas: the canvas to paint on
        :type canvas: :py:class:`TTkCanvas`
        :param item: the layout item
        :param geometry: the geometry information
        :param offset: the drawing offset
        '''
        pass

    def paintChildCanvas(self) -> None:
        '''
        Paint child widgets on the canvas

        This method is called during the paint process to render child widgets.
        Override in container widgets to implement custom child rendering.

        .. note:: Override this method in subclasses to handle child widget painting
        '''
        pass

    def moveEvent(self, x: int, y: int) -> None:
        '''
        Convenience function,
        Event Callback triggered after a successful move

        .. note:: Override this method to handle this event

        :param x: the new horizontal position
        :type x: int
        :param y: the new vertical position
        :type y: int
        '''
        pass

    def resizeEvent(self, width: int, height: int) -> None:
        '''
        Convenience function,
        Event Callback triggered after a successful resize

        .. note:: Override this method to handle this event

        :param width: the new width
        :type width: int
        :param height: the new height
        :type height: int
        '''
        pass

    def setDefaultSize(self, arg, width: int, height: int) -> None:
        # TODO: Get rid of this method
        '''
        Set default size if not already specified in arguments

        This is a helper method for widgets to set default dimensions when no explicit size was provided.

        .. note:: This is typically called during widget initialization

        :param arg: the arguments dictionary
        :type arg: dict
        :param width: the default width in characters
        :type width: int
        :param height: the default height in characters
        :type height: int
        '''
        if ( 'size' in arg or
             'width' in arg or
             'height' in arg ):
             return
        arg['width'] = width
        arg['height'] = height

    def move(self, x: int, y: int) -> None:
        ''' Move the widget

        :param x: the horizontal position
        :type x: int
        :param y: the vertical position
        :type y: int
        '''
        if x==self._x and y==self._y: return
        self._x = x
        self._y = y
        self.update(repaint=False, updateLayout=False)
        self.moveEvent(x,y)

    def resize(self, width: int, height: int) ->  None:
        ''' Resize the widget

        :param width: the new width
        :type width: int
        :param height: the new height
        :type height: int
        '''
        # TTkLog.debug(f"resize: {w,h} {self._name}")
        if width!=self._width or height!=self._height:
            self._width  = width
            self._height = height
            self._canvas.resize(self._width, self._height)
            self.update(repaint=True, updateLayout=True)
        self.resizeEvent(width,height)
        self.sizeChanged.emit(width,height)

    def setGeometry(self, x: int, y: int, width: int, height: int):
        ''' Resize and move the widget

        :param x: the horizontal position
        :type x: int
        :param y: the vertical position
        :type y: int
        :param width: the new width
        :type width: int
        :param height: the new height
        :type height: int
        '''
        self.resize(width, height)
        self.move(x, y)

    def pasteEvent(self, txt:str) -> bool:
        '''
        Callback triggered when a paste event is forwarded to this widget.

        .. note:: Reimplement this function to handle this event

        :param txt: the paste object
        :type txt: str

        :return: the state of the paste operation
        :rtype: bool
        '''
        return False

    def _mouseEventParseChildren(self, evt:TTkMouseEvent) -> bool:
        '''
        Parse mouse events for child widgets

        This method is called to allow container widgets to handle mouse events for their children.
        Override this method in container widgets to parse and forward mouse events to child widgets.

        .. note:: This is an internal method

        :param evt: the mouse event
        :type evt: :py:class:`TTkMouseEvent`
        :return: True if the event was handled, False otherwise
        :rtype: bool
        '''
        return False

    _mouseOver = None
    _mouseOverTmp = None
    _mouseOverProcessed = False
    def mouseEvent(self, evt:TTkMouseEvent) -> bool:
        '''
        Handle mouse events for this widget and its children

        This method handles all mouse-related events including clicks, movement, dragging, and wheel events.
        It manages focus, hover states, and delegates events to child widgets and event handlers.

        .. note:: This is an internal method

        :param evt: the mouse event
        :type evt: :py:class:`TTkMouseEvent`
        :return: True if the event was handled, False otherwise
        :rtype: bool
        '''
        if not self._enabled: return False

        # Saving self in this global variable
        # So that after the "_mouseEventLayoutHandle"
        # this tmp value will hold the last widget below the mouse
        TTkWidget._mouseOverTmp = self

        # Mouse Drag has priority because it
        # should be handled by the focused widget and
        # not pushed to the unfocused childs
        # unless there is a Drag and Drop event ongoing
        if evt.evt == TTkK.Drag and not TTkHelper.isDnD():
            if self.mouseDragEvent(evt):
                return True

        # if self.rootLayout() is not None:
        #     if  TTkWidget._mouseEventLayoutHandle(evt, self.rootLayout()):
        #         return True

        if self._mouseEventParseChildren(evt):
            return True

        # If there is an overlay and it is modal,
        # return False if this widget is not part of any
        # of the widgets above the modal
        if not TTkHelper.checkModalOverlay(self):
            return False

        # Handle Drag and Drop Events
        if _dnd:=TTkHelper.dndGetDnd():
            ret = False
            dndw = _dnd.w
            dndg = _dnd.d
            if evt.evt == TTkK.Drag:
                if dndw == self:
                    self.dragMoveEvent(dndg.getDragMoveEvent(evt))
                    return True
                else:
                    if ( self.dragEnterEvent(dndg.getDragEnterEvent(evt)) or
                         self.dragMoveEvent(dndg.getDragMoveEvent(evt))):
                        if dndw:
                            ret = dndw.dragLeaveEvent(dndg.getDragLeaveEvent(evt))
                        TTkHelper.dndEnter(self)
                        return True
            if evt.evt == TTkK.Release:
                if self.dropEvent(self._dropEventProxy(dndg.getDropEvent(evt))):
                    return True
            return ret

        # handle Enter/Leave Events
        # _mouseOverTmp hold the top widget under the mouse
        # if different than self it means that it is a child
        if evt.evt == TTkK.Move:
            if not TTkWidget._mouseOverProcessed:
                if TTkWidget._mouseOver != TTkWidget._mouseOverTmp == self:
                    if TTkWidget._mouseOver:
                        # TTkLog.debug(f"Leave: {TTkWidget._mouseOver._name}")
                        TTkWidget._mouseOver.leaveEvent(evt)
                    TTkWidget._mouseOver = self
                    # TTkLog.debug(f"Enter: {TTkWidget._mouseOver._name}")
                    TTkHelper.toolTipClose()
                    if self._toolTip and self._toolTip != '':
                        TTkHelper.toolTipTrigger(self._toolTip)
                    # TTkHelper.triggerToolTip(self._name)
                    TTkWidget._mouseOver.enterEvent(evt)
                TTkWidget._mouseOverProcessed = True
            if self.mouseMoveEvent(evt):
                return True
        else:
            TTkHelper.toolTipClose()

        if evt.evt == TTkK.Release:
            self._processStyleEvent(TTkWidget._S_NONE)
            if self.mouseReleaseEvent(evt):
                return True

        if evt.evt == TTkK.Press:
            # in case of parent focus, check the parent that can accept the focus
            w = self
            while w._parent and (w.focusPolicy() & TTkK.ParentFocus) == TTkK.ParentFocus:
                w = w._parent
            self._processStyleEvent(TTkWidget._S_PRESSED)
            if w.focusPolicy() & TTkK.ClickFocus == TTkK.ClickFocus:
                w.setFocus()
                w.raiseWidget()
            if evt.tap == 2 and self.mouseDoubleClickEvent(evt):
                return True
            if evt.tap > 1 and self.mouseTapEvent(evt):
                return True
            if evt.tap == 1 and self.mousePressEvent(evt):
                # TTkLog.debug(f"Click {self._name}")
                self._setPendingMouseRelease()
                return True

        if evt.key == TTkK.Wheel:
            if self.wheelEvent(evt):
                return True

        return False

    def setParent(self, parent) -> None:
        '''
        Set the parent widget

        :param parent: the parent widget
        :type parent: :py:class:`TTkContainer`
        '''
        self._parent = parent
    def parentWidget(self):
        '''
        Retrieve the parent widget

        :return: the parent widget or None if top-level
        :rtype: :py:class:`TTkContainer` or None
        '''
        return self._parent

    def x(self) -> int:
        '''
        Retrieve the horizontal position

        :return: the x coordinate
        :rtype: int
        '''
        return self._x
    def y(self) -> int:
        '''
        Retrieve the vertical position

        :return: the y coordinate
        :rtype: int
        '''
        return self._y
    def width(self)  -> int:
        '''
        Retrieve the widget width

        :return: the width in characters
        :rtype: int
        '''
        return self._width
    def height(self) -> int:
        '''
        Retrieve the widget height

        :return: the height in characters
        :rtype: int
        '''
        return self._height

    def pos(self)  -> tuple[int,int]:
        '''
        Retrieve the widget position

        :return: a tuple of (x, y) coordinates
        :rtype: tuple[int, int]
        '''
        return self._x, self._y
    def size(self) -> tuple[int,int]:
        '''
        Retrieve the widget size

        :return: a tuple of (width, height)
        :rtype: tuple[int, int]
        '''
        return self._width, self._height
    def geometry(self) -> tuple[int,int,int,int]:
        '''
        Retrieve the widget geometry

        :return: a tuple of (x, y, width, height)
        :rtype: tuple[int, int, int, int]
        '''
        return self._x, self._y, self._width, self._height

    def maximumSize(self) -> tuple[int,int]:
        '''
        Retrieve the maximum size

        :return: a tuple of (max_width, max_height)
        :rtype: tuple[int, int]
        '''
        return self.maximumWidth(), self.maximumHeight()
    def maxDimension(self, orientation:TTkK.Direction) -> int:
        '''
        Retrieve the maximum dimension for the given orientation

        :param orientation: the orientation (:py:class:`TTkK.HORIZONTAL` or :py:class:`TTkK.VERTICAL`)
        :type orientation: :py:class:`TTkK.Direction`
        :return: the maximum dimension
        :rtype: int
        '''
        if orientation == TTkK.HORIZONTAL:
            return self.maximumWidth()
        else:
            return self.maximumHeight()
    def maximumHeight(self) -> int:
        '''
        Retrieve the maximum height

        :return: the maximum height in characters
        :rtype: int
        '''
        return self._maxh
    def maximumWidth(self) -> int:
        '''
        Retrieve the maximum width

        :return: the maximum width in characters
        :rtype: int
        '''
        return self._maxw

    def minimumSize(self) -> tuple[int,int]:
        '''
        Retrieve the minimum size

        :return: a tuple of (min_width, min_height)
        :rtype: tuple[int, int]
        '''
        return self.minimumWidth(), self.minimumHeight()
    def minDimension(self, orientation:TTkK.Direction) -> int:
        '''
        Retrieve the minimum dimension for the given orientation

        :param orientation: the orientation (:py:class:`TTkK.HORIZONTAL` or :py:class:`TTkK.VERTICAL`)
        :type orientation: :py:class:`TTkK.Direction`
        :return: the minimum dimension
        :rtype: int
        '''
        if orientation == TTkK.HORIZONTAL:
            return self.minimumWidth()
        else:
            return self.minimumHeight()
    def minimumHeight(self) -> int:
        '''
        Retrieve the minimum height

        :return: the minimum height in characters
        :rtype: int
        '''
        return self._minh
    def minimumWidth(self) -> int:
        '''
        Retrieve the minimum width

        :return: the minimum width in characters
        :rtype: int
        '''
        return self._minw

    def setMaximumSize(self, maxw: int, maxh: int) -> None:
        '''
        Set the maximum size of the widget

        :param maxw: the maximum width in characters
        :type maxw: int
        :param maxh: the maximum height in characters
        :type maxh: int
        '''
        self.setMaximumWidth(maxw)
        self.setMaximumHeight(maxh)

    def _clampCurrentSizeToBoundaries(self) -> bool:
        '''
        Clamp the current widget size to its minimum and maximum boundaries

        .. note:: This is an internal method

        :return: True if resize was needed, False otherwise
        :rtype: bool
        '''
        neww = max(self._minw, min(self._width,  self._maxw))
        newh = max(self._minh, min(self._height, self._maxh))
        if neww == self._width and newh == self._height:
            return False
        self.resize(neww, newh)
        return True

    def setMaximumHeight(self, maxh: int) -> None:
        '''
        Set the maximum height of the widget

        If the current height exceeds the new maximum, the widget will be resized.
        If the minimum height exceeds the new maximum, the minimum height is adjusted.

        :param maxh: the maximum height in characters
        :type maxh: int
        '''
        if self._maxh == maxh: return
        self._maxh = maxh
        if self._minh > self._maxh:
            self._minh = self._maxh
        if not self._clampCurrentSizeToBoundaries():
            self.update(updateLayout=True, updateParent=True)

    def setMaximumWidth(self, maxw: int) -> None:
        '''
        Set the maximum width of the widget

        If the current width exceeds the new maximum, the widget will be resized.
        If the minimum width exceeds the new maximum, the minimum width is adjusted.

        :param maxw: the maximum width in characters
        :type maxw: int
        '''
        if self._maxw == maxw: return
        self._maxw = maxw
        if self._minw > self._maxw:
            self._minw = self._maxw
        if not self._clampCurrentSizeToBoundaries():
            self.update(updateLayout=True, updateParent=True)

    def setMinimumSize(self, minw: int, minh: int) -> None:
        '''
        Set the minimum size of the widget

        :param minw: the minimum width in characters
        :type minw: int
        :param minh: the minimum height in characters
        :type minh: int
        '''
        self.setMinimumWidth(minw)
        self.setMinimumHeight(minh)

    def setMinimumHeight(self, minh: int) -> None:
        '''
        Set the minimum height of the widget

        If the current height is less than the new minimum, the widget will be resized.
        If the maximum height is less than the new minimum, the maximum height is adjusted.

        :param minh: the minimum height in characters
        :type minh: int
        '''
        if self._minh == minh: return
        self._minh = minh
        if self._maxh < self._minh:
            self._maxh = self._minh
        if not self._clampCurrentSizeToBoundaries():
            self.update(updateLayout=True, updateParent=True)

    def setMinimumWidth(self, minw: int) -> None:
        '''
        Set the minimum width of the widget

        If the current width is less than the new minimum, the widget will be resized.
        If the maximum width is less than the new minimum, the maximum width is adjusted.

        :param minw: the minimum width in characters
        :type minw: int
        '''
        if self._minw == minw: return
        self._minw = minw
        if self._maxw < self._minw:
            self._maxw = self._minw
        if not self._clampCurrentSizeToBoundaries():
            self.update(updateLayout=True, updateParent=True)

    @pyTTkSlot()
    def show(self) -> None:
        '''show the widget'''
        if self._visible: return
        self._visible = True
        self._canvas.show()
        self.update(updateLayout=True, updateParent=True)

    @pyTTkSlot()
    def hide(self) -> None:
        '''hide the widget'''
        if not self._visible: return
        self._visible = False
        self._canvas.hide()
        self.update(repaint=False, updateParent=True)

    @pyTTkSlot()
    def raiseWidget(self, raiseParent:bool=True) -> None:
        '''Raise the Widget above its relatives'''
        if self._parent is not None and \
           self._parent.rootLayout() is not None:
            if raiseParent:
                self._parent.raiseWidget(raiseParent)
            self._parent.rootLayout().raiseWidget(self)

    @pyTTkSlot()
    def lowerWidget(self) -> None:
        '''Lower the Widget below its relatives'''
        if self._parent is not None and \
           self._parent.rootLayout() is not None:
            self._parent.lowerWidget()
            self._parent.rootLayout().lowerWidget(self)

    @pyTTkSlot()
    def close(self) -> None:
        '''Close (Destroy/Remove) the widget'''
        if _p := self._parent:
            if _rl := _p.rootLayout():
                _rl.removeWidget(self)
            _p.update()
        TTkHelper.removeOverlayAndChild(self)
        self._parent = None
        self.hide()
        self.closed.emit(self)

    @pyTTkSlot(bool)
    def setVisible(self, visible: bool) -> None:
        '''
        Set the visibility status of this widget

        :param visible: status
        :type visible: bool
        '''
        if visible: self.show()
        else: self.hide()

    def isVisibleAndParent(self) -> bool:
        '''
        Check if the widget and all its parents are visible

        :return: True if the widget and all its parents are visible, False otherwise
        :rtype: bool
        '''
        return ( self._visible and
            ( self._parent is not None ) and
            self._parent.isVisibleAndParent() )

    def isVisible(self) -> bool:
        '''
        Retrieve the visibility status of this widget

        :return: bool
        '''
        return self._visible

    @pyTTkSlot()
    def update(self, repaint: bool =True, updateLayout: bool =False, updateParent: bool =False) -> None:
        '''
        Notify the drawing routine that the widget changed and needs to draw its new content.

        It is important to call this method anytime a canvas update is required after a a status update.

        Once :py:meth:`update` is called, the :py:meth:`paintEvent` is executed during the next screen refresh.

        i.e.

        .. code-block:: python

            class NewLabel(TTkWidget):
                def __init__(self,**kwargs) -> None:
                    self.text = ""
                    super().__init__(**kwargs)

                def setText(self, text:str) -> None:
                    self.text = text
                    # Notify the runtime that un update
                    # is required will trigger the paintEvent
                    # at the next screen (terminal) refresh
                    self.update()

                def paintEvent(self, canvas:TTkCanvas) -> None:
                    canvas.drawText(pos=(0,0), text=self.text)
        '''
        if repaint:
            TTkHelper.addUpdateBuffer(self)
        TTkHelper.addUpdateWidget(self)
        if updateParent and self._parent is not None:
            self._parent.update(updateLayout=True)

    def _setPendingMouseRelease(self) -> None:
        '''
        Set this widget as the pending mouse release widget

        .. note:: This is an internal method used to track which widget should receive a mouse release event
        '''
        if not (_p:=self._parent):
             return
        _p._setPendingMouseReleaseWidget(self)

    @pyTTkSlot()
    def setFocus(self) -> None:
        '''Focus the widget'''
        if not (_p:=self._parent):
             return
        if (_old_fw:=_p._getFocusWidget()) is self:
            return
        if _old_fw:
            _old_fw.clearFocus()
        _p._setFocusWidget(self)
        self.focusChanged.emit(True)
        self.focusInEvent()
        self._processStyleEvent(TTkWidget._S_DEFAULT)
        self._pushWidgetCursor()
        TTkHelper.removeOverlayChild(self)
        self.update()

    def clearFocus(self) -> None:
        '''Remove the Focus state of this widget'''
        if not (_p:=self._parent) or _p._getFocusWidget() is not self:
            return
        _p._setFocusWidget(None)
        self.focusChanged.emit(False)
        self.focusOutEvent()
        self._processStyleEvent(TTkWidget._S_DEFAULT)
        self.update()

    def hasFocus(self) -> bool:
        '''
        This property holds the focus status of this widget

        :return: bool
        '''
        return bool((_p:=self._parent) and _p._getFocusWidget() is self)

    def getCanvas(self) -> TTkCanvas:
        '''
        Retrieve the widget canvas

        :return: the canvas object used for drawing
        :rtype: :py:class:`TTkCanvas`
        '''
        return self._canvas

    def focusPolicy(self) -> TTkK.FocusPolicy:
        '''
        Retrieve the focus policy of this widget

        :return: the focus policy
        :rtype: :py:class:`TTkK.FocusPolicy`
        '''
        return self._focus_policy

    def setFocusPolicy(self, policy:TTkK.FocusPolicy) -> None:
        '''
        This property holds the way the widget accepts keyboard focus

        The policy is :py:class:`TTkK.FocusPolicy.TabFocus` if the widget accepts keyboard focus by tabbing,
        :py:class:`TTkK.FocusPolicy.ClickFocus` if the widget accepts focus by clicking,
        :py:class:`TTkK.FocusPolicy.StrongFocus` if it accepts both,
        and :py:class:`TTkK.FocusPolicy.NoFocus` (the default) if it does not accept focus at all.

        You must enable keyboard focus for a widget if it processes keyboard events.
        This is normally done from the widget's constructor. For instance,
        the :py:class:`TTkLineEdit` constructor calls :py:meth:`setFocusPolicy` with :py:class:`TTkK.FocusPolicy.StrongFocus`.

        If the widget has a focus proxy, then the focus policy will be propagated to it.

        :param policy: the focus policy
        :type policy: :py:class:`TTkK.FocusPolicy`
        '''
        self._focus_policy = policy

    def focusInEvent(self) -> None:
        '''
        Callback triggered when the widget receives focus

        .. note:: Override this method to handle focus in events
        '''
        pass
    def focusOutEvent(self) -> None:
        '''
        Callback triggered when the widget loses focus

        .. note:: Override this method to handle focus out events
        '''
        pass

    def isEntered(self) -> bool:
        '''
        Check if the mouse cursor is currently over this widget

        :return: True if the mouse is over this widget, False otherwise
        :rtype: bool
        '''
        return self._mouseOver == self

    def isEnabled(self) -> bool:
        '''
        This property holds whether the widget is enabled

        use :py:meth:`setEnabled` or :py:meth:`setDisabled` to change this property

        :return: bool
        '''
        return self._enabled

    @pyTTkSlot(bool)
    def setEnabled(self, enabled:bool=True) -> None:
        '''
        This property holds whether the widget is enabled

        In general an enabled widget handles keyboard and mouse events;
        a disabled widget does not.

        Some widgets display themselves differently when they are disabled.
        For example a button might draw its label grayed out.
        If your widget needs to know when it becomes enabled or disabled.

        Disabling a widget implicitly disables all its children.
        Enabling respectively enables all child widgets unless they have been explicitly disabled.

        By default, this property is true.

        :param enabled: the enabled status, defaults to True
        :type enabled: bool
        '''
        if self._enabled == enabled: return
        self._enabled = enabled
        self._processStyleEvent(TTkWidget._S_DEFAULT if enabled else TTkWidget._S_DISABLED)
        self.update()

    @pyTTkSlot(bool)
    def setDisabled(self, disabled:bool=True) -> None:
        '''This property holds whether the widget is disabled

        This is a convenience function wrapped around :py:meth:`setEnabled` where (not disabled) is used

        :param disabled: the disabled status, defaults to True
        :type disabled: bool
        '''
        self.setEnabled(not disabled)

    def toolTip(self) -> TTkString:
        '''
        Retrieve the widget tooltip

        :return: the tooltip text
        :rtype: :py:class:`TTkString`
        '''
        return self._toolTip

    def setToolTip(self, toolTip: TTkString) -> None:
        '''
        Set the widget tooltip

        :param toolTip: the tooltip text to display
        :type toolTip: :py:class:`TTkString`
        '''
        self._toolTip = TTkString(toolTip)

    def getWidgetByName(self, name: str):
        '''
        Get a widget by its name (recursively searches this widget and its children)

        :param name: the widget name to search for
        :type name: str
        :return: the widget with the given name, or None if not found
        :rtype: :py:class:`TTkWidget` or None
        '''
        if name == self._name:
            return self
        return None

    _BASE_STYLE = {'default' : {'color': TTkColor.RST}}

    # Style Methods
    _S_NONE     = 0x00
    _S_DEFAULT  = 0x01
    _S_ACTIVE   = 0x02
    _S_DISABLED = 0x03
    _S_HOVER    = 0x10
    _S_PRESSED  = 0x20
    _S_RELEASED = 0x40

    def style(self) -> Dict:
        '''
        Retrieve a copy of the widget style dictionary

        :return: a dictionary containing the style configuration
        :rtype: dict
        '''
        return self._style.copy()

    def currentStyle(self) -> Dict:
        '''
        Retrieve the currently active style

        :return: a dictionary containing the active style
        :rtype: dict
        '''
        return self._currentStyle

    def setCurrentStyle(self, style) -> None:
        '''
        Set the currently active style

        :param style: the style dictionary to apply
        :type style: dict
        '''
        if style == self._currentStyle:
            return
        self._currentStyle = style
        self.currentStyleChanged.emit(style)
        self.update()

    def setStyle(self, style:Dict[str,Dict]={}) -> None:
        '''
        Set the style for the widget

        The style dictionary should have keys for different states like 'default', 'hover', 'focus', 'disabled', 'clicked'.
        Each state has its own style dictionary.

        :param style: the style configuration dictionary
        :type style: dict[str, dict]
        '''
        if not style:
            style = self.classStyle.copy()
        defaultStyle = style['default']
        # Use the default style to apply the missing fields of the other actions
        mergeStyle = {t:defaultStyle | style[t] for t in style}
        self._style = mergeStyle
        self._processStyleEvent(TTkWidget._S_DEFAULT)

    def mergeStyle(self, style) -> None:
        '''
        Merge additional style properties with the existing style

        This allows updating only specific style properties without replacing the entire style.

        :param style: a dictionary with style properties to merge
        :type style: dict
        '''
        cs = None
        # for field in style:
        #     if field in self._style:
        #         mergeStyle[field] = defaultStyle | self._style[field] | style[field]
        #     else:
        #         mergeStyle[field] = defaultStyle
        for t in self._style:
            if self._style[t] == self._currentStyle:
                cs = t
            if t in style:
                self._style[t] =  self._style[t] | style[t]
        if cs:
            self.setCurrentStyle(self._style[cs])

    def _processStyleEvent(self, evt=_S_DEFAULT) -> bool:
        '''
        Process a style event and update the widget appearance

        This internal method handles style transitions based on widget state events.

        .. note:: This is an internal method

        :param evt: the style event type
        :type evt: int
        :return: True if the style was changed, False otherwise
        :rtype: bool
        '''
        if not self._style: return False
        if not self._enabled and 'disabled' in self._style:
            self.setCurrentStyle(self._style['disabled'])
            return True

        if evt in (TTkWidget._S_DEFAULT,
                   TTkWidget._S_NONE,
                   TTkWidget._S_ACTIVE):
            if self.hasFocus() and 'focus' in self._style:
                self.setCurrentStyle(self._style['focus'])
                return True
            elif 'default' in self._style:
                self.setCurrentStyle(self._style['default'])
                return True
        elif evt & TTkWidget._S_HOVER and 'hover' in self._style:
            self.setCurrentStyle(self._style['hover'])
            return True
        elif evt & TTkWidget._S_PRESSED and 'clicked' in self._style:
            self.setCurrentStyle(self._style['clicked'])
            return True
        elif evt & TTkWidget._S_DISABLED and 'disabled' in self._style:
            self.setCurrentStyle(self._style['disabled'])
            return True
        if self.hasFocus() and 'focus' in self._style:
            self.setCurrentStyle(self._style['focus'])
            return True
        return False

    # Widget Cursor Helpers
    def enableWidgetCursor(self, enable:bool=True) -> None:
        '''
        Enable or disable the widget cursor

        :param enable: True to enable the cursor, False to disable
        :type enable: bool
        '''
        self._widgetCursorEnabled = enable
        self._pushWidgetCursor()

    def disableWidgetCursor(self, disable:bool=True) -> None:
        '''
        Disable or enable the widget cursor

        This is a convenience method that is equivalent to enableWidgetCursor(not disable).

        :param disable: True to disable the cursor, False to enable
        :type disable: bool
        '''
        self._widgetCursorEnabled = not disable
        self._pushWidgetCursor()

    def setWidgetCursor(self, pos=None, type=None) -> None:
        '''
        Set the widget cursor position and type

        :param pos: the cursor position as (x, y) tuple, or None to keep current
        :type pos: tuple[int, int] or None
        :param type: the cursor type (e.g., :py:class:`TTkK.Cursor_Blinking_Bar`), or None to keep current
        :type type: int or None
        '''
        self._widgetCursor     = pos  if pos  else self._widgetCursor
        self._widgetCursorType = type if type else self._widgetCursorType
        self._pushWidgetCursor()

    def _pushWidgetCursor(self) -> None:
        '''
        Push the widget cursor to the terminal display

        .. note:: This is an internal method
        '''
        if ( self._widgetCursorEnabled and
             self._visible and
             ( self.hasFocus() or self == TTkHelper.cursorWidget() ) ):
            cx,cy  = self._widgetCursor
            ax, ay = TTkHelper.absPos(self)
            if ( self == TTkHelper.widgetAt(cx+ax, cy+ay) or
                # Since the blinking bar can be placed also at the left side of the next
                # char, it can be displayed also if its position is one char outside the boudaries
                 ( self._widgetCursorType == TTkK.Cursor_Blinking_Bar and
                   self == TTkHelper.widgetAt(cx+ax-1, cy+ay) ) ):
                TTkHelper.showCursor(self._widgetCursorType)
                TTkHelper.moveCursor(self, cx, cy)
            else:
                TTkHelper.hideCursor()
