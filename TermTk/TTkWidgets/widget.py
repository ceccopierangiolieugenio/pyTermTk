#!/usr/bin/env python3

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

from TermTk.TTkCore.cfg       import TTkCfg, TTkGlbl
from TermTk.TTkCore.constant  import TTkK
from TermTk.TTkCore.log       import TTkLog
from TermTk.TTkCore.helper    import TTkHelper
from TermTk.TTkCore.color     import TTkColor
from TermTk.TTkCore.string    import TTkString
from TermTk.TTkCore.canvas    import TTkCanvas
from TermTk.TTkCore.signal    import pyTTkSignal, pyTTkSlot
from TermTk.TTkTemplates.lookandfeel import TTkLookAndFeel
from TermTk.TTkTemplates.dragevents import TDragEvents
from TermTk.TTkTemplates.mouseevents import TMouseEvents
from TermTk.TTkTemplates.keyevents import TKeyEvents
from TermTk.TTkLayouts.layout import TTkLayout, TTkWidgetItem
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

class TTkWidget(TMouseEvents,TKeyEvents, TDragEvents):
    ''' Widget Layout sizes:

    ::

        Terminal area (i.e. XTerm)
        ┌─────────────────────────────────────────┐
        │                                         │
        │    TTkWidget     width                  │
        │ (x,y)┌─────────────────────────┐        │
        │      │      padt (Top Padding) │        │
        │      │    ┌───────────────┐    │ height │
        │      │padl│ Layout/child  │padr│        │
        │      │    └───────────────┘    │        │
        │      │      padb (Bottom Pad.) │        │
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

    :param int padding: the padding (top, bottom, left, right) of the widget, defaults to 0
    :param int paddingTop: the Top padding, override Top padding if already defined, optional, default=padding
    :param int paddingBottom: the Bottom padding, override Bottom padding if already defined, optional, default=padding
    :param int paddingLeft: the Left padding, override Left padding if already defined, optional, default=padding
    :param int paddingRight: the Right padding, override Right padding if already defined, optional, default=padding
    :param int maxWidth: the maxWidth of the widget, optional, defaults to 0x10000
    :param int maxHeight: the maxHeight of the widget, optional, defaults to 0x10000
    :param [int,int] maxSize: the max [width,height] of the widget, optional
    :param int minWidth: the minWidth of the widget, defaults to 0
    :param int minHeight: the minHeight of the widget, defaults to 0
    :param [int,int] minSize: the minSize [width,height] of the widget, optional

    :param toolTip: This property holds the widget's tooltip
    :type toolTip: :class:`~TermTk.TTkCore.string.TTkString`

    :param lookAndFeel: the style helper to be used for any customization
    :type lookAndFeel: :class:`~TermTk.TTkTemplates.lookandfeel.TTkTTkLookAndFeel`

    :param bool,optional visible: the visibility, optional, defaults to True
    :param bool,optional enabled: the ability to handle input events, optional, defaults to True
    :param layout: the layout of this widget, optional, defaults to :class:`~TermTk.TTkLayouts.layout.TTkLayout`
    :type layout: :mod:`TermTk.TTkLayouts`
    '''

    __slots__ = (
        '_name', '_parent',
        '_x', '_y', '_width', '_height',
        '_padt', '_padb', '_padl', '_padr',
        '_maxw', '_maxh', '_minw', '_minh',
        '_focus','_focus_policy',
        '_layout', '_canvas', '_widgetItem',
        '_visible', '_transparent',
        '_pendingMouseRelease',
        '_enabled',
        '_lookAndFeel', '_style', '_currentStyle',
        '_toolTip',
        #Signals
        'focusChanged', 'sizeChanged')

    def __init__(self, *args, **kwargs):
        #Signals
        self.focusChanged = pyTTkSignal(bool)
        self.sizeChanged = pyTTkSignal(int,int)
        # self.sizeChanged.connect(self.resizeEvent)

        self._name = kwargs.get('name', self.__class__.__name__)
        self._parent = kwargs.get('parent', None )

        self._lookAndFeel = None
        self.setLookAndFeel(kwargs.get('lookAndFeel', TTkLookAndFeel()))
        self._style = TTkWidget._BASE_STYLE
        self._currentStyle = TTkWidget._BASE_STYLE['default']

        self._pendingMouseRelease = False

        self._x = kwargs.get('x', 0 )
        self._y = kwargs.get('y', 0 )
        self._x, self._y = kwargs.get('pos', (self._x, self._y))
        self._width  = kwargs.get('width' , 0 )
        self._height = kwargs.get('height', 0 )
        self._width, self._height = kwargs.get('size', (self._width, self._height))

        padding = kwargs.get('padding', 0 )
        self._padt = kwargs.get('paddingTop',    padding )
        self._padb = kwargs.get('paddingBottom', padding )
        self._padl = kwargs.get('paddingLeft',   padding )
        self._padr = kwargs.get('paddingRight',  padding )

        self._maxw = kwargs.get('maxWidth',  0x10000)
        self._maxh = kwargs.get('maxHeight', 0x10000)
        self._maxw, self._maxh = kwargs.get('maxSize', (self._maxw, self._maxh))
        self._minw = kwargs.get('minWidth',  0x00000)
        self._minh = kwargs.get('minHeight', 0x00000)
        self._minw, self._minh = kwargs.get('minSize', (self._minw, self._minh))

        self._visible = kwargs.get('visible', True)
        self._enabled = kwargs.get('enabled', True)
        self._processStyleEvent(TTkWidget._S_DEFAULT)

        self._toolTip = TTkString(kwargs.get('toolTip',''))

        self._focus = False
        self._focus_policy = TTkK.NoFocus

        self._widgetItem = TTkWidgetItem(widget=self)

        self._layout = TTkLayout() # root layout
        self._layout.setParent(self)
        self._layout.addItem(kwargs.get('layout',TTkLayout())) # main layout

        self._canvas = TTkCanvas(
                            widget = self,
                            width  = self._width  ,
                            height = self._height )


        if self._parent and self._parent.layout():
            self._parent.layout().addWidget(self)
            self._parent.update(repaint=True, updateLayout=True)

        self.update(repaint=True, updateLayout=True)

    def __del__(self):
        ''' .. caution:: Don't touch this! '''
        # TTkLog.debug("DESTRUCTOR")

        # clean all the signals, slots
        #for an in dir(self):
        #    att = self.__getattribute__(an)
        #    # TODO: TBD, I need to find the time to do this

        if self._parent and self._parent.layout():
            self._parent.layout().removeWidget(self)
            self._parent = None

    def name(self):
        return self._name

    def widgetItem(self): return self._widgetItem

    def addWidget(self, widget):
        '''
        .. warning::
            Method Deprecated,

            use :class:`TTkWidget` -> :class:`~TermTk.TTkWidgets.widget.TTkWidget.layout` -> :class:`~TermTk.TTkLayouts.layout.TTkLayout.addWidget`

            i.e.

            .. code:: python

                parentWidget.layout().addWidget(childWidget)
        '''
        TTkLog.error("<TTkWidget>.addWidget(...) is deprecated, use <TTkWidget>.layout().addWidget(...)")
        if self.layout(): self.layout().addWidget(widget)

    def removeWidget(self, widget):
        '''
        .. warning::
            Method Deprecated,

            use :class:`TTkWidget` -> :class:`~TermTk.TTkWidgets.widget.TTkWidget.layout` -> :class:`~TermTk.TTkLayouts.layout.TTkLayout.removeWidget`

            i.e.

            .. code:: python

                parentWidget.layout().removeWidget(childWidget)
        '''
        TTkLog.error("<TTkWidget>.removeWidget(...) is deprecated, use <TTkWidget>.layout().removeWidget(...)")
        if self.layout(): self.layout().removeWidget(widget)

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
        ''' .. caution:: Don't touch this! '''
        lx,ly,lw,lh = geometry
        ox, oy = offset
        if item.layoutItemType() == TTkK.WidgetItem and not item.isEmpty():
            child = item.widget()
            cx,cy,cw,ch = child.geometry()
            canvas.paintCanvas(
                        child.getCanvas(),
                        (cx+ox, cy+oy, cw, ch), # geometry
                        (    0,     0, cw, ch), # slice
                        (   lx,    ly, lw, lh)) # bound
        else:
            for child in item.zSortedItems:
                # The Parent Layout Geometry (lx,ly,lw,lh) include the padding of the layout
                igx, igy, igw, igh = item.geometry()
                iox, ioy = item.offset()
                # Moved Layout to the new geometry (ix,iy,iw,ih)
                ix = igx+ox # + iox
                iy = igy+oy # + ioy
                iw = igw # -iox
                ih = igh # -ioy
                # return if Child outside the bound
                if ix+iw < lx and ix > lx+lw and iy+ih < ly and iy > ly+lh: continue
                # Crop the Layout based on the Parent Layout Geometry
                bx = max(ix,lx)
                by = max(iy,ly)
                bw = min(ix+iw,lx+lw)-bx
                bh = min(iy+ih,ly+lh)-by
                TTkWidget._paintChildCanvas(canvas, child, (bx,by,bw,bh), (ix+iox,iy+ioy))

    def paintChildCanvas(self):
        ''' .. caution:: Don't touch this! '''
        TTkWidget._paintChildCanvas(self._canvas, self.rootLayout(), self.rootLayout().geometry(), self.rootLayout().offset())

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

    def getPadding(self) -> (int, int, int, int):
        ''' Retrieve the widget padding sizes

        :return: list[top, bottom, left, right]: the 4 padding sizes
        '''
        return self._padt, self._padb, self._padl, self._padr

    def setPadding(self, top: int, bottom: int, left: int, right: int):
        ''' Set the padding of the widget

        :param int top: top padding
        :param int bottom: bottom padding
        :param int left: left padding
        :param int right: right padding
        '''
        if self._padt == top  and self._padb == bottom and \
           self._padl == left and self._padr == right: return
        self._padt = top
        self._padb = bottom
        self._padl = left
        self._padr = right
        self.update(repaint=True, updateLayout=True)

    @staticmethod
    def _mouseEventLayoutHandle(evt, layout):
        ''' .. caution:: Don't touch this! '''
        x, y = evt.x, evt.y
        lx,ly,lw,lh =layout.geometry()
        lox, loy = layout.offset()
        lx,ly,lw,lh = lx+lox, ly+loy, lw-lox, lh-loy
        # opt of bounds
        if x<lx or x>=lx+lw or y<ly or y>=lh+ly:
            return False
        x-=lx
        y-=ly
        for item in reversed(layout.zSortedItems):
        # for item in layout.zSortedItems:
            if item.layoutItemType() == TTkK.WidgetItem and not item.isEmpty():
                widget = item.widget()
                if not widget._visible: continue
                wx,wy,ww,wh = widget.geometry()
                # Skip the mouse event if outside this widget
                if not (wx <= x < wx+ww and wy <= y < wy+wh): continue
                wevt = evt.clone(pos=(x-wx, y-wy))
                if widget.mouseEvent(wevt):
                    return True
            elif item.layoutItemType() == TTkK.LayoutItem:
                levt = evt.clone(pos=(x, y))
                if TTkWidget._mouseEventLayoutHandle(levt, item):
                    return True
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

        if self.rootLayout() is not None:
            if  TTkWidget._mouseEventLayoutHandle(evt, self.rootLayout()):
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
            if w.focusPolicy() & TTkK.ClickFocus == TTkK.ClickFocus:
                w.setFocus()
                w.raiseWidget()
            self._processStyleEvent(TTkWidget._S_PRESSED)
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

    def setLayout(self, layout):
        self._layout.replaceItem(layout, 0)
        #self.layout().setParent(self)
        self.update(repaint=True, updateLayout=True)

    def layout(self):
        ''' Get the layout

        :return: The layout used
        :rtype: :class:`TTkLayout` or derived
        '''
        return self._layout.itemAt(0)
    def rootLayout(self): return self._layout

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
        wMaxH = self._maxh
        if self.layout() is not None:
            lMaxH = self.layout().maximumHeight() + self._padt + self._padb
            if lMaxH < wMaxH:
                return lMaxH
        return wMaxH
    def maximumWidth(self):
        wMaxW = self._maxw
        if self.layout() is not None:
            lMaxW = self.layout().maximumWidth() + self._padl + self._padr
            if lMaxW < wMaxW:
                return lMaxW
        return wMaxW

    def minimumSize(self):
        return self.minimumWidth(), self.minimumHeight()
    def minDimension(self, orientation) -> int:
        if orientation == TTkK.HORIZONTAL:
            return self.minimumWidth()
        else:
            return self.minimumHeight()
    def minimumHeight(self):
        wMinH = self._minh
        if self.layout() is not None:
            lMinH = self.layout().minimumHeight() + self._padt + self._padb
            if lMinH > wMinH:
                return lMinH
        return wMinH
    def minimumWidth(self):
        wMinW = self._minw
        if self.layout() is not None:
            lMinW = self.layout().minimumWidth() + self._padl + self._padr
            if lMinW > wMinW:
                return lMinW
        return wMinW

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
        for w in self.rootLayout().iterWidgets(onlyVisible=True):
            w.update()

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
        if self._parent is not None and \
           self._parent.rootLayout() is not None:
            self._parent.rootLayout().removeWidget(self)
            self._parent.update()
        TTkHelper.removeOverlayAndChild(self)
        self._parent = None
        self.hide()

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
        if updateLayout and self.rootLayout() is not None:
            self.rootLayout().setGeometry(0,0,self._width,self._height)
            self.layout().setGeometry(
                        self._padl, self._padt,
                        self._width   - self._padl - self._padr,
                        self._height  - self._padt - self._padb)
        if updateParent and self._parent is not None:
            self._parent.update(updateLayout=True)
        if updateLayout and self.rootLayout() is not None:
            self.rootLayout().update()

    @pyTTkSlot()
    def setFocus(self):
        '''setFocus'''
        # TTkLog.debug(f"setFocus: {self._name} - {self._focus}")
        if self._focus and self == TTkHelper.getFocus(): return
        tmp = TTkHelper.getFocus()
        if tmp == self: return
        if tmp is not None:
            tmp.clearFocus()
        TTkHelper.removeOverlayChild(self)
        TTkHelper.setFocus(self)
        self._focus = True
        self.focusChanged.emit(self._focus)
        self.focusInEvent()

    def clearFocus(self):
        # TTkLog.debug(f"clearFocus: {self._name} - {self._focus}")
        if not self._focus and self != TTkHelper.getFocus(): return
        TTkHelper.clearFocus()
        self._focus = False
        self.focusChanged.emit(self._focus)
        self.focusOutEvent()
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

    def lookAndFeel(self):
        return self._lookAndFeel

    def setLookAndFeel(self, laf):
        if self._lookAndFeel:
            self._lookAndFeel.modified.disconnect(self.update)
        if not laf:
            laf = TTkLookAndFeel()
        self._lookAndFeel = laf
        self._lookAndFeel.modified.connect(self.update)

    def toolTip(self):
        return self._toolTip

    def setToolTip(self, toolTip: TTkString):
        self._toolTip = toolTip

    def getWidgetByName(self, name: str):
        if name == self._name:
            return self
        for w in self.rootLayout().iterWidgets(onlyVisible=False, recurse=True):
            if w._name == name:
                return w
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

    def setStyle(self, style):
        self._style = style[type(self)]
        self._processStyleEvent(TTkWidget._S_DEFAULT)

    def _processStyleEvent(self, evt):
        if not self._style: return False
        if not self._enabled and 'disabled' in self._style:
            self._currentStyle = self._style['disabled']
            self.update()
            return True

        self._currentStyle = self._style['default']
        if evt in (TTkWidget._S_DEFAULT,
                   TTkWidget._S_NONE,
                   TTkWidget._S_ACTIVE) and 'default' in self._style:
            self._currentStyle = self._style['default']
            self.update()
            return True
        elif evt & TTkWidget._S_HOVER and 'hover' in self._style:
            self._currentStyle = self._style['hover']
            self.update()
            return True
        elif evt & TTkWidget._S_PRESSED and 'clicked' in self._style:
            self._currentStyle = self._style['clicked']
            self.update()
            return True
        elif evt & TTkWidget._S_DISABLED and 'disabled' in self._style:
            self._currentStyle = self._style['disabled']
            self.update()
            return True
        return False