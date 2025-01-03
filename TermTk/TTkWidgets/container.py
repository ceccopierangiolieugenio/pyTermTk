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

__all__ = ['TTkContainer', 'TTkPadding']

from typing import NamedTuple

from TermTk.TTkCore.constant  import TTkK
from TermTk.TTkCore.log       import TTkLog
from TermTk.TTkCore.helper    import TTkHelper
from TermTk.TTkCore.signal    import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkWidgets.widget import TTkWidget

class TTkPadding(NamedTuple):
    top    : int = 0
    bottom : int = 0
    left   : int = 0
    right  : int = 0

class TTkContainer(TTkWidget):
    '''
    :py:class:`TTkContainer` include the layout management through :py:class:`TTkLayout` or one of its implementations.

    It is the base class of all the composite widgets like :py:class:`TTkSpinBox`
    where a :py:class:`TTkLineEdit` is placed and shown when edited, or in the :py:class:`TTkFrame` and
    its extension :py:class:`TTkWindow` where the :py:class:`TTkLayout` is used for the child
    widgets placements or the :py:class:`TTkMenuBarLayout`,
    the main root widget :py:class:`TTk` inherit the layout capabilities of :py:class:`TTkContainer` for any widget placed in the `pyTermTk <https://github.com/ceccopierangiolieugenio/pyTermTk>`__ app.

    Main widgets subclassing :py:class:`TTkContainer`:

    #. :py:class:`TTk`
    #. :py:class:`TTkFrame`
    #. :py:class:`TTkWindow`
    #. :py:class:`TTkSplitter`
    #. :py:class:`TTkAppTemplate`
    #. :py:class:`TTkTabWidget`
    #. :py:class:`TTkTreeWidget`

    More info and examples are available in the :ref:`Tutorial <Layout-Tutorial_Intro>`

    .. _Container-Layout-Topology:

    :py:class:`TTkContainer` Layout topology:

    ::

        Terminal area (i.e. XTerm) = TTk
        ┌────────────────────────────────────────────┐
        │                                            │
        │   TTkContainer                             │
        │       < --------  width  ----->            │
        │ (x,y)╔═════════════════════════╗  ^        │
        │      ║      padt (Top Padding) ║  |        │
        │      ║    ┌───────────────┐    ║  | height │
        │      ║padl│ Layout        │padr║  |        │
        │      ║    └───────────────┘    ║  |        │
        │      ║      padb (Bottom Pad.) ║  |        │
        │      ╚═════════════════════════╝  v        │
        └────────────────────────────────────────────┘

    Example:

    .. code-block:: python

        from TermTk import TTk, TTkButton, TTkHBoxLayout

        # The class TTk, that could be referred as the terminal layout, is a subclass of TTkContainer
        root = TTk( layout=TTkHBoxLayout(), padding=(1,2,4,8))

        TTkButton(parent=root, border=True,  text="Btn 1!")
        TTkButton(parent=root, border=True,  text="Btn 2!")
        TTkButton(parent=root, border=True,  text="Btn 3!")
        TTkButton(parent=root, border=True,  text="Btn 4!")

        root.mainloop()

    '''

    __slots__ = (
        '_padt', '_padb', '_padl', '_padr',
        '_forwardStyle',
        '_layout')

    def __init__(self, *,
                 layout:TTkLayout=None,
                 padding:TTkPadding = None,
                 paddingTop:int = 0,
                 paddingBottom:int = 0,
                 paddingLeft:int = 0,
                 paddingRight:int = 0,
                 forwardStyle:bool = False,
                 **kwargs) -> None:
        '''
        :param layout: the layout of this widget, optional, defaults to :py:class:`TTkLayout`
        :type layout: :mod:`TermTk.TTkLayouts`

        :param padding: the padding (top, bottom, left, right) of the widget, defaults to (0,0,0,0)
        :type padding: :py:class:`TTkPadding`

        :param paddingTop: the Top padding, override Top padding if already defined, optional, default=0 if padding is not defined
        :type paddingTop: int
        :param paddingBottom: the Bottom padding, override Bottom padding if already defined, optional, default=0 if padding is not defined
        :type paddingBottom: int
        :param paddingLeft: the Left padding, override Left padding if already defined, optional, default=0 if padding is not defined
        :type paddingLeft: int
        :param paddingRight: the Right padding, override Right padding if already defined, optional, default=0 if padding is not defined
        :type paddingRight: int

        :param bool forwardStyle: [**Experimental**] any change of style will reflect the children, defaults to False
        :type forwardStyle: bool
        '''
        self._forwardStyle = forwardStyle
        if padding:
            self._padt = padding[0]
            self._padb = padding[1]
            self._padl = padding[2]
            self._padr = padding[3]
        else:
            self._padt = paddingTop
            self._padb = paddingBottom
            self._padl = paddingLeft
            self._padr = paddingRight

        self._layout = TTkLayout() # root layout
        self._layout.addItem(layout if layout else TTkLayout()) # main layout

        super().__init__(**kwargs)

        self._layout.setParent(self)
        self.update(updateLayout=True)

    def addWidget(self, widget:TTkWidget) -> None:
        '''
        .. warning::
            Method Deprecated,

            use :py:class:`TTkContainer` -> :py:meth:`layout` -> :py:class:`TTkLayout.addWidget`

            i.e.

            .. code:: python

                parentWidget.layout().addWidget(childWidget)
        '''
        TTkLog.error("<TTkWidget>.addWidget(...) is deprecated, use <TTkWidget>.layout().addWidget(...)")
        if self.layout(): self.layout().addWidget(widget)

    def removeWidget(self, widget:TTkWidget) -> None:
        '''
        .. warning::
            Method Deprecated,

            use :py:class:`TTkContainer` -> :py:meth:`layout` -> :py:class:`TTkLayout.removeWidget`

            i.e.

            .. code:: python

                parentWidget.layout().removeWidget(childWidget)
        '''
        TTkLog.error("<TTkWidget>.removeWidget(...) is deprecated, use <TTkWidget>.layout().removeWidget(...)")
        if self.layout(): self.layout().removeWidget(widget)

    # def forwardStyleTo(self, widget:TTkWidget):
    #     widget._currentStyle |= self._currentStyle
    #     widget.update()

    def _processForwardStyle(self) -> None:
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

    def setCurrentStyle(self, *args, **kwargs) -> None:
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

    def paintChildCanvas(self) -> None:
        ''' .. caution:: Don't touch this! '''
        TTkContainer._paintChildCanvas(self._canvas, self.rootLayout(), self.rootLayout().geometry(), self.rootLayout().offset())

    def getPadding(self) -> TTkPadding:
        ''' Retrieve the :py:class:`TTkContainer`'s paddings sizes as shown in :ref:`Layout Topology <Container-Layout-Topology>`

        :return: :py:class:`TTkPadding` the NamedTuple representing a 4 int values tuple (top,bottom,left,right)
        '''
        return TTkPadding(self._padt, self._padb, self._padl, self._padr)

    def setPadding(self, top: int, bottom: int, left: int, right: int) -> None:
        ''' Set the :py:class:`TTkContainer`'s paddings sizes as shown in :ref:`Layout Topology <Container-Layout-Topology>`

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

    def _mouseEventParseChildren(self, evt:TTkMouseEvent) -> bool:
        return TTkContainer._mouseEventLayoutHandle(evt, self.rootLayout())

    def setLayout(self, layout:TTkLayout) -> None:
        '''
        Set the :ref:`Layout <Layout-Tutorial_Intro>` used by this widget to place all the child widgets.

        :param layout:
        :type layout: :py:class:`TTkLayout`
        '''
        self._layout.replaceItem(layout, 0)
        #self.layout().setParent(self)
        self.update(repaint=True, updateLayout=True)

    def layout(self) -> TTkLayout:
        '''
        Get the :ref:`Layout <Layout-Tutorial_Intro>`

        :return: The :ref:`Layout <Layout-Tutorial_Intro>` used
        :rtype: :py:class:`TTkLayout` or derived
        '''
        return self._layout.itemAt(0)

    def rootLayout(self) -> TTkLayout:
        '''
        This is a root layout mainly used to place items that are not supposed to be inside the main layout (i.e. the menu elements)

        .. caution:: Use this layout only if you know what you are doing

        :return: :py:class:``TTkLayout`
        '''
        return self._layout

    def maximumHeight(self) -> int:
        wMaxH = self._maxh
        if self.layout() is not None:
            lMaxH = self.layout().maximumHeight() + self._padt + self._padb
            if lMaxH < wMaxH:
                return lMaxH
        return wMaxH
    def maximumWidth(self) -> int:
        wMaxW = self._maxw
        if self.layout() is not None:
            lMaxW = self.layout().maximumWidth() + self._padl + self._padr
            if lMaxW < wMaxW:
                return lMaxW
        return wMaxW

    def minimumHeight(self) -> int:
        wMinH = self._minh
        if self.layout() is not None:
            lMinH = self.layout().minimumHeight() + self._padt + self._padb
            if lMinH > wMinH:
                return lMinH
        return wMinH
    def minimumWidth(self) -> int:
        wMinW = self._minw
        if self.layout() is not None:
            lMinW = self.layout().minimumWidth() + self._padl + self._padr
            if lMinW > wMinW:
                return lMinW
        return wMinW

    @pyTTkSlot()
    def show(self) -> None:
        if self._visible: return
        self._visible = True
        self._canvas.show()
        self.update(updateLayout=True, updateParent=True)
        for w in self.rootLayout().iterWidgets(onlyVisible=True):
            w.update()

    @pyTTkSlot()
    def hide(self) -> None:
        if not self._visible: return
        self._visible = False
        self._canvas.hide()
        self.update(repaint=False, updateParent=True)

    def update(self, repaint: bool = True, updateLayout: bool = False, updateParent: bool = False) -> None:
        super().update(repaint=repaint, updateLayout=updateLayout, updateParent=updateParent)
        if updateLayout and self.rootLayout() is not None and self.size() != (0,0):
            self.rootLayout().setGeometry(0,0,self._width,self._height)
            self.layout().setGeometry(
                        self._padl, self._padt,
                        self._width   - self._padl - self._padr,
                        self._height  - self._padt - self._padb)
            self.rootLayout().update()

    def getWidgetByName(self, name: str) -> TTkWidget:
        '''
        Return the widget from its name.

        :param name: the widget's name, normally defined in the constructor or through :py:meth:`TTkWidget.setName`
        :type name:

        :return: :py:class:`TTkWidget`
        '''
        if name == self._name:
            return self
        for w in self.rootLayout().iterWidgets(onlyVisible=False, recurse=True):
            if w._name == name:
                return w
        return None
