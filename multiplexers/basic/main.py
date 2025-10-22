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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

parser = argparse.ArgumentParser()
parser.add_argument('-d', help='Debug (Add LogViewer Panel)',    action='store_true')
args = parser.parse_args()

# ttk.TTkLog.use_default_file_logging()
root = ttk.TTk(layout=ttk.TTkGridLayout())

split = ttk.TTkSplitter(parent=root, orientation=ttk.TTkK.VERTICAL)

split.addItem(top := ttk.TTkLayout())

if args.d:
    split.addWidget(ttk.TTkLogViewer(follow=False ), title='Log', size=20)

quitBtn = ttk.TTkButton(text="QUIT", border=True)
quitBtn.clicked.connect(ttk.TTkHelper.quit)

cb_c = ttk.TTkCheckbox(pos=(0,3),size=(20,1), text="CTRL-C (VINTR) ", checked=ttk.TTkK.Checked)
cb_s = ttk.TTkCheckbox(pos=(0,4),size=(20,1), text="CTRL-S (VSTOP) ", checked=ttk.TTkK.Checked)
cb_z = ttk.TTkCheckbox(pos=(0,5),size=(20,1), text="CTRL-Z (VSUSP) ", checked=ttk.TTkK.Checked)
cb_q = ttk.TTkCheckbox(pos=(0,6),size=(20,1), text="CTRL-Q (VSTART)", checked=ttk.TTkK.Checked)

cb_c.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_C,x==ttk.TTkK.Checked))
cb_s.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_S,x==ttk.TTkK.Checked))
cb_z.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_Z,x==ttk.TTkK.Checked))
cb_q.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_Q,x==ttk.TTkK.Checked))

win1  = ttk.TTkWindow(pos=(90,5), size=(70,15), title="Terminallo n.1", border=True, layout=ttk.TTkVBoxLayout(), flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
term1 = ttk.TTkTerminal(parent=win1)
th1 = ttk.TTkTerminalHelper(term=term1)
th1.runShell()

win2  = ttk.TTkWindow(pos=(0,0), size=(150,30), title="Terminallo n.2", border=True, layout=ttk.TTkVBoxLayout(), flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
term2 = ttk.TTkTerminal(parent=win2)
th2 = ttk.TTkTerminalHelper(term=term2)
th2.runShell()

win3  = ttk.TTkWindow(pos=(92,8), size=(70,15), title="Terminallo n.3", border=True, layout=ttk.TTkVBoxLayout(), flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
term3 = ttk.TTkTerminal(parent=win3)
th3 = ttk.TTkTerminalHelper(term=term3)
th3.runShell()

win4  = ttk.TTkWindow(pos=(94,11), size=(70,15), title="Terminallo n.4", border=True, layout=ttk.TTkVBoxLayout(), flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
term4 = ttk.TTkTerminal(parent=win4)
th4 = ttk.TTkTerminalHelper(term=term4)
th4.runShell()

top.addWidgets([quitBtn, cb_c, cb_s, cb_z, cb_q, win1, win2, win3, win4])

term2.setFocus()

root.mainloop()