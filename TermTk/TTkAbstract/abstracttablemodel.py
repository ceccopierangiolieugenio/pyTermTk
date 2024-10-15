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

__all__ = ['TTkAbstractTableModel']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot

class TTkModelIndex():
    '''
    This class is used as an index into item models derived from :class:`~TermTk.TTkAbstract.abstracttablemodel.TTkAbstractTableModel`.
    The index is used by item views, delegates, and selection models to locate an item in the model.

    New :class:`~TermTk.TTkAbstract.abstracttablemodel.TTkModelIndex` objects are created by the model using the :class:`~TermTk.TTkAbstract.abstracttablemodel.TTkAbstractTableModel` -> :meth:`~TermTk.TTkAbstract.abstracttablemodel.TTkAbstractTableModel.index` function.
    An invalid model index can be constructed with the :class:`~TermTk.TTkAbstract.abstracttablemodel.TTkModelIndex` constructor.

    Model indexes refer to items in models, and contain all the information required to specify their locations in those models.
    Each index is located in a given row and column; use :meth:`row`, :meth:`column`, and :meth:`data` to obtain this information.

    To obtain a model index that refers to an existing item in a model, call :class:`~TermTk.TTkAbstract.abstracttablemodel.TTkAbstractTableModel` -> :meth:`~TermTk.TTkAbstract.abstracttablemodel.TTkAbstractTableModel.index` with the required row and column values.
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

class TTkAbstractTableModel():
    '''
    :class:`TTkAbstractTableModel` provides a standard interface for
    models that represent their data as a two-dimensional array of items.
    It is not used directly, but must be subclassed.

    Since the model provides a more specialized interface than :class:`~TermTk.TTkAbstract.abstractitemmodel.TTkAbstractItemModel`,
    it is not suitable for use with tree views.

    The :meth:`rowCount` and :meth:`columnCount` functions return the dimensions of the table.

    **Subclassing**

    When subclassing :class:`TTkAbstractTableModel`, you must implement :meth:`rowCount`, :meth:`columnCount`, and :meth:`data`.
    Well behaved models will also implement :meth:`headerData`.

    Editable models need to implement :meth:`setData`.

    **Built-In Implementation**

    :class:`~TermTk.TTkWidgets.TTkModelView.tablemodellist.TTkTableModelList` basic subclass implementing a 2d list as data structure

    :class:`~TermTk.TTkWidgets.TTkModelView.tablemodelcsv.TTkTableModelCSV` subclass of :class:`~TermTk.TTkWidgets.TTkModelView.tablemodellist.TTkTableModelList` including the api to import csv data

    +-----------------------------------------------------------------------------------------------+
    | `Signals <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/003-signalslots.html>`_ |
    +-----------------------------------------------------------------------------------------------+

        .. py:method:: dataChanged(pos,size)
            :signal:

            This signal is emitted whenever the data in an existing item changes.

            If more items are affected, the pos/size definne the minimum area including all of those changes.

            When reimplementing the :meth:`setData` function, this signal must be emitted explicitly.

            :param pos: the topLeft margin of the modified area
            :type pos: tuple(int,int)

            :param size: the size of the modified area
            :type size: tuple(int,int)
            '''
    __slots__ = (
        # Signals
        'dataChanged'
    )
    def __init__(self):
        self.dataChanged = pyTTkSignal(tuple[int,int],tuple[int,int])

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

        :return: :class:`~TermTk.TTkAbstract.abstracttablemodel.TTkModelIndex`
        '''
        return TTkModelIndex()

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
        Returns the :class:`~TermTk.TTkCore.string.TTkString` reprsents the ddata stored in the row/column.

        :param row: the row position of the data
        :type row: int
        :param col: the column position of the data
        :type col: int

        :return: :class:`~TermTk.TTkCore.string.TTkString`
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
        :type orientation: :class:`~TermTk.TTkCore.constant.TTkConstant.Direction`

        :return: :class:`~TermTk.TTkCore.string.TTkString`
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
        enables the item (:class:`~TermTk.TTkCore.constant.TTkConstant.ItemFlag.ItemIsEnabled`)
        and allows it to be selected (:class:`~TermTk.TTkCore.constant.TTkConstant.ItemFlag.ItemIsSelectable`).

        :param row: the row position od the data
        :type row: int
        :param col: the column position of the data
        :type col: int

        :return: :class:`~TermTk.TTkCore.constant.TTkConstant.ItemFlag`
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
        :type order: :class:`~TermTk.TTkCore.constant.TTkConstant.SortOrder`
        '''
        pass
