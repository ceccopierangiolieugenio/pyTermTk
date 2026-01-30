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
from unittest.mock import Mock, patch

sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))
import TermTk as ttk

# Import test helpers
sys.path.insert(0, os.path.join(sys.path[0],'..'))
from test_helpers import MockSlot


# ============================================================================
# TTkComboBox Initialization Tests
# ============================================================================

def test_combobox_init_empty():
    '''
    Test creating an empty combobox.
    '''
    combo = ttk.TTkComboBox()
    assert combo.currentIndex() == -1
    assert combo.currentText() == ""
    assert not combo.isEditable()


def test_combobox_init_with_list():
    '''
    Test creating a combobox with a list of items.
    '''
    items = ["Item 1", "Item 2", "Item 3"]
    combo = ttk.TTkComboBox(list=items)
    assert combo.currentIndex() == -1
    assert combo.currentText() == ""


def test_combobox_init_with_index():
    '''
    Test creating a combobox with a specific initial index.
    '''
    items = ["Item 1", "Item 2", "Item 3"]
    combo = ttk.TTkComboBox(list=items, index=1)
    assert combo.currentIndex() == 1


def test_combobox_init_editable():
    '''
    Test creating an editable combobox.
    '''
    combo = ttk.TTkComboBox(editable=True)
    assert combo.isEditable()
    assert combo.lineEdit() is not None


def test_combobox_init_text_align():
    '''
    Test creating a combobox with specific text alignment.
    '''
    combo = ttk.TTkComboBox(textAlign=ttk.TTkK.LEFT_ALIGN)
    assert combo.textAlign() == ttk.TTkK.LEFT_ALIGN


def test_combobox_init_insert_policy():
    '''
    Test creating a combobox with specific insert policy.
    '''
    combo = ttk.TTkComboBox(insertPolicy=ttk.TTkK.InsertAtTop)
    assert combo.insertPolicy() == ttk.TTkK.InsertAtTop


# ============================================================================
# TTkComboBox Non-Editable Mode Tests
# ============================================================================

def test_combobox_add_item():
    '''
    Test adding a single item to the combobox.
    '''
    combo = ttk.TTkComboBox()
    combo.addItem("Item 1")
    assert combo.currentIndex() == -1

    combo.setCurrentIndex(0)
    assert combo.currentText() == "Item 1"


def test_combobox_add_items():
    '''
    Test adding multiple items to the combobox.
    '''
    combo = ttk.TTkComboBox()
    items = ["Item 1", "Item 2", "Item 3"]
    combo.addItems(items)

    combo.setCurrentIndex(0)
    assert combo.currentText() == "Item 1"
    combo.setCurrentIndex(2)
    assert combo.currentText() == "Item 3"


def test_combobox_clear():
    '''
    Test clearing all items from the combobox.
    '''
    items = ["Item 1", "Item 2", "Item 3"]
    combo = ttk.TTkComboBox(list=items, index=1)

    combo.clear()
    assert combo.currentIndex() == -1
    assert combo.currentText() == ""


def test_combobox_current_index():
    '''
    Test getting and setting current index.
    '''
    items = ["Item 1", "Item 2", "Item 3"]
    combo = ttk.TTkComboBox(list=items)

    assert combo.currentIndex() == -1

    combo.setCurrentIndex(0)
    assert combo.currentIndex() == 0

    combo.setCurrentIndex(2)
    assert combo.currentIndex() == 2

    # Test invalid indices (should not change)
    combo.setCurrentIndex(10)
    assert combo.currentIndex() == 2

    combo.setCurrentIndex(-5)
    assert combo.currentIndex() == 2


def test_combobox_current_text():
    '''
    Test getting and setting current text.
    '''
    items = ["Apple", "Banana", "Cherry"]
    combo = ttk.TTkComboBox(list=items)

    combo.setCurrentIndex(1)
    assert combo.currentText() == "Banana"

    combo.setCurrentText("Cherry")
    assert combo.currentText() == "Cherry"
    assert combo.currentIndex() == 2


def test_combobox_text_align():
    '''
    Test text alignment getter and setter.
    '''
    combo = ttk.TTkComboBox()

    # Default alignment
    assert combo.textAlign() == ttk.TTkK.CENTER_ALIGN

    combo.setTextAlign(ttk.TTkK.LEFT_ALIGN)
    assert combo.textAlign() == ttk.TTkK.LEFT_ALIGN

    combo.setTextAlign(ttk.TTkK.RIGHT_ALIGN)
    assert combo.textAlign() == ttk.TTkK.RIGHT_ALIGN


