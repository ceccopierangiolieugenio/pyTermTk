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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

def demoScrollArea(root= None):
    scrollArea = ttk.TTkScrollArea(parent=root)
    ttk.TTkTestWidgetSizes(pos=(0,0)   , size=(40,20), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(10,25) , size=(40,20), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(20,50) , size=(60,10), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(50,0)  , size=(40,10), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(100,0)  , size=(40,10), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(150,0)  , size=(40,10), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(60,30) , size=(60,10), parent=scrollArea.viewport(), border=True)
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
        rootGraph = ttk.TTkWindow(parent=root,pos=(1,1), size=(100,40), title="Test Graph", border=True, layout=ttk.TTkGridLayout())
    demoScrollArea(rootGraph)
    root.mainloop()

if __name__ == "__main__":
    main()