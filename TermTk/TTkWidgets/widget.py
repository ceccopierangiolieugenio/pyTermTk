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

import TermTk.libbpytop as lbt
from TermTk.TTkCore.canvas import *
from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.signal import *
from TermTk.TTkLayouts.layout import TTkLayout, TTkWidgetItem


class TTkWidget:
    # Focus Policies
    NoFocus    = 0x0000
    ClickFocus = 0x0001
    WheelFocus = 0x0002
    TabFocus   = 0x0004

    # positions
    NONE   = 0x0000
    TOP    = 0x0001
    BOTTOM = 0x0002
    LEFT   = 0x0004
    RIGHT  = 0x0008

    '''
    Terminal
    ┌─────────────────────────────────────────┐
    │                                         │
    │    TTkWidget     width                  │
    │ (x,y)┌─────────────────────────┐        │
    │      │      padt               │        │
    │      │    ┌───────────────┐    │ height │
    │      │padl│ Layout/childs │padr│        │
    │      │    └───────────────┘    │        │
    │      │      padl               │        │
    │      └─────────────────────────┘        │
    └─────────────────────────────────────────┘
    '''
    __slots__ = (
        '_name', '_parent',
        '_x', '_y', '_width', '_height',
        '_padt', '_padb', '_padl', '_padr',
        '_maxw', '_maxh', '_minw', '_minh',
        '_focus','_focus_policy',
        '_layout', '_canvas', '_visible')

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name', None )
        self._parent = kwargs.get('parent', None )

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

        self._focus = False
        self._focus_policy = TTkWidget.NoFocus

        self._canvas = TTkCanvas(
                            widget = self,
                            width  = self._width  ,
                            height = self._height )
        self.setLayout(kwargs.get('layout',TTkLayout()))
        if self._parent is not None:
            self._parent.addWidget(self)
            self._parent.update(repaint=True, updateLayout=True)

        self.update(repaint=True, updateLayout=True)

    def addWidget(self, widget):
        if self._layout is not None:
            self._layout.addWidget(widget)
            self.update(repaint=True, updateLayout=True)

    def removeWidget(self, widget):
        if self._layout is not None:
            self._layout.removeWidget(widget)
            self.update(repaint=True, updateLayout=True)

    def paintEvent(self): pass

    def paintChildCanvas(self):
        # paint over child canvas
        lx,ly,lw,lh = self._layout.geometry()
        for item in self._layout.zSortedItems:
            if isinstance(item, TTkWidgetItem) and not item.isEmpty():
                child = item.widget()
                cx,cy,cw,ch = child.geometry()
                self._canvas.paintCanvas(
                                child.getCanvas(),
                                (cx,  cy,  cw, ch),
                                (0,0,cw,ch),
                                (lx, ly, lw, lh))

    def paintNotifyParent(self):
        parent = self._parent
        while parent is not None:
            parent._canvas.clean()
            parent.paintEvent()
            parent.paintChildCanvas()
            parent = parent._parent

    def moveEvent(self, x, y): pass
    def resizeEvent(self, w, h): pass

    def move(self, x, y):
        self._x = x
        self._y = y
        self.update(repaint=False, updateLayout=False)
        self.moveEvent(x,y)

    def resize(self, w, h):
        self._width  = w
        self._height = h
        self._canvas.resize(self._width, self._height)
        if self._layout is not None:
            self._layout.setGeometry(
                                self._padl, self._padt,
                                self._width   - self._padl - self._padr,
                                self._height  - self._padt - self._padb)
        self.update(repaint=True, updateLayout=True)
        self.resizeEvent(w,h)

    def setGeometry(self, x, y, w, h):
        self.resize(w, h)
        self.move(x, y)

    def getPadding(self):
        return self._padt, self._padb, self._padl, self._padr

    def setPadding(self, top, bottom, left, right):
        self._padt = top
        self._padb = bottom
        self._padl = left
        self._padr = right
        if self._layout is not None:
            self._layout.setGeometry(
                                self._padl, self._padt,
                                self._width   - self._padl - self._padr,
                                self._height  - self._padt - self._padb)

    def mouseDoubleClickEvent(self, evt): return False
    def mouseMoveEvent(self, evt): return False
    def mouseDragEvent(self, evt): return False
    def mousePressEvent(self, evt): return False
    def mouseReleaseEvent(self, evt): return False
    def wheelEvent(self, evt): return False
    def enterEvent(self, evt): return False
    def leaveEvent(self, evt): return False
    def keyPressEvent(self, evt): return False
    def keyReleaseEvent(self, evt): return False

    @staticmethod
    def _mouseEventLayoutHandle(evt, layout):
        x, y = evt.x, evt.y
        lx,ly,lw,lh =layout.geometry()
        # opt of bounds
        if x<lx or x>lx+lw or y<ly or y>lh+ly:
            return True
        for item in reversed(layout.zSortedItems):
        # for item in layout.zSortedItems:
            if isinstance(item, TTkWidgetItem) and not item.isEmpty():
                widget = item.widget()
                if not widget._visible: continue
                wevt = None
                mouseEvent = False
                if isinstance(evt, lbt.MouseEvent):
                    mouseEvent = True
                    wx,wy,ww,wh = widget.geometry()
                    # Skip the mouse event if outside this widget
                    if x >= wx and x<wx+ww and y>=wy and y<wy+wh:
                        wevt = evt.clone(pos=(x-wx, y-wy))
                if mouseEvent:
                    if wevt is not None:
                        #if not widget._data['mouse']['underMouse']:
                        #    widget._data['mouse']['underMouse'] = True
                        #    widget.enterEvent(wevt)
                        if widget.mouseEvent(wevt):
                            return True
                    #else:
                    #    if widget._data['mouse']['underMouse']:
                    #        widget._data['mouse']['underMouse'] = False
                    #        widget.leaveEvent(evt)
                    #    if widget._data['layout'] is not None:
                    #        CuWidget._broadcastLeaveEvent(evt, widget._data['layout'])
                    continue

                #if widget.event(evt):
                #    return True
            elif isinstance(item, TTkLayout):
                levt = evt.clone(pos=(x, y))
                if TTkWidget._mouseEventLayoutHandle(levt, item):
                    return True
        return False

    def mouseEvent(self, evt):
        # handle own events
        if evt.evt == lbt.MouseEvent.Move:
            if self.mouseMoveEvent(evt):
                return True
        if evt.evt == lbt.MouseEvent.Drag:
            if self.mouseDragEvent(evt):
                return True
        elif   evt.evt == lbt.MouseEvent.Release:
            #if self.hasFocus():
            #    self.clearFocus()
            if self.mouseReleaseEvent(evt):
                return True
        elif   evt.evt == lbt.MouseEvent.Press:
            if self.focusPolicy() & TTkWidget.ClickFocus == TTkWidget.ClickFocus:
                self.setFocus()
                self.raiseWidget()
            if self.mousePressEvent(evt):
                TTkLog.debug(f"Click {self._name}")
                return True
        elif evt.key == lbt.MouseEvent.Wheel:
            if self.wheelEvent(evt):
                return True
            #if self.focusPolicy() & CuT.WheelFocus == CuT.WheelFocus:
            #    self.setFocus()
        #elif evt.type() == CuEvent.KeyPress:
        #    self.keyPressEvent(evt)
        #elif evt.type() == CuEvent.KeyRelease:
        #    self.keyReleaseEvent(evt)
        # Trigger this event to the childs
        if self._layout is not None:
            return TTkWidget._mouseEventLayoutHandle(evt, self._layout)

    def keyEvent(self, evt):
        pass

    #def event(self, evt):
    #    pass
