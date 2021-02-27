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
    Layout System
'''

from TermTk.TTkCore.log import TTkLog

class TTkLayoutItem:
    __slots__ = ('_x', '_y', '_w', '_h', '_sMax', '_sMaxVal', '_sMin', '_sMinVal')
    def __init__(self, *args, **kwargs):
        self._x, self._y = 0, 0
        self._w, self._h = 0, 0
        self._sMax,    self._sMin    = False, False
        self._sMaxVal, self._sMinVal = 0, 0
        pass
    def minimumSize(self):
        return self.minimumWidth(), self.minimumHeight()
    def minimumHeight(self) -> int: return 0
    def minimumWidth(self)  -> int: return 0

    def maximumSize(self):
        return self.maximumWidth(), self.maximumHeight()
    def maximumHeight(self) -> int: return 0x80000000
    def maximumWidth(self)  -> int:  return 0x80000000

    def geometry(self):
        return self._x, self._y, self._w, self._h

    def setGeometry(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h


class TTkLayout(TTkLayoutItem):
    __slots__ = ('_items', '_zSortedItems', '_parent')
    def __init__(self, *args, **kwargs):
        TTkLayoutItem.__init__(self, args, kwargs)
        self._items = []
        self._zSortedItems = []
        self._parent = None
        pass

    def children(self):
        return self._items

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if index < len(self._items):
            return self._items[index]
        return 0

    def setParent(self, parent):
        self._parent = parent

    def parentWidget(self):
        return self._parent

    def _zSortItems(self):
        self._zSortedItems = sorted(self._items, key=lambda item: item.z)

    @property
    def zSortedItems(self): return self._zSortedItems

    def addItem(self, item):
        self._items.append(item)
        self._zSortItems()

    def addWidget(self, widget):
        if widget.parentWidget() is not None:
            widget.parentWidget().removeWidget(self)
        self.addItem(TTkWidgetItem(widget))

    def removeWidget(self, widget):
        for i in self._items:
            if i.widget() == widget:
                self._items.remove(i)
                return
        self._zSortItems()

    def raiseWidget(self, widget):
        maxz = 0
        item = None
        for i in self._items:
            if i.widget() == widget:
                item = i
            elif i.z >= maxz:
                maxz=i.z+1
        item.z = maxz
        self._zSortItems()


    def lowerWidget(self, widget):
        minz = 0
        item = None
        for i in self._items:
            if i.widget() == widget:
                item = i
            elif i.z <= minz:
                minz=i.z-1
        item.z = minz
        self._zSortItems()

    def setGeometry(self, x, y, w, h):
        ax, ay, aw, ah = self.geometry()
        if ax==x and ay==y and aw==w and ah==h: return
        TTkLayoutItem.setGeometry(self, x, y, w, h)
        self.update()

    def update(self):
        ret = False
        for i in self.children():
            if isinstance(i, TTkWidgetItem) and not i.isEmpty():
                ret = ret or i.widget().update()
                # TODO: Have a look at this:
                # i.getCanvas().top()
            elif isinstance(i, TTkLayout):
                ret= ret or i.update()
        return ret

class TTkWidgetItem(TTkLayoutItem):
    slots = ('_widget','_z')
    def __init__(self, widget, z=0):
        TTkLayoutItem.__init__(self)
        self._widget = widget
        self.z = z

    def widget(self):
        return self._widget

    def isVisible(self): return self._widget.isVisible()

    def isEmpty(self): return self._widget is None

    def minimumSize(self)  -> int: return self._widget.minimumSize()
    def minimumHeight(self)-> int: return self._widget.minimumHeight()
    def minimumWidth(self) -> int: return self._widget.minimumWidth()
    def maximumSize(self)  -> int: return self._widget.maximumSize()
    def maximumHeight(self)-> int: return self._widget.maximumHeight()
    def maximumWidth(self) -> int: return self._widget.maximumWidth()

    def geometry(self):      return self._widget.geometry()

    def setGeometry(self, x, y, w, h):
        self._widget.setGeometry(x, y, w, h)

    @property
    def z(self): return self._z
    @z.setter
    def z(self, z): self._z = z
