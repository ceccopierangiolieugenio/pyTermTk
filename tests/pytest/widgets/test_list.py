# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))
import TermTk as ttk

# ============================================================================
# TTkListWidget Tests
# ============================================================================

def test_listwidget_add_items():
    '''
    Test adding items to TTkListWidget using addItem() and addItems().
    Verifies that items are added correctly to the list.
    '''
    listWidget = ttk.TTkListWidget()

    assert len(listWidget.items()) == 0

    # Add single item
    listWidget.addItem("Item 1")
    assert len(listWidget.items()) == 1
    assert listWidget.itemAt(0).text() == "Item 1"

    # Add item with data
    listWidget.addItem("Item 2", data="data2")
    assert len(listWidget.items()) == 2
    assert listWidget.itemAt(1).text() == "Item 2"
    assert listWidget.itemAt(1).data() == "data2"

    # Add multiple items
    listWidget.addItems(["Item 3", "Item 4", "Item 5"])
    assert len(listWidget.items()) == 5
    assert listWidget.itemAt(2).text() == "Item 3"
    assert listWidget.itemAt(3).text() == "Item 4"
    assert listWidget.itemAt(4).text() == "Item 5"

def test_listwidget_add_items_at():
    '''
    Test inserting items at specific positions using addItemAt() and addItemsAt().
    '''
    listWidget = ttk.TTkListWidget()

    listWidget.addItems(["Item 0", "Item 1", "Item 2"])
    assert len(listWidget.items()) == 3

    # Insert at beginning
    listWidget.addItemAt("Item -1", 0)
    assert len(listWidget.items()) == 4
    assert listWidget.itemAt(0).text() == "Item -1"
    assert listWidget.itemAt(1).text() == "Item 0"

    # Insert in middle
    listWidget.addItemAt("Item 0.5", 2)
    assert len(listWidget.items()) == 5
    assert listWidget.itemAt(2).text() == "Item 0.5"

    # Insert at end
    listWidget.addItemsAt(["Item 3", "Item 4"], 5)
    assert len(listWidget.items()) == 7
    assert listWidget.itemAt(5).text() == "Item 3"
    assert listWidget.itemAt(6).text() == "Item 4"

def test_listwidget_remove_items():
    '''
    Test removing items from TTkListWidget.
    '''
    listWidget = ttk.TTkListWidget()

    listWidget.addItems(["Item 0", "Item 1", "Item 2", "Item 3"])
    assert len(listWidget.items()) == 4

    # Remove by index
    listWidget.removeAt(1)
    assert len(listWidget.items()) == 3
    assert listWidget.itemAt(0).text() == "Item 0"
    assert listWidget.itemAt(1).text() == "Item 2"
    assert listWidget.itemAt(2).text() == "Item 3"

    # Remove by item
    item = listWidget.itemAt(1)
    listWidget.removeItem(item)
    assert len(listWidget.items()) == 2
    assert listWidget.itemAt(0).text() == "Item 0"
    assert listWidget.itemAt(1).text() == "Item 3"

    # Remove multiple items
    items = [listWidget.itemAt(0), listWidget.itemAt(1)]
    listWidget.removeItems(items)
    assert len(listWidget.items()) == 0

def test_listwidget_indexOf_itemAt():
    '''
    Test finding items by index and value.
    '''
    listWidget = ttk.TTkListWidget()

    listWidget.addItem("Item 0")
    listWidget.addItem("Item 1", data="data1")
    listWidget.addItem("Item 2")

    # Test itemAt
    item0 = listWidget.itemAt(0)
    assert item0.text() == "Item 0"

    item1 = listWidget.itemAt(1)
    assert item1.text() == "Item 1"
    assert item1.data() == "data1"

    # Test indexOf with item object
    assert listWidget.indexOf(item0) == 0
    assert listWidget.indexOf(item1) == 1

    # Test indexOf with text
    assert listWidget.indexOf("Item 0") == 0
    assert listWidget.indexOf("Item 2") == 2

    # Test indexOf with data
    assert listWidget.indexOf("data1") == 1

    # Test indexOf with non-existent item
    assert listWidget.indexOf("Not Found") == -1

