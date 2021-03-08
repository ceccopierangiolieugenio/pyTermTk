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

import TermTk as ttk

root = ttk.TTk()

    # Create a window with a logviewer
logWin = ttk.TTkWindow(parent=root,pos = (10,2), size=(80,20), title="LogViewer Window", border=True, layout=ttk.TTkVBoxLayout())
ttk.TTkLogViewer(parent=logWin)

    # Create 2 buttons
btnShow = ttk.TTkButton(parent=root, text="Show", pos=(0,0), size=(10,3), border=True)
btnHide = ttk.TTkButton(parent=root, text="Hide", pos=(0,3), size=(10,3), border=True)

    # Connect the btnShow's "clicked" signal with the window's "show" slot
btnShow.clicked.connect(logWin.show)
    # Connect the btnHide's "clicked" signal with the window's "hide" slot
btnHide.clicked.connect(logWin.hide)

root.mainloop()