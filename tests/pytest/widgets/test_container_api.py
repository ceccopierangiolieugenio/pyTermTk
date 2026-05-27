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


def test_container_padding_initialization_variants():
    container_tuple = ttk.TTkContainer(padding=ttk.TTkPadding(1, 2, 3, 4))
    container_args = ttk.TTkContainer(
        paddingTop=5,
        paddingBottom=6,
        paddingLeft=7,
        paddingRight=8,
    )

    assert container_tuple.getPadding() == ttk.TTkPadding(1, 2, 3, 4)
    assert container_args.getPadding() == ttk.TTkPadding(5, 6, 7, 8)


def test_container_update_applies_root_and_main_layout_geometry_from_padding():
    container = ttk.TTkContainer(size=(20, 10), padding=ttk.TTkPadding(1, 2, 3, 4))

    container.update(updateLayout=True)

    assert container.rootLayout().geometry() == (0, 0, 20, 10)
    assert container.layout().geometry() == (3, 1, 13, 7)

    container.setPadding(2, 1, 1, 2)
    container.update(updateLayout=True)

    assert container.layout().geometry() == (1, 2, 17, 7)


def test_set_layout_replaces_layout_and_unparents_old_layout_widgets():
    first_layout = ttk.TTkLayout()
    child = ttk.TTkWidget()
    first_layout.addWidget(child)

    container = ttk.TTkContainer(layout=first_layout)
    assert container.layout() is first_layout
    assert child.parentWidget() is container

    second_layout = ttk.TTkLayout()
    container.setLayout(second_layout)

    assert container.layout() is second_layout
    assert child.parentWidget() is None


def test_get_widget_by_name_is_recursive_and_includes_hidden_children():
    root = ttk.TTkContainer(name='root')
    inner = ttk.TTkContainer(name='inner', parent=root)
    leaf = ttk.TTkWidget(name='leaf', parent=inner, visible=False)

    assert root.getWidgetByName('root') is root
    assert root.getWidgetByName('inner') is inner
    assert root.getWidgetByName('leaf') is leaf
    assert root.getWidgetByName('missing') is None


def test_deprecated_container_add_remove_widget_still_delegate_to_layout():
    container = ttk.TTkContainer()
    widget = ttk.TTkWidget()

    container.addWidget(widget)
    assert widget.parentWidget() is container

    container.removeWidget(widget)
    assert widget.parentWidget() is None


def test_container_min_max_dimensions_include_layout_constraints_and_padding():
    layout = ttk.TTkLayout(minWidth=5, minHeight=6, maxWidth=8, maxHeight=9)
    container = ttk.TTkContainer(
        layout=layout,
        padding=ttk.TTkPadding(1, 2, 3, 4),
        minWidth=0,
        minHeight=0,
        maxWidth=100,
        maxHeight=100,
    )

    assert container.minimumWidth() == 12
    assert container.minimumHeight() == 9
    assert container.maximumWidth() == 15
    assert container.maximumHeight() == 12