def test_listwidget_move_item():
    '''
    Test moving items within the list.
    '''
    listWidget = ttk.TTkListWidget()

    listWidget.addItems(["Item 0", "Item 1", "Item 2", "Item 3"])

    # Move item from position 0 to position 2
    listWidget.moveItem(0, 2)
    assert listWidget.itemAt(0).text() == "Item 2"
    assert listWidget.itemAt(1).text() == "Item 1"
    assert listWidget.itemAt(2).text() == "Item 0"
    assert listWidget.itemAt(3).text() == "Item 3"

    # Move item from position 3 to position 1
    listWidget.moveItem(3, 1)
    assert listWidget.itemAt(0).text() == "Item 2"
    assert listWidget.itemAt(1).text() == "Item 3"
    assert listWidget.itemAt(2).text() == "Item 0"
    assert listWidget.itemAt(3).text() == "Item 1"

def test_listwidget_selection_mode():
    '''
    Test single and multi-selection modes.
    '''
    # Test SingleSelection mode
    listWidget = ttk.TTkListWidget(selectionMode=ttk.TTkK.SingleSelection)
    assert listWidget.selectionMode() == ttk.TTkK.SingleSelection

    listWidget.addItems(["Item 0", "Item 1", "Item 2"])

    item0 = listWidget.itemAt(0)
    item1 = listWidget.itemAt(1)
    item2 = listWidget.itemAt(2)

    listWidget.setCurrentItem(item0)
    assert len(listWidget.selectedItems()) == 1
    assert item0 in listWidget.selectedItems()

    listWidget.setCurrentItem(item1)
    assert len(listWidget.selectedItems()) == 1
    assert item1 in listWidget.selectedItems()
    assert item0 not in listWidget.selectedItems()

    # Test MultiSelection mode
    listWidget2 = ttk.TTkListWidget(selectionMode=ttk.TTkK.MultiSelection)
    assert listWidget2.selectionMode() == ttk.TTkK.MultiSelection

    listWidget2.addItems(["Item 0", "Item 1", "Item 2"])

    item0_2 = listWidget2.itemAt(0)
    item1_2 = listWidget2.itemAt(1)
    item2_2 = listWidget2.itemAt(2)

    listWidget2.setCurrentItem(item0_2)
    assert len(listWidget2.selectedItems()) == 1
    assert item0_2 in listWidget2.selectedItems()

    listWidget2.setCurrentItem(item1_2)
    assert len(listWidget2.selectedItems()) == 2
    assert item0_2 in listWidget2.selectedItems()
    assert item1_2 in listWidget2.selectedItems()

    listWidget2.setCurrentItem(item2_2)
    assert len(listWidget2.selectedItems()) == 3

def test_listwidget_change_selection_mode():
    '''
    Test dynamically changing selection mode.
    '''
    listWidget = ttk.TTkListWidget(selectionMode=ttk.TTkK.SingleSelection)
    assert listWidget.selectionMode() == ttk.TTkK.SingleSelection

    listWidget.setSelectionMode(ttk.TTkK.MultiSelection)
    assert listWidget.selectionMode() == ttk.TTkK.MultiSelection

    listWidget.setSelectionMode(ttk.TTkK.SingleSelection)
    assert listWidget.selectionMode() == ttk.TTkK.SingleSelection

def test_listwidget_selected_items():
    '''
    Test getting selected items and labels.
    '''
    listWidget = ttk.TTkListWidget(selectionMode=ttk.TTkK.MultiSelection)

    listWidget.addItems(["Item 0", "Item 1", "Item 2"])

    # Initially no selection
    assert len(listWidget.selectedItems()) == 0
    assert len(listWidget.selectedLabels()) == 0

    # Select items
    item0 = listWidget.itemAt(0)
    item1 = listWidget.itemAt(1)

    listWidget.setCurrentItem(item0)
    assert len(listWidget.selectedItems()) == 1
    assert listWidget.selectedLabels() == ["Item 0"]

    listWidget.setCurrentItem(item1)
    assert len(listWidget.selectedItems()) == 2
    assert set([str(_l) for _l in listWidget.selectedLabels()]) == {"Item 0", "Item 1"}

