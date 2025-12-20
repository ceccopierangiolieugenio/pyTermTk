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
from typing import List

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

def test_focus_container_with_tab_focus():
    '''
        Container (TabFocus) ─┬─▶ Widget1
                              ├─▶ Widget2
                              └─▶ Widget3
    '''
    root = ttk.TTk()
    container = ttk.TTkContainer(parent=root)
    container.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget1 = ttk.TTkWidget(parent=container)
    widget2 = ttk.TTkWidget(parent=container)
    widget3 = ttk.TTkWidget(parent=container)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    container.setFocus()

    assert True  is container.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.NoModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is container.hasFocus()
    assert True  is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is container.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is container.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert True  is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert True  is container.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

def test_focus_nested_containers_with_tab_focus():
    '''
        Root ─▶ Container1 (TabFocus) ─┬─▶ Widget1
                                       └─▶ Container2 (TabFocus) ─┬─▶ Widget2
                                                                  └─▶ Widget3
    '''
    root = ttk.TTk()
    container1 = ttk.TTkContainer(parent=root)
    container1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget1 = ttk.TTkWidget(parent=container1)
    container2 = ttk.TTkContainer(parent=container1)
    container2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2 = ttk.TTkWidget(parent=container2)
    widget3 = ttk.TTkWidget(parent=container2)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    container1.setFocus()

    assert True  is container1.hasFocus()
    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.NoModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is container1.hasFocus()
    assert True  is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is container1.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is container1.hasFocus()
    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is container1.hasFocus()
    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert True  is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert True  is container1.hasFocus()
    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

def test_focus_nested_containers_with_tab_focus_reversed():
    '''
        Root ─▶ Container1 (TabFocus) ─┬─▶ Widget1
                                       └─▶ Container2 (TabFocus) ─┬─▶ Widget2
                                                                  └─▶ Widget3
    '''
    root = ttk.TTk()
    container1 = ttk.TTkContainer(name='container1', parent=root)
    widget1 = ttk.TTkWidget(name='widget1', parent=container1)
    container2 = ttk.TTkContainer(name='container2', parent=container1)
    widget2 = ttk.TTkWidget(name='widget2', parent=container2)
    widget3 = ttk.TTkWidget(name='widget3', parent=container2)
    container1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    container2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    widget2.setFocus()

    assert False is container1.hasFocus()
    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.ShiftModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is container1.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is container1.hasFocus()
    assert True  is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert True  is container1.hasFocus()
    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is container1.hasFocus()
    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert True  is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is container1.hasFocus()
    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

def test_focus_mixed_containers_tab_focus():
    '''
        Root ─▶ Container1 (No TabFocus) ─┬─▶ Widget1
                                          ├─▶ Container2 (TabFocus) ─┬─▶ Widget2
                                          │                          └─▶ Widget3
                                          └─▶ Widget4
    '''
    root = ttk.TTk()
    container1 = ttk.TTkContainer(parent=root)
    widget1 = ttk.TTkWidget(parent=container1)
    container2 = ttk.TTkContainer(parent=container1)
    container2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2 = ttk.TTkWidget(parent=container2)
    widget3 = ttk.TTkWidget(parent=container2)
    widget4 = ttk.TTkWidget(parent=container1)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget4.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    widget1.setFocus()

    assert True  is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.NoModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is widget1.hasFocus()
    assert True  is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert True  is widget3.hasFocus()
    assert False is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert True  is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert True  is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

def test_focus_mixed_containers_tab_focus_disabled_2():
    '''
        Root ─▶ Container1 (No TabFocus) ─┬─▶ Widget1
                                          ├─▶ Container2 (TabFocus) ─┬─▶ Widget2
                                          │                          └─▶ Widget3
                                          └─▶ Widget4
    '''
    root = ttk.TTk()
    container1 = ttk.TTkContainer(parent=root)
    widget1 = ttk.TTkWidget(parent=container1)
    container2 = ttk.TTkContainer(parent=container1)
    container2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2 = ttk.TTkWidget(parent=container2)
    widget3 = ttk.TTkWidget(parent=container2)
    widget4 = ttk.TTkWidget(parent=container1)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget4.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    widget3.setDisabled()

    widget1.setFocus()

    assert True  is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.NoModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is widget1.hasFocus()
    assert True  is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False  is widget3.hasFocus()
    assert True is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert True  is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

def test_focus_mixed_containers_tab_focus_disabled_1():
    '''
        Root ─▶ Container1 (No TabFocus) ─┬─▶ Widget1
                                          ├─▶ Container2 (TabFocus) ─┬─▶ Widget2
                                          │                          └─▶ Widget3
                                          └─▶ Widget4
    '''
    root = ttk.TTk()
    container1 = ttk.TTkContainer(parent=root)
    widget1 = ttk.TTkWidget(parent=container1)
    container2 = ttk.TTkContainer(parent=container1)
    container2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2 = ttk.TTkWidget(parent=container2)
    widget3 = ttk.TTkWidget(parent=container2)
    widget4 = ttk.TTkWidget(parent=container1)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget4.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    container2.setDisabled()

    widget1.setFocus()

    assert True  is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.NoModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is widget1.hasFocus()
    assert False  is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert True is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert True is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False  is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

