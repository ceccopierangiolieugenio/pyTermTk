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
from TermTk.TTkLayouts.layout import TTkLayout, TTkWidgetItem
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

    :param name: the name of the widget, defaults to ""
    :type name: str, optional
    :param parent: the parent widget, defaults to None
    :type parent: :class:`TTkWidget`, optional

    :param int x: the x position, defaults to 0
    :param int y: the y position, defaults to 0
    :param [int,int] pos: the [x,y] position (override the previously defined x, y), optional, default=[0,0]

    :param int width: the width of the widget, defaults to 0
    :param int height: the height of the widget, defaults to 0
    :param [int,int] size: the size [width, height] of the widget (override the previously defined sizes), optional, default=[0,0]

    :param int maxWidth: the maxWidth of the widget, optional, defaults to 0x10000
    :param int maxHeight: the maxHeight of the widget, optional, defaults to 0x10000
    :param [int,int] maxSize: the max [width,height] of the widget, optional
    :param int minWidth: the minWidth of the widget, defaults to 0
    :param int minHeight: the minHeight of the widget, defaults to 0
    :param [int,int] minSize: the minSize [width,height] of the widget, optional

    :param toolTip: This property holds the widget's tooltip
    :type toolTip: :class:`~TermTk.TTkCore.string.TTkString`

    :param bool,optional visible: the visibility, optional, defaults to True
    :param bool,optional enabled: the ability to handle input events, optional, defaults to True
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
        '_widgetCursor', '_widgetCursorEnabled', '_widgetCursorType',
        #Signals
        'focusChanged', 'sizeChanged', 'currentStyleChanged', 'closed')

    def __init__(self, *args, **kwargs):
        #Signals
        self.focusChanged = pyTTkSignal(bool)
        self.sizeChanged = pyTTkSignal(int,int)
        self.currentStyleChanged = pyTTkSignal(dict)
        self.closed = pyTTkSignal(TTkWidget)
        # self.sizeChanged.connect(self.resizeEvent)

        self._widgetCursor = (0,0)
        self._widgetCursorEnabled = False
        self._widgetCursorType = TTkK.Cursor_Blinking_Bar

        self._name = kwargs.get('name', self.__class__.__name__)
        self._parent = kwargs.get('parent', None )

        self._pendingMouseRelease = False

        self._x = kwargs.get('x', 0 )
        self._y = kwargs.get('y', 0 )
        self._x, self._y = kwargs.get('pos', (self._x, self._y))
        self._width  = kwargs.get('width' , 0 )
        self._height = kwargs.get('height', 0 )
        self._width, self._height = kwargs.get('size', (self._width, self._height))

        self._maxw = kwargs.get('maxWidth',  0x10000)
        self._maxh = kwargs.get('maxHeight', 0x10000)
        self._maxw, self._maxh = kwargs.get('maxSize', (self._maxw, self._maxh))
        self._minw = kwargs.get('minWidth',  0x00000)
        self._minh = kwargs.get('minHeight', 0x00000)
        self._minw, self._minh = kwargs.get('minSize', (self._minw, self._minh))

        self._focus = False
        self._focus_policy = TTkK.NoFocus

        self._visible = kwargs.get('visible', True)
        self._enabled = kwargs.get('enabled', True)

        self._toolTip = TTkString(kwargs.get('toolTip',''))

        self._widgetItem = TTkWidgetItem(widget=self)

        self._currentStyle = TTkWidget.classStyle['default']
        self.setStyle(self.classStyle)
        self._processStyleEvent(TTkWidget._S_DEFAULT)

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

    def setName(self, name:str):
        '''setName'''
        self._name = name

    def widgetItem(self): return self._widgetItem

    def paintEvent(self, canvas:TTkCanvas):
        '''
        Paint Event callback,
        this need to be overridden in the widget.
        '''
        pass

    def getPixmap(self) -> TTkCanvas:
        self.paintEvent(self._canvas)
        self.paintChildCanvas()
        return self._canvas.copy()

    @staticmethod
    def _paintChildCanvas(canvas, item, geometry, offset):
        pass

    def paintChildCanvas(self):
        pass

    def moveEvent(self, x: int, y: int):
        ''' Event Callback triggered after a successful move'''
        pass
    @pyTTkSlot(int,int)
    def resizeEvent(self, w: int, h: int):
        ''' Event Callback triggered after a successful resize'''
        pass

    def setDefaultSize(self, arg, width: int, height: int):
        if ( 'size' in arg or
             'width' in arg or
             'height' in arg ):
             return
        arg['width'] = width
        arg['height'] = height

    def move(self, x: int, y: int):
        ''' Move the widget

        :param int x: x position
        :param int y: y position
        '''
        if x==self._x and y==self._y: return
        self._x = x
        self._y = y
        self.update(repaint=False, updateLayout=False)
        self.moveEvent(x,y)

    def resize(self, w: int, h: int):
        ''' Resize the widget

        :param int w: the new width
        :param int h: the new height
        '''
        # TTkLog.debug(f"resize: {w,h} {self._name}")
        if w!=self._width or h!=self._height:
            self._width  = w
            self._height = h
            self._canvas.resize(self._width, self._height)
            self.update(repaint=True, updateLayout=True)
        self.resizeEvent(w,h)
        self.sizeChanged.emit(w,h)

    def setGeometry(self, x: int, y: int, w: int, h: int):
        ''' Resize and move the widget

        :param int x: x position
        :param int y: y position
        :param int w: the new width
        :param int h: the new height
        '''
        self.resize(w, h)
        self.move(x, y)

    def pasteEvent(self, txt:str):
        return False

    _mouseOver = None
    _mouseOverTmp = None
    _mouseOverProcessed = False
    def mouseEvent(self, evt):
        ''' .. caution:: Don't touch this! '''
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
                    if self.dragMoveEvent(TTkHelper.dndGetDrag().getDragMoveEvent(evt)):
                        return True
                else:
                    if self.dragEnterEvent(TTkHelper.dndGetDrag().getDragEnterEvent(evt)):
                        if dndw:
                            ret = dndw.dragLeaveEvent(TTkHelper.dndGetDrag().getDragLeaveEvent(evt))
                        TTkHelper.dndEnter(self)
                        return True
            if evt.evt == TTkK.Release:
                if self.dropEvent(TTkHelper.dndGetDrag().getDropEvent(evt)):
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

    def setParent(self, parent):
        self._parent = parent
    def parentWidget(self):
        return self._parent

    def x(self): return self._x
    def y(self): return self._y
    def width(self):  return self._width
    def height(self): return self._height

    def pos(self):      return self._x, self._y
    def size(self):     return self._width, self._height
    def geometry(self): return self._x, self._y, self._width, self._height

    def maximumSize(self):
        return self.maximumWidth(), self.maximumHeight()
    def maxDimension(self, orientation) -> int:
        if orientation == TTkK.HORIZONTAL:
            return self.maximumWidth()
        else:
            return self.maximumHeight()
    def maximumHeight(self):
        return self._maxh
    def maximumWidth(self):
        return self._maxw

    def minimumSize(self):
        return self.minimumWidth(), self.minimumHeight()
    def minDimension(self, orientation) -> int:
        if orientation == TTkK.HORIZONTAL:
            return self.minimumWidth()
        else:
            return self.minimumHeight()
    def minimumHeight(self):
        return self._minh
    def minimumWidth(self):
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
    def show(self):
        '''show'''
        if self._visible: return
        self._visible = True
        self._canvas.show()
        self.update(updateLayout=True, updateParent=True)

    @pyTTkSlot()
    def hide(self):
        '''hide'''
        if not self._visible: return
        self._visible = False
        self._canvas.hide()
        self.update(repaint=False, updateParent=True)

    @pyTTkSlot()
    def raiseWidget(self, raiseParent=True):
        '''raiseWidget'''
        if self._parent is not None and \
           self._parent.rootLayout() is not None:
            if raiseParent:
                self._parent.raiseWidget(raiseParent)
            self._parent.rootLayout().raiseWidget(self)

    @pyTTkSlot()
    def lowerWidget(self):
        '''lowerWidget'''
        if self._parent is not None and \
           self._parent.rootLayout() is not None:
            self._parent.lowerWidget()
            self._parent.rootLayout().lowerWidget(self)

    @pyTTkSlot()
    def close(self):
        '''close'''
        if _p := self._parent:
            if _rl := _p.rootLayout():
                _rl.removeWidget(self)
            _p.update()
        TTkHelper.removeOverlayAndChild(self)
        self._parent = None
        self.hide()
        self.closed.emit(self)

    @pyTTkSlot(bool)
    def setVisible(self, visible: bool):
        '''setVisible'''
        if visible: self.show()
        else: self.hide()

    def isVisibleAndParent(self):
        return ( self._visible and
            ( self._parent is not None ) and
            self._parent.isVisibleAndParent() )

    def isVisible(self):
        return self._visible

    def update(self, repaint: bool =True, updateLayout: bool =False, updateParent: bool =False):
        if repaint:
            TTkHelper.addUpdateBuffer(self)
        TTkHelper.addUpdateWidget(self)
        if updateParent and self._parent is not None:
            self._parent.update(updateLayout=True)

    @pyTTkSlot()
    def setFocus(self):
        '''setFocus'''
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

    def clearFocus(self):
        # TTkLog.debug(f"clearFocus: {self._name} - {self._focus}")
        if not self._focus and self != TTkHelper.getFocus(): return
        TTkHelper.clearFocus()
        self._focus = False
        self.focusChanged.emit(self._focus)
        self.focusOutEvent()
        self._processStyleEvent(TTkWidget._S_DEFAULT)
        self.update(repaint=True, updateLayout=False)

    def hasFocus(self):
        return self._focus

    def getCanvas(self):
        return self._canvas

    def focusPolicy(self):
        return self._focus_policy

    def setFocusPolicy(self, policy):
        self._focus_policy = policy

    def focusInEvent(self): pass
    def focusOutEvent(self): pass

    def isEntered(self):
        return self._mouseOver == self

    def isEnabled(self):
        return self._enabled

    @pyTTkSlot(bool)
    def setEnabled(self, enabled: bool=True):
        '''setEnabled'''
        if self._enabled == enabled: return
        self._enabled = enabled
        self._processStyleEvent(TTkWidget._S_DEFAULT if enabled else TTkWidget._S_DISABLED)
        self.update()

    @pyTTkSlot(bool)
    def setDisabled(self, disabled=True):
        '''setDisabled'''
        self.setEnabled(not disabled)

    def toolTip(self):
        return self._toolTip

    def setToolTip(self, toolTip: TTkString):
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

    def style(self):
        return self._style

    def currentStyle(self):
        return self._currentStyle

    def setCurrentStyle(self, style):
        if style == self._currentStyle: return
        self._currentStyle = style
        self.currentStyleChanged.emit(style)
        self.update()

    def setStyle(self, style):
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

    def mergeStyle(self, style):
        cs = None
        for t in self._style:
            if self._style[t] == self._currentStyle:
                cs = t
            if t in style:
                self._style[t] =  self._style[t] | style[t]
        if cs:
            self.setCurrentStyle(self._style[cs])

    def _processStyleEvent(self, evt=_S_DEFAULT):
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
    def enableWidgetCursor(self, enable=True):
        self._widgetCursorEnabled = enable
        self._pushWidgetCursor()

    def disableWidgetCursor(self, disable=True):
        self._widgetCursorEnabled = not disable
        self._pushWidgetCursor()

    def setWidgetCursor(self, pos=None, type=None):
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
