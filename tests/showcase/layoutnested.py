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

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk


def demoLayoutNested(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)
    mainLayout = ttk.TTkVBoxLayout()
    frame.setLayout(mainLayout)

    gridLayout = ttk.TTkGridLayout()
    mainLayout.addItem(gridLayout)

    mainLayout.addWidget(ttk.TTkFrame(border=True,title="Frame1"))
    mainLayout.addWidget(ttk.TTkFrame(border=True,title="Frame2"))

    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button1"),0,0)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button2"),1,1)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button3"),2,2)

    gridLayout.addWidget(ttk.TTkFrame(border=True,title="Frame3"),0,1)
    gridLayout.addWidget(ttk.TTkFrame(border=True,title="Frame4"),2,3)

    return frame




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if args.f:
        rootLayout = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootLayout = ttk.TTkWindow(title="Test Layout", parent=root,pos=(1,1), size=(100,40), border=True, layout=ttk.TTkGridLayout())
    demoLayoutNested(rootLayout)
    root.mainloop()

if __name__ == "__main__":
    main()