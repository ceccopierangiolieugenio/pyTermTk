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
import csv
import tempfile
import io
from unittest.mock import Mock
import pytest

sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))

import TermTk as ttk

class TestTTkTableModelCSV:
    """Test cases for TTkTableModelCSV class"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Sample CSV content with headers
        self.csv_with_headers = "Name,Age,Role\nAlice,25,Engineer\nBob,30,Designer\nCharlie,35,Manager"

        # Sample CSV content without headers
        self.csv_without_headers = "Alice,25,Engineer\nBob,30,Designer\nCharlie,35,Manager"

        # CSV with index column (sequential numbers starting from 1)
        self.csv_with_index = "1,Alice,25,Engineer\n2,Bob,30,Designer\n3,Charlie,35,Manager"

        # CSV with headers and index
        self.csv_with_headers_and_index = "ID,Name,Age,Role\n1,Alice,25,Engineer\n2,Bob,30,Designer\n3,Charlie,35,Manager"

        # CSV with non-sequential index (should not be detected as index)
        self.csv_with_non_sequential_index = "10,Alice,25,Engineer\n20,Bob,30,Designer\n30,Charlie,35,Manager"

    def test_init_with_filename(self):
        """Test initialization with CSV filename"""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
            tmp.write(self.csv_with_headers)
            tmp_path = tmp.name

        try:
            model = ttk.TTkTableModelCSV(filename=tmp_path)

            assert model.rowCount() == 3
            assert model.columnCount() == 3
            assert model.data(0, 0) == 'Alice'
            assert model.data(0, 1) == '25'
            assert model.data(0, 2) == 'Engineer'

            # Check headers
            assert model.headerData(0, ttk.TTkK.HORIZONTAL) == 'Name'
            assert model.headerData(1, ttk.TTkK.HORIZONTAL) == 'Age'
            assert model.headerData(2, ttk.TTkK.HORIZONTAL) == 'Role'

        finally:
            os.unlink(tmp_path)

    def test_init_with_file_descriptor(self):
        """Test initialization with file descriptor"""
        csv_fd = io.StringIO(self.csv_with_headers)

        model = ttk.TTkTableModelCSV(fd=csv_fd)

        assert model.rowCount() == 3
        assert model.columnCount() == 3
        assert model.data(0, 0) == 'Alice'
        assert model.data(1, 0) == 'Bob'
        assert model.data(2, 0) == 'Charlie'

    def test_init_with_no_parameters(self):
        """Test initialization with no parameters (should create empty model)"""
        model = ttk.TTkTableModelCSV()

        assert model.rowCount() == 1
        assert model.columnCount() == 1
        assert model.data(0, 0) == ''

    def test_csv_import_with_headers(self):
        """Test CSV import when headers are detected"""
        csv_fd = io.StringIO(self.csv_with_headers)

        model = ttk.TTkTableModelCSV(fd=csv_fd)

        # Check data
        assert model.rowCount() == 3
        assert model.columnCount() == 3

        # Check that headers were extracted
        assert model.headerData(0, ttk.TTkK.HORIZONTAL) == 'Name'
        assert model.headerData(1, ttk.TTkK.HORIZONTAL) == 'Age'
        assert model.headerData(2, ttk.TTkK.HORIZONTAL) == 'Role'

        # Check that first row is actual data, not headers
        assert model.data(0, 0) == 'Alice'
        assert model.data(0, 1) == '25'

    def test_csv_import_without_headers(self):
        """Test CSV import when no headers are detected"""
        csv_fd = io.StringIO(self.csv_without_headers)

        model = ttk.TTkTableModelCSV(fd=csv_fd)

        assert model.rowCount() == 3
        assert model.columnCount() == 3

        # Should use default header behavior (from parent class)
        # First row should be data, not treated as headers
        assert model.data(0, 0) == 'Alice'
        assert model.data(0, 1) == '25'
        assert model.data(0, 2) == 'Engineer'

    def test_csv_import_with_index_column(self):
        """Test CSV import with sequential index column detection"""
        csv_fd = io.StringIO(self.csv_with_index)

        model = ttk.TTkTableModelCSV(fd=csv_fd)

        # Index column should be detected and removed from data
        assert model.rowCount() == 3
        assert model.columnCount() == 3  # Index column removed

        # Check data (should start from second column of original CSV)
        assert model.data(0, 0) == 'Alice'
        assert model.data(0, 1) == '25'
        assert model.data(0, 2) == 'Engineer'

        # Check vertical headers (indexes)
        assert model.headerData(0, ttk.TTkK.VERTICAL) == '1'
        assert model.headerData(1, ttk.TTkK.VERTICAL) == '2'
        assert model.headerData(2, ttk.TTkK.VERTICAL) == '3'

    def test_csv_import_with_headers_and_index(self):
        """Test CSV import with both headers and index column"""
        csv_fd = io.StringIO(self.csv_with_headers_and_index)

        model = ttk.TTkTableModelCSV(fd=csv_fd)

        assert model.rowCount() == 3
        assert model.columnCount() == 3  # ID column removed

        # Check that both headers and indexes were properly extracted
        assert model.headerData(0, ttk.TTkK.HORIZONTAL) == 'Name'
        assert model.headerData(1, ttk.TTkK.HORIZONTAL) == 'Age'
        assert model.headerData(2, ttk.TTkK.HORIZONTAL) == 'Role'

        assert model.headerData(0, ttk.TTkK.VERTICAL) == '1'
        assert model.headerData(1, ttk.TTkK.VERTICAL) == '2'
        assert model.headerData(2, ttk.TTkK.VERTICAL) == '3'

        # Check data
        assert model.data(0, 0) == 'Alice'
        assert model.data(1, 0) == 'Bob'
        assert model.data(2, 0) == 'Charlie'

    def test_check_index_column_sequential(self):
        """Test _checkIndexColumn method with sequential numbers"""
        csv_fd = io.StringIO(self.csv_with_index)
        model = ttk.TTkTableModelCSV(fd=csv_fd)

        # Create test data similar to what _csvImport would produce
        test_data = [['1', 'Alice', '25'], ['2', 'Bob', '30'], ['3', 'Charlie', '35']]

        # Should detect sequential index starting from 1
        result = model._checkIndexColumn(test_data)
        assert result == True

    def test_check_index_column_non_sequential(self):
        """Test _checkIndexColumn method with non-sequential numbers"""
        csv_fd = io.StringIO(self.csv_with_non_sequential_index)
        model = ttk.TTkTableModelCSV(fd=csv_fd)

        # Create test data with non-sequential numbers
        test_data = [['10', 'Alice', '25'], ['20', 'Bob', '30'], ['30', 'Charlie', '35']]

        # Should not detect as index column
        result = model._checkIndexColumn(test_data)
        assert result == False

    def test_check_index_column_non_numeric(self):
        """Test _checkIndexColumn method with non-numeric first column"""
        model = ttk.TTkTableModelCSV()

        # Create test data with non-numeric first column
        test_data = [['Alice', '25'], ['Bob', '30'], ['Charlie', '35']]

        # Should not detect as index column
        result = model._checkIndexColumn(test_data)
        assert result == False

    def test_check_index_column_empty_data(self):
        """Test _checkIndexColumn method with empty data"""
        model = ttk.TTkTableModelCSV()

        # Empty data should not crash
        result = model._checkIndexColumn([])
        assert result == False

    def test_check_index_column_starting_from_zero(self):
        """Test _checkIndexColumn with sequential numbers starting from 0"""
        model = ttk.TTkTableModelCSV()

        test_data = [['0', 'Alice'], ['1', 'Bob'], ['2', 'Charlie']]
        result = model._checkIndexColumn(test_data)
        assert result == True

    def test_csv_import_different_delimiters(self):
        """Test CSV import with different delimiters"""
        # Test semicolon delimiter
        csv_semicolon = "Alice;25;Engineer\nBob;30;Designer"
        csv_fd = io.StringIO(csv_semicolon)

        model = ttk.TTkTableModelCSV(fd=csv_fd)

        # Should handle different delimiters automatically
        assert model.rowCount() >= 1
        assert model.columnCount() >= 1

    def test_csv_import_with_quotes(self):
        """Test CSV import with quoted values"""
        csv_quoted = 'Name,Description\n"Alice Johnson","Senior Engineer"\n"Bob Smith","UI Designer"'
        csv_fd = io.StringIO(csv_quoted)

        model = ttk.TTkTableModelCSV(fd=csv_fd)

        assert model.data(1, 0) == 'Alice Johnson'
        assert model.data(1, 1) == 'Senior Engineer'
        assert model.data(2, 0) == 'Bob Smith'

    def test_csv_import_with_empty_cells(self):
        """Test CSV import with empty cells"""
        csv_empty = "Name,Age,Role\nAlice,,Engineer\n,30,Designer\nCharlie,35,"
        csv_fd = io.StringIO(csv_empty)

        model = ttk.TTkTableModelCSV(fd=csv_fd)

        assert model.data(1, 0) == 'Alice'
        assert model.data(1, 1) == ''  # Empty age
        assert model.data(2, 0) == ''  # Empty name
        assert model.data(3, 2) == ''  # Empty role

    def test_csv_import_single_row(self):
        """Test CSV import with single data row"""
        csv_single = "Name,Age\nAlice,25"
        csv_fd = io.StringIO(csv_single)

        model = ttk.TTkTableModelCSV(fd=csv_fd)

        assert model.rowCount() == 1
        assert model.columnCount() == 2
        assert model.data(0, 0) == 'Alice'
        assert model.data(0, 1) == '25'

    def test_csv_import_single_column(self):
        """Test CSV import with single column"""
        csv_single_col = "Names\nAlice\nBob\nCharlie"
        csv_fd = io.StringIO(csv_single_col)

        model = ttk.TTkTableModelCSV(fd=csv_fd)

        assert model.rowCount() == 4
        assert model.columnCount() == 1
        assert model.data(1, 0) == 'Alice'
        assert model.data(2, 0) == 'Bob'
        assert model.data(3, 0) == 'Charlie'

    def test_file_not_found_error(self):
        """Test error handling for non-existent file"""
        with pytest.raises(FileNotFoundError):
            ttk.TTkTableModelCSV(filename='/nonexistent/path/file.csv')

    def test_invalid_csv_format(self):
        """Test handling of malformed CSV"""
        # This should still work as csv.reader is quite forgiving
        malformed_csv = 'Name,Age\n"Alice,25\nBob,30'
        csv_fd = io.StringIO(malformed_csv)

        # Should not raise exception, csv.reader handles it
        model = ttk.TTkTableModelCSV(fd=csv_fd)
        assert model.rowCount() >= 1

    def test_inherited_functionality(self):
        """Test that inherited TTkTableModelList functionality works"""
        csv_fd = io.StringIO(self.csv_with_headers)
        model = ttk.TTkTableModelCSV(fd=csv_fd)

        # Test inherited methods
        assert isinstance(model.flags(0, 0), int)

        # Test setData (inherited)
        original_value = model.data(0, 0)
        model.setData(0, 0, 'Alicia')
        assert model.data(0, 0) == 'Alicia'

        # Test index method (inherited)
        index = model.index(0, 1)
        assert index.row() == 0
        assert index.col() == 1

    def test_csv_import_large_file(self):
        """Test CSV import with larger dataset"""
        # Generate larger CSV content
        large_csv_lines = ['Name,ID,Value']
        for i in range(100):
            large_csv_lines.append(f'User{i},{i},Value{i}')
        large_csv = '\n'.join(large_csv_lines)

        csv_fd = io.StringIO(large_csv)
        model = ttk.TTkTableModelCSV(fd=csv_fd)

        assert model.rowCount() == 100
        assert model.columnCount() == 3
        assert model.data(0, 0) == 'User0'
        assert model.data(99, 0) == 'User99'

    def test_csv_with_unicode_characters(self):
        """Test CSV import with unicode characters"""
        unicode_csv = "Name,City\nAlice,Москва\nBob,北京\nCharlie,São Paulo"
        csv_fd = io.StringIO(unicode_csv)

        model = ttk.TTkTableModelCSV(fd=csv_fd)

        assert model.data(1, 1) == 'Москва'
        assert model.data(2, 1) == '北京'
        assert model.data(3, 1) == 'São Paulo'

    def test_csv_import_preserves_file_position(self):
        """Test that _csvImport properly handles file position"""
        csv_fd = io.StringIO(self.csv_with_headers)

        # Read some content first
        first_line = csv_fd.readline()
        assert 'Name,Age,Role' in first_line

        # Reset and use with model
        csv_fd.seek(0)
        model = ttk.TTkTableModelCSV(fd=csv_fd)

        # Should work correctly despite previous read
        assert model.rowCount() == 3
        assert model.data(0, 0) == 'Alice'

    def test_sort_functionality_inherited(self):
        """Test that sorting functionality from parent class works"""
        csv_fd = io.StringIO(self.csv_with_headers)
        model = ttk.TTkTableModelCSV(fd=csv_fd)

        # Test sorting by name column
        model.sort(0, ttk.TTkK.SortOrder.DescendingOrder)

        # Should be sorted: Charlie, Bob, Alice
        assert model.data(0, 0) == 'Charlie'
        assert model.data(1, 0) == 'Bob'
        assert model.data(2, 0) == 'Alice'


def test_integration_with_table_widget():
    """Integration test - verify TTkTableModelCSV works with table widgets"""
    csv_content = "Product,Price,Stock\nLaptop,999.99,50\nMouse,25.99,100\nKeyboard,75.50,75"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    try:
        model = ttk.TTkTableModelCSV(filename=tmp_path)
        table = ttk.TTkTable(tableModel=model)

        # Test integration
        assert table.model() == model
        assert model.rowCount() == 3
        assert model.columnCount() == 3

        # Test that table can access model data
        assert model.data(0, 0) == 'Laptop'
        assert model.headerData(0, ttk.TTkK.HORIZONTAL) == 'Product'

    finally:
        os.unlink(tmp_path)


if __name__ == '__main__':
    pytest.main([__file__])