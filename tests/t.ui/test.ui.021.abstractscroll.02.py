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

import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

class ScrollAreaTest(ttk.TTkAbstractScrollArea):
    __slots__ = ('_areaView')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'parent' in kwargs: kwargs.pop('parent')
        self.setFocusPolicy(ttk.TTkK.ClickFocus)
        scrollLayout = ttk.TTkAbstractScrollViewGridLayout()
        w1 = ttk.TTkTestAbstractScrollWidget(areaSize=(100,40), areaPos=(10,5))
        w2 = ttk.TTkTestAbstractScrollWidget(areaSize=(100,40), areaPos=(10,5), maxWidth=30)
        w3 = ttk.TTkTestAbstractScrollWidget(areaSize=( 50,20), areaPos=(10,5))
        scrollLayout.addWidget(w1,0,0,2,1)
        scrollLayout.addWidget(w2,0,1)
        scrollLayout.addWidget(w3,1,1)
        self.setViewport(scrollLayout)

def demoScrollArea(root= None):
    scrollArea = ScrollAreaTest(parent=root)
    return scrollArea

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if args.f:
        rootGraph = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootGraph = ttk.TTkWindow(parent=root,pos=(1,1), size=(55,20), title="Test Graph", border=True, layout=ttk.TTkGridLayout())
    demoScrollArea(rootGraph)
    root.mainloop()

if __name__ == "__main__":
    main()