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

def test_focus_01_no_root():
    '''
        Container ─┬─▶ Widget1
                   ├─▶ Widget3
                   └─▶ Widget3
    '''
    container = ttk.TTkContainer()
    widget1 = ttk.TTkWidget(parent=container)
    widget2 = ttk.TTkWidget(parent=container)
    widget3 = ttk.TTkWidget(parent=container)

    assert False is container.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    widget2.setFocus()

    assert False is container.hasFocus()
    assert False is widget1.hasFocus()
    assert False  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    widget2.clearFocus()

    assert False is container.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

def test_focus_01_with_root():
    '''
        Container ─┬─▶ Widget1
                   ├─▶ Widget3
                   └─▶ Widget3
    '''
    root = ttk.TTk()
    widget1 = ttk.TTkWidget(parent=root)
    widget2 = ttk.TTkWidget(parent=root)
    widget3 = ttk.TTkWidget(parent=root)

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    widget2.setFocus()

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    widget2.clearFocus()

    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

def test_focus_02():
    '''
        Root ─▶ Container ─┬─▶ Widget1
                           ├─▶ Widget2
                           └─▶ Widget3
    '''
    root = ttk.TTk()
    container = ttk.TTkContainer(parent=root)
    widget1 = ttk.TTkWidget(parent=container)
    widget2 = ttk.TTkWidget(parent=container)
    widget3 = ttk.TTkWidget(parent=container)

    assert False is container.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    widget2.setFocus()

    assert False is container.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    widget2.clearFocus()

    assert False is container.hasFocus()
    assert False is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

def test_focus_03_sequential():
    '''Test sequential focus changes between widgets'''
    root = ttk.TTk()
    widget1 = ttk.TTkWidget(parent=root)
    widget2 = ttk.TTkWidget(parent=root)
    widget3 = ttk.TTkWidget(parent=root)

    widget1.setFocus()
    assert False is root.hasFocus()
    assert True  is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

    widget2.setFocus()
    assert False is root.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    widget3.setFocus()
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
    container2 = ttk.TTkContainer(parent=container1)
    widget1 = ttk.TTkWidget(parent=container1)
    widget2 = ttk.TTkWidget(parent=container2)
    widget3 = ttk.TTkWidget(parent=container2)

    widget2.setFocus()
    assert False is container1.hasFocus()
    assert False is container2.hasFocus()
    assert False is widget1.hasFocus()
    assert True  is widget2.hasFocus()
    assert False is widget3.hasFocus()

    widget1.setFocus()
    assert False is container1.hasFocus()
    assert False is container2.hasFocus()
    assert True  is widget1.hasFocus()
    assert False is widget2.hasFocus()
    assert False is widget3.hasFocus()

def test_focus_05_multiple_setFocus():
    '''Test calling setFocus multiple times on same widget'''
    root = ttk.TTk()
    widget1 = ttk.TTkWidget(parent=root)
    widget2 = ttk.TTkWidget(parent=root)

    widget1.setFocus()
    widget1.setFocus()
    assert (widget1.hasFocus(), widget2.hasFocus()) == (True, False)

def test_focus_06_clearFocus_without_focus():
    '''Test clearFocus on widget that doesn't have focus'''
    root = ttk.TTk()
    widget1 = ttk.TTkWidget(parent=root)
    widget2 = ttk.TTkWidget(parent=root)

    widget1.setFocus()
    widget2.clearFocus()
    assert (widget1.hasFocus(), widget2.hasFocus()) == (True, False)

def test_focus_07_single_widget():
    '''Test focus behavior with single widget'''
    root = ttk.TTk()
    widget = ttk.TTkWidget(parent=root)

    assert (root.hasFocus(), widget.hasFocus()) == (False, False)

    widget.setFocus()
    assert (root.hasFocus(), widget.hasFocus()) == (False, True)

    widget.clearFocus()
    assert (root.hasFocus(), widget.hasFocus()) == (False, False)