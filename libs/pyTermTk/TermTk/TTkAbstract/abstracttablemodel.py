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

__all__ = ['TTkAbstractTableModel','TTkModelIndex']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot

class TTkModelIndex():
    '''
    This class is used as an index into item models derived from :py:class:`TTkAbstractTableModel`.
    The index is used by item views, delegates, and selection models to locate an item in the model.

    New :py:class:`TTkModelIndex` objects are created by the model using the :py:class:`TTkAbstractTableModel` -> :meth:`~TermTk.TTkAbstract.abstracttablemodel.TTkAbstractTableModel.index` function.
    An invalid model index can be constructed with the :py:class:`TTkModelIndex` constructor.

    Model indexes refer to items in models, and contain all the information required to specify their locations in those models.
    Each index is located in a given row and column; use :meth:`row`, :meth:`column`, and :meth:`data` to obtain this information.

    To obtain a model index that refers to an existing item in a model, call :py:class:`TTkAbstractTableModel` -> :meth:`~TermTk.TTkAbstract.abstracttablemodel.TTkAbstractTableModel.index` with the required row and column values.
    '''
    def __init__(self) -> None:
        pass

    def row(self) -> int:
        '''
        Returns the row this model index refers to.

        :return: int
        '''
        pass

    def col(self) -> int:
        '''
        Returns the column this model index refers to.

        :return: int
        '''
        pass

    def data(self) -> object:
        '''
        Returns the data for the item referred to by the index.

        :return: object
        '''
        pass

    def setData(self, data:object) -> None:
        '''
        Set the data in the item referred by the current index.

        :param data: the data to be set in the (row,col) position of the table
        :type data: object
        '''
        pass

class _TTkModelIndexList(TTkModelIndex):
    __slots__ = ('_col','_row','_model')
    def __init__(self, row:int, col:list, model) -> None:
        self._col = col
        self._row = row
        self._model = model
        super().__init__()

    def row(self) -> int:
        return self._row

    def col(self) -> int:
        return self._col

    def data(self) -> object:
        return self._model.data(self._row,self._col)

    def setData(self, data: object) -> None:
        self._model.setData(self._row,self._col,data)