def test_focus_mixed_containers_tab_focus_disabled_1_rev():
    '''
        Root ─▶ Container1 (No TabFocus) ─┬─▶ Widget1
                                          ├─▶ Container2 (TabFocus) ─┬─▶ Widget2
                                          │                          └─▶ Widget3
                                          └─▶ Widget4
    '''
    root = ttk.TTk()
    container1 = ttk.TTkContainer(parent=root)
    widget1 = ttk.TTkWidget(parent=container1)
    container2 = ttk.TTkContainer(parent=container1)
    container2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2 = ttk.TTkWidget(parent=container2)
    widget3 = ttk.TTkWidget(parent=container2)
    widget4 = ttk.TTkWidget(parent=container1)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget4.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    container2.setDisabled()

    widget1.setFocus()

    assert True  is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.ShiftModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is widget1.hasFocus()
    assert False  is container2.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert True is widget4.hasFocus()

    root.keyEvent(evt=tab_key)

    assert True is widget1.hasFocus()
    assert False is container2.hasFocus()
    assert False  is widget2.hasFocus()
    assert False is widget3.hasFocus()
    assert False is widget4.hasFocus()

def test_focus_container_tab_focus_reversed():
    '''
        Container (TabFocus) ─┬─▶ Widget1
                              ├─▶ Widget2
                              └─▶ Widget3
    '''
    root = ttk.TTk()
    container = ttk.TTkContainer(parent=root)
    container.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget1 = ttk.TTkWidget(parent=container)
    widget2 = ttk.TTkWidget(parent=container)
    widget3 = ttk.TTkWidget(parent=container)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    widget2.setFocus()

    assert False is container.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.ShiftModifier,
        code='',)

    root.keyEvent(evt=tab_key)

    assert False is container.hasFocus()
    assert True  is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert True  is container.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is container.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert True  is widget3.hasFocus()

    root.keyEvent(evt=tab_key)

    assert False is container.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

def _check_focus_order(root:ttk.TTk, widgets:List[ttk.TTkWidget], all_widgets:List[ttk.TTkWidget], evt:ttk.TTkKeyEvent):
    for wid in widgets:
        root.keyEvent(evt=evt)
        print(f"Send {evt}")
        for test_wid in all_widgets:
            assert_condition = wid is test_wid
            print(f"{assert_condition} == {test_wid.hasFocus()} - {test_wid.name()}")
        for test_wid in all_widgets:
            assert_condition = wid is test_wid
            assert assert_condition is test_wid.hasFocus(), f"{assert_condition} != {test_wid.hasFocus()} - {test_wid.name()}"


def test_focus_mixed_containers_tab_focus_disabled_3():
    '''
        Root ─▶ Container1 (No TabFocus) ─┬─▶ Widget1
                                          ├─▶ Container2 (TabFocus) ─┬─▶ Widget2
                                          │                          └─▶ Widget3
                                          └─▶ Widget4
    '''
    root = ttk.TTk()
    container1 = ttk.TTkContainer(parent=root)
    widget1 = ttk.TTkWidget(parent=container1)
    container2 = ttk.TTkContainer(parent=container1)
    container2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2 = ttk.TTkWidget(parent=container2)
    widget3 = ttk.TTkWidget(parent=container2)
    widget4 = ttk.TTkWidget(parent=container1)
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget4.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    widget3.setDisabled()

    widget1.setFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.NoModifier,
        code='',)

    _check_focus_order(
        root=root, evt=tab_key,
        widgets=[
            container2,
            widget2,
            widget4,
            widget1,
        ],
        all_widgets=[
            container1,
            container2,
            widget1,
            widget2,
            widget3,
            widget4,
        ]
    )

def test_focus_mixed_containers_tab_focus_disabled_4():
    '''
        Root ─▶ Container1 (No TabFocus) ─┬─▶ Widget1
                                          ├─▶ Container2 (TabFocus) ─┬─▶ Widget2
                                          │                          └─▶ Widget3
                                          └─▶ Widget4
    '''
    root = ttk.TTk()
    container1 = ttk.TTkContainer(parent=root, name='Container1')
    widget1 = ttk.TTkWidget(parent=container1, name='Widget1')
    container2 = ttk.TTkContainer(parent=container1, name='Container2')
    container2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2 = ttk.TTkWidget(parent=container2, name='Widget2')
    widget3 = ttk.TTkWidget(parent=container2, name='Widget3')
    widget4 = ttk.TTkWidget(parent=container1, name='Widget4')
    widget1.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget2.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget3.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)
    widget4.setFocusPolicy(ttk.TTkK.FocusPolicy.TabFocus)

    all_widgets=[
        container1,
        container2,
        widget1,
        widget2,
        widget3,
        widget4,
    ]

    container2.setDisabled()
    widget2.setFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.NoModifier,
        code='',)

    _check_focus_order(
        root=root, evt=tab_key, all_widgets=all_widgets,
        widgets=[
            widget4,
            widget1,
            widget4,
        ],
    )

    container2.setDisabled()
    widget3.setFocus()

    tab_key = ttk.TTkKeyEvent(
        type=ttk.TTkK.KeyType.SpecialKey,
        key=ttk.TTkK.Key_Tab,
        mod=ttk.TTkK.ShiftModifier,
        code='',)

    _check_focus_order(
        root=root, evt=tab_key, all_widgets=all_widgets,
        widgets=[
            widget1,
            widget4,
            widget1,
        ],
    )
