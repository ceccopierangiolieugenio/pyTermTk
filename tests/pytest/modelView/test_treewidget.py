import pytest
from unittest.mock import MagicMock, patch
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.TTkModelView.treewidget import TTkTreeWidget
from TermTk.TTkWidgets.TTkModelView.treewidgetitem import TTkTreeWidgetItem


class TestTTkTreeWidgetEmpty:
    """Test TTkTreeWidget with empty tree to catch crashes"""

    def test_empty_tree_creation(self):
        """Test creating an empty tree widget"""
        tree = TTkTreeWidget()
        assert tree is not None
        assert tree._rootItem is not None

    def test_empty_tree_view_area_size(self):
        """Test viewFullAreaSize with empty tree"""
        tree = TTkTreeWidget()
        w, h = tree.viewFullAreaSize()
        assert w == 0
        assert h == 1  # Header row

    def test_empty_tree_clear(self):
        """Test clear on empty tree"""
        tree = TTkTreeWidget()
        tree.clear()  # Should not crash
        assert tree._rootItem.size() == 0

    def test_empty_tree_paint_event(self):
        """Test paintEvent with empty tree"""
        tree = TTkTreeWidget()
        canvas = MagicMock()
        tree.paintEvent(canvas)  # Should not crash

    def test_empty_tree_selected_items(self):
        """Test selectedItems with empty tree"""
        tree = TTkTreeWidget()
        selected = tree.selectedItems()
        assert selected == []

    def test_empty_tree_mouse_press(self):
        """Test mouse press on empty tree"""
        tree = TTkTreeWidget()
        evt = MagicMock()
        evt.x = 5
        evt.y = 5
        evt.mod = 0
        tree.mousePressEvent(evt)  # Should not crash

    def test_empty_tree_resize_column(self):
        """Test resizeColumnToContents with empty tree"""
        tree = TTkTreeWidget(header=[TTkString("Col1")])
        tree.resizeColumnToContents(0)  # Should not crash


class TestTTkTreeWidgetBasic:
    """Test basic TTkTreeWidget functionality"""

    def test_tree_with_header(self):
        """Test tree creation with headers"""
        tree = TTkTreeWidget(header=[TTkString("A"), TTkString("B")])
        assert len(tree._header) == 2
        assert len(tree._columnsPos) == 2

    def test_add_top_level_item(self):
        """Test adding a top-level item"""
        tree = TTkTreeWidget()
        item = TTkTreeWidgetItem(["Item 1"])
        tree.addTopLevelItem(item)
        assert tree._rootItem.size() == 1
        assert tree.topLevelItem(0) == item

    def test_add_multiple_top_level_items(self):
        """Test adding multiple top-level items"""
        tree = TTkTreeWidget()
        items = [TTkTreeWidgetItem([f"Item {i}"]) for i in range(3)]
        tree.addTopLevelItems(items)
        assert tree._rootItem.size() == 3

    def test_take_top_level_item(self):
        """Test removing top-level item"""
        tree = TTkTreeWidget()
        item = TTkTreeWidgetItem(["Item 1"])
        tree.addTopLevelItem(item)
        taken = tree.takeTopLevelItem(0)
        assert taken == item
        assert tree._rootItem.size() == 0

    def test_index_of_top_level_item(self):
        """Test finding index of top-level item"""
        tree = TTkTreeWidget()
        items = [TTkTreeWidgetItem([f"Item {i}"]) for i in range(3)]
        tree.addTopLevelItems(items)
        assert tree.indexOfTopLevelItem(items[1]) == 1

    def test_invisible_root_item(self):
        """Test getting invisible root item"""
        tree = TTkTreeWidget()
        root = tree.invisibleRootItem()
        assert root == tree._rootItem


class TestTTkTreeWidgetSelection:
    """Test selection modes"""

    def test_single_selection_mode(self):
        """Test single selection mode"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.SingleSelection)
        assert tree.selectionMode() == TTkK.SelectionMode.SingleSelection

    def test_multi_selection_mode(self):
        """Test multi selection mode"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)
        assert tree.selectionMode() == TTkK.SelectionMode.MultiSelection

    def test_set_selection_mode(self):
        """Test changing selection mode"""
        tree = TTkTreeWidget()
        tree.setSelectionMode(TTkK.SelectionMode.MultiSelection)
        assert tree.selectionMode() == TTkK.SelectionMode.MultiSelection


class TestTTkTreeWidgetSorting:
    """Test sorting functionality"""

    def test_sorting_enabled_default(self):
        """Test sorting is enabled by default"""
        tree = TTkTreeWidget()
        assert tree.isSortingEnabled() is True

    def test_set_sorting_enabled(self):
        """Test enabling/disabling sorting"""
        tree = TTkTreeWidget(sortingEnabled=False)
        assert tree.isSortingEnabled() is False
        tree.setSortingEnabled(True)
        assert tree.isSortingEnabled() is True

    def test_sort_column(self):
        """Test sort column getter"""
        tree = TTkTreeWidget()
        assert tree.sortColumn() == -1

    def test_sort_items_when_disabled(self):
        """Test sorting when disabled does nothing"""
        tree = TTkTreeWidget(sortingEnabled=False)
        tree.sortItems(0, TTkK.AscendingOrder)
        assert tree._sortColumn == -1


class TestTTkTreeWidgetColumns:
    """Test column operations"""

    def test_column_width(self):
        """Test getting column width"""
        tree = TTkTreeWidget(header=[TTkString("A"), TTkString("B")])
        width = tree.columnWidth(0)
        assert width == 20  # Default width

    def test_set_column_width(self):
        """Test setting column width"""
        tree = TTkTreeWidget(header=[TTkString("A"), TTkString("B")])
        tree.setColumnWidth(0, 30)
        assert tree.columnWidth(0) == 30 + 1 # separator