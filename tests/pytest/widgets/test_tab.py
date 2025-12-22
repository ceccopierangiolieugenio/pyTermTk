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

sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))
import TermTk as ttk

# ============================================================================
# TTkTabBar Tests
# ============================================================================

def test_tabbar_add_tabs():
    '''
    Test adding tabs to TTkTabBar using addTab().
    Verifies that tabs are added correctly and currentIndex is updated.
    '''
    tabBar = ttk.TTkTabBar()

    assert tabBar.currentIndex() == -1

    index0 = tabBar.addTab("Tab 1")
    assert index0 == 0
    assert tabBar.currentIndex() == 0

    index1 = tabBar.addTab("Tab 2", data="data2")
    assert index1 == 1
    assert tabBar.currentIndex() == 0

    index2 = tabBar.addTab("Tab 3")
    assert index2 == 2
    assert tabBar.currentIndex() == 0

def test_tabbar_insert_tabs():
    '''
    Test inserting tabs at specific positions in TTkTabBar.
    Verifies that tabs are inserted at correct indices and currentIndex is adjusted.
    '''
    tabBar = ttk.TTkTabBar()

    tabBar.addTab("Tab 1")
    tabBar.addTab("Tab 2")
    tabBar.addTab("Tab 3")

    # Insert at beginning
    index = tabBar.insertTab(0, "Tab 0")
    assert index == 0
    assert tabBar.currentIndex() == 1  # Current should shift

    # Insert in middle
    index = tabBar.insertTab(2, "Tab 1.5")
    assert index == 2
    assert tabBar.currentIndex() == 1  # Current shouldn't change

def test_tabbar_remove_tabs():
    '''
    Test removing tabs from TTkTabBar.
    Verifies that tabs are removed correctly and currentIndex is adjusted.
    '''
    tabBar = ttk.TTkTabBar()

    tabBar.addTab("Tab 0")
    tabBar.addTab("Tab 1")
    tabBar.addTab("Tab 2")
    tabBar.addTab("Tab 3")

    tabBar.setCurrentIndex(2)
    assert tabBar.currentIndex() == 2

    # Remove tab before current
    tabBar.removeTab(0)
    assert tabBar.currentIndex() == 1  # Should decrement

    # Remove current tab
    tabBar.removeTab(1)
    assert tabBar.currentIndex() == 0  # Should stay but point to next tab

    # Remove last tab
    tabBar.removeTab(1)
    assert tabBar.currentIndex() == 0

def test_tabbar_tab_data():
    '''
    Test setting and getting tab data.
    '''
    tabBar = ttk.TTkTabBar()

    tabBar.addTab("Tab 1", data="data1")
    tabBar.addTab("Tab 2", data={"key": "value"})
    tabBar.addTab("Tab 3")

    assert tabBar.tabData(0) == "data1"
    assert tabBar.tabData(1) == {"key": "value"}
    assert tabBar.tabData(2) is None

    # Test setTabData
    tabBar.setTabData(2, "new_data")
    assert tabBar.tabData(2) == "new_data"

    # Test currentData
    tabBar.setCurrentIndex(1)
    assert tabBar.currentData() == {"key": "value"}

def test_tabbar_current_index():
    '''
    Test setting and getting current index.
    '''
    tabBar = ttk.TTkTabBar()

    tabBar.addTab("Tab 0")
    tabBar.addTab("Tab 1")
    tabBar.addTab("Tab 2")

    assert tabBar.currentIndex() == 0

    tabBar.setCurrentIndex(1)
    assert tabBar.currentIndex() == 1

    tabBar.setCurrentIndex(2)
    assert tabBar.currentIndex() == 2

    # Test invalid index (should not change)
    tabBar.setCurrentIndex(10)
    assert tabBar.currentIndex() == 2

    tabBar.setCurrentIndex(-1)
    assert tabBar.currentIndex() == 2

def test_tabbar_signals():
    '''
    Test that signals are emitted correctly.
    '''
    tabBar = ttk.TTkTabBar()

    current_changed_called = []
    tab_clicked_called = []
    tab_close_called = []

    tabBar.currentChanged.connect(lambda i: current_changed_called.append(i))
    tabBar.tabBarClicked.connect(lambda i: tab_clicked_called.append(i))
    tabBar.tabCloseRequested.connect(lambda i: tab_close_called.append(i))

    tabBar.addTab("Tab 0")
    assert len(current_changed_called) == 1
    assert current_changed_called[0] == 0

    tabBar.addTab("Tab 1")
    tabBar.setCurrentIndex(1)
    assert len(current_changed_called) == 2
    assert current_changed_called[1] == 1

