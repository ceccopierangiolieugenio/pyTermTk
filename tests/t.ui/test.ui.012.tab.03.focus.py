#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

ttk.TTkLog.use_default_file_logging()

class TestFocus(ttk.TTkContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        le = ttk.TTkLineEdit(parent=self, pos=(0,1), size=(50,1))
        self.focusChanged.connect(le.setFocus)

root = ttk.TTk()

winTabbed1 = ttk.TTkWindow(parent=root,pos=(1,1), size=(100,40), title="Test Tab", border=True, layout=ttk.TTkGridLayout())
tabWidget1 = ttk.TTkTabWidget(parent=winTabbed1, border=True)
tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.1"), "Label 1.1")
tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.2"), "Label 1.2")
tabWidget1.addTab(TestFocus(), "Test Focus 1")
tabWidget1.addTab(ttk.TTkTextEdit(), "Text Edit 1")
tabWidget1.addTab(ttk.TTkTestWidget(border=True, title="Frame1.5"), "Label Test 1.5")
tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.6"), "Label 1.6")

@ttk.pyTTkSlot(int)
def _handleCurrentChanged(int):
    wid = tabWidget1.widget(int)
    if isinstance(wid, TestFocus):
        wid.setFocus()

tabWidget1.currentChanged.connect(_handleCurrentChanged)

root.mainloop()