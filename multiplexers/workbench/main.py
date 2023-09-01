#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the"Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED"AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import pty
import sys
import threading
import argparse
from select import select


sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from TermTk.TTkCore.canvas import TTkCanvas

from wblib import *

# parser = argparse.ArgumentParser()
# parser.add_argument('-d', help='Debug (Add LogViewer Panel)',    action='store_true')
# args = parser.parse_args()

# class WBWindow(ttk.TTkWindow):

class WorkBench(ttk.TTkContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPadding(1,0,0,0)
    def paintEvent(self, canvas: TTkCanvas):
        w,h = self.size()
        canvas.fill(color=bgBLUE)
        # draw the title
        canvas.drawText(
            text=" pyTermTk Workbench.  Version 1.0   plenty of free memory",
            width=w,
            color=bgWHITE+fgBLUE)

        canvas.drawText(
            text="│◪│◩│",
            pos=(w-5,0),
            color=bgWHITE+fgBLUE)

class TTkWorkbench(ttk.TTk):
    def paintEvent(self, canvas: TTkCanvas):
        canvas.fill(color=bgBLUE)

root = TTkWorkbench(layout=ttk.TTkGridLayout())
root.setPadding(3,3,15,10)

wbl = WBLoader(size=root.size())
root.rootLayout().addWidget(wbl)

wb = WorkBench(parent=root)

win2  = WBWindow(parent=wb, pos=(5,2), size=(50,15), title="euWorkbench",)


win3  = WBWindow(parent=wb, pos=(15,10), size=(70,25),
                 wbbg=bgBLACK+fgWHITE,
                 title="Terminallo n.1",layout=ttk.TTkVBoxLayout())
term3 = ttk.TTkTerminal(parent=win3)
term3.runShell()

win1  = WBWindow(parent=wb, pos=(10,5), size=(60,20),
                 wbbg=bgBLACK+fgWHITE,
                 title="Terminallo n.1",layout=ttk.TTkVBoxLayout())
term1 = ttk.TTkTerminal(parent=win1)
term1.runShell()

wink  = WBWindow(parent=wb, pos=(10,30), size=(70,6),
                 wbbg=bgBLACK+fgWHITE,
                 title="Terminallo n.1",layout=ttk.TTkVBoxLayout())
ttk.TTkKeyPressView(parent=wink)


root.mainloop()