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

    def test_parent_link_set_and_cleared_for_top_level_item(self):
        """Test top-level item parent link is set on add and cleared on remove"""
        tree = TTkTreeWidget()
        item = TTkTreeWidgetItem(["Item 1"])

        tree.addTopLevelItem(item)
        assert item._parent == tree._rootItem

        taken = tree.takeTopLevelItem(0)
        assert taken == item
        assert item._parent is None

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

    def test_programmatic_single_selection(self):
        """Test select/deselect API in single selection mode"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.SingleSelection)
        item1 = TTkTreeWidgetItem(["Item 1"])
        item2 = TTkTreeWidgetItem(["Item 2"])
        tree.addTopLevelItems([item1, item2])

        tree.selectItem(item1)
        assert tree.selectedItems() == [item1]

        tree.selectItem(item2)
        assert tree.selectedItems() == [item2]

        tree.deselectItem(item2)
        assert tree.selectedItems() == []

    def test_programmatic_multi_selection(self):
        """Test select/deselect API in multi selection mode"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)
        item1 = TTkTreeWidgetItem(["Item 1"])
        item2 = TTkTreeWidgetItem(["Item 2"])
        tree.addTopLevelItems([item1, item2])

        tree.selectItem(item1)
        tree.selectItem(item2)
        assert tree.selectedItems() == [item1, item2]

        tree.deselectItem(item1)
        assert tree.selectedItems() == [item2]

        tree.clearSelection()
        assert tree.selectedItems() == []

    def test_programmatic_no_selection_mode(self):
        """Test selection API is ignored in no selection mode"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.NoSelection)
        item = TTkTreeWidgetItem(["Item 1"])

        tree.selectItem(item)
        tree.setCurrentItem(item)
        assert tree.selectedItems() == []

    def test_set_selection_mode_trims_selected_items(self):
        """Test selection gets trimmed when switching to single mode"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)
        item1 = TTkTreeWidgetItem(["Item 1"])
        item2 = TTkTreeWidgetItem(["Item 2"])
        tree.addTopLevelItems([item1, item2])

        tree.selectItem(item1)
        tree.selectItem(item2)
        tree.setSelectionMode(TTkK.SelectionMode.SingleSelection)

        assert tree.selectedItems() == [item1]

    def test_programmatic_selection_ignores_detached_items(self):
        """Test selection API ignores items not belonging to this tree"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)
        in_tree = TTkTreeWidgetItem(["In tree"])
        detached = TTkTreeWidgetItem(["Detached"])
        tree.addTopLevelItem(in_tree)

        tree.selectItem(detached)
        tree.setCurrentItem(detached)
        tree.deselectItem(detached)

        assert tree.selectedItems() == []

    def test_multilevel_single_selection(self):
        """Test single selection mode with nested items"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.SingleSelection)
        parent = TTkTreeWidgetItem(["Parent"])
        child1 = TTkTreeWidgetItem(["Child 1"])
        child2 = TTkTreeWidgetItem(["Child 2"])
        grandchild = TTkTreeWidgetItem(["Grandchild"])

        parent.addChildren([child1, child2])
        child1.addChild(grandchild)
        tree.addTopLevelItem(parent)

        # Select parent
        tree.selectItem(parent)
        assert tree.selectedItems() == [parent]

        # Select child (replaces parent)
        tree.selectItem(child1)
        assert tree.selectedItems() == [child1]

        # Select grandchild (replaces child)
        tree.selectItem(grandchild)
        assert tree.selectedItems() == [grandchild]

    def test_multilevel_multi_selection(self):
        """Test multi selection mode with nested items"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)
        parent = TTkTreeWidgetItem(["Parent"])
        child1 = TTkTreeWidgetItem(["Child 1"])
        child2 = TTkTreeWidgetItem(["Child 2"])
        grandchild = TTkTreeWidgetItem(["Grandchild"])

        parent.addChildren([child1, child2])
        child1.addChild(grandchild)
        tree.addTopLevelItem(parent)

        # Select multiple items at different levels
        tree.selectItem(parent)
        tree.selectItem(child1)
        tree.selectItem(grandchild)
        assert tree.selectedItems() == [parent, child1, grandchild]

        # Deselect middle item
        tree.deselectItem(child1)
        assert tree.selectedItems() == [parent, grandchild]

        # Clear selection
        tree.clearSelection()
        assert tree.selectedItems() == []

    def test_multilevel_deselect_nested_item(self):
        """Test deselecting deeply nested items"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)
        root = TTkTreeWidgetItem(["Root"])
        level1 = TTkTreeWidgetItem(["Level 1"])
        level2 = TTkTreeWidgetItem(["Level 2"])
        level3 = TTkTreeWidgetItem(["Level 3"])

        root.addChild(level1)
        level1.addChild(level2)
        level2.addChild(level3)
        tree.addTopLevelItem(root)

        # Select all levels
        tree.selectItem(root)
        tree.selectItem(level1)
        tree.selectItem(level2)
        tree.selectItem(level3)
        assert len(tree.selectedItems()) == 4

        # Deselect items at different levels
        tree.deselectItem(level3)
        assert tree.selectedItems() == [root, level1, level2]

        tree.deselectItem(level1)
        assert tree.selectedItems() == [root, level2]

    def test_multilevel_selection_after_tree_modification(self):
        """Test selection is pruned after removing items from tree"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)
        parent = TTkTreeWidgetItem(["Parent"])
        child = TTkTreeWidgetItem(["Child"])
        parent.addChild(child)
        tree.addTopLevelItem(parent)

        # Select both items
        tree.selectItem(parent)
        tree.selectItem(child)
        assert len(tree.selectedItems()) == 2

        # Remove child from parent
        parent.removeChild(child)
        # Selection should be pruned to only include items still in tree
        tree._pruneSelection()
        assert tree.selectedItems() == [parent]

    def test_detached_item_from_another_tree_multilevel(self):
        """Test selection ignores detached items from another tree (multilevel)"""
        tree1 = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)
        tree2 = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)

        # Create structured trees
        parent1 = TTkTreeWidgetItem(["Parent 1"])
        child1 = TTkTreeWidgetItem(["Child 1"])
        parent1.addChild(child1)
        tree1.addTopLevelItem(parent1)

        parent2 = TTkTreeWidgetItem(["Parent 2"])
        child2 = TTkTreeWidgetItem(["Child 2"])
        parent2.addChild(child2)
        tree2.addTopLevelItem(parent2)

        # Try to select items from tree2 in tree1
        tree1.selectItem(parent2)
        tree1.selectItem(child2)
        assert tree1.selectedItems() == []

        # Select valid item from tree1
        tree1.selectItem(parent1)
        assert tree1.selectedItems() == [parent1]

        # Deselect items from tree2 in tree1 (should do nothing)
        tree1.deselectItem(child2)
        assert tree1.selectedItems() == [parent1]

    def test_orphaned_item_after_reparenting(self):
        """Test selection handles orphaned items that were reparented"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)
        parent1 = TTkTreeWidgetItem(["Parent 1"])
        parent2 = TTkTreeWidgetItem(["Parent 2"])
        child = TTkTreeWidgetItem(["Child"])

        parent1.addChild(child)
        tree.addTopLevelItems([parent1, parent2])

        # Select all items
        tree.selectItem(parent1)
        tree.selectItem(parent2)
        tree.selectItem(child)
        assert len(tree.selectedItems()) == 3

        # Reparent child to parent2
        parent1.removeChild(child)
        parent2.addChild(child)

        # Selection should still be valid (item is still in tree)
        tree._pruneSelection()
        assert len(tree.selectedItems()) == 3

    def test_selection_after_take_child(self):
        """Test selection after using takeChild API"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)
        parent = TTkTreeWidgetItem(["Parent"])
        child1 = TTkTreeWidgetItem(["Child 1"])
        child2 = TTkTreeWidgetItem(["Child 2"])

        parent.addChildren([child1, child2])
        tree.addTopLevelItem(parent)

        # Select both children
        tree.selectItem(child1)
        tree.selectItem(child2)
        assert len(tree.selectedItems()) == 2

        # Take child1 from tree
        taken = parent.takeChild(0)
        assert taken == child1

        # Prune selection
        tree._pruneSelection()
        # Only child2 should remain in selection
        assert tree.selectedItems() == [child2]

    def test_selection_after_take_children(self):
        """Test selection pruning after using takeChildren API"""
        tree = TTkTreeWidget(selectionMode=TTkK.SelectionMode.MultiSelection)
        parent = TTkTreeWidgetItem(["Parent"])
        child1 = TTkTreeWidgetItem(["Child 1"])
        child2 = TTkTreeWidgetItem(["Child 2"])

        parent.addChildren([child1, child2])
        tree.addTopLevelItem(parent)

        # Select parent and children
        tree.selectItem(parent)
        tree.selectItem(child1)
        tree.selectItem(child2)
        assert len(tree.selectedItems()) == 3

        # Detach all children from parent
        taken = parent.takeChildren()
        assert taken == [child1, child2]

        # Selection should keep only items still in the tree
        tree._pruneSelection()
        assert tree.selectedItems() == [parent]

    def test_parent_link_set_and_cleared_for_nested_manipulation(self):
        """Test nested item parent link across remove and reparent operations"""
        tree = TTkTreeWidget()
        parent1 = TTkTreeWidgetItem(["Parent 1"])
        parent2 = TTkTreeWidgetItem(["Parent 2"])
        child = TTkTreeWidgetItem(["Child"])
        tree.addTopLevelItems([parent1, parent2])

        parent1.addChild(child)
        assert child._parent == parent1

        parent1.removeChild(child)
        assert child._parent is None

        parent2.addChild(child)
        assert child._parent == parent2

        parent2.removeChild(child)
        assert child._parent is None


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