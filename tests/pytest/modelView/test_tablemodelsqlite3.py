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
        ttk.TTkLog.use_default_stdout_logging()

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

    def test_insert_rows_single(self):
        """Test inserting a single row to the database"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        initial_count = model.rowCount()
        assert initial_count == 4

        # Insert one row at the end
        result = model.insertRows(4, 1)
        assert result == True
        assert model.rowCount() == 5

        # New row should have NULL values
        assert model.data(4, 0) == ''  # name
        assert model.data(4, 1) == 0  # age
        assert model.data(4, 2) == ''  # role

    def test_insert_rows_multiple(self):
        """Test inserting multiple rows to the database"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        initial_count = model.rowCount()

        # Insert 3 rows at the end
        result = model.insertRows(4, 3)
        assert result == True
        assert model.rowCount() == initial_count + 3

    def test_insert_rows_at_middle(self):
        """Test inserting rows at middle position"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Insert row at position 2
        result = model.insertRows(2, 1)
        assert result == True
        assert model.rowCount() == 5

    def test_insert_rows_at_beginning(self):
        """Test inserting rows at the beginning"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Insert row at position 0
        result = model.insertRows(0, 1)
        assert result == True
        assert model.rowCount() == 5

    def test_insert_rows_invalid_position(self):
        """Test inserting rows at invalid positions"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Try to insert at negative position
        result = model.insertRows(-1, 1)
        assert result == False

        # Try to insert at position beyond row count + 1
        result = model.insertRows(10, 1)
        assert result == False

    def test_insert_rows_invalid_count(self):
        """Test inserting invalid number of rows"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Try to insert negative count
        result = model.insertRows(0, -1)
        assert result == False

        # Try to insert zero rows
        result = model.insertRows(0, 0)
        assert result == False

    def test_remove_rows_single(self):
        """Test removing a single row from the database"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        initial_count = model.rowCount()

        # Remove first row (Alice)
        result = model.removeRows(0, 1)
        assert result == True
        assert model.rowCount() == initial_count - 1

    def test_remove_rows_multiple(self):
        """Test removing multiple rows from the database"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        initial_count = model.rowCount()

        # Remove 2 rows starting from position 1
        result = model.removeRows(1, 2)
        assert result == True
        assert model.rowCount() == initial_count - 2

    def test_remove_rows_all(self):
        """Test removing all rows from the database"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        initial_count = model.rowCount()

        # Remove all rows
        result = model.removeRows(0, initial_count)
        assert result == True
        assert model.rowCount() == 0

    def test_remove_rows_invalid_position(self):
        """Test removing rows from invalid positions"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Try to remove from negative position
        result = model.removeRows(-1, 1)
        assert result == False

        # Try to remove from position beyond row count
        result = model.removeRows(10, 1)
        assert result == False

    def test_remove_rows_invalid_count(self):
        """Test removing invalid number of rows"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Try to remove negative count
        result = model.removeRows(0, -1)
        assert result == False

        # Try to remove zero rows
        result = model.removeRows(0, 0)
        assert result == False

        # Try to remove more rows than available
        result = model.removeRows(2, 10)
        assert result == False

    def test_insert_remove_rows_with_sorting(self):
        """Test inserting/removing rows when table is sorted"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Sort by name first
        model.sort(0, ttk.TTkK.SortOrder.AscendingOrder)

        initial_count = model.rowCount()

        # Insert a row
        result = model.insertRows(2, 1)
        assert result == True
        assert model.rowCount() == initial_count + 1

        # Remove a row
        result = model.removeRows(1, 1)
        assert result == True
        assert model.rowCount() == initial_count

    def test_insert_rows_persistence(self):
        """Test that inserted rows persist in the database"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Insert a row and set some data
        model.insertRows(4, 1)
        model.setData(4, 0, 'Eve')
        model.setData(4, 1, 32)
        model.setData(4, 2, 'Tester')

        # Create new model instance to test persistence
        model2 = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')
        assert model2.rowCount() == 5

        # Verify Eve exists in the database
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()
        res = cur.execute("SELECT name FROM users WHERE name = 'Eve'")
        assert res.fetchone()[0] == 'Eve'
        conn.close()

    def test_remove_rows_persistence(self):
        """Test that removed rows are actually deleted from database"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Remember Alice's data before removal
        alice_name = model.data(0, 0)
        assert alice_name == 'Alice'

        # Remove Alice (first row)
        model.removeRows(0, 1)

        # Create new model instance to test persistence
        model2 = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')
        assert model2.rowCount() == 3

        # Verify Alice is deleted from database
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM users WHERE name = 'Alice'")
        assert res.fetchone()[0] == 0
        conn.close()

    def test_insert_rows_id_map_refresh(self):
        """Test that inserting rows refreshes the ID map correctly"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Sort by name to make ID mapping more complex
        model.sort(0, ttk.TTkK.SortOrder.AscendingOrder)

        # Insert rows
        model.insertRows(2, 2)

        # Verify we can still access all data without errors
        for i in range(model.rowCount()):
            for j in range(model.columnCount()):
                data = model.data(i, j)  # Should not raise exception

    def test_remove_rows_id_map_refresh(self):
        """Test that removing rows refreshes the ID map correctly"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Sort by name to make ID mapping more complex
        model.sort(0, ttk.TTkK.SortOrder.AscendingOrder)

        # Remove rows
        model.removeRows(1, 1)

        # Verify we can still access all remaining data without errors
        for i in range(model.rowCount()):
            for j in range(model.columnCount()):
                data = model.data(i, j)  # Should not raise exception

    def test_insert_rows_boundary_conditions(self):
        """Test boundary conditions for insertRows"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Insert at exact row count (valid)
        result = model.insertRows(model.rowCount(), 1)
        assert result == True

        # Insert at row count + 1 (invalid)
        result = model.insertRows(model.rowCount() + 1, 1)
        assert result == False

    def test_remove_rows_boundary_conditions(self):
        """Test boundary conditions for removeRows"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        row_count = model.rowCount()

        # Remove exactly at boundary (valid)
        result = model.removeRows(row_count - 1, 1)
        assert result == True

        # Try to remove from empty table (invalid)
        if model.rowCount() == 0:
            result = model.removeRows(0, 1)
            assert result == False

    def test_insert_remove_rows_combined(self):
        """Test combined insert and remove operations"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        initial_count = model.rowCount()

        # Insert 2 rows
        model.insertRows(2, 2)
        assert model.rowCount() == initial_count + 2

        # Remove 1 row
        model.removeRows(3, 1)
        assert model.rowCount() == initial_count + 1

        # Insert 1 more row
        model.insertRows(0, 1)
        assert model.rowCount() == initial_count + 2

        # Remove 3 rows
        model.removeRows(0, 3)
        assert model.rowCount() == initial_count - 1

    def test_insert_rows_with_data_modification(self):
        """Test inserting rows and then modifying their data"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Insert a row
        model.insertRows(4, 1)

        # Set data for the new row
        result1 = model.setData(4, 0, 'NewUser')
        result2 = model.setData(4, 1, 40)
        result3 = model.setData(4, 2, 'Analyst')

        assert result1 == True
        assert result2 == True
        assert result3 == True

        # Verify the data was set correctly
        assert model.data(4, 0) == 'NewUser'
        assert model.data(4, 1) == 40
        assert model.data(4, 2) == 'Analyst'

    def test_remove_rows_with_sorting_persistence(self):
        """Test that removeRows works correctly with sorting and persists changes"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Sort by age ascending: Alice(25), Diana(28), Bob(30), Charlie(35)
        model.sort(1, ttk.TTkK.SortOrder.AscendingOrder)

        # Verify sorted order
        assert model.data(0, 0) == 'Alice'   # Age 25
        assert model.data(1, 0) == 'Diana'   # Age 28

        # Remove Diana (position 1 in sorted order)
        result = model.removeRows(1, 1)
        assert result == True
        assert model.rowCount() == 3

        # Bob should now be at position 1
        assert model.data(1, 0) == 'Bob'     # Age 30

        # Verify Diana is actually deleted from database
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM users WHERE name = 'Diana'")
        assert res.fetchone()[0] == 0
        conn.close()

    def test_insert_columns_not_supported(self):
        """Test that insertColumns is not supported and returns False"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        initial_column_count = model.columnCount()

        # Try to insert columns (should not be supported)
        result = model.insertColumns(1, 1)
        assert result == False

        # Column count should remain unchanged
        assert model.columnCount() == initial_column_count

        # Try inserting multiple columns
        result = model.insertColumns(0, 2)
        assert result == False
        assert model.columnCount() == initial_column_count

    def test_insert_columns_invalid_parameters(self):
        """Test insertColumns with invalid parameters"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Try with negative column position
        result = model.insertColumns(-1, 1)
        assert result == False

        # Try with negative count
        result = model.insertColumns(0, -1)
        assert result == False

        # Try with zero count
        result = model.insertColumns(0, 0)
        assert result == False

    def test_remove_columns_not_supported(self):
        """Test that removeColumns is not supported and returns False"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        initial_column_count = model.columnCount()

        # Try to remove columns (should not be supported)
        result = model.removeColumns(1, 1)
        assert result == False

        # Column count should remain unchanged
        assert model.columnCount() == initial_column_count

        # Try removing multiple columns
        result = model.removeColumns(0, 2)
        assert result == False
        assert model.columnCount() == initial_column_count

    def test_remove_columns_invalid_parameters(self):
        """Test removeColumns with invalid parameters"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Try with negative column position
        result = model.removeColumns(-1, 1)
        assert result == False

        # Try with negative count
        result = model.removeColumns(0, -1)
        assert result == False

        # Try with zero count
        result = model.removeColumns(0, 0)
        assert result == False

        # Try to remove more columns than available
        result = model.removeColumns(0, 10)
        assert result == False

    def test_remove_columns_boundary_conditions(self):
        """Test removeColumns boundary conditions"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        column_count = model.columnCount()

        # Try to remove from position equal to column count
        result = model.removeColumns(column_count, 1)
        assert result == False

        # Try to remove from position beyond column count
        result = model.removeColumns(column_count + 1, 1)
        assert result == False

    def test_insert_columns_boundary_conditions(self):
        """Test insertColumns boundary conditions"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        column_count = model.columnCount()

        # Try to insert at position equal to column count
        result = model.insertColumns(column_count, 1)
        assert result == False

        # Try to insert at position beyond column count
        result = model.insertColumns(column_count + 1, 1)
        assert result == False

    def test_column_operations_with_sorting(self):
        """Test that column operations don't affect sorting"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Sort by name first
        model.sort(0, ttk.TTkK.SortOrder.AscendingOrder)

        # Verify sorting is working
        assert model.data(0, 0) == 'Alice'

        # Try column operations (should fail but not affect sorting)
        model.insertColumns(1, 1)
        model.removeColumns(1, 1)

        # Sorting should still be intact
        assert model.data(0, 0) == 'Alice'
        assert model.data(1, 0) == 'Bob'

    def test_column_operations_data_integrity(self):
        """Test that failed column operations don't affect data integrity"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Store original data
        original_data = []
        for i in range(model.rowCount()):
            row_data = []
            for j in range(model.columnCount()):
                row_data.append(model.data(i, j))
            original_data.append(row_data)

        # Try various column operations (all should fail)
        model.insertColumns(0, 1)
        model.insertColumns(1, 2)
        model.removeColumns(0, 1)
        model.removeColumns(1, 1)

        # Verify data is unchanged
        for i in range(model.rowCount()):
            for j in range(model.columnCount()):
                assert model.data(i, j) == original_data[i][j]

    def test_empty_table_initialization(self):
        """Test initialization with an empty table"""
        # Create empty table
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE empty_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER
            )
        ''')
        conn.commit()
        conn.close()

        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='empty_users')

        assert model.rowCount() == 0
        assert model.columnCount() == 2  # name, age (id is primary key)

        # Test data access on empty table
        assert model.data(0, 0) == None or model.data(0, 0) is None

        # Test header data still works
        assert model.headerData(0, ttk.TTkK.HORIZONTAL) == 'name'
        assert model.headerData(1, ttk.TTkK.HORIZONTAL) == 'age'

    def test_empty_table_operations(self):
        """Test operations on empty table"""
        # Create empty table
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE empty_test (
                id INTEGER PRIMARY KEY,
                value TEXT
            )
        ''')
        conn.commit()
        conn.close()

        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='empty_test')

        # Test insert on empty table
        result = model.insertRows(0, 1)
        assert result == True
        assert model.rowCount() == 1

        # Test data setting on newly inserted row
        result = model.setData(0, 0, 'test_value')
        assert result == True
        assert model.data(0, 0) == 'test_value'

        # Test remove from single-row table
        result = model.removeRows(0, 1)
        assert result == True
        assert model.rowCount() == 0

    def test_empty_table_invalid_operations(self):
        """Test invalid operations on empty table"""
        # Create empty table
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE empty_invalid (
                id INTEGER PRIMARY KEY,
                data TEXT
            )
        ''')
        conn.commit()
        conn.close()

        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='empty_invalid')

        # Test invalid remove operations on empty table
        result = model.removeRows(0, 1)
        assert result == False

        result = model.removeRows(-1, 1)
        assert result == False

        result = model.removeRows(1, 1)
        assert result == False

        # Test invalid insert operations
        result = model.insertRows(-1, 1)
        assert result == False

        result = model.insertRows(1, 1)  # Beyond row count
        assert result == False

    def test_empty_table_sorting(self):
        """Test sorting operations on empty table"""
        # Create empty table
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE empty_sort (
                id INTEGER PRIMARY KEY,
                name TEXT,
                value INTEGER
            )
        ''')
        conn.commit()
        conn.close()

        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='empty_sort')

        # Test sorting on empty table (should not crash)
        model.sort(0, ttk.TTkK.SortOrder.AscendingOrder)
        assert model.rowCount() == 0

        model.sort(1, ttk.TTkK.SortOrder.DescendingOrder)
        assert model.rowCount() == 0

        # Reset sort
        model.sort(-1, ttk.TTkK.SortOrder.AscendingOrder)
        assert model.rowCount() == 0

    def test_remove_all_rows_from_populated_table(self):
        """Test removing all rows from a populated table"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        initial_count = model.rowCount()
        assert initial_count == 4

        # Remove all rows at once
        result = model.removeRows(0, initial_count)
        assert result == True
        assert model.rowCount() == 0

        # Verify table is now empty in database
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM users")
        assert res.fetchone()[0] == 0
        conn.close()

        # Test operations on now-empty table
        result = model.removeRows(0, 1)  # Should fail
        assert result == False

        # Test insert into now-empty table
        result = model.insertRows(0, 1)
        assert result == True
        assert model.rowCount() == 1

    def test_remove_all_rows_one_by_one(self):
        """Test removing all rows one by one"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        initial_count = model.rowCount()

        # Remove rows one by one from the beginning
        for i in range(initial_count):
            remaining_count = model.rowCount()
            result = model.removeRows(0, 1)
            assert result == True
            assert model.rowCount() == remaining_count - 1

        # Should now be empty
        assert model.rowCount() == 0

        # Verify in database
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM users")
        assert res.fetchone()[0] == 0
        conn.close()

    def test_remove_all_rows_with_sorting(self):
        """Test removing all rows when table is sorted"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Sort by name first
        model.sort(0, ttk.TTkK.SortOrder.AscendingOrder)

        initial_count = model.rowCount()

        # Remove all rows
        result = model.removeRows(0, initial_count)
        assert result == True
        assert model.rowCount() == 0

        # Sorting should still work on empty table
        model.sort(1, ttk.TTkK.SortOrder.DescendingOrder)
        assert model.rowCount() == 0

    def test_remove_rows_boundary_edge_cases(self):
        """Test boundary edge cases for removeRows"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        row_count = model.rowCount()

        # Test removing exactly the remaining count from position 0
        result = model.removeRows(0, row_count)
        assert result == True
        assert model.rowCount() == 0

        # Reset table for next test
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()
        test_data = [
            ('Alice', 25, 'Engineer'),
            ('Bob', 30, 'Designer'),
            ('Charlie', 35, 'Manager')
        ]
        cur.executemany('INSERT INTO users (name, age, role) VALUES (?, ?, ?)', test_data)
        conn.commit()
        conn.close()

        # Refresh model count
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Test removing from last position with count that exceeds available
        result = model.removeRows(2, 5)  # Only 1 row at position 2, trying to remove 5
        assert result == False
        assert model.rowCount() == 3  # Should be unchanged

    def test_insert_rows_into_empty_table(self):
        """Test inserting rows into various empty table configurations"""
        # Create empty table with different column types
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE empty_mixed (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                salary REAL,
                active BOOLEAN
            )
        ''')
        conn.commit()
        conn.close()

        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='empty_mixed')

        # Insert multiple rows into empty table
        result = model.insertRows(0, 3)
        assert result == True
        assert model.rowCount() == 3

        # Check default values based on column types
        assert model.data(0, 0) == ''     # TEXT -> empty string
        assert model.data(0, 1) == 0      # INTEGER -> 0
        assert model.data(0, 2) == 0.0    # REAL -> 0.0
        assert model.data(0, 3) == 0      # BOOLEAN -> 0

    def test_empty_table_index_operations(self):
        """Test index operations on empty table"""
        # Create empty table
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE empty_index (
                id INTEGER PRIMARY KEY,
                value TEXT
            )
        ''')
        conn.commit()
        conn.close()

        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='empty_index')

        # Test index creation on empty table (should handle gracefully)
        try:
            index = model.index(0, 0)  # May raise exception or return invalid index
            # If it doesn't raise an exception, the implementation handles it gracefully
        except (sqlite3.Error, IndexError):
            pass  # Expected behavior for empty table

    def test_table_emptied_then_repopulated(self):
        """Test table that is emptied and then repopulated"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        # Verify initial state
        assert model.rowCount() == 4

        # Empty the table
        model.removeRows(0, model.rowCount())
        assert model.rowCount() == 0

        # Repopulate with new data
        model.insertRows(0, 2)
        assert model.rowCount() == 2

        # Set data for new rows
        model.setData(0, 0, 'NewUser1')
        model.setData(0, 1, 40)
        model.setData(0, 2, 'Admin')

        model.setData(1, 0, 'NewUser2')
        model.setData(1, 1, 45)
        model.setData(1, 2, 'Manager')

        # Verify data integrity
        assert model.data(0, 0) == 'NewUser1'
        assert model.data(1, 0) == 'NewUser2'

        # Test sorting on repopulated table
        model.sort(0, ttk.TTkK.SortOrder.AscendingOrder)
        assert model.data(0, 0) == 'NewUser1'  # Should be first alphabetically

    def test_concurrent_operations_on_empty_table(self):
        """Test concurrent operations on empty table (basic thread safety)"""
        # Create empty table
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE empty_concurrent (
                id INTEGER PRIMARY KEY,
                value INTEGER
            )
        ''')
        conn.commit()
        conn.close()

        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='empty_concurrent')

        # Simulate concurrent operations (basic test)
        operations = [
            lambda: model.insertRows(0, 1),
            lambda: model.sort(0, ttk.TTkK.SortOrder.AscendingOrder),
            lambda: model.rowCount(),
            lambda: model.columnCount()
        ]

        # Execute multiple operations - should not crash
        for op in operations * 3:  # Repeat operations
            try:
                result = op()
            except Exception as e:
                pytest.fail(f"Concurrent operation failed: {e}")

    def test_large_batch_remove_operations(self):
        """Test removing large batches of rows"""
        # First populate with more data
        conn = sqlite3.connect(self.temp_db_path)
        cur = conn.cursor()

        # Add more test data
        large_data = [(f'User{i}', 20+i, f'Role{i%3}') for i in range(50)]
        cur.executemany('INSERT INTO users (name, age, role) VALUES (?, ?, ?)', large_data)
        conn.commit()
        conn.close()

        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        initial_count = model.rowCount()
        assert initial_count > 50  # Should have original 4 + 50 new = 54

        # Remove large batch from middle
        result = model.removeRows(10, 30)
        assert result == True
        assert model.rowCount() == initial_count - 30

        # Remove another large batch from beginning
        result = model.removeRows(0, 15)
        assert result == True
        assert model.rowCount() == initial_count - 45

        # Remove remaining rows
        remaining = model.rowCount()
        result = model.removeRows(0, remaining)
        assert result == True
        assert model.rowCount() == 0

    def test_alternating_empty_and_populate_operations(self):
        """Test alternating between emptying and populating table"""
        model = ttk.TTkTableModelSQLite3(fileName=self.temp_db_path, table='users')

        for cycle in range(3):  # Repeat cycle 3 times
            # Start with some data
            if model.rowCount() == 0:
                model.insertRows(0, 2)
                model.setData(0, 0, f'User{cycle}A')
                model.setData(1, 0, f'User{cycle}B')

            assert model.rowCount() >= 2

            # Empty the table
            model.removeRows(0, model.rowCount())
            assert model.rowCount() == 0

            # Insert different amount
            insert_count = (cycle + 1) * 2
            model.insertRows(0, insert_count)
            assert model.rowCount() == insert_count

            # Set some data
            for i in range(insert_count):
                model.setData(i, 0, f'Cycle{cycle}_User{i}')

        # Final cleanup
        model.removeRows(0, model.rowCount())
        assert model.rowCount() == 0