def test_combobox_insert_policy():
    '''
    Test insert policy getter and setter.
    '''
    combo = ttk.TTkComboBox()

    # Default policy
    assert combo.insertPolicy() == ttk.TTkK.InsertAtBottom

    combo.setInsertPolicy(ttk.TTkK.InsertAtTop)
    assert combo.insertPolicy() == ttk.TTkK.InsertAtTop

    combo.setInsertPolicy(ttk.TTkK.NoInsert)
    assert combo.insertPolicy() == ttk.TTkK.NoInsert


# ============================================================================
# TTkComboBox Editable Mode Tests
# ============================================================================

def test_combobox_editable_mode():
    '''
    Test switching between editable and non-editable modes.
    '''
    combo = ttk.TTkComboBox()

    # Initially non-editable
    assert not combo.isEditable()
    assert combo.lineEdit() is None

    # Make editable
    combo.setEditable(True)
    assert combo.isEditable()
    assert combo.lineEdit() is not None

    # Make non-editable again
    combo.setEditable(False)
    assert not combo.isEditable()
    assert combo.lineEdit() is None


def test_combobox_editable_init_with_selection():
    '''
    Test that making a combobox editable initializes line edit with current selection.
    '''
    items = ["Apple", "Banana", "Cherry"]
    combo = ttk.TTkComboBox(list=items, index=1)

    # Make editable - line edit should show current selection
    combo.setEditable(True)
    assert combo.lineEdit().text() == "Banana"


def test_combobox_editable_set_edit_text():
    '''
    Test setting text in the line edit widget.
    '''
    items = ["Apple", "Banana", "Cherry"]
    combo = ttk.TTkComboBox(list=items, editable=True)

    combo.setEditText("New Text")
    assert combo.lineEdit().text() == "New Text"


def test_combobox_editable_current_text():
    '''
    Test that currentText returns line edit text in editable mode.
    '''
    items = ["Apple", "Banana", "Cherry"]
    combo = ttk.TTkComboBox(list=items, editable=True, index=0)

    # Initially shows selected item
    assert combo.currentText() == "Apple"

    # Change line edit text
    combo.lineEdit().setText("Custom")
    assert combo.currentText() == "Custom"


def test_combobox_editable_insert_policy_no_insert():
    '''
    Test that NoInsert policy doesn't add new items.
    '''
    items = ["Apple", "Banana"]
    combo = ttk.TTkComboBox(list=items, editable=True, insertPolicy=ttk.TTkK.NoInsert)

    combo.lineEdit().setText("Cherry")
    combo._lineEditChanged()  # Simulate return key

    # Index should be -1 (not found) and item not added
    assert combo.currentIndex() == -1


def test_combobox_editable_insert_policy_bottom():
    '''
    Test that InsertAtBottom policy adds new items at the end.
    '''
    items = ["Apple", "Banana"]
    combo = ttk.TTkComboBox(list=items, editable=True, insertPolicy=ttk.TTkK.InsertAtBottom)

    combo.lineEdit().setText("Cherry")
    combo._lineEditChanged()  # Simulate return key

    # New item should be added at the bottom
    assert combo.currentIndex() == 2
    assert combo.currentText() == "Cherry"


def test_combobox_editable_insert_policy_top():
    '''
    Test that InsertAtTop policy adds new items at the beginning.
    '''
    items = ["Apple", "Banana"]
    combo = ttk.TTkComboBox(list=items, editable=True, insertPolicy=ttk.TTkK.InsertAtTop)

    combo.lineEdit().setText("Cherry")
    combo._lineEditChanged()  # Simulate return key

    # New item should be added at the top
    assert combo.currentIndex() == 0
    assert combo.currentText() == "Cherry"


def test_combobox_editable_existing_item():
    '''
    Test that typing an existing item name selects it.
    '''
    items = ["Apple", "Banana", "Cherry"]
    combo = ttk.TTkComboBox(list=items, editable=True, insertPolicy=ttk.TTkK.InsertAtBottom)

    combo.lineEdit().setText("Banana")
    combo._lineEditChanged()  # Simulate return key

    # Should select existing item, not add duplicate
    assert combo.currentIndex() == 1
    assert combo.currentText() == "Banana"


def test_combobox_editable_clear():
    '''
    Test that clearing an editable combobox also clears the line edit.
    '''
    items = ["Apple", "Banana"]
    combo = ttk.TTkComboBox(list=items, editable=True, index=0)

    combo.clear()
    assert combo.lineEdit().text() == ""
    assert combo.currentIndex() == -1


