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

__all__ = ['TTkFancyTableView']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

from TermTk.TTkWidgets.widget import TTkWidget

from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class _TTkFancyTableViewHeader(TTkAbstractScrollView):
    __slots__ = ('_header', '_alignments', '_headerColor', '_columns')
    def __init__(self, *,
                 columns:list[int]=None,
                 headerColor:TTkColor=TTkColor.BOLD,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self._columns = columns if columns else [-1]
        self._header = [TTkString()]*len(self._columns)
        self._alignments = [TTkK.NONE]*len(self._columns)
        self._headerColor = headerColor
        self.setMaximumHeight(1)
        self.setMinimumHeight(1)

    # Override this function
    def viewFullAreaSize(self) -> tuple[int,int]:
        return self.size()

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int):
        pass

    def setAlignment(self, alignments):
        if len(alignments) != len(self._columns):
            return
        self._alignments = alignments

    def setHeader(self, header):
        if len(header) != len(self._columns):
            return
        self._header = [TTkString(i) if isinstance(i,str) else i if issubclass(type(i), TTkString) else TTkString() for i in header]


    def setColumnSize(self, columns):
        self._columns = columns
        self._header += [TTkString()]*(len(self._columns)-len(self._header))
        self._alignments = [TTkK.NONE]*len(self._columns)

    def paintEvent(self, canvas):
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
        canvas.drawTableLine(pos=(0,0), items=self._header, sizes=sizes, colors=colors, alignments=self._alignments)


class _TTkFancyTableView(TTkAbstractScrollView):
    __slots__ = (
            '_alignments', '_headerColor',
            '_columns', '_columnColors',
            '_tableDataId', '_tableDataText', '_tableDataWidget', '_shownWidgets',
            '_selectColor', '_selected',
            '_tableWidth',
            # Signals
            'activated', 'doubleClicked')
    def __init__(self, *,
                 columns:list[int]=None,
                 columnColors:list[TTkColor]=None,
                 selectColor:TTkColor=TTkColor.BOLD,
                 headerColor:TTkColor=TTkColor.BOLD,
                 **kwargs) -> None:
        self._tableDataId = []
        self._tableDataText = []
        self._tableDataWidget = []
        self._shownWidgets = []
        super().__init__(**kwargs)
        # define signals
        self.activated = pyTTkSignal(int) # Value
        self.doubleClicked = pyTTkSignal(int) # Value

        self._tableWidth = 0
        self._columns = columns if columns else [-1]
        self._alignments = [TTkK.NONE]*len(self._columns)
        self._columnColors = columnColors if columnColors else [TTkColor.RST]*len(self._columns)
        self._selectColor = selectColor
        self._headerColor = headerColor
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
                        self.layout().addWidget(widget)
                    widget.setGeometry(x,y,size,1)
                    widget.show()
                    self._shownWidgets.append(widget)
                x+=size+1
        for widget in widgetsToHide:
            if widget not in self._shownWidgets:
                widget.hide()



    def viewFullAreaSize(self) -> tuple[int,int]:
        return self._tableWidth, len(self._tableDataText)

    # def items(self): return self._tableDataText

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

    def _processValues(self):
        size = 0
        for txt in self._tableDataText:
            size=max(size,sum(t.termWidth() for t in txt))
        if self._tableWidth != size:
            self._tableWidth = size
            self.viewChanged.emit()


    def appendItem(self, item, id=None):
        if len(item) != len(self._columns):
            return
        textItem = [TTkString(i) if isinstance(i,str) else i if issubclass(type(i), TTkString) else TTkString() for i in item]
        widgetItem = [i if isinstance(i,TTkWidget) else None for i in item]
        if id is not None:
            self._tableDataId.append(id)
        else:
            self._tableDataId.append(item)
        self._tableDataText.append(textItem)
        self._tableDataWidget.append(widgetItem)
        self._processValues()
        self.viewChanged.emit()
        self.update()

    def insertItem(self, index: int, item, id=None):
        if len(item) != len(self._columns):
            return#
        textItem = [TTkString(i) if isinstance(i,str) else i if issubclass(type(i), TTkString) else TTkString() for i in item]
        widgetItem = [i if isinstance(i,TTkWidget) else None for i in item]
        if id is not None:
            self._tableDataId.insert(index, id)
        else:
            self._tableDataId.insert(index, item)
        self._tableDataText.insert(index, textItem)
        self._tableDataWidget.insert(index, widgetItem)
        self._processValues()
        self.viewChanged.emit()
        self.update()

    def removeItem(self, item):
        index = self.indexOf(item)
        self.removeItemAt(index)
        self._processValues()
        self.viewChanged.emit()
        self.update()

    def removeItemAt(self, index: int):
        if self._selected == index:
            self._selected = -1
        del self._tableDataId[index]
        del self._tableDataText[index]
        del self._tableDataWidget[index]
        self._processValues()
        self.viewChanged.emit()
        self.update()

    def removeItemsFrom(self, index: int):
        if self._selected >= index:
            self._selected = -1
        self._tableDataId = self._tableDataId[:index]
        self._tableDataText = self._tableDataText[:index]
        self._tableDataWidget = self._tableDataWidget[:index]
        self._processValues()
        self.viewChanged.emit()
        self.update()

    def itemAt(self, index: int):
        if 0 <= index < len(self._tableDataId):
            if item:=self._tableDataWidget[index]:
                return item
            else:
                return self._tableDataText[index]
        return None

    def dataAt(self, index: int):
        if 0 <= index < len(self._tableDataId):
            return self._tableDataId[index]
        return None

    def indexOf(self, id) -> int:
        for index, value in enumerate(self._tableDataId):
            if id is value:
                return index
        return -1

    def mouseDoubleClickEvent(self, evt:TTkMouseEvent) -> bool:
        _,y = evt.x, evt.y
        _, oy = self.getViewOffsets()
        if y >= 0:
            selected = oy + y
            if selected >= len(self._tableDataText):
                selected = -1
            self._selected = selected
            self.update()
            self.doubleClicked.emit(self._selected)
        return True

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
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

    def paintEvent(self, canvas):
        w,h = self.size()
        ox, oy = self.getViewOffsets()
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
        varSizes = []
        for width in self._columns:
            if width > 0:
                sizes.append(width)
            else:
                varSizes.append(len(sizes))
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
            item = self._tableDataText[it].copy()
            if self._selected > 0:
                val = self._selected - itemFrom
            else:
                val = h//2
            if val < 0 : val = 0
            if val > h : val = h
            for vid in varSizes:
                strPos = item[vid].tabCharPos(ox)
                item[vid] = item[vid].substring(fr=strPos)
            if it == self._selected:
                colors = [self._selectColor]*len(self._columnColors)
                canvas.drawTableLine(pos=(0,y), items=item, sizes=sizes, colors=colors, alignments=self._alignments)
            else:
                colors = [c.modParam(val=-val) for c in self._columnColors]
                canvas.drawTableLine(pos=(0,y), items=item, sizes=sizes, colors=colors, alignments=self._alignments)

