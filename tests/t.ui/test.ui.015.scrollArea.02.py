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

def demoScrollArea(root):
    w1 = ttk.TTkWindow(parent=root,pos=(0,0), size=(50,20), title="sa1", border=True, layout=ttk.TTkGridLayout())
    sa1 = ttk.TTkScrollArea(parent=w1)
    ttk.TTkTestWidgetSizes(pos=(0,0)   , size=(40,10), parent=sa1.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(10,15) , size=(40,10), parent=sa1.viewport(), border=True)

    w2 = ttk.TTkWindow(parent=root,pos=(10,10), size=(50,20), title="sa2 - Vertical Off", border=True, layout=ttk.TTkGridLayout())
    sa2 = ttk.TTkScrollArea(parent=w2, verticalScrollBarPolicy=ttk.TTkK.ScrollBarAlwaysOff)
    ttk.TTkTestWidgetSizes(pos=(0,0)   , size=(40,10), parent=sa2.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(10,15) , size=(40,10), parent=sa2.viewport(), border=True)

    w3 = ttk.TTkWindow(parent=root,pos=(20,20), size=(50,20), title="sa3 - Horizontal Off", border=True, layout=ttk.TTkGridLayout())
    sa3 = ttk.TTkScrollArea(parent=w3, horizontalScrollBarPolicy=ttk.TTkK.ScrollBarAlwaysOff)
    ttk.TTkTestWidgetSizes(pos=(0,0)   , size=(40,10), parent=sa3.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(10,15) , size=(40,10), parent=sa3.viewport(), border=True)

    ttk.TTkLabel(             parent=root, pos=(55,0), size=(15,1), text="sa1 - Vertical Scrollbar:" )
    vsb1 = ttk.TTkRadioButton(parent=root, pos=(55,1), size=(15,1), text="As Needed" , radiogroup="VSB", checked=True)
    vsb2 = ttk.TTkRadioButton(parent=root, pos=(55,2), size=(15,1), text="Always On" , radiogroup="VSB")
    vsb3 = ttk.TTkRadioButton(parent=root, pos=(55,3), size=(15,1), text="Always Off", radiogroup="VSB")

    ttk.TTkLabel(             parent=root, pos=(55,5), size=(15,1), text="sa1 - Horizontal Scrollbar:" )
    hsb1 = ttk.TTkRadioButton(parent=root, pos=(55,6), size=(15,1), text="As Needed" , radiogroup="HSB", checked=True)
    hsb2 = ttk.TTkRadioButton(parent=root, pos=(55,7), size=(15,1), text="Always On" , radiogroup="HSB")
    hsb3 = ttk.TTkRadioButton(parent=root, pos=(55,8), size=(15,1), text="Always Off", radiogroup="HSB")

    vsb1.clicked.connect(lambda : sa1.setVerticalScrollBarPolicy(ttk.TTkK.ScrollBarAsNeeded))
    vsb2.clicked.connect(lambda : sa1.setVerticalScrollBarPolicy(ttk.TTkK.ScrollBarAlwaysOn))
    vsb3.clicked.connect(lambda : sa1.setVerticalScrollBarPolicy(ttk.TTkK.ScrollBarAlwaysOff))

    hsb1.clicked.connect(lambda : sa1.setHorizontalScrollBarPolicy(ttk.TTkK.ScrollBarAsNeeded))
    hsb2.clicked.connect(lambda : sa1.setHorizontalScrollBarPolicy(ttk.TTkK.ScrollBarAlwaysOn))
    hsb3.clicked.connect(lambda : sa1.setHorizontalScrollBarPolicy(ttk.TTkK.ScrollBarAlwaysOff))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if args.f:
        rootGraph = root
    else:
        rootGraph = ttk.TTkWindow(parent=root,pos=(1,1), size=(150,50), title="Test Graph", border=True)
    demoScrollArea(rootGraph)
    root.mainloop()

if __name__ == "__main__":
    main()