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


def demoSplitter(root=None):
    vsplitter = ttk.TTkSplitter(parent=root, border=True, orientation=ttk.TTkK.VERTICAL)
    ttk.TTkFrame(parent=vsplitter ,border=True, title="Frame1.1")
    hsplitter1 = ttk.TTkSplitter(parent=vsplitter, border=True)
    ttk.TTkFrame(parent=vsplitter ,border=True, title="Frame1.2")
    hsplitter2 = ttk.TTkSplitter(parent=vsplitter, border=True)
    ttk.TTkFrame(parent=vsplitter ,border=True, title="Frame1.3")
    ttk.TTkFrame(parent=hsplitter1 ,border=True, title="Frame3")
    ttk.TTkTestWidgetSizes(parent=hsplitter1 ,border=True, title="Frame2", minSize=(33,7), maxSize=(33,7))
    ttk.TTkFrame(parent=hsplitter1 ,border=True, title="Frame4")

    ttk.TTkFrame(parent=hsplitter2 ,border=True, title="Frame5")
    ttk.TTkTestWidgetSizes(parent=hsplitter2 ,border=True, title="Frame6", minSize=(33,7), maxSize=(33,7))
    ttk.TTkFrame(parent=hsplitter2 ,border=True, title="Frame7")
    ttk.TTkTestWidgetSizes(parent=hsplitter2 ,border=True, title="Frame8", minSize=(33,7), maxSize=(33,7))
    ttk.TTkFrame(parent=hsplitter2 ,border=True, title="Frame9")
    return vsplitter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    root = ttk.TTk()
    if args.f:
        rootSplitter = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootSplitter = ttk.TTkWindow(parent=root,pos = (5,5), size=(100,40), title="Test Splitter", border=True, layout=ttk.TTkGridLayout())
    demoSplitter(rootSplitter)
    root.mainloop()

if __name__ == "__main__":
    main()