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
### Grid Layout
[Tutorial](https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/002-layout.md)

The grid layout allows an automatic place all the widgets in a grid
the empty rows/cols are resized to the "columnMinHeight,columnMinWidth" parameters

    TTkGridLayout        ┌┐ columnMinWidth
     ╔═════════╤═════════╤╤═════════╗
     ║ Widget1 │ Widget2 ││ Widget3 ║
     ║ (0,0)   │ (0,1)   ││ (0,3)   ║
     ╟─────────┼─────────┼┼─────────╢ ┐ columnMinHeight
     ╟─────────┼─────────┼┼─────────╢ ┘
     ║ Widget4 │         ││         ║
     ║ (2,0)   │         ││         ║
     ╟─────────┼─────────┼┼─────────╢
     ║         │         ││ Widget5 ║
     ║         │         ││ (3,3)   ║
     ╚═════════╧═════════╧╧═════════╝
'''

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkLayouts.layout import TTkLayout, TTkWidgetItem

class TTkGridLayout(TTkLayout):
    __slots__ = ('_gridItems','_columnMinWidth','_columnMinHeight')
    def __init__(self, *args, **kwargs):
        '''
        TTkGridLayout constructor

        Args:
            columnMinWidth (int, optional, default=0): the minimum width of the column
            columnMinHeight (int, optional, default=0): the minimum height of the column
        '''
        TTkLayout.__init__(self, *args, **kwargs)
        self._gridItems = [[]]
        self._columnMinWidth = kwargs.get('columnMinWidth',0)
        self._columnMinHeight = kwargs.get('columnMinHeight',0)

    def _gridUsedsize(self):
        rows = 1
        cols = 0
        for gridRow in range(len(self._gridItems)):
            if rows  < gridRow:
                rows = gridRow
            for gridCol in range(len(self._gridItems[0])):
                if self._gridItems[gridRow][gridCol] is not None:
                    if cols < gridCol:
                        cols = gridCol
        return (rows+1, cols+1)

    def _reshapeGrid(self, size):
        rows = size[0]
        cols = size[1]

        # remove extra rows
        if   rows < len(self._gridItems):
            self._gridItems = self._gridItems[:rows]
        elif rows > len(self._gridItems):
            self._gridItems += [None]*(rows-len(self._gridItems))
        # remove extra cols
        for gridRow in range(len(self._gridItems)):
            if self._gridItems[gridRow] is None:
                self._gridItems[gridRow] = [None]*(cols)
                continue
            sizeRow = len(self._gridItems[gridRow])
            if cols < sizeRow:
                self._gridItems[gridRow] = self._gridItems[gridRow][:cols]
            elif cols > sizeRow:
                self._gridItems[gridRow] += [None]*(cols-sizeRow)

    # addWidget(self, widget, row, col)
    def addWidget(self, *args, **kwargs):
        widget = args[0]
        self.removeWidget(widget)
        item = TTkWidgetItem(widget=widget)
        if len(args) == 3:
            TTkGridLayout.addItem(self, item, args[1], args[2])
        else:
            TTkGridLayout.addItem(self, item)
        widget.update()

    def replaceItem(self, item, index): pass

    def addItem(self, *args, **kwargs):
        item = args[0]
        self.removeItem(item)
        if len(args) == 3:
            row = args[1]
            col = args[2]
        else:
            # Append The widget at the end
            row = 0
            col = len(self._gridItems[0])

        #retrieve the max col/rows to reshape the grid
        maxrow = row
        maxcol = col
        for child in self.children():
            if maxrow < child._row: maxrow = child._row
            if maxcol < child._col: maxcol = child._col
        # reshape the gridItems
        maxrow += 1
        maxcol += 1

        # TODO: This is RUBBISH!!!
        self._reshapeGrid(size=(maxrow,maxcol))
        if self._gridItems[row][col] is not None:
            # TODO: Handle the LayoutItem
            self.removeItem(self._gridItems[row][col])
        self._reshapeGrid(size=(maxrow,maxcol))

        item._row = row
        item._col = col
        self._gridItems[row][col] = item
        TTkLayout.addItem(self, item)

    def removeItem(self, item):
        TTkLayout.removeItem(self, item)
        for gridRow in range(len(self._gridItems)):
            for gridCol in range(len(self._gridItems[0])):
                if self._gridItems[gridRow][gridCol] == item:
                    self._gridItems[gridRow][gridCol] = None
        self._reshapeGrid(self._gridUsedsize())

    def removeWidget(self, widget):
        TTkLayout.removeWidget(self, widget)
        for gridRow in range(len(self._gridItems)):
            for gridCol in range(len(self._gridItems[0])):
                if self._gridItems[gridRow][gridCol] is not None and \
                   self._gridItems[gridRow][gridCol].layoutItemType == TTkK.WidgetItem and \
                   self._gridItems[gridRow][gridCol].widget() == widget:
                    self._gridItems[gridRow][gridCol] = None
        self._reshapeGrid(self._gridUsedsize())

    def itemAtPosition(self, row: int, col: int):
        if row >= len(self._gridItems) or \
           col >= len(self._gridItems[0]):
            return None
        return self._gridItems[row][col]

    def minimumColWidth(self, gridCol: int) -> int:
        colw = 0
        anyItem = False
        for gridRow in range(len(self._gridItems)):
            item = self._gridItems[gridRow][gridCol]
            if item is not None and \
               ( item.layoutItemType == TTkK.LayoutItem or item.isVisible() ):
                    anyItem = True
                    w = item.minimumWidth()
                    if colw < w:
                        colw = w
        if not anyItem:
            return self._columnMinWidth
        return colw

    def minimumRowHeight(self, gridRow: int):
        rowh = 0
        anyItem = False
        for item in self._gridItems[gridRow]:
            if item is not None and \
               ( item.layoutItemType == TTkK.LayoutItem or item.isVisible() ):
                    anyItem = True
                    h = item.minimumHeight()
                    if rowh < h:
                        rowh = h
        if not anyItem:
            return self._columnMinHeight
        return rowh

    def maximumColWidth(self, gridCol: int) -> int:
        colw = 0x10000
        anyItem = False
        for gridRow in range(len(self._gridItems)):
            item = self._gridItems[gridRow][gridCol]
            if item is not None and \
               ( item.layoutItemType == TTkK.LayoutItem or item.isVisible() ):
                    anyItem = True
                    w = item.maximumWidth()
                    if colw > w:
                        colw = w
        if not anyItem:
            return self._columnMinWidth
        return colw

    def maximumRowHeight(self, gridRow: int):
        rowh = 0x10000
        anyItem = False
        for item in self._gridItems[gridRow]:
            if item is not None and \
               ( item.layoutItemType == TTkK.LayoutItem or item.isVisible() ):
                    anyItem = True
                    h = item.maximumHeight()
                    if rowh > h:
                        rowh = h
        if not anyItem:
            return self._columnMinHeight
        return rowh

    def minimumWidth(self) -> int:
        ''' process the widgets and get the min size '''
        minw = 0
        for gridCol in range(len(self._gridItems[0])):
            minw += self.minimumColWidth(gridCol)
        return minw

    def minimumHeight(self) -> int:
        ''' process the widgets and get the min size '''
        minh = 0
        for gridRow in range(len(self._gridItems)):
            minh += self.minimumRowHeight(gridRow)
        return minh

    def maximumWidth(self) -> int:
        ''' process the widgets and get the min size '''
        if not self._gridItems[0]:
            return 0x1000
        maxw = 0
        for gridCol in range(len(self._gridItems[0])):
            maxw += self.maximumColWidth(gridCol)
        return maxw

    def maximumHeight(self) -> int:
        ''' process the widgets and get the min size '''
        if not self._gridItems[0]:
            return 0x1000
        maxh = 0
        for gridRow in range(len(self._gridItems)):
            maxh += self.maximumRowHeight(gridRow)
        return maxh


    def update(self, *args, **kwargs):
        x, y, w, h = self.geometry()
        newx, newy = x, y

        # Sorted List of minimum heights
        #                    min                        max                       val
        #  content IDs     0 1                          2                         3
        sortedHeights = [ [i, self.minimumRowHeight(i), self.maximumRowHeight(i), -1] for i in range(len(self._gridItems)) ]
        sortedWidths  = [ [i, self.minimumColWidth(i),  self.maximumColWidth(i),  -1] for i in range(len(self._gridItems[0])) ]
        sortedHeights = sorted(sortedHeights, key=lambda h: h[1])
        sortedWidths  = sorted(sortedWidths,  key=lambda w: w[1])

        minWidth = 0
        minHeight = 0
        for i in sortedWidths:  minWidth  += i[1]
        for i in sortedHeights: minHeight += i[1]

        if h < minHeight: h = minHeight
        if w < minWidth:  w = minWidth

        #TTkLog.debug(f"w,h:({w,h}) mh:{minHeight} sh:{sortedHeights}")
        #TTkLog.debug(f"w,h:({w,h}) mw:{minWidth}  sw:{sortedWidths}")

        def parseSizes(sizes, space, out):
            iterate = True
            freeSpace = space
            leftSlots = len(sizes)
            while iterate and leftSlots > 0:
                iterate = False
                for item in sizes:
                    if item[3] != -1: continue
                    if freeSpace < 0: freeSpace=0
                    sliceSize = freeSpace//leftSlots
                    mins = item[1]
                    maxs = item[2]
                    if sliceSize >= maxs:
                        iterate = True
                        freeSpace -= maxs
                        leftSlots -= 1
                        item[3] = maxs
                    elif sliceSize < mins:
                        iterate = True
                        freeSpace -= mins
                        leftSlots -= 1
                        item[3] = mins
            # Push the sizes
            for item in sizes:
                out[item[0]] = [0,item[3]]
                if item[3] == -1:
                    sliceSize = freeSpace//leftSlots
                    out[item[0]] = [0,sliceSize]
                    freeSpace -= sliceSize
                    leftSlots -= 1

        vertSizes = [None]*len(sortedHeights)
        horSizes  = [None]*len(sortedWidths)
        parseSizes(sortedHeights,h, vertSizes)
        parseSizes(sortedWidths, w, horSizes)

        for i in horSizes:
            i[0] = newx
            newx += i[1]
        for i in vertSizes:
            i[0] = newy
            newy += i[1]

        #TTkLog.debug(f"h:{horSizes} v:{vertSizes}")

        # loop and set the geometry of any item
        for item in self.children():
            col = item._col
            row = item._row
            item.setGeometry(
                    horSizes[col][0], vertSizes[row][0] ,
                    horSizes[col][1], vertSizes[row][1] )
            #TTkLog.debug(f"Children: {item.geometry()}")
            if item.layoutItemType == TTkK.WidgetItem and not item.isEmpty():
                #TTkLog.debug(f"Children name: {item.widget()._name}")
                item.widget().update(*args, **kwargs)
            elif item.layoutItemType == TTkK.LayoutItem:
                item.update(*args, **kwargs)
        return True
