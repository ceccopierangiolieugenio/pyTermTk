# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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


__all__ = ['TTkTableWidget','TTkHeaderView']

from dataclasses import dataclass

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

from TermTk.TTkGui.clipboard import TTkClipboard
from TermTk.TTkGui.textcursor import TTkTextCursor

from TermTk.TTkWidgets.texedit  import TTkTextEdit
from TermTk.TTkWidgets.spinbox  import TTkSpinBox
from TermTk.TTkWidgets.TTkPickers.textpicker import TTkTextPicker
from TermTk.TTkWidgets.TTkModelView.tablemodellist import TTkTableModelList, TTkModelIndex

from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView
from TermTk.TTkAbstract.abstracttablemodel import TTkAbstractTableModel

class TTkHeaderView():
    '''TTkHeaderView
    This is a placeholder for a proper "TTkHeaderView"
    '''
    __slots__ = ('_visible','visibilityUpdated')
    def __init__(self, visible=True) -> None:
        self.visibilityUpdated = pyTTkSignal(bool)
        self._visible = visible

    @pyTTkSlot(bool)
    def setVisible(self, visible: bool) -> None:
        '''setVisible'''
        if self._visible == visible: return
        self._visible = visible
        self.visibilityUpdated.emit(visible)

    @pyTTkSlot()
    def show(self) -> None:
        '''show'''
        self.setVisible(True)

    @pyTTkSlot()
    def hide(self) -> None:
        '''hide'''
        self.setVisible(False)

    def isVisible(self) -> bool:
        return self._visible

class _ClipboardTable(TTkString):
    __slots__=('_data')
    def __init__(self,data) -> None:
        self._data = data
        super().__init__(self._toTTkString())

    def data(self) -> list:
        return self._data

    def _toTTkString(self) -> str:
        def _lineHeight(_line):
            return max(len(str(_item[2]).split('\n')) for _item in _line)
        ret  = []
        minx,maxx = min(_a:=[_item[1] for _line in self._data for _item in _line]),max(_a)
        # miny,maxy = min(_a:=[x[0][0] for x in self._data]),max(_a)
        cols = maxx-minx+1
        colSizes=[0]*cols
        for line in self._data:
            height = _lineHeight(line)
            baseStr = TTkString()
            retLines = [[baseStr]*cols for _ in range(height)]
            for c,item in enumerate(line):
                row,col,data = item
                for r,txt in enumerate(TTkString(data).split('\n')):
                    colSizes[col-minx] = max(colSizes[col-minx],txt.termWidth())
                    retLines[r][col-minx] = TTkString(txt)
            ret += retLines
        return TTkString('\n').join(TTkString(' ').join(s.align(width=colSizes[c]) for c,s in enumerate(l)) for l in ret)

