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

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()

win1 = ttk.TTkWindow(parent=root,pos = (1,1), size=(60,30), title="Test Window 1", border=True)

win2_1 = ttk.TTkWindow(parent=win1,pos = (3,3), size=(40,20), title="Test Window 2.1", border=True)
win2_1.setLayout(ttk.TTkHBoxLayout())
ttk.TTkTestWidget(parent=win2_1, border=False)

win2_2 = ttk.TTkWindow(parent=win1,pos = (5,5), size=(40,20), title="Test Window 2.2", border=True)
win2_2.setLayout(ttk.TTkHBoxLayout())
ttk.TTkTestWidget(parent=win2_2, border=False)


win3 = ttk.TTkWindow(parent=root,pos = (20,5), size=(60,20), title="Test Window 3", border=True)
win3.setLayout(ttk.TTkHBoxLayout())

ttk.TTkTestWidget(parent=win3, border=True, maxWidth=30, minWidth=20)
rightFrame = ttk.TTkFrame(parent=win3, border=True)
rightFrame.setLayout(ttk.TTkVBoxLayout())

ttk.TTkTestWidget(parent=rightFrame, border=True, maxSize=(50,15), minSize=(30,8))
bottomrightframe = ttk.TTkFrame(parent=rightFrame,border=True)

win4 = ttk.TTkWindow(parent=bottomrightframe, pos = (3,3), size=(40,20), title="Test Window 4", border=True)
win4.setLayout(ttk.TTkHBoxLayout())
ttk.TTkTestWidget(parent=win4, border=False)

root.mainloop()