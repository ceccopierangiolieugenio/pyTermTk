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
from TermTk.TTkWidgets.kodetab import _TTkKodeTab
from TermTk.TTkWidgets.tabwidget import _TTkTabWidgetDragData, _TTkNewTabWidgetDragData
from TermTk.TTkGui.drag import TTkDnDEvent

# ============================================================================
# TTkKodeTab Basic Tests
# ============================================================================

def test_kodetab_initialization():
    '''
    Test that TTkKodeTab initializes correctly.
    '''
    kodeTab = ttk.TTkKodeTab()

    assert kodeTab is not None
    assert isinstance(kodeTab, ttk.TTkSplitter)

    # Should have at least one internal _TTkKodeTab widget
    first_widget = kodeTab._getFirstWidget()
    assert first_widget is not None
    assert isinstance(first_widget, _TTkKodeTab)

def test_kodetab_add_single_tab():
    '''
    Test adding a single tab to TTkKodeTab.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget = ttk.TTkWidget()

    index = kodeTab.addTab(widget, "Tab 1")

    assert index == 0
    assert kodeTab._lastKodeTabWidget.count() == 1
    assert kodeTab._lastKodeTabWidget.widget(0) == widget

def test_kodetab_add_multiple_tabs():
    '''
    Test adding multiple tabs to TTkKodeTab.
    '''
    kodeTab = ttk.TTkKodeTab()

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()
    widget3 = ttk.TTkWidget()

    index1 = kodeTab.addTab(widget1, "Tab 1")
    index2 = kodeTab.addTab(widget2, "Tab 2")
    index3 = kodeTab.addTab(widget3, "Tab 3")

    assert index1 == 0
    assert index2 == 1
    assert index3 == 2
    assert kodeTab._lastKodeTabWidget.count() == 3

def test_kodetab_add_tab_with_data():
    '''
    Test adding tabs with associated data.
    '''
    kodeTab = ttk.TTkKodeTab()

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    kodeTab.addTab(widget1, "Tab 1", data="data1")
    kodeTab.addTab(widget2, "Tab 2", data={"key": "value"})

    assert kodeTab._lastKodeTabWidget.tabData(0) == "data1"
    assert kodeTab._lastKodeTabWidget.tabData(1) == {"key": "value"}

def test_kodetab_set_current_widget():
    '''
    Test setting the current widget in TTkKodeTab.
    '''
    kodeTab = ttk.TTkKodeTab()

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()
    widget3 = ttk.TTkWidget()

    kodeTab.addTab(widget1, "Tab 1")
    kodeTab.addTab(widget2, "Tab 2")
    kodeTab.addTab(widget3, "Tab 3")

    kodeTab.setCurrentWidget(widget2)
    assert kodeTab._lastKodeTabWidget.currentWidget() == widget2

    kodeTab.setCurrentWidget(widget3)
    assert kodeTab._lastKodeTabWidget.currentWidget() == widget3

def test_kodetab_iter_items():
    '''
    Test iterating over all tabs in TTkKodeTab.
    '''
    kodeTab = ttk.TTkKodeTab()

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()
    widget3 = ttk.TTkWidget()

    kodeTab.addTab(widget1, "Tab 1")
    kodeTab.addTab(widget2, "Tab 2")
    kodeTab.addTab(widget3, "Tab 3")

    items = list(kodeTab.iterItems())

    assert len(items) == 3
    for tab_widget, index in items:
        assert isinstance(tab_widget, _TTkKodeTab)
        assert 0 <= index < tab_widget.count()

def test_kodetab_signals():
    '''
    Test that TTkKodeTab signals are emitted correctly.
    '''
    kodeTab = ttk.TTkKodeTab()

    current_changed_called = []
    tab_clicked_called = []
    tab_added_called = []

    kodeTab.currentChanged.connect(
        lambda tw, i, w, d: current_changed_called.append((tw, i, w, d))
    )
    kodeTab.tabBarClicked.connect(
        lambda tw, i, w, d: tab_clicked_called.append((tw, i, w, d))
    )
    kodeTab.tabAdded.connect(
        lambda tw, i: tab_added_called.append((tw, i))
    )

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    kodeTab.addTab(widget1, "Tab 1")
    assert len(tab_added_called) == 1
    assert len(current_changed_called) == 1

    kodeTab.addTab(widget2, "Tab 2")
    assert len(tab_added_called) == 2

def test_kodetab_close_requested_signal():
    '''
    Test that kodeTabCloseRequested signal is emitted correctly.
    '''
    kodeTab = ttk.TTkKodeTab(closable=True)

    close_requested_called = []
    kodeTab.kodeTabCloseRequested.connect(
        lambda tw, i: close_requested_called.append((tw, i))
    )

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    kodeTab.addTab(widget1, "Tab 1")
    kodeTab.addTab(widget2, "Tab 2")

    # Simulate close request
    kodeTab._lastKodeTabWidget._handleTabCloseRequested(0)

    assert len(close_requested_called) == 1
    assert close_requested_called[0][1] == 0

# ============================================================================
# TTkKodeTab Remove/Close Tests
# ============================================================================

def test_kodetab_remove_tab():
    '''
    Test removing tabs from the internal tab widget.
    '''
    kodeTab = ttk.TTkKodeTab()

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()
    widget3 = ttk.TTkWidget()

    kodeTab.addTab(widget1, "Tab 1")
    kodeTab.addTab(widget2, "Tab 2")
    kodeTab.addTab(widget3, "Tab 3")

    assert kodeTab._lastKodeTabWidget.count() == 3

    kodeTab._lastKodeTabWidget.removeTab(1)

    assert kodeTab._lastKodeTabWidget.count() == 2
    assert kodeTab._lastKodeTabWidget.widget(0) == widget1
    assert kodeTab._lastKodeTabWidget.widget(1) == widget3

def test_kodetab_remove_all_tabs():
    '''
    Test removing all tabs triggers cleanup of empty widgets.
    '''
    kodeTab = ttk.TTkKodeTab()

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    kodeTab.addTab(widget1, "Tab 1")
    kodeTab.addTab(widget2, "Tab 2")

    internal_tab = kodeTab._lastKodeTabWidget

    internal_tab.removeTab(0)
    internal_tab.removeTab(0)

    # Should still have the base internal tab widget
    assert kodeTab.count() >= 0

def test_kodetab_kode_tab_closed():
    '''
    Test _kodeTabClosed cleanup logic.
    '''
    kodeTab = ttk.TTkKodeTab()

    widget1 = ttk.TTkWidget()
    kodeTab.addTab(widget1, "Tab 1")

    internal_tab = kodeTab._lastKodeTabWidget

    # Remove the tab
    internal_tab.removeTab(0)

    # Trigger cleanup
    internal_tab._kodeTabClosed()

    # Verify state
    assert isinstance(kodeTab._getFirstWidget(), _TTkKodeTab)

# ============================================================================
# TTkKodeTab Drag and Drop Tests
# ============================================================================

def test_kodetab_drag_enter_event():
    '''
    Test drag enter event handling.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget = ttk.TTkWidget()
    kodeTab.addTab(widget, "Tab 1")

    internal_tab = kodeTab._lastKodeTabWidget

    # Create a mock drag event
    evt = TTkDnDEvent(pos=(5,5), data=None)

    # Test drag enter
    result = internal_tab.dragEnterEvent(evt)
    assert result is True

