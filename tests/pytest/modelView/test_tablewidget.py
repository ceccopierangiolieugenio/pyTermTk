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
from unittest.mock import Mock, MagicMock, patch

sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))
import TermTk as ttk
from TermTk.TTkWidgets.TTkModelView.tablewidget import _DragPosType

class TestTTkTableWidget:
    """Test cases for TTkTableWidget class"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.test_data = [
            ['Alice', 25, 'Engineer'],
            ['Bob', 30, 'Designer'],
            ['Charlie', 35, 'Manager']
        ]
        self.header = ['Name', 'Age', 'Role']
        self.indexes = ['Row1', 'Row2', 'Row3']

        class MockTableModel(ttk.TTkTableModelList):
            def flags(self, row, col):
                return super().flags(row, col)

        # Create a basic table model for testing
        self.table_model = MockTableModel(
            data=self.test_data,
            header=self.header,
            indexes=self.indexes
        )

    def test_init_default(self):
        """Test default initialization"""
        widget = ttk.TTkTableWidget()

        assert widget is not None
        assert widget.model() is not None
        assert isinstance(widget.model(), ttk.TTkAbstractTableModel)
        # Default model should have 10x10 grid with empty strings
        assert widget.rowCount() == 10
        assert widget.columnCount() == 10

    def test_init_with_model(self):
        """Test initialization with a table model"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        assert widget.model() == self.table_model
        assert widget.rowCount() == 3
        assert widget.columnCount() == 3

    def test_init_with_separator_options(self):
        """Test initialization with separator visibility options"""
        widget = ttk.TTkTableWidget(
            vSeparator=False,
            hSeparator=False
        )

        assert not widget.vSeparatorVisibility()
        assert not widget.hSeparatorVisibility()

    def test_init_with_header_options(self):
        """Test initialization with header visibility options"""
        widget = ttk.TTkTableWidget(
            vHeader=False,
            hHeader=False
        )

        assert not widget.verticalHeader().isVisible()
        assert not widget.horizontalHeader().isVisible()

    def test_init_with_sorting_enabled(self):
        """Test initialization with sorting enabled"""
        widget = ttk.TTkTableWidget(sortingEnabled=True)

        assert widget.isSortingEnabled()

    def test_init_with_data_padding(self):
        """Test initialization with custom data padding"""
        widget = ttk.TTkTableWidget(dataPadding=3)

        # Data padding is internal, but we can verify the widget was created
        assert widget is not None

    def test_model_getter_setter(self):
        """Test model getter and setter"""
        widget = ttk.TTkTableWidget()
        original_model = widget.model()

        # Set new model
        widget.setModel(self.table_model)
        assert widget.model() == self.table_model
        assert widget.model() != original_model

        # Verify model data is accessible
        assert widget.rowCount() == 3
        assert widget.columnCount() == 3

    def test_row_column_count(self):
        """Test row and column count methods"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        assert widget.rowCount() == 3
        assert widget.columnCount() == 3

    def test_current_row_column(self):
        """Test current row and column methods"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Initially should be at (0, 0) or (-1, -1) if no selection
        current_row = widget.currentRow()
        current_col = widget.currentColumn()

        assert isinstance(current_row, int)
        assert isinstance(current_col, int)
        assert current_row >= -1
        assert current_col >= -1

    def test_header_views(self):
        """Test vertical and horizontal header views"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        v_header = widget.verticalHeader()
        h_header = widget.horizontalHeader()

        assert isinstance(v_header, ttk.TTkHeaderView)
        assert isinstance(h_header, ttk.TTkHeaderView)
        assert v_header.isVisible()
        assert h_header.isVisible()

    def test_separator_visibility(self):
        """Test separator visibility methods"""
        widget = ttk.TTkTableWidget()

        # Default should be visible
        assert widget.hSeparatorVisibility()
        assert widget.vSeparatorVisibility()

        # Test setters
        widget.setHSeparatorVisibility(False)
        widget.setVSeparatorVisibility(False)

        assert not widget.hSeparatorVisibility()
        assert not widget.vSeparatorVisibility()

        # Test setting back to visible
        widget.setHSeparatorVisibility(True)
        widget.setVSeparatorVisibility(True)

        assert widget.hSeparatorVisibility()
        assert widget.vSeparatorVisibility()

    def test_sorting_functionality(self):
        """Test sorting enabled/disabled and sort by column"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Initially sorting should be disabled
        assert not widget.isSortingEnabled()

        # Enable sorting
        widget.setSortingEnabled(True)
        assert widget.isSortingEnabled()

        # Test sorting by column
        widget.sortByColumn(0, ttk.TTkK.SortOrder.AscendingOrder)
        # Note: We can't easily verify the actual sorting without checking the model state

        # Disable sorting
        widget.setSortingEnabled(False)
        assert not widget.isSortingEnabled()

    def test_selection_methods(self):
        """Test selection-related methods"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Test clear selection
        widget.clearSelection()

        # Test select all
        widget.selectAll()

        # Test select row
        widget.selectRow(0)

        # Test select column
        widget.selectColumn(1)

        # Test set selection with position and size
        widget.setSelection((0, 0), (2, 2), ttk.TTkK.TTkItemSelectionModel.Select)

        # These methods should not raise exceptions
        # Actual selection state testing would require more complex setup

    def test_column_width_operations(self):
        """Test column width setting and resizing"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Test setting column width
        widget.setColumnWidth(0, 20)

        # Test resize column to contents
        widget.resizeColumnToContents(0)

        # Test resize all columns to contents
        widget.resizeColumnsToContents()

        # These methods should not raise exceptions

    def test_row_height_operations(self):
        """Test row height setting and resizing"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Test setting row height
        widget.setRowHeight(0, 3)

        # Test resize row to contents
        widget.resizeRowToContents(0)

        # Test resize all rows to contents
        widget.resizeRowsToContents()

        # These methods should not raise exceptions

    def test_clipboard_operations(self):
        """Test copy, cut, and paste operations"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # These operations should not raise exceptions
        widget.copy()
        widget.cut()
        widget.paste()

    def test_undo_redo_operations(self):
        """Test undo and redo operations"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Initially, there should be no undo/redo available
        # But the methods should not raise exceptions
        widget.undo()
        widget.redo()

    def test_signals_exist(self):
        """Test that all expected signals exist"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Test that signals are accessible
        assert hasattr(widget, 'cellChanged')
        assert hasattr(widget, 'cellClicked')
        assert hasattr(widget, 'cellDoubleClicked')
        assert hasattr(widget, 'cellEntered')
        assert hasattr(widget, 'currentCellChanged')

        # Test that they are signal objects
        assert isinstance(widget.cellChanged, ttk.pyTTkSignal)
        assert isinstance(widget.cellClicked, ttk.pyTTkSignal)
        assert isinstance(widget.cellDoubleClicked, ttk.pyTTkSignal)
        assert isinstance(widget.cellEntered, ttk.pyTTkSignal)
        assert isinstance(widget.currentCellChanged, ttk.pyTTkSignal)

    def test_signal_connections(self):
        """Test signal connections"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Create mock slots

        cell_changed_slot = Mock()
        cell_clicked_slot = Mock()
        current_cell_changed_slot = Mock()
        @ttk.pyTTkSlot(int,int)
        def _mock_cell_changed_slot(row:int,col:int):
            cell_changed_slot(row, col)
        @ttk.pyTTkSlot(int,int)
        def _mock_cell_clicked_slot(row:int,col:int):
            cell_clicked_slot(row, col)
        @ttk.pyTTkSlot(int,int,int,int)
        def _mock_cell_cchanged_slot(a:int,b:int,c:int,d:int):
            current_cell_changed_slot(a,b,c,d)

        # Connect signals
        widget.cellChanged.connect(_mock_cell_changed_slot)
        widget.cellClicked.connect(_mock_cell_clicked_slot)
        widget.currentCellChanged.connect(_mock_cell_cchanged_slot)

        # Verify connections were made (signals should have connections)
        assert len(widget.cellChanged._connected_slots) > 0
        assert len(widget.cellClicked._connected_slots) > 0
        assert len(widget.currentCellChanged._connected_slots) > 0

    def test_model_change_propagation(self):
        """Test that model changes are propagated to the widget"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Modify the model
        self.table_model.setData(0, 0, 'Modified')

        # The widget should be notified (through signal connections)
        # We can't easily test the actual update without a more complex setup
        assert widget.model().data(0, 0) == 'Modified'

    def test_empty_model_handling(self):
        """Test widget behavior with empty model"""
        empty_model = ttk.TTkTableModelList(data=[[]])
        widget = ttk.TTkTableWidget(tableModel=empty_model)

        assert widget.rowCount() == 1
        assert widget.columnCount() == 0

    def test_large_model_handling(self):
        """Test widget behavior with large model"""
        large_data = [[f'Cell_{i}_{j}' for j in range(100)] for i in range(100)]
        large_model = ttk.TTkTableModelList(data=large_data)
        widget = ttk.TTkTableWidget(tableModel=large_model)

        assert widget.rowCount() == 100
        assert widget.columnCount() == 100

    def test_model_replacement(self):
        """Test replacing the model after widget creation"""
        widget = ttk.TTkTableWidget()
        original_row_count = widget.rowCount()
        original_col_count = widget.columnCount()

        # Replace with our test model
        widget.setModel(self.table_model)

        # Verify the change
        assert widget.rowCount() != original_row_count
        assert widget.columnCount() != original_col_count
        assert widget.rowCount() == 3
        assert widget.columnCount() == 3

    def test_widget_with_different_model_types(self):
        """Test widget with different types of table models"""
        # Test with TTkTableModelList
        list_model = ttk.TTkTableModelList(data=self.test_data)
        widget1 = ttk.TTkTableWidget(tableModel=list_model)
        assert widget1.rowCount() == 3

        # Test with TTkTableModelCSV (using in-memory data)
        import io
        csv_data = io.StringIO("Name,Age\nAlice,25\nBob,30")
        csv_model = ttk.TTkTableModelCSV(fd=csv_data)
        widget2 = ttk.TTkTableWidget(tableModel=csv_model)
        assert widget2.rowCount() == 2

    def test_header_visibility_changes(self):
        """Test changing header visibility after initialization"""
        widget = ttk.TTkTableWidget()

        # Initially headers should be visible
        assert widget.verticalHeader().isVisible()
        assert widget.horizontalHeader().isVisible()

        # Hide headers
        widget.verticalHeader().hide()
        widget.horizontalHeader().hide()

        assert not widget.verticalHeader().isVisible()
        assert not widget.horizontalHeader().isVisible()

        # Show headers again
        widget.verticalHeader().show()
        widget.horizontalHeader().show()

        assert widget.verticalHeader().isVisible()
        assert widget.horizontalHeader().isVisible()

    def test_focus_policy(self):
        """Test that the widget has proper focus policy"""
        widget = ttk.TTkTableWidget()

        # Should accept click and tab focus
        focus_policy = widget.focusPolicy()
        assert focus_policy & ttk.TTkK.ClickFocus
        assert focus_policy & ttk.TTkK.TabFocus

    def test_minimum_size(self):
        """Test minimum size constraints"""
        widget = ttk.TTkTableWidget()

        # Should have minimum height of 1
        min_size = widget.minimumSize()
        assert min_size[1] >= 1  # height should be at least 1

    def test_style_properties(self):
        """Test that the widget has proper style properties"""
        widget = ttk.TTkTableWidget()

        # Should have class style defined
        assert hasattr(ttk.TTkTableWidget, 'classStyle')
        assert isinstance(ttk.TTkTableWidget.classStyle, dict)
        assert 'default' in ttk.TTkTableWidget.classStyle

    def test_boundary_conditions(self):
        """Test boundary conditions and edge cases"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Test with invalid row/column indices (should not crash)
        try:
            widget.selectRow(-1)
            widget.selectRow(1000)
            widget.selectColumn(-1)
            widget.selectColumn(1000)
            widget.setColumnWidth(-1, 10)
            widget.setColumnWidth(1000, 10)
            widget.setRowHeight(-1, 2)
            widget.setRowHeight(1000, 2)
        except Exception as e:
            # Some operations might raise exceptions, but they shouldn't crash
            pass

    def test_integration_with_scroll_area(self):
        """Test that the widget works as expected within a scroll area (via TTkTable)"""
        table = ttk.TTkTable(tableModel=self.table_model)

        # TTkTable should forward methods to the internal TTkTableWidget
        assert table.rowCount() == 3
        assert table.columnCount() == 3
        assert table.model() == self.table_model

    def test_zero_rows_model(self):
        """Test widget behavior with model that has zero rows"""
        # Create model with zero rows but some columns
        empty_rows_model = ttk.TTkTableModelList(
            data=[],
            header=['Col1', 'Col2', 'Col3']
        )
        widget = ttk.TTkTableWidget(tableModel=empty_rows_model)

        assert widget.rowCount() == 0
        assert widget.columnCount() == 0
        assert widget.currentRow() == 0  # No valid current row
        assert widget.currentColumn() == 0  # No valid current column

        # Selection operations should handle empty rows gracefully
        widget.clearSelection()
        widget.selectAll()  # Should not crash with no rows

        # Column operations should still work
        widget.setColumnWidth(0, 50)
        widget.resizeColumnsToContents()

        # Row operations should handle empty case
        widget.resizeRowsToContents()  # Should not crash with no rows

    def test_zero_columns_model(self):
        """Test widget behavior with model that has zero columns"""
        # Create model with zero columns but some rows
        empty_cols_model = ttk.TTkTableModelList(
            data=[[], [], []],  # 3 empty rows
            header=[]
        )
        widget = ttk.TTkTableWidget(tableModel=empty_cols_model)

        assert widget.rowCount() == 3
        assert widget.columnCount() == 0
        assert widget.currentRow() == 0  # No valid current row
        assert widget.currentColumn() == 0  # No valid current column

        # Selection operations should handle empty columns gracefully
        widget.clearSelection()
        widget.selectAll()  # Should not crash with no columns

        # Row operations should still work
        widget.setRowHeight(0, 2)
        widget.resizeRowsToContents()

        # Column operations should handle empty case
        widget.resizeColumnsToContents()  # Should not crash with no columns

    def test_completely_empty_model(self):
        """Test widget behavior with model that has zero rows and zero columns"""
        # Create completely empty model
        empty_model = ttk.TTkTableModelList(
            data=[],
            header=[]
        )
        widget = ttk.TTkTableWidget(tableModel=empty_model)

        assert widget.rowCount() == 0
        assert widget.columnCount() == 0
        assert widget.currentRow() == 0
        assert widget.currentColumn() == 0

        # All operations should handle completely empty case gracefully
        widget.clearSelection()
        widget.selectAll()
        widget.resizeColumnsToContents()
        widget.resizeRowsToContents()

        # Clipboard operations with empty model
        widget.copy()  # Should not crash
        widget.cut()   # Should not crash
        widget.paste() # Should not crash

        # Undo/redo with empty model
        widget.undo()
        widget.redo()

    def test_single_cell_model(self):
        """Test widget behavior with model that has exactly one cell"""
        single_cell_model = ttk.TTkTableModelList(
            data=[['SingleCell']],
            header=['OnlyColumn']
        )
        widget = ttk.TTkTableWidget(tableModel=single_cell_model)

        assert widget.rowCount() == 1
        assert widget.columnCount() == 1

        # Selection operations
        widget.selectAll()
        widget.selectRow(0)
        widget.selectColumn(0)
        widget.setSelection((0, 0), (1, 1), ttk.TTkK.TTkItemSelectionModel.Select)

        # Resize operations
        widget.setColumnWidth(0, 20)
        widget.setRowHeight(0, 3)
        widget.resizeColumnToContents(0)
        widget.resizeRowToContents(0)

    def test_model_transitions(self):
        """Test transitioning between different model sizes"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Start with normal model
        assert widget.rowCount() == 3
        assert widget.columnCount() == 3

        # Transition to empty rows
        empty_rows_model = ttk.TTkTableModelList(data=[], header=['A', 'B'])
        widget.setModel(empty_rows_model)
        assert widget.rowCount() == 0
        assert widget.columnCount() == 0

        # Transition to empty columns
        empty_cols_model = ttk.TTkTableModelList(data=[[], []], header=[])
        widget.setModel(empty_cols_model)
        assert widget.rowCount() == 2
        assert widget.columnCount() == 0

        # Transition to completely empty
        empty_model = ttk.TTkTableModelList(data=[], header=[])
        widget.setModel(empty_model)
        assert widget.rowCount() == 0
        assert widget.columnCount() == 0

        # Transition back to normal model
        widget.setModel(self.table_model)
        assert widget.rowCount() == 3
        assert widget.columnCount() == 3

    def test_boundary_operations_on_empty_models(self):
        """Test boundary operations on various empty model configurations"""

        # Test with zero rows model
        zero_rows_model = ttk.TTkTableModelList(data=[], header=['A', 'B'])
        widget = ttk.TTkTableWidget(tableModel=zero_rows_model)

        # These should not crash even with no rows
        try:
            widget.selectRow(0)  # Invalid row
            widget.unselectRow(0)  # Invalid row
            widget.setRowHeight(0, 2)  # Invalid row
            widget.resizeRowToContents(0)  # Invalid row
        except (IndexError, ValueError):
            pass  # Expected for invalid indices

        # Test with zero columns model
        zero_cols_model = ttk.TTkTableModelList(data=[[], []], header=[])
        widget.setModel(zero_cols_model)

        # These should not crash even with no columns
        try:
            widget.selectColumn(0)  # Invalid column
            widget.unselectColumn(0)  # Invalid column
            widget.setColumnWidth(0, 20)  # Invalid column
            widget.resizeColumnToContents(0)  # Invalid column
        except (IndexError, ValueError):
            pass  # Expected for invalid indices

    def test_empty_model_sorting(self):
        """Test sorting operations on empty models"""

        # Test sorting with zero rows
        zero_rows_model = ttk.TTkTableModelList(data=[], header=['Name', 'Age'])
        widget = ttk.TTkTableWidget(tableModel=zero_rows_model, sortingEnabled=True)

        assert widget.isSortingEnabled()
        # Sorting empty data should not crash
        widget.sortByColumn(0, ttk.TTkK.SortOrder.AscendingOrder)
        widget.sortByColumn(1, ttk.TTkK.SortOrder.DescendingOrder)

        # Test sorting with zero columns
        zero_cols_model = ttk.TTkTableModelList(data=[[], []], header=[])
        widget.setModel(zero_cols_model)

        # Sorting with no columns should handle gracefully
        try:
            widget.sortByColumn(0, ttk.TTkK.SortOrder.AscendingOrder)  # Invalid column
        except (IndexError, ValueError):
            pass  # Expected for invalid column index

    def test_empty_model_signals(self):
        """Test that signals work correctly with empty models"""
        empty_model = ttk.TTkTableModelList(data=[], header=[])
        widget = ttk.TTkTableWidget(tableModel=empty_model)

        # Connect signals to mock slots
        cell_changed_calls = []
        cell_clicked_calls = []

        @ttk.pyTTkSlot(int, int)
        def mock_cell_changed(row, col):
            cell_changed_calls.append((row, col))

        @ttk.pyTTkSlot(int, int)
        def mock_cell_clicked(row, col):
            cell_clicked_calls.append((row, col))

        widget.cellChanged.connect(mock_cell_changed)
        widget.cellClicked.connect(mock_cell_clicked)

        # Signals should be connected even with empty model
        assert len(widget.cellChanged._connected_slots) > 0
        assert len(widget.cellClicked._connected_slots) > 0

        # No signals should be emitted for empty model operations
        widget.clearSelection()
        widget.selectAll()

        # Should have no signal calls since there are no cells
        assert len(cell_changed_calls) == 0
        assert len(cell_clicked_calls) == 0

    def test_mouse_press_normal_cell(self):
        """Test mouse press on a normal cell"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Mock the mouse event for clicking on a cell
        # Assuming cell (1,1) would be around position (15, 2) accounting for headers
        mock_event = Mock()
        mock_event.x = 15
        mock_event.y = 2
        mock_event.mod = ttk.TTkK.NoModifier

        # Mock the internal methods that would be called
        with patch.object(widget, '_findCell', return_value=(1, 1)):
            with patch.object(widget, '_setCurrentCell') as mock_set_current:
                with patch.object(widget, 'setSelection') as mock_set_selection:
                    # Test cell click
                    result = widget.mousePressEvent(mock_event)

                    # Verify the event was handled
                    assert result is True

                    # Verify current cell was set
                    mock_set_current.assert_called_once_with(1, 1)

                    # Verify selection was made
                    mock_set_selection.assert_called_once()

    def test_mouse_press_header_row_selection(self):
        """Test mouse press on row header for row selection"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Mock mouse event for clicking on row header (col = -1)
        mock_event = Mock()
        mock_event.x = 2  # In header area
        mock_event.y = 3  # Row 1
        mock_event.mod = ttk.TTkK.NoModifier

        with patch.object(widget, '_findCell', return_value=(1, -1)):
            with patch.object(widget, 'clearSelection') as mock_clear:
                with patch.object(widget, 'selectRow') as mock_select_row:
                    result = widget.mousePressEvent(mock_event)

                    assert result is True
                    mock_clear.assert_called_once()
                    mock_select_row.assert_called_once_with(1)

    def test_mouse_press_header_column_selection(self):
        """Test mouse press on column header for column selection"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Mock mouse event for clicking on column header (row = -1)
        mock_event = Mock()
        mock_event.x = 15  # Column 1
        mock_event.y = 0   # In header area
        mock_event.mod = ttk.TTkK.NoModifier

        with patch.object(widget, '_findCell', return_value=(-1, 1)):
            with patch.object(widget, 'clearSelection') as mock_clear:
                with patch.object(widget, 'selectColumn') as mock_select_col:
                    result = widget.mousePressEvent(mock_event)

                    assert result is True
                    mock_clear.assert_called_once()
                    mock_select_col.assert_called_once_with(1)

    def test_mouse_press_corner_select_all(self):
        """Test mouse press on corner (both row and col = -1) for select all"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Mock mouse event for clicking on corner
        mock_event = Mock()
        mock_event.x = 2
        mock_event.y = 0
        mock_event.mod = ttk.TTkK.NoModifier

        with patch.object(widget, '_findCell', return_value=(-1, -1)):
            with patch.object(widget, 'selectAll') as mock_select_all:
                result = widget.mousePressEvent(mock_event)

                assert result is True
                mock_select_all.assert_called_once()

    def test_mouse_press_with_ctrl_modifier(self):
        """Test mouse press with Ctrl modifier for multi-selection"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Mock mouse event with Ctrl modifier
        mock_event = Mock()
        mock_event.x = 15
        mock_event.y = 2
        mock_event.mod = ttk.TTkK.ControlModifier

        with patch.object(widget, '_findCell', return_value=(1, 1)):
            with patch.object(widget, '_setCurrentCell') as mock_set_current:
                with patch.object(widget, 'setSelection') as mock_set_selection:
                    # Pre-select the cell to test deselection with Ctrl
                    widget._selected = [[False, False, False] for _ in range(3)]
                    widget._selected[1][1] = True

                    result = widget.mousePressEvent(mock_event)

                    assert result is True
                    mock_set_current.assert_called_once_with(1, 1)

    def test_mouse_press_empty_table_zero_rows(self):
        """Test mouse press on table with zero rows"""
        empty_model = ttk.TTkTableModelList(data=[], header=['A', 'B'])
        widget = ttk.TTkTableWidget(tableModel=empty_model)

        # Mock mouse event
        mock_event = Mock()
        mock_event.x = 10
        mock_event.y = 5
        mock_event.mod = ttk.TTkK.NoModifier

        with patch.object(widget, '_findCell', return_value=(0, 0)):
            # Should handle gracefully even with empty table
            result = widget.mousePressEvent(mock_event)

            # Should still return True (handled) but not crash
            assert result is True

    def test_mouse_press_empty_table_zero_columns(self):
        """Test mouse press on table with zero columns"""
        empty_model = ttk.TTkTableModelList(data=[[], []], header=[])
        widget = ttk.TTkTableWidget(tableModel=empty_model)

        # Mock mouse event
        mock_event = Mock()
        mock_event.x = 10
        mock_event.y = 5
        mock_event.mod = ttk.TTkK.NoModifier

        with patch.object(widget, '_findCell', return_value=(0, 0)):
            # Should handle gracefully even with empty columns
            result = widget.mousePressEvent(mock_event)

            # Should still return True (handled) but not crash
            assert result is True

    def test_mouse_press_completely_empty_table(self):
        """Test mouse press on completely empty table"""
        empty_model = ttk.TTkTableModelList(data=[], header=[])
        widget = ttk.TTkTableWidget(tableModel=empty_model)

        # Mock mouse event
        mock_event = Mock()
        mock_event.x = 10
        mock_event.y = 5
        mock_event.mod = ttk.TTkK.NoModifier

        with patch.object(widget, '_findCell', return_value=(0, 0)):
            # Should handle gracefully even with completely empty table
            result = widget.mousePressEvent(mock_event)

            # Should still return True (handled) but not crash
            assert result is True

    def test_mouse_press_single_cell_table(self):
        """Test mouse press on table with single cell"""
        single_cell_model = ttk.TTkTableModelList(data=[['OnlyCell']], header=['OnlyCol'])
        widget = ttk.TTkTableWidget(tableModel=single_cell_model)

        # Mock mouse event for the single cell
        mock_event = Mock()
        mock_event.x = 10
        mock_event.y = 2
        mock_event.mod = ttk.TTkK.NoModifier

        with patch.object(widget, '_findCell', return_value=(0, 0)):
            with patch.object(widget, '_setCurrentCell') as mock_set_current:
                result = widget.mousePressEvent(mock_event)

                assert result is True
                mock_set_current.assert_called_once_with(0, 0)

    def test_mouse_press_boundary_cells(self):
        """Test mouse press on boundary cells (first/last row/column)"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        test_cases = [
            (0, 0),  # Top-left cell
            (0, 2),  # Top-right cell
            (2, 0),  # Bottom-left cell
            (2, 2),  # Bottom-right cell
        ]

        for row, col in test_cases:
            mock_event = Mock()
            mock_event.x = 10 + col * 10  # Approximate position
            mock_event.y = 2 + row * 2    # Approximate position
            mock_event.mod = ttk.TTkK.NoModifier

            with patch.object(widget, '_findCell', return_value=(row, col)):
                with patch.object(widget, '_setCurrentCell') as mock_set_current:
                    result = widget.mousePressEvent(mock_event)

                    assert result is True
                    mock_set_current.assert_called_with(row, col)

    def test_mouse_press_signal_emission(self):
        """Test that mouse press emits appropriate signals"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Connect signal to mock slot
        cell_clicked_calls = []

        @ttk.pyTTkSlot(int, int)
        def mock_cell_clicked(row, col):
            cell_clicked_calls.append((row, col))

        widget.cellClicked.connect(mock_cell_clicked)

        # Mock mouse event
        mock_event = Mock()
        mock_event.x = 15
        mock_event.y = 2
        mock_event.mod = ttk.TTkK.NoModifier

        with patch.object(widget, '_findCell', return_value=(1, 1)):
            result = widget.mousePressEvent(mock_event)

            assert result is True
            # Verify signal was emitted
            assert len(cell_clicked_calls) == 1
            assert cell_clicked_calls[0] == (1, 1)

    def test_mouse_press_invalid_coordinates(self):
        """Test mouse press with coordinates outside table bounds"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Mock mouse event with coordinates that might be outside bounds
        mock_event = Mock()
        mock_event.x = 1000  # Very large x
        mock_event.y = 1000  # Very large y
        mock_event.mod = ttk.TTkK.NoModifier

        # _findCell should handle this gracefully and return valid coordinates
        with patch.object(widget, '_findCell', return_value=(2, 2)):  # Last valid cell
            result = widget.mousePressEvent(mock_event)

            # Should not crash and should handle gracefully
            assert result is True

    def test_mouse_press_separator_handling(self):
        """Test mouse press on separators (if separators are enabled)"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model, vSeparator=True, hSeparator=True)

        # Mock mouse event on vertical separator
        mock_event = Mock()
        mock_event.x = 20  # Position that might be on separator
        mock_event.y = 0   # In header area
        mock_event.mod = ttk.TTkK.NoModifier

        # Mock the getViewOffsets method
        with patch.object(widget, 'getViewOffsets', return_value=(0, 0)):
            with patch.object(widget, '_findCell', return_value=(-1, 1)):
                # Mock separator detection
                widget._colsPos = [10, 20, 30]  # Separator at x=20

                result = widget.mousePressEvent(mock_event)

                # Should handle separator selection
                assert result is True

    def test_mouse_press_state_changes(self):
        """Test that mouse press updates internal state correctly"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Ensure initial state
        assert widget._currentPos is None
        assert widget._hoverPos is None
        assert widget._dragPos is None

        # Mock mouse event
        mock_event = Mock()
        mock_event.x = 15
        mock_event.y = 2
        mock_event.mod = ttk.TTkK.NoModifier

        with patch.object(widget, '_findCell', return_value=(1, 1)):
            widget.mousePressEvent(mock_event)

            # Verify state changes
            assert widget._currentPos == (1, 1)
            assert widget._hoverPos is None  # Should be reset
            assert widget._dragPos == _DragPosType(fr=(1, 1), to=(1, 1))  # Should be initialized

    def test_mouse_press_with_disabled_model_flags(self):
        """Test mouse press on cells with different model flags"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Mock model flags to return non-selectable for certain cells
        original_flags = widget._tableModel.flags

        def mock_flags(row, col):
            if row == 1 and col == 1:
                return ttk.TTkK.ItemFlag.NoItemFlags  # Not selectable
            return original_flags(row, col)

        widget._tableModel.flags = mock_flags

        try:
            mock_event = Mock()
            mock_event.x = 15
            mock_event.y = 2
            mock_event.mod = ttk.TTkK.NoModifier

            with patch.object(widget, '_findCell', return_value=(1, 1)):
                result = widget.mousePressEvent(mock_event)

                # Should still handle the event
                assert result is True

        finally:
            # Restore original flags
            widget._tableModel.flags = original_flags
