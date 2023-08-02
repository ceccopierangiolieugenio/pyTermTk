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
    hsplitter1 = ttk.TTkSplitter(border=True)
    hsplitter2 = ttk.TTkSplitter(border=True)

    wid11 = ttk.TTkFrame(border=True, title="Frame1.1")
    wid12 = ttk.TTkFrame(border=True, title="Frame1.2")
    wid13 = ttk.TTkFrame(border=True, title="Frame1.3")
    wid3  = ttk.TTkFrame(border=True, title="Frame3")
    wid2  = ttk.TTkTestWidgetSizes(border=True, title="Frame2", minSize=(33,7), maxSize=(33,7))
    wid4  = ttk.TTkFrame(border=True, title="Frame4")

    wid5  = ttk.TTkFrame(border=True, title="Frame5")
    wid6  = ttk.TTkTestWidgetSizes(border=True, title="Frame6", minSize=(33,7), maxSize=(33,7))
    wid7  = ttk.TTkFrame(border=True, title="Frame7")
    wid8  = ttk.TTkTestWidgetSizes(border=True, title="Frame8", minSize=(33,7), maxSize=(33,7))
    wid9  = ttk.TTkFrame(border=True, title="Frame9")

    vsplitter.addWidget(wid11, title="Test 1.1")
    vsplitter.addWidget(hsplitter1)
    vsplitter.addWidget(wid12, title="Test 1.2")
    vsplitter.addWidget(hsplitter2, title="Test HSplit 2")
    vsplitter.addWidget(wid13)

    hsplitter1.addWidget(wid3, title="Test 3")
    hsplitter1.addWidget(wid2, title="Test 2")
    hsplitter1.addWidget(wid4)

    hsplitter2.addWidget(wid5, title="Test 5")
    hsplitter2.addWidget(wid6)
    hsplitter2.addWidget(wid7, title="Test 7")
    hsplitter2.addWidget(wid8, title="Test 8")
    hsplitter2.addWidget(wid9, title="Test 9")

    return vsplitter

def demoSplitter(root=None):
    vsplitter = ttk.TTkSplitter(parent=root, border=True, orientation=ttk.TTkK.VERTICAL)
    hsplitter1 = ttk.TTkSplitter(border=True)
    hsplitter2 = ttk.TTkSplitter(border=True)

    wid11 = ttk.TTkFrame(border=True, title="Frame1.1")
    wid12 = ttk.TTkFrame(border=True, title="Frame1.2")
    wid13 = ttk.TTkFrame(border=True, title="Frame1.3")
    wid3  = ttk.TTkFrame(border=True, title="Frame3")
    wid2  = ttk.TTkTestWidgetSizes(border=True, title="Frame2", minSize=(33,7), maxSize=(33,7))
    wid4  = ttk.TTkFrame(border=True, title="Frame4")

    wid5  = ttk.TTkFrame(border=True, title="Frame5")
    wid6  = ttk.TTkTestWidgetSizes(border=True, title="Frame6", minSize=(33,7), maxSize=(33,7))
    wid7  = ttk.TTkFrame(border=True, title="Frame7")
    wid8  = ttk.TTkTestWidgetSizes(border=True, title="Frame8", minSize=(33,7), maxSize=(33,7))
    wid9  = ttk.TTkFrame(border=True, title="Frame9")

    vsplitter.addWidget(wid11, title="Test 1.1")
    vsplitter.addWidget(hsplitter1)
    vsplitter.addWidget(wid12, title="Test 1.2")
    vsplitter.addWidget(hsplitter2, title="Test HSplit 2")
    vsplitter.addWidget(wid13)

    hsplitter1.addWidget(wid3, title="Test 3")
    hsplitter1.addWidget(wid2, title="Test 2")
    hsplitter1.addWidget(wid4)

    hsplitter2.addWidget(wid5, title="Test 5")
    hsplitter2.addWidget(wid6)
    hsplitter2.addWidget(wid7, title="Test 7")
    hsplitter2.addWidget(wid8, title="Test 8")
    hsplitter2.addWidget(wid9, title="Test 9")

    return vsplitter

def demoHSplitter(root=None):
    hsplitter2 = ttk.TTkSplitter(parent=root, border=True)

    wid5  = ttk.TTkFrame(border=True, title="Frame5")
    wid6  = ttk.TTkTestWidgetSizes(border=True, title="Frame6")
    wid7  = ttk.TTkFrame(border=True, title="Frame7")
    wid8  = ttk.TTkTestWidgetSizes(border=True, title="Frame8")
    wid9  = ttk.TTkFrame(border=True, title="Frame9")

    hsplitter2.addWidget(wid5, title="Test 5")
    hsplitter2.addWidget(wid6)
    hsplitter2.addWidget(wid7, title="Test 7")
    hsplitter2.addWidget(wid8, title="Test 8")
    hsplitter2.addWidget(wid9, title="Test 9")

    return hsplitter2
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    root = ttk.TTk()
    if args.f:
        rootSplitter = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootSplitter = ttk.TTkWindow(parent=root,pos = (5,5), size=(100,40), title="Test Splitter",  border=True, layout=ttk.TTkGridLayout())
        demoHSplitter(ttk.TTkWindow(parent=root,pos = (0,0), size=(100,15), title="Test H Splitter", border=True, layout=ttk.TTkGridLayout()))
    demoSplitter(rootSplitter)
    root.mainloop()

if __name__ == "__main__":
    main()