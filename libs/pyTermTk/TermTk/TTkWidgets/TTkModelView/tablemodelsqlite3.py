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

__all__=['TTkTableModelSQLite3']

import sqlite3
import threading

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkAbstract.abstracttablemodel import TTkAbstractTableModel, TTkModelIndex

class _TTkModelIndexSQLite3(TTkModelIndex):
    __slots__ = ('_col','_rowId','_sqModel')
    def __init__(self, col:int, rowId:str, sqModel) -> None:
        self._col     = col
        self._rowId   = rowId
        self._sqModel = sqModel
        super().__init__()

    def row(self) -> int:
        return self._sqModel._getRow(self._rowId)-1
    def col(self) -> int:
        return self._col

    def data(self) -> object:
        return self._sqModel.data(row=self.row(),col=self.col())

    def setData(self, data: object) -> None:
        return self._sqModel.setData(row=self.row(),col=self.col(),data=data)

class TTkTableModelSQLite3(TTkAbstractTableModel):
    '''
    :py:class:`TTkTableModelSQLite3` extends :py:class:`TTkAbstractTableModel`,
    allowing to map an sqlite3 table to this table model

    Quickstart:

    In This example i assume i have a database named **sqlite.database.db** which contain a table **users**

    Please refer to `test.ui.032.table.10.sqlite.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tests/t.ui/test.ui.032.table.10.sqlite.py>`_ for  working eample.

    .. code-block:: python

        import TermTk as ttk

        filename='sqlite.database.db'
        tablename='users'

        root = ttk.TTk(mouseTrack=True, layout=ttk.TTkGridLayout())

        basicTableModel = ttk.TTkTableModelSQLite3(fileName=filename, table=tablename)
        table = ttk.TTkTable(parent=root, tableModel=basicTableModel, sortingEnabled=True)
        table.resizeColumnsToContents()

        root.mainloop()

    '''

    __slots__ = (
        '_conn', '_cur', '_table',
        '_key', '_columns', '_count',
        '_sort', '_sortColumn',
        '_sqliteMutex',
        '_idMap')

    def __init__(self, *,
                 fileName:str,
                 table:str,
                 # header:list[str]=None
                 ) -> None:
        '''
        :param fileName: the sqlite3 file database
        :type fileName: str

        :param table: the name of the sqlite3 table to be mapped
        :type table: str
        '''
        self._sqliteMutex = threading.Lock()
        self._table = table
        self._columns = []
        self._idMap = {}
        self._sort = ''
        self._sortColumn = -1

        self._sqliteMutex.acquire()
        self._conn = conn = sqlite3.connect(fileName, check_same_thread=False)
        self._cur  = cur  = self._conn.cursor()

        res = cur.execute(f"SELECT COUNT(*) FROM {table}")
        self._count = res.fetchone()[0]

        for row in cur.execute(f"PRAGMA table_info({table})"):
            if row[-1] == 0:
                self._columns.append(row[1])
            if row[-1] == 1:
                self._key = row[1]

        self._refreshIdMap()
        self._sqliteMutex.release()

        super().__init__()

    def _refreshIdMap(self):
        self._idMap = {
            _id : _rn
            for _rn,_id in self._cur.execute(f"SELECT ROW_NUMBER() OVER ({self._sort}) RN, {self._key} from users")}

    def rowCount(self) -> int:
        return self._count

    def columnCount(self) -> int:
        return len(self._columns)

    def _getRow(self, key:str) -> int:
        return self._idMap[key]

    def index(self, row:int, col:int) -> TTkModelIndex:
        self._sqliteMutex.acquire()
        res = self._cur.execute(
            f"SELECT {self._key} FROM {self._table} "
            f"{self._sort} "
            f"LIMIT 1 OFFSET {row}")
        key=res.fetchone()[0]
        self._sqliteMutex.release()
        return _TTkModelIndexSQLite3(col=col,rowId=key,sqModel=self)

    def data(self, row:int, col:int) -> None:
        self._sqliteMutex.acquire()
        res = self._cur.execute(
            f"SELECT {self._columns[col]} FROM {self._table} "
            f"{self._sort} "
            f"LIMIT 1 OFFSET {row}")
        self._sqliteMutex.release()
        return res.fetchone()[0]

    def setData(self, row:int, col:int, data:object) -> None:
        self._sqliteMutex.acquire()
        res = self._cur.execute(
            f"SELECT {self._key} FROM {self._table} "
            f"{self._sort} "
            f"LIMIT 1 OFFSET {row}")
        key=res.fetchone()[0]
        res = self._cur.execute(
            f"UPDATE {self._table} "
            f"SET {self._columns[col]} = '{data}' "
            f"WHERE {self._key} = {key} ")
        self._conn.commit()
        if col == self._sortColumn:
            self._refreshIdMap()
        self._sqliteMutex.releases()
        return True

    def headerData(self, num:int, orientation:int):
        if orientation == TTkK.HORIZONTAL:
            if self._columns:
                return self._columns[num]
        return super().headerData(num, orientation)

    def flags(self, row:int, col:int) -> TTkK.ItemFlag:
        return (
            TTkK.ItemFlag.ItemIsEnabled  |
            TTkK.ItemFlag.ItemIsEditable |
            TTkK.ItemFlag.ItemIsSelectable )

    def sort(self, column:int, order:TTkK.SortOrder) -> None:
        self._sortColumn = column
        if column == -1:
            self._sort = ''
        else:
            if order ==TTkK.SortOrder.AscendingOrder:
                self._sort = f"ORDER BY {self._columns[column]} ASC"
            else:
                self._sort = f"ORDER BY {self._columns[column]} DESC"
        self._sqliteMutex.acquire()
        self._refreshIdMap()
        self._sqliteMutex.release()
