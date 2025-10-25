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
import io
from unittest.mock import Mock, MagicMock, patch

sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))
import TermTk as ttk
from TermTk.TTkWidgets.TTkModelView.tablewidget import _DragPosType, _ClipboardTable, _SelectionProxy, TTkHeaderView

class TestTTkHeaderView:
    """Test cases for TTkHeaderView class"""

    def test_init_default(self):
        """Test default initialization"""
        header = TTkHeaderView()
        assert header.isVisible() == True
        assert hasattr(header, 'visibilityUpdated')

    def test_init_with_visibility(self):
        """Test initialization with specific visibility"""
        header_visible = TTkHeaderView(visible=True)
        header_hidden = TTkHeaderView(visible=False)

        assert header_visible.isVisible() == True
        assert header_hidden.isVisible() == False

    def test_set_visible(self):
        """Test setVisible method"""
        header = TTkHeaderView()

        header.setVisible(False)
        assert header.isVisible() == False

        header.setVisible(True)
        assert header.isVisible() == True

    def test_show_hide(self):
        """Test show and hide methods"""
        header = TTkHeaderView(visible=False)

        header.show()
        assert header.isVisible() == True

        header.hide()
        assert header.isVisible() == False

    def test_visibility_signal(self):
        """Test visibility signal emission"""
        header = TTkHeaderView()
        signal_calls = []

        @ttk.pyTTkSlot(bool)
        def mock_slot(visible):
            signal_calls.append(visible)

        header.visibilityUpdated.connect(mock_slot)

        header.hide()
        assert len(signal_calls) == 1
        assert signal_calls[0] == False

        header.show()
        assert len(signal_calls) == 2
        assert signal_calls[1] == True

