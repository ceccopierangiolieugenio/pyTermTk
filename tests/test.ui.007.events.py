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

sys.path.append(os.path.join(sys.path[0], ".."))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()
btn1 = ttk.TTkButton(parent=root, x=0, y=0, width=15, height=3, text="Hide Window1")
btn2 = ttk.TTkButton(parent=root, x=0, y=3, width=15, height=3, text="Show Window1")
btn3 = ttk.TTkButton(
    parent=root, x=0, y=6, width=28, height=3, text="Hide Window2.1 and Window3"
)
btn4 = ttk.TTkButton(
    parent=root, x=0, y=9, width=28, height=3, text="Show Window2.1 and Window3"
)

win1 = ttk.TTkWindow(
    parent=root, pos=(1, 4), size=(60, 30), title="Test Window 1", border=True
)
# Connect the Buttons (clicked) signals to the Window slots (hide/show)
btn1.clicked.connect(win1.hide)
btn2.clicked.connect(win1.show)

win2_1 = ttk.TTkWindow(
    parent=win1,
    pos=(3, 3),
    size=(40, 20),
    title="Test Window 2.1",
    layout=ttk.TTkHBoxLayout(),
    border=True,
)
btn3.clicked.connect(win2_1.hide)
btn4.clicked.connect(win2_1.show)
ttk.TTkTestWidget(parent=win2_1, border=False)


win2_2 = ttk.TTkWindow(
    parent=win1,
    pos=(5, 5),
    size=(40, 20),
    title="Test Window 2.2",
    layout=ttk.TTkHBoxLayout(),
    border=True,
)
ttk.TTkTestWidget(parent=win2_2, border=False)


win3 = ttk.TTkWindow(
    parent=root,
    pos=(20, 7),
    size=(60, 20),
    title="Test Window 3",
    layout=ttk.TTkHBoxLayout(),
    border=True,
)
btn3.clicked.connect(win3.hide)
btn4.clicked.connect(win3.show)

ttk.TTkTestWidget(parent=win3, border=True, maxWidth=30, minWidth=20)
rightFrame = ttk.TTkFrame(parent=win3, layout=ttk.TTkVBoxLayout(), border=True)

ttk.TTkTestWidget(parent=rightFrame, border=True, maxSize=(50, 15), minSize=(30, 8))
bottomrightframe = ttk.TTkFrame(parent=rightFrame, border=True)

win4 = ttk.TTkWindow(
    parent=bottomrightframe,
    pos=(3, 3),
    size=(40, 20),
    title="Test Window 4",
    layout=ttk.TTkHBoxLayout(),
    border=True,
)
ttk.TTkTestWidget(parent=win4, border=False)

root.mainloop()
