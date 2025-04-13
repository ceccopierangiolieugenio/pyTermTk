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

__all__ = ['TTkWidget']

from typing import Callable, Any, List

try:
    from typing import Self
except:
    class Self(): pass

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

class TTkWidget(TMouseEvents,TKeyEvents, TDragEvents):
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
        '_focus','_focus_policy',
        '_canvas', '_widgetItem',
        '_visible',
        '_pendingMouseRelease',
        '_enabled',
        '_style', '_currentStyle',
        '_toolTip',
        '_dropEventProxy',
        '_widgetCursor', '_widgetCursorEnabled', '_widgetCursorType',
        #Signals
        'focusChanged', 'sizeChanged', 'currentStyleChanged', 'closed')

    def __init__(self,
                 parent:Self = None,
                 x:int=0,     y:int=0,
                 width:int=0, height:int=0,
                 pos  : tuple = None,
                 size : tuple = None,
                 maxSize  : tuple = None,
                 maxWidth : int   = 0x10000,
                 maxHeight: int   = 0x10000,
                 minSize  : tuple = None,
                 minWidth : int   = 0x00000,
                 minHeight: int   = 0x00000,
                 name     : str = None,
                 visible  : bool = True,
                 enabled  : bool = True,
                 toolTip  : TTkString = '',
                 style    : dict = None,
                 addStyle : dict = None,
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
        self._parent:TTkWidget = parent

        self._pendingMouseRelease = False

        self._x, self._y = pos if pos else (x,y)
        self._width, self._height = size if size else (width,height)

        self._maxw, self._maxh = maxSize if maxSize else (maxWidth,maxHeight)
        self._minw, self._minh = minSize if minSize else (minWidth,minHeight)

        self._focus = False
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
        ''' .. caution:: Don't touch this! '''
        # TTkLog.debug("DESTRUCTOR")

        # clean all the signals, slots
        #for an in dir(self):
        #    att = self.__getattribute__(an)
        #    # TODO: TBD, I need to find the time to do this

        if hasattr(self._parent,'layout') and self._parent.layout():
            self._parent.layout().removeWidget(self)
            self._parent = None

    def name(self) -> str:
        '''name'''
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
            This is an alpha Method to prototype the Drag and Drop prosy feature and may change in the future
        '''
        self._dropEventProxy = proxy

    def widgetItem(self) -> TTkWidgetItem:
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
        pass

    def paintChildCanvas(self) -> None:
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

    def pasteEvent(self, txt:str) -> None:
        '''
        Callback triggered when a paste event is forwarded to this widget.

        .. note:: Reimplement this function to handle this event

        :param txt: the paste object
        :type txt: str
        '''
        return False

    def _mouseEventParseChildren(self, evt:TTkMouseEvent) -> bool:
        return False

    _mouseOver = None
    _mouseOverTmp = None
    _mouseOverProcessed = False
    def mouseEvent(self, evt:TTkMouseEvent) -> bool:
        ''' .. caution:: Don Not touch this! '''
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
        if TTkHelper.isDnD():
            ret = False
            if evt.evt == TTkK.Drag:
                dndw = TTkHelper.dndWidget()
                if dndw == self:
                    self.dragMoveEvent(TTkHelper.dndGetDrag().getDragMoveEvent(evt))
                    return True
                else:
                    if ( self.dragEnterEvent(TTkHelper.dndGetDrag().getDragEnterEvent(evt)) or
                         self.dragMoveEvent(TTkHelper.dndGetDrag().getDragMoveEvent(evt))):
                        if dndw:
                            ret = dndw.dragLeaveEvent(TTkHelper.dndGetDrag().getDragLeaveEvent(evt))
                        TTkHelper.dndEnter(self)
                        return True
            if evt.evt == TTkK.Release:
                if self.dropEvent(self._dropEventProxy(TTkHelper.dndGetDrag().getDropEvent(evt))):
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
            self._pendingMouseRelease = False
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
                #self._pendingMouseRelease = True
                return True
            if evt.tap > 1 and self.mouseTapEvent(evt):
                return True
            if evt.tap == 1 and self.mousePressEvent(evt):
                # TTkLog.debug(f"Click {self._name}")
                self._pendingMouseRelease = True
                return True

        if evt.key == TTkK.Wheel:
            if self.wheelEvent(evt):
                return True

        return False

    def setParent(self, parent) -> None:
        self._parent = parent
    def parentWidget(self):
        return self._parent

    def x(self) -> int: return self._x
    def y(self) -> int: return self._y
    def width(self)  -> int: return self._width
    def height(self) -> int: return self._height

    def pos(self)  -> tuple[int,int]: return self._x, self._y
    def size(self) -> tuple[int,int]: return self._width, self._height
    def geometry(self) -> tuple[int,int,int,int]: return self._x, self._y, self._width, self._height

    def maximumSize(self) -> tuple[int,int]:
        return self.maximumWidth(), self.maximumHeight()
    def maxDimension(self, orientation:TTkK.Direction) -> int:
        if orientation == TTkK.HORIZONTAL:
            return self.maximumWidth()
        else:
            return self.maximumHeight()
    def maximumHeight(self) -> int:
        return self._maxh
    def maximumWidth(self) -> int:
        return self._maxw

    def minimumSize(self) -> tuple[int,int]:
        return self.minimumWidth(), self.minimumHeight()
    def minDimension(self, orientation:TTkK.Direction) -> int:
        if orientation == TTkK.HORIZONTAL:
            return self.minimumWidth()
        else:
            return self.minimumHeight()
    def minimumHeight(self) -> int:
        return self._minh
    def minimumWidth(self) -> int:
        return self._minw

    def setMaximumSize(self, maxw: int, maxh: int):
        self.setMaximumWidth(maxw)
        self.setMaximumHeight(maxh)
    def setMaximumHeight(self, maxh: int):
        if self._maxh == maxh: return
        self._maxh = maxh
        self.update(updateLayout=True, updateParent=True)
    def setMaximumWidth(self, maxw: int):
        if self._maxw == maxw: return
        self._maxw = maxw
        self.update(updateLayout=True, updateParent=True)

    def setMinimumSize(self, minw: int, minh: int):
        self.setMinimumWidth(minw)
        self.setMinimumHeight(minh)
    def setMinimumHeight(self, minh: int):
        if self._minh == minh: return
        self._minh = minh
        self.update(updateLayout=True, updateParent=True)
    def setMinimumWidth(self, minw: int):
        if self._minw == minw: return
        self._minw = minw
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
        :type visible: bool:
        '''
        if visible: self.show()
        else: self.hide()

    def isVisibleAndParent(self) -> bool:
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

    @pyTTkSlot()
    def setFocus(self) -> None:
        '''Focus the widget'''
        # TTkLog.debug(f"setFocus: {self._name} - {self._focus}")
        if self._focus and self == TTkHelper.getFocus(): return
        tmp = TTkHelper.getFocus()
        if tmp == self: return
        if tmp is not None:
            tmp.clearFocus()
        TTkHelper.setFocus(self)
        self._focus = True
        self.focusChanged.emit(self._focus)
        self.focusInEvent()
        TTkHelper.removeOverlayChild(self)
        self._pushWidgetCursor()
        self._processStyleEvent(TTkWidget._S_DEFAULT)

    def clearFocus(self) -> None:
        '''Remove the Focus state of this widget'''
        # TTkLog.debug(f"clearFocus: {self._name} - {self._focus}")
        if not self._focus and self != TTkHelper.getFocus(): return
        TTkHelper.clearFocus()
        self._focus = False
        self.focusChanged.emit(self._focus)
        self.focusOutEvent()
        self._processStyleEvent(TTkWidget._S_DEFAULT)
        self.update(repaint=True, updateLayout=False)

    def hasFocus(self) -> bool:
        '''
        This property holds the focus status of this widget

        :return: bool
        '''
        return self._focus

    def getCanvas(self) -> TTkCanvas:
        return self._canvas

    def focusPolicy(self) -> TTkK.FocusPolicy:
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

    def focusInEvent(self) -> None: pass
    def focusOutEvent(self) -> None: pass

    def isEntered(self) -> bool:
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
        '''This property holds whether the widget is disnabled

        This is a convenience function wrapped around :py:meth:`setEnabled` where (not disabled) is used

        :param disabled: the disabled status, defaults to True
        :type disabled: bool
        '''
        self.setEnabled(not disabled)

    def toolTip(self) -> TTkString:
        return self._toolTip

    def setToolTip(self, toolTip: TTkString) -> None:
        self._toolTip = TTkString(toolTip)

    def getWidgetByName(self, name: str):
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

    def style(self) -> dict:
        return self._style.copy()

    def currentStyle(self) -> dict:
        return self._currentStyle

    def setCurrentStyle(self, style) -> dict:
        if style == self._currentStyle: return
        self._currentStyle = style
        self.currentStyleChanged.emit(style)
        self.update()

    def setStyle(self, style=None) -> None:
        if not style:
            style = self.classStyle.copy()
        if 'default' not in style:
            # find the closest subclass/parent holding the style
            styleType = TTkWidget
            for cc in type(self).__mro__:
                if cc in style:
                    styleType = cc
                    break
            # Filtering out the current object style
            style = style[styleType]
        defaultStyle = style['default']
        # Use the default style to apply the missing fields of the other actions
        mergeStyle = {t:defaultStyle | style[t] for t in style}
        self._style = mergeStyle
        self._processStyleEvent(TTkWidget._S_DEFAULT)

    def mergeStyle(self, style) -> None:
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
        self._widgetCursorEnabled = enable
        self._pushWidgetCursor()

    def disableWidgetCursor(self, disable:bool=True) -> None:
        self._widgetCursorEnabled = not disable
        self._pushWidgetCursor()

    def setWidgetCursor(self, pos=None, type=None) -> None:
        self._widgetCursor     = pos  if pos  else self._widgetCursor
        self._widgetCursorType = type if type else self._widgetCursorType
        self._pushWidgetCursor()

    def _pushWidgetCursor(self):
        if ( self._widgetCursorEnabled and
             self._visible and
             ( self._focus or self == TTkHelper.cursorWidget() ) ):
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