def test_listwidget_set_current_row():
    '''
    Test setting current row by index.
    '''
    listWidget = ttk.TTkListWidget()

    listWidget.addItems(["Item 0", "Item 1", "Item 2"])

    signal_received = []
    listWidget.itemClicked.connect(lambda item: signal_received.append(item))

    listWidget.setCurrentRow(0)
    assert len(signal_received) == 1
    assert signal_received[0].text() == "Item 0"

    listWidget.setCurrentRow(2)
    assert len(signal_received) == 2
    assert signal_received[1].text() == "Item 2"

def test_listwidget_signals():
    '''
    Test that itemClicked and textClicked signals are emitted correctly.
    '''
    listWidget = ttk.TTkListWidget()

    listWidget.addItems(["Item 0", "Item 1", "Item 2"])

    item_clicked = []
    text_clicked = []

    listWidget.itemClicked.connect(lambda item: item_clicked.append(item))
    listWidget.textClicked.connect(lambda text: text_clicked.append(text))

    item0 = listWidget.itemAt(0)
    item1 = listWidget.itemAt(1)

    listWidget.setCurrentItem(item0)
    assert len(item_clicked) == 1
    assert item_clicked[0] == item0
    assert len(text_clicked) == 1
    assert text_clicked[0] == "Item 0"

    listWidget.setCurrentItem(item1)
    assert len(item_clicked) == 2
    assert item_clicked[1] == item1
    assert len(text_clicked) == 2
    assert text_clicked[1] == "Item 1"

def test_listwidget_search():
    '''
    Test search functionality.
    '''
    listWidget = ttk.TTkListWidget()

    listWidget.addItems(["Apple", "Banana", "Cherry", "Date", "Elderberry"])

    assert listWidget.search() == ""
    assert len(listWidget.filteredItems()) == 5

    # Search for items containing 'e'
    listWidget.setSearch("e")
    assert listWidget.search() == "e"
    filtered = listWidget.filteredItems()
    assert len(filtered) == 4  # Apple, Cherry, Date, Elderberry

    # Search for items containing 'an'
    listWidget.setSearch("an")
    assert listWidget.search() == "an"
    filtered = listWidget.filteredItems()
    assert len(filtered) == 1  # Banana
    assert filtered[0].text() == "Banana"

    # Clear search
    listWidget.setSearch("")
    assert listWidget.search() == ""
    assert len(listWidget.filteredItems()) == 5

def test_listwidget_search_signal():
    '''
    Test that searchModified signal is emitted when search text changes.
    '''
    listWidget = ttk.TTkListWidget()

    listWidget.addItems(["Item 0", "Item 1", "Item 2"])

    search_texts = []
    listWidget.searchModified.connect(lambda text: search_texts.append(text))

    listWidget.setSearch("test")
    assert len(search_texts) == 1
    assert search_texts[0] == "test"

    listWidget.setSearch("test2")
    assert len(search_texts) == 2
    assert search_texts[1] == "test2"

    listWidget.setSearch("")
    assert len(search_texts) == 3
    assert search_texts[2] == ""

def test_listwidget_search_visibility():
    '''
    Test search visibility setting.
    '''
    listWidget1 = ttk.TTkListWidget(showSearch=True)
    assert listWidget1.searchVisibility() is True

    listWidget2 = ttk.TTkListWidget(showSearch=False)
    assert listWidget2.searchVisibility() is False

    # Test changing visibility
    listWidget1.setSearchVisibility(False)
    assert listWidget1.searchVisibility() is False

    listWidget2.setSearchVisibility(True)
    assert listWidget2.searchVisibility() is True

def test_listwidget_dragdrop_mode():
    '''
    Test drag-drop mode settings.
    '''
    listWidget = ttk.TTkListWidget()
    assert listWidget.dragDropMode() == ttk.TTkK.DragDropMode.NoDragDrop

    listWidget.setDragDropMode(ttk.TTkK.DragDropMode.AllowDrag)
    assert listWidget.dragDropMode() == ttk.TTkK.DragDropMode.AllowDrag

    listWidget.setDragDropMode(ttk.TTkK.DragDropMode.AllowDrop)
    assert listWidget.dragDropMode() == ttk.TTkK.DragDropMode.AllowDrop

    listWidget.setDragDropMode(ttk.TTkK.DragDropMode.AllowDragDrop)
    assert listWidget.dragDropMode() == ttk.TTkK.DragDropMode.AllowDragDrop

