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


def test_next_prev_widget_01():
    '''
        Container ─┬─▶ Widget1
                   ├─▶ Widget2
                   └─▶ Widget3
    '''
    container = ttk.TTkContainer()
    widget1 = ttk.TTkWidget(parent=container)
    widget2 = ttk.TTkWidget(parent=container)
    widget3 = ttk.TTkWidget(parent=container)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    # Forward
    ff = container._getFirstFocus(widget=None, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget1
    ff = container._getFirstFocus(widget=widget1, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget2
    ff = container._getFirstFocus(widget=widget2, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget3
    ff = container._getFirstFocus(widget=widget3, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is None

    # Reverse
    ff = container._getLastFocus(widget=None, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget3
    ff = container._getLastFocus(widget=widget3, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget2
    ff = container._getLastFocus(widget=widget2, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget1
    ff = container._getLastFocus(widget=widget1, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is None

def test_next_prev_widget_02_nested():
    '''
        Root ─▶ Container1 ─┬─▶ Widget1
                            └─▶ Container2 ─┬─▶ Widget2
                                            ├─▶ Widget3
                                            └─▶ Widget4
    '''
    root = ttk.TTk()
    container1 = ttk.TTkContainer(parent=root)
    widget1 = ttk.TTkWidget(parent=container1)
    container2 = ttk.TTkContainer(parent=container1)
    widget2 = ttk.TTkWidget(parent=container2)
    widget3 = ttk.TTkWidget(parent=container2)
    widget4 = ttk.TTkWidget(parent=container2)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget4.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    # Forward
    ff = container1._getFirstFocus(widget=None, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget1
    ff = container2._getFirstFocus(widget=None, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget2

    ff = container1._getFirstFocus(widget=widget1, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget2

    ff = container2._getFirstFocus(widget=widget2, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget3
    ff = container2._getFirstFocus(widget=widget3, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget4
    ff = container2._getFirstFocus(widget=widget4, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is None

    # Reverse
    ff = container1._getLastFocus(widget=None, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget4
    ff = container2._getLastFocus(widget=None, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget4

    ff = container1._getLastFocus(widget=widget1, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is None

    ff = container2._getLastFocus(widget=widget4, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget3
    ff = container2._getLastFocus(widget=widget3, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is widget2
    ff = container2._getLastFocus(widget=widget2, focusPolicy=ttk.TTkK.FocusPolicy.TabFocus)
    assert ff is None

