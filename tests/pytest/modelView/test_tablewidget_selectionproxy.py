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
import pytest
from unittest.mock import Mock

sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))
import TermTk as ttk
from TermTk.TTkWidgets.TTkModelView.tablewidget import _SelectionProxy

class TestSelectionProxy:
    """Test cases for _SelectionProxy class"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.proxy = _SelectionProxy()

        # Mock flags function that returns selectable for all cells
        def mock_flags_all_selectable(row, col):
            return ttk.TTkK.ItemFlag.ItemIsSelectable

        # Mock flags function that returns non-selectable for specific cells
        def mock_flags_some_non_selectable(row, col):
            if row == 1 and col == 1:
                return ttk.TTkK.ItemFlag.NoItemFlags
            return ttk.TTkK.ItemFlag.ItemIsSelectable

        self.mock_flags_all = mock_flags_all_selectable
        self.mock_flags_some = mock_flags_some_non_selectable

    def test_init_default(self):
        """Test default initialization"""
        proxy = _SelectionProxy()

        assert proxy._cols == 0
        assert proxy._rows == 0
        assert proxy._selected_2d_list == []

    def test_resize_valid_dimensions(self):
        """Test resizing with valid dimensions"""
        self.proxy.resize(3, 4)

        assert self.proxy._cols == 3
        assert self.proxy._rows == 4
        assert len(self.proxy._selected_2d_list) == 4
        assert all(len(row) == 3 for row in self.proxy._selected_2d_list)
        assert all(all(not cell for cell in row) for row in self.proxy._selected_2d_list)

    def test_resize_zero_dimensions(self):
        """Test resizing with zero dimensions"""
        self.proxy.resize(0, 0)

        assert self.proxy._cols == 0
        assert self.proxy._rows == 0
        assert self.proxy._selected_2d_list == []

    def test_resize_negative_dimensions(self):
        """Test resizing with negative dimensions raises ValueError"""
        with pytest.raises(ValueError, match="unexpected negative value"):
            self.proxy.resize(-1, 3)

        with pytest.raises(ValueError, match="unexpected negative value"):
            self.proxy.resize(3, -1)

    def test_update_model(self):
        """Test updateModel method"""
        self.proxy.updateModel(cols=3, rows=4, flags=self.mock_flags_all)

        assert self.proxy._cols == 3
        assert self.proxy._rows == 4
        assert self.proxy._flags == self.mock_flags_all

    def test_clear_with_data(self):
        """Test clearing selection with existing data"""
        self.proxy.resize(3, 4)
        # Manually set some selections
        self.proxy._selected_2d_list[1][2] = True
        self.proxy._selected_2d_list[3][0] = True

        self.proxy.clear()

        assert all(all(not cell for cell in row) for row in self.proxy._selected_2d_list)

    def test_clear_selection_alias(self):
        """Test that clearSelection is alias for clear"""
        self.proxy.resize(3, 4)
        self.proxy._selected_2d_list[1][1] = True

        self.proxy.clearSelection()

        assert all(all(not cell for cell in row) for row in self.proxy._selected_2d_list)

    def test_select_all_with_all_selectable(self):
        """Test selectAll with all cells selectable"""
        self.proxy.updateModel(cols=3, rows=2, flags=self.mock_flags_all)

        self.proxy.selectAll()

        assert all(all(cell for cell in row) for row in self.proxy._selected_2d_list)

    def test_select_all_with_some_non_selectable(self):
        """Test selectAll with some cells non-selectable"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_some)

        self.proxy.selectAll()

        # Cell (1,1) should not be selected due to flags
        assert not self.proxy._selected_2d_list[1][1]
        # Other cells should be selected
        assert self.proxy._selected_2d_list[0][0]
        assert self.proxy._selected_2d_list[2][2]

    def test_select_row_valid(self):
        """Test selecting a valid row"""
        self.proxy.updateModel(cols=4, rows=3, flags=self.mock_flags_all)

        self.proxy.selectRow(1)

        # Row 1 should be fully selected
        assert all(self.proxy._selected_2d_list[1])
        # Other rows should not be selected
        assert not any(self.proxy._selected_2d_list[0])
        assert not any(self.proxy._selected_2d_list[2])

    def test_select_row_with_non_selectable_cells(self):
        """Test selecting row with non-selectable cells"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_some)

        self.proxy.selectRow(1)

        # Cell (1,1) should not be selected due to flags
        assert not self.proxy._selected_2d_list[1][1]
        # Other cells in row 1 should be selected
        assert self.proxy._selected_2d_list[1][0]
        assert self.proxy._selected_2d_list[1][2]

    def test_select_row_invalid_indices(self):
        """Test selecting invalid row indices"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_all)

        # Should not crash or change anything
        self.proxy.selectRow(-1)
        self.proxy.selectRow(5)

        assert not any(any(row) for row in self.proxy._selected_2d_list)

    def test_select_column_valid(self):
        """Test selecting a valid column"""
        self.proxy.updateModel(cols=4, rows=3, flags=self.mock_flags_all)

        self.proxy.selectColumn(2)

        # Column 2 should be selected in all rows
        assert all(self.proxy._selected_2d_list[row][2] for row in range(3))
        # Other columns should not be selected
        for row in range(3):
            assert not self.proxy._selected_2d_list[row][0]
            assert not self.proxy._selected_2d_list[row][1]
            assert not self.proxy._selected_2d_list[row][3]

    def test_select_column_with_non_selectable_cells(self):
        """Test selecting column with non-selectable cells"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_some)

        self.proxy.selectColumn(1)

        # Cell (1,1) should not be selected due to flags
        assert not self.proxy._selected_2d_list[1][1]
        # Other cells in column 1 should be selected
        assert self.proxy._selected_2d_list[0][1]
        assert self.proxy._selected_2d_list[2][1]

    def test_select_column_invalid_indices(self):
        """Test selecting invalid column indices"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_all)

        # Should not crash or change anything
        self.proxy.selectColumn(-1)
        self.proxy.selectColumn(5)

        assert not any(any(row) for row in self.proxy._selected_2d_list)

    def test_unselect_row_valid(self):
        """Test unselecting a valid row"""
        self.proxy.updateModel(cols=4, rows=3, flags=self.mock_flags_all)
        self.proxy.selectAll()

        self.proxy.unselectRow(1)

        # Row 1 should be unselected
        assert not any(self.proxy._selected_2d_list[1])
        # Other rows should remain selected
        assert all(self.proxy._selected_2d_list[0])
        assert all(self.proxy._selected_2d_list[2])

    def test_unselect_row_invalid_indices(self):
        """Test unselecting invalid row indices"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_all)
        self.proxy.selectAll()
        original_state = [row[:] for row in self.proxy._selected_2d_list]

        # Should not crash or change anything
        self.proxy.unselectRow(-1)
        self.proxy.unselectRow(5)

        assert self.proxy._selected_2d_list == original_state

    def test_unselect_column_valid(self):
        """Test unselecting a valid column"""
        self.proxy.updateModel(cols=4, rows=3, flags=self.mock_flags_all)
        self.proxy.selectAll()

        self.proxy.unselectColumn(2)

        # Column 2 should be unselected in all rows
        assert not any(self.proxy._selected_2d_list[row][2] for row in range(3))
        # Other columns should remain selected
        for row in range(3):
            assert self.proxy._selected_2d_list[row][0]
            assert self.proxy._selected_2d_list[row][1]
            assert self.proxy._selected_2d_list[row][3]

    def test_unselect_column_invalid_indices(self):
        """Test unselecting invalid column indices"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_all)
        self.proxy.selectAll()
        original_state = [row[:] for row in self.proxy._selected_2d_list]

        # Should not crash or change anything
        self.proxy.unselectColumn(-1)
        self.proxy.unselectColumn(5)

        assert self.proxy._selected_2d_list == original_state

    def test_set_selection_select(self):
        """Test setSelection with Select flag"""
        self.proxy.updateModel(cols=5, rows=4, flags=self.mock_flags_all)

        self.proxy.setSelection(pos=(1, 1), size=(2, 2), flags=ttk.TTkK.TTkItemSelectionModel.Select)

        # Selected area should be (1,1) to (2,2)
        assert self.proxy._selected_2d_list[1][1]
        assert self.proxy._selected_2d_list[1][2]
        assert self.proxy._selected_2d_list[2][1]
        assert self.proxy._selected_2d_list[2][2]
        # Outside area should not be selected
        assert not self.proxy._selected_2d_list[0][0]
        assert not self.proxy._selected_2d_list[3][3]

    def test_set_selection_clear(self):
        """Test setSelection with Clear flag"""
        self.proxy.updateModel(cols=4, rows=3, flags=self.mock_flags_all)
        self.proxy.selectAll()

        self.proxy.setSelection(pos=(1, 1), size=(2, 1), flags=ttk.TTkK.TTkItemSelectionModel.Clear)

        # Specified area should be cleared
        assert not self.proxy._selected_2d_list[1][1]
        assert not self.proxy._selected_2d_list[1][2]
        # Other areas should remain selected
        assert self.proxy._selected_2d_list[0][0]
        assert self.proxy._selected_2d_list[2][3]

    def test_set_selection_deselect(self):
        """Test setSelection with Deselect flag"""
        self.proxy.updateModel(cols=4, rows=3, flags=self.mock_flags_all)
        self.proxy.selectAll()

        self.proxy.setSelection(pos=(0, 0), size=(2, 2), flags=ttk.TTkK.TTkItemSelectionModel.Deselect)

        # Specified area should be deselected
        assert not self.proxy._selected_2d_list[0][0]
        assert not self.proxy._selected_2d_list[0][1]
        assert not self.proxy._selected_2d_list[1][0]
        assert not self.proxy._selected_2d_list[1][1]
        # Other areas should remain selected
        assert self.proxy._selected_2d_list[2][2]
        assert self.proxy._selected_2d_list[2][3]

    def test_set_selection_boundary_conditions(self):
        """Test setSelection with boundary conditions"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_all)

        # Selection extending beyond boundaries should be clipped
        self.proxy.setSelection(pos=(2, 2), size=(3, 3), flags=ttk.TTkK.TTkItemSelectionModel.Select)

        # Only valid cells should be selected
        assert self.proxy._selected_2d_list[2][2]
        # Should not crash or cause index errors

    def test_is_row_selected_all_selectable(self):
        """Test isRowSelected with all selectable cells"""
        self.proxy.updateModel(cols=4, rows=3, flags=self.mock_flags_all)
        self.proxy.selectRow(1)

        assert self.proxy.isRowSelected(1)
        assert not self.proxy.isRowSelected(0)
        assert not self.proxy.isRowSelected(2)

    def test_is_row_selected_with_non_selectable_cells(self):
        """Test isRowSelected with non-selectable cells"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_some)
        self.proxy.selectRow(1)

        # Row 1 should be considered selected even though cell (1,1) is not selectable
        # because isRowSelected only considers selectable cells
        assert self.proxy.isRowSelected(1)

    def test_is_row_selected_invalid_indices(self):
        """Test isRowSelected with invalid indices"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_all)

        assert not self.proxy.isRowSelected(-1)
        assert not self.proxy.isRowSelected(5)

    def test_is_col_selected_all_selectable(self):
        """Test isColSelected with all selectable cells"""
        self.proxy.updateModel(cols=4, rows=3, flags=self.mock_flags_all)
        self.proxy.selectColumn(2)

        assert self.proxy.isColSelected(2)
        assert not self.proxy.isColSelected(0)
        assert not self.proxy.isColSelected(3)

    def test_is_col_selected_with_non_selectable_cells(self):
        """Test isColSelected with non-selectable cells"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_some)
        self.proxy.selectColumn(1)

        # Column 1 should be considered selected even though cell (1,1) is not selectable
        assert self.proxy.isColSelected(1)

    def test_is_col_selected_invalid_indices(self):
        """Test isColSelected with invalid indices"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_all)

        assert not self.proxy.isColSelected(-1)
        assert not self.proxy.isColSelected(5)

    def test_is_cell_selected_valid(self):
        """Test isCellSelected with valid coordinates"""
        self.proxy.updateModel(cols=4, rows=3, flags=self.mock_flags_all)
        self.proxy._selected_2d_list[1][2] = True

        assert self.proxy.isCellSelected(2, 1)
        assert not self.proxy.isCellSelected(1, 1)
        assert not self.proxy.isCellSelected(0, 0)

    def test_is_cell_selected_invalid_indices(self):
        """Test isCellSelected with invalid indices"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_all)

        assert not self.proxy.isCellSelected(-1, 1)
        assert not self.proxy.isCellSelected(1, -1)
        assert not self.proxy.isCellSelected(5, 1)
        assert not self.proxy.isCellSelected(1, 5)

    def test_iterate_selected_empty(self):
        """Test iterateSelected with no selections"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_all)

        selections = list(self.proxy.iterateSelected())

        assert selections == []

    def test_iterate_selected_with_selections(self):
        """Test iterateSelected with some selections"""
        self.proxy.updateModel(cols=4, rows=3, flags=self.mock_flags_all)
        self.proxy._selected_2d_list[0][1] = True
        self.proxy._selected_2d_list[1][2] = True
        self.proxy._selected_2d_list[2][3] = True

        selections = list(self.proxy.iterateSelected())

        expected = [(0, 1), (1, 2), (2, 3)]
        assert selections == expected

    def test_iterate_selected_by_rows_empty(self):
        """Test iterateSelectedByRows with no selections"""
        self.proxy.updateModel(cols=3, rows=3, flags=self.mock_flags_all)

        selections = list(self.proxy.iterateSelectedByRows())

        assert selections == []

    def test_iterate_selected_by_rows_with_selections(self):
        """Test iterateSelectedByRows with selections across multiple rows"""
        self.proxy.updateModel(cols=4, rows=4, flags=self.mock_flags_all)
        # Row 0: select columns 1, 2
        self.proxy._selected_2d_list[0][1] = True
        self.proxy._selected_2d_list[0][2] = True
        # Row 1: no selections
        # Row 2: select column 0
        self.proxy._selected_2d_list[2][0] = True
        # Row 3: select columns 1, 3
        self.proxy._selected_2d_list[3][1] = True
        self.proxy._selected_2d_list[3][3] = True

        selections = list(self.proxy.iterateSelectedByRows())

        expected = [
            [(0, 1), (0, 2)],  # Row 0
            [(2, 0)],          # Row 2
            [(3, 1), (3, 3)]   # Row 3
        ]
        assert selections == expected

    def test_iterate_selected_by_rows_single_row_multiple_cols(self):
        """Test iterateSelectedByRows with single row, multiple columns"""
        self.proxy.updateModel(cols=5, rows=3, flags=self.mock_flags_all)
        self.proxy._selected_2d_list[1][0] = True
        self.proxy._selected_2d_list[1][2] = True
        self.proxy._selected_2d_list[1][4] = True

        selections = list(self.proxy.iterateSelectedByRows())

        expected = [[(1, 0), (1, 2), (1, 4)]]
        assert selections == expected

    def test_empty_proxy_operations(self):
        """Test operations on empty proxy (0 rows, 0 columns)"""
        proxy = _SelectionProxy()

        # All operations should handle empty state gracefully
        proxy.clear()
        proxy.clearSelection()
        proxy.selectAll()
        proxy.selectRow(0)
        proxy.selectColumn(0)
        proxy.unselectRow(0)
        proxy.unselectColumn(0)

        assert not proxy.isRowSelected(0)
        assert not proxy.isColSelected(0)
        assert not proxy.isCellSelected(0, 0)
        assert list(proxy.iterateSelected()) == []
        assert list(proxy.iterateSelectedByRows()) == []

    def test_single_cell_proxy(self):
        """Test operations on single cell proxy (1 row, 1 column)"""
        self.proxy.updateModel(cols=1, rows=1, flags=self.mock_flags_all)

        # Select the single cell
        self.proxy.selectAll()

        assert self.proxy.isRowSelected(0)
        assert self.proxy.isColSelected(0)
        assert self.proxy.isCellSelected(0, 0)

        selections = list(self.proxy.iterateSelected())
        assert selections == [(0, 0)]

        row_selections = list(self.proxy.iterateSelectedByRows())
        assert row_selections == [[(0, 0)]]

    def test_complex_selection_scenario(self):
        """Test complex selection scenario with mixed operations"""
        self.proxy.updateModel(cols=5, rows=4, flags=self.mock_flags_all)

        # Select all
        self.proxy.selectAll()

        # Unselect row 1
        self.proxy.unselectRow(1)

        # Unselect column 2
        self.proxy.unselectColumn(2)

        # Set specific selection
        self.proxy.setSelection(pos=(3, 1), size=(1, 2), flags=ttk.TTkK.TTkItemSelectionModel.Select)

        # Verify final state
        # Row 0: all except column 2
        assert self.proxy.isCellSelected(0, 0)
        assert self.proxy.isCellSelected(1, 0)
        assert not self.proxy.isCellSelected(2, 0)  # Column 2 unselected
        assert self.proxy.isCellSelected(3, 0)
        assert self.proxy.isCellSelected(4, 0)

        # Row 1: only column 3 (from setSelection)
        assert not self.proxy.isCellSelected(0, 1)  # Row 1 was unselected
        assert not self.proxy.isCellSelected(1, 1)
        assert not self.proxy.isCellSelected(2, 1)  # Column 2 unselected
        assert self.proxy.isCellSelected(3, 1)      # Added by setSelection
        assert not self.proxy.isCellSelected(4, 1)  # Row 1 was unselected

        # # Row 2: column 3 (from setSelection)
        # assert not self.proxy.isCellSelected(0, 2)  # Row was affected by other operations
        # assert not self.proxy.isCellSelected(1, 2)
        # assert not self.proxy.isCellSelected(2, 2)  # Column 2 unselected
        # assert self.proxy.isCellSelected(3, 2)      # Added by setSelection
        # assert not self.proxy.isCellSelected(4, 2)

    def test_flags_integration(self):
        """Test integration with different flag functions"""
        # Test with all non-selectable flags
        def no_flags(row, col):
            return ttk.TTkK.ItemFlag.NoItemFlags

        self.proxy.updateModel(cols=3, rows=3, flags=no_flags)
        self.proxy.selectAll()

        # Nothing should be selected
        assert not any(any(row) for row in self.proxy._selected_2d_list)

        # Test with selective flags
        def selective_flags(row, col):
            if row % 2 == 0 and col % 2 == 0:  # Only even positions
                return ttk.TTkK.ItemFlag.ItemIsSelectable
            return ttk.TTkK.ItemFlag.NoItemFlags

        self.proxy.updateModel(cols=4, rows=4, flags=selective_flags)
        self.proxy.selectAll()

        # Only cells at even positions should be selected
        for row in range(4):
            for col in range(4):
                if row % 2 == 0 and col % 2 == 0:
                    assert self.proxy._selected_2d_list[row][col]
                else:
                    assert not self.proxy._selected_2d_list[row][col]

    def test_selection_state_consistency(self):
        """Test that selection state remains consistent across operations"""
        self.proxy.updateModel(cols=4, rows=3, flags=self.mock_flags_all)

        # Perform various operations and check consistency
        self.proxy.selectRow(0)
        initial_selected = sum(sum(row) for row in self.proxy._selected_2d_list)

        self.proxy.selectColumn(1)
        # Should have added new selections
        current_selected = sum(sum(row) for row in self.proxy._selected_2d_list)
        assert current_selected >= initial_selected

        self.proxy.clearSelection()
        assert sum(sum(row) for row in self.proxy._selected_2d_list) == 0

        # Verify dimensions remain correct
        assert len(self.proxy._selected_2d_list) == 3
        assert all(len(row) == 4 for row in self.proxy._selected_2d_list)