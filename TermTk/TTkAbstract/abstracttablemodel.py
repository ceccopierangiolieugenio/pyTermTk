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

    def data(self, row:int, col:int) -> object:
        '''
        Returns the data stored for the item referred to by the row/column.

        Note: If you do not have a value to return, return *None* instead of returning 0.

        :return: object
        '''
        raise NotImplementedError()

    def setData(self, row:int, col:int, data:object) -> bool:
        '''
        Returns true if successful; otherwise returns false.

        The :meth:`~TermTk.TTkAbstract.abstracttablemodel.TTkAbstractTableModel.dataChanged` signal should be emitted if the data was successfully set.

        The base class implementation returns false. This function and :meth:`data` must be reimplemented for editable models.

        :return: bool
        '''
        return False

    def ttkStringData(self, row:int, col:int) -> TTkString:
        '''
        Returns the :class:`~TermTk.TTkCore.string.TTkString` reprsents the ddata stored in the row/column.

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
        :type pos: tuple(int,int)
        :param orientation: the orienttin of the header to be retrieved
        :type orientation: :class:`~TermTk.TTkCore.constant.TTkConstant.Direction`

        :return: :class:`~TermTk.TTkCore.string.TTkString`
        '''
        if orientation==TTkK.HORIZONTAL:
            return TTkString(str(pos))
        elif orientation==TTkK.VERTICAL:
            return TTkString(str(pos))
        return TTkString()

    def sort(self, col:int, order) -> None:
        pass
