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
from TermTk.TTkWidgets.TTkModelView.tablewidget import TTkTableWidget, TTkHeaderView
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea, _ForwardData
from TermTk.TTkAbstract.abstracttablemodel import TTkAbstractTableModel

class TTkTable(TTkAbstractScrollArea):
    __doc__ = '''
    :py:class:`TTkTable` is a container widget which place :py:class:`TTkTableWidget` in a scrolling area with on-demand scroll bars.

    ''' + TTkTableWidget.__doc__

    classStyle = TTkTableWidget.classStyle

    _ttk_forward = _ForwardData(
        forwardClass=TTkTableWidget ,
        instance="self._tableView",
        signals=[ # Forwarded Signals From TTkTable
            # 'cellActivated',
            'cellChanged',
            'cellClicked', 'cellDoubleClicked',
            'cellEntered', # 'cellPressed',
            'currentCellChanged'],
        methods=[ # Forwarded Methods From TTkTable
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
            'setRowHeight', 'resizeRowToContents', 'resizeRowsToContents']
    )

    __slots__ = ('_tableView', *_ttk_forward.signals)

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
        '''
        :param tableWidget: a custom Table Widget to be used instead of the default one.
        :type tableWidget: :py:class:`TTkTableWidget`, optional
        '''
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

        for _attr in self._ttk_forward.signals:
            setattr(self,_attr,getattr(self._tableView,_attr))

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

    #--FORWARD-AUTOGEN-START--#
    @pyTTkSlot()
    def undo(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.undo`

        Undoes the last operation if undo is available.
        '''
        return self._tableView.undo()
    @pyTTkSlot()
    def redo(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.redo`

        Redoes the last operation if redo is available.
        '''
        return self._tableView.redo()
    def isUndoAvailable(self) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.isUndoAvailable`

        isUndoAvailable
        
        :return: bool
        '''
        return self._tableView.isUndoAvailable()
    def isRedoAvailable(self) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.isRedoAvailable`

        isRedoAvailable
        
        :return: bool
        '''
        return self._tableView.isRedoAvailable()
    @pyTTkSlot()
    def copy(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.copy`

        Copies any selected cells to the clipboard.
        '''
        return self._tableView.copy()
    @pyTTkSlot()
    def cut(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.cut`

        Copies the selected ccells to the clipboard and deletes them from the table.
        '''
        return self._tableView.cut()
    @pyTTkSlot()
    def paste(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.paste`

        Pastes the text/cells from the clipboard into the table at the current cursor position.
        '''
        return self._tableView.paste()
    @pyTTkSlot(bool)
    def setSortingEnabled(self, enable:bool) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.setSortingEnabled`

        If enable is true, enables sorting for the table and immediately trigger a
        call to :meth:`sortByColumn`
        with the current sort section and order
        
        **Note**: Setter function for property sortingEnabled.
        
        :param enable: the availability of undo
        :type enable: bool
        '''
        return self._tableView.setSortingEnabled(enable=enable)
    def isSortingEnabled(self) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.isSortingEnabled`

        This property holds whether sorting is enabled
        If this property is true, sorting is enabled for the table.
        If this property is false, sorting is not enabled. The default value is false.
        
        **Note**: . Setting the property to true with :meth:`setSortingEnabled`
        immediately triggers a call to :meth:`sortByColumn`
        with the current sort section and order.
        
        :return: bool
        '''
        return self._tableView.isSortingEnabled()
    @pyTTkSlot(int, TTkK.SortOrder)
    def sortByColumn(self, column:int, order:TTkK.SortOrder) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.sortByColumn`

        Sorts the model by the values in the given column and order.
        
        column may be -1, in which case no sort indicator will be shown and the model will return to its natural, unsorted order.
        Note that not all models support this and may even crash in this case.
        
        :param column: the column used for the sorting, -1 to keep the table unsorted
        :type column: bool
        
        :param order: the sort order
        :type order: :py:class:`TTkK.SortOrder`
        '''
        return self._tableView.sortByColumn(column=column, order=order)
    def clearSelection(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.clearSelection`

        Deselects all selected items.
        The current index will not be changed.
        '''
        return self._tableView.clearSelection()
    def selectAll(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.selectAll`

        Selects all items in the view.
        This function will use the selection behavior set on the view when selecting.
        '''
        return self._tableView.selectAll()
    def setSelection(self, pos:tuple[int,int], size:tuple[int,int], flags:TTkK.TTkItemSelectionModel) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.setSelection`

        Selects the items within the given rect and in accordance with the specified selection flags.
        
        :param pos: the x,y position of the rect
        :type pos: tuple[int,int]
        :param size: the width,height of the rect used for the selection
        :type size: tuple[int,int]
        :param flags: the selection model used (i.e. :py:class:`TTkItemSelectionModel.Select`)
        :type flags: :py:class:`TTkItemSelectionModel`
        '''
        return self._tableView.setSelection(pos=pos, size=size, flags=flags)
    def selectRow(self, row:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.selectRow`

        Selects the given row in the table view
        
        :param row: the row to be selected
        :type row: int
        '''
        return self._tableView.selectRow(row=row)
    def selectColumn(self, col:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.selectColumn`

        Selects the given column in the table view
        
        :param col: the column to be selected
        :type col: int
        '''
        return self._tableView.selectColumn(col=col)
    def unselectRow(self, row:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.unselectRow`

        Unselects the given row in the table view
        
        :param row: the row to be unselected
        :type row: int
        '''
        return self._tableView.unselectRow(row=row)
    def unselectColumn(self, column:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.unselectColumn`

        Unselects the given column in the table view
        
        :param column: the column to be unselected
        :type column: int
        '''
        return self._tableView.unselectColumn(column=column)
    def rowCount(self) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.rowCount`

        Returns the number of rows.
        
        :return: int
        '''
        return self._tableView.rowCount()
    def currentRow(self) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.currentRow`

        Returns the row of the current item.
        
        :return: int
        '''
        return self._tableView.currentRow()
    def columnCount(self) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.columnCount`

        Returns the number of columns.
        
        :return: int
        '''
        return self._tableView.columnCount()
    def currentColumn(self) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.currentColumn`

        Returns the column of the current item.
        
        :return: int
        '''
        return self._tableView.currentColumn()
    def verticalHeader(self) -> TTkHeaderView:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.verticalHeader`

        Returns the table view's vertical header.
        
        :return: :py:class:`TTkHeaderView`
        '''
        return self._tableView.verticalHeader()
    def horizontalHeader(self) -> TTkHeaderView:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.horizontalHeader`

        Returns the table view's horizontal header.
        
        :return: :py:class:`TTkHeaderView`
        '''
        return self._tableView.horizontalHeader()
    def hSeparatorVisibility(self) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.hSeparatorVisibility`

        Returns the visibility status of the horizontal separator
        
        :return: bool
        '''
        return self._tableView.hSeparatorVisibility()
    def vSeparatorVisibility(self) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.vSeparatorVisibility`

        Returns the visibility status of the vertical separator
        
        :return: bool
        '''
        return self._tableView.vSeparatorVisibility()
    def setHSeparatorVisibility(self, visibility:bool) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.setHSeparatorVisibility`

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
        return self._tableView.setHSeparatorVisibility(visibility=visibility)
    def setVSeparatorVisibility(self, visibility:bool):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.setVSeparatorVisibility`

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
        return self._tableView.setVSeparatorVisibility(visibility=visibility)
    def model(self) -> TTkAbstractTableModel:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.model`

        Returns the model that this view is presenting.
        
        :return: :py:class:`TTkAbstractTableModel`
        '''
        return self._tableView.model()
    def setModel(self, model:TTkAbstractTableModel) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.setModel`

        Sets the model for the view to present.
        
        :param model:
        :type model: :py:class:`TTkAbstractTableModel`
        '''
        return self._tableView.setModel(model=model)
    @pyTTkSlot(int,int)
    def setColumnWidth(self, column:int, width: int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.setColumnWidth`

        Sets the width of the given column.
        
        :param column: the column
        :type column: int
        :param width: its width
        :type width: int
        '''
        return self._tableView.setColumnWidth(column=column, width=width)
    @pyTTkSlot(int)
    def resizeColumnToContents(self, column:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.resizeColumnToContents`

        Resizes the given column based on the size hints of the delegate used to render each item in the column.
        
        :param column: the column to be resized
        :type column: int
        '''
        return self._tableView.resizeColumnToContents(column=column)
    @pyTTkSlot()
    def resizeColumnsToContents(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.resizeColumnsToContents`

        Resizes all columns based on the size hints of the delegate used to render each item in the columns.
        '''
        return self._tableView.resizeColumnsToContents()
    @pyTTkSlot(int,int)
    def setRowHeight(self, row:int, height: int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.setRowHeight`

        Sets the height of the given row.
        
        :param row: the row
        :type row: int
        :param height: its height
        :type height: int
        '''
        return self._tableView.setRowHeight(row=row, height=height)
    @pyTTkSlot(int)
    def resizeRowToContents(self, row:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.resizeRowToContents`

        Resizes the given row based on the size hints of the delegate used to render each item in the row.
        
        :param row: the row to be resized
        :type row: int
        '''
        return self._tableView.resizeRowToContents(row=row)
    @pyTTkSlot()
    def resizeRowsToContents(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTableWidget.resizeRowsToContents`

        Resizes all rows based on the size hints of the delegate used to render each item in the rows.
        '''
        return self._tableView.resizeRowsToContents()
    #--FORWARD-AUTOGEN-END--#