def test_tabbar_closable_tabs():
    '''
    Test closable tabs functionality.
    '''
    tabBar = ttk.TTkTabBar(closable=True)

    assert tabBar.tabsClosable() is True

    tabBar.addTab("Tab 0")
    tabBar.addTab("Tab 1", closable=False)  # Override for this tab
    tabBar.addTab("Tab 2")

    # Test that tabs can be added with different closable settings
    button0 = tabBar.tabButton(0)
    button1 = tabBar.tabButton(1)
    button2 = tabBar.tabButton(2)

    assert button0 is not None
    assert button1 is not None
    assert button2 is not None

# ============================================================================
# TTkTabWidget Tests
# ============================================================================

def test_tabwidget_add_tabs():
    '''
    Test adding tabs to TTkTabWidget with widgets.
    '''
    tabWidget = ttk.TTkTabWidget()

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    assert tabWidget.count() == 0
    assert tabWidget.currentIndex() == -1

    index0 = tabWidget.addTab(widget0, "Tab 0")
    assert index0 == 0
    assert tabWidget.count() == 1
    assert tabWidget.currentIndex() == 0
    assert widget0.parentWidget() == tabWidget

    index1 = tabWidget.addTab(widget1, "Tab 1", data="data1")
    assert index1 == 1
    assert tabWidget.count() == 2

    index2 = tabWidget.addTab(widget2, "Tab 2")
    assert index2 == 2
    assert tabWidget.count() == 3

def test_tabwidget_insert_tabs():
    '''
    Test inserting tabs at specific positions.
    '''
    tabWidget = ttk.TTkTabWidget()

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()
    widget3 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1")
    tabWidget.addTab(widget2, "Tab 2")

    # Insert at beginning
    index = tabWidget.insertTab(0, widget3, "Tab -1")
    assert index == 0
    assert tabWidget.count() == 4
    assert tabWidget.widget(0) == widget3
    assert tabWidget.currentIndex() == 1  # Should shift

def test_tabwidget_remove_tabs():
    '''
    Test removing tabs from TTkTabWidget.
    '''
    tabWidget = ttk.TTkTabWidget()

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1")
    tabWidget.addTab(widget2, "Tab 2")

    assert tabWidget.count() == 3

    tabWidget.removeTab(1)
    assert tabWidget.count() == 2
    assert tabWidget.widget(0) == widget0
    assert tabWidget.widget(1) == widget2

    tabWidget.removeTab(0)
    assert tabWidget.count() == 1
    assert tabWidget.widget(0) == widget2

def test_tabwidget_current_widget():
    '''
    Test getting and setting current widget.
    '''
    tabWidget = ttk.TTkTabWidget()

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1")
    tabWidget.addTab(widget2, "Tab 2")

    assert tabWidget.currentWidget() == widget0

    tabWidget.setCurrentWidget(widget1)
    assert tabWidget.currentWidget() == widget1
    assert tabWidget.currentIndex() == 1

    tabWidget.setCurrentWidget(widget2)
    assert tabWidget.currentWidget() == widget2
    assert tabWidget.currentIndex() == 2

def test_tabwidget_widget_by_index():
    '''
    Test accessing widgets by index.
    '''
    tabWidget = ttk.TTkTabWidget()

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1")
    tabWidget.addTab(widget2, "Tab 2")

    assert tabWidget.widget(0) == widget0
    assert tabWidget.widget(1) == widget1
    assert tabWidget.widget(2) == widget2
    assert tabWidget.widget(10) is None
    assert tabWidget.widget(-1) is None

def test_tabwidget_index_of():
    '''
    Test finding index of a widget.
    '''
    tabWidget = ttk.TTkTabWidget()

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()
    widget_not_added = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1")
    tabWidget.addTab(widget2, "Tab 2")

    assert tabWidget.indexOf(widget0) == 0
    assert tabWidget.indexOf(widget1) == 1
    assert tabWidget.indexOf(widget2) == 2
    assert tabWidget.indexOf(widget_not_added) == -1