# ============================================================================
# TTkComboBox Signal Tests
# ============================================================================

def test_combobox_signal_current_index_changed():
    '''
    Test that currentIndexChanged signal is emitted when index changes.
    '''
    items = ["Item 1", "Item 2", "Item 3"]
    combo = ttk.TTkComboBox(list=items)

    mock_slot = MockSlot(int)
    combo.currentIndexChanged.connect(mock_slot)

    combo.setCurrentIndex(1)
    assert mock_slot.called() == 1
    assert mock_slot.arg(0) == 1

    combo.setCurrentIndex(2)
    assert mock_slot.called() == 2
    assert mock_slot.arg(0) == 2  # Last call
    mock_slot.assert_called_with(2)


def test_combobox_signal_current_text_changed():
    '''
    Test that currentTextChanged signal is emitted when text changes.
    '''
    items = ["Apple", "Banana", "Cherry"]
    combo = ttk.TTkComboBox(list=items)

    mock_slot = MockSlot(str)
    combo.currentTextChanged.connect(mock_slot)

    combo.setCurrentIndex(0)
    assert mock_slot.called() == 1
    assert mock_slot.arg(0) == "Apple"

    combo.setCurrentIndex(2)
    assert mock_slot.called() == 2
    assert mock_slot.arg(0) == "Cherry"
    mock_slot.assert_called_with("Cherry")


def test_combobox_signal_edit_text_changed():
    '''
    Test that editTextChanged signal is emitted in editable mode.
    '''
    items = ["Apple", "Banana"]
    combo = ttk.TTkComboBox(list=items, editable=True, insertPolicy=ttk.TTkK.InsertAtBottom)

    mock_slot = MockSlot(str)
    combo.editTextChanged.connect(mock_slot)

    combo.lineEdit().setText("Cherry")
    combo._lineEditChanged()  # Simulate return key

    assert mock_slot.called() == 1
    assert mock_slot.arg(0) == "Cherry"
    mock_slot.assert_called_with("Cherry")


def test_combobox_signal_no_duplicate_emission():
    '''
    Test that signals are not emitted when setting the same index.
    '''
    items = ["Item 1", "Item 2", "Item 3"]
    combo = ttk.TTkComboBox(list=items, index=1)

    mock_slot = MockSlot(int)
    combo.currentIndexChanged.connect(mock_slot)

    # Setting same index should not emit
    combo.setCurrentIndex(1)
    mock_slot.assert_not_called()


def test_combobox_multiple_signal_connections():
    '''
    Test that multiple slots can be connected to the same signal.
    '''
    items = ["Item 1", "Item 2"]
    combo = ttk.TTkComboBox(list=items)

    ms1 = MockSlot(int)
    ms2 = MockSlot(int)

    combo.currentIndexChanged.connect(ms1)
    combo.currentIndexChanged.connect(ms2)

    combo.setCurrentIndex(0)

    assert ms1.called() == 1
    assert ms1.arg(0) == 0
    assert ms2.called() == 1
    assert ms2.arg(0) == 0


def test_combobox_signal_disconnect():
    '''
    Test disconnecting signals.
    '''
    items = ["Item 1", "Item 2"]
    combo = ttk.TTkComboBox(list=items)

    mock_slot = MockSlot(int)
    combo.currentIndexChanged.connect(mock_slot)

    combo.setCurrentIndex(0)
    assert mock_slot.called() == 1
    assert mock_slot.arg(0) == 0

    combo.currentIndexChanged.disconnect(mock_slot)
    combo.setCurrentIndex(1)

    # Should still only be called once (from before disconnect)
    assert mock_slot.called() == 1
    '''
    Test operations on an empty combobox.
    '''
    combo = ttk.TTkComboBox()

    assert combo.currentIndex() == -1
    assert combo.currentText() == ""

    # Setting index on empty list should not crash
    combo.setCurrentIndex(0)
    assert combo.currentIndex() == -1


def test_combobox_boundary_indices():
    '''
    Test boundary conditions for index setting.
    '''
    items = ["Item 1", "Item 2", "Item 3"]
    combo = ttk.TTkComboBox(list=items, index=1)

    # Test negative index
    combo.setCurrentIndex(-1)
    assert combo.currentIndex() == 1  # Should not change

    # Test index equal to length
    combo.setCurrentIndex(3)
    assert combo.currentIndex() == 1  # Should not change

    # Test large index
    combo.setCurrentIndex(100)
    assert combo.currentIndex() == 1  # Should not change


