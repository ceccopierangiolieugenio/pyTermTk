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

'''
### Layout
[Tutorial](https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/002-layout.md)
'''

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK

class TTkLayoutItem:
    __slots__ = (
        '_x', '_y', '_z', '_w', '_h',
        '_row','_col',
        '_sMax', '_sMaxVal',
        '_sMin', '_sMinVal',
        '_alignment',
        '_layoutItemType')
    def __init__(self, *args, **kwargs):
        self._x, self._y = 0, 0
        self._z = kwargs.get('z',0)
        self._row = kwargs.get('row', 0)
        self._col = kwargs.get('col', 0)
        self._layoutItemType = kwargs.get('layoutItemType', TTkK.NONE)
        self._alignment =  kwargs.get('alignment', TTkK.NONE)
        self._w, self._h = 0, 0
        self._sMax,    self._sMin    = False, False
        self._sMaxVal, self._sMinVal = 0, 0

    def minimumSize(self):
        return self.minimumWidth(), self.minimumHeight()
    def minDimension(self,o)-> int: return 0
    def minimumHeight(self) -> int: return 0
    def minimumWidth(self)  -> int: return 0

    def maximumSize(self):
        return self.maximumWidth(), self.maximumHeight()
    def maxDimension(self,o)-> int: return 0x1000
    def maximumHeight(self) -> int: return 0x10000
    def maximumWidth(self)  -> int: return 0x10000

    def geometry(self):
        return self._x, self._y, self._w, self._h

    def setGeometry(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    @property
    def z(self): return self._z
    @z.setter
    def z(self, z): self._z = z

    @property
    def layoutItemType(self): return self._layoutItemType
    @layoutItemType.setter
    def layoutItemType(self, t): self._layoutItemType = t


class TTkLayout(TTkLayoutItem):
    __slots__ = ('_items', '_zSortedItems', '_parent')
    def __init__(self, *args, **kwargs):
        TTkLayoutItem.__init__(self, args, kwargs)
        self._items = []
        self._zSortedItems = []
        self._parent = None
        self.layoutItemType = TTkK.LayoutItem

    def children(self):
        return self._items

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if index < len(self._items):
            return self._items[index]
        return 0

    def setParent(self, parent):
        if isinstance(parent, TTkLayoutItem):
            self._parent = parent
        else:
            self._parent = TTkWidgetItem(widget=parent)
        for item in self._items:
            if item.layoutItemType == TTkK.LayoutItem:
                item.setParent(self)
            else:
                item.widget().setParent(self.parentWidget())

    def parentWidget(self):
        if self._parent is None: return None
        if self._parent.layoutItemType == TTkK.WidgetItem:
            return self._parent.widget()
        else:
            return self._parent.parentWidget()

    def _zSortItems(self):
        self._zSortedItems = sorted(self._items, key=lambda item: item.z)

    @property
    def zSortedItems(self): return self._zSortedItems

    def replaceItem(self, item, index):
        self._items[index] = item
        self._zSortItems()
        self.update()
        if item.layoutItemType == TTkK.LayoutItem:
            item.setParent(self)
        else:
            item.widget().setParent(self.parentWidget())
        if self.parentWidget():
            self.parentWidget().update(repaint=True, updateLayout=True)

    def addItem(self, item):
        self._items.append(item)
        self._zSortItems()
        self.update()
        if item.layoutItemType == TTkK.LayoutItem:
            item.setParent(self)
        else:
            item.widget().setParent(self.parentWidget())
        if self.parentWidget():
            self.parentWidget().update(repaint=True, updateLayout=True)

    def addWidget(self, widget):
        if widget.parentWidget() is not None:
            widget.parentWidget().removeWidget(self)
        self.addItem(TTkWidgetItem(widget=widget))

    def removeItem(self, item):
        if item in self._items:
            self._items.remove(item)
        self._zSortItems()

    def removeWidget(self, widget):
        for item in self._items:
            if item.layoutItemType == TTkK.WidgetItem and \
               item.widget() == widget:
                self.removeItem(item)

    def findBranchWidget(self, widget):
        for item in self._items:
            if item.layoutItemType == TTkK.LayoutItem:
                if item.findBranchWidget(widget) is not None:
                    return item
            else:
                if item.widget() == widget:
                    return item
        return None

    def raiseWidget(self, widget):
        maxz = 0
        item = self.findBranchWidget(widget)
        for i in self._items:
            maxz=max(i.z+1,maxz)
        item.z = maxz
        if item.layoutItemType == TTkK.LayoutItem:
            item.raiseWidget(widget)
        self._zSortItems()

    def lowerWidget(self, widget):
        minz = 0
        item = self.findBranchWidget(widget)
        for i in self._items:
            minz=min(i.z-1,minz)
        item.z = minz
        if item.layoutItemType == TTkK.LayoutItem:
            item.lowerWidget(widget)
        self._zSortItems()

    def setGeometry(self, x, y, w, h):
        ax, ay, aw, ah = self.geometry()
        if ax==x and ay==y and aw==w and ah==h: return
        TTkLayoutItem.setGeometry(self, x, y, w, h)
        self.update(repaint=True, updateLayout=True)

    def groupMoveTo(self, x, y):
        ox,oy,_,_ = self.fullWidgetAreaGeometry()
        dx = x-ox
        dy = y-oy
        for item in self._items:
            x,y,w,h = item.geometry()
            item.setGeometry(x+dx,y+dy,w,h)

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
        for i in self.children():
            if i.layoutItemType == TTkK.WidgetItem and not i.isEmpty():
                ret = ret or i.widget().update(*args, **kwargs)
                # TODO: Have a look at this:
                # i.getCanvas().top()
            elif i.layoutItemType == TTkK.LayoutItem:
                ret= ret or i.update(*args, **kwargs)
        return ret

class TTkWidgetItem(TTkLayoutItem):
    slots = ('_widget')
    def __init__(self, *args, **kwargs):
        TTkLayoutItem.__init__(self, *args, **kwargs)
        self._widget = kwargs.get('widget', None)
        self.layoutItemType = TTkK.WidgetItem

    def widget(self):
        return self._widget

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

    def geometry(self):      return self._widget.geometry()

    def setGeometry(self, x, y, w, h):
        self._widget.setGeometry(x, y, w, h)

    #def update(self, *args, **kwargs):
    #    self.widget().update(*args, **kwargs)
