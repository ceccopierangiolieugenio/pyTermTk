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

    Since the model provides a more specialized interface than QAbstractItemModel,
    it is not suitable for use with tree views, although it can be used to provide data to a QListView.
    If you need to represent a simple list of items, and only need a model to contain a single column of data,
    subclassing the QAbstractListModel may be more appropriate.

    The rowCount() and columnCount() functions return the dimensions of the table.
    To retrieve a model index corresponding to an item in the model,
    use index() and provide only the row and column numbers.

    **Subclassing**

    When subclassing QAbstractTableModel, you must implement :meth:`rowCount`, :meth:`columnCount`, and :meth:`data`.
    Well behaved models will also implement :meth:`headerData`.

    Editable models need to implement :meth:`setData`.

    Models that provide interfaces to resizable data structures can provide implementations of
    insertRows(), removeRows(), insertColumns(), and removeColumns().

    **Built-In Implementation**

    :class:`~TermTk.TTkWidgets.TTkModelView.tablemodellist.TTkTableModelList` basic subclass implementing a 2d list as data structure

    :class:`~TermTk.TTkWidgets.TTkModelView.tablemodelcsv.TTkTableModelCSV` subclass of :class:`~TermTk.TTkWidgets.TTkModelView.tablemodellist.TTkTableModelList` including the api to import csv data

    :class:`~TermTk.TTkWidgets.TTkModelView.tablemodeljson.TTkTableModelJson` subclass of :class:`~TermTk.TTkWidgets.TTkModelView.tablemodellist.TTkTableModelList` with a focus on json data structures
    '''
    __slots__ = (
        # Signals
        'dataChanged'
    )
    def __init__(self):
        self.dataChanged = pyTTkSignal()

    def rowCount(self) -> int:
        raise NotImplementedError()

    def columnCount(self) -> int:
        raise NotImplementedError()

    def data(self, row:int, col:int) -> object:
        raise NotImplementedError()

    def ttkStringData(self, row:int, col:int) -> TTkString:
        data = self.data(row,col)
        if isinstance(data,TTkString):
            return data
        elif type(data) == str:
            return TTkString(data)
        else:
            return TTkString(str(data))

    def setData(self, row:int, col:int, data:object):
        raise NotImplementedError()

    def headerData(self, pos:int, orientation:TTkK.Direction) -> TTkString:
        if orientation==TTkK.HORIZONTAL:
            return TTkString(str(pos))
        elif orientation==TTkK.VERTICAL:
            return TTkString(str(pos))
        return TTkString()

    def sort(self, col:int, order) -> None:
        pass
