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

__all__=['TTkTableModelList']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkAbstract.abstracttablemodel import TTkAbstractTableModel, TTkModelIndex

class _TTkModelIndexList(TTkModelIndex):
    __slots__ = ('_col','_rowId','_rowCb')
    def __init__(self, col:int, rowId:list, rowCb) -> None:
        self._col   = col
        self._rowId = rowId
        self._rowCb = rowCb
        super().__init__()

    def row(self) -> int:
        return self._rowCb(self._rowId)

    def col(self) -> int:
        return self._col

    def data(self) -> object:
        return self._rowId[self._col]

    def setData(self, data: object) -> None:
        self._rowId[self._col] = data

class TTkTableModelList(TTkAbstractTableModel):
    '''
    :py:class:`TTkTableModelList` extends :py:class:`TTkAbstractTableModel`,
    including a basic model with a 2d list data structure

    '''

    __slots__ = ('_data','_dataOriginal', '_hheader', '_vheader')

    def __init__(self, *,
                 data:list[list[object]]=None,
                 header:list[str]=None,
                 indexes:list[str]=None) -> None:
        '''
        :param data: the 2D List model for the view to present.
        :type data: list[list]

        :param header: the header labels, defaults to the column number.
        :type header: list[str], optional

        :param indexes: the index labels, defaults to the line number.
        :type indexes: list[str], optional
        '''
        self._data = self._dataOriginal = data if data else [['']]
        self._hheader = header  if header  else []
        self._vheader = indexes if indexes else []
        super().__init__()

    def modelList(self) -> list[list]:
        return self._data

    def setModelList(self, modelList:list[list]) -> None:
        if modelList == self._data: return
        self._data = modelList
        self.modelChanged.emit()

    def rowCount(self) -> int:
        return len(self._data)

    def columnCount(self) -> int:
        return len(self._data[0]) if self._data else 0

    def index(self, row:int, col:int) -> TTkModelIndex:
        return _TTkModelIndexList(
                    col   = col ,
                    rowId = self._data[row] ,
                    rowCb = lambda rid: self._data.index(rid) )

    def data(self, row:int, col:int) -> None:
        return self._data[row][col]

    def setData(self, row:int, col:int, data:object) -> None:
        self._data[row][col] = data
        self.dataChanged.emit((row,col),(1,1))
        return True

    def headerData(self, num:int, orientation:int):
        if orientation == TTkK.HORIZONTAL:
            if self._hheader:
                return self._hheader[num]
        if orientation == TTkK.VERTICAL:
            if self._vheader:
                return self._vheader[num]
        return super().headerData(num, orientation)

    def flags(self, row:int, col:int) -> TTkK.ItemFlag:
        return (
            TTkK.ItemFlag.ItemIsEnabled  |
            TTkK.ItemFlag.ItemIsEditable |
            TTkK.ItemFlag.ItemIsSelectable )

    def sort(self, column:int, order:TTkK.SortOrder) -> None:
        if column == -1:
            self._data = self._dataOriginal
        else:
            try:
                self._data = sorted(self._dataOriginal, key=lambda x:x[column],     reverse=order==TTkK.SortOrder.DescendingOrder)
            except TypeError as _:
                self._data = sorted(self._dataOriginal, key=lambda x:str(x[column]), reverse=order==TTkK.SortOrder.DescendingOrder)
