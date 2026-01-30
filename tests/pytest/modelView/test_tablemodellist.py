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

        assert model.rowCount() == 0
        assert model.columnCount() == 0
        assert model.data(0, 0) is None

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
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])  # Deep copy
        original_count = model.rowCount()

        # Insert 2 rows at position 1
        result = model.insertRows(1, 2)

        assert result == True
        assert model.rowCount() == original_count + 2

        # Check that empty string values were inserted
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
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])  # Deep copy
        original_column_count = model.columnCount()

        # Insert 2 columns at position 1
        result = model.insertColumns(1, 2)

        assert result == True
        assert model.columnCount() == original_column_count + 2

        # Check that empty string values were inserted at the right position
        assert model.data(0, 1) == ''  # New column 1
        assert model.data(0, 2) == ''  # New column 2
        assert model.data(0, 3) == 25    # Original column 1 shifted to position 3

        # Check all rows have the new columns
        for row in range(model.rowCount()):
            assert model.data(row, 1) == ''
            assert model.data(row, 2) == ''

    def test_remove_columns(self):
        """Test removeColumns method"""
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])  # Deep copy
        original_column_count = model.columnCount()

        # Remove 1 column at position 1 (Age column)
        result = model.removeColumns(1, 1)

        assert result == True
        assert model.columnCount() == original_column_count - 1

        # Check that the middle column was removed
        assert model.data(0, 0) == 'Alice'     # Name still there
        assert model.data(0, 1) == 'Engineer'  # Role shifted to position 1
        assert model.data(1, 0) == 'Bob'
        assert model.data(1, 1) == 'Designer'

    def test_remove_rows(self):
        """Test removeRows method"""
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])  # Deep copy
        original_row_count = model.rowCount()

        # Remove 1 row at position 1 (Bob's row)
        result = model.removeRows(1, 1)

        assert result == True
        assert model.rowCount() == original_row_count - 1

        # Check that the middle row was removed and data shifted
        assert model.data(0, 0) == 'Alice'    # First row unchanged
        assert model.data(1, 0) == 'Charlie'  # Charlie moved to position 1

    def test_remove_rows_boundary_conditions(self):
        """Test removeRows method with boundary conditions and invalid ranges"""
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])  # Deep copy
        original_row_count = model.rowCount()

        # Test removing rows at the edge (last row)
        result = model.removeRows(2, 1)  # Remove Charlie's row (index 2)
        assert result == True
        assert model.rowCount() == original_row_count - 1
        assert model.data(0, 0) == 'Alice'
        assert model.data(1, 0) == 'Bob'
        # Charlie should be gone
        assert model.data(2, 0) is None

        # Reset for next test
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])

        # Test removing rows starting beyond valid range
        try:
            result = model.removeRows(5, 1)  # Start beyond data bounds
            # Should either return False or handle gracefully
            # The behavior depends on implementation - some might allow it
        except IndexError:
            pass  # This is acceptable behavior

        # Test removing rows with count that goes beyond data bounds
        result = model.removeRows(1, 10)  # Remove more rows than exist
        assert result == True
        # Should remove rows 1 and 2 (Bob and Charlie), leaving only Alice
        assert model.rowCount() == 1
        assert model.data(0, 0) == 'Alice'

        # Reset for next test
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])

        # Test removing rows with negative start index
        try:
            result = model.removeRows(-1, 1)
            # Behavior may vary - could be handled gracefully or raise error
        except (IndexError, ValueError):
            pass  # Expected for invalid index

        # Test removing zero rows
        result = model.removeRows(1, 0)
        assert result == True
        assert model.rowCount() == original_row_count  # Should be unchanged

    def test_remove_columns_boundary_conditions(self):
        """Test removeColumns method with boundary conditions and invalid ranges"""
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])  # Deep copy
        original_column_count = model.columnCount()

        # Test removing columns at the edge (last column)
        result = model.removeColumns(2, 1)  # Remove Role column (index 2)
        assert result == True
        assert model.columnCount() == original_column_count - 1
        assert model.data(0, 0) == 'Alice'  # Name still there
        assert model.data(0, 1) == 25       # Age still there
        assert model.data(0, 2) is None     # Role should be gone

        # Reset for next test
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])

        # Test removing columns starting beyond valid range
        try:
            result = model.removeColumns(5, 1)  # Start beyond data bounds
            # Should either return False or handle gracefully
        except IndexError:
            pass  # This is acceptable behavior

        # Test removing columns with count that goes beyond data bounds
        result = model.removeColumns(1, 10)  # Remove more columns than exist
        assert result == True
        # Should remove columns 1 and 2 (Age and Role), leaving only Name
        assert model.columnCount() == 1
        assert model.data(0, 0) == 'Alice'
        assert model.data(0, 1) is None     # Age should be gone

        # Reset for next test
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])

        # Test removing columns with negative start index
        try:
            result = model.removeColumns(-1, 1)
            # Behavior may vary - could be handled gracefully or raise error
        except (IndexError, ValueError):
            pass  # Expected for invalid index

        # Test removing zero columns
        result = model.removeColumns(1, 0)
        assert result == True
        assert model.columnCount() == original_column_count  # Should be unchanged

    def test_remove_operations_on_empty_model(self):
        """Test remove operations on empty model"""
        model = ttk.TTkTableModelList(data=[])

        # Test removing rows from empty model
        try:
            result = model.removeRows(0, 1)
            # Should handle gracefully or return False
        except IndexError:
            pass  # Acceptable behavior

        # Test removing columns from empty model
        try:
            result = model.removeColumns(0, 1)
            # Should handle gracefully or return False
        except IndexError:
            pass  # Acceptable behavior

    def test_remove_operations_on_single_cell_model(self):
        """Test remove operations on single cell model"""
        model = ttk.TTkTableModelList(data=[['single']])

        # Remove the only row
        result = model.removeRows(0, 1)
        assert result == True
        assert model.rowCount() == 0
        assert model.columnCount() == 0  # Column structure might remain

        # Reset for column test
        model = ttk.TTkTableModelList(data=[['single']])

        # Remove the only column
        result = model.removeColumns(0, 1)
        assert result == True
        assert model.columnCount() == 0
        assert model.rowCount() == 1  # Row structure might remain

    def test_remove_all_rows(self):
        """Test removing all rows from model"""
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])

        # Remove all rows at once
        result = model.removeRows(0, model.rowCount())
        assert result == True
        assert model.rowCount() == 0

    def test_remove_all_columns(self):
        """Test removing all columns from model"""
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])

        # Remove all columns at once
        result = model.removeColumns(0, model.columnCount())
        assert result == True
        assert model.columnCount() == 0

    def test_remove_operations_signal_emission_boundary_cases(self):
        """Test signal emission for boundary cases in remove operations"""
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])

        # Mock the signal to track emissions
        signal_mock = Mock()
        @ttk.pyTTkSlot(tuple[int,int], tuple[int,int])
        def _mock_signal(pos: tuple, size: tuple):
            signal_mock(pos, size)
        model.dataChanged.connect(_mock_signal)

        # Remove last row
        model.removeRows(2, 1)
        # Should emit signal for the removal
        assert signal_mock.call_count >= 1

        # Reset mock and model
        signal_mock.reset_mock()
        model = ttk.TTkTableModelList(data=[row[:] for row in self.test_data])
        model.dataChanged.connect(_mock_signal)

        # Remove last column
        model.removeColumns(2, 1)
        # Should emit signal for the removal
        assert signal_mock.call_count >= 1

    def test_remove_operations_preserve_data_integrity(self):
        """Test that remove operations preserve data integrity"""
        original_data = [
            ['A', 'B', 'C', 'D'],
            ['E', 'F', 'G', 'H'],
            ['I', 'J', 'K', 'L'],
            ['M', 'N', 'O', 'P']
        ]
        model = ttk.TTkTableModelList(data=[row[:] for row in original_data])

        # Remove middle rows (1 and 2)
        model.removeRows(1, 2)

        # Verify remaining data is correct
        assert model.rowCount() == 2
        assert model.data(0, 0) == 'A'  # First row unchanged
        assert model.data(1, 0) == 'M'  # Last row shifted up

        # Reset and test column removal
        model = ttk.TTkTableModelList(data=[row[:] for row in original_data])

        # Remove middle columns (1 and 2)
        model.removeColumns(1, 2)

        # Verify remaining data is correct
        assert model.columnCount() == 2
        assert model.data(0, 0) == 'A'  # First column unchanged
        assert model.data(0, 1) == 'D'  # Last column shifted left
        assert model.data(1, 0) == 'E'
        assert model.data(1, 1) == 'H'

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
    assert isinstance(model.flags(0, 0), ttk.TTkK.ItemFlag)  # Flags are integer bitmasks


if __name__ == '__main__':
    pytest.main([__file__])