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

from typing import Any

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
        '_key', '_columns', '_columnTypes', '_count',
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
        self._columnTypes = []  # Add this to store column types
        self._idMap = {}
        self._sort = ''
        self._sortColumn = -1

        with self._sqliteMutex:
            self._conn = conn = sqlite3.connect(fileName, check_same_thread=False)
            self._cur  = cur  = self._conn.cursor()

            res = cur.execute(f"SELECT COUNT(*) FROM {table}")
            self._count = res.fetchone()[0]

            for row in cur.execute(f"PRAGMA table_info({table})"):
                if row[-1] == 0:
                    self._columns.append(row[1])      # column name
                    self._columnTypes.append(row[2])  # column type
                if row[-1] == 1:
                    self._key = row[1]

            self._refreshIdMap()

        super().__init__()

    def _refreshIdMap(self):
        self._idMap = {
            _id : _rn
            for _rn,_id in self._cur.execute(f"SELECT ROW_NUMBER() OVER ({self._sort}) RN, {self._key} from {self._table}")}

    def rowCount(self) -> int:
        return self._count

    def columnCount(self) -> int:
        return len(self._columns)

    def _getRow(self, key:str) -> int:
        return self._idMap[key]

    def index(self, row:int, col:int) -> TTkModelIndex:
        with self._sqliteMutex:
            res = self._cur.execute(
                f"SELECT {self._key} FROM {self._table} "
                f"{self._sort} "
                f"LIMIT 1 OFFSET {row}")
            key=res.fetchone()[0]
            return _TTkModelIndexSQLite3(col=col,rowId=key,sqModel=self)

    def data(self, row:int, col:int) -> Any:
        with self._sqliteMutex:
            res = self._cur.execute(
                f"SELECT {self._columns[col]} FROM {self._table} "
                f"{self._sort} "
                f"LIMIT 1 OFFSET {row}")
            return res.fetchone()[0]

    def setData(self, row:int, col:int, data:object) -> None:
        with self._sqliteMutex:
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
        with self._sqliteMutex:
            self._refreshIdMap()

    def _getDefaultValueForType(self, sqlite_type: str) -> str:
        """Get appropriate default value based on SQLite column type"""
        sqlite_type = sqlite_type.upper()

        if 'INT' in sqlite_type:
            return '0'
        elif 'REAL' in sqlite_type or 'FLOAT' in sqlite_type or 'DOUBLE' in sqlite_type:
            return '0.0'
        elif 'TEXT' in sqlite_type or 'CHAR' in sqlite_type or 'VARCHAR' in sqlite_type:
            return "''"  # Empty string
        elif 'BLOB' in sqlite_type:
            return 'NULL'
        elif 'BOOL' in sqlite_type:
            return '0'  # False
        else:
            return 'NULL'  # Default fallback

    def insertRows(self, row: int, count: int = 1) -> bool:
        if row < 0 or count <= 0 or row > self._count:
            return False

        try:
            with self._sqliteMutex:
                # Create appropriate default values based on column types
                placeholders = [self._getDefaultValueForType(_ct) for _ct in self._columnTypes]
                placeholders_str = f"({', '.join(placeholders)})"
                columns_str = ', '.join(self._columns)

                # Insert the specified number of rows
                self._cur.execute(f"""
                    INSERT INTO {self._table} ({columns_str})
                    VALUES {','.join([placeholders_str]*count)}
                """)

                self._conn.commit()
                self._count += count
                self._refreshIdMap()
        except sqlite3.Error as e:
            TTkLog.error(f"Error adding rows: {e}")
            return False
        self.dataChanged.emit((row,0),(self._count - row, self.columnCount()))
        self.modelChanged.emit()
        return True

    def removeRows(self, row: int, count: int = 1) -> bool:
        if row < 0 or count <= 0 or row >= self._count or row + count > self._count:
            return False

        try:
            with self._sqliteMutex:
                self._cur.execute(f"""
                    DELETE FROM {self._table}
                    WHERE {self._key} in (
                        SELECT {self._key} from {self._table}
                        {self._sort}
                        LIMIT {count} OFFSET {row}
                    )
                """)
                self._conn.commit()

                # Update The rows Count
                res = self._cur.execute(f"SELECT COUNT(*) FROM {self._table}")
                self._count = res.fetchone()[0]

                self._refreshIdMap()
        except sqlite3.Error as e:
            TTkLog.error(f"Error removing rows: {e}")
            return False
        self.dataChanged.emit((row,0),(self._count - row, self.columnCount()))
        self.modelChanged.emit()
        return True

    def insertColumns(self, column:int, count:int) -> bool:
        '''
        .. attention:: The current implementation of :py:class:`TTkTableModelSQLite3` does not supports columns operations
        '''
        TTkLog.warn("The current implementation of ModelSQLite3 does not supports columns operations")
        return False

    def removeColumns(self, column:int, count:int) -> bool:
        '''
        .. attention:: The current implementation of :py:class:`TTkTableModelSQLite3` does not supports columns operations
        '''
        TTkLog.warn("The current implementation of ModelSQLite3 does not supports columns operations")
        return False
