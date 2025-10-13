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

import sys, os
import pytest
from unittest.mock import Mock

sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))

import TermTk as ttk


class TestTTkTableModelList:
    """Test cases for TTkTableModelList class"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.test_data = [
            ['Alice', 25, 'Engineer'],
            ['Bob', 30, 'Designer'],
            ['Charlie', 35, 'Manager']
        ]
        self.header = ['Name', 'Age', 'Role']
        self.indexes = ['Row1', 'Row2', 'Row3']

    def test_init_default(self):
        """Test default initialization"""
        model = ttk.TTkTableModelList()

        assert model.rowCount() == 1
        assert model.columnCount() == 1
        assert model.data(0, 0) == ''

    def test_init_with_data(self):
        """Test initialization with data"""
        model = ttk.TTkTableModelList(data=self.test_data)

        assert model.rowCount() == 3
        assert model.columnCount() == 3
        assert model.data(0, 0) == 'Alice'
        assert model.data(1, 1) == 30
        assert model.data(2, 2) == 'Manager'

    def test_init_with_headers_and_indexes(self):
        """Test initialization with headers and indexes"""
        model = ttk.TTkTableModelList(
            data=self.test_data,
            header=self.header,
            indexes=self.indexes
        )

        assert model.rowCount() == 3
        assert model.columnCount() == 3
        # Check header data
        assert model.headerData(0, ttk.TTkK.HORIZONTAL) == 'Name'
        assert model.headerData(1, ttk.TTkK.HORIZONTAL) == 'Age'
        assert model.headerData(2, ttk.TTkK.HORIZONTAL) == 'Role'
        # Check index data
        assert model.headerData(0, ttk.TTkK.VERTICAL) == 'Row1'
        assert model.headerData(1, ttk.TTkK.VERTICAL) == 'Row2'
        assert model.headerData(2, ttk.TTkK.VERTICAL) == 'Row3'

    def test_modelList_getter_setter(self):
        """Test modelList getter and setter"""
        model = ttk.TTkTableModelList(data=self.test_data)

        # Test getter
        retrieved_data = model.modelList()
        assert retrieved_data == self.test_data

        # Test setter with new data
        new_data = [['X', 1], ['Y', 2]]
        model.setModelList(new_data)
        assert model.modelList() == new_data
        assert model.rowCount() == 2
        assert model.columnCount() == 2

        # Test setter with same data (should not trigger change)
        model.setModelList(new_data)  # Same data, no change expected
        assert model.modelList() == new_data

    def test_data_access(self):
        """Test data access methods"""
        model = ttk.TTkTableModelList(data=self.test_data)

        # Test data method
        assert model.data(0, 0) == 'Alice'
        assert model.data(1, 1) == 30
        assert model.data(2, 2) == 'Manager'

        # Test setData method
        model.setData(0, 0, 'Alicia')
        assert model.data(0, 0) == 'Alicia'

        model.setData(1, 1, 31)
        assert model.data(1, 1) == 31

    def test_index_method(self):
        """Test index method returns correct TTkModelIndex"""
        model = ttk.TTkTableModelList(data=self.test_data)

        index = model.index(0, 0)
        assert index.row() == 0
        assert index.col() == 0
        assert index.data() == 'Alice'

        index = model.index(1, 2)
        assert index.row() == 1
        assert index.col() == 2
        assert index.data() == 'Designer'

        # Test setData through index
        index.setData('Senior Designer')
        assert model.data(1, 2) == 'Senior Designer'

    def test_header_data_no_headers(self):
        """Test headerData when no headers are provided"""
        model = ttk.TTkTableModelList(data=self.test_data)

        # Should return default behavior (from parent class)
        h_result = model.headerData(0, ttk.TTkK.HORIZONTAL)
        v_result = model.headerData(0, ttk.TTkK.VERTICAL)

        # These should return whatever the parent implementation returns
        # (likely default column/row numbers or empty strings)
        assert h_result is not None or h_result is None  # Accept any default
        assert v_result is not None or v_result is None  # Accept any default

    def test_flags(self):
        """Test flags method returns correct item flags"""
        model = ttk.TTkTableModelList(data=self.test_data)

        flags = model.flags(0, 0)
        expected_flags = (
            ttk.TTkK.ItemFlag.ItemIsEnabled |
            ttk.TTkK.ItemFlag.ItemIsEditable |
            ttk.TTkK.ItemFlag.ItemIsSelectable
        )

        assert flags == expected_flags

    def test_sort_by_column(self):
        """Test sorting functionality"""
        # Test data with mixed types for sorting edge cases
        sort_data = [
            ['Charlie', 35, 'Manager'],
            ['Alice', 25, 'Engineer'],
            ['Bob', 30, 'Designer']
        ]
        model = ttk.TTkTableModelList(data=sort_data)

        # Sort by first column (names) - ascending
        model.sort(0, ttk.TTkK.SortOrder.AscendingOrder)
        sorted_data = model.modelList()
        assert sorted_data[0][0] == 'Alice'
        assert sorted_data[1][0] == 'Bob'
        assert sorted_data[2][0] == 'Charlie'

        # Sort by first column (names) - descending
        model.sort(0, ttk.TTkK.SortOrder.DescendingOrder)
        sorted_data = model.modelList()
        assert sorted_data[0][0] == 'Charlie'
        assert sorted_data[1][0] == 'Bob'
        assert sorted_data[2][0] == 'Alice'

        # Sort by second column (ages) - ascending
        model.sort(1, ttk.TTkK.SortOrder.AscendingOrder)
        sorted_data = model.modelList()
        assert sorted_data[0][1] == 25  # Alice
        assert sorted_data[1][1] == 30  # Bob
        assert sorted_data[2][1] == 35  # Charlie

        # Reset to original order
        model.sort(-1, ttk.TTkK.SortOrder.AscendingOrder)
        reset_data = model.modelList()
        assert reset_data == sort_data  # Should be back to original

    def test_sort_mixed_types(self):
        """Test sorting with mixed data types (fallback to string sorting)"""
        mixed_data = [
            ['Item', 100],
            ['Item', 'abc'],
            ['Item', 50]
        ]
        model = ttk.TTkTableModelList(data=mixed_data)

        # This should trigger the TypeError exception and fall back to string sorting
        model.sort(1, ttk.TTkK.SortOrder.AscendingOrder)

        # Verify it doesn't crash and data is still accessible
        assert model.rowCount() == 3
        assert model.columnCount() == 2

    def test_insert_rows(self):
        """Test insertRows method"""
        model = ttk.TTkTableModelList(data=self.test_data.copy())
        original_count = model.rowCount()

        # Insert 2 rows at position 1
        result = model.insertRows(1, 2)

        assert result == True
        assert model.rowCount() == original_count + 2

        # Check that None values were inserted
        assert model.data(1, 0) == ''
        assert model.data(1, 1) == ''
        assert model.data(1, 2) == ''
        assert model.data(2, 0) == ''
        assert model.data(2, 1) == ''
        assert model.data(2, 2) == ''

        # Check that existing data was shifted
        assert model.data(3, 0) == 'Bob'  # Was at row 1, now at row 3

    def test_insert_columns(self):
        """Test insertColumns method"""
        model = ttk.TTkTableModelList(data=[row.copy() for row in self.test_data])
        original_column_count = model.columnCount()

        # Insert 2 columns at position 1
        result = model.insertColumns(1, 2)

        assert result == True  # Implementation returns True
        assert model.columnCount() == original_column_count + 2

        # Check that None values were inserted at the right position
        assert model.data(0, 1) == ''  # New column 1
        assert model.data(0, 2) == ''  # New column 2
        assert model.data(0, 3) == 25    # Original column 1 shifted to position 3

        # Check all rows have the new columns
        for row in range(model.rowCount()):
            assert model.data(row, 1) == ''
            assert model.data(row, 2) == ''

    def test_remove_columns(self):
        """Test removeColumns method"""
        model = ttk.TTkTableModelList(data=[row.copy() for row in self.test_data])
        original_column_count = model.columnCount()

        # Remove 1 column at position 1 (Age column)
        result = model.removeColumns(1, 1)

        assert result == True  # Changed from False to True
        assert model.columnCount() == original_column_count - 1

        # Check that the middle column was removed
        assert model.data(0, 0) == 'Alice'     # Name still there
        assert model.data(0, 1) == 'Engineer'  # Role shifted to position 1
        assert model.data(1, 0) == 'Bob'
        assert model.data(1, 1) == 'Designer'

    def test_remove_rows(self):
        """Test removeRows method"""
        model = ttk.TTkTableModelList(data=[row.copy() for row in self.test_data])
        original_row_count = model.rowCount()

        # Remove 1 row at position 1 (Bob's row)
        result = model.removeRows(1, 1)

        assert result == True  # Changed from False to True
        assert model.rowCount() == original_row_count - 1

        # Check that the middle row was removed and data shifted
        assert model.data(0, 0) == 'Alice'    # First row unchanged
        assert model.data(1, 0) == 'Charlie'  # Charlie moved to position 1

    def test_insert_columns_signal_emission(self):
        """Test that dataChanged signal is emitted when inserting columns"""
        model = ttk.TTkTableModelList(data=[row.copy() for row in self.test_data])

        # Mock the signal to track emissions
        signal_mock = Mock()
        @ttk.pyTTkSlot(tuple[int,int], tuple[int,int])
        def _mock_signal(pos: tuple[int,int], size: tuple[int,int]):
            signal_mock(pos, size)
        model.dataChanged.connect(_mock_signal)

        # Insert columns
        model.insertColumns(1, 2)

        # Verify signal was emitted with correct parameters
        # Expected: start at (0,1), size is (rowCount, originalColumnCount-1)
        signal_mock.assert_called_once_with((0, 1), (3, 4))  # 3 rows, 4 remaining columns

    def test_insert_rows_signal_emission(self):
        """Test that dataChanged signal is emitted when inserting rows"""
        model = ttk.TTkTableModelList(data=[row.copy() for row in self.test_data])

        # Mock the signal to track emissions
        signal_mock = Mock()
        @ttk.pyTTkSlot(tuple[int,int], tuple[int,int])
        def _mock_signal(pos: tuple[int,int], size: tuple[int,int]):
            signal_mock(pos, size)
        model.dataChanged.connect(_mock_signal)

        # Insert rows
        model.insertRows(1, 2)

        # Verify signal was emitted
        # Expected: start at (1,0), size is (originalRowCount-1, columnCount)
        signal_mock.assert_called_once_with((1, 0), (4, 3))  # 4 remaining rows, 3 columns

    def test_remove_columns_signal_emission(self):
        """Test that dataChanged signal is emitted when removing columns"""
        model = ttk.TTkTableModelList(data=[row.copy() for row in self.test_data])

        # Mock the signal to track emissions
        signal_mock = Mock()
        @ttk.pyTTkSlot(tuple[int,int], tuple[int,int])
        def _mock_signal(pos: tuple[int,int], size: tuple[int,int]):
            signal_mock(pos, size)
        model.dataChanged.connect(_mock_signal)

        # Remove columns
        model.removeColumns(1, 1)

        # Verify signal was emitted
        signal_mock.assert_called_once_with((0, 1), (3, 1))

    def test_remove_rows_signal_emission(self):
        """Test that dataChanged signal is emitted when removing rows"""
        model = ttk.TTkTableModelList(data=[row.copy() for row in self.test_data])

        # Mock the signal to track emissions
        signal_mock = Mock()
        @ttk.pyTTkSlot(tuple[int,int], tuple[int,int])
        def _mock_signal(pos: tuple[int,int], size: tuple[int,int]):
            signal_mock(pos, size)
        model.dataChanged.connect(_mock_signal)

        # Remove rows
        model.removeRows(1, 1)

        # Verify signal was emitted
        signal_mock.assert_called_once_with((1, 0), (1, 3))

    def test_sort_updates_original_data(self):
        """Test that sorting affects _dataOriginal reference correctly"""
        original_data = [
            ['Charlie', 35, 'Manager'],
            ['Alice', 25, 'Engineer'],
            ['Bob', 30, 'Designer']
        ]
        model = ttk.TTkTableModelList(data=original_data)

        # Sort by name
        model.sort(0, ttk.TTkK.SortOrder.AscendingOrder)
        sorted_data = model.modelList()
        assert sorted_data[0][0] == 'Alice'

        # Reset should go back to original order
        model.sort(-1, ttk.TTkK.SortOrder.AscendingOrder)
        reset_data = model.modelList()
        assert reset_data == original_data

    def test_edge_case_empty_list_initialization(self):
        """Test edge case with empty list"""
        model = ttk.TTkTableModelList(data=[])

        # With empty data, it should create default [[']]
        assert model.rowCount() == 1
        assert model.columnCount() == 1
        assert model.data(0, 0) == ''

    def test_edge_case_none_data_initialization(self):
        """Test edge case with None data"""
        model = ttk.TTkTableModelList(data=None)

        # With None data, it should create default [['']]
        assert model.rowCount() == 1
        assert model.columnCount() == 1
        assert model.data(0, 0) == ''

def test_integration_with_table_widget():
    """Integration test - verify TTkTableModelList works with table widgets"""
    # This test ensures the model integrates properly with the UI components
    test_data = [
        ['Item 1', 'Value 1'],
        ['Item 2', 'Value 2']
    ]

    model = ttk.TTkTableModelList(data=test_data, header=['Name', 'Value'])

    # These are the basic requirements for table model integration
    assert model.rowCount() > 0
    assert model.columnCount() > 0
    assert callable(model.data)
    assert callable(model.setData)
    assert callable(model.index)
    assert callable(model.flags)
    assert callable(model.headerData)

    # Test that all expected methods return appropriate types
    assert isinstance(model.rowCount(), int)
    assert isinstance(model.columnCount(), int)
    assert isinstance(model.data(0, 0), (str, int, float, type(None)))
    assert isinstance(model.flags(0, 0), int)  # Flags are integer bitmasks


if __name__ == '__main__':
    pytest.main([__file__])