class TTkAbstractTableModel():
    '''
    :py:class:`TTkAbstractTableModel` provides a standard interface for
    models that represent their data as a two-dimensional array of items.
    It is not used directly, but must be subclassed.

    Since the model provides a more specialized interface than :py:class:`TTkAbstractItemModel`,
    it is not suitable for use with tree views.

    The :meth:`rowCount` and :meth:`columnCount` functions return the dimensions of the table.

    **Subclassing**

    When subclassing :py:class:`TTkAbstractTableModel`, you must implement :meth:`rowCount`, :meth:`columnCount`, and :meth:`data`.
    Well behaved models will also implement :meth:`headerData`.

    Editable models need to implement :meth:`setData`.

    **Built-In Implementation**

    :py:class:`TTkTableModelList` basic subclass implementing a 2d list as data structure

    :py:class:`TTkTableModelCSV` subclass of :py:class:`TTkTableModelList` including the api to import csv data

    :py:class:`TTkTableModelSQLite3` subclass of :py:class:`TTkTableModelList` including support for `sqlite3 <https://www.sqlite.org>`__ databases

    '''

    __slots__ = (
        # Signals
        'dataChanged', 'modelChanged'
    )

    dataChanged:pyTTkSignal
    '''
        This signal is emitted whenever the data in an existing item changes.

        If more items are affected, the pos/size definne the minimum area including all of those changes.

        When reimplementing the :meth:`setData` function, this signal must be emitted explicitly.

        :param pos: the topLeft margin of the modified area
        :type pos: tuple(int,int)

        :param size: the size of the modified area
        :type size: tuple(int,int)
    '''
    modelChanged:pyTTkSignal
    '''
        This signal is emitted whenever the model changes.

        When the model topology changes, this signal must be emitted explicitly.
    '''
    def __init__(self):
        self.dataChanged = pyTTkSignal(tuple[int,int],tuple[int,int])
        self.modelChanged = pyTTkSignal()

    def rowCount(self) -> int:
        '''
        Returns the number of rows of the current model.

        :return: int
        '''
        raise NotImplementedError()

    def columnCount(self) -> int:
        '''
        Returns the number of columns of the current moodel.

        :return: int
        '''
        raise NotImplementedError()

    def index(self, row:int, col:int) -> TTkModelIndex:
        '''
        Returns the index of the item in the model specified by the given row, column.

        :param row: the row position of the index
        :type row: int
        :param col: the column position of the index
        :type col: int

        :return: :py:class:`TTkModelIndex`
        '''
        return _TTkModelIndexList(row,col,self)

    def data(self, row:int, col:int) -> object:
        '''
        Returns the data stored for the item referred to by the row/column.

        Note: If you do not have a value to return, return *None* instead of returning 0.

        :param row: the row position of the data
        :type row: int
        :param col: the column position of the data
        :type col: int

        :return: object
        '''
        raise NotImplementedError()

    def setData(self, row:int, col:int, data:object) -> bool:
        '''
        Returns true if successful; otherwise returns false.

        The :meth:`~TermTk.TTkAbstract.abstracttablemodel.TTkAbstractTableModel.dataChanged` signal should be emitted if the data was successfully set.

        The base class implementation returns false. This function and :meth:`data` must be reimplemented for editable models.

        :param row: the row position of the data
        :type row: int
        :param col: the column position of the data
        :type col: int
        :param data: the data to be set in the (row,col) position of the table
        :type data: object

        :return: bool
        '''
        return False

    def ttkStringData(self, row:int, col:int) -> TTkString:
        '''
        Returns the :py:class:`TTkString` reprsents the ddata stored in the row/column.

        :param row: the row position of the data
        :type row: int
        :param col: the column position of the data
        :type col: int

        :return: :py:class:`TTkString`
        '''
        data = self.data(row,col)
        if isinstance(data,TTkString):
            return data
        elif type(data) == str:
            return TTkString(data)
        else:
            return TTkString(str(data))

    def headerData(self, pos:int, orientation:TTkK.Direction) -> TTkString:
        '''
        Returns the data for the given role and section in the header with the specified orientation.

        For horizontal headers, the section number corresponds to the column number.
        Similarly, for vertical headers, the section number corresponds to the row number.

        :param pos: the position (col or row) of the header
        :type pos: int
        :param orientation: the orienttin of the header to be retrieved
        :type orientation: :py:class:`TTkConstant.Direction`

        :return: :py:class:`TTkString`
        '''
        if orientation==TTkK.HORIZONTAL:
            return TTkString(str(pos))
        elif orientation==TTkK.VERTICAL:
            return TTkString(str(pos))
        return TTkString()

    def flags(self, row:int, col:int) -> TTkK.ItemFlag:
        '''
        Returns the item flags for the given row,column.

        The base class implementation returns a combination of flags that
        enables the item (:py:class:`~TermTk.TTkCore.constant.TTkConstant.ItemFlag.ItemIsEnabled`)
        and allows it to be selected (:py:class:`~TermTk.TTkCore.constant.TTkConstant.ItemFlag.ItemIsSelectable`).

        :param row: the row position od the data
        :type row: int
        :param col: the column position of the data
        :type col: int

        :return: :py:class:`TTkConstant.ItemFlag`
        '''
        return (
            TTkK.ItemFlag.ItemIsEnabled  |
            TTkK.ItemFlag.ItemIsSelectable )

    def sort(self, column:int, order:TTkK.SortOrder) -> None:
        '''
        Sorts the model by column in the given order.

        :param column: The column index to be sorted, if -1 is provided the original unsorted order is used.
        :type column: int
        :param order: the sorting order
        :type order: :py:class:`TTkConstant.SortOrder`
        '''
        pass

    def insertColumn(self, column:int) -> bool:
        '''
        Inserts a single column before the given column.

        .. note:: This function calls the method :py:meth:`TTkAbstractTableModel.insertColumns`.

        :param column: The column index.
        :type column: int

        :return: true if the column is inserted; otherwise returns false.
        :rtype: bool
        '''
        return self.insertColumns(column=column, count=1)

    def insertColumns(self, column:int, count:int) -> bool:
        '''
        On models that support this,
        inserts <count> new columns into the model before the given column..

        If column is 0, the columns are prepended to any existing columns.

        If column is :py:meth:`TTkAbstractTableModel.columnCount`,
        the columns are appended to any existing columns.

        If you implement your own model,
        you can reimplement this function if you want to support insertions.
        Alternatively, you can provide your own API for altering the data.

        .. note:: The base class implementation (:py:class:`TTkAbstractTableModel`) of this function does nothing and returns false.

        :param column: Starting position of columns to insert (0-based index).
        :type column: int
        :param count: The number of columns to be inserted.
        :type count: int

        :return: true if the columns were successfully inserted; otherwise returns false.
        :rtype: bool
        '''
        return False

    def insertRow(self, row:int) -> bool:
        '''
        Inserts a single row before the given row.

        .. note:: This function calls the method :py:meth:`TTkAbstractTableModel.insertRows`.

        :param row: The row index.
        :type row: int

        :return: true if the row is inserted; otherwise returns false.
        :rtype: bool
        '''
        return self.insertRows(row=row, count=1)

    def insertRows(self, row:int, count:int) -> bool:
        '''
        On models that support this,
        inserts count rows into the model before the given row.

        If row is 0, the rows are prepended to any existing rows in the parent.

        If row is :py:meth:`TTkAbstractTableModel.rowCount`,
        the rows are appended to any existing rows in the parent.

        If you implement your own model,
        you can reimplement this function if you want to support insertions.
        Alternatively, you can provide your own API for altering the data.

        .. note:: The base class implementation (:py:class:`TTkAbstractTableModel`) of this function does nothing and returns false.

        :param row: Starting position of rows to insert (0-based index)
        :type row: int
        :param count: The number of rows to be inserted.
        :type count: int

        :return: true if the rows were successfully inserted; otherwise returns false.
        :rtype: bool
        '''
        return False

    def removeColumn(self, column:int) -> bool:
        '''
        Removes the given column.

        .. note:: This function calls the method :py:meth:`TTkAbstractTableModel.removeColumns`.

        :param column: The column index.
        :type column: int

        :return: true if the column is removed; otherwise returns false.
        :rtype: bool
        '''
        return self.removeColumns(column=column, count=1)

    def removeColumns(self, column:int, count:int) -> bool:
        '''
        On models that support this,
        removes count columns starting with the given column.

        If you implement your own model,
        you can reimplement this function if you want to support removing.
        Alternatively, you can provide your own API for altering the data.

        .. note:: The base class implementation (:py:class:`TTkAbstractTableModel`) of this function does nothing and returns false.

        :param column: Starting position of columns to remove (0-based index)
        :type column: int
        :param count: The number of columns to remove.
        :type count: int

        :return: true if the columns were successfully removed; otherwise returns false.
        :rtype: bool
        '''
        return False

    def removeRow(self, row:int) -> bool:
        '''
        Removes the given row.

        .. note:: This function calls the method :py:meth:`TTkAbstractTableModel.removeRows`.

        :param row: The row index.
        :type row: int

        :return: true if the row is removed; otherwise returns false.
        :rtype: bool
        '''
        return self.removeRows(row=row, count=1)

    def removeRows(self, row:int, count:int) -> bool:
        '''
        On models that support this,
        removes count rows starting with the given row.

        If you implement your own model,
        you can reimplement this function if you want to support removing.
        Alternatively, you can provide your own API for altering the data.

        .. note:: The base class implementation (:py:class:`TTkAbstractTableModel`) of this function does nothing and returns false.

        :param row: Starting position of rows to remove (0-based index)
        :type row: int
        :param count: The number of rows to remove.
        :type count: int

        :return: true if the rows were successfully removed; otherwise returns false.
        :rtype: bool
        '''
        return False
