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

root = TTkWorkbench(layout=ttk.TTkGridLayout(), mouseTrack=True)
root.setPadding(3,3,15,10)

wbl = WBLoader(size=root.size())
root.rootLayout().addWidget(wbl)

wb = WorkBench(parent=root)

ttk.pyTTkSlot()
def _openTerminal(term=[]):
    _x,_y = 15,5
    while (_x,_y) in [_t['pos'] for _t in term]:
        _x += 4
        _y += 2
    _win  = WBWindow(parent=wb, pos=(_x,_y), size=(60,20),
                    whiteBg=False,
                    title=f"Terminallo n.{len(term)+1}",layout=ttk.TTkVBoxLayout())
    _term = ttk.TTkTerminal(parent=_win)
    _term.runShell()
    _term.bell.connect(lambda : ttk.TTkLog.debug("BELL!!! 🔔🔔🔔"))
    _term.titleChanged.connect(_win.setTitle)
    term.append({'pos':(_x,_y),'term':_term,'win':_win})

winWb  = WBWindow(parent=wb, pos=(5,2), size=(50,15), title="euWorkbench")
WBIconButton(parent=winWb, text="Terminal").clicked.connect(_openTerminal)

root.mainloop()