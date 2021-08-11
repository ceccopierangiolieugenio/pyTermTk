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

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class _TTkTableViewHeader(TTkWidget):
    __slots__ = ('_header', '_alignments', '_headerColor', '_columns')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTableViewHeader' )
        self._columns = kwargs.get('columns' , [-1] )
        self._header = [""]*len(self._columns)
        self._alignments = [TTkK.NONE]*len(self._columns)
        self._headerColor = kwargs.get('headerColor' , TTkColor.BOLD )
        self.setMaximumHeight(1)
        self.setMinimumHeight(1)

    def setAlignment(self, alignments):
        if len(alignments) != len(self._columns):
            return
        self._alignments = alignments

    def setHeader(self, header):
        if len(header) != len(self._columns):
            return
        self._header = header

    def setColumnSize(self, columns):
        self._columns = columns
        self._header += [""]*(len(self._columns)-len(self._header))
        self._alignments = [TTkK.NONE]*len(self._columns)

    def paintEvent(self):
        w,h = self.size()
        total = 0
        variableCols = 0
        # Retrieve the free size
        for width in self._columns:
            if width > 0:
                total += width
            else:
                variableCols += 1
        # Define the list of cols sizes
        sizes = []
        for width in self._columns:
            if width > 0:
                sizes.append(width)
            else:
                sizes.append((w-total)//variableCols)
                variableCols -= 1
        colors = [self._headerColor]*len(self._header)
        self._canvas.drawTableLine(pos=(0,0), items=self._header, sizes=sizes, colors=colors, alignments=self._alignments)


class _TTkTableView(TTkAbstractScrollView):
    __slots__ = (
            '_alignments', '_headerColor',
            '_columns', '_columnColors',
            '_tableDataId', '_tableDataText', '_tableDataWidget', '_shownWidgets',
            '_selectColor', '_selected',
            # Signals
            'activated')
    def __init__(self, *args, **kwargs):
        self._tableDataId = []
        self._tableDataText = []
        self._tableDataWidget = []
        self._shownWidgets = []
        TTkAbstractScrollView.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTableView' )
        # define signals
        self.activated = pyTTkSignal(int) # Value

        self._columns = kwargs.get('columns' , [-1] )
        self._alignments = [TTkK.NONE]*len(self._columns)
        self._columnColors = kwargs.get('columnColors' , [TTkColor.RST]*len(self._columns) )
        self._selectColor = kwargs.get('selectColor' , TTkColor.BOLD )
        self._headerColor = kwargs.get('headerColor' , TTkColor.BOLD )
        self._selected = -1
        self.setFocusPolicy(TTkK.ClickFocus)
        self.viewChanged.connect(self._viewChangedHandler)

    def _initSignals(self):
        # self.cellActivated(int row, int column)
        # self.cellChanged(int row, int column)
        # self.cellClicked(int row, int column)
        # self.cellDoubleClicked(int row, int column)
        # self.cellEntered(int row, int column)
        # self.cellPressed(int row, int column)
        # self.currentCellChanged(int currentRow, int currentColumn, int previousRow, int previousColumn)
        # self.currentItemChanged(QTableWidgetItem *current, QTableWidgetItem *previous)
        # self.itemActivated(QTableWidgetItem *item)
        # self.itemChanged(QTableWidgetItem *item)
        # self.itemClicked(QTableWidgetItem *item)
        # self.itemDoubleClicked(QTableWidgetItem *item)
        # self.itemEntered(QTableWidgetItem *item)
        # self.itemPressed(QTableWidgetItem *item)
        # self.itemSelectionChanged()
        pass

    @pyTTkSlot()
    def _viewChangedHandler(self):
        w,h = self.size()
        _, oy = self.getViewOffsets()
        total = 0
        variableCols = 0
        # Retrieve the free size
        for width in self._columns:
            if width > 0:
                total += width
            else:
                variableCols += 1
        # Define the list of cols sizes
        sizes = []
        for width in self._columns:
            if width > 0:
                sizes.append(width)
            else:
                sizes.append((w-total)//variableCols)
                variableCols -= 1

        maxItems = len(self._tableDataText)
        itemFrom = oy
        if itemFrom > maxItems-h: itemFrom = maxItems-h
        if itemFrom < 0 : itemFrom = 0
        itemTo   = itemFrom + h
        if itemTo > maxItems: itemTo = maxItems

        widgetsToHide = self._shownWidgets
        self._shownWidgets = []
        for y, it in enumerate(range(itemFrom, itemTo)):
            x = 0
            item = self._tableDataWidget[it]
            for iw, widget in enumerate(item):
                size = sizes[iw]
                if widget is not None:
                    if widget.parentWidget() != self:
                        self.addWidget(widget)
                    widget.setGeometry(x,y,size,1)
                    widget.show()
                    self._shownWidgets.append(widget)
                x+=size+1
        for widget in widgetsToHide:
            if widget not in self._shownWidgets:
                widget.hide()



    def viewFullAreaSize(self) -> (int, int):
        return self.width(), len(self._tableDataText)

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def items(self): return self._tableDataText

    def setAlignment(self, alignments):
        if len(alignments) != len(self._columns):
            return
        self._alignments = alignments

    def setColumnSize(self, columns):
        self._columns = columns
        self._columnColors = [TTkColor.RST]*len(self._columns)
        self._alignments = [TTkK.NONE]*len(self._columns)

    def setColumnColors(self, colors):
        if len(colors) != len(self._columns):
            return
        self._columnColors = colors

    def appendItem(self, item, id=None):
        if len(item) != len(self._columns):
            return
        textItem = [i if isinstance(i,str) else "" for i in item]
        widgetItem = [i if isinstance(i,TTkWidget) else None for i in item]
        if id is not None:
            self._tableDataId.append(id)
        else:
            self._tableDataId.append(item)
        self._tableDataText.append(textItem)
        self._tableDataWidget.append(widgetItem)
        self.viewChanged.emit()
        self.update()

    def insertItem(self, index, item, id=None):
        if len(item) != len(self._columns):
            return#
        textItem = [i if isinstance(i,str) else "" for i in item]
        widgetItem = [i if isinstance(i,TTkWidget) else None for i in item]
        if id is not None:
            self._tableDataId.insert(index, id)
        else:
            self._tableDataId.insert(index, item)
        self._tableDataText.insert(index, textItem)
        self._tableDataWidget.insert(index, widgetItem)
        self.viewChanged.emit()
        self.update()

    def removeItem(self, item):
        index = self.indexOf(item)
        self.removeItemAt(index)
        self.viewChanged.emit()
        self.update()

    def removeItemAt(self, index):
        if self._selected == index:
            self._selected = -1
        del self._tableDataId[index]
        del self._tableDataText[index]
        del self._tableDataWidget[index]
        self.viewChanged.emit()
        self.update()

    def removeItemsFrom(self, index):
        if self._selected >= index:
            self._selected = -1
        self._tableDataId = self._tableDataId[:index]
        self._tableDataText = self._tableDataText[:index]
        self._tableDataWidget = self._tableDataWidget[:index]
        self.viewChanged.emit()
        self.update()

    def indexOf(self, id) -> int:
        for index, value in enumerate(self._tableDataId):
            if id is value:
                return index
        return -1


    def mousePressEvent(self, evt):
        _,y = evt.x, evt.y
        _, oy = self.getViewOffsets()
        if y >= 0:
            selected = oy + y
            if selected >= len(self._tableDataText):
                selected = -1
            self._selected = selected
            self.update()
            self.activated.emit(self._selected)
        return True

    def paintEvent(self):
        w,h = self.size()
        _, oy = self.getViewOffsets()
        total = 0
        variableCols = 0
        # Retrieve the free size
        for width in self._columns:
            if width > 0:
                total += width
            else:
                variableCols += 1
        # Define the list of cols sizes
        sizes = []
        for width in self._columns:
            if width > 0:
                sizes.append(width)
            else:
                sizes.append((w-total)//variableCols)
                variableCols -= 1

        maxItems = len(self._tableDataText)
        itemFrom = oy
        if itemFrom > maxItems-h: itemFrom = maxItems-h
        if itemFrom < 0 : itemFrom = 0
        itemTo   = itemFrom + h
        if itemTo > maxItems: itemTo = maxItems
        # TTkLog.debug(f"moveto:{self._moveTo}, maxItems:{maxItems}, f:{itemFrom}, t{itemTo}, h:{h}, sel:{self._selected}")

        for y, it in enumerate(range(itemFrom, itemTo)):
            item = self._tableDataText[it]
            if self._selected > 0:
                val = self._selected - itemFrom
            else:
                val = h//2
            if val < 0 : val = 0
            if val > h : val = h
            if it == self._selected:
                colors = [self._selectColor]*len(self._columnColors)
                self._canvas.drawTableLine(pos=(0,y), items=item, sizes=sizes, colors=colors, alignments=self._alignments)
            else:
                colors = [c.modParam(val=-val) for c in self._columnColors]
                self._canvas.drawTableLine(pos=(0,y), items=item, sizes=sizes, colors=colors, alignments=self._alignments)

class TTkTableView(TTkAbstractScrollView):
    __slots__ = (
        '_header', '_tableView', '_showHeader', 'activated',
        # Forwarded Methods
        'setHeader', 'setColumnColors', 'appendItem', 'indexOf', 'insertItem', 'removeItem', 'removeItemAt', 'removeItemsFrom')

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTableView' )
        if 'parent' in kwargs: kwargs.pop('parent')
        self._showHeader = kwargs.get('showHeader', True)
        self.setLayout(TTkGridLayout())
        self._tableView = _TTkTableView(*args, **kwargs)
        self._header = _TTkTableViewHeader(*args, **kwargs)
        self.layout().addWidget(self._header,0,0)
        self.layout().addWidget(self._tableView,1,0)
        # Forward the tableSignals
        self.viewMovedTo     = self._tableView.viewMovedTo
        self.viewSizeChanged = self._tableView.viewSizeChanged
        self.activated       = self._tableView.activated
        self.viewChanged     = self._tableView.viewChanged
        if not self._showHeader:
            self._header.hide()

        # Forward Methods
        self.setHeader       = self._header.setHeader
        self.setColumnColors = self._tableView.setColumnColors
        self.appendItem      = self._tableView.appendItem
        self.indexOf         = self._tableView.indexOf
        self.insertItem      = self._tableView.insertItem
        self.removeItem      = self._tableView.removeItem
        self.removeItemAt    = self._tableView.removeItemAt
        self.removeItemsFrom = self._tableView.removeItemsFrom

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x, y):
        self._tableView.viewMoveTo(x, y)

    def getViewOffsets(self):
        return self._tableView.getViewOffsets()

    def viewFullAreaSize(self) -> (int, int):
        return self._tableView.viewFullAreaSize()

    def viewDisplayedSize(self) -> (int, int):
        return self._tableView.viewDisplayedSize()

    def setAlignment(self, *args, **kwargs)   :
        self._tableView.setAlignment(*args, **kwargs)
        self._header.setAlignment(*args, **kwargs)
    def setColumnSize(self, *args, **kwargs)  :
        self._tableView.setColumnSize(*args, **kwargs)
        self._header.setColumnSize(*args, **kwargs)
