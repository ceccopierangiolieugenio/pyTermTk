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


def demoLayoutSpan1(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)

    gridLayout = ttk.TTkGridLayout()
    frame.setLayout(gridLayout)

    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button1"),0,0,1,4)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button2"),0,4,4,1)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button3"),1,0,4,1)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button4"),4,1,1,4)

    gridLayout.addWidget(ttk.TTkButton(border=True, text="B1"),1,1,2,1)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="B2"),1,2,1,2)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="B3"),2,3,2,1)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="B4"),3,1,1,2)

    return frame

def demoLayoutSpan2(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)

    gridLayout = ttk.TTkGridLayout()
    frame.setLayout(gridLayout)

    nestedLayout = ttk.TTkGridLayout()
    gridLayout.addItem(nestedLayout,1,1)

    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button1"),0,0,1,2)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button2"),0,2,2,1)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button3"),1,0,2,1)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button4"),2,1,1,2)

    nestedLayout.addWidget(ttk.TTkButton(border=True, text="B1", color=ttk.TTkColor.fg("#880000")+ttk.TTkColor.bg("#ffff66")+ttk.TTkColor.BOLD),0,0,2,1)
    nestedLayout.addWidget(ttk.TTkButton(border=True, text="B2", color=ttk.TTkColor.fg("#880000")+ttk.TTkColor.bg("#ffff66")+ttk.TTkColor.BOLD),0,1,1,2)
    nestedLayout.addWidget(ttk.TTkButton(border=True, text="B3", color=ttk.TTkColor.fg("#880000")+ttk.TTkColor.bg("#ffff66")+ttk.TTkColor.BOLD),1,2,2,1)
    nestedLayout.addWidget(ttk.TTkButton(border=True, text="B4", color=ttk.TTkColor.fg("#880000")+ttk.TTkColor.bg("#ffff66")+ttk.TTkColor.BOLD),2,0,1,2)

    return frame

def demoLayoutSpan3(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)

    gridLayout = ttk.TTkGridLayout()
    frame.setLayout(gridLayout)

    nestedLayout = ttk.TTkGridLayout()
    gridLayout.addItem(nestedLayout,1,1)

    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button1"),0,0,1,5)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button2"),0,5,3,1)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button3"),1,0,4,1)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button4"),4,1,1,2)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button5"),1,1,3,3)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button6"),1,4,2,1)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button7"),3,4,2,2)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button8"),4,3)

    return frame


def main():
    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    rootLayout1 = ttk.TTkWindow(title="Test Layout", parent=root,pos=(0,0), size=(70,30), border=True, layout=ttk.TTkGridLayout())
    demoLayoutSpan1(rootLayout1)
    rootLayout2 = ttk.TTkWindow(title="Test Nested Layout", parent=root,pos=(10,5), size=(70,30), border=True, layout=ttk.TTkGridLayout())
    demoLayoutSpan2(rootLayout2)
    rootLayout3 = ttk.TTkWindow(title="Test 2d Span", parent=root,pos=(20,10), size=(70,30), border=True, layout=ttk.TTkGridLayout())
    demoLayoutSpan3(rootLayout3)
    rootLayout4 = ttk.TTkWindow(title="Logs", parent=root,pos=(15,7), size=(100,25), border=True, layout=ttk.TTkGridLayout())
    ttk.TTkLogViewer(parent=rootLayout4)

    root.mainloop()

if __name__ == "__main__":
    main()