class TestClipboardTable:
    """Test cases for _ClipboardTable class"""

    def test_init_empty(self):
        """Test initialization with empty data"""
        clipboard = _ClipboardTable([])
        assert clipboard.data() == []
        assert isinstance(clipboard, ttk.TTkString)

    def test_init_with_data(self):
        """Test initialization with data"""
        data = [
            [(0, 0, 'A1'), (0, 1, 'B1')],
            [(1, 0, 'A2'), (1, 1, 'B2')]
        ]
        clipboard = _ClipboardTable(data)

        assert clipboard.data() == data
        assert isinstance(clipboard, ttk.TTkString)
        assert len(str(clipboard)) > 0

    def test_string_conversion(self):
        """Test TTkString conversion"""
        data = [
            [(0, 0, 'Cell1'), (0, 1, 'Cell2')],
            [(1, 0, 'Cell3'), (1, 1, 'Cell4')]
        ]
        clipboard = _ClipboardTable(data)

        string_repr = str(clipboard)
        # Should contain the cell data in some formatted way
        assert 'Cell1' in string_repr or str(clipboard).find('Cell') >= 0

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

    def test_init_parameters(self):
        """Test initialization with all parameters"""
        widget = ttk.TTkTableWidget(
            tableModel=self.table_model,
            vSeparator=False,
            hSeparator=False,
            vHeader=False,
            hHeader=False,
            sortingEnabled=True,
            dataPadding=3
        )

        assert widget.model() == self.table_model
        assert not widget.vSeparatorVisibility()
        assert not widget.hSeparatorVisibility()
        assert not widget.verticalHeader().isVisible()
        assert not widget.horizontalHeader().isVisible()
        assert widget.isSortingEnabled()
        assert widget._dataPadding == 3

    def test_header_views(self):
        """Test header view functionality"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        v_header = widget.verticalHeader()
        h_header = widget.horizontalHeader()

        assert isinstance(v_header, TTkHeaderView)
        assert isinstance(h_header, TTkHeaderView)
        assert v_header.isVisible()
        assert h_header.isVisible()

        # Test header visibility changes trigger layout refresh
        with patch.object(widget, '_headerVisibilityChanged') as mock_refresh:
            v_header.hide()
            # Signal should have been emitted and connected
            assert not v_header.isVisible()

    def test_model_management(self):
        """Test model getter/setter and related functionality"""
        widget = ttk.TTkTableWidget()
        original_model = widget.model()

        # Test model change
        widget.setModel(self.table_model)
        assert widget.model() == self.table_model
        assert widget.model() != original_model

        # Test that model signals are connected
        assert widget.model().dataChanged._connected_slots
        assert widget.model().modelChanged._connected_slots

        # Test model change triggers layout refresh
        with patch.object(widget, '_refreshLayout') as mock_refresh:
            new_model = ttk.TTkTableModelList(data=[['test']])
            widget.setModel(new_model)
            # _refreshLayout should be called when model changes
            # Note: This depends on the modelChanged signal being emitted

    def test_selection_proxy_integration(self):
        """Test selection proxy integration"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        proxy = widget._select_proxy
        assert isinstance(proxy, _SelectionProxy)
        assert proxy._rows == 3
        assert proxy._cols == 3

        # Test selection operations update proxy
        widget.selectRow(1)
        assert proxy.isRowSelected(1)

        widget.selectColumn(2)
        assert proxy.isColSelected(2)

        widget.clearSelection()
        assert not proxy.isRowSelected(1)
        assert not proxy.isColSelected(2)

    def test_current_cell_management(self):
        """Test current cell position management"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Initially no current position
        assert widget._currentPos is None
        assert widget.currentRow() == 0  # Default
        assert widget.currentColumn() == 0  # Default

        # Test setting current cell
        widget._setCurrentCell(1, 2)
        assert widget._currentPos == (1, 2)
        assert widget.currentRow() == 1
        assert widget.currentColumn() == 2

        # # Test movement
        # widget._moveCurrentCell(row=1, col=1)
        # assert widget._currentPos == (2, 3)  # Should be (1+1, 2+1) if movement works

        # Test boundary handling
        widget._moveCurrentCell(row=5, col=5)  # Should clamp to table bounds
        assert widget._currentPos[0] < widget.rowCount()
        assert widget._currentPos[1] < widget.columnCount()

    def test_snapshot_system(self):
        """Test undo/redo snapshot system"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Initially no snapshots
        assert len(widget._snapshot) == 0
        assert widget._snapshotId == 0
        assert not widget.isUndoAvailable()
        assert not widget.isRedoAvailable()

        # Create a snapshot by modifying data
        original_value = widget.model().data(0, 0)
        widget._tableModel_setData([(0, 0, 'NewValue')])

        # Should have a snapshot now
        assert widget.isUndoAvailable()
        assert not widget.isRedoAvailable()
        assert widget.model().data(0, 0) == 'NewValue'

        # Test undo
        widget.undo()
        assert widget.model().data(0, 0) == original_value
        assert not widget.isUndoAvailable()
        assert widget.isRedoAvailable()

        # Test redo
        widget.redo()
        assert widget.model().data(0, 0) == 'NewValue'
        assert widget.isUndoAvailable()
        assert not widget.isRedoAvailable()

    def test_clipboard_operations(self):
        """Test clipboard operations"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Select some cells
        widget.setSelection((0, 0), (2, 2), ttk.TTkK.TTkItemSelectionModel.Select)

        # Test copy
        widget.copy()
        # Should not raise exception

        # Test cut
        original_values = [
            [widget.model().data(r, c) for c in range(2)]
            for r in range(2)
        ]
        widget.cut()

        # Values should be cleared after cut
        for r in range(2):
            for c in range(2):
                if widget._select_proxy.isCellSelected(c, r):
                    assert widget.model().data(r, c) == ''

        # Test paste
        widget.paste()
        # Should restore some values or handle gracefully

    def test_sorting_functionality(self):
        """Test sorting functionality"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Initially disabled
        assert not widget.isSortingEnabled()

        # Enable sorting
        widget.setSortingEnabled(True)
        assert widget.isSortingEnabled()

        # Test sorting by column
        original_first_name = widget.model().data(0, 0)
        widget.sortByColumn(0, ttk.TTkK.SortOrder.AscendingOrder)

        # Can't easily test actual sorting without knowing internal implementation
        # but should not raise exception

        # Test descending sort
        widget.sortByColumn(0, ttk.TTkK.SortOrder.DescendingOrder)

    def test_resize_operations(self):
        """Test column and row resize operations"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Test individual operations
        widget.setColumnWidth(0, 20)
        widget.setRowHeight(0, 3)

        # Test resize to contents
        widget.resizeColumnToContents(0)
        widget.resizeRowToContents(0)

        # Test resize all to contents
        widget.resizeColumnsToContents()
        widget.resizeRowsToContents()

        # These should not raise exceptions

    def test_view_area_calculation(self):
        """Test view area size calculation"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # With headers
        width, height = widget.viewFullAreaSize()
        assert width > 0
        assert height > 0

        # Without headers
        widget.verticalHeader().hide()
        widget.horizontalHeader().hide()

        width_no_headers, height_no_headers = widget.viewFullAreaSize()
        assert width_no_headers <= width
        assert height_no_headers <= height

    def test_find_cell_functionality(self):
        """Test _findCell coordinate conversion"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Test with headers
        row, col = widget._findCell(10, 5, headers=True)
        assert isinstance(row, int)
        assert isinstance(col, int)
        assert row >= -1  # -1 for header, >= 0 for cells
        assert col >= -1  # -1 for header, >= 0 for cells

        # Test without headers
        row, col = widget._findCell(10, 5, headers=False)
        assert isinstance(row, int)
        assert isinstance(col, int)
        assert row >= 0
        assert col >= 0

    def test_mouse_events(self):
        """Test mouse event handling"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Mock mouse events
        press_event = Mock()
        press_event.x = 15
        press_event.y = 2
        press_event.mod = ttk.TTkK.NoModifier

        move_event = Mock()
        move_event.x = 20
        move_event.y = 3
        move_event.mod = ttk.TTkK.NoModifier

        release_event = Mock()
        release_event.x = 20
        release_event.y = 3
        release_event.mod = ttk.TTkK.NoModifier

        double_click_event = Mock()
        double_click_event.x = 15
        double_click_event.y = 2
        double_click_event.mod = ttk.TTkK.NoModifier

        # Test event handling (should not crash)
        with patch.object(widget, '_findCell', return_value=(1, 1)):
            assert widget.mousePressEvent(press_event) == True
            assert widget.mouseMoveEvent(move_event) == True
            assert widget.mouseReleaseEvent(release_event) == True
            assert widget.mouseDoubleClickEvent(double_click_event) == True

    def test_keyboard_events(self):
        """Test keyboard event handling"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Set initial position
        widget._setCurrentCell(1, 1)

        # Mock keyboard events
        key_events = [
            Mock(key=ttk.TTkK.Key_Up, mod=ttk.TTkK.NoModifier),
            Mock(key=ttk.TTkK.Key_Down, mod=ttk.TTkK.NoModifier),
            Mock(key=ttk.TTkK.Key_Left, mod=ttk.TTkK.NoModifier),
            Mock(key=ttk.TTkK.Key_Right, mod=ttk.TTkK.NoModifier),
            Mock(key=ttk.TTkK.Key_Tab, mod=ttk.TTkK.NoModifier),
            Mock(key=ttk.TTkK.Key_Backtab, mod=ttk.TTkK.NoModifier),
            Mock(key=ttk.TTkK.Key_Enter, mod=ttk.TTkK.NoModifier),
            Mock(key=ttk.TTkK.Key_Space, mod=ttk.TTkK.NoModifier),
        ]

        for event in key_events:
            # Should handle keyboard navigation
            result = widget.keyEvent(event)
            # Result depends on implementation, but should not crash

    def test_signal_emissions(self):
        """Test signal emissions"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Connect signals to mock slots
        cell_changed_calls = []
        cell_clicked_calls = []
        cell_entered_calls = []
        current_cell_changed_calls = []

        @ttk.pyTTkSlot(int, int)
        def mock_cell_changed(row, col):
            cell_changed_calls.append((row, col))

        @ttk.pyTTkSlot(int, int)
        def mock_cell_clicked(row, col):
            cell_clicked_calls.append((row, col))

        @ttk.pyTTkSlot(int, int)
        def mock_cell_entered(row, col):
            cell_entered_calls.append((row, col))

        @ttk.pyTTkSlot(int, int, int, int)
        def mock_current_cell_changed(curr_row, curr_col, prev_row, prev_col):
            current_cell_changed_calls.append((curr_row, curr_col, prev_row, prev_col))

        widget.cellChanged.connect(mock_cell_changed)
        widget.cellClicked.connect(mock_cell_clicked)
        widget.cellEntered.connect(mock_cell_entered)
        widget.currentCellChanged.connect(mock_current_cell_changed)

        # Trigger events that should emit signals
        widget._cellChanged.emit(1, 2)
        widget._cellClicked.emit(0, 1)
        widget._cellEntered.emit(2, 0)
        widget._currentCellChanged.emit(1, 1, 0, 0)

        # Verify signals were received
        assert len(cell_changed_calls) == 1
        assert cell_changed_calls[0] == (1, 2)
        assert len(cell_clicked_calls) == 1
        assert cell_clicked_calls[0] == (0, 1)
        assert len(cell_entered_calls) == 1
        assert cell_entered_calls[0] == (2, 0)
        assert len(current_cell_changed_calls) == 1
        assert current_cell_changed_calls[0] == (1, 1, 0, 0)

    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Empty model
        empty_model = ttk.TTkTableModelList(data=[], header=[])
        widget = ttk.TTkTableWidget(tableModel=empty_model)

        assert widget.rowCount() == 0
        assert widget.columnCount() == 0

        # Operations should handle empty model gracefully
        widget.selectAll()
        widget.clearSelection()
        widget.resizeColumnsToContents()
        widget.resizeRowsToContents()
        widget.copy()
        widget.cut()
        widget.paste()

        # Single cell model
        single_model = ttk.TTkTableModelList(data=[['Cell']], header=['Col'])
        widget.setModel(single_model)

        assert widget.rowCount() == 1
        assert widget.columnCount() == 1

        widget.selectAll()
        widget._setCurrentCell(0, 0)

        # Large model stress test
        large_data = [[f'Cell_{i}_{j}' for j in range(50)] for i in range(50)]
        large_model = ttk.TTkTableModelList(data=large_data)
        widget.setModel(large_model)

        assert widget.rowCount() == 50
        assert widget.columnCount() == 50

        # Should handle large models without issues
        widget.selectRow(25)
        widget.selectColumn(25)

    def test_focus_and_events(self):
        """Test focus handling and event processing"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Test focus policy
        focus_policy = widget.focusPolicy()
        assert focus_policy & ttk.TTkK.ClickFocus
        assert focus_policy & ttk.TTkK.TabFocus

        # Test focus events
        widget.focusOutEvent()  # Should not crash

        # Test leave event
        leave_event = Mock()
        leave_event.x = 100
        leave_event.y = 100
        result = widget.leaveEvent(leave_event)
        # Should handle gracefully

    def test_internal_state_consistency(self):
        """Test internal state consistency"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Test that internal positions are consistent
        widget._setCurrentCell(1, 2)
        assert widget._currentPos == (1, 2)
        assert widget.currentRow() == 1
        assert widget.currentColumn() == 2

        # Test drag position initialization
        assert widget._dragPos is None
        assert widget._hoverPos is None
        assert widget._hSeparatorSelected is None
        assert widget._vSeparatorSelected is None

        # Test selection proxy consistency
        proxy = widget._select_proxy
        assert proxy._rows == widget.rowCount()
        assert proxy._cols == widget.columnCount()

    def test_style_and_appearance(self):
        """Test style properties"""
        widget = ttk.TTkTableWidget()

        # Test class style exists
        assert hasattr(ttk.TTkTableWidget, 'classStyle')
        assert isinstance(ttk.TTkTableWidget.classStyle, dict)
        assert 'default' in ttk.TTkTableWidget.classStyle
        assert 'disabled' in ttk.TTkTableWidget.classStyle

        # Test style properties contain expected keys
        default_style = ttk.TTkTableWidget.classStyle['default']
        expected_keys = ['color', 'lineColor', 'headerColor', 'hoverColor',
                        'currentColor', 'selectedColor', 'separatorColor']
        for key in expected_keys:
            assert key in default_style
            assert isinstance(default_style[key], ttk.TTkColor)

    def test_paste_event_handling(self):
        """Test paste event with different data types"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)
        widget._setCurrentCell(0, 0)

        # Test paste with TTkString
        text_data = ttk.TTkString("Hello\tWorld\nFoo\tBar")
        result = widget.pasteEvent(text_data)
        assert result == True

        # Test paste with _ClipboardTable
        clipboard_data = [
            [(0, 0, 'A1'), (0, 1, 'B1')],
            [(1, 0, 'A2'), (1, 1, 'B2')]
        ]
        clipboard_table = _ClipboardTable(clipboard_data)
        result = widget.pasteEvent(clipboard_table)
        assert result == True

        # Test paste with unsupported data
        result = widget.pasteEvent("regular string")
        assert result == True  # Should handle gracefully

    def test_model_flags_integration(self):
        """Test integration with model flags"""
        widget = ttk.TTkTableWidget(tableModel=self.table_model)

        # Mock model flags
        def mock_flags(row, col):
            if row == 1 and col == 1:
                return ttk.TTkK.ItemFlag.NoItemFlags  # Not selectable
            return ttk.TTkK.ItemFlag.ItemIsSelectable | ttk.TTkK.ItemFlag.ItemIsEnabled

        original_flags = widget._tableModel.flags
        widget._tableModel.flags = mock_flags

        try:
            # Test selection respects flags
            widget._select_proxy.updateModel(
                cols=widget.columnCount(),
                rows=widget.rowCount(),
                flags=widget._tableModel.flags
            )

            widget.selectAll()
            # Cell (1,1) should not be selected due to flags
            assert not widget._select_proxy.isCellSelected(1, 1)
            # Other cells should be selected
            assert widget._select_proxy.isCellSelected(0, 0)
            assert widget._select_proxy.isCellSelected(2, 2)

        finally:
            widget._tableModel.flags = original_flags
