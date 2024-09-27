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
from TermTk.TTkAbstract.abstracttablemodel import TTkAbstractTableModel

class TTkTableModelList(TTkAbstractTableModel):
    __slots__ = ('_list','_listOriginal', '_hheader', '_vheader')
    def __init__(self, *, list=[], header=[], indexes=[]):
        self._list = self._listOriginal = list
        self._hheader = header
        self._vheader = indexes
        super().__init__()

    def modelList(self) -> list[list]:
        return self._list

    def setModelList(self, modelList:list[list]) -> None:
        if modelList == self._list: return
        self._list = modelList

    def rowCount(self) -> int:
        return len(self._list)

    def columnCount(self) -> int:
        return len(self._list[0]) if self._list else 0

    def data(self, row:int, col:int) -> None:
        return self._list[row][col]

    def setData(self, row:int, col:int, data:object) -> None:
        self._list[row][col] = data

    def headerData(self, num:int, orientation:int):
        if orientation == TTkK.HORIZONTAL:
            if self._hheader:
                return self._hheader[num]
        if orientation == TTkK.VERTICAL:
            if self._vheader:
                return self._vheader[num]
        return super().headerData(num, orientation)

    def sort(self, column:int, order:TTkK.SortOrder) -> None:
        if column == -1:
            self._list = self._listOriginal
        else:
            try:
                self._list = sorted(self._listOriginal, key=lambda x:x[column],     reverse=order==TTkK.SortOrder.DescendingOrder)
            except TypeError as _:
                self._list = sorted(self._listOriginal, key=lambda x:str(x[column]), reverse=order==TTkK.SortOrder.DescendingOrder)
