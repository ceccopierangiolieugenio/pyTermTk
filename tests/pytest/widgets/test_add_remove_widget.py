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


def test_add_widget_to_container():
    '''
    Test that adding widgets to a container using addWidget() correctly sets the parent relationship.
    Verifies that widgets initially have no parent, and after being added to a container,
    their parentWidget() returns the container.
    '''
    container = ttk.TTkContainer()
    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    assert widget1.parentWidget() is None
    assert widget2.parentWidget() is None

    container.addWidget(widget1)
    assert widget1.parentWidget() is container

    container.addWidget(widget2)
    assert widget2.parentWidget() is container

def test_add_widget_to_container_02():
    '''
    Test that widgets added via parent= constructor parameter correctly establish
    the parent-child relationship immediately upon construction.
    '''
    container = ttk.TTkContainer()
    widget1 = ttk.TTkWidget(parent=container)
    widget2 = ttk.TTkWidget(parent=container)

    assert widget1.parentWidget() is container
    assert widget2.parentWidget() is container

def test_remove_widget_from_container():
    '''
    Test that removing a widget from a container using removeWidget() correctly
    unsets the parent relationship, returning the widget to an orphaned state.
    '''
    container = ttk.TTkContainer()
    widget = ttk.TTkWidget()

    container.addWidget(widget)
    assert widget.parentWidget() is container

    container.removeWidget(widget)
    assert widget.parentWidget() is None

def test_remove_widget_from_container_02():
    '''
    Test that removing a widget that was added via parent= constructor parameter
    correctly unsets the parent relationship.
    '''
    container = ttk.TTkContainer()
    widget = ttk.TTkWidget(parent=container)

    assert widget.parentWidget() is container
    container.removeWidget(widget)
    assert widget.parentWidget() is None

def test_gridlayout_add_remove():
    '''
    Test :py:class:`TTkGridLayout` add/remove operations using container.layout().addWidget().
    Verifies that widgets added to specific grid positions have their parent correctly set
    to the container, and that removing widgets unsets the parent relationship while
    preserving other widgets' parents.
    '''
    container = ttk.TTkContainer()
    layout = ttk.TTkGridLayout()
    container.setLayout(layout)

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()
    widget3 = ttk.TTkWidget()

    # Add widgets to grid using container.layout()
    container.layout().addWidget(widget1, 0, 0)
    container.layout().addWidget(widget2, 0, 1)
    container.layout().addWidget(widget3, 1, 0)

    assert widget1.parentWidget() is container
    assert widget2.parentWidget() is container
    assert widget3.parentWidget() is container

    # Remove widget using container.layout()
    container.layout().removeWidget(widget2)
    assert widget2.parentWidget() is None
    assert widget1.parentWidget() is container
    assert widget3.parentWidget() is container


def test_hboxlayout_add_remove():
    '''
    Test :py:class:`TTkHBoxLayout` add/remove operations using container.layout().addWidget().
    Verifies that widgets are correctly parented when added sequentially, and that
    removing specific widgets from the middle of the layout updates their parent
    relationships while preserving others.
    '''
    container = ttk.TTkContainer()
    layout = ttk.TTkHBoxLayout()
    container.setLayout(layout)

    widgets = [ttk.TTkWidget() for _ in range(4)]

    # Add all widgets using container.layout()
    for widget in widgets:
        container.layout().addWidget(widget)
        assert widget.parentWidget() is container

    # Remove middle widgets using container.layout()
    container.layout().removeWidget(widgets[1])
    container.layout().removeWidget(widgets[2])

    assert widgets[0].parentWidget() is container
    assert widgets[1].parentWidget() is None
    assert widgets[2].parentWidget() is None
    assert widgets[3].parentWidget() is container


def test_vboxlayout_add_remove():
    '''
    Test :py:class:`TTkVBoxLayout` add/remove operations using container.layout().addWidget().
    Verifies parent relationships when adding button widgets vertically, and that
    removing the first widget correctly unsets its parent while preserving others.
    '''
    container = ttk.TTkContainer()
    layout = ttk.TTkVBoxLayout()
    container.setLayout(layout)

    widget1 = ttk.TTkButton(text='Button 1')
    widget2 = ttk.TTkButton(text='Button 2')
    widget3 = ttk.TTkButton(text='Button 3')

    container.layout().addWidget(widget1)
    container.layout().addWidget(widget2)
    container.layout().addWidget(widget3)

    assert widget1.parentWidget() is container
    assert widget2.parentWidget() is container
    assert widget3.parentWidget() is container

    # Remove first widget using container.layout()
    container.layout().removeWidget(widget1)
    assert widget1.parentWidget() is None
    assert widget2.parentWidget() is container


def test_nested_layouts():
    '''
    Test parent relationships with nested layouts using container.layout().addWidget().
    Verifies that when a container with its own layout is added to another container,
    the parent relationships form a proper hierarchy. Widgets remain parented to their
    immediate container even when that container is removed from the root.
    '''
    root = ttk.TTkContainer()
    root_layout = ttk.TTkVBoxLayout()
    root.setLayout(root_layout)

    # Create nested container
    nested = ttk.TTkContainer()
    nested_layout = ttk.TTkHBoxLayout()
    nested.setLayout(nested_layout)

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    # Add nested container to root using root.layout()
    root.layout().addWidget(nested)
    assert nested.parentWidget() is root

    # Add widgets to nested layout using nested.layout()
    nested.layout().addWidget(widget1)
    nested.layout().addWidget(widget2)

    assert widget1.parentWidget() is nested
    assert widget2.parentWidget() is nested

    # Remove nested container using root.layout()
    root.layout().removeWidget(nested)
    assert nested.parentWidget() is None
    assert widget1.parentWidget() is nested  # Still parented to nested


def test_replace_widget_in_layout():
    '''
    Test that replacing a widget in the same layout position correctly maintains
    parent relationships using container.layout() operations. The removed widget
    should have no parent, while the replacement widget should be parented to the container.
    '''
    container = ttk.TTkContainer()
    layout = ttk.TTkGridLayout()
    container.setLayout(layout)

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    container.layout().addWidget(widget1, 0, 0)
    assert widget1.parentWidget() is container

    # Replace widget1 with widget2 using container.layout()
    container.layout().removeWidget(widget1)
    container.layout().addWidget(widget2, 0, 0)

    assert widget1.parentWidget() is None
    assert widget2.parentWidget() is container


def test_move_widget_between_containers():
    '''
    Test that moving a widget between containers correctly updates the parent relationship.
    The widget should first be parented to the first container, then have no parent briefly,
    then be parented to the second container.
    '''
    container1 = ttk.TTkContainer()
    container2 = ttk.TTkContainer()
    widget = ttk.TTkWidget()

    container1.addWidget(widget)
    assert widget.parentWidget() is container1

    # Move to second container
    container1.removeWidget(widget)
    container2.addWidget(widget)

    assert widget.parentWidget() is container2


def test_complex_layout_operations():
    '''
    Test complex add/remove operations across multiple layout types using container.layout().addWidget().
    Creates a hierarchy with :py:class:`TTkVBoxLayout`, :py:class:`TTkHBoxLayout`, and :py:class:`TTkGridLayout`.
    Verifies that all parent relationships are correctly maintained throughout the hierarchy,
    and that removing a section of the layout tree properly updates parent relationships.
    '''
    root = ttk.TTkContainer()
    vbox = ttk.TTkVBoxLayout()
    root.setLayout(vbox)

    # Create horizontal section
    hbox_container = ttk.TTkContainer()
    hbox = ttk.TTkHBoxLayout()
    hbox_container.setLayout(hbox)

    # Create grid section
    grid_container = ttk.TTkContainer()
    grid = ttk.TTkGridLayout()
    grid_container.setLayout(grid)

    widgets = [ttk.TTkButton(text=f'Btn{i}') for i in range(6)]

    # Add to vbox using root.layout()
    root.layout().addWidget(hbox_container)
    root.layout().addWidget(grid_container)

    # Add to hbox using hbox_container.layout()
    hbox_container.layout().addWidget(widgets[0])
    hbox_container.layout().addWidget(widgets[1])

    # Add to grid using grid_container.layout()
    grid_container.layout().addWidget(widgets[2], 0, 0)
    grid_container.layout().addWidget(widgets[3], 0, 1)
    grid_container.layout().addWidget(widgets[4], 1, 0)
    grid_container.layout().addWidget(widgets[5], 1, 1)

    # Verify all parents
    assert hbox_container.parentWidget() is root
    assert grid_container.parentWidget() is root
    assert widgets[0].parentWidget() is hbox_container
    assert widgets[1].parentWidget() is hbox_container
    assert widgets[2].parentWidget() is grid_container
    assert widgets[3].parentWidget() is grid_container

    # Remove grid section using root.layout()
    root.layout().removeWidget(grid_container)
    assert grid_container.parentWidget() is None
    assert widgets[2].parentWidget() is grid_container  # Still parented to grid_container

    # Remove widgets from hbox using hbox_container.layout()
    hbox_container.layout().removeWidget(widgets[0])
    assert widgets[0].parentWidget() is None
    assert widgets[1].parentWidget() is hbox_container