def test_listwidget_list_item():
    '''
    Test TTkListItem functionality.
    '''
    item = ttk.TTkListItem(text="Test Item", data="test_data")

    assert item.text() == "Test Item"
    assert item.data() == "test_data"

    # Test setText
    item.setText("New Text")
    assert item.text() == "New Text"

    # Test setData
    item.setData("new_data")
    assert item.data() == "new_data"

def test_listwidget_list_item_signal():
    '''
    Test that TTkListItem.dataChanged signal is emitted when item changes.
    '''
    item = ttk.TTkListItem(text="Test Item", data="test_data")

    signal_count = []
    item.dataChanged.connect(lambda: signal_count.append(1))

    item.setText("New Text")
    assert len(signal_count) == 1

    item.setData("new_data")
    assert len(signal_count) == 2

    # Setting same data shouldn't emit signal
    item.setData("new_data")
    assert len(signal_count) == 2

def test_listwidget_with_ttk_string():
    '''
    Test adding items with TTkString objects.
    '''
    listWidget = ttk.TTkListWidget()

    colored_text = ttk.TTkString("Colored Item", ttk.TTkColor.fg("#FF0000"))
    listWidget.addItem(colored_text)

    assert len(listWidget.items()) == 1
    assert listWidget.itemAt(0).text() == "Colored Item"

def test_listwidget_custom_list_items():
    '''
    Test adding custom TTkListItem objects.
    '''
    listWidget = ttk.TTkListWidget()

    item1 = ttk.TTkListItem(text="Custom Item 1", data={"id": 1})
    item2 = ttk.TTkListItem(text="Custom Item 2", data={"id": 2})

    listWidget.addItem(item1)
    listWidget.addItem(item2)

    assert len(listWidget.items()) == 2
    assert listWidget.itemAt(0).data() == {"id": 1}
    assert listWidget.itemAt(1).data() == {"id": 2}

def test_listwidget_items_vs_filtered_items():
    '''
    Test the difference between items() and filteredItems() with search.
    '''
    listWidget = ttk.TTkListWidget()

    listWidget.addItems(["Apple", "Apricot", "Banana", "Cherry"])

    # Without search, both should be the same
    assert len(listWidget.items()) == 4
    assert len(listWidget.filteredItems()) == 4

    # With search, items() should return all, filteredItems() should return matches
    listWidget.setSearch("Ap")
    assert len(listWidget.items()) == 4
    assert len(listWidget.filteredItems()) == 2
    assert listWidget.filteredItems()[0].text() == "Apple"
    assert listWidget.filteredItems()[1].text() == "Apricot"

def test_listwidget_empty_list():
    '''
    Test operations on empty list.
    '''
    listWidget = ttk.TTkListWidget()

    assert len(listWidget.items()) == 0
    assert len(listWidget.filteredItems()) == 0
    assert len(listWidget.selectedItems()) == 0
    assert len(listWidget.selectedLabels()) == 0
    assert listWidget.search() == ""

# ============================================================================
# TTkList (ScrollArea wrapper) Tests
# ============================================================================

def test_list_add_items():
    '''
    Test adding items to TTkList (which wraps TTkListWidget in a scroll area).
    '''
    ttkList = ttk.TTkList()

    assert len(ttkList.items()) == 0

    ttkList.addItem("Item 1")
    assert len(ttkList.items()) == 1

    ttkList.addItems(["Item 2", "Item 3"])
    assert len(ttkList.items()) == 3

def test_list_initial_items():
    '''
    Test creating TTkList with initial items.
    '''
    ttkList = ttk.TTkList(items=["Item 0", "Item 1", "Item 2"])

    assert len(ttkList.items()) == 3
    assert ttkList.itemAt(0).text() == "Item 0"
    assert ttkList.itemAt(1).text() == "Item 1"
    assert ttkList.itemAt(2).text() == "Item 2"

def test_list_selection_mode():
    '''
    Test TTkList with different selection modes.
    '''
    list1 = ttk.TTkList(selectionMode=ttk.TTkK.SingleSelection)
    assert list1.selectionMode() == ttk.TTkK.SingleSelection

    list2 = ttk.TTkList(selectionMode=ttk.TTkK.MultiSelection)
    assert list2.selectionMode() == ttk.TTkK.MultiSelection