class TTkTableWidget(TTkAbstractScrollView):
    '''
    A :py:class:`TTkTableWidget` implements a table view that displays items from a model.

    ::

            Customer Id     ╿First Name ╿Last Name   ╿Company                         ╿City                ╿
        1  │DD37Cf93aecA6Dc │Sheryl     │Baxter      │Rasmussen Group                 │East Leonard        │
        ╾╌╌┼────────────────┼───────────┼────────────┼────────────────────────────────┼────────────────────┤
        2  │1Ef7b82A4CAAD10 │Preston    │Lozano      │Vega-Gentry                     │East Jimmychester   │
        ╾╌╌┼────────────────┼───────────┼────────────┼────────────────────────────────┼────────────────────┤
        3  │6F94879bDAfE5a6 │Roy        │Berry       │Murillo-Perry                   │Isabelborough       │
        ╾╌╌┼────────────────┼───────────┼────────────┼────────────────────────────────┼────────────────────┤
        4  │5Cef8BFA16c5e3c │Linda      │Olsen       │Dominguez, Mcmillan and Donovan │Bensonview          │
        ╾╌╌┼────────────────┼───────────┼────────────┼────────────────────────────────┼────────────────────┤
        5  │053d585Ab6b3159 │Joanna     │Bender      │Martin, Lang and Andrade        │West Priscilla      │
        ╾╌╌┼────────────────┼───────────┼────────────┼────────────────────────────────┼────────────────────┤
        6  │2d08FB17EE273F4 │Aimee      │Downs       │Steele Group                    │Chavezborough       │
        ╾╌╌┴────────────────┴───────────┴────────────┴────────────────────────────────┴────────────────────┘

    The :py:class:`TTkTableWidget` class is one of the Model/View Classes and is part of TermTk's model/view framework.

    :py:class:`TTkTableWidget` implements the methods to allow it to display data provided by models derived from the :py:class:`TTkAbstractTableModel` class.

    **Navigation**

    You can navigate the cells in the table by clicking on a cell with the mouse,
    or by using the arrow keys,
    you can also hit Tab and Backtab to move from cell to cell.

    **Visual Appearance**

    The table has a vertical header that can be obtained using the :meth:`verticalHeader` function,
    and a horizontal header that is available through the :meth:`horizontalHeader` function.
    The height of each row in the table can be set using :meth:`setRowHeight`;
    similarly, the width of columns can be set using :meth:`setColumnWidth`.

    They can be selected with :meth:`selectRow` and :meth:`selectColumn`.
    The table will show a grid depending on the :meth:`setHSeparatorVisibility` :meth:`setVSeparatorVisibility` methods.

    The items shown in a table view, like those in the other item views, are rendered and edited using standard delegates.
    However, for some tasks it is sometimes useful to be able to insert widgets in a table instead.
    Widgets are set for particular indexes with the setIndexWidget() function, and later retrieved with indexWidget().

    By default, the cells in a table do not expand to fill the available space.
    You can make the cells fill the available space by stretching the last header section.

    To distribute the available space according to the space requirement of each column or row,
    call the view's :meth:`resizeColumnsToContents` or :meth:`resizeRowsToContents` functions.

    '''

    cellChanged:pyTTkSignal
    '''
        This signal is emitted whenever the data of the item in the cell specified by row and column has changed.

        :param row: the row
        :type row: int
        :param col: the column
        :type col: int
    '''
    cellClicked:pyTTkSignal
    '''
        This signal is emitted whenever a cell in the table is clicked.
        The row and column specified is the cell that was clicked.

        :param row: the row
        :type row: int
        :param col: the column
        :type col: int
    '''
    cellDoubleClicked:pyTTkSignal
    '''
        This signal is emitted whenever a cell in the table is double clicked.
        The row and column specified is the cell that was double clicked.

        :param row: the row
        :type row: int
        :param col: the column
        :type col: int
    '''
    cellEntered:pyTTkSignal
    '''
        This signal is emitted when the mouse cursor enters a cell.
        The cell is specified by row and column.

        :param row: the row
        :type row: int
        :param col: the column
        :type col: int
    '''
    # self.cellPressed       = pyTTkSignal(int,int)
    currentCellChanged:pyTTkSignal
    '''
        This signal is emitted whenever the current cell changes.
        The cell specified by **prevRow** and **prevCol** is the cell that previously had the focus,
        the cell specified by **currRow** and **currCol** is the new current cell.

        :param currRow: the current row
        :type currRow: int
        :param currColumn: the current column
        :type currColumn: int
        :param prevRow: the previous row
        :type prevRow: int
        :param prevCol: the previous column
        :type prevCol: int
    '''

    classStyle = {
                'default':     {
                    'color':          TTkColor.RST,
                    'lineColor':      TTkColor.fg("#444444"),
                    'headerColor':    TTkColor.fg("#FFFFFF")+TTkColor.bg("#444444")+TTkColor.BOLD,
                    'hoverColor':     TTkColor.fg("#FFFF00")+TTkColor.bg("#0088AA")+TTkColor.BOLD,
                    'currentColor':   TTkColor.fg("#FFFF00")+TTkColor.bg("#0088FF")+TTkColor.BOLD,
                    'selectedColor':  TTkColor.bg("#0066AA"),
                    'separatorColor': TTkColor.fg("#555555")+TTkColor.bg("#444444")},
                'disabled':    {
                    'color':          TTkColor.fg("#888888"),
                    'lineColor':      TTkColor.fg("#888888"),
                    'headerColor':    TTkColor.fg("#888888"),
                    'hoverColor':     TTkColor.bg("#888888"),
                    'currentColor':   TTkColor.bg("#888888"),
                    'selectedColor':  TTkColor.fg("#888888"),
                    'separatorColor': TTkColor.fg("#888888")},
            }
    '''default style'''

    __slots__ = ( '_tableModel',
                  '_clipboard',
                  '_vHeaderSize', '_hHeaderSize',
                  '_showVSeparators', '_showHSeparators',
                  '_verticalHeader', '_horizontallHeader',
                  '_colsPos', '_rowsPos',
                  '_sortingEnabled',
                  '_dataPadding',
                  '_internal',
                  '_selected', '_selectedBase',
                  '_hSeparatorSelected', '_vSeparatorSelected',
                  '_hoverPos', '_dragPos', '_currentPos',
                  '_sortColumn', '_sortOrder',
                  '_fastCheck', '_guessDataEdit',
                  '_snapshot', '_snapshotId',
                  # Signals
                  # 'cellActivated',
                  'cellChanged',
                  'cellClicked', 'cellDoubleClicked',
                  'cellEntered', # 'cellPressed',
                  'currentCellChanged',
                  )

    def __init__(self, *,
                 tableModel:TTkAbstractTableModel=None,
                 vSeparator:bool=True,
                 hSeparator:bool=True,
                 vHeader:bool=True,
                 hHeader:bool=True,
                 sortingEnabled=False,
                 dataPadding=1,
                 **kwargs) -> None:
        '''
        :param tableModel: the model for the view to present.
        :type tableModel: :py:class:`TTkAbstractTableModel`

        :param vSeparator: show the vertical separators, defaults to True
        :type vSeparator: bool, optional

        :param hSeparator: show the horizontal separators, defaults to True
        :type hSeparator: bool, optional

        :param vHeader: show the vertical header, defaults to True
        :type vHeader: bool, optional

        :param hHeader: show the horizontal header, defaults to True
        :type hHeader: bool, optional

        :param sortingEnabled: enable the column sorting, defaults to False
        :type sortingEnabled: bool, optional

        :param dataPadding: the right column padding, defaults to 1
        :type dataPadding: int, optional
        '''
        # Signals
        # self.itemActivated     = pyTTkSignal(TTkTableWidgetItem, int)
        # self.itemChanged       = pyTTkSignal(TTkTableWidgetItem, int)
        # self.itemClicked       = pyTTkSignal(TTkTableWidgetItem, int)
        # self.itemDoubleClicked = pyTTkSignal(TTkTableWidgetItem, int)
        # self.itemExpanded      = pyTTkSignal(TTkTableWidgetItem)
        # self.itemCollapsed     = pyTTkSignal(TTkTableWidgetItem)

        # self.cellActivated     = pyTTkSignal(int,int)
        self.cellChanged       = pyTTkSignal(int,int)
        self.cellClicked       = pyTTkSignal(int,int)
        self.cellDoubleClicked = pyTTkSignal(int,int)
        self.cellEntered       = pyTTkSignal(int,int)
        # self.cellPressed       = pyTTkSignal(int,int)
        self.currentCellChanged = pyTTkSignal(int,int,int,int)
        # self.currentItemChanged(QTableWidgetItem *current, QTableWidgetItem *previous)

        self._fastCheck = True
        self._guessDataEdit = True

        self._clipboard = TTkClipboard()
        self._snapshot = []
        self._snapshotId = 0
        self._dataPadding = dataPadding
        self._sortingEnabled = sortingEnabled
        self._showHSeparators = hSeparator
        self._showVSeparators = vSeparator
        self._verticalHeader    = TTkHeaderView(visible=vHeader)
        self._horizontallHeader = TTkHeaderView(visible=hHeader)
        self._selected = None
        self._selectedBase = None
        self._hoverPos = None
        self._dragPos = None
        self._currentPos = None
        self._internal = {}
        self._hSeparatorSelected = None
        self._vSeparatorSelected = None
        self._sortColumn = -1
        self._sortOrder = TTkK.AscendingOrder
        self._tableModel = tableModel if tableModel else TTkTableModelList(data=[['']*10 for _ in range(10)])
        self._tableModel.dataChanged.connect(self.update)
        self._tableModel.modelChanged.connect(self._refreshLayout)
        super().__init__(**kwargs)
        self._refreshLayout()
        self.setMinimumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)
        # self._rootItem = TTkTableWidgetItem(expanded=True)
        # self.clear()
        self.viewChanged.connect(self._viewChangedHandler)
        self._verticalHeader.visibilityUpdated.connect(   self._headerVisibilityChanged)
        self._horizontallHeader.visibilityUpdated.connect(self._headerVisibilityChanged)

    @dataclass
    class _SnapItem():
        dataIndex: TTkModelIndex = None
        newData: object = None
        oldData: object = None

    def _saveSnapshot(self, items:list, currentPos:tuple[int]) -> None:
        self._snapshot = self._snapshot[:self._snapshotId] + [[currentPos]+items]
        self._snapshotId += 1

    def _restoreSnapshot(self, snapId:int,newData=True):
        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        self.clearSelection()
        for i in self._snapshot[snapId][1:]:
            row=i.dataIndex.row()
            col=i.dataIndex.col()
            self.setSelection(pos=(col,row),size=(1,1),flags=TTkK.TTkItemSelectionModel.Select)
            i.dataIndex.setData(i.newData if newData else i.oldData)
        cpsi:TTkModelIndex = self._snapshot[snapId][0]
        self._setCurrentCell(cpsi.row(),cpsi.col())
        self._moveCurrentCell(diff=(0,0))
        self.update()

    @pyTTkSlot()
    def undo(self) -> None:
        '''
        Undoes the last operation if undo is available.
        '''
        if self._snapshotId == 0: return
        self._snapshotId-=1
        self._restoreSnapshot(self._snapshotId, newData=False)

    @pyTTkSlot()
    def redo(self) -> None:
        '''
        Redoes the last operation if redo is available.
        '''
        if self._snapshotId >= len(self._snapshot): return
        self._restoreSnapshot(self._snapshotId, newData=True)
        self._snapshotId+=1

    def isUndoAvailable(self) -> bool:
        '''
        isUndoAvailable

        :return: bool
        '''
        return self._snapshotId > 0

    def isRedoAvailable(self) -> bool:
        '''
        isRedoAvailable

        :return: bool
        '''
        return self._snapshotId < len(self._snapshot)

    @pyTTkSlot()
    def copy(self) -> None:
        '''
        Copies any selected cells to the clipboard.
        '''
        data = []
        for row,line in enumerate(self._selected):
            dataLine = []
            for col,x in enumerate(line):
                if x:
                    dataLine.append((row,col,self._tableModel.data(row,col)))
            if dataLine:
                data.append(dataLine)
        clip = _ClipboardTable(data)
        # str(clip)
        self._clipboard.setText(clip)

    def _cleanSelectedContent(self):
        selected = [(_r,_c) for _r,_l in enumerate(self._selected) for _c,_v in enumerate(_l) if _v]
        mods = []
        for _row,_col in selected:
            mods.append((_row,_col,''))
        self._tableModel_setData(mods)
        self.update()

    @pyTTkSlot()
    def cut(self) -> None:
        '''
        Copies the selected ccells to the clipboard and deletes them from the table.
        '''
        self.copy()
        self._cleanSelectedContent()

    @pyTTkSlot()
    def paste(self) -> None:
        '''
        Pastes the text/cells from the clipboard into the table at the current cursor position.
        '''
        data = self._clipboard.text()
        self.pasteEvent(data)

    def pasteEvent(self, data:object):
        row,col = self._currentPos if self._currentPos else (0,0)
        if isinstance(data,_ClipboardTable):
            rows = self._tableModel.rowCount()
            cols = self._tableModel.columnCount()
            dataList = []
            linearData = [_item for _line in data.data() for _item in _line]
            minx,maxx = min(_a:=[_item[1] for _item in linearData]),max(_a)
            miny,maxy = min(_a:=[_item[0] for _item in linearData]),max(_a)
            for _dl in data.data():
                for item in _dl:
                    _r,_c,_d = item
                    _r+=row-miny
                    _c+=col-minx
                    if _r<rows and _c<cols:
                        dataList.append((_r,_c,_d))
            if dataList:
                self._tableModel_setData(dataList)
        elif isinstance(data,TTkString):
            self._tableModel_setData([(row,col,data)])
        else:
            self._tableModel_setData([(row,col,str(data))])
        self.update()
        return True

    def _tableModel_setData(self, dataList:list):
        # this is a helper to keep a snapshot copy if the data change
        snaps = []
        for row,col,newData in dataList:
            oldData   = self._tableModel.data(row=row,col=col)
            dataIndex = self._tableModel.index(row=row,col=col)
            if newData == oldData: continue
            self.cellChanged.emit(row,col)
            snaps.append(self._SnapItem(
                                dataIndex=dataIndex,
                                oldData=oldData,
                                newData=newData))
            self._tableModel.setData(row=row,col=col,data=newData)
        if snaps:
            row,col = self._currentPos if self._currentPos else (0,0)
            self._saveSnapshot(snaps,self._tableModel.index(row=row,col=col))

    @pyTTkSlot(bool)
    def setSortingEnabled(self, enable:bool) -> None:
        '''
        If enable is true, enables sorting for the table and immediately trigger a
        call to :meth:`sortByColumn`
        with the current sort section and order

        **Note**: Setter function for property sortingEnabled.

        :param enable: the availability of undo
        :type enable: bool
        '''
        if enable == self._sortingEnabled: return
        self._sortingEnabled = enable
        self.sortByColumn(self._sortColumn, self._sortOrder)

    def isSortingEnabled(self) -> bool:
        '''
        This property holds whether sorting is enabled
        If this property is true, sorting is enabled for the table.
        If this property is false, sorting is not enabled. The default value is false.

        **Note**: . Setting the property to true with :meth:`setSortingEnabled`
        immediately triggers a call to :meth:`sortByColumn`
        with the current sort section and order.

        :return: bool
        '''
        return self._sortingEnabled

    @pyTTkSlot(int, TTkK.SortOrder)
    def sortByColumn(self, column:int, order:TTkK.SortOrder) -> None:
        '''
        Sorts the model by the values in the given column and order.

        column may be -1, in which case no sort indicator will be shown and the model will return to its natural, unsorted order.
        Note that not all models support this and may even crash in this case.

        :param column: the column used for the sorting, -1 to keep the table unsorted
        :type column: bool

        :param order: the sort order
        :type order: :py:class:`TTkK.SortOrder`
        '''
        self._sortColumn = column
        self._sortOrder = order
        self._tableModel.sort(column,order)
        self.update()

    @pyTTkSlot()
    def _headerVisibilityChanged(self):
        showVH = self._verticalHeader.isVisible()
        showHH = self._horizontallHeader.isVisible()
        vhs = self._vHeaderSize if showVH else 0
        hhs = self._hHeaderSize if showHH else 0
        self.setPadding(hhs,0,vhs,0)
        self.viewChanged.emit()

    @pyTTkSlot()
    def _refreshLayout(self):
        self._selected = None
        self._selectedBase = None
        self._hoverPos = None
        self._dragPos = None
        self._currentPos = None
        self._hSeparatorSelected = None
        self._vSeparatorSelected = None
        self._sortColumn = -1
        self._sortOrder = TTkK.AscendingOrder
        self._snapshot = []
        self._snapshotId = 0
        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        self._vHeaderSize = vhs = 1+max(len(self._tableModel.headerData(_p, TTkK.VERTICAL)) for _p in range(rows) )
        self._hHeaderSize = hhs = 1
        self.setPadding(hhs,0,vhs,0)
        if self._showVSeparators:
            self._colsPos  = [(1+x)*11 for x in range(cols)]
        else:
            self._colsPos  = [(1+x)*10 for x in range(cols)]
        if self._showHSeparators:
            self._rowsPos     = [1+x*2  for x in range(rows)]
        else:
            self._rowsPos     = [1+x    for x in range(rows)]
        # self._selectedBase = sb =  [False]*cols
        # self._selected = [sb]*rows
        self.clearSelection()
        self.viewChanged.emit()

    # Overridden function
    def viewFullAreaSize(self) -> tuple[int, int]:
        showVH = self._verticalHeader.isVisible()
        showHH = self._horizontallHeader.isVisible()
        hhs = self._hHeaderSize if showHH else 0
        vhs = self._vHeaderSize if showVH else 0
        w = vhs+self._colsPos[-1]+1
        h = hhs+self._rowsPos[-1]+1
        return w,h

    def clearSelection(self) -> None:
        '''
        Deselects all selected items.
        The current index will not be changed.
        '''
        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        self._selected = [[False]*cols for _ in range(rows)]
        self.update()

    def selectAll(self) -> None:
        '''
        Selects all items in the view.
        This function will use the selection behavior set on the view when selecting.
        '''
        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        flagFunc = self._tableModel.flags
        cmp = TTkK.ItemFlag.ItemIsSelectable
        self._selected = [[cmp==(cmp&flagFunc(_r,_c)) for _c in range(cols)] for _r in range(rows)]
        self.update()

    def setSelection(self, pos:tuple[int,int], size:tuple[int,int], flags:TTkK.TTkItemSelectionModel) -> None:
        '''
        Selects the items within the given rect and in accordance with the specified selection flags.

        :param pos: the x,y position of the rect
        :type pos: tuple[int,int]
        :param size: the width,height of the rect used for the selection
        :type size: tuple[int,int]
        :param flags: the selection model used (i.e. :py:class:`TTkItemSelectionModel.Select`)
        :type flags: :py:class:`TTkItemSelectionModel`
        '''
        x,y = pos
        w,h = size
        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        flagFunc = self._tableModel.flags
        cmp = TTkK.ItemFlag.ItemIsSelectable
        if flags & (TTkK.TTkItemSelectionModel.Clear|TTkK.TTkItemSelectionModel.Deselect):
            for line in self._selected[y:y+h]:
                line[x:x+w]=[False]*w
        elif flags & TTkK.TTkItemSelectionModel.Select:
            for _r, line in enumerate(self._selected[y:y+h],y):
                line[x:x+w]=[cmp==(cmp&flagFunc(_r,_c)) for _c in range(x,min(x+w,cols))]
        self.update()

    def selectRow(self, row:int) -> None:
        '''
        Selects the given row in the table view

        :param row: the row to be selected
        :type row: int
        '''
        cols = self._tableModel.columnCount()
        cmp = TTkK.ItemFlag.ItemIsSelectable
        flagFunc = self._tableModel.flags
        self._selected[row] = [cmp==(cmp&flagFunc(row,col)) for col in range(cols)]
        self.update()

    def selectColumn(self, col:int) -> None:
        '''
        Selects the given column in the table view

        :param col: the column to be selected
        :type col: int
        '''
        cmp = TTkK.ItemFlag.ItemIsSelectable
        flagFunc = self._tableModel.flags
        for row,line in enumerate(self._selected):
            line[col] = cmp==(cmp&flagFunc(row,col))
        self.update()

    def unselectRow(self, row:int) -> None:
        '''
        Unselects the given row in the table view

        :param row: the row to be unselected
        :type row: int
        '''
        cols = self._tableModel.columnCount()
        self._selected[row] = [False]*cols
        self.update()

    def unselectColumn(self, column:int) -> None:
        '''
        Unselects the given column in the table view

        :param column: the column to be unselected
        :type column: int
        '''
        for line in self._selected:
            line[column] = False
        self.update()

    @pyTTkSlot()
    def _viewChangedHandler(self) -> None:
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)
        self.update()

    def rowCount(self) -> int:
        '''
        Returns the number of rows.

        :return: int
        '''
        return self._tableModel.rowCount()

    def currentRow(self) -> int:
        '''
        Returns the row of the current item.

        :return: int
        '''
        if _cp := self._currentPos:
            return _cp[0]
        return 0

    def columnCount(self) -> int:
        '''
        Returns the number of columns.

        :return: int
        '''
        return self._tableModel.columnCount()

    def currentColumn(self) -> int:
        '''
        Returns the column of the current item.

        :return: int
        '''
        if _cp := self._currentPos:
            return _cp[1]
        return 0

    def verticalHeader(self) -> TTkHeaderView:
        '''
        Returns the table view's vertical header.

        :return: :py:class:`TTkHeaderView`
        '''
        return self._verticalHeader

    def horizontalHeader(self) -> TTkHeaderView:
        '''
        Returns the table view's horizontal header.

        :return: :py:class:`TTkHeaderView`
        '''
        return self._horizontallHeader

    def hSeparatorVisibility(self) -> bool:
        '''
        Returns the visibility status of the horizontal separator

        :return: bool
        '''
        return self._showHSeparators
    def vSeparatorVisibility(self) -> bool:
        '''
        Returns the visibility status of the vertical separator

        :return: bool
        '''
        return self._showVSeparators

    def setHSeparatorVisibility(self, visibility:bool) -> None:
        '''
        Set the the visibility of the horizontal separators (lines)

        ::

                 Customer Id      First Name  Last Name   Company
            1  │ DD37Cf93aecA6Dc  Sheryl      Baxter      Rasmussen Group
            ╾╌╌┼───────────────────────────────────────────────────────────
            2  │ 1Ef7b82A4CAAD10  Preston     Lozano      Vega-Gentry
            ╾╌╌┼───────────────────────────────────────────────────────────
            3  │ 6F94879bDAfE5a6  Roy         Berry       Murillo-Perry
            ╾╌╌┼───────────────────────────────────────────────────────────

        :param visibility: the visibility status
        :type visibility: bool
        '''
        if self._showHSeparators == visibility: return
        self._showHSeparators = visibility
        if visibility:
            self._rowsPos = [v+i for i,v in enumerate(self._rowsPos,1)]
        else:
            self._rowsPos = [v-i for i,v in enumerate(self._rowsPos,1)]
        self.viewChanged.emit()

    def setVSeparatorVisibility(self, visibility:bool):
        '''
        Set the the visibility of the vertical separators (lines)

        ::

                 Customer Id     ╿First Name ╿Last Name   ╿Company                     ╿
            1  │ DD37Cf93aecA6Dc │Sheryl     │Baxter      │Rasmussen Group             │
            2  │ 1Ef7b82A4CAAD10 │Preston    │Lozano      │Vega-Gentry                 │
            3  │ 6F94879bDAfE5a6 │Roy        │Berry       │Murillo-Perry               │
            4  │ 5Cef8BFA16c5e3c │Linda      │Olsen       │Dominguez, Mcmillan and Don │
            5  │ 053d585Ab6b3159 │Joanna     │Bender      │Martin, Lang and Andrade    │
            6  │ 2d08FB17EE273F4 │Aimee      │Downs       │Steele Group                │

        :param visibility: the visibility status
        :type visibility: bool
        '''
        if self._showVSeparators == visibility: return
        self._showVSeparators = visibility
        if visibility:
            self._colsPos = [v+i for i,v in enumerate(self._colsPos,1)]
        else:
            self._colsPos = [v-i for i,v in enumerate(self._colsPos,1)]
        self.viewChanged.emit()

    def model(self) -> TTkAbstractTableModel:
        '''
        Returns the model that this view is presenting.

        :return: :py:class:`TTkAbstractTableModel`
        '''
        return self._tableModel

    def setModel(self, model:TTkAbstractTableModel) -> None:
        '''
        Sets the model for the view to present.

        :param model:
        :type model: :py:class:`TTkAbstractTableModel`
        '''
        self._tableModel.dataChanged.disconnect(self.update)
        self._tableModel = model
        self._tableModel.dataChanged.connect(self.update)
        self._refreshLayout()

    def focusOutEvent(self) -> None:
        self._hSeparatorSelected = None
        self._vSeparatorSelected = None

    def leaveEvent(self, evt:TTkMouseEvent) -> bool:
        self._hoverPos = None
        self.update()
        return super().leaveEvent(evt)

    @pyTTkSlot(int,int)
    def setColumnWidth(self, column:int, width: int) -> None:
        '''
        Sets the width of the given column.

        :param column: the column
        :type column: int
        :param width: its width
        :type width: int
        '''
        i = column
        prevPos = self._colsPos[i-1] if i>0 else -1
        if self._showVSeparators:
            newPos = prevPos + width + 1
        else:
            newPos = prevPos + width
        oldPos = self._colsPos[i]
        diff    = newPos-oldPos
        for ii in range(i,len(self._colsPos)):
            self._colsPos[ii] += diff
        self.viewChanged.emit()
        self.update()

    def _columnContentsSize(self, column:int) -> int:
        def _wid(_c):
            txt = self._tableModel.ttkStringData(_c, column)
            return max(t.termWidth() for t in txt.split('\n'))
        rows = self._tableModel.rowCount()
        if self._fastCheck:
            w,h = self.size()
            row,_ = self._findCell(w//2, h//2, False)
            rowa,rowb = max(0,row-100), min(row+100,rows)
        else:
            rowa,rowb = 0,rows
        return max(_wid(i) for i in range(rowa,rowb))+self._dataPadding

    @pyTTkSlot(int)
    def resizeColumnToContents(self, column:int) -> None:
        '''
        Resizes the given column based on the size hints of the delegate used to render each item in the column.

        :param column: the column to be resized
        :type column: int
        '''
        self.setColumnWidth(column, self._columnContentsSize(column))

    @pyTTkSlot()
    def resizeColumnsToContents(self) -> None:
        '''
        Resizes all columns based on the size hints of the delegate used to render each item in the columns.
        '''
        _d = 1 if self._showVSeparators else 0
        cols = self._tableModel.columnCount()
        pos = -1
        for _c in range(cols):
            pos += _d+self._columnContentsSize(_c)
            self._colsPos[_c] = pos
        self.viewChanged.emit()
        self.update()

    @pyTTkSlot(int,int)
    def setRowHeight(self, row:int, height: int) -> None:
        '''
        Sets the height of the given row.

        :param row: the row
        :type row: int
        :param height: its height
        :type height: int
        '''
        i = row
        prevPos = self._rowsPos[i-1] if i>0 else -1
        if self._showHSeparators:
            newPos = prevPos + height + 1
        else:
            newPos = prevPos + height
        oldPos = self._rowsPos[i]
        diff    = newPos-oldPos
        for ii in range(i,len(self._rowsPos)):
            self._rowsPos[ii] += diff
        self.viewChanged.emit()
        self.update()

    def _rowContentsSize(self, row:int) -> int:
        def _hei(_c):
            txt = self._tableModel.ttkStringData(row, _c)
            return len(txt.split('\n'))
        cols = self._tableModel.columnCount()
        if self._fastCheck:
            w,h = self.size()
            _,col = self._findCell(w//2, h//2, False)
            cola,colb = max(0,col-30), min(col+30,cols)
        else:
            cola,colb = 0,cols
        return max(_hei(i) for i in range(cola,colb))

    @pyTTkSlot(int)
    def resizeRowToContents(self, row:int) -> None:
        '''
        Resizes the given row based on the size hints of the delegate used to render each item in the row.

        :param row: the row to be resized
        :type row: int
        '''
        self.setRowHeight(row, self._rowContentsSize(row))

    @pyTTkSlot()
    def resizeRowsToContents(self) -> None:
        '''
        Resizes all rows based on the size hints of the delegate used to render each item in the rows.
        '''
        rows = self._tableModel.rowCount()
        _d = 1 if self._showHSeparators else 0
        pos = -1
        for _r in range(rows):
            pos += _d + self._rowContentsSize(_r)
            self._rowsPos[_r] = pos
        self.viewChanged.emit()
        self.update()

    def _findCell(self, x, y, headers):
        showVH = self._verticalHeader.isVisible()
        showHH = self._horizontallHeader.isVisible()
        hhs = self._hHeaderSize if showHH else 0
        vhs = self._vHeaderSize if showVH else 0
        ox, oy = self.getViewOffsets()
        rp = self._rowsPos
        cp = self._colsPos

        row = 0
        col = 0

        if headers and y<hhs:
            row = -1
        else:
            y += oy-hhs
            for row,py in enumerate(rp):
                if py>=y:
                    break

        if headers and x<vhs:
            col = -1
        else:
            x += ox-vhs
            for col,px in enumerate(cp):
                if px>=x:
                    break

        return row,col

    def _editStr(self, x,y,w,h, row, col, data):
        _te = TTkTextEdit(
                    parent=self, pos=(x, y), size=(w,h),
                    readOnly=False, wrapMode=TTkK.NoWrap)
        _tev = _te.textEditView()
        _te.setText(data)
        _te.textCursor().movePosition(operation=TTkTextCursor.EndOfLine)
        _te.setFocus()

        @pyTTkSlot(bool)
        def _processClose(change):
            if change:
                self.focusChanged.disconnect(_processClose)
                txt = _te.toRawText()
                val = str(txt) if txt.isPlainText() else txt
                self._tableModel_setData([(row,col,val)])
                self.update()
                _te.close()
                self.setFocus()

        # Override the key event
        _ke = _tev.keyEvent
        _doc = _tev.document()
        _cur = _tev.textCursor()
        def _keyEvent(evt):
            if ( evt.type == TTkK.SpecialKey):
                _line = _cur.anchor().line
                _pos  = _cur.anchor().pos
                _lineCount = _doc.lineCount()
                # _lineLen
                if evt.mod==TTkK.NoModifier:
                    if evt.key == TTkK.Key_Enter:
                        # self.enterPressed.emit(True)
                        self._moveCurrentCell(diff=(0,+1))
                        _processClose(True)
                        return True
                    elif evt.key == TTkK.Key_Up:
                        if _line == 0:
                            self._moveCurrentCell(diff=(0,-1))
                            _processClose(True)
                            return True
                    elif evt.key == TTkK.Key_Down:
                        if _lineCount == 1:
                            self._moveCurrentCell(diff=(0,+1))
                            _processClose(True)
                            return True
                    elif evt.key == TTkK.Key_Left:
                        if _pos == _line == 0:
                            self._moveCurrentCell(diff=(-1, 0))
                            _processClose(True)
                            return True
                    elif evt.key == TTkK.Key_Right:
                        if _lineCount == 1 and _pos==len(_doc.toPlainText()):
                            self._moveCurrentCell(diff=(+1, 0))
                            _processClose(True)
                            return True
                elif ( evt.type == TTkK.SpecialKey and
                       evt.mod==TTkK.ControlModifier|TTkK.AltModifier and
                       evt.key == TTkK.Key_M ):
                    evt.mod = TTkK.NoModifier
                    evt.key = TTkK.Key_Enter
            return _ke(evt)
        _tev.keyEvent = _keyEvent

        # _tev.enterPressed.connect(_processClose)
        self.focusChanged.connect(_processClose)

    def _editNum(self, x,y,w,h, row, col, data):
        _sb = TTkSpinBox(
                    parent=self, pos=(x, y), size=(w,1),
                    minimum=-1000000, maximum=1000000,
                    value=data)
        _sb.setFocus()

        @pyTTkSlot(bool)
        def _processClose(change):
            if change:
                self.focusChanged.disconnect(_processClose)
                val = _sb.value()
                self._tableModel_setData([(row,col,val)])
                self.update()
                _sb.close()
                self.setFocus()

        # Override the key event
        _ke = _sb.keyEvent
        def _keyEvent(evt):
            if ( evt.type == TTkK.SpecialKey):
                if evt.mod==TTkK.NoModifier:
                    if evt.key == TTkK.Key_Enter:
                        self._moveCurrentCell( 0,+1)
                        _processClose(True)
                        return True
            return _ke(evt)
        _sb.keyEvent = _keyEvent

        self.focusChanged.connect(_processClose)

    def _editTTkString(self, x,y,w,h, row, col, data):
        _tp = TTkTextPicker(
                    parent=self, pos=(x, y), size=(w,h),
                    text=data, autoSize=False, wrapMode=TTkK.NoWrap)

        _tp.setFocus()

        @pyTTkSlot(bool)
        def _processClose(change):
            if change:
                self.focusChanged.disconnect(_processClose)
                txt = _tp.getTTkString()
                self._tableModel_setData([(row,col,txt)])
                self.update()
                _tp.close()
                self.setFocus()

        self.focusChanged.connect(_processClose)

    def _editCell(self, row:int, col:int, richEditSupport:bool=True) -> None:
        if not (self._tableModel.flags(row=row,col=col) & TTkK.ItemFlag.ItemIsEditable):
            return
        showHS = self._showHSeparators
        showVS = self._showVSeparators
        rp = self._rowsPos
        cp = self._colsPos
        xa,xb = 1+cp[col-1] if col>0 else 0, cp[col] + (0 if showVS else 1)
        ya,yb = 1+rp[row-1] if row>0 else 0, rp[row] + (0 if showHS else 1)

        # Mark only the current cell as aselected
        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        self.clearSelection()
        self.setSelection(pos=(col,row),size=(1,1),flags=TTkK.TTkItemSelectionModel.Select)

        data = self._tableModel.data(row, col)
        if type(data) is str:
            self._editStr(xa,ya,xb-xa,yb-ya,row,col,data)
        elif type(data) in [int,float]:
            self._editNum(xa,ya,xb-xa,yb-ya,row,col,data)
        else:
            data = self._tableModel.ttkStringData(row, col)
            if richEditSupport:
                self._editTTkString(xa,ya,xb-xa,yb-ya,row,col,data)
            else:
                self._editStr(xa,ya,xb-xa,yb-ya,row,col,data)

    def _setCurrentCell(self, currRow:int, currCol:int) -> None:
        prevRow,prevCol = self._currentPos if self._currentPos else (0,0)
        self._currentPos = (currRow,currCol)
        if (currRow,currRow)!=(prevRow,prevCol):
            self.currentCellChanged.emit(currRow,currCol,prevRow,prevCol)

    def _moveCurrentCell(self, col=0, row=0, borderStop=True, diff=None):
        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()

        if diff:
            row,col = self._currentPos if self._currentPos else (0,0)
            dc,dr = diff
            row+=dr
            col+=dc

        if borderStop:
            row = max(0,min(row, rows-1))
            col = max(0,min(col, cols-1))
        else:
            if col >= cols: col=0      ; row+=1
            if col < 0:     col=cols-1 ; row-=1
            if row >= rows: row=0
            if row < 0:     row=rows-1
        self._setCurrentCell(row,col)
        # move the offset to include the cell
        w,h = self.size()
        ox, oy = self.getViewOffsets()
        showVH = self._verticalHeader.isVisible()
        showHH = self._horizontallHeader.isVisible()
        hhs = self._hHeaderSize if showHH else 0
        vhs = self._vHeaderSize if showVH else 0
        cxa,cxb = self._colsPos[col-1] if col else 0, self._colsPos[col]
        cya,cyb = self._rowsPos[row-1] if row else 0, self._rowsPos[row]
        if w+ox-vhs < cxb: ox=cxb+vhs-w
        if ox > cxa: ox=cxa
        if h+oy-hhs < cyb: oy=cyb+hhs-h
        if oy > cya: oy=cya
        self.viewMoveTo(ox,oy)
        self.update()

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        # rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        if self._currentPos:
            row,col = self._currentPos
        else:
            row,col = 0,0
        if evt.type == TTkK.SpecialKey:
            if evt.mod==TTkK.ControlModifier:
                if   evt.key == TTkK.Key_Z:  self.undo()
                elif evt.key == TTkK.Key_Y:  self.redo()
                elif evt.key == TTkK.Key_C:  self.copy()
                elif evt.key == TTkK.Key_V:  self.paste()
                elif evt.key == TTkK.Key_X:  self.cut()
            elif evt.key == TTkK.Key_Tab: # Process Next/Prev
                if   evt.mod == TTkK.NoModifier:    self._moveCurrentCell(col=col+1, row=row, borderStop=False)
                elif evt.mod == TTkK.ShiftModifier: self._moveCurrentCell(col=col-1, row=row, borderStop=False)
            elif evt.key == TTkK.Key_PageDown:
                _,h = self.size()
                rp=self._rowsPos[row]
                for dy,rh in enumerate(self._rowsPos[row:]):
                    if rh-rp >= h: break
                self._moveCurrentCell(col=col, row=row+dy, borderStop=True)
            elif evt.key == TTkK.Key_PageUp:
                _,h = self.size()
                rp=self._rowsPos[row]
                for dy,rh in enumerate(self._rowsPos[row::-1]):
                    if rp-rh >= h: break
                self._moveCurrentCell(col=col, row=row-dy, borderStop=True)
            elif evt.key == TTkK.Key_Home: self._moveCurrentCell(col=0,    row=row, borderStop=True)
            elif evt.key == TTkK.Key_End:  self._moveCurrentCell(col=cols, row=row, borderStop=True)
            elif evt.mod==TTkK.NoModifier:
                if   evt.key == TTkK.Key_Up:    self._moveCurrentCell(col=col  , row=row-1, borderStop=True)
                elif evt.key == TTkK.Key_Down:  self._moveCurrentCell(col=col  , row=row+1, borderStop=True)
                elif evt.key == TTkK.Key_Left:  self._moveCurrentCell(col=col-1, row=row  , borderStop=True)
                elif evt.key == TTkK.Key_Right: self._moveCurrentCell(col=col+1, row=row  , borderStop=True)
                elif evt.key == TTkK.Key_Enter:
                    if (self._tableModel.flags(row=row,col=col) & TTkK.ItemFlag.ItemIsEditable):
                        self._editCell(row,col,richEditSupport=False)
                    else:
                        self._moveCurrentCell(col=col  , row=row+1, borderStop=False)
                elif evt.key in (TTkK.Key_Delete, TTkK.Key_Backspace):
                    self._cleanSelectedContent()
                self.update()
            return True
        else:
            if (self._tableModel.flags(row=row,col=col) & TTkK.ItemFlag.ItemIsEditable):
                self._tableModel_setData([(row,col,evt.key)])
                self._editCell(row,col,richEditSupport=False)
        return True


    def mouseDoubleClickEvent(self, evt:TTkMouseEvent) -> bool:
        x,y = evt.x, evt.y
        ox, oy = self.getViewOffsets()
        showHS = self._showHSeparators
        showVS = self._showVSeparators
        showVH = self._verticalHeader.isVisible()
        showHH = self._horizontallHeader.isVisible()
        hhs = self._hHeaderSize if showHH else 0
        vhs = self._vHeaderSize if showVH else 0

        self._hSeparatorSelected = None
        self._vSeparatorSelected = None

        rp = self._rowsPos
        cp = self._colsPos

        # Handle Header Events
        # And return if handled
        # This is important to handle the header selection in the next part
        if showVS and y < hhs:
            _x = x+ox-vhs
            for i, c in enumerate(self._colsPos):
                if _x == c:
                    # I-th separator selected
                    self.resizeColumnToContents(i)
                    return True
            # return True
        elif showHS and x < vhs:
            _y = y+oy-hhs
            for i, r in enumerate(self._rowsPos):
                if _y == r:
                    # I-th separator selected
                    # I-th separator selected
                    self.resizeRowToContents(i)
                    return True

        row,col = self._findCell(x,y, headers=False)
        self.cellDoubleClicked.emit(row,col)
        self._editCell(row,col)
        return True

    def mouseMoveEvent(self, evt:TTkMouseEvent) -> bool:
        x,y = evt.x,evt.y
        ox, oy = self.getViewOffsets()
        showHS = self._showHSeparators
        showVS = self._showVSeparators
        showVH = self._verticalHeader.isVisible()
        showHH = self._horizontallHeader.isVisible()
        hhs = self._hHeaderSize if showHH else 0
        vhs = self._vHeaderSize if showVH else 0

        self._hoverPos = (row,col) = self._findCell(x,y, headers=True)
        if showVS and row==-1:
            _x = x+ox-vhs
            for i, c in enumerate(self._colsPos):
                if _x == c:
                    # Over the I-th separator
                    self._hoverPos = None
                    self.update()
                    return True
        if showHS and col==-1:
            _y = y+oy-hhs
            for i, r in enumerate(self._rowsPos):
                if _y == r:
                    # Over the I-th separator
                    self._hoverPos = None
                    self.update()
                    return True
        if row>=0 and col>>0:
            self.cellEntered.emit(row,col)
        self.update()
        return True

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        x,y = evt.x, evt.y
        ox, oy = self.getViewOffsets()
        showHS = self._showHSeparators
        showVS = self._showVSeparators
        showVH = self._verticalHeader.isVisible()
        showHH = self._horizontallHeader.isVisible()
        hhs = self._hHeaderSize if showHH else 0
        vhs = self._vHeaderSize if showVH else 0

        self._hSeparatorSelected = None
        self._vSeparatorSelected = None

        # Handle Header Events
        # And return if handled
        # This is important to handle the header selection in the next part
        if y < hhs:
            _x = x+ox-vhs
            for i, c in enumerate(self._colsPos):
                if showVS and _x == c:
                    # I-th separator selected
                    self._hSeparatorSelected = i
                    self.update()
                    return True
                elif self._sortingEnabled and _x == c-(1 if showVS else 0) : # Pressed the sort otder icon
                    if self._sortColumn == i:
                        order = TTkK.SortOrder.DescendingOrder if self._sortOrder==TTkK.SortOrder.AscendingOrder else TTkK.SortOrder.AscendingOrder
                    else:
                        order = TTkK.SortOrder.AscendingOrder
                    self.sortByColumn(i,order)
                    return True
        elif showHS and x < vhs:
            _y = y+oy-hhs
            for i, r in enumerate(self._rowsPos):
                if _y == r:
                    # I-th separator selected
                    self._vSeparatorSelected = i
                    self.update()
                    return True

        row,col = self._findCell(x,y, headers=True)
        if not row==col==-1:
            self._dragPos = [(row,col),(row,col)]
        _ctrl = evt.mod==TTkK.ControlModifier
        if row==col==-1:
            # Corner Press
            # Select Everything
            self.selectAll()
        elif col==-1:
            # Row select
            flagFunc = self._tableModel.flags
            cmp = TTkK.ItemFlag.ItemIsSelectable
            state = all(_sel for i,_sel in enumerate(self._selected[row]) if flagFunc(row,i)&cmp)
            if not _ctrl:
                self.clearSelection()
            if state:
                self.unselectRow(row)
            else:
                self.selectRow(row)
        elif row==-1:
            # Col select
            flagFunc = self._tableModel.flags
            cmp = TTkK.ItemFlag.ItemIsSelectable
            state = all(_sel[col] for i,_sel in enumerate(self._selected) if flagFunc(i,col)&cmp)
            if not _ctrl:
                self.clearSelection()
            if state:
                self.unselectColumn(col)
            else:
                self.selectColumn(col)
        else:
            # Cell Select
            self.cellClicked.emit(row,col)
            # self.cellPressed.emit(row,col)
            self._setCurrentCell(row,col)
            self.setSelection(pos   = (col,row), size = (1,1),
                              flags = TTkK.TTkItemSelectionModel.Clear if (self._selected[row][col] and  _ctrl) else TTkK.TTkItemSelectionModel.Select)
        self._hoverPos = None
        self.update()
        return True

    def mouseDragEvent(self, evt:TTkMouseEvent) -> bool:
        #     columnPos       (Selected = 2)
        #         0       1        2          3   4
        #     ----|-------|--------|----------|---|
        #     Mouse (Drag) Pos
        #                             ^
        #     I consider at least 4 char (3+1) as spacing
        #     Min Selected Pos = (Selected+1) * 4
        x,y = evt.x, evt.y
        ox, oy = self.getViewOffsets()
        showVH = self._verticalHeader.isVisible()
        showHH = self._horizontallHeader.isVisible()
        hhs = self._hHeaderSize if showHH else 0
        vhs = self._vHeaderSize if showVH else 0
        if self._dragPos and not self._hSeparatorSelected and not self._vSeparatorSelected:
            self._dragPos[1] = self._findCell(x,y, headers=False)
            self.update()
            return True
        if self._hSeparatorSelected is not None:
            x += ox-vhs
            ss = self._hSeparatorSelected
            pos = max((ss+1)*4, x)
            diff = pos - self._colsPos[ss]
            # Align the previous Separators if pushed
            for i in range(ss):
                self._colsPos[i] = min(self._colsPos[i], pos-(ss-i)*4)
            # Align all the other Separators relative to the selection
            for i in range(ss, len(self._colsPos)):
                self._colsPos[i] += diff
            # self._alignWidgets()
            self.viewChanged.emit()
            self.update()
            return True
        if self._vSeparatorSelected is not None:
            y += oy-hhs
            ss = self._vSeparatorSelected
            pos = max((ss+1)*2-1, y)
            diff = pos - self._rowsPos[ss]
            # Align the previous Separators if pushed
            for i in range(ss):
                self._rowsPos[i] = min(self._rowsPos[i], pos-(ss-i)*2)
            # Align all the other Separators relative to the selection
            for i in range(ss, len(self._rowsPos)):
                self._rowsPos[i] += diff
            # self._alignWidgets()
            self.viewChanged.emit()
            self.update()
            return True
        return False

    def mouseReleaseEvent(self, evt:TTkMouseEvent) -> bool:
        if self._dragPos:
            rows = self._tableModel.rowCount()
            cols = self._tableModel.columnCount()
            state = True
            (rowa,cola),(rowb,colb) = self._dragPos

            if evt.mod==TTkK.ControlModifier:
                # Pick the status to be applied to the selection if CTRL is Pressed
                # In case of line/row selection I choose the element 0 of that line
                state = self._selected[max(0,rowa)][max(0,cola)]
            else:
                # Clear the selection if no ctrl has been pressed
                self.clearSelection()

            if rowa == -1:
                cola,colb=min(cola,colb),max(cola,colb)
                rowa,rowb=0,rows-1
            elif cola == -1:
                rowa,rowb=min(rowa,rowb),max(rowa,rowb)
                cola,colb=0,cols-1
            else:
                cola,colb=min(cola,colb),max(cola,colb)
                rowa,rowb=min(rowa,rowb),max(rowa,rowb)

            self.setSelection(pos   = (cola,rowa), size = (colb-cola+1,rowb-rowa+1),
                              flags = TTkK.TTkItemSelectionModel.Select if state else TTkK.TTkItemSelectionModel.Clear)

        self._hoverPos = None
        self._dragPos = None
        self.update()
        return True

    #
    #   -1  X
    #        <-(0,0)->│<-(1,0)->│<-(2,0)->│<-(3,0)->│
    #    1   ─────────┼─────────┼─────────┼─────────┼
    #        <-(0,1)->│<-(1,1)->│<-(2,1)->│<-(3,1)->│
    #    3   ─────────┼─────────┼─────────┼─────────┼
    #        <-(0,2)->│<-(1,2)->│<-(2,2)->│<-(3,2)->│
    #    4   ─────────┼─────────┼─────────┼─────────┼
    #        <-(0,3)->│<-(1,3)->│<-(2,3)->│<-(3,3)->│ h-cell = 5 = 10-(4+1)
    #                 │ abc     │         │         │
    #                 │ de      │         │         │
    #                 │         │         │         │
    #                 │         │         │         │
    #   10   ─────────┼─────────┼─────────┼─────────┼
    #        <-(0,4)->│<-(1,4)->│<-(2,4)->│<-(3,4)->│
    #   12   ─────────┼─────────┼─────────┼─────────┼
    #        <-(0,5)->│<-(1,5)->│<-(2,5)->│<-(3,5)->│
    #   14   ─────────┼─────────┼─────────┼─────────┼

    #   -1   X
    #    0   <-(0,0)->│<-(1,0)->│<-(2,0)->│<-(3,0)->│
    #    1   <-(0,1)->│<-(1,1)->│<-(2,1)->│<-(3,1)->│
    #    2   <-(0,2)->│<-(1,2)->│<-(2,2)->│<-(3,2)->│
    #    3   <-(0,3)->│<-(1,3)->│<-(2,3)->│<-(3,3)->│ h-cell = 5 = 10-(4+1)
    #                 │ abc     │         │         │
    #                 │ de      │         │         │
    #                 │         │         │         │
    #                 │         │         │         │
    #    8   <-(0,4)->│<-(1,4)->│<-(2,4)->│<-(3,4)->│
    #    9   <-(0,5)->│<-(1,5)->│<-(2,5)->│<-(3,5)->│
    #
    def paintEvent(self, canvas) -> None:
        style = self.currentStyle()

        color:TTkColor= style['color']
        lineColor:TTkColor= style['lineColor']
        headerColor:TTkColor= style['headerColor']
        hoverColor:TTkColor= style['hoverColor']
        currentColor:TTkColor= style['currentColor']
        selectedColor:TTkColor= style['selectedColor']
        separatorColor:TTkColor= style['separatorColor']

        selectedColorInv:TTkColor = selectedColor.background().invertFgBg()

        vHSeparator = TTkString('▐', separatorColor)

        ox,oy = self.getViewOffsets()
        w,h = self.size()

        rows = self._tableModel.rowCount()
        cols = self._tableModel.columnCount()
        rp = self._rowsPos
        cp = self._colsPos

        showVH = self._verticalHeader.isVisible()
        showHH = self._horizontallHeader.isVisible()
        hhs = self._hHeaderSize if showHH else 0
        vhs = self._vHeaderSize if showVH else 0

        showHS = self._showHSeparators
        showVS = self._showVSeparators

        sliceCol=list(zip([-1]+cp,cp))
        sliceRow=list(zip([-1]+rp,rp))

        # NOTE: Add Color Cache
        # NOTE: Add Select/Hover Cache
        # Draw cell and right/bottom corner

        # Find First/Last displayed Rows
        rowa, rowb = 0,rows-1
        for row in range(rows):
            ya,yb = sliceRow[row]
            ya,yb = ya+hhs-oy, yb+hhs-oy
            if ya>h  :
                rowb = row
                break
            if yb<hhs:
                rowa = row
                continue
        # Use this in range
        rrows = (rowa,rowb+1)

        # Find First/Last displayed Cols
        cola, colb = 0, cols-1
        for col in range(cols):
            xa,xb = sliceCol[col]
            xa,xb = xa+vhs-ox, xb+vhs-ox
            if xa>w  :
                colb = col
                break
            if xb<vhs:
                cola = col
                continue
        # Use this in range
        rcols = (cola,colb+1)

        # Cache Cells
        _cellsCache   = []
        _colorCache2d = [[None]*(colb+1-cola) for _ in range(rowb+1-rowa)]
        for row in range(*rrows):
            ya,yb = sliceRow[row]
            if showHS:
                ya,yb = ya+hhs-oy+1, yb+hhs-oy
            else:
                ya,yb = ya+hhs-oy+1, yb+hhs-oy+1
            if ya>h  : break
            if yb<hhs: continue
            rowColor = color.mod(0,row)
            for col in range(*rcols):
                xa,xb = sliceCol[col]
                if showVS:
                    xa,xb = xa+vhs-ox+1, xb+vhs-ox
                else:
                    xa,xb = xa+vhs-ox+1, xb+vhs-ox+1
                if xa>w  : break
                if xb<vhs: continue
                cellColor = (
                    currentColor if self._currentPos == (row,col) else
                    hoverColor if self._hoverPos in [(row,col),(-1,col),(row,-1),(-1,-1)] else
                    selectedColor if self._selected[row][col] else
                    rowColor )
                _colorCache2d[row-rowa][col-cola] = cellColor
                _cellsCache.append([row,col,xa,xb,ya,yb,cellColor])

        def _drawCellContent(_col,_row,_xa,_xb,_ya,_yb,_color):
                txt = self._tableModel.ttkStringData(_row, _col)
                if _color != TTkColor.RST:
                    txt = txt.completeColor(_color)
                for i,line in enumerate(txt.split('\n')):
                    y = i+_ya
                    canvas.drawTTkString(pos=(_xa,y), text=line, width=_xb-_xa, color=_color)
                    if y >= _yb-1: break
                canvas.fill(pos=(_xa,y+1),size=(_xb-_xa,_yb-y-1),color=_color)

        def _drawCellBottom(_col,_row,_xa,_xb,_ya,_yb,cellColor):
            if _yb>=h: return
            if _row<rows-1:
                _belowColor:TTkColor = _colorCache2d[_row+1-rowa][_col-cola]

                # force black border if there are selections
                _sa = self._selected[_row  ][_col  ]
                _sb = self._selected[_row+1][_col  ]
                if (showHS and showVS) and _sa and not _sb:
                    _bgA:TTkColor = cellColor.background()
                    _bgB:TTkColor = TTkColor.RST
                elif (showHS and showVS) and not _sa and _sb:
                    _bgA:TTkColor = TTkColor.RST
                    _bgB:TTkColor = _belowColor.background()
                else:
                    _bgA:TTkColor = cellColor.background()
                    _bgB:TTkColor = _belowColor.background()

                if _bgA == _bgB:
                    _char='─'
                    _color = lineColor if _bgA == TTkColor.RST else _bgA + lineColor
                elif _bgB == TTkColor.RST:
                    _char='▀'
                    _color=_bgA.invertFgBg()
                elif _bgA == TTkColor.RST:
                    _char='▄'
                    _color=_bgB.invertFgBg()
                else:
                    _char='▀'
                    _color=_bgB + _bgA.invertFgBg()
            else:
                if self._selected[_row  ][_col  ]:
                    _char='▀'
                    _color=selectedColorInv
                elif cellColor.hasBackground():
                    _char='▀'
                    _color=cellColor.background().invertFgBg()
                else:
                    _char='─'
                    _color=lineColor
            canvas.fill(pos=(_xa,_yb), size=(_xb-_xa,1), char=_char, color=_color)

        def _drawCellRight(_col,_row,_xa,_xb,_ya,_yb,cellColor):
            if _xb>=w: return
            if _col<cols-1:
                _rightColor:TTkColor = _colorCache2d[_row-rowa][_col+1-cola]

                # force black border if there are selections
                _sa = self._selected[_row  ][_col  ]
                _sc = self._selected[_row  ][_col+1]
                if (showHS and showVS) and _sa and not _sc:
                    _bgA:TTkColor = cellColor.background()
                    _bgC:TTkColor = TTkColor.RST
                elif (showHS and showVS) and not _sa and _sc:
                    _bgA:TTkColor = TTkColor.RST
                    _bgC:TTkColor = _rightColor.background()
                else:
                    _bgA:TTkColor = cellColor.background()
                    _bgC:TTkColor = _rightColor.background()

                if _bgA == _bgC:
                    _char='│'
                    _color = lineColor if _bgA == TTkColor.RST else _bgA + lineColor
                elif _bgC == TTkColor.RST:
                    _char='▌'
                    _color=_bgA.invertFgBg()
                elif _bgA == TTkColor.RST:
                    _char='▐'
                    _color=_bgC.invertFgBg()
                else:
                    _char='▌'
                    _color=_bgC + _bgA.invertFgBg()
            else:
                if self._selected[_row  ][_col  ]:
                    _char='▌'
                    _color=selectedColorInv
                elif cellColor.hasBackground():
                    _char=' '
                    _color=cellColor.background()
                else:
                    _char='│'
                    _color=lineColor
            canvas.fill(pos=(_xb,_ya), size=(1,_yb-_ya), char=_char, color=_color)

        _charList = [
            # 0x00 0x01 0x02 0x03
              ' ', '▘', '▝', '▀',
            # 0x04 0x05 0x06 0x07
              '▖', '▌', '▞', '▛',
            # 0x08 0x09 0x0A 0x0B
              '▗', '▚', '▐', '▜',
            # 0x0C 0x0D 0x0E 0x0F
              '▄', '▙', '▟', '█']

        def _drawCellCorner(_col:int,_row:int,_xa:int,_xb:int,_ya:int,_yb:int,cellColor:TTkColor):
            if _yb>=h or _xb>=w: return
            _char = 'X'
            _color = cellColor
            if _row<rows-1 and _col<cols-1:
                # Check if there are selected cells:
                chId = (
                    0x01 * self._selected[_row  ][_col  ] +
                    0x02 * self._selected[_row  ][_col+1] +
                    0x04 * self._selected[_row+1][_col  ] +
                    0x08 * self._selected[_row+1][_col+1] )
                if chId==0x00 or chId==0x0F:
                    _belowColor:TTkColor = _colorCache2d[_row+1-rowa][_col-cola]
                    _bgA:TTkColor = cellColor.background()
                    _bgB:TTkColor = _belowColor.background()

                    if _bgA == _bgB:
                        _color = lineColor if _bgA == TTkColor.RST else _bgA + lineColor
                        _char='┼'
                    elif _bgB == TTkColor.RST:
                        _char='▀'
                        _color=_bgA.invertFgBg()
                    elif _bgA == TTkColor.RST:
                        _char='▄'
                        _color=_bgB.invertFgBg()
                    else:
                        _char='▀'
                        _color=_bgB + _bgA.invertFgBg()
                else:
                    _char = _charList[chId]
                    _color=selectedColorInv

            elif _col<cols-1:
                chId = (
                    0x01 * self._selected[row  ][col  ] +
                    0x02 * self._selected[row  ][col+1] )
                if chId:
                    _char = _charList[chId]
                    _color=selectedColorInv
                elif cellColor.hasBackground():
                    _char='▀'
                    _color = cellColor.background().invertFgBg()
                else:
                    _char = '┴'
                    _color = lineColor
            elif _row<rows-1:
                chId = (
                    (0x01) * self._selected[row  ][col  ] +
                    (0x04) * self._selected[row+1][col  ] )
                _belowColor:TTkColor = _colorCache2d[_row+1-rowa][_col-cola]
                _bgA:TTkColor = cellColor.background()
                _bgB:TTkColor = _belowColor.background()

                if chId:
                    _char = _charList[chId]
                    _color=selectedColorInv
                elif _bgA == _bgB == TTkColor.RST:
                    _char = '┤'
                    _color = lineColor
                elif _bgB == TTkColor.RST:
                    _char='▀'
                    _color=_bgA.invertFgBg()
                elif _bgA == TTkColor.RST:
                    _char='▄'
                    _color=_bgB.invertFgBg()
                else:
                    _char='▀'
                    _color=_bgB + _bgA.invertFgBg()
            else:
                chId = (
                    (0x01) * self._selected[row  ][col  ] )
                if chId:
                    _char = _charList[chId]
                    _color=selectedColorInv
                elif cellColor.hasBackground():
                    _char='▀'
                    _color = cellColor.background().invertFgBg()
                else:
                    _char = '┘'
                    _color = lineColor
            canvas.fill(pos=(_xb,_yb), size=(1,1), char=_char, color=_color)

        # # Draw Cells
        for row,col,xa,xb,ya,yb,cellColor in _cellsCache:
            _drawCellContent(col,row,xa,xb,ya,yb,cellColor)

            if showHS:
                _drawCellBottom(col,row,xa,xb,ya,yb,cellColor)
            if showVS:
                _drawCellRight( col,row,xa,xb,ya,yb,cellColor)
            if showHS and showVS:
                _drawCellCorner(col,row,xa,xb,ya,yb,cellColor)

        # return f"cc={len(_cellsCache)}  size={(w,h)} tw={(sliceCol[0],sliceCol[-1])} th={(sliceRow[0],sliceRow[-1])}"

        if self._hoverPos:
            row,col = self._hoverPos
            if row == -1:
                ya,yb = -1,rp[-1]
            else:
                ya,yb = sliceRow[row]
            if col == -1:
                xa,xb = -1,cp[-1]
            else:
                xa,xb = sliceCol[col]

            if showVS:
                xa,xb = xa+vhs-ox, xb+vhs-ox
            else:
                xa,xb = xa+vhs-ox, xb+vhs-ox+1

            if showHS:
                ya,yb = ya+hhs-oy, yb+hhs-oy
            else:
                ya,yb = ya+hhs-oy, yb+hhs-oy+1

            # _drawCell(col,row,xa,xb,ya,yb,hoverColor)

            # Draw Borders
            # Top, Bottom
            hoverColorInv = hoverColor.background().invertFgBg()
            canvas.drawTTkString(pos=(xa,ya), text=TTkString('▗'+('▄'*(xb-xa-1))+'▖',hoverColorInv))
            canvas.drawTTkString(pos=(xa,yb), text=TTkString('▝'+('▀'*(xb-xa-1))+'▘',hoverColorInv))
            # Left, Right
            canvas.fill(char='▐',pos=(xa,ya+1), size=(1,yb-ya-1), color=hoverColorInv)
            canvas.fill(char='▌',pos=(xb,ya+1), size=(1,yb-ya-1), color=hoverColorInv)

        if self._dragPos:
            (rowa,cola),(rowb,colb) = self._dragPos
            if rowa == -1:
                cola,colb = min(cola,colb),max(cola,colb)
                xa = sliceCol[cola][0]-ox+vhs
                xb = sliceCol[colb][1]-ox+vhs + (0 if showHS else 1)
                ya,yb = -1-oy+hhs,rp[-1]-oy+hhs
            elif cola == -1:
                rowa,rowb = min(rowa,rowb),max(rowa,rowb)
                ya = sliceRow[rowa][0]-oy+hhs
                yb = sliceRow[rowb][1]-oy+hhs + (0 if showVS else 1)
                xa,xb = -1-ox+vhs,cp[-1]-ox+vhs
            else:
                cola,colb = min(cola,colb),max(cola,colb)
                rowa,rowb = min(rowa,rowb),max(rowa,rowb)
                xa = sliceCol[cola][0]-ox+vhs
                xb = sliceCol[colb][1]-ox+vhs + (0 if showHS else 1)
                ya = sliceRow[rowa][0]-oy+hhs
                yb = sliceRow[rowb][1]-oy+hhs + (0 if showVS else 1)

            hoverColorInv = hoverColor.background().invertFgBg()
            canvas.drawTTkString(pos=(xa,ya), text=TTkString('▗'+('▄'*(xb-xa-1))+'▖',hoverColorInv))
            canvas.drawTTkString(pos=(xa,yb), text=TTkString('▝'+('▀'*(xb-xa-1))+'▘',hoverColorInv))
            canvas.fill(char='▐',pos=(xa,ya+1), size=(1,yb-ya-1), color=hoverColorInv)
            canvas.fill(char='▌',pos=(xb,ya+1), size=(1,yb-ya-1), color=hoverColorInv)

        if self._currentPos:
            row,col = self._currentPos
            xa = sliceCol[col][0]-ox+vhs
            xb = sliceCol[col][1]-ox+vhs + (0 if showVS else 1)
            ya = sliceRow[row][0]-oy+hhs
            yb = sliceRow[row][1]-oy+hhs + (0 if showHS else 1)
            currentColorInv = currentColor.background().invertFgBg()
            if showVS and showHS:
                canvas.drawTTkString(pos=(xa,ya),   text=TTkString('▗'+('▄'*(xb-xa-1))+'▖',currentColorInv))
                canvas.drawTTkString(pos=(xa,yb),   text=TTkString('▝'+('▀'*(xb-xa-1))+'▘',currentColorInv))
                canvas.fill(char='▐',pos=(xa,ya+1), size=(1,yb-ya-1), color=currentColorInv)
                canvas.fill(char='▌',pos=(xb,ya+1), size=(1,yb-ya-1), color=currentColorInv)
            # elif showHS:
            #     canvas.drawTTkString(pos=(xa+1,ya), text=TTkString(     '▄'*(xb-xa-1)     ,currentColorInv))
            #     canvas.drawTTkString(pos=(xa+1,yb), text=TTkString(     '▀'*(xb-xa-1)     ,currentColorInv))
            # if showVS:
            #     canvas.fill(char='▐',pos=(xa,ya+1), size=(1,yb-ya-1), color=currentColorInv)
            #     canvas.fill(char='▌',pos=(xb,ya+1), size=(1,yb-ya-1), color=currentColorInv)

        # Draw H-Header first:
        if showHH:
            for col in range(*rcols):
                txt = self._tableModel.headerData(col,TTkK.HORIZONTAL)
                if isinstance(txt,TTkString): pass
                elif type(txt) == str: txt = TTkString(txt)
                else:                  txt = TTkString(f"{txt}")
                xa,xb = sliceCol[col]
                if showVS:
                    xa,xb = xa+vhs-ox+1, xb+vhs-ox
                else:
                    xa,xb = xa+vhs-ox+1, xb+vhs-ox+1
                canvas.drawText(pos=(xa,0), text=txt, width=xb-xa, color=headerColor)
                if self._sortingEnabled:
                    s = '•' if col != self._sortColumn else '▼' if self._sortOrder == TTkK.AscendingOrder else '▲'
                    canvas.drawText(pos=(xb-1,0), text=s, color=headerColor)
                if showVS:
                    canvas.drawChar(pos=(xb,0), char='╿', color=headerColor)

        # Draw V-Header :
        if showVH:
            hlineHead = TTkString('╾'+'╌'*(vhs-2), color=headerColor) + vHSeparator
            for row in range(*rrows):
                ya,yb = sliceRow[row]
                if showHS:
                    ya,yb = ya+hhs-oy+1, yb+hhs-oy
                else:
                    ya,yb = ya+hhs-oy+1, yb+hhs-oy+1
                if ya>h  : break
                if yb<hhs: continue
                txt = self._tableModel.headerData(row,TTkK.VERTICAL)
                if isinstance(txt,TTkString): pass
                elif type(txt) == str: txt = TTkString(txt)
                else:                  txt = TTkString(f"{txt}")
                canvas.drawTTkString(pos=(0    ,ya), text=txt, width=vhs, color=headerColor)
                canvas.drawTTkString(pos=(vhs-1,ya), text=vHSeparator)
                for y in range(ya+1,yb):
                    canvas.drawTTkString(pos=(0,y), text=vHSeparator, width=vhs, alignment=TTkK.RIGHT_ALIGN, color=headerColor)
                if showHS:
                    canvas.drawTTkString(pos=(0,yb), text=hlineHead)

        # Draw Top/Left Corner
        canvas.drawText(pos=(0,0), text=' ', width=vhs, color=separatorColor.invertFgBg() )