def test_tabwidget_tab_data():
    '''
    Test tab data in TTkTabWidget.
    '''
    tabWidget = ttk.TTkTabWidget()

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0", data="data0")
    tabWidget.addTab(widget1, "Tab 1", data={"key": "value"})

    assert tabWidget.tabData(0) == "data0"
    assert tabWidget.tabData(1) == {"key": "value"}

    tabWidget.setTabData(0, "new_data")
    assert tabWidget.tabData(0) == "new_data"

    assert tabWidget.currentData() == "new_data"

def test_tabwidget_signals():
    '''
    Test that TTkTabWidget signals are emitted correctly.
    '''
    tabWidget = ttk.TTkTabWidget()

    current_changed_called = []
    tab_clicked_called = []

    tabWidget.currentChanged.connect(lambda i: current_changed_called.append(i))
    tabWidget.tabBarClicked.connect(lambda i: tab_clicked_called.append(i))

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    assert len(current_changed_called) == 1

    tabWidget.addTab(widget1, "Tab 1")
    tabWidget.setCurrentIndex(1)
    assert len(current_changed_called) == 2
    assert current_changed_called[1] == 1

def test_tabwidget_widget_visibility():
    '''
    Test that only the current widget is visible.
    '''
    tabWidget = ttk.TTkTabWidget()

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1")
    tabWidget.addTab(widget2, "Tab 2")

    # Initially all should be hidden (added hidden)
    assert widget0.isVisible() is True
    assert widget1.isVisible() is False
    assert widget2.isVisible() is False

    # After setting index, current should be visible
    tabWidget.setCurrentIndex(0)
    # Note: Visibility is controlled internally, check currentWidget
    assert tabWidget.currentWidget() == widget0

    tabWidget.setCurrentIndex(1)
    assert tabWidget.currentWidget() == widget1

    tabWidget.setCurrentIndex(2)
    assert tabWidget.currentWidget() == widget2

def test_tabwidget_closable():
    '''
    Test closable tabs in TTkTabWidget.
    '''
    tabWidget = ttk.TTkTabWidget(closable=True)

    assert tabWidget.tabsClosable() is True

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1", closable=False)

    # Both tabs should be added
    assert tabWidget.count() == 2

def test_tabwidget_remove_all_tabs():
    '''
    Test removing all tabs from TTkTabWidget.
    '''
    tabWidget = ttk.TTkTabWidget()

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1")
    tabWidget.addTab(widget2, "Tab 2")

    assert tabWidget.count() == 3

    tabWidget.removeTab(0)
    tabWidget.removeTab(0)
    tabWidget.removeTab(0)

    assert tabWidget.count() == 0
    assert tabWidget.currentIndex() == -1

def test_tabwidget_bar_type():
    '''
    Test different bar types.
    '''
    from TermTk.TTkWidgets.tabwidget import TTkBarType

    tabWidget1 = ttk.TTkTabWidget(barType=TTkBarType.DEFAULT_3)
    tabWidget2 = ttk.TTkTabWidget(barType=TTkBarType.DEFAULT_2)
    tabWidget3 = ttk.TTkTabWidget(barType=TTkBarType.NERD_1)

    # Just verify they can be created
    assert tabWidget1 is not None
    assert tabWidget2 is not None
    assert tabWidget3 is not None

# ============================================================================
# Drag and Drop Related Tests
# ============================================================================

def test_tabwidget_drag_data_classes():
    '''
    Test that drag data classes exist and can be instantiated.
    '''
    from TermTk.TTkWidgets.tabwidget import (
        _TTkTabWidgetDragData,
        _TTkNewTabWidgetDragData,
        _TTkTabBarDragData
    )

    tabWidget = ttk.TTkTabWidget()
    widget = ttk.TTkWidget()
    tabWidget.addTab(widget, "Tab 0")

    button = tabWidget.tabButton(0)

    # Test _TTkTabWidgetDragData
    drag_data1 = _TTkTabWidgetDragData(button, tabWidget)
    assert drag_data1.tabButton() == button
    assert drag_data1.tabWidget() == tabWidget

    # Test _TTkNewTabWidgetDragData
    new_widget = ttk.TTkWidget()
    drag_data2 = _TTkNewTabWidgetDragData("Label", new_widget, data="test", closable=True)
    assert drag_data2.label() == "Label"
    assert drag_data2.widget() == new_widget
    assert drag_data2.data() == "test"
    assert drag_data2.closable() is True

    # Test _TTkTabBarDragData
    tabBar = ttk.TTkTabBar()
    tabBar.addTab("Tab")
    bar_button = tabBar.tabButton(0)
    drag_data3 = _TTkTabBarDragData(bar_button, tabBar)
    assert drag_data3.tabButton() == bar_button
    assert drag_data3.tabBar() == tabBar

