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

__all__ = ['TTkTable']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkWidgets.TTkModelView.tablewidget import TTkTableWidget
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstracttablemodel import TTkAbstractTableModel

class TTkTable(TTkAbstractScrollArea):
    '''
    A :py:class:`TTkTable` implements a table view (:py:class:`TTkTableWidget`) that displays items from a model.

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

    please refer to :py:class:`TTkTableWidget` for a detailed descriptoin of all the available methods and init params



    .. py:method:: undo()

        This method is forwarded to :meth:`TTkTableWidget.undo`

    .. py:method:: redo()

        This method is forwarded to :meth:`TTkTableWidget.redo`

    .. py:method:: isUndoAvailable()

        This method is forwarded to :meth:`TTkTableWidget.isUndoAvailable`

    .. py:method:: isRedoAvailable()

        This method is forwarded to :meth:`TTkTableWidget.isRedoAvailable`

    .. py:method:: copy()

        This method is forwarded to :meth:`TTkTableWidget.copy`

    .. py:method:: cut()

        This method is forwarded to :meth:`TTkTableWidget.cut`

    .. py:method:: paste()

        This method is forwarded to :meth:`TTkTableWidget.paste`

    .. py:method:: setSortingEnabled()

        This method is forwarded to :meth:`TTkTableWidget.setSortingEnabled`

    .. py:method:: isSortingEnabled()

        This method is forwarded to :meth:`TTkTableWidget.isSortingEnabled`

    .. py:method:: sortByColumn()

        This method is forwarded to :meth:`TTkTableWidget.sortByColumn`

    .. py:method:: clearSelection()

        This method is forwarded to :meth:`TTkTableWidget.clearSelection`

    .. py:method:: selectAll()

        This method is forwarded to :meth:`TTkTableWidget.selectAll`

    .. py:method:: setSelection()

        This method is forwarded to :meth:`TTkTableWidget.setSelection`

    .. py:method:: selectRow()

        This method is forwarded to :meth:`TTkTableWidget.selectRow`

    .. py:method:: selectColumn()

        This method is forwarded to :meth:`TTkTableWidget.selectColumn`

    .. py:method:: unselectRow()

        This method is forwarded to :meth:`TTkTableWidget.unselectRow`

    .. py:method:: unselectColumn()

        This method is forwarded to :meth:`TTkTableWidget.unselectColumn`

    .. py:method:: rowCount()

        This method is forwarded to :meth:`TTkTableWidget.rowCount`

    .. py:method:: currentRow()

        This method is forwarded to :meth:`TTkTableWidget.currentRow`

    .. py:method:: columnCount()

        This method is forwarded to :meth:`TTkTableWidget.columnCount`

    .. py:method:: currentColumn()

        This method is forwarded to :meth:`TTkTableWidget.currentColumn`

    .. py:method:: verticalHeader()

        This method is forwarded to :meth:`TTkTableWidget.verticalHeader`

    .. py:method:: horizontalHeader()

        This method is forwarded to :meth:`TTkTableWidget.horizontalHeader`

    .. py:method:: hSeparatorVisibility()

        This method is forwarded to :meth:`TTkTableWidget.hSeparatorVisibility`

    .. py:method:: vSeparatorVisibility()

        This method is forwarded to :meth:`TTkTableWidget.vSeparatorVisibility`

    .. py:method:: setHSeparatorVisibility()

        This method is forwarded to :meth:`TTkTableWidget.setHSeparatorVisibility`

    .. py:method:: setVSeparatorVisibility()

        This method is forwarded to :meth:`TTkTableWidget.setVSeparatorVisibility`

    .. py:method:: model()

        This method is forwarded to :meth:`TTkTableWidget.model`

    .. py:method:: setModel()

        This method is forwarded to :meth:`TTkTableWidget.setModel`

    .. py:method:: setColumnWidth()

        This method is forwarded to :meth:`TTkTableWidget.setColumnWidth`

    .. py:method:: resizeColumnToContents()

        This method is forwarded to :meth:`TTkTableWidget.resizeColumnToContents`

    .. py:method:: resizeColumnsToContents()

        This method is forwarded to :meth:`TTkTableWidget.resizeColumnsToContents`

    .. py:method:: setRowHeight()

        This method is forwarded to :meth:`TTkTableWidget.setRowHeight`

    .. py:method:: resizeRowToContents()

        This method is forwarded to :meth:`TTkTableWidget.resizeRowToContents`

    .. py:method:: resizeRowsToContents()

        This method is forwarded to :meth:`TTkTableWidget.resizeRowsToContents`
    '''

    # resizeRowsToContents:TTkTableWidget.resizeRowsToContents
    # '''
    #     This method is forwarded to :meth:`TTkTableWidget.resizeRowsToContents`
    # '''

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

    classStyle = TTkTableWidget.classStyle

    __slots__ = (
        '_tableView',
        # Forwarded Signals
        # 'cellActivated',
        'cellChanged',
        'cellClicked', 'cellDoubleClicked',
        'cellEntered', # 'cellPressed',
        'currentCellChanged',

        # Forwarded Methods From TTkTable
        'undo', 'redo',
        'isUndoAvailable','isRedoAvailable',
        'copy', 'cut', 'paste',
        'setSortingEnabled', 'isSortingEnabled', 'sortByColumn',
        'clearSelection', 'selectAll', 'setSelection',
        'selectRow', 'selectColumn', 'unselectRow', 'unselectColumn',
        'rowCount', 'currentRow', 'columnCount', 'currentColumn',
        'verticalHeader', 'horizontalHeader',
        'hSeparatorVisibility', 'vSeparatorVisibility', 'setHSeparatorVisibility', 'setVSeparatorVisibility',
        'model', 'setModel',
        'setColumnWidth', 'resizeColumnToContents', 'resizeColumnsToContents',
        'setRowHeight', 'resizeRowToContents', 'resizeRowsToContents',
        )

    def __init__(self, *,
                 tableWidget:TTkTableWidget=None,
                 tableModel:TTkAbstractTableModel=None,
                 vSeparator:bool=True,
                 hSeparator:bool=True,
                 vHeader:bool=True,
                 hHeader:bool=True,
                 sortingEnabled=False,
                 dataPadding=1,
                 **kwargs) -> None:
        self._tableView = None
        self._tableView:TTkTableWidget = tableWidget if tableWidget else TTkTableWidget(
                                                                                tableModel=tableModel,
                                                                                vSeparator=vSeparator,
                                                                                hSeparator=hSeparator,
                                                                                vHeader=vHeader,
                                                                                hHeader=hHeader,
                                                                                sortingEnabled=sortingEnabled,
                                                                                dataPadding=dataPadding,
                                                                                **kwargs|{'parent':None,'visible':True})
        super().__init__(**kwargs)
        self.setViewport(self._tableView)
        # self.setFocusPolicy(TTkK.ClickFocus)

        # Forward Signals
        self.cellChanged = self._tableView.cellChanged
        self.cellClicked = self._tableView.cellClicked
        self.cellEntered = self._tableView.cellEntered
        self.cellDoubleClicked  = self._tableView.cellDoubleClicked
        self.currentCellChanged = self._tableView.currentCellChanged

        # Forward Methods
        self.setFocus = self._tableView.setFocus
        self.focusChanged = self._tableView.focusChanged

        self.undo = self._tableView.undo
        self.redo = self._tableView.redo

        self.isUndoAvailable = self._tableView.isUndoAvailable
        self.isRedoAvailable = self._tableView.isRedoAvailable

        self.copy = self._tableView.copy
        self.cut = self._tableView.cut
        self.paste = self._tableView.paste

        self.setSortingEnabled = self._tableView.setSortingEnabled
        self.isSortingEnabled = self._tableView.isSortingEnabled
        self.sortByColumn = self._tableView.sortByColumn

        self.clearSelection = self._tableView.clearSelection
        self.selectAll = self._tableView.selectAll
        self.setSelection = self._tableView.setSelection
        self.selectRow = self._tableView.selectRow
        self.selectColumn = self._tableView.selectColumn
        self.unselectRow = self._tableView.unselectRow
        self.unselectColumn = self._tableView.unselectColumn

        self.rowCount = self._tableView.rowCount
        self.currentRow = self._tableView.currentRow
        self.columnCount = self._tableView.columnCount
        self.currentColumn = self._tableView.currentColumn

        self.verticalHeader = self._tableView.verticalHeader
        self.horizontalHeader = self._tableView.horizontalHeader

        self.hSeparatorVisibility = self._tableView.hSeparatorVisibility
        self.vSeparatorVisibility = self._tableView.vSeparatorVisibility
        self.setHSeparatorVisibility = self._tableView.setHSeparatorVisibility
        self.setVSeparatorVisibility = self._tableView.setVSeparatorVisibility

        self.model = self._tableView.model
        self.setModel = self._tableView.setModel

        self.setColumnWidth = self._tableView.setColumnWidth
        self.resizeColumnToContents = self._tableView.resizeColumnToContents
        self.resizeColumnsToContents = self._tableView.resizeColumnsToContents
        self.setRowHeight = self._tableView.setRowHeight
        self.resizeRowToContents = self._tableView.resizeRowToContents
        self.resizeRowsToContents = self._tableView.resizeRowsToContents


    def style(self):
        if self._tableView:
            return self._tableView.style()
        return super().style()

    def setStyle(self, style):
        if self._tableView:
            self._tableView.setStyle(style)
        return super().setStyle(style)

    def mergeStyle(self, style):
        if self._tableView:
            self._tableView.mergeStyle(style)
        return super().mergeStyle(style)