def test_list_signals_forwarding():
    '''
    Test that signals are properly forwarded from TTkListWidget to TTkList.
    '''
    ttkList = ttk.TTkList()

    ttkList.addItems(["Item 0", "Item 1", "Item 2"])

    item_clicked = []
    text_clicked = []

    ttkList.itemClicked.connect(lambda item: item_clicked.append(item))
    ttkList.textClicked.connect(lambda text: text_clicked.append(text))

    ttkList.setCurrentRow(0)
    assert len(item_clicked) == 1
    assert len(text_clicked) == 1
    assert text_clicked[0] == "Item 0"

    ttkList.setCurrentRow(1)
    assert len(item_clicked) == 2
    assert len(text_clicked) == 2
    assert text_clicked[1] == "Item 1"

def test_list_dragdrop_mode():
    '''
    Test TTkList with drag-drop mode.
    '''
    ttkList = ttk.TTkList(dragDropMode=ttk.TTkK.DragDropMode.AllowDragDrop)
    assert ttkList.dragDropMode() == ttk.TTkK.DragDropMode.AllowDragDrop

def test_list_search():
    '''
    Test search functionality in TTkList.
    '''
    ttkList = ttk.TTkList()

    ttkList.addItems(["Apple", "Banana", "Cherry"])

    assert ttkList.search() == ""

    ttkList.setSearch("an")
    assert ttkList.search() == "an"
    assert len(ttkList.items()) == 3  # All items still exist
    # Note: filteredItems() is a TTkListWidget method, not forwarded to TTkList

def test_list_show_search():
    '''
    Test showSearch parameter in TTkList.
    '''
    list1 = ttk.TTkList(showSearch=True)
    assert list1.searchVisibility() is True

    list2 = ttk.TTkList(showSearch=False)
    assert list2.searchVisibility() is False

def test_list_remove_selected():
    '''
    Test removing selected items from list.
    '''
    ttkList = ttk.TTkList(selectionMode=ttk.TTkK.MultiSelection)

    ttkList.addItems(["Item 0", "Item 1", "Item 2", "Item 3"])

    item0 = ttkList.itemAt(0)
    item2 = ttkList.itemAt(2)

    ttkList.setCurrentItem(item0)
    ttkList.setCurrentItem(item2)

    assert len(ttkList.selectedItems()) == 2

    ttkList.removeItems(ttkList.selectedItems().copy())
    assert len(ttkList.items()) == 2
    assert ttkList.itemAt(0).text() == "Item 1"
    assert ttkList.itemAt(1).text() == "Item 3"
    assert len(ttkList.selectedItems()) == 0

def test_list_move_items_between_lists():
    '''
    Test moving items from one list to another (typical use case).
    '''
    list1 = ttk.TTkList(selectionMode=ttk.TTkK.MultiSelection)
    list2 = ttk.TTkList()

    list1.addItems(["Item 0", "Item 1", "Item 2"])

    item0 = list1.itemAt(0)
    item1 = list1.itemAt(1)

    list1.setCurrentItem(item0)
    list1.setCurrentItem(item1)

    selected = list1.selectedItems().copy()
    assert len(selected) == 2

    # Move selected items to list2
    list1.removeItems(selected)
    for item in selected:
        list2.addItem(item)

    assert len(list1.items()) == 1
    assert len(list2.items()) == 2
    assert list2.itemAt(0).text() == "Item 0"
    assert list2.itemAt(1).text() == "Item 1"

def test_list_mixed_data_types():
    '''
    Test adding items with mixed data types (strings, integers, custom objects).
    '''
    ttkList = ttk.TTkList()

    ttkList.addItem(123)
    ttkList.addItem(456.789)
    ttkList.addItem("String Item")
    ttkList.addItem(None)

    assert len(ttkList.items()) == 4
    assert ttkList.itemAt(0).text() == "123"
    assert ttkList.itemAt(1).text() == "456.789"
    assert ttkList.itemAt(2).text() == "String Item"
    assert ttkList.itemAt(3).text() == "None"
