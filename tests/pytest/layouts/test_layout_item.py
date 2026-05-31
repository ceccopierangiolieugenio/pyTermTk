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


def test_layout_item_initialization_respects_pos_size_and_bounds_overrides():
    item = ttk.TTkLayoutItem(
        x=1,
        y=2,
        width=3,
        height=4,
        pos=(5, 6),
        size=(7, 8),
        maxWidth=9,
        maxHeight=10,
        maxSize=(11, 12),
        minWidth=1,
        minHeight=2,
        minSize=(3, 4),
        row=2,
        col=3,
        rowspan=2,
        colspan=3
    )

    assert item.pos() == (5, 6)
    assert item.size() == (7, 8)
    assert item.minimumSize() == (3, 4)
    assert item.maximumSize() == (11, 12)


def test_layout_item_span_value_splitting_for_first_and_following_cells():
    item = ttk.TTkLayoutItem(
        row=4,
        col=5,
        rowspan=3,
        colspan=2,
        minSize=(10, 7),
        maxSize=(11, 8)
    )

    assert item.minimumWidthSpan(5) == 5
    assert item.minimumWidthSpan(6) == 5

    assert item.minimumHeightSpan(4) == 3
    assert item.minimumHeightSpan(5) == 2

    assert item.maximumWidthSpan(5) == 6
    assert item.maximumWidthSpan(6) == 5

    assert item.maximumHeightSpan(4) == 4
    assert item.maximumHeightSpan(6) == 2


def test_layout_item_setters_update_geometry_parent_and_layer_values():
    item = ttk.TTkLayoutItem(z=7)

    item.setOffset(9, 4)
    item.setGeometry(1, 2, 3, 4)
    parent = ttk.TTkLayoutItem()
    item.setParent(parent)

    assert item.offset() == (9, 4)
    assert item.geometry() == (1, 2, 3, 4)
    assert item.parent() is parent

    item.setLayer(ttk.TTkLayoutItem.LAYER2)

    expected_z = (7 & ttk.TTkLayoutItem.LAYERMASK) | ttk.TTkLayoutItem.LAYER2
    assert item.layer() == ttk.TTkLayoutItem.LAYER2
    assert item._z == expected_z