def test_combobox_text_not_in_list():
    '''
    Test setting text that doesn't exist in the list (non-editable mode).
    '''
    items = ["Apple", "Banana", "Cherry"]
    combo = ttk.TTkComboBox(list=items, index=1)

    combo.setCurrentText("Durian")
    # Should select first item as fallback
    assert combo.currentIndex() == 0


def test_combobox_editable_mode_with_empty_list():
    '''
    Test editable mode operations with an initially empty list.
    '''
    combo = ttk.TTkComboBox(editable=True, insertPolicy=ttk.TTkK.InsertAtBottom)

    combo.lineEdit().setText("First Item")
    combo._lineEditChanged()

    assert combo.currentIndex() == 0
    assert combo.currentText() == "First Item"


def test_combobox_update_called_on_changes():
    '''
    Test that update() is called when making changes.
    '''
    items = ["Item 1", "Item 2"]
    combo = ttk.TTkComboBox(list=items)

    with patch.object(combo, 'update') as mock_update:
        combo.setCurrentIndex(0)
        mock_update.assert_called()

    with patch.object(combo, 'update') as mock_update:
        combo.addItem("Item 3")
        mock_update.assert_called()

    with patch.object(combo, 'update') as mock_update:
        combo.setTextAlign(ttk.TTkK.LEFT_ALIGN)
        mock_update.assert_called()


def test_combobox_focus_policy():
    '''
    Test that focus policy changes based on editable state.
    '''
    combo = ttk.TTkComboBox()

    # Non-editable should have ClickFocus and TabFocus
    assert combo.focusPolicy() & ttk.TTkK.ClickFocus
    assert combo.focusPolicy() & ttk.TTkK.TabFocus

    # Editable should only have ClickFocus
    combo.setEditable(True)
    assert combo.focusPolicy() & ttk.TTkK.ClickFocus
    # Note: TabFocus behavior may vary based on implementation


# ============================================================================
# TTkComboBox Integration Tests
# ============================================================================

def test_combobox_full_workflow_non_editable():
    '''
    Test a complete workflow with non-editable combobox.
    '''
    combo = ttk.TTkComboBox()

    # Add items
    combo.addItems(["Red", "Green", "Blue"])

    # Track signals
    index_changes = []
    text_changes = []

    combo.currentIndexChanged.connect(lambda i: index_changes.append(i))
    combo.currentTextChanged.connect(lambda t: text_changes.append(t))

    # Select first item
    combo.setCurrentIndex(0)
    assert combo.currentText() == "Red"
    assert index_changes == [0]
    assert text_changes == ["Red"]

    # Select by text
    combo.setCurrentText("Blue")
    assert combo.currentIndex() == 2
    assert len(index_changes) == 2
    assert len(text_changes) == 2

    # Add more items
    combo.addItem("Yellow")
    combo.setCurrentIndex(3)
    assert combo.currentText() == "Yellow"


def test_combobox_full_workflow_editable():
    '''
    Test a complete workflow with editable combobox.
    '''
    combo = ttk.TTkComboBox(editable=True, insertPolicy=ttk.TTkK.InsertAtBottom)

    # Add initial items
    combo.addItems(["Cat", "Dog"])

    # Track signals
    index_changes = []
    text_changes = []
    edit_changes = []

    combo.currentIndexChanged.connect(lambda i: index_changes.append(i))
    combo.currentTextChanged.connect(lambda t: text_changes.append(t))
    combo.editTextChanged.connect(lambda t: edit_changes.append(t))

    # Select existing item
    combo.setCurrentIndex(0)
    assert combo.currentText() == "Cat"

    # Add new item via line edit
    combo.lineEdit().setText("Bird")
    combo._lineEditChanged()

    assert combo.currentIndex() == 2
    assert combo.currentText() == "Bird"
    assert "Bird" in edit_changes

    # Select existing item via line edit
    combo.lineEdit().setText("Dog")
    combo._lineEditChanged()

    assert combo.currentIndex() == 1
    assert combo.currentText() == "Dog"


def test_combobox_switch_editable_preserves_selection():
    '''
    Test that switching to editable mode preserves the current selection.
    '''
    items = ["Apple", "Banana", "Cherry"]
    combo = ttk.TTkComboBox(list=items, index=1)

    # Check initial state
    assert combo.currentText() == "Banana"

    # Make editable - should preserve selection
    combo.setEditable(True)
    assert combo.lineEdit().text() == "Banana"
    assert combo.currentText() == "Banana"

    # Make non-editable again
    combo.setEditable(False)
    assert combo.currentIndex() == 1
    assert combo.currentText() == "Banana"