def test_nested_layout_widgets_01():
    '''
    Test that widgets added to a nested layout (one layout containing another) correctly
    inherit the parent from the container that owns the root layout. Widgets added to
    the nested layout should be parented to the container, not to the layout itself.
    '''
    layout1 = ttk.TTkLayout()
    layout2 = ttk.TTkLayout()

    layout1.addItem(layout2)

    container = ttk.TTkContainer(layout=layout1)

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    assert widget1.parentWidget() is None
    assert widget2.parentWidget() is None

    layout2.addWidget(widget1)
    assert widget1.parentWidget() is container

    layout2.addWidget(widget2)
    assert widget2.parentWidget() is container

def test_nested_layout_widgets_02():
    '''
    Test that widgets added to a nested layout before the layout is attached to a container
    get their parent set correctly when setLayout() is called. Also verifies that removing
    the nested layout from the parent layout unsets the widgets' parents.
    '''
    layout1 = ttk.TTkLayout()
    layout2 = ttk.TTkLayout()

    layout1.addItem(layout2)

    container = ttk.TTkContainer()

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    layout2.addWidget(widget1)
    layout2.addWidget(widget2)

    assert widget1.parentWidget() is None
    assert widget2.parentWidget() is None

    container.setLayout(layout1)

    assert widget1.parentWidget() is container
    assert widget2.parentWidget() is container

    layout1.removeItem(layout2)

    assert widget1.parentWidget() is None
    assert widget2.parentWidget() is None

def test_nested_layout_widgets_03():
    '''
    Test that replacing a container's layout with a different layout correctly unsets
    the parent relationships for widgets in the old layout's hierarchy. Widgets in
    nested layouts should have their parents cleared when the root layout is replaced.
    '''
    layout1 = ttk.TTkLayout()
    layout2 = ttk.TTkLayout()
    layout3 = ttk.TTkLayout()

    layout1.addItem(layout2)

    container = ttk.TTkContainer()

    widget1 = ttk.TTkWidget()
    widget2 = ttk.TTkWidget()

    layout2.addWidget(widget1)
    layout2.addWidget(widget2)

    assert widget1.parentWidget() is None
    assert widget2.parentWidget() is None

    container.setLayout(layout1)

    assert widget1.parentWidget() is container
    assert widget2.parentWidget() is container

    container.setLayout(layout3)

    assert widget1.parentWidget() is None
    assert widget2.parentWidget() is None

def test_nested_layout_widgets_04():
    '''
    Test complex parent relationships where a container with its own child widgets
    is added to a nested layout within another container. Verifies that the container
    maintains its parent relationship to its widgets, while also being correctly parented
    to the outer container. Removing the nested layout should only affect the intermediate
    container's parent, not the leaf widgets' relationship to their immediate parent.
    '''
    layout1 = ttk.TTkLayout()
    layout2 = ttk.TTkLayout()

    layout1.addItem(layout2)

    container1 = ttk.TTkContainer(layout=layout1)
    container2 = ttk.TTkContainer()

    widget1 = ttk.TTkWidget(parent=container2)
    widget2 = ttk.TTkWidget(parent=container2)

    assert container2.parentWidget() is None
    assert widget1.parentWidget() is container2
    assert widget2.parentWidget() is container2

    layout2.addWidget(container2)
    assert container2.parentWidget() is container1
    assert widget1.parentWidget() is container2
    assert widget2.parentWidget() is container2

    layout1.removeItem(layout2)
    assert container2.parentWidget() is None
    assert widget1.parentWidget() is container2
    assert widget2.parentWidget() is container2