def test_tabbar_tab_button():
    '''
    Test accessing tab buttons from TTkTabBar.
    '''
    tabBar = ttk.TTkTabBar()

    tabBar.addTab("Tab 0")
    tabBar.addTab("Tab 1")
    tabBar.addTab("Tab 2")

    button0 = tabBar.tabButton(0)
    button1 = tabBar.tabButton(1)
    button2 = tabBar.tabButton(2)

    assert button0 is not None
    assert button1 is not None
    assert button2 is not None

    # Test button text
    assert button0.text() == "Tab 0"
    assert button1.text() == "Tab 1"
    assert button2.text() == "Tab 2"

    # Test invalid index
    assert tabBar.tabButton(10) is None
    assert tabBar.tabButton(-1) is None

def test_tabwidget_tab_button():
    '''
    Test accessing tab buttons from TTkTabWidget.
    '''
    tabWidget = ttk.TTkTabWidget()

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1")

    button0 = tabWidget.tabButton(0)
    button1 = tabWidget.tabButton(1)

    assert button0 is not None
    assert button1 is not None
    assert button0.text() == "Tab 0"
    assert button1.text() == "Tab 1"

def test_tabbar_multiple_add_remove():
    '''
    Test multiple add/remove operations to ensure state consistency.
    '''
    tabBar = ttk.TTkTabBar()

    # Add multiple tabs
    for i in range(5):
        tabBar.addTab(f"Tab {i}")

    assert tabBar.currentIndex() == 0

    # Remove some tabs
    tabBar.removeTab(2)
    tabBar.removeTab(1)

    # Add more tabs
    tabBar.addTab("New Tab 1")
    tabBar.addTab("New Tab 2")

    # Verify state is consistent
    assert tabBar.tabButton(0) is not None
    assert tabBar.tabButton(0).text() == "Tab 0"

def test_tabwidget_multiple_add_remove():
    '''
    Test multiple add/remove operations with widgets.
    '''
    tabWidget = ttk.TTkTabWidget()

    widgets = [ttk.TTkWidget() for _ in range(5)]

    # Add all widgets
    for i, widget in enumerate(widgets):
        tabWidget.addTab(widget, f"Tab {i}")

    assert tabWidget.count() == 5

    # Remove some
    tabWidget.removeTab(2)
    tabWidget.removeTab(1)

    assert tabWidget.count() == 3

    # Add more
    new_widget = ttk.TTkWidget()
    tabWidget.addTab(new_widget, "New Tab")

    assert tabWidget.count() == 4

def test_tabbar_set_current_after_remove():
    '''
    Test that setting current index works correctly after removing tabs.
    '''
    tabBar = ttk.TTkTabBar()

    tabBar.addTab("Tab 0")
    tabBar.addTab("Tab 1")
    tabBar.addTab("Tab 2")
    tabBar.addTab("Tab 3")

    tabBar.setCurrentIndex(3)
    assert tabBar.currentIndex() == 3

    # Remove current tab
    tabBar.removeTab(3)

    # Current should be adjusted
    assert tabBar.currentIndex() < 3

    # Should be able to set to valid index
    tabBar.setCurrentIndex(1)
    assert tabBar.currentIndex() == 1

def test_tabwidget_parent_relationship():
    '''
    Test that widgets maintain correct parent relationships when added to tabs.
    '''
    tabWidget = ttk.TTkTabWidget()

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()

    assert widget0.parentWidget() is None
    assert widget1.parentWidget() is None

    tabWidget.addTab(widget0, "Tab 0")
    assert widget0.parentWidget() == tabWidget

    tabWidget.addTab(widget1, "Tab 1")
    assert widget1.parentWidget() == tabWidget

    # After removal, parent should still be tabWidget (it's in the layout)
    tabWidget.removeTab(0)
    # Note: The widget may still have tabWidget as parent depending on implementation

