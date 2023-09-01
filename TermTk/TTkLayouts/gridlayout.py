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
**Grid Layout** [`Tutorial <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/002-layout.html#simple-ttkgridlayout>`__]
'''

__all__ = ['TTkGridLayout']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkLayouts.layout import TTkLayout

class TTkGridLayout(TTkLayout):
    '''
    The grid layout allows an automatic place all the widgets in a grid, <br/>
    the empty rows/cols are resized to the "rowMinHeight,columnMinWidth" parameters

    ::

        TTkGridLayout        ┌┐ columnMinWidth
         ╔═════════╤═════════╤╤═════════╗
         ║ Widget1 │ Widget2 ││ Widget3 ║
         ║ (0,0)   │ (0,1)   ││ (0,3)   ║
         ╟─────────┼─────────┼┼─────────╢ ┐ rowMinHeight
         ╟─────────┼─────────┼┼─────────╢ ┘
         ║ Widget4 │         ││         ║
         ║ (2,0)   │         ││         ║
         ╟─────────┼─────────┼┼─────────╢
         ║         │         ││ Widget5 ║
         ║         │         ││ (3,3)   ║
         ╚═════════╧═════════╧╧═════════╝

    :param int columnMinWidth: the minimum width of the column, optional, defaults to 0
    :param int rowMinHeight: the minimum height of the column, optional, defaults to 0
    '''

    __slots__ = ('_gridItems','_columnMinWidth','_rowMinHeight', '_rows', '_cols', '_horSizes', '_verSizes')
    def __init__(self, *args, **kwargs):
        self._rows = 0
        self._cols = 0
        TTkLayout.__init__(self, *args, **kwargs)
        self._gridItems = [[]]
        self._horSizes = []
        self._verSizes = []
        self._columnMinWidth = kwargs.get('columnMinWidth',0)
        self._rowMinHeight = kwargs.get('rowMinHeight',0)

    def _gridUsedsize(self):
        rows = 0
        cols = 0
        for gridRow in range(self._rows):
            for gridCol in range(self._cols):
                if item:=self._gridItems[gridRow][gridCol]:
                    rows = max(rows, gridRow+item._rowspan)
                    cols = max(cols, gridCol+item._colspan)
        return (rows, cols)

    def _reshapeGrid(self, size):
        rows, cols = size
        self._rows, self._cols = size

        # remove extra rows
        if   rows < len(self._gridItems):
            self._gridItems = self._gridItems[:rows]
            self._verSizes  = self._verSizes[:rows]
        elif rows > len(self._gridItems):
            self._gridItems += [None]*(rows-len(self._gridItems))
            self._verSizes += [(0,0)]*(rows-len(self._verSizes))

        # remove extra cols
        if   cols < len(self._gridItems):
            self._horSizes  = self._verSizes[:cols]
        elif cols > len(self._gridItems):
            self._horSizes += [(0,0)]*(cols-len(self._horSizes))

        for gridRow in range(len(self._gridItems)):
            if self._gridItems[gridRow] is None:
                self._gridItems[gridRow] = [None]*(cols)
                continue
            sizeRow = len(self._gridItems[gridRow])
            if cols < sizeRow:
                self._gridItems[gridRow] = self._gridItems[gridRow][:cols]
            elif cols > sizeRow:
                self._gridItems[gridRow] += [None]*(cols-sizeRow)

    def gridSize(self):
        return self._rows, self._cols

    def getSizes(self):
        return self._horSizes, self._verSizes

    def columnMinWidth(self):
        return self._columnMinWidth

    def setColumnMinWidth(self, cmw):
        if self._columnMinWidth == cmw: return
        self._columnMinWidth = cmw
        self.update()

    def rowMinHeight(self):
        return self._rowMinHeight

    def setRowMinHeight(self, rmh):
        if self._rowMinHeight == rmh: return
        self._rowMinHeight = rmh
        self.update()

    def gridItems(self):
        return self._gridItems

    def repack(self):
        rown=coln= -1
        # remove empty rows
        for r in reversed(range(self._rows)):
            if not(any([self.itemAtPosition(r,c) for c in range(self._cols)])):
                # the row is empty
                self._gridItems.pop(r)
        # Realign the rows
        for rown,r in enumerate(self._gridItems):
            for coln,w in enumerate(r):
                if w: w._row = rown
        self._reshapeGrid((rown+1,self._cols))
        #remove empty cols
        unusedCols = []
        for c in range(self._cols):
            if not(any([self.itemAtPosition(r,c) for r in range(self._rows)])):
                unusedCols.append(c)
        for c in reversed(unusedCols):
            for r in self._gridItems:
                r.pop(c)
        # Realign the cols
        for rown,r in enumerate(self._gridItems):
            for coln,w in enumerate(r):
                if w: w._col = coln
        self._reshapeGrid((rown+1,coln+1))
        self.update()

    def insertColumn(self, col):
        self._cols += 1
        for c in self.children():
            if c._col >= col:
                c._col += 1
        for i,r in enumerate(self._gridItems):
            self._gridItems[i][col:col] = [None]
        self.update()

    def insertRow(self, row):
        self._rows += 1
        for c in self.children():
            if c._row >= row:
                c._row += 1
        self._gridItems.insert(row, [None]*self._cols)
        self.update()

    # addWidget(self, widget, row, col)
    def addWidget(self, widget, row=None, col=None, rowspan=1, colspan=1, direction=TTkK.HORIZONTAL):
        '''Add the widget to this :class:`TTkGridLayout`, this function uses :meth:`~addItem`

        :param widget: the widget to be added
        :type widget: :class:`~TermTk.TTkWidgets.widget.TTkWidget`
        :param int row:     the row of the grid, optional, defaults to None
        :param int col:     the col of the grid, optional, defaults to None
        :param int rowspan: the rows used by the widget, optional, defaults to 1
        :param int colspan: the cols used by the widget, optional, defaults to 1
        :param direction: The direction the new item will be added if row/col are not specified, defaults to defaults to :class:`~TermTk.TTkCore.constant.TTkConstant.Direction.HORIZONTAL`
        :type direction: :class:`~TermTk.TTkCore.constant.TTkConstant.Direction`
        '''
        TTkGridLayout.addWidgets(self,[widget], row, col, rowspan, colspan, direction)

    def addWidgets(self, widgets, row=None, col=None, rowspan=1, colspan=1, direction=TTkK.HORIZONTAL):
        '''Add the widgets to this :class:`TTkGridLayout`, this function uses :meth:`~addItem`

        :param widgets: the widgets to be added
        :type widgets: list of :class:`~TermTk.TTkWidgets.widget.TTkWidget`
        :param int row:     the row of the grid, optional, defaults to None
        :param int col:     the col of the grid, optional, defaults to None
        :param int rowspan: the rows used by the widget, optional, defaults to 1
        :param int colspan: the cols used by the widget, optional, defaults to 1
        :param direction: The direction the new items will be added if row/col are not specified, defaults to defaults to :class:`~TermTk.TTkCore.constant.TTkConstant.Direction.HORIZONTAL`
        :type direction: :class:`~TermTk.TTkCore.constant.TTkConstant.Direction`
        '''
        self.removeWidgets(widgets)
        items = [w.widgetItem() for w in widgets]
        TTkGridLayout.addItems(self, items, row, col, rowspan, colspan, direction)
        for w in widgets:
            w.update()

    def replaceItem(self, item, index): pass

    def addItem(self, item, row=None, col=None, rowspan=1, colspan=1, direction=TTkK.HORIZONTAL):
        '''Add the item to this :class:`TTkGridLayout`

        :param item: the item to be added
        :type item: :class:`~TermTk.TTkLayouts.layout.TTkLayoutItem`
        :param int row:     the row of the grid, optional, defaults to None
        :param int col:     the col of the grid, optional, defaults to None
        :param int rowspan: the rows used by the item, optional, defaults to 1
        :param int colspan: the cols used by the item, optional, defaults to 1
        :param direction: The direction the new item will be added if row/col are not specified, defaults to defaults to :class:`~TermTk.TTkCore.constant.TTkConstant.Direction.HORIZONTAL`
        :type direction: :class:`~TermTk.TTkCore.constant.TTkConstant.Direction`
        '''
        self.addItems([item],row,col,rowspan,colspan,direction)

    def addItems(self, items, row=None, col=None, rowspan=1, colspan=1, direction=TTkK.HORIZONTAL):
        '''Add the items to this :class:`TTkGridLayout`

        :param items: the items to be added
        :type items: list of :class:`~TermTk.TTkLayouts.layout.TTkLayoutItem`
        :param int row:     the row of the grid, optional, defaults to None
        :param int col:     the col of the grid, optional, defaults to None
        :param int rowspan: the rows used by the item, optional, defaults to 1
        :param int colspan: the cols used by the item, optional, defaults to 1
        :param direction: The direction the new items will be added if row/col are not specified, defaults to defaults to :class:`~TermTk.TTkCore.constant.TTkConstant.Direction.HORIZONTAL`
        :type direction: :class:`~TermTk.TTkCore.constant.TTkConstant.Direction`
        '''
        nitems = len(items)
        self.removeItems(items)
        if row is None and col is None:
            # Append The widget at the end
            if direction==TTkK.HORIZONTAL:
                row = 0
                col = self._cols
            else:
                row = self._rows
                col = 0

        #retrieve the max col/rows to reshape the grid
        maxrow = row + rowspan * nitems
        maxcol = col + colspan * nitems
        for child in self.children():
            maxrow = max(maxrow, child._row + child._rowspan)
            maxcol = max(maxcol, child._col + child._colspan)

        # TODO: This is RUBBISH!!!
        self._reshapeGrid(size=(maxrow,maxcol))
        if self._gridItems[row][col] is not None:
            # TODO: Handle the LayoutItem
            self.removeItem(self._gridItems[row][col])
        self._reshapeGrid(size=(maxrow,maxcol))

        for item in items:
            item._row = row
            item._col = col
            item._rowspan = rowspan
            item._colspan = colspan
            self._gridItems[row][col] = item
            if direction==TTkK.HORIZONTAL:
                col += colspan
            else:
                row += rowspan

        TTkLayout.addItems(self, items)

    def removeItem(self, item):
        self.removeItems([item])

    def removeItems(self, items):
        TTkLayout.removeItems(self, items)
        for gridRow in range(self._rows):
            for gridCol in range(self._cols):
                if self._gridItems[gridRow][gridCol] in items:
                    self._gridItems[gridRow][gridCol] = None
        self._reshapeGrid(self._gridUsedsize())

    def removeWidget(self, widget):
        self.removeWidgets([widget])

    def removeWidgets(self, widgets):
        TTkLayout.removeWidgets(self, widgets)
        for gridRow in range(self._rows):
            for gridCol in range(self._cols):
                if self._gridItems[gridRow][gridCol] is not None and \
                   self._gridItems[gridRow][gridCol]._layoutItemType == TTkK.WidgetItem and \
                   self._gridItems[gridRow][gridCol].widget() in widgets:
                    self._gridItems[gridRow][gridCol] = None
        self._reshapeGrid(self._gridUsedsize())

    def itemAtPosition(self, row: int, col: int):
        if ( row<0 or row >= self._rows or
             col<0 or col >= self._cols ):
            return None
        if item := self._gridItems[row][col]:
            return item
        for item in self.children():
            if item._row + item._rowspan > row >= item._row and \
               item._col + item._colspan > col >= item._col :
                return item
        return None

    def minimumColWidth(self, gridCol: int) -> int:
        colw = 0
        anyItem = False
        for gridRow in range(self._rows):
            item = self.itemAtPosition(gridRow,gridCol)
            if item is not None and \
               ( item._layoutItemType == TTkK.LayoutItem or item.isVisible() ):
                    anyItem = True
                    w = item.minimumWidthSpan(gridCol)
                    if colw < w:
                        colw = w
        if not anyItem:
            return self._columnMinWidth
        return colw

    def minimumRowHeight(self, gridRow: int):
        rowh = 0
        anyItem = False
        for gridCol in range(self._cols):
            item = self.itemAtPosition(gridRow,gridCol)
            if item is not None and \
               ( item._layoutItemType == TTkK.LayoutItem or item.isVisible() ):
                    anyItem = True
                    h = item.minimumHeightSpan(gridRow)
                    if rowh < h:
                        rowh = h
        if not anyItem:
            return self._rowMinHeight
        return rowh

    def maximumColWidth(self, gridCol: int) -> int:
        colw = 0x10000
        anyItem = False
        for gridRow in range(self._rows):
            item = self.itemAtPosition(gridRow,gridCol)
            if item is not None and \
               ( item._layoutItemType == TTkK.LayoutItem or item.isVisible() ):
                    anyItem = True
                    w = item.maximumWidthSpan(gridCol)
                    if colw > w:
                        colw = w
        if not anyItem:
            return self._columnMinWidth
        return colw

    def maximumRowHeight(self, gridRow: int):
        rowh = 0x10000
        anyItem = False
        for gridCol in range(self._cols):
            item = self.itemAtPosition(gridRow,gridCol)
            if item is not None and \
               ( item._layoutItemType == TTkK.LayoutItem or item.isVisible() ):
                    anyItem = True
                    h = item.maximumHeightSpan(gridRow)
                    if rowh > h:
                        rowh = h
        if not anyItem:
            return self._rowMinHeight
        return rowh

    def minimumWidth(self) -> int:
        ''' process the widgets and get the min size '''
        minw = 0
        for gridCol in range(self._cols):
            minw += self.minimumColWidth(gridCol)
        return minw

    def minimumHeight(self) -> int:
        ''' process the widgets and get the min size '''
        minh = 0
        for gridRow in range(self._rows):
            minh += self.minimumRowHeight(gridRow)
        return minh

    def maximumWidth(self) -> int:
        ''' process the widgets and get the min size '''
        if not self._rows:
            return 0x1000
        maxw = 0
        for gridCol in range(self._cols):
            maxw += self.maximumColWidth(gridCol)
        return maxw

    def maximumHeight(self) -> int:
        ''' process the widgets and get the min size '''
        if not self._cols:
            return 0x1000
        maxh = 0
        for gridRow in range(self._rows):
            maxh += self.maximumRowHeight(gridRow)
        return maxh


    def update(self, *args, **kwargs):
        _, _, w, h = self.geometry()
        newx, newy = 0, 0

        # Sorted List of minimum heights
        #                    min                        max                       val
        #  content IDs     0 1                          2                         3
        sortedHeights = [ [i, self.minimumRowHeight(i), self.maximumRowHeight(i), -1] for i in range(self._rows) ]
        sortedWidths  = [ [i, self.minimumColWidth(i),  self.maximumColWidth(i),  -1] for i in range(self._cols) ]
        sortedHeights = sorted(sortedHeights, key=lambda h: h[1])
        sortedWidths  = sorted(sortedWidths,  key=lambda w: w[1])

        minWidth = 0
        minHeight = 0
        for i in sortedWidths:  minWidth  += i[1]
        for i in sortedHeights: minHeight += i[1]

        if h < minHeight: h = minHeight
        if w < minWidth:  w = minWidth

        # TTkLog.debug(f"Height: w,h:({w,h}) mh:{minHeight} sh:{sortedHeights}")
        # TTkLog.debug(f"width:  w,h:({w,h}) mw:{minWidth}  sw:{sortedWidths}")

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

        # TTkLog.debug(f"h:{horSizes} v:{vertSizes}")

        # loop and set the geometry of any item
        for item in self.children():
            col = item._col
            row = item._row
            x,y = horSizes[col][0], vertSizes[row][0]
            w = sum( horSizes[col+i][1]  for i in range(item._colspan) )
            h = sum( vertSizes[row+i][1] for i in range(item._rowspan) )
            item.setGeometry(x, y, w, h)
            #TTkLog.debug(f"Children: {item.geometry()}")
            if item._layoutItemType == TTkK.WidgetItem and not item.isEmpty():
                #TTkLog.debug(f"Children name: {item.widget()._name}")
                item.widget().update(*args, **kwargs)
            elif item._layoutItemType == TTkK.LayoutItem:
                item.update(*args, **kwargs)
        self._horSizes = horSizes
        self._verSizes = vertSizes
        return True
