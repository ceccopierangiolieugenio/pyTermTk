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


def test_focus_01_tab():
    '''
        Container ─┬─▶ Widget1
                   ├─▶ Widget2
                   └─▶ Widget3
    '''
    root = ttk.TTk()
    widget1 = ttk.TTkWidget(parent=root)
    widget2 = ttk.TTkWidget(parent=root)
    widget3 = ttk.TTkWidget(parent=root)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    widget2.setFocus()

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.NoModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert True is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is root.hasFocus()
    assert True  is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

def test_focus_01_tab_reverse():
    '''
        Container ─┬─▶ Widget1
                   ├─▶ Widget2
                   └─▶ Widget3
    '''
    root = ttk.TTk()
    widget1 = ttk.TTkWidget(parent=root)
    widget2 = ttk.TTkWidget(parent=root)
    widget3 = ttk.TTkWidget(parent=root)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    widget2.setFocus()

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.ShiftModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is root.hasFocus()
    assert True  is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert True  is widget3.hasFocus()

def test_focus_04_nested_containers():
    '''
        Root ─▶ Container1 ─┬─▶ Widget1
                            └─▶ Container2 ─┬─▶ Widget2
                                            └─▶ Widget3
    '''
    root = ttk.TTk()
    container1 = ttk.TTkContainer(parent=root)
    widget1 = ttk.TTkWidget(parent=container1)
    container2 = ttk.TTkContainer(parent=container1)
    widget2 = ttk.TTkWidget(parent=container2)
    widget3 = ttk.TTkWidget(parent=container2)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    widget2.setFocus()

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.NoModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert True  is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is root.hasFocus()
    assert True  is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

def test_focus_04_nested_containers_reversed():
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

    widget3.setFocus()

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert True  is widget3.hasFocus()
    assert False is widget4.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.ShiftModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is root.hasFocus()
    assert True is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert True is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert True is widget3.hasFocus()
    assert False is widget4.hasFocus()