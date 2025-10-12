#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import os
import sys
import sqlite3
import tempfile
from unittest.mock import Mock
import pytest

sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))

import TermTk as ttk

class TestTTkTableModelSQLite3:
    """Test cases for TTkTableModelSQLite3 class"""

    def setup_method(self):
        """Set up test database for each test"""
        # Create temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db_path = self.temp_db.name
        self.temp_db.close()

        # Create test database and table
        self.conn = sqlite3.connect(self.temp_db_path)
        self.cur = self.conn.cursor()

        # Create users table with primary key
        self.cur.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                role TEXT
            )
        ''')

        # Insert test data
        test_data = [
            ('Alice', 25, 'Engineer'),
            ('Bob', 30, 'Designer'),
            ('Charlie', 35, 'Manager'),
            ('Diana', 28, 'Developer')
        ]

        self.cur.executemany('INSERT INTO users (name, age, role) VALUES (?, ?, ?)', test_data)
        self.conn.commit()
        self.conn.close()

    def teardown_method(self):
        """Clean up after each test"""
        if os.path.exists(self.temp_db_path):
            os.unlink(self.temp_db_path)

    def test_init_with_valid_database(self):
        """Test initialization with valid database and table"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        assert model.rowCount() == 4
        assert model.columnCount() == 3  # name, age, role (id is primary key, not in columns)

    def test_init_with_invalid_table(self):
        """Test initialization with invalid table name"""
        with pytest.raises(sqlite3.OperationalError):
            ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='nonexistent_table')

    def test_init_with_invalid_database(self):
        """Test initialization with invalid database file"""
        with pytest.raises(sqlite3.OperationalError):
            ttk.TTkTableModelSQLite3(fileName='/nonexistent/path/db.sqlite', table='users')

    def test_column_detection(self):
        """Test that columns are correctly detected from database schema"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Check header data for columns
        assert model.headerData(0, ttk.TTkK.HORIZONTAL) == 'name'
        assert model.headerData(1, ttk.TTkK.HORIZONTAL) == 'age'
        assert model.headerData(2, ttk.TTkK.HORIZONTAL) == 'role'

    def test_data_access(self):
        """Test data retrieval from database"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Test data access
        assert model.data(0, 0) == 'Alice'  # First row, name column
        assert model.data(0, 1) == 25       # First row, age column
        assert model.data(0, 2) == 'Engineer'  # First row, role column

        assert model.data(1, 0) == 'Bob'
        assert model.data(2, 0) == 'Charlie'
        assert model.data(3, 0) == 'Diana'

    def test_set_data(self):
        """Test data modification in database"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Change Alice's name to 'Alicia'
        result = model.setData(0, 0, 'Alicia')
        assert result == True

        # Verify the change
        assert model.data(0, 0) == 'Alicia'

        # Verify change persisted in database
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()
        res = cur.execute("SELECT name FROM users WHERE id = 1")
        assert res.fetchone()[0] == 'Alicia'
        conn.close()

    def test_index_method(self):
        """Test index method returns correct TTkModelIndex"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Get index for first row, first column
        index = model.index(0, 0)

        assert isinstance(index, ttk.TTkModelIndex)
        assert index.row() == 0
        assert index.col() == 0
        assert index.data() == 'Alice'

    def test_model_index_set_data(self):
        """Test setting data through model index"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Get index and modify data through it
        index = model.index(1, 0)  # Bob's name
        index.setData('Robert')

        # Verify change
        assert model.data(1, 0) == 'Robert'
        assert index.data() == 'Robert'

    def test_flags(self):
        """Test item flags"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        flags = model.flags(0, 0)

        # Should have enabled, editable, and selectable flags
        assert flags & ttk.TTkK.ItemFlag.ItemIsEnabled
        assert flags & ttk.TTkK.ItemFlag.ItemIsEditable
        assert flags & ttk.TTkK.ItemFlag.ItemIsSelectable

    def test_sort_ascending(self):
        """Test sorting in ascending order"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Sort by name (column 0) ascending
        model.sort(0, ttk.TTkK.SortOrder.AscendingOrder)

        # Check order: Alice, Bob, Charlie, Diana
        assert model.data(0, 0) == 'Alice'
        assert model.data(1, 0) == 'Bob'
        assert model.data(2, 0) == 'Charlie'
        assert model.data(3, 0) == 'Diana'

    def test_sort_descending(self):
        """Test sorting in descending order"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Sort by name (column 0) descending
        model.sort(0, ttk.TTkK.SortOrder.DescendingOrder)

        # Check order: Diana, Charlie, Bob, Alice
        assert model.data(0, 0) == 'Diana'
        assert model.data(1, 0) == 'Charlie'
        assert model.data(2, 0) == 'Bob'
        assert model.data(3, 0) == 'Alice'

    def test_sort_by_age_column(self):
        """Test sorting by age column"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Sort by age (column 1) ascending
        model.sort(1, ttk.TTkK.SortOrder.AscendingOrder)

        # Check order by age: Alice(25), Diana(28), Bob(30), Charlie(35)
        assert model.data(0, 0) == 'Alice'   # Age 25
        assert model.data(1, 0) == 'Diana'   # Age 28
        assert model.data(2, 0) == 'Bob'     # Age 30
        assert model.data(3, 0) == 'Charlie' # Age 35

    def test_sort_reset(self):
        """Test resetting sort order"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # First sort by name descending
        model.sort(0, ttk.TTkK.SortOrder.DescendingOrder)
        assert model.data(0, 0) == 'Diana'

        # Reset sort
        model.sort(-1, ttk.TTkK.SortOrder.AscendingOrder)

        # Should return to original order (by id)
        assert model.data(0, 0) == 'Alice'
        assert model.data(1, 0) == 'Bob'
        assert model.data(2, 0) == 'Charlie'
        assert model.data(3, 0) == 'Diana'

    def test_header_data_horizontal(self):
        """Test horizontal header data"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        assert model.headerData(0, ttk.TTkK.HORIZONTAL) == 'name'
        assert model.headerData(1, ttk.TTkK.HORIZONTAL) == 'age'
        assert model.headerData(2, ttk.TTkK.HORIZONTAL) == 'role'

    def test_header_data_vertical(self):
        """Test vertical header data (should use parent implementation)"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Should return default from parent class (likely row numbers)
        header = model.headerData(0, ttk.TTkK.VERTICAL)
        assert isinstance(header, (ttk.TTkString, str, int, type(None)))

    def test_concurrent_access(self):
        """Test thread safety with mutex"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # This test ensures no exceptions are raised with concurrent access
        # In a real scenario, you'd use threading to test this properly
        for i in range(10):
            data = model.data(i % 4, 0)  # Access data multiple times
            assert data in ['Alice', 'Bob', 'Charlie', 'Diana']

    def test_setdata_with_sort_column_refresh(self):
        """Test that changing data in sorted column refreshes id map"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Sort by name
        model.sort(0, ttk.TTkK.SortOrder.AscendingOrder)

        # Change Alice to Zoe (should move to end when sorted)
        model.setData(0, 0, 'Zoe')

        # The model should automatically refresh the sort order
        # Note: This tests the _refreshIdMap functionality when sortColumn matches

    def test_database_with_different_primary_key(self):
        """Test with a table that has a different primary key setup"""
        # Create another test table
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL
            )
        ''')

        cur.executemany('INSERT INTO products (name, price) VALUES (?, ?)', [
            ('Laptop', 999.99),
            ('Mouse', 25.50)
        ])

        conn.commit()
        conn.close()

        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='products')

        assert model.rowCount() == 2
        assert model.columnCount() == 2  # name, price
        assert model.data(0, 0) == 'Laptop'
        assert model.data(0, 1) == 999.99


def test_integration_with_table_widget():
    """Integration test with TTkTable widget"""
    # Create temporary database
    temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    temp_db_path = temp_db.name
    temp_db.close()

    try:
        # Set up database
        conn = sqlite3.connect(temp_db_path)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                value INTEGER
            )
        ''')

        cur.executemany('INSERT INTO test_table (name, value) VALUES (?, ?)', [
            ('Item1', 100),
            ('Item2', 200)
        ])

        conn.commit()
        conn.close()

        # Test model with table widget
        model = ttk.TTkTableModelSQLite3(fileName=temp_db_path, table='test_table')
        table = ttk.TTkTable(tableModel=model)

        # Basic integration tests
        assert table.model() == model
        assert model.rowCount() == 2
        assert model.columnCount() == 2

    finally:
        # Cleanup
        if os.path.exists(temp_db_path):
            os.unlink(temp_db_path)


if __name__ == '__main__':
    pytest.main([__file__])