def test_tabbar_empty_initialization():
    '''
    Test that empty TTkTabBar initializes correctly.
    '''
    tabBar = ttk.TTkTabBar()

    assert tabBar.currentIndex() == -1
    assert tabBar.tabButton(0) is None
    assert tabBar.tabData(0) is None
    assert tabBar.currentData() is None

def test_tabwidget_empty_initialization():
    '''
    Test that empty TTkTabWidget initializes correctly.
    '''
    tabWidget = ttk.TTkTabWidget()

    assert tabWidget.count() == 0
    assert tabWidget.currentIndex() == -1
    assert tabWidget.widget(0) is None
    assert tabWidget.indexOf(ttk.TTkWidget()) == -1

# ============================================================================
# Keyboard Navigation Tests
# ============================================================================

def test_tabbar_highlight_navigation_with_arrow_keys():
    '''
    Test that arrow keys navigate through highlighted tabs.
    '''
    tabBar = ttk.TTkTabBar()

    tabBar.addTab("Tab 0")
    tabBar.addTab("Tab 1")
    tabBar.addTab("Tab 2")
    tabBar.addTab("Tab 3")

    # Initial state - highlighted should be 0
    assert tabBar._tabStatus.highlighted == None
    assert tabBar.currentIndex() == 0

    # Press Right arrow
    evt = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Right, "", ttk.TTkK.NoModifier)
    result = tabBar.keyEvent(evt)
    assert result is True
    assert tabBar._tabStatus.highlighted == 1
    assert tabBar.currentIndex() == 0  # Current doesn't change yet

    # Press Right arrow again
    result = tabBar.keyEvent(evt)
    assert result is True
    assert tabBar._tabStatus.highlighted == 2

    # Press Left arrow
    evt = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Left, "", ttk.TTkK.NoModifier)
    result = tabBar.keyEvent(evt)
    assert result is True
    assert tabBar._tabStatus.highlighted == 1

def test_tabbar_enter_activates_highlighted_tab():
    '''
    Test that pressing Enter activates the highlighted tab.
    '''
    tabBar = ttk.TTkTabBar()

    tabBar.addTab("Tab 0")
    tabBar.addTab("Tab 1")
    tabBar.addTab("Tab 2")

    # Set current to Tab 0
    tabBar.setCurrentIndex(0)
    assert tabBar.currentIndex() == 0

    # Highlight Tab 2 using arrow keys
    evt_right = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Right, "", ttk.TTkK.NoModifier)
    tabBar.keyEvent(evt_right)
    tabBar.keyEvent(evt_right)
    tabBar.keyEvent(evt_right)
    assert tabBar._tabStatus.highlighted == 2
    assert tabBar.currentIndex() == 0  # Still on Tab 0

    # Press Enter to activate highlighted tab
    evt_enter = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Enter, "", ttk.TTkK.NoModifier)
    result = tabBar.keyEvent(evt_enter)
    assert result is True
    assert tabBar.currentIndex() == 2  # Now switched to Tab 2

def test_tabbar_space_activates_highlighted_tab():
    '''
    Test that pressing Space activates the highlighted tab.
    '''
    tabBar = ttk.TTkTabBar()

    tabBar.addTab("Tab 0")
    tabBar.addTab("Tab 1")
    tabBar.addTab("Tab 2")

    # Set current to Tab 0
    tabBar.setCurrentIndex(0)
    assert tabBar.currentIndex() == 0

    # Highlight Tab 1 using arrow key
    evt_right = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Right, "", ttk.TTkK.NoModifier)
    tabBar.keyEvent(evt_right)
    assert tabBar._tabStatus.highlighted == 1
    assert tabBar.currentIndex() == 0  # Still on Tab 0

    # Press Space to activate highlighted tab
    evt_space = ttk.TTkKeyEvent(ttk.TTkK.Character, " ", " ", ttk.TTkK.NoModifier)
    result = tabBar.keyEvent(evt_space)
    assert result is True
    assert tabBar.currentIndex() == 1  # Now switched to Tab 1

