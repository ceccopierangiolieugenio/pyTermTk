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
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkWidgets.testwidget import TTkTestWidget
from TermTk.TTkWidgets.spacer import TTkSpacer
from TermTk.TTkWidgets.scrollbar import TTkScrollBar

class _TTkTableViewHeader(TTkWidget):
    __slots__ = (
            '_header', '_showHeader',
            '_alignments', '_headerColor',
            '_columns')
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
    def setHeader(self, header):
        if len(header) != len(self._columns):
            return
        self._header = header

    def setColumnSize(self, columns):
        self._columns = columns
        self._header = [""]*len(self._columns)
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

class _TTkTableViewData(TTkWidget):
    __slots__ = (
            '_alignments',
            '_columns', '_columnColors',
             '_tableData',
            '_selectColor', '_moveTo', '_selected')
    def __init__(self, *args, **kwargs):
        self._moveTo = 0
        self._tableData = []
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTableViewData' )
        self._columns = kwargs.get('columns' , [-1] )
        self._alignments = [TTkK.NONE]*len(self._columns)
        self._columnColors = kwargs.get('columnColors' , [TTkColor.RST]*len(self._columns) )
        self._selectColor = kwargs.get('selectColor' , TTkColor.BOLD )
        self._selected = -1
        self.setFocusPolicy(TTkK.ClickFocus)

class _TTkTableView(TTkWidget):
    __slots__ = (
            '_header', '_showHeader',
            '_alignments', '_headerColor',
            '_columns', '_columnColors',
             '_tableData',
            '_selectColor', '_moveTo', '_selected',
            # Signals
            'tableMoved', 'displayedMaxRowsChanged', 'tablePropertiesChanged')
    def __init__(self, *args, **kwargs):
        self._moveTo = 0
        self._tableData = []
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTableView' )
        # define signals
        self.tableMoved = pyTTkSignal(int) # Value
        self.displayedMaxRowsChanged = pyTTkSignal(int) # Value
        self.tablePropertiesChanged  = pyTTkSignal(int, int, int, int) # selected, numItems, displayed lines, offsetView

        self._columns = kwargs.get('columns' , [-1] )
        self._header = [""]*len(self._columns)
        self._showHeader = False
        self._alignments = [TTkK.NONE]*len(self._columns)
        self._columnColors = kwargs.get('columnColors' , [TTkColor.RST]*len(self._columns) )
        self._selectColor = kwargs.get('selectColor' , TTkColor.BOLD )
        self._headerColor = kwargs.get('headerColor' , TTkColor.BOLD )
        self._selected = -1
        self.setFocusPolicy(TTkK.ClickFocus)

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

    def items(self): return self._tableData

    def setAlignment(self, alignments):
        if len(alignments) != len(self._columns):
            return
        self._alignments = alignments

    def setColumnSize(self, columns):
        self._columns = columns
        self._columnColors = [TTkColor.RST]*len(self._columns)
        self._header = [""]*len(self._columns)
        self._alignments = [TTkK.NONE]*len(self._columns)

    def setColumnColors(self, colors):
        if len(colors) != len(self._columns):
            return
        self._columnColors = colors

    def appendItem(self, item):
        if len(item) != len(self._columns):
            return
        self._tableData.append(item)
        self.tablePropertiesChanged.emit(self._selected, len(self._tableData), self.height(), self._moveTo)
        self.update()

    def mousePressEvent(self, evt):
        x,y = evt.x, evt.y
        if x == self.width() - 1:
            return False
        if y > 0:
            self._selected = self._moveTo + y - 1
            self.update()
        return True

    def wheelEvent(self, evt):
        delta = TTkCfg.scrollDelta
        if evt.evt == TTkK.WHEEL_Up:
            delta = -delta
        self.scrollTo(self._moveTo + delta)
        self.update()
        return True

    def resizeEvent(self, w, h):
        if self._moveTo > len(self._tableData)-h-1:
            self._moveTo = len(self._tableData)-h-1
        if self._moveTo < 0:
            self._moveTo = 0
        self.displayedMaxRowsChanged.emit(h)
        self.tablePropertiesChanged.emit(self._selected, len(self._tableData), self.height(), self._moveTo)

    @pyTTkSlot(int)
    def scrollTo(self, to):
        # TTkLog.debug(f"to:{to},h{self._height},size:{len(self._tableData)}")
        max = len(self._tableData) - self.height()
        if to>max: to=max
        if to<0: to=0
        self._moveTo = to
        self.tableMoved.emit(to)
        self.tablePropertiesChanged.emit(self._selected, len(self._tableData), self.height(), self._moveTo)
        self.update()


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

        maxItems = len(self._tableData)
        itemFrom = self._moveTo
        if itemFrom > maxItems-h: itemFrom = maxItems-h
        if itemFrom < 0 : itemFrom = 0
        itemTo   = itemFrom + h
        if itemTo > maxItems: itemTo = maxItems
        # TTkLog.debug(f"moveto:{self._moveTo}, maxItems:{maxItems}, f:{itemFrom}, t{itemTo}, h:{h}, sel:{self._selected}")

        y = 0
        for it in range(itemFrom, itemTo):
            item = self._tableData[it]
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
            y+=1


class TTkTable(TTkWidget):
    __slots__ = ('_vscroller', '_hscroller', '_tableView', '_headerView', '_showHeader')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTable' )
        if 'parent' in kwargs:
            kwargs.pop('parent')
        self._tableView = _TTkTableView(*args, **kwargs)
        self._headerView = _TTkTableViewHeader(*args, **kwargs)
        self._showHeader = kwargs.get('showHeader',True)
        self._vscroller = TTkScrollBar(orientation=TTkK.VERTICAL)
        self._hscroller = TTkScrollBar(orientation=TTkK.HORIZONTAL)
        self.setLayout(TTkGridLayout())
        self._vscroller.sliderMoved.connect(self._tableView.scrollTo)
        self._tableView.tablePropertiesChanged.connect(self.handleTableProperties)
        self.layout().addWidget(self._headerView,0,0)
        self.layout().addWidget(self._tableView,1,0)
        # self.layout().addWidget(TTkTestWidget(border=True),0,0)
        self.layout().addWidget(self._vscroller,1,1)
        # self.layout().addWidget(self._hscroller,1,0)
        if not self._showHeader:
            self._headerView.hide()

        self.setFocusPolicy(TTkK.ClickFocus)

    def setAlignment(self, *args, **kwargs)   :
        self._tableView.setAlignment(*args, **kwargs)
        self._headerView.setAlignment(*args, **kwargs)
    def setHeader(self, *args, **kwargs)      :
        self._headerView.setHeader(*args, **kwargs)
    def setColumnSize(self, *args, **kwargs)  :
        self._tableView.setColumnSize(*args, **kwargs)
        self._headerView.setColumnSize(*args, **kwargs)
    def setColumnColors(self, *args, **kwargs):
        self._tableView.setColumnColors(*args, **kwargs)
    def appendItem(self, *args, **kwargs)     :
        self._vscroller.setRangeTo(len(self._tableView.items()))
        self._tableView.appendItem(*args, **kwargs)

    @pyTTkSlot(int, int, int, int)
    def handleTableProperties(self, selected, items, height, offset):
        self._vscroller.setRange(0, items-height)
        self._vscroller.setValue(offset)




