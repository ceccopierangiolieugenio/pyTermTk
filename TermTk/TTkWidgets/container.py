# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkContainer']

from TermTk.TTkCore.constant  import TTkK
from TermTk.TTkCore.log       import TTkLog
from TermTk.TTkCore.helper    import TTkHelper
from TermTk.TTkCore.signal    import pyTTkSignal, pyTTkSlot
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkWidgets.widget import TTkWidget

class TTkContainer(TTkWidget):
    ''' TTkContainer Layout sizes:

    ::

        Terminal area (i.e. XTerm) = TTk
        ┌─────────────────────────────────────────┐
        │                                         │
        │    TTkContainer   width                 │
        │ (x,y)┌─────────────────────────┐        │
        │      │      padt (Top Padding) │        │
        │      │    ┌───────────────┐    │ height │
        │      │padl│ Layout/child  │padr│        │
        │      │    └───────────────┘    │        │
        │      │      padb (Bottom Pad.) │        │
        │      └─────────────────────────┘        │
        └─────────────────────────────────────────┘

    :param bool forwardStyle: any change of style will reflect the children, defaults to False
    :type forwardStyle: bool

    :param int padding: the padding (top, bottom, left, right) of the widget, defaults to 0
    :param int paddingTop: the Top padding, override Top padding if already defined, optional, default=padding
    :param int paddingBottom: the Bottom padding, override Bottom padding if already defined, optional, default=padding
    :param int paddingLeft: the Left padding, override Left padding if already defined, optional, default=padding
    :param int paddingRight: the Right padding, override Right padding if already defined, optional, default=padding

    :param layout: the layout of this widget, optional, defaults to :class:`~TermTk.TTkLayouts.layout.TTkLayout`
    :type layout: :mod:`TermTk.TTkLayouts`
    '''

    __slots__ = (
        '_padt', '_padb', '_padl', '_padr',
        '_forwardStyle',
        '_layout')

    def __init__(self, *, padding=(0,0,0,0), forwardStyle=False,**kwargs):

        self._forwardStyle = forwardStyle
        padding = kwargs.get('padding', 0 )
        self._padt = kwargs.get('paddingTop',    padding )
        self._padb = kwargs.get('paddingBottom', padding )
        self._padl = kwargs.get('paddingLeft',   padding )
        self._padr = kwargs.get('paddingRight',  padding )

        self._layout = TTkLayout() # root layout
        self._layout.addItem(kwargs.get('layout',TTkLayout())) # main layout

        super().__init__(**kwargs)

        self._layout.setParent(self)
        self.update(updateLayout=True)

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

    # def forwardStyleTo(self, widget:TTkWidget):
    #     widget._currentStyle |= self._currentStyle
    #     widget.update()

    def _processForwardStyle(self):
        if not self._forwardStyle: return
        def _getChildren():
            for w in self.rootLayout().iterWidgets(onlyVisible=True, recurse=False):
                yield w
            for w in self.layout().iterWidgets(onlyVisible=True, recurse=False):
                yield w

        for w in _getChildren():
            self.setCurrentStyle(w._currentStyle | self._currentStyle)
            if issubclass(type(w),TTkContainer):
                w._processForwardStyle()

    def setCurrentStyle(self, *args, **kwargs):
        super().setCurrentStyle(*args, **kwargs)
        self._processForwardStyle()

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
                TTkContainer._paintChildCanvas(canvas, child, (bx,by,bw,bh), (ix+iox,iy+ioy))

    def paintChildCanvas(self):
        ''' .. caution:: Don't touch this! '''
        TTkContainer._paintChildCanvas(self._canvas, self.rootLayout(), self.rootLayout().geometry(), self.rootLayout().offset())

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
                if TTkContainer._mouseEventLayoutHandle(levt, item):
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
            if  TTkContainer._mouseEventLayoutHandle(evt, self.rootLayout()):
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

    def update(self, repaint: bool =True, updateLayout: bool =False, updateParent: bool =False):
        super().update(repaint=repaint, updateLayout=updateLayout, updateParent=updateParent)
        if updateLayout and self.rootLayout() is not None:
            self.rootLayout().setGeometry(0,0,self._width,self._height)
            self.layout().setGeometry(
                        self._padl, self._padt,
                        self._width   - self._padl - self._padr,
                        self._height  - self._padt - self._padb)
            self.rootLayout().update()

    def getWidgetByName(self, name: str):
        if name == self._name:
            return self
        for w in self.rootLayout().iterWidgets(onlyVisible=False, recurse=True):
            if w._name == name:
                return w
        return None
