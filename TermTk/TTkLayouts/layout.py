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



#class TTkHBoxLayout(TTkLayout):
#    def __init__(self):
#        TTkLayout.__init__(self)
#
#    def minimumWidth(self) -> int:
#        ''' process the widgets and get the min size '''
#        minw = 0
#        for item in self.children():
#            w1  = item.minimumWidth()
#            minw += w1
#        return minw
#
#    def minimumHeight(self) -> int:
#        ''' process the widgets and get the min size '''
#        minh = TTkLayout.minimumHeight(self)
#        for item in self.children():
#            h1  = item.minimumHeight()
#            if h1 > minh : minh = h1
#        return minh
#
#    def maximumWidth(self) -> int:
#        ''' process the widgets and get the min size '''
#        maxw = 0
#        for item in self.children():
#            w1 = item.maximumWidth()
#            maxw += w1
#        return maxw
#
#    def maximumHeight(self) -> int:
#        ''' process the widgets and get the min size '''
#        maxh = TTkLayout.maximumHeight(self)
#        for item in self.children():
#            h1  = item.maximumHeight()
#            if h1 < maxh : maxh = h1
#        return maxh
#
#    def update(self):
#        x, y, w, h = self.geometry()
#        numWidgets = self.count()
#        leftWidgets = numWidgets
#        freeWidth = w
#        newx, newy = x, y
#        # Loop to check the resizable space
#        for item in self.children():
#            item._sMax = False
#            item._sMin = False
#        iterate = True
#
#        # Copy and Sort list of items based on the minsize
#        sortedItems = sorted(self.children(), key=lambda item: item.minimumWidth())
#
#        while iterate and leftWidgets > 0:
#            iterate = False
#            for item in sortedItems:
#                if item._sMax or item._sMin: continue
#                sliceSize = freeWidth//leftWidgets
#                maxs = item.maximumWidth()
#                mins = item.minimumWidth()
#                if sliceSize >= maxs:
#                    freeWidth -= maxs
#                    iterate = True
#                    item._sMax = True
#                    item._sMaxVal = maxs
#                    leftWidgets -= 1
#                elif sliceSize < mins:
#                    freeWidth -= mins
#                    leftWidgets -= 1
#                    iterate = True
#                    item._sMin = True
#                    item._sMinVal = mins
#
#        # loop and set the geometry of any item
#        for item in self.children():
#            if item._sMax:
#                item.setGeometry(newx, newy, item._sMaxVal, h)
#                newx += item._sMaxVal
#            elif item._sMin:
#                item.setGeometry(newx, newy, item._sMinVal, h)
#                newx += item._sMinVal
#            else:
#                sliceSize = freeWidth//leftWidgets
#                item.setGeometry(newx, newy, sliceSize, h)
#                newx += sliceSize
#                freeWidth -= sliceSize
#                leftWidgets -= 1
#            if isinstance(item, TTkWidgetItem) and not item.isEmpty():
#                item.widget().update()
#            elif isinstance(item, TTkLayout):
#                item.update()
#
#
#class TTkVBoxLayout(TTkLayout):
#    def __init__(self):
#        TTkLayout.__init__(self)
#
#    def minimumWidth(self) -> int:
#        ''' process the widgets and get the min size '''
#        minw = TTkLayout.minimumWidth(self)
#        for item in self.children():
#            w1  = item.minimumWidth()
#            if w1 > minw : minw = w1
#        return minw
#
#    def minimumHeight(self) -> int:
#        ''' process the widgets and get the min size '''
#        minh = 0
#        for item in self.children():
#            h1  = item.minimumHeight()
#            minh += h1
#        return minh
#
#    def maximumWidth(self) -> int:
#        ''' process the widgets and get the min size '''
#        maxw = TTkLayout.maximumWidth(self)
#        for item in self.children():
#            w1  = item.maximumWidth()
#            if w1 < maxw : maxw = w1
#        return maxw
#
#    def maximumHeight(self) -> int:
#        ''' process the widgets and get the min size '''
#        maxh = 0
#        for item in self.children():
#            h1 = item.maximumHeight()
#            maxh += h1
#        return maxh
#
#    def update(self):
#        x, y, w, h = self.geometry()
#        numWidgets = self.count()
#        leftWidgets = numWidgets
#        freeHeight = h
#        newx, newy = x, y
#        # Loop to check the resizable space
#        for item in self.children():
#            item._sMax = False
#            item._sMin = False
#        iterate = True
#
#        # Copy and Sort list of items based on the minsize
#        sortedItems = sorted(self.children(), key=lambda item: item.minimumHeight())
#
#        while iterate and leftWidgets > 0:
#            iterate = False
#            for item in sortedItems:
#                if item._sMax or item._sMin: continue
#                sliceSize = freeHeight//leftWidgets
#                maxs = item.maximumHeight()
#                mins = item.minimumHeight()
#                if sliceSize >= maxs:
#                    freeHeight -= maxs
#                    iterate = True
#                    item._sMax = True
#                    item._sMaxVal = maxs
#                    leftWidgets -= 1
#                elif sliceSize < mins:
#                    freeHeight -= mins
#                    leftWidgets -= 1
#                    iterate = True
#                    item._sMin = True
#                    item._sMinVal = mins
#
#        # loop and set the geometry of any item
#        for item in self.children():
#            if item._sMax:
#                item.setGeometry(newx, newy, w, item._sMaxVal)
#                newy += item._sMaxVal
#            elif item._sMin:
#                item.setGeometry(newx, newy, w, item._sMinVal)
#                newy += item._sMinVal
#            else:
#                sliceSize = freeHeight//leftWidgets
#                item.setGeometry(newx, newy, w, sliceSize)
#                newy += sliceSize
#                freeHeight -= sliceSize
#                leftWidgets -= 1
#            if isinstance(item, TTkWidgetItem) and not item.isEmpty():
#                item.widget().update()
#            elif isinstance(item, TTkLayout):
#                item.update()
#
#class TTkGridWidgetItem(TTkWidgetItem):
#    __slots__ = ('_row','_col')
#    def __init__(self, *args, **kwargs):
#        TTkWidgetItem.__init__(self, args[0])
#        self._row = kwargs.get('row')
#        self._col = kwargs.get('col')
#
#class TTkGridLayout(TTkLayout):
#    __slots__ = ('_gridItems')
#    def __init__(self):
#        TTkLayout.__init__(self)
#        self._gridItems = [[]]
#
#    # addWidget(self, widget, row, col)
#    def addWidget(self, *args, **kwargs):
#        if len(args) == 3:
#            row = args[1]
#            col = args[2]
#        else:
#            # Append The widget at the end
#            row = 0
#            col = len(self._gridItems[0])
#        #retrieve the max col/rows to reshape the grid
#        maxrow = row + 1
#        maxcol = col + 1
#        for item in self.children():
#            if maxrow < item._row: maxrow = item._row + 1
#            if maxcol < item._col: maxcol = item._col + 1
#        # reshape the gridItems
#        if len(self._gridItems) > maxrow:
#            self._gridItems = self._gridItems[:maxrow]
#        if len(self._gridItems) < maxrow:
#            self._gridItems += [[]]*(maxrow-len(self._gridItems))
#        for gridRow in range(len(self._gridItems)):
#            if len(self._gridItems[gridRow]) > maxcol:
#                self._gridItems[gridRow] = self._gridItems[gridRow][:maxcol]
#            if len(self._gridItems[gridRow]) < maxcol:
#                self._gridItems[gridRow] += [None]*(maxcol-len(self._gridItems[gridRow]))
#        if self._gridItems[row][col] is not None:
#            # TODO: Handle the LayoutItem
#            self.removeWidget(self._gridItems[row][col])
#
#        item = TTkGridWidgetItem(args[0], row=row, col=col)
#        self._gridItems[row][col] = item
#        self.addItem(item)
#
#    def itemAtPosition(self, row: int, col: int):
#        if row >= len(self._gridItems) or \
#           col >= len(self._gridItems[0]):
#            return None
#        return self._gridItems[row][col]
#
#    def minimumColWidth(self, gridCol: int) -> int:
#        colw = 0
#        for gridRow in range(len(self._gridItems)):
#            item = self._gridItems[gridRow][gridCol]
#            if item is not None:
#                w = item.minimumWidth()
#                if colw < w:
#                    colw = w
#        return colw
#
#    def minimumRowHeight(self, gridRow: int):
#        rowh = 0
#        for item in self._gridItems[gridRow]:
#            if item is not None:
#                h = item.minimumHeight()
#                if rowh < h:
#                    rowh = h
#        return rowh
#
#    def maximumColWidth(self, gridCol: int) -> int:
#        colw = 0x10000
#        for gridRow in range(len(self._gridItems)):
#            item = self._gridItems[gridRow][gridCol]
#            if item is not None:
#                w = item.maximumWidth()
#                if colw > w:
#                    colw = w
#        return colw
#
#    def maximumRowHeight(self, gridRow: int):
#        rowh = 0x10000
#        for item in self._gridItems[gridRow]:
#            if item is not None:
#                h = item.maximumHeight()
#                if rowh > h:
#                    rowh = h
#        return rowh
#
#    def minimumWidth(self) -> int:
#        ''' process the widgets and get the min size '''
#        minw = 0
#        for gridCol in range(len(self._gridItems[0])):
#            minw += self.minimumColWidth(gridCol)
#        return minw
#
#    def minimumHeight(self) -> int:
#        ''' process the widgets and get the min size '''
#        minh = 0
#        for gridRow in range(len(self._gridItems)):
#            minh += self.minimumRowHeight(gridRow)
#        return minh
#
#    def maximumWidth(self) -> int:
#        ''' process the widgets and get the min size '''
#        maxw = 0
#        for gridCol in range(len(self._gridItems[0])):
#            maxw += self.maximumColWidth(gridCol)
#        return maxw
#
#    def maximumHeight(self) -> int:
#        ''' process the widgets and get the min size '''
#        maxh = 0
#        for gridRow in range(len(self._gridItems)):
#            maxh += self.maximumRowHeight(gridRow)
#        return maxh
#
#
#    def update(self):
#        x, y, w, h = self.geometry()
#        newx, newy = x, y
#        TTkLog.debug(f"1) x:{x} y:{y} w:{w} h:{h}")
#
#        # Sorted List of minimum heights
#        #                  0 1                     2                     3
#        sortedHeights = [ [i,self.minimumRowHeight(i),self.maximumRowHeight(i),-1] for i in range(len(self._gridItems)) ]
#        sortedWidths  = [ [i,self.minimumColWidth(i), self.maximumColWidth(i), -1] for i in range(len(self._gridItems[0])) ]
#        sortedHeights = sorted(sortedHeights, key=lambda h: h[1])
#        sortedWidths  = sorted(sortedWidths,  key=lambda w: w[1])
#
#        minWidth = 0
#        minHeight = 0
#        for i in sortedWidths:  minWidth  += i[1]
#        for i in sortedHeights: minHeight += i[1]
#
#        if h < minHeight: h = minHeight
#        if w < minWidth:  w = minWidth
#        TTkLog.debug(f"2) x:{x} y:{y} w:{w} h:{h} - {self._gridItems}")
#
#        def parseSizes(sizes, space, out):
#            iterate = True
#            freeSpace = space
#            leftSlots = len(sizes)+1
#            while iterate and leftSlots > 0:
#                iterate = False
#                for item in sizes:
#                    if item[3] != -1: continue
#                    if freeSpace < 0: freeSpace=0
#                    sliceSize = freeSpace//leftSlots
#                    mins = item[1]
#                    maxs = item[2]
#                    if sliceSize >= maxs:
#                        iterate = True
#                        freeSpace -= maxs
#                        leftSlots -= 1
#                        item[3] = maxs
#                    elif sliceSize < mins:
#                        iterate = True
#                        freeSpace -= mins
#                        leftSlots -= 1
#                        item[3] = mins
#            # Push the sizes
#            TTkLog.debug(f"2) sizes:{sizes}, space:{space}, fs:{freeSpace}, ls:{leftSlots}")
#            for item in sizes:
#                out[item[0]] = [0,item[3]]
#                if item[3] != -1:
#                    sliceSize = freeSpace//leftSlots
#                    out[item[0]] = [0,sliceSize]
#                    freeSpace -= sliceSize
#                    leftSlots -= 1
#
#        vertSizes = [None]*len(sortedHeights)
#        horSizes  = [None]*len(sortedWidths)
#        parseSizes(sortedHeights,h, vertSizes)
#        parseSizes(sortedWidths, w, horSizes)
#
#        for i in horSizes:
#            i[0] = newx
#            newx += i[1]
#        for i in vertSizes:
#            i[0] = newy
#            newy += i[1]
#
#        # loop and set the geometry of any item
#        for item in self.children():
#            col = item._col
#            row = item._row
#            item.setGeometry(horSizes[col][0], vertSizes[row][0], 10, 3)
#            if isinstance(item, TTkWidgetItem) and not item.isEmpty():
#                item.widget().update()
#            elif isinstance(item, TTkLayout):
#                item.update()
#