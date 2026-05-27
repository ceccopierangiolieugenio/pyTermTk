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


def test_gridlayout_auto_placement_horizontal_and_vertical():
    horizontal = ttk.TTkGridLayout()
    w1 = ttk.TTkWidget()
    w2 = ttk.TTkWidget()

    horizontal.addWidget(w1)
    horizontal.addWidget(w2)

    assert horizontal.gridSize() == (1, 2)
    assert horizontal.itemAtPosition(0, 0).widget() is w1
    assert horizontal.itemAtPosition(0, 1).widget() is w2

    vertical = ttk.TTkGridLayout()
    v1 = ttk.TTkWidget()
    v2 = ttk.TTkWidget()

    vertical.addWidget(v1, direction=ttk.TTkK.VERTICAL)
    vertical.addWidget(v2, direction=ttk.TTkK.VERTICAL)

    assert vertical.gridSize() == (2, 1)
    assert vertical.itemAtPosition(0, 0).widget() is v1
    assert vertical.itemAtPosition(1, 0).widget() is v2


def test_gridlayout_item_at_position_resolves_rowspan_and_colspan():
    grid = ttk.TTkGridLayout()
    widget = ttk.TTkWidget()

    grid.addWidget(widget, row=1, col=2, rowspan=2, colspan=3)

    item = grid.itemAtPosition(1, 2)
    assert item is not None
    assert item.widget() is widget

    # Covered by row/col span
    assert grid.itemAtPosition(1, 4) is item
    assert grid.itemAtPosition(2, 3) is item

    # Outside the widget area
    assert grid.itemAtPosition(0, 0) is None
    assert grid.itemAtPosition(3, 5) is None


def test_gridlayout_insert_row_and_column_shift_existing_items():
    grid = ttk.TTkGridLayout()
    first = ttk.TTkWidget()
    second = ttk.TTkWidget()

    grid.addWidget(first, row=0, col=0)
    grid.addWidget(second, row=1, col=1)

    grid.insertRow(0)
    grid.insertColumn(1)

    assert grid.itemAtPosition(1, 0).widget() is first
    assert grid.itemAtPosition(2, 2).widget() is second


def test_gridlayout_repack_compacts_sparse_grid_and_realigns_indices():
    grid = ttk.TTkGridLayout()
    widget = ttk.TTkWidget()

    grid.addWidget(widget, row=2, col=3)
    assert grid.gridSize() == (3, 4)

    grid.repack()

    assert grid.gridSize() == (1, 1)
    assert grid.itemAtPosition(0, 0).widget() is widget


def test_gridlayout_empty_lines_use_row_and_column_minimum_fallbacks():
    grid = ttk.TTkGridLayout(columnMinWidth=4, rowMinHeight=3)

    grid.addWidget(ttk.TTkWidget(), row=0, col=0)
    grid.addWidget(ttk.TTkWidget(), row=0, col=2)
    grid.addWidget(ttk.TTkWidget(), row=2, col=0)

    # Col 1 and row 1 are empty but inside the used grid bounds
    assert grid.minimumColWidth(1) == 4
    assert grid.maximumColWidth(1) == 4
    assert grid.minimumRowHeight(1) == 3
    assert grid.maximumRowHeight(1) == 3


def test_gridlayout_hidden_widget_does_not_drive_column_minimum_width():
    grid = ttk.TTkGridLayout(columnMinWidth=2)

    hidden = ttk.TTkWidget(minSize=(9, 1), visible=False)
    visible = ttk.TTkWidget(minSize=(3, 1))

    grid.addWidget(hidden, row=0, col=0)
    grid.addWidget(visible, row=0, col=1)

    assert grid.minimumColWidth(0) == 2
    assert grid.minimumColWidth(1) == 3


def test_gridlayout_update_sets_child_geometries_and_exposes_computed_sizes():
    grid = ttk.TTkGridLayout()
    left = ttk.TTkWidget(minSize=(3, 2), maxSize=(3, 2))
    right = ttk.TTkWidget(minSize=(5, 2), maxSize=(5, 2))

    grid.addWidget(left, row=0, col=0)
    grid.addWidget(right, row=0, col=1)

    grid.setGeometry(0, 0, 20, 5)
    grid.update()

    assert left.geometry() == (0, 0, 3, 2)
    assert right.geometry() == (3, 0, 5, 2)

    hor_sizes, ver_sizes = grid.getSizes()
    assert hor_sizes == [[0, 3], [3, 5]]
    assert ver_sizes == [[0, 2]]
