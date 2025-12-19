#!/usr/bin/env python3

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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

root = ttk.TTk(mouseTrack=True)

winTabbed1 = ttk.TTkWindow(parent=root,pos=(0,0), size=(80,20), title="Test Tab 1", border=True, layout=ttk.TTkGridLayout())
tabWidget1 = ttk.TTkTabWidget(parent=winTabbed1, border=True, barType=ttk.TTkBarType.DEFAULT_3)
tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.1"), "Label 1.1")
tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.2"), "Label 1.2")
tabWidget1.addTab(ttk.TTkTestWidget(border=True, title="Frame1.3"), "Label Test 1.3")
tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.4"), "Label 1.4")
tabWidget1.addTab(ttk.TTkTestWidget(border=True, title="Frame1.5"), "Label Test 1.5")
tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.6"), "Label 1.6")

winTabbed2 = ttk.TTkWindow(parent=root,pos=(10,2), size=(80,20), title="Test Tab 2", border=True, layout=ttk.TTkGridLayout())
tabWidget2 = ttk.TTkTabWidget(parent=winTabbed2, border=True, barType=ttk.TTkBarType.DEFAULT_3)
tabWidget2.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame2.1"), "Label 2.1")
tabWidget2.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame2.2"), "Label 2.2")
tabWidget2.addTab(ttk.TTkTestWidget(border=True, title="Frame2.3"), "Label Test 2.3")
tabWidget2.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame2.4"), "Label 2.4")
tabWidget2.addTab(ttk.TTkTestWidget(border=True, title="Frame2.5"), "Label Test 2.5")
tabWidget2.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame2.6"), "Label 2.6")
tabWidget2.addMenu("Foo")
tabWidget2.addMenu("Bar", ttk.TTkK.RIGHT)

winTabbed3 = ttk.TTkWindow(parent=root,pos=(20,4), size=(80,20), title="Test Tab 3", border=True, layout=ttk.TTkGridLayout())
tabWidget3 = ttk.TTkTabWidget(parent=winTabbed3, border=True, barType=ttk.TTkBarType.DEFAULT_2)
tabWidget3.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame3.1"), "Label 3.1")
tabWidget3.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame3.2"), "Label 3.2")
tabWidget3.addTab(ttk.TTkTestWidget(border=True, title="Frame3.3"), "Label Test 3.3")
tabWidget3.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame3.4"), "Label 3.4")
tabWidget3.addTab(ttk.TTkTestWidget(border=True, title="Frame3.5"), "Label Test 3.5")
tabWidget3.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame3.6"), "Label 3.6")

winTabbed4 = ttk.TTkWindow(parent=root,pos=(30,6), size=(80,20), title="Test Tab 4", border=True, layout=ttk.TTkGridLayout())
tabWidget4 = ttk.TTkTabWidget(parent=winTabbed4, border=True, barType=ttk.TTkBarType.DEFAULT_2)
tabWidget4.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame4.1"), "Label 4.1")
tabWidget4.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame4.2"), "Label 4.2")
tabWidget4.addTab(ttk.TTkTestWidget(border=True, title="Frame4.3"), "Label Test 4.3")
tabWidget4.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame4.4"), "Label 4.4")
tabWidget4.addTab(ttk.TTkTestWidget(border=True, title="Frame4.5"), "Label Test 4.5")
tabWidget4.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame4.6"), "Label 4.6")
tabWidget4.addMenu("Baz")
tabWidget4.addMenu("Foo", ttk.TTkK.RIGHT)

winTabbed5 = ttk.TTkWindow(parent=root,pos=(40,8), size=(80,20), title="Test Tab 5", border=True, layout=ttk.TTkGridLayout())
tabWidget5 = ttk.TTkTabWidget(parent=winTabbed5, border=True, barType=ttk.TTkBarType.NERD_1)
tabWidget5.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame5.1"), "Label 5.1")
tabWidget5.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame5.2"), "Label 5.2")
tabWidget5.addTab(ttk.TTkTestWidget(border=True, title="Frame5.3"), "Label Test 5.3")
tabWidget5.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame5.4"), "Label 5.4")
tabWidget5.addTab(ttk.TTkTestWidget(border=True, title="Frame5.5"), "Label Test 5.5")
tabWidget5.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame5.6"), "Label 5.6")

winLogs = ttk.TTkWindow(parent=root,pos=(45,10), size=(100,30), title="Logs", border=True, layout=ttk.TTkGridLayout())
ttk.TTkLogViewer(parent=winLogs)

root.mainloop()