#        # handle own events
#        if evt.type() == CuEvent.MouseMove:
#            if evt.button() == CuT.NoButton:
#                self.mouseMoveEvent(evt)
#        elif   evt.type() == CuEvent.MouseButtonRelease:
#            self.mouseReleaseEvent(evt)
#        elif evt.type() == CuEvent.MouseButtonPress:
#            self.mousePressEvent(evt)
#            if self.focusPolicy() & CuT.ClickFocus == CuT.ClickFocus:
#                self.setFocus()
#        elif evt.type() == CuEvent.Wheel:
#            self.wheelEvent(evt)
#            if self.focusPolicy() & CuT.WheelFocus == CuT.WheelFocus:
#                self.setFocus()
#        elif evt.type() == CuEvent.KeyPress:
#            self.keyPressEvent(evt)
#        elif evt.type() == CuEvent.KeyRelease:
#            self.keyReleaseEvent(evt)
#        # Trigger this event to the childs
#        if self._layout is not None:
#            return CuWidget._eventLayoutHandle(evt, self._layout)

    def setLayout(self, layout):
        self._layout = layout
        self._layout.setParent(self)
        self._layout.setGeometry(
                        self._padl, self._padt,
                        self._width   - self._padl - self._padr,
                        self._height  - self._padt - self._padb)
        self.update(repaint=True, updateLayout=True)

    def layout(self): return self._layout

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
    def maximumHeight(self):
        wMaxH = self._maxh
        if self._layout is not None:
            lMaxH = self._layout.maximumHeight() + self._padt + self._padb
            if lMaxH < wMaxH:
                return lMaxH
        return wMaxH
    def maximumWidth(self):
        wMaxW = self._maxw
        if self._layout is not None:
            lMaxW = self._layout.maximumWidth() + self._padl + self._padr
            if lMaxW < wMaxW:
                return lMaxW
        return wMaxW

    def minimumSize(self):
        return self.minimumWidth(), self.minimumHeight()
    def minimumHeight(self):
        wMinH = self._minh
        if self._layout is not None:
            lMinH = self._layout.minimumHeight() + self._padt + self._padb
            if lMinH > wMinH:
                return lMinH
        return wMinH
    def minimumWidth(self):
        wMinW = self._minw
        if self._layout is not None:
            lMinW = self._layout.minimumWidth() + self._padl + self._padr
            if lMinW > wMinW:
                return lMinW
        return wMinW

    def setMaximumSize(self, maxw, maxh):
        self.setMaximumWidth(maxw)
        self.setMaximumHeight(maxh)
    def setMaximumHeight(self, maxh):
        self._maxh = maxh
        self.update(updateLayout=True, updateParent=True)
    def setMaximumWidth(self, maxw):
        self._maxw = maxw
        self.update(updateLayout=True, updateParent=True)

    def setMinimumSize(self, minw, minh):
        self.setMinimumWidth(minw)
        self.setMinimumHeight(minh)
    def setMinimumHeight(self, minh):
        self._minh = minh
        self.update(updateLayout=True, updateParent=True)
    def setMinimumWidth(self, minw):
        self._minw = minw
        self.update(updateLayout=True, updateParent=True)

    #@staticmethod
    #def _showHandle(layout):
    #    for i in range(layout.count()):
    #        item = layout.itemAt(i)
    #        if isinstance(item, CuWidgetItem) and not item.isEmpty():
    #            item.widget().show()
    #        elif isinstance(item, CuLayout):
    #            CuWidget._showHandle(item)

    @pyTTkSlot()
    def show(self):
        self._canvas.show()
        self._visible = True
        self.update()
    #    if self._data['layout'] is not None:
    #        CuWidget._showHandle(self._data['layout'])

    #@staticmethod
    #def _hideHandle(layout):
    #    for i in range(layout.count()):
    #        item = layout.itemAt(i)
    #        if isinstance(item, CuWidgetItem) and not item.isEmpty():
    #            item.widget().hide()
    #        elif isinstance(item, CuLayout):
    #            CuWidget._hideHandle(item)

    @pyTTkSlot()
    def hide(self):
        self._canvas.hide()
        self._visible = False
        # self._parent._canvas.clean(self.pos(),self.size())
        self.update()
    #    if self._layout is not None:
    #        TTkWidget._hideHandle(self._layout])

    def raiseWidget(self):
        if self._parent is not None and \
           self._parent._layout is not None:
            self._parent.raiseWidget()
            self._parent._layout.raiseWidget(self)

    def lowerWidget(self):
        if self._parent is not None and \
           self._parent._layout is not None:
            self._parent.lowerWidget()
            self._parent._layout.lowerWidget(self)

    def close(self): pass

    def isVisible(self):
        return self._visible

    def update(self, repaint=True, updateLayout=False, updateParent=False):
        if repaint:
            TTkHelper.addUpdateBuffer(self)
        TTkHelper.addUpdateWidget(self)
        if updateLayout and self._layout is not None:
            self._layout.update()
        if updateParent and self._parent is not None:
            self._parent.update(updateLayout=True)

    def setFocus(self):
        tmp = TTkHelper.getFocus()
        if tmp is not None:
            tmp.clearFocus()
            tmp.focusOutEvent()
            tmp.update(repaint=True, updateLayout=False)
        TTkHelper.setFocus(self)
        self._focus = True
        self.focusInEvent()

    def clearFocus(self):
        TTkHelper.clearFocus()
        self._focus = False
        self.focusOutEvent()

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