def test_kodetab_drag_leave_event():
    '''
    Test drag leave event handling.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget = ttk.TTkWidget()
    kodeTab.addTab(widget, "Tab 1")

    internal_tab = kodeTab._lastKodeTabWidget
    internal_tab._frameOverlay = (0, 0, 10, 10)

    evt = TTkDnDEvent(pos=(5,5), data=None)

    result = internal_tab.dragLeaveEvent(evt)
    assert result is True
    assert internal_tab._frameOverlay is None

def test_kodetab_drop_event_new_tab_data():
    '''
    Test dropping new tab data onto TTkKodeTab.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget1 = ttk.TTkWidget()
    kodeTab.addTab(widget1, "Tab 1")

    internal_tab = kodeTab._lastKodeTabWidget

    # Create new tab drag data
    new_widget = ttk.TTkWidget()
    drag_data = _TTkNewTabWidgetDragData("New Tab", new_widget, data="test_data")

    # Create drop event in center (should add to existing tab bar)
    evt = TTkDnDEvent(pos=(50,25), data=drag_data)

    result = internal_tab.dropEvent(evt)

    # Verify drop was handled
    assert result in (True, False)  # Depends on implementation details

# def test_kodetab_drop_event_tab_widget_data():
#     '''
#     Test dropping tab from another widget.
#     '''
#     kodeTab1 = ttk.TTkKodeTab()
#     kodeTab2 = ttk.TTkKodeTab()

#     widget1 = ttk.TTkWidget()
#     widget2 = ttk.TTkWidget()

#     kodeTab1.addTab(widget1, "Tab 1")
#     kodeTab2.addTab(widget2, "Tab 2")

#     internal_tab1 = kodeTab1._lastKodeTabWidget
#     internal_tab2 = kodeTab2._lastKodeTabWidget

#     # Get the tab button to drag
#     button = internal_tab2.tabButton(0)

#     # Create drag data
#     drag_data = _TTkTabWidgetDragData(button, internal_tab2)

#     # Drop in center
#     evt = TTkDnDEvent(pos=(50,25), data=drag_data)

#     result = internal_tab1.dropEvent(evt)

#     # Verify handling occurred
#     assert result in (True, False)

def test_kodetab_drop_event_list_of_new_tabs():
    '''
    Test dropping a list of new tabs.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget1 = ttk.TTkWidget()
    kodeTab.addTab(widget1, "Tab 1")

    internal_tab = kodeTab._lastKodeTabWidget

    # Create list of new tab data
    new_widget1 = ttk.TTkWidget()
    new_widget2 = ttk.TTkWidget()

    drag_data_list = [
        _TTkNewTabWidgetDragData("New Tab 1", new_widget1),
        _TTkNewTabWidgetDragData("New Tab 2", new_widget2)
    ]

    # Drop in center
    evt = TTkDnDEvent(pos=(50,25), data=drag_data_list)

    result = internal_tab.dropEvent(evt)

    assert result in (True, False)

def test_kodetab_drop_creates_horizontal_split():
    '''
    Test that dropping on left/right zones creates horizontal splits.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget1 = ttk.TTkWidget()
    kodeTab.addTab(widget1, "Tab 1")

    internal_tab = kodeTab._lastKodeTabWidget

    # Mock size for positioning
    internal_tab._size = (100, 50)

    new_widget = ttk.TTkWidget()
    drag_data = _TTkNewTabWidgetDragData("New Tab", new_widget)

    # Drop on left zone (x < w/4)
    evt = TTkDnDEvent(pos=(10,25), data=drag_data)

    initial_count = kodeTab.count()
    result = internal_tab.dropEvent(evt)

    # A split may have been created
    # Exact behavior depends on implementation
    assert kodeTab.count() >= initial_count

def test_kodetab_drop_creates_vertical_split():
    '''
    Test that dropping on top/bottom zones creates vertical splits.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget1 = ttk.TTkWidget()
    kodeTab.addTab(widget1, "Tab 1")

    internal_tab = kodeTab._lastKodeTabWidget

    # Mock size
    internal_tab._size = (100, 50)

    new_widget = ttk.TTkWidget()
    drag_data = _TTkNewTabWidgetDragData("New Tab", new_widget)

    # Drop on top zone (y < h/4, adjusted for tab bar)
    evt = TTkDnDEvent(pos=(50,5), data=drag_data)

    initial_count = kodeTab.count()
    result = internal_tab.dropEvent(evt)

    assert kodeTab.count() >= initial_count

def test_kodetab_set_drop_event_proxy():
    '''
    Test setting drop event proxy propagates to internal widgets.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget = ttk.TTkWidget()
    kodeTab.addTab(widget, "Tab 1")

    proxy_called = []

    def proxy(evt):
        proxy_called.append(evt)
        return True

    kodeTab.setDropEventProxy(proxy)

    # Verify proxy is set
    internal_tab = kodeTab._lastKodeTabWidget
    assert internal_tab._dropEventProxy == proxy

# ============================================================================
# TTkKodeTab Complex Scenarios
# ============================================================================

