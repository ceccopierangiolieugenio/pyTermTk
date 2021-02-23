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
    def __init__(self):
        self._x, self._y = 0, 0
        self._w, self._h = 0, 0
        self._sMax,    self._sMin    = False, False
        self._sMaxVal, self._sMinVal = 0, 0
        pass
    def minimumSize(self):
        return self.minimumWidth(), self.minimumHeight()
    def minimumHeight(self): return 0
    def minimumWidth(self):  return 0

    def maximumSize(self):
        return self.maximumWidth(), self.maximumHeight()
    def maximumHeight(self): return 0x80000000
    def maximumWidth(self):  return 0x80000000

    def geometry(self):
        return self._x, self._y, self._w, self._h

    def setGeometry(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h


class TTkLayout(TTkLayoutItem):
    __slots__ = ('_items', '_zSortedItems', '_parent')
    def __init__(self):
        TTkLayoutItem.__init__(self)
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

    def update(self):
        for i in self.children():
            if isinstance(i, TTkWidgetItem) and not i.isEmpty():
                i.widget().update()
                # TODO: Have a look at this:
                # i.getCanvas().top()
            elif isinstance(i, TTkLayout):
                i.update()

class TTkWidgetItem(TTkLayoutItem):
    slots = ('_widget','_z')
    def __init__(self, widget, z=0):
        TTkLayoutItem.__init__(self)
        self._widget = widget
        self.z = z

    def widget(self):
        return self._widget

    def isEmpty(self): return self._widget is None

    def minimumSize(self):   return self._widget.minimumSize()
    def minimumHeight(self): return self._widget.minimumHeight()
    def minimumWidth(self):  return self._widget.minimumWidth()
    def maximumSize(self):   return self._widget.maximumSize()
    def maximumHeight(self): return self._widget.maximumHeight()
    def maximumWidth(self):  return self._widget.maximumWidth()

    def geometry(self):      return self._widget.geometry()

    def setGeometry(self, x, y, w, h):
        self._widget.setGeometry(x, y, w, h)

    @property
    def z(self): return self._z
    @z.setter
    def z(self, z): self._z = z



class TTkHBoxLayout(TTkLayout):
    def __init__(self):
        TTkLayout.__init__(self)

    def minimumWidth(self):
        ''' process the widgets and get the min size '''
        minw = 0
        for item in self.children():
            w1  = item.minimumWidth()
            minw += w1
        return minw

    def minimumHeight(self):
        ''' process the widgets and get the min size '''
        minh = TTkLayout.minimumHeight(self)
        for item in self.children():
            h1  = item.minimumHeight()
            if h1 > minh : minh = h1
        return minh

    def maximumWidth(self):
        ''' process the widgets and get the min size '''
        maxw = 0
        for item in self.children():
            w1 = item.maximumWidth()
            maxw += w1
        return maxw

    def maximumHeight(self):
        ''' process the widgets and get the min size '''
        maxh = TTkLayout.maximumHeight(self)
        for item in self.children():
            h1  = item.maximumHeight()
            if h1 < maxh : maxh = h1
        return maxh

    def update(self):
        x, y, w, h = self.geometry()
        numWidgets = self.count()
        leftWidgets = numWidgets
        freeWidth = w
        newx, newy = x, y
        # Loop to check the resizable space
        for item in self.children():
            item._sMax = False
            item._sMin = False
        iterate = True

        # Copy and Sort list of items based on the minsize
        sortedItems = sorted(self.children(), key=lambda item: item.minimumWidth())

        while iterate and leftWidgets > 0:
            iterate = False
            for item in sortedItems:
                if item._sMax or item._sMin: continue
                sliceSize = freeWidth//leftWidgets
                maxs = item.maximumWidth()
                mins = item.minimumWidth()
                if sliceSize >= maxs:
                    freeWidth -= maxs
                    iterate = True
                    item._sMax = True
                    item._sMaxVal = maxs
                    leftWidgets -= 1
                elif sliceSize < mins:
                    freeWidth -= mins
                    leftWidgets -= 1
                    iterate = True
                    item._sMin = True
                    item._sMinVal = mins

        # loop and set the geometry of any item
        for item in self.children():
            if item._sMax:
                item.setGeometry(newx, newy, item._sMaxVal, h)
                newx += item._sMaxVal
            elif item._sMin:
                item.setGeometry(newx, newy, item._sMinVal, h)
                newx += item._sMinVal
            else:
                sliceSize = freeWidth//leftWidgets
                item.setGeometry(newx, newy, sliceSize, h)
                newx += sliceSize
                freeWidth -= sliceSize
                leftWidgets -= 1
            if isinstance(item, TTkWidgetItem) and not item.isEmpty():
                item.widget().update()
            elif isinstance(item, TTkLayout):
                item.update()


class TTkVBoxLayout(TTkLayout):
    def __init__(self):
        TTkLayout.__init__(self)

    def minimumWidth(self):
        ''' process the widgets and get the min size '''
        minw = TTkLayout.minimumWidth(self)
        for item in self.children():
            w1  = item.minimumWidth()
            if w1 > minw : minw = w1
        return minw

    def minimumHeight(self):
        ''' process the widgets and get the min size '''
        minh = 0
        for item in self.children():
            h1  = item.minimumHeight()
            minh += h1
        return minh

    def maximumWidth(self):
        ''' process the widgets and get the min size '''
        maxw = TTkLayout.maximumWidth(self)
        for item in self.children():
            w1  = item.maximumWidth()
            if w1 < maxw : maxw = w1
        return maxw

    def maximumHeight(self):
        ''' process the widgets and get the min size '''
        maxh = 0
        for item in self.children():
            h1 = item.maximumHeight()
            maxh += h1
        return maxh

    def update(self):
        x, y, w, h = self.geometry()
        numWidgets = self.count()
        leftWidgets = numWidgets
        freeHeight = h
        newx, newy = x, y
        # Loop to check the resizable space
        for item in self.children():
            item._sMax = False
            item._sMin = False
        iterate = True

        # Copy and Sort list of items based on the minsize
        sortedItems = sorted(self.children(), key=lambda item: item.minimumHeight())

        while iterate and leftWidgets > 0:
            iterate = False
            for item in sortedItems:
                if item._sMax or item._sMin: continue
                sliceSize = freeHeight//leftWidgets
                maxs = item.maximumHeight()
                mins = item.minimumHeight()
                if sliceSize >= maxs:
                    freeHeight -= maxs
                    iterate = True
                    item._sMax = True
                    item._sMaxVal = maxs
                    leftWidgets -= 1
                elif sliceSize < mins:
                    freeHeight -= mins
                    leftWidgets -= 1
                    iterate = True
                    item._sMin = True
                    item._sMinVal = mins

        # loop and set the geometry of any item
        for item in self.children():
            if item._sMax:
                item.setGeometry(newx, newy, w, item._sMaxVal)
                newy += item._sMaxVal
            elif item._sMin:
                item.setGeometry(newx, newy, w, item._sMinVal)
                newy += item._sMinVal
            else:
                sliceSize = freeHeight//leftWidgets
                item.setGeometry(newx, newy, w, sliceSize)
                newy += sliceSize
                freeHeight -= sliceSize
                leftWidgets -= 1
            if isinstance(item, TTkWidgetItem) and not item.isEmpty():
                item.widget().update()
            elif isinstance(item, TTkLayout):
                item.update()
