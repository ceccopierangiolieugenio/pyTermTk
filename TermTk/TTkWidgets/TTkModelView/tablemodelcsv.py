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

__all__=['TTkTableModelCSV']

import csv

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkAbstract.abstracttablemodel import TTkAbstractTableModel

class TTkTableModelCSV(TTkAbstractTableModel):
    __slots__ = ('_list', '_hheader', '_vheader')
    def __init__(self, *, filename='', fd=None):
        self._list = []
        self._hheader = []
        self._vheader = []
        if filename:
            with open(filename, "r") as fd:
                self._csvImport(fd)
        elif fd:
            self._csvImport(fd)
        super().__init__()

    def _csvImport(self, fd):
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(fd.read(2048))
        fd.seek(0)
        csvreader = csv.reader(fd)
        for row in csvreader:
            self._list.append(row)
        if has_header:
            self._hheader = self._list.pop(0)
        # check if the first column include an index:
        if self._checkIndexColumn():
            self._hheader.pop(0)
            for l in self._list:
                self._vheader.append(l.pop(0))

    def _checkIndexColumn(self):
        if all(l[0].isdigit() for l in self._list):
            num = int(self._list[0][0])
            return all(num+i==int(l[0]) for i,l in enumerate(self._list))
        return False

    def rowCount(self):
        return len(self._list)

    def columnCount(self):
        return len(self._list[0]) if self._list else 0

    def data(self, row, col):
        return self._list[row][col]

    def setData(self, row, col, data):
        self._list[row][col] = data

    def headerData(self, num, orientation):
        if orientation == TTkK.HORIZONTAL:
            if self._hheader:
                return self._hheader[num]
        if orientation == TTkK.VERTICAL:
            if self._vheader:
                return self._vheader[num]
        return super().headerData(num, orientation)