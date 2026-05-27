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

import pytest
import TermTk as ttk


def test_layout_add_and_remove_widget_updates_count_and_parent_relationships():
    container = ttk.TTkContainer()
    layout = container.layout()
    widget = ttk.TTkWidget()

    layout.addWidget(widget)

    assert layout.count() == 1
    assert widget.parentWidget() is container

    layout.removeWidget(widget)

    assert layout.count() == 0
    assert widget.parentWidget() is None


def test_layout_replace_item_raises_when_index_is_invalid():
    layout = ttk.TTkLayout()

    with pytest.raises(ValueError):
        layout.replaceItem(ttk.TTkLayout(), 0)


def test_layout_replace_item_swaps_content_and_unparents_removed_widgets():
    layout = ttk.TTkLayout()
    container = ttk.TTkContainer(layout=layout)
    widget = ttk.TTkWidget()

    layout.addWidget(widget)
    assert widget.parentWidget() is container

    replacement = ttk.TTkLayout()
    layout.replaceItem(replacement, 0)

    assert layout.itemAt(0) is replacement
    assert widget.parentWidget() is None


def test_layout_iter_widgets_filters_visibility_and_supports_reverse_order():
    layout = ttk.TTkLayout()
    nested = ttk.TTkLayout()
    first = ttk.TTkWidget(name='first')
    hidden = ttk.TTkWidget(name='hidden', visible=False)
    nested_child = ttk.TTkWidget(name='nested')

    layout.addWidget(first)
    layout.addWidget(hidden)
    nested.addWidget(nested_child)
    layout.addItem(nested)

    assert list(layout.iterWidgets()) == [first, nested_child]
    assert list(layout.iterWidgets(onlyVisible=False, recurse=False)) == [first, hidden]
    assert list(layout.iterWidgets(reverse=True)) == [nested_child, first]


def test_layout_remove_widgets_removes_nested_targets_recursively():
    layout = ttk.TTkLayout()
    nested = ttk.TTkLayout()
    top_widget = ttk.TTkWidget()
    nested_widget = ttk.TTkWidget()

    nested.addWidget(nested_widget)
    layout.addWidget(top_widget)
    layout.addItem(nested)

    layout.removeWidgets([nested_widget])

    assert nested_widget.parentWidget() is None
    assert top_widget.parentWidget() is None
    assert list(nested.iterWidgets(onlyVisible=False)) == []


def test_layout_full_widget_area_geometry_tracks_all_children_bounds():
    layout = ttk.TTkLayout()
    widget_a = ttk.TTkWidget(pos=(2, 3), size=(4, 5))
    widget_b = ttk.TTkWidget(pos=(-1, 1), size=(2, 2))

    layout.addWidget(widget_a)
    layout.addWidget(widget_b)

    assert layout.fullWidgetAreaGeometry() == (-1, 1, 7, 7)


def test_layout_clear_unparents_widgets_from_direct_and_nested_items():
    layout = ttk.TTkLayout()
    nested = ttk.TTkLayout()
    direct_widget = ttk.TTkWidget()
    nested_widget = ttk.TTkWidget()

    layout.addWidget(direct_widget)
    nested.addWidget(nested_widget)
    layout.addItem(nested)

    container = ttk.TTkContainer(layout=layout)
    assert direct_widget.parentWidget() is container
    assert nested_widget.parentWidget() is container

    layout.clear()

    assert layout.count() == 0
    assert direct_widget.parentWidget() is None
    assert nested_widget.parentWidget() is None