def test_tabwidget_enter_shows_highlighted_widget():
    '''
    Test that pressing Enter shows the widget of the highlighted tab.
    '''
    tabWidget = ttk.TTkTabWidget()
    tabBar = tabWidget._tabStatus.tabBar

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1")
    tabWidget.addTab(widget2, "Tab 2")

    # Initially Tab 0 is current
    assert tabWidget.currentIndex() == 0
    assert tabWidget.currentWidget() == widget0

    evt_right = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Right, "", ttk.TTkK.NoModifier)
    tabBar.keyEvent(evt_right)
    tabBar.keyEvent(evt_right)
    tabBar.keyEvent(evt_right)
    assert tabBar._tabStatus.highlighted == 2

    # Press Enter to activate
    evt_enter = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Enter, "", ttk.TTkK.NoModifier)
    result = tabBar.keyEvent(evt_enter)

    # Verify the widget changed
    assert tabWidget.currentIndex() == 2
    assert tabWidget.currentWidget() == widget2

def test_tabwidget_space_shows_highlighted_widget():
    '''
    Test that pressing Space shows the widget of the highlighted tab.
    '''
    tabWidget = ttk.TTkTabWidget()
    tabBar = tabWidget._tabStatus.tabBar

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1")
    tabWidget.addTab(widget2, "Tab 2")

    # Initially Tab 0 is current
    assert tabWidget.currentIndex() == 0
    assert tabWidget.currentWidget() == widget0

    # Navigate to Tab 1 using arrow key
    evt_right = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Right, "", ttk.TTkK.NoModifier)
    tabBar.setFocus()
    tabBar.keyEvent(evt_right)
    assert tabWidget._tabStatus.highlighted == 1

    # Press Space to activate
    evt_space = ttk.TTkKeyEvent(ttk.TTkK.Character, " ", " ", ttk.TTkK.NoModifier)
    result = tabBar.keyEvent(evt_space)

    # Verify the widget changed
    assert tabWidget.currentIndex() == 1
    assert tabWidget.currentWidget() == widget1

def test_tabbar_highlight_bounds():
    '''
    Test that highlight stays within bounds when navigating.
    '''
    tabBar = ttk.TTkTabBar()

    tabBar.addTab("Tab 0")
    tabBar.addTab("Tab 1")
    tabBar.addTab("Tab 2")

    # At start
    assert tabBar._tabStatus.highlighted == None

    # Try to go left from first tab
    evt_left = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Left, "", ttk.TTkK.NoModifier)
    tabBar.keyEvent(evt_left)
    assert tabBar._tabStatus.highlighted == 0  # Should stay at 0

    # Navigate to last tab
    evt_right = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Right, "", ttk.TTkK.NoModifier)
    tabBar.keyEvent(evt_right)
    tabBar.keyEvent(evt_right)
    assert tabBar._tabStatus.highlighted == 2

    # Try to go right from last tab
    tabBar.keyEvent(evt_right)
    assert tabBar._tabStatus.highlighted == 2  # Should stay at 2

def test_tabwidget_keyboard_navigation_with_signals():
    '''
    Test that currentChanged signal is emitted when activating with Enter/Space.
    '''
    tabWidget = ttk.TTkTabWidget()
    tabBar = tabWidget._tabStatus.tabBar

    widget0 = ttk.TTkWidget()
    widget1 = ttk.TTkWidget()

    tabWidget.addTab(widget0, "Tab 0")
    tabWidget.addTab(widget1, "Tab 1")

    current_changed_calls = []
    tabWidget.currentChanged.connect(lambda i: current_changed_calls.append(i))

    # Clear initial signal
    current_changed_calls.clear()

    # Highlight Tab 1 and activate with Enter
    tabBar.setFocus()
    evt_right = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Right, "", ttk.TTkK.NoModifier)
    tabBar.keyEvent(evt_right)
    tabBar.keyEvent(evt_right)

    evt_enter = ttk.TTkKeyEvent(ttk.TTkK.SpecialKey, ttk.TTkK.Key_Enter, "", ttk.TTkK.NoModifier)
    tabBar.keyEvent(evt_enter)

    # Signal should be emitted
    assert len(current_changed_calls) == 1
    assert current_changed_calls[0] == 1
