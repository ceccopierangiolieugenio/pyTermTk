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

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()

win1 = ttk.TTkWindow(parent=root, title='1', pos=( 0,0), size=(40,10), border=True)
win2 = ttk.TTkWindow(parent=root, title='2', pos=(20,3), size=(40,15), border=True)
win3 = ttk.TTkWindow(parent=win2, title='3', pos=( 0,0), size=(30,10), border=True)
win4 = ttk.TTkWindow(parent=win2, title='4', pos=( 5,4), size=(30,5), border=True)
win5 = ttk.TTkWindow(parent=win3, title='5', pos=( 0,0), size=(20,5), border=True)

win1.setFocusPolicy(ttk.TTkK.TabFocus | ttk.TTkK.ClickFocus)
win2.setFocusPolicy(ttk.TTkK.TabFocus | ttk.TTkK.ClickFocus)
win3.setFocusPolicy(ttk.TTkK.TabFocus | ttk.TTkK.ClickFocus)
win4.setFocusPolicy(ttk.TTkK.TabFocus | ttk.TTkK.ClickFocus)
win5.setFocusPolicy(ttk.TTkK.TabFocus | ttk.TTkK.ClickFocus)

root.mainloop()