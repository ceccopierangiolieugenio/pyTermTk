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

'''
**Layout** [`Tutorial <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/002-layout.html#simple-ttklayout>`__]
'''

__all__ = ['TTkLayoutItem', 'TTkLayout']

from TermTk.TTkCore.constant import TTkK

class TTkLayoutItem:
    ''' :class:`~TTkLayoutItem` is the base class of layout Items inherited by :class:`~TTkLayout`, :class:`~TTkWidgetItem`, and all the derived layout managers.

    :param int row:     (used only in the :class:`~TermTk.TTkLayouts.gridlayout.TTkGridLayout`), the row of the grid,   optional, defaults to None
    :param int col:     (used only in the :class:`~TermTk.TTkLayouts.gridlayout.TTkGridLayout`), the col of the grid,   optional, defaults to None
    :param int rowspan: (used only in the :class:`~TermTk.TTkLayouts.gridlayout.TTkGridLayout`), the rows used by this, optional, defaults to 1
    :param int colspan: (used only in the :class:`~TermTk.TTkLayouts.gridlayout.TTkGridLayout`), the cols used by this, optional, defaults to 1
    :param layoutItemType: The Type of this class, optional, defaults to TTkK.NONE
    :type  layoutItemType: :class:`~TermTk.TTkCore.constant.TTkConstant.LayoutItemTypes`
    :param alignment: The alignment of this item in the layout (not yet used)
    :type  alignment: :class:`~TermTk.TTkCore.constant.TTkConstant.Alignment`
    '''

    LAYER0    =  0x00000000
    LAYER1    =  0x40000000
    LAYER2    =  0x80000000
    LAYER3    =  0xC0000000
    LAYERMASK = ~0xC0000000

    __slots__ = (
        '_x', '_y', '_z', '_w', '_h',
        '_layer',
        '_xOffset', '_yOffset',
        '_maxw', '_maxh', '_minw', '_minh',
        '_row','_col',
        '_rowspan', '_colspan',
        '_sMax', '_sMaxVal',
        '_sMin', '_sMinVal',
        '_parent',
        '_alignment',
        '_layoutItemType')

    def __init__(self, *args, **kwargs):
        self._x = kwargs.get('x', 0 )
        self._y = kwargs.get('y', 0 )
        self._x, self._y = kwargs.get('pos', (self._x, self._y))
        self._w  = kwargs.get('width' , 0 )
        self._h = kwargs.get('height', 0 )
        self._w, self._h = kwargs.get('size', (self._w, self._h))
        self._z = kwargs.get('z',0)
        self._layer = TTkLayoutItem.LAYER0
        self._xOffset = 0
        self._yOffset = 0
        self._row = kwargs.get('row', 0)
        self._col = kwargs.get('col', 0)
        self._rowspan = kwargs.get('rowspan', 1)
        self._colspan = kwargs.get('colspan', 1)
        self._layoutItemType = kwargs.get('layoutItemType', TTkK.NONE)
        self._alignment =  kwargs.get('alignment', TTkK.NONE)
        self._sMax,    self._sMin    = False, False
        self._sMaxVal, self._sMinVal = 0, 0
        self._maxw = kwargs.get('maxWidth',  0x10000)
        self._maxh = kwargs.get('maxHeight', 0x10000)
        self._maxw, self._maxh = kwargs.get('maxSize', (self._maxw, self._maxh))
        self._minw = kwargs.get('minWidth',  0x00000)
        self._minh = kwargs.get('minHeight', 0x00000)
        self._minw, self._minh = kwargs.get('minSize', (self._minw, self._minh))
        self._parent = None


    def minimumSize(self):
        return self.minimumWidth(), self.minimumHeight()
    def minDimension(self,o)-> int: return self._minh if o == TTkK.HORIZONTAL else self._minw
    def minimumHeight(self) -> int: return self._minh
    def minimumWidth(self)  -> int: return self._minw

    def maximumSize(self):
        return self.maximumWidth(), self.maximumHeight()
    def maxDimension(self,o)-> int: return self._maxh if o == TTkK.HORIZONTAL else self._maxw
    def maximumHeight(self) -> int: return self._maxh
    def maximumWidth(self)  -> int: return self._maxw

    @staticmethod
    def _calcSpanValue(value, pos, curpos, span):
        if pos==curpos:
            return value - (value//span) * (span-1)
        else:
            return value//span

    def minimumHeightSpan(self,pos) -> int:
        return TTkLayoutItem._calcSpanValue(self.minimumHeight(),pos,self._row,self._rowspan)
    def minimumWidthSpan(self,pos)  -> int:
        return TTkLayoutItem._calcSpanValue(self.minimumWidth(), pos,self._col,self._colspan)
    def maximumHeightSpan(self,pos) -> int:
        return TTkLayoutItem._calcSpanValue(self.maximumHeight(),pos,self._row,self._rowspan)
    def maximumWidthSpan(self,pos)  -> int:
        return TTkLayoutItem._calcSpanValue(self.maximumWidth(), pos,self._col,self._colspan)

    def offset(self):   return self._xOffset, self._yOffset
    def pos(self):      return self._x, self._y
    def size(self):     return self._w, self._h
    def geometry(self): return self._x, self._y, self._w, self._h

    def setOffset(self, x, y):
        '''setOffset'''
        self._xOffset = x
        self._yOffset = y

    def setGeometry(self, x, y, w, h):
        '''setGeometry'''
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def parent(self):
        '''parent'''
        return self._parent

    def setParent(self, parent):
        '''setParent'''
        self._parent = parent

    def layer(self):
        '''layer'''
        return self._layer

    def setLayer(self, layer):
        '''setLayer'''
        self._layer = layer
        self._z = (self._z & TTkLayoutItem.LAYERMASK) | layer

    def layoutItemType(self): return self._layoutItemType

class TTkLayout(TTkLayoutItem):
    '''
    | The :class:`TTkLayout` class is the base class of geometry managers. <br/>
    | It allows free placement of the widgets in the layout area. <br/>
    | Used mainly to have free range moving :class:`~TermTk.TTkWidgets.window.TTkWindow` because the widgets are not automatically rearranged after a layout event

    ::

        ╔════════════════════════════╗
        ║   pos(4,2)                 ║
        ║   ┌───────┐   pos(16,4)    ║
        ║   │Widget1│   ┌─────────┐  ║
        ║   │       │   │ Widget2 │  ║
        ║   │       │   └─────────┘  ║
        ║   │       │                ║
        ║   └───────┘                ║
        ║                            ║
        ╚════════════════════════════╝
    '''
    __slots__ = ('_items', '_zSortedItems')
    def __init__(self, *args, **kwargs):
        TTkLayoutItem.__init__(self, *args, **kwargs)
        self._items = []
        self._zSortedItems = []
        self._layoutItemType = TTkK.LayoutItem

    def children(self):
        return self._items

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if index < len(self._items):
            return self._items[index]
        return None

    def setParent(self, parent):
        if parent is None:
            self._parent = parent
        elif isinstance(parent, TTkLayoutItem):
            self._parent = parent
        else:
            self._parent = parent.widgetItem()
        for item in self._items:
            item.setParent(self)
            if item._layoutItemType == TTkK.WidgetItem:
                item.widget().setParent(self.parentWidget())

    def parentWidget(self):
        if self._parent is None: return None
        if self._parent._layoutItemType == TTkK.WidgetItem:
            return self._parent.widget()
        else:
            return self._parent.parentWidget()

    def iterWidgets(self, onlyVisible=True, recurse=True):
        for child in self._items:
            if child._layoutItemType == TTkK.WidgetItem:
                if onlyVisible and not child.widget().isVisible(): continue
                yield child.widget()
                if recurse and hasattr(cw:=child.widget(),'rootLayout'):
                    yield from cw.rootLayout().iterWidgets(onlyVisible, recurse)
            if child._layoutItemType == TTkK.LayoutItem and recurse:
                yield from child.iterWidgets(onlyVisible, recurse)

    def _zSortItems(self):
        self._zSortedItems = sorted(self._items, key=lambda item: item._z)

    @property
    def zSortedItems(self): return self._zSortedItems

    def replaceItem(self, item, index):
        self._items[index] = item
        self._zSortItems()
        self.update()
        item.setParent(self)
        if item._layoutItemType == TTkK.WidgetItem:
            item.widget().setParent(self.parentWidget())
        if self.parentWidget():
            self.parentWidget().update(repaint=True, updateLayout=True)

    def addItem(self, item):
        self.insertItems(len(self._items),[item])

    def addItems(self, items):
        self.insertItems(len(self._items),items)

    def insertItem(self, index, item):
        return self.insertItems(index,[item])

    def insertItems(self, index, items):
        for i,item in enumerate(items):
            if not issubclass(type(widget := item), TTkLayoutItem):
                if widget.parentWidget() and widget.parentWidget().layout():
                    widget.parentWidget().layout().removeWidget(self)
                item = widget.widgetItem()
                items[i]=item
        self._items[index:index] = items
        self._zSortItems()
        #self.update()
        for item in items:
            item.setParent(self)
            if item._layoutItemType == TTkK.WidgetItem:
                item.widget().setParent(self.parentWidget())
        if self.parentWidget() and self.parentWidget().isVisible():
            self.parentWidget().update(repaint=True, updateLayout=True)

    def addWidget(self, widget):
        ''' Add a widget to this Layout

        :param widget: the widget to be added
        :type widget: :class:`~TermTk.TTkWidgets`
        '''
        self.insertItems(len(self._items),[widget])

    def addWidgets(self, widgets):
        ''' Add a list of widgets to this Layout

        :param widgets: the widget to be added
        :type widgets: list of :class:`~TermTk.TTkWidgets`
        '''
        self.insertItems(len(self._items),widgets)

    def insertWidget(self, index, widget):
        '''insertWidget'''
        self.insertItems(index, [widget])

    def insertWidgets(self, index, widgets):
        '''insertWidgets'''
        self.insertItems(index, widgets)

    def removeItem(self, item):
        '''removeItem'''
        self.removeItems([item])

    def removeItems(self, items):
        '''removeItems'''
        for item in items:
            if item in self._items:
                self._items.remove(item)
                if item._layoutItemType == TTkK.WidgetItem:
                    item.widget().setParent(None)
                item.setParent(None)
        self._zSortItems()

    def removeWidget(self, widget):
        ''' Remove a widget from this Layout

        :param widget: the widget to be removed
        :type widget: :class:`~TermTk.TTkWidgets`
        '''
        self.removeWidgets([widget])

    def removeWidgets(self, widgets):
        ''' Remove a list of widget from this Layout

        :param widgets: the widget to be removed
        :type widgets: list of :class:`~TermTk.TTkWidgets`
        '''
        for item in reversed(self._items):
            if item._layoutItemType == TTkK.WidgetItem:
               if item.widget() in widgets:
                    self.removeItem(item)
            elif item._layoutItemType == TTkK.LayoutItem:
                item.removeWidgets(widgets)

    def _findBranchWidget(self, widget):
        for item in self._items:
            if item._layoutItemType == TTkK.LayoutItem:
                if item._findBranchWidget(widget) is not None:
                    return item
            else:
                if item.widget() == widget:
                    return item
        return None

    def raiseWidget(self, widget):
        '''raiseWidget'''
        item = self._findBranchWidget(widget)
        item._z = item._z if (maxz:=max(TTkLayoutItem.LAYERMASK & i._z for i in self._items))==(TTkLayoutItem.LAYERMASK & item._z)!=0 else item._layer|maxz+1
        if item._layoutItemType == TTkK.LayoutItem:
            item.raiseWidget(widget)
        self._zSortItems()

    def lowerWidget(self, widget):
        '''lowerWidget'''
        item = self._findBranchWidget(widget)
        for i in self._items: i._z+=1
        item._z = item._layer
        if item._layoutItemType == TTkK.LayoutItem:
            item.lowerWidget(widget)
        self._zSortItems()

    def setGeometry(self, x, y, w, h):
        '''setGeometry'''
        ax, ay, aw, ah = self.geometry()
        if ax==x and ay==y and aw==w and ah==h: return
        TTkLayoutItem.setGeometry(self, x, y, w, h)
        self.update(repaint=True, updateLayout=True)

    def fullWidgetAreaGeometry(self):
        if not self._items: return 0,0,0,0
        minx,miny,maxx,maxy = 0x10000,0x10000,-0x10000,-0x10000
        for item in self._items:
            x,y,w,h = item.geometry()
            minx = min(minx,x)
            miny = min(miny,y)
            maxx = max(maxx,x+w)
            maxy = max(maxy,y+h)
        return minx, miny, maxx-minx, maxy-miny

    def update(self, *args, **kwargs):
        ret = False
        for i in self._items:
            if i._layoutItemType == TTkK.WidgetItem and (_wid:=i._widget):
                ret = ret or _wid.update(*args, **kwargs)
            elif i._layoutItemType == TTkK.LayoutItem:
                ret = ret or i.update(*args, **kwargs)
        return ret

class TTkWidgetItem(TTkLayoutItem):
    __slots__ = ('_widget')
    def __init__(self, *args, **kwargs):
        TTkLayoutItem.__init__(self, *args, **kwargs)
        self._widget = kwargs.get('widget', None)
        self._layoutItemType = TTkK.WidgetItem

    def widget(self): return self._widget

    def isVisible(self): return self._widget.isVisible()

    def isEmpty(self): return self._widget is None

    def minimumSize(self)   -> int: return self._widget.minimumSize()
    def minDimension(self,o)-> int: return self._widget.minDimension(o)
    def minimumHeight(self) -> int: return self._widget.minimumHeight()
    def minimumWidth(self)  -> int: return self._widget.minimumWidth()
    def maximumSize(self)   -> int: return self._widget.maximumSize()
    def maxDimension(self,o)-> int: return self._widget.maxDimension(o)
    def maximumHeight(self) -> int: return self._widget.maximumHeight()
    def maximumWidth(self)  -> int: return self._widget.maximumWidth()

    def pos(self):      return self._widget.pos()
    def size(self):     return self._widget.size()
    def geometry(self): return self._widget.geometry()

    def setGeometry(self, x, y, w, h):
        self._widget.setGeometry(x, y, w, h)

    #def update(self, *args, **kwargs):
    #    self.widget().update(*args, **kwargs)
