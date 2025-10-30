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

import sys, os, argparse

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

def demoDnDTabs(root=None, border=True):
    vsplitter = ttk.TTkSplitter(parent=root, orientation=ttk.TTkK.VERTICAL)
    tabWidget1 = ttk.TTkTabWidget(parent=vsplitter, border=border)
    hsplitter = ttk.TTkSplitter(parent=vsplitter)
    tabWidget2 = ttk.TTkTabWidget(parent=hsplitter, border=False, barType=ttk.TTkBarType.DEFAULT_2)
    tabWidget3 = ttk.TTkTabWidget(parent=hsplitter, border=False, barType=ttk.TTkBarType.NERD_1)

    tabWidget1.addTab(ttk.TTkLogViewer(follow=True),  "Logs")

    tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.1"),  "Label 1.1")
    tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.2"),  "Label 1.2")
    tabWidget1.addTab(ttk.TTkTestWidget(     border=True, title="Frame1.3"),  "Label Test 1.3")
    tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.4"),  "Label 1.4")
    tabWidget1.addTab(ttk.TTkTestWidget(     border=True, title="Frame1.5"),  "Label Test 1.5")
    tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.6"),  "Label 1.6")
    tabWidget1.addTab(ttk.TTkTestWidget(     border=True, title="Frame1.7"),  "Label Test 1.7")
    tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.8"),  "Label 1.8")
    tabWidget2.addTab(ttk.TTkTestWidget(     border=True, title="Frame1.9"),  "Label Test 1.9")
    tabWidget3.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.10"), "Label 1.10")

    fileMenu1 = tabWidget1.addMenu("XX")
    fileMenu1.addMenu("Open")
    fileMenu1.addMenu("Close")
    fileMenu1.addMenu("Exit")

    fileMenu2 = tabWidget1.addMenu("YY")
    fileMenu2.addMenu("Open")
    fileMenu2.addMenu("Close")
    fileMenu2.addMenu("Exit")

    tabWidget1.addMenu("ZZ", ttk.TTkK.RIGHT)
    tabWidget1.addMenu("KK", ttk.TTkK.RIGHT)

    return vsplitter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    root = ttk.TTk()
    if args.f:
        rootTab = root
        root.setLayout(ttk.TTkGridLayout())
        border=False
    else:
        rootTab = ttk.TTkWindow(parent=root,pos=(1,1), size=(100,44), title="Test Tab", border=True, layout=ttk.TTkGridLayout())
        border=True
    demoDnDTabs(rootTab, border)
    root.mainloop()

if __name__ == "__main__":
    main()