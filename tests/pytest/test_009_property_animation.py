#!/usr/bin/env python3
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

import sys, os

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

import TermTk as ttk

def test_cast_bound_method_postponed_annotations():
    # TTkWidget.move(x:int, y:int) lives in a module using
    # "from __future__ import annotations", so its annotations are strings.
    widget = ttk.TTkWidget()
    anim = ttk.TTkPropertyAnimation(None, widget.move)
    assert anim._cast(1.6, 2.4) == [1, 2]

def test_cast_property_name_postponed_annotations():
    widget = ttk.TTkWidget()
    anim = ttk.TTkPropertyAnimation(widget, 'move')
    assert anim._cast(1.6, 2.4) == [1, 2]

def test_cast_lambda_is_not_casted():
    anim = ttk.TTkPropertyAnimation(None, lambda x: x)
    assert anim._cast(3.7) == [3.7]