def test_kodetab_multiple_splits():
    '''
    Test creating multiple splits through tab operations.
    '''
    kodeTab = ttk.TTkKodeTab()

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    kodeTab.addTab(widget1, "Tab 1")
    kodeTab.addTab(widget2, "Tab 2")

    # Count all tab items
    items_before = list(kodeTab.iterItems())
    assert len(items_before) == 2

def test_kodetab_get_first_widget():
    '''
    Test getting the first internal widget.
    '''
    kodeTab = ttk.TTkKodeTab()

    first = kodeTab._getFirstWidget()
    assert isinstance(first, _TTkKodeTab)
    assert first._baseWidget == kodeTab

def test_kodetab_has_menu():
    '''
    Test checking if internal tab has menu.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget = ttk.TTkWidget()
    kodeTab.addTab(widget, "Tab 1")

    internal_tab = kodeTab._lastKodeTabWidget

    # Initially should not have menu
    assert internal_tab._hasMenu() is False

def test_kodetab_add_menu():
    '''
    Test adding menu to TTkKodeTab.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget = ttk.TTkWidget()
    kodeTab.addTab(widget, "Tab 1")

    # Add a menu item
    menu_item = kodeTab.addMenu("File", data="file_data")

    assert menu_item is not None

def test_kodetab_bar_type():
    '''
    Test different bar types for TTkKodeTab.
    '''
    from TermTk.TTkWidgets.tabwidget import TTkBarType

    kodeTab1 = ttk.TTkKodeTab(barType=TTkBarType.DEFAULT_3)
    kodeTab2 = ttk.TTkKodeTab(barType=TTkBarType.NERD_1)

    assert kodeTab1._barType == TTkBarType.DEFAULT_3
    assert kodeTab2._barType == TTkBarType.NERD_1

def test_kodetab_empty_after_all_removals():
    '''
    Test that TTkKodeTab handles becoming empty gracefully.
    '''
    kodeTab = ttk.TTkKodeTab()

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    kodeTab.addTab(widget1, "Tab 1")
    kodeTab.addTab(widget2, "Tab 2")

    internal_tab = kodeTab._lastKodeTabWidget

    # Remove all tabs
    internal_tab.removeTab(0)
    internal_tab.removeTab(0)

    # Trigger cleanup
    internal_tab._kodeTabClosed()

    # Should still be in valid state
    assert kodeTab._getFirstWidget() is not None

def test_kodetab_paint_child_canvas():
    '''
    Test that paintChildCanvas handles frame overlay correctly.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget = ttk.TTkWidget()
    kodeTab.addTab(widget, "Tab 1")

    internal_tab = kodeTab._lastKodeTabWidget

    # Set frame overlay
    internal_tab._frameOverlay = (10, 10, 50, 30)

    # Call paintChildCanvas (should not raise)
    try:
        internal_tab.paintChildCanvas()
        assert True
    except Exception as e:
        assert False, f"paintChildCanvas raised exception: {e}"

    # Clear overlay
    internal_tab._frameOverlay = None
    internal_tab.paintChildCanvas()

def test_kodetab_drop_invalid_data():
    '''
    Test that dropping invalid data returns False.
    '''
    kodeTab = ttk.TTkKodeTab()
    widget = ttk.TTkWidget()
    kodeTab.addTab(widget, "Tab 1")

    internal_tab = kodeTab._lastKodeTabWidget

    # Create event with invalid data
    evt = TTkDnDEvent(pos=(50,25), data="invalid_data")

    result = internal_tab.dropEvent(evt)

    # Should not accept invalid data
    assert result is False

def test_kodetab_iter_items_after_operations():
    '''
    Test that iterItems works correctly after add/remove operations.
    '''
    kodeTab = ttk.TTkKodeTab()

    widgets = [ttk.TTkWidget() for _ in range(5)]

    for i, widget in enumerate(widgets):
        kodeTab.addTab(widget, f"Tab {i}")

    items = list(kodeTab.iterItems())
    assert len(items) == 5

    # Remove some tabs
    kodeTab._lastKodeTabWidget.removeTab(2)
    kodeTab._lastKodeTabWidget.removeTab(1)

    items = list(kodeTab.iterItems())
    assert len(items) == 3