class TTkFancyTableView(TTkAbstractScrollView):
    __slots__ = (
        '_header', '_tableView', '_showHeader', 'activated', '_excludeEvent',
        # Forwarded Methods
        'setHeader', 'setColumnColors', 'appendItem', 'itemAt', 'dataAt', 'indexOf', 'insertItem',
        'removeItem', 'removeItemAt', 'removeItemsFrom', 'doubleClicked')

    def __init__(self, *,
                 # _TTkFancyTableView init
                 columns:list[int]=None,
                 columnColors:list[TTkColor]=None,
                 selectColor:TTkColor=TTkColor.BOLD,
                 headerColor:TTkColor=TTkColor.BOLD,
                 # TTkFancyTableView init
                 showHeader:bool=True,
                 **kwargs) -> None:
        self._excludeEvent = False
        super().__init__(**kwargs|{'layout':TTkGridLayout()})
        self._showHeader = showHeader
        self._tableView = _TTkFancyTableView(columns=columns, columnColors=columnColors, selectColor=selectColor, headerColor=headerColor, **kwargs)
        self._header = _TTkFancyTableViewHeader(columns=columns, headerColor=headerColor, **kwargs)
        self.layout().addWidget(self._header,0,0)
        self.layout().addWidget(self._tableView,1,0)
        self._tableView.viewChanged.connect(self._viewChanged)
        self._tableView.viewMovedTo.connect(self._viewMovedTo)
        # Forward the tableSignals
        self.activated       = self._tableView.activated
        self.doubleClicked   = self._tableView.doubleClicked
        if not self._showHeader:
            self._header.hide()

        # Forward Methods
        self.setHeader       = self._header.setHeader
        self.setColumnColors = self._tableView.setColumnColors
        self.appendItem      = self._tableView.appendItem
        self.dataAt          = self._tableView.dataAt
        self.itemAt          = self._tableView.itemAt
        self.indexOf         = self._tableView.indexOf
        self.insertItem      = self._tableView.insertItem
        self.removeItem      = self._tableView.removeItem
        self.removeItemAt    = self._tableView.removeItemAt
        self.removeItemsFrom = self._tableView.removeItemsFrom

    @pyTTkSlot()
    def _viewChanged(self):
        if self._excludeEvent: return
        self.viewChanged.emit()

    @pyTTkSlot(int,int)
    def _viewMovedTo(self, x, y):
        if self._excludeEvent: return
        self.viewMoveTo(x, y)

    @pyTTkSlot(int, int)
    def viewMoveTo(self, x: int, y: int):
        fw, fh = self.viewFullAreaSize()
        dw, dh = self.viewDisplayedSize()
        rangex = fw - dw
        rangey = fh - dh
        # TTkLog.debug(f"x:{x},y:{y}, full:{fw,fh}, display:{dw,dh}, range:{rangex,rangey}")
        x = max(0,min(rangex,x))
        y = max(0,min(rangey,y))
        # TTkLog.debug(f"x:{x},y:{y}, wo:{self._viewOffsetX,self._viewOffsetY}")
        if self._viewOffsetX == x and \
           self._viewOffsetY == y: # Nothong to do
            return
        self._excludeEvent = True
        for widget in self.layout().iterWidgets(recurse=False):
            widget.viewMoveTo(x,y)
        self._excludeEvent = False
        self._viewOffsetX = x
        self._viewOffsetY = y
        self.viewMovedTo.emit(x,y)
        self.viewChanged.emit()
        self.update()

    def getViewOffsets(self):
        return self._tableView.getViewOffsets()

    def viewFullAreaSize(self) -> tuple[int,int]:
        return self._tableView.viewFullAreaSize()

    def viewDisplayedSize(self) -> tuple[int,int]:
        return self._tableView.viewDisplayedSize()

    def setAlignment(self, *args, **kwargs)   :
        self._tableView.setAlignment(*args, **kwargs)
        self._header.setAlignment(*args, **kwargs)
    def setColumnSize(self, *args, **kwargs)  :
        self._tableView.setColumnSize(*args, **kwargs)
        self._header.setColumnSize(*args, **kwargs)
