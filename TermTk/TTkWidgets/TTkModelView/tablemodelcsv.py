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
from TermTk.TTkWidgets.TTkModelView.tablemodellist import TTkTableModelList

class TTkTableModelCSV(TTkTableModelList):
    '''
    :py:class:`TTkTableModelCSV` extends :py:class:`TTkTableModelList` with cvs loading helpers.

    You can address the csv file through the Filename (filename) or the FileDescriptor (fd).

    ::

        import TermTk as ttk

        # TableModel from csv filename
        tm1 = ttk.TTkTableModelCSV(filename='path/file.csv')

        # TableModel from csv FileDescriptor
        with open('path/file.csv') as fd:
            tm2 = ttk.TTkTableModelCSV(fd=fd)

    '''

    def __init__(self, *,
                 filename:str=None,
                 fd=None) -> None:
        '''
        :param filename: the csv filename, if missing the file descriptor is used instead.
        :type filename: str, optional

        :param fd: the FileDescriptor
        :type fd: io, optional
        '''
        data, head, idx = [[]], [], []
        if filename:
            with open(filename, "r") as fd:
                data, head, idx = self._csvImport(fd)
        elif fd:
            data, head, idx = self._csvImport(fd)
        super().__init__(data=data,header=head,indexes=idx)

    def _csvImport(self, fd) -> tuple[list,list,list[list]]:
        data, head, idx = [], [], []
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(fd.read(2048))
        fd.seek(0)
        csvreader = csv.reader(fd)
        for row in csvreader:
            data.append(row)
        if has_header:
            head = data.pop(0)
        # check if the first column include an index:
        if self._checkIndexColumn(data):
            head.pop(0)
            for l in data:
                idx.append(l.pop(0))
        return data, head, idx

    def _checkIndexColumn(self, data:list[list]) -> bool:
        if all(l[0].isdigit() for l in data):
            num = int(data[0][0])
            return all(num+i==int(l[0]) for i,l in enumerate(data))
        return False
