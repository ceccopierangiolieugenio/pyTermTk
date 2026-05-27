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

import TermTk as ttk


def test_hboxlayout_add_widget_places_items_horizontally_by_default():
    layout = ttk.TTkHBoxLayout()
    first = ttk.TTkWidget()
    second = ttk.TTkWidget()

    layout.addWidget(first)
    layout.addWidget(second)

    assert layout.gridSize() == (1, 2)
    assert layout.itemAtPosition(0, 0).widget() is first
    assert layout.itemAtPosition(0, 1).widget() is second


def test_hboxlayout_add_widgets_keeps_order_on_single_row():
    layout = ttk.TTkHBoxLayout()
    widgets = [ttk.TTkWidget() for _ in range(3)]

    layout.addWidgets(widgets)

    rows, cols = layout.gridSize()
    assert rows >= 1
    assert cols >= 3
    assert [layout.itemAtPosition(0, col).widget() for col in range(3)] == widgets


def test_vboxlayout_add_widget_places_items_vertically():
    layout = ttk.TTkVBoxLayout()
    first = ttk.TTkWidget()
    second = ttk.TTkWidget()

    layout.addWidget(first)
    layout.addWidget(second)

    assert layout.gridSize() == (2, 1)
    assert layout.itemAtPosition(0, 0).widget() is first
    assert layout.itemAtPosition(1, 0).widget() is second


def test_vboxlayout_add_widgets_keeps_order_on_single_column():
    layout = ttk.TTkVBoxLayout()
    widgets = [ttk.TTkWidget() for _ in range(3)]

    layout.addWidgets(widgets)

    rows, cols = layout.gridSize()
    assert rows >= 3
    assert cols >= 1
    assert [layout.itemAtPosition(row, 0).widget() for row in range(3)] == widgets


def test_vboxlayout_add_item_and_add_items_use_vertical_direction():
    layout = ttk.TTkVBoxLayout()
    first = ttk.TTkWidget().widgetItem()
    second = ttk.TTkWidget().widgetItem()
    third = ttk.TTkWidget().widgetItem()

    layout.addItem(first)
    layout.addItems([second, third])

    rows, cols = layout.gridSize()
    assert rows >= 3
    assert cols >= 1
    assert layout.itemAtPosition(0, 0) is first
    assert layout.itemAtPosition(1, 0) is second
    assert layout.itemAtPosition(2, 0) is third


def test_box_layouts_update_assigns_geometry_in_expected_axis():
    hbox = ttk.TTkHBoxLayout()
    h_left = ttk.TTkWidget(minSize=(2, 3), maxSize=(2, 3))
    h_right = ttk.TTkWidget(minSize=(4, 3), maxSize=(4, 3))
    hbox.addWidget(h_left)
    hbox.addWidget(h_right)
    hbox.setGeometry(0, 0, 20, 10)
    hbox.update()

    assert h_left.geometry() == (0, 0, 2, 3)
    assert h_right.geometry() == (2, 0, 4, 3)

    vbox = ttk.TTkVBoxLayout()
    v_top = ttk.TTkWidget(minSize=(5, 2), maxSize=(5, 2))
    v_bottom = ttk.TTkWidget(minSize=(5, 4), maxSize=(5, 4))
    vbox.addWidget(v_top)
    vbox.addWidget(v_bottom)
    vbox.setGeometry(0, 0, 20, 20)
    vbox.update()

    assert v_top.geometry() == (0, 0, 5, 2)
    assert v_bottom.geometry() == (0, 2, 5, 4)
