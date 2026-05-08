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


def test_set_maximum_width_clamps_current_width_and_aligns_minimum_width():
    widget = ttk.TTkWidget(size=(10, 4), minSize=(8, 1), maxSize=(20, 20))

    widget.setMaximumWidth(6)

    assert widget.minimumWidth() == 6
    assert widget.maximumWidth() == 6
    assert widget.size() == (6, 4)


def test_set_maximum_height_clamps_current_height_and_aligns_minimum_height():
    widget = ttk.TTkWidget(size=(5, 9), minSize=(1, 7), maxSize=(20, 20))

    widget.setMaximumHeight(6)

    assert widget.minimumHeight() == 6
    assert widget.maximumHeight() == 6
    assert widget.size() == (5, 6)


def test_set_minimum_width_clamps_current_width_and_aligns_maximum_width():
    widget = ttk.TTkWidget(size=(4, 3), minSize=(0, 0), maxSize=(3, 20))

    widget.setMinimumWidth(6)

    assert widget.minimumWidth() == 6
    assert widget.maximumWidth() == 6
    assert widget.size() == (6, 3)


def test_set_minimum_height_clamps_current_height_and_aligns_maximum_height():
    widget = ttk.TTkWidget(size=(3, 4), minSize=(0, 0), maxSize=(20, 3))

    widget.setMinimumHeight(6)

    assert widget.minimumHeight() == 6
    assert widget.maximumHeight() == 6
    assert widget.size() == (3, 6)


def test_bound_updates_do_not_resize_when_current_size_is_already_valid():
    widget = ttk.TTkWidget(size=(7, 5), minSize=(2, 2), maxSize=(10, 10))

    widget.setMaximumWidth(8)
    widget.setMaximumHeight(6)
    widget.setMinimumWidth(3)
    widget.setMinimumHeight(4)

    assert widget.size() == (7, 5)
    assert widget.minimumSize() == (3, 4)
    assert widget.maximumSize() == (8, 6)


def test_reapplying_the_same_bound_is_a_no_op():
    widget = ttk.TTkWidget(size=(7, 5), minSize=(3, 4), maxSize=(8, 6))

    widget.setMaximumWidth(8)
    widget.setMaximumHeight(6)
    widget.setMinimumWidth(3)
    widget.setMinimumHeight(4)

    assert widget.size() == (7, 5)
    assert widget.minimumSize() == (3, 4)
    assert widget.maximumSize() == (8, 6)