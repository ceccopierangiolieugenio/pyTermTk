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

import os, sys, argparse
from select import select

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

parser = argparse.ArgumentParser()
parser.add_argument('-d', help='Debug (Add LogViewer Panel)',    action='store_true')
args = parser.parse_args()

# ttk.TTkLog.use_default_file_logging()
root = ttk.TTk(layout=ttk.TTkGridLayout(), mouseTrack=True)

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

winT  = ttk.TTkWindow(pos=(20,10), size=(100,30), title="TextEdit", border=True, layout=ttk.TTkVBoxLayout(), flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint|ttk.TTkK.WindowFlag.WindowCloseButtonHint)
te = ttk.TTkTextEdit(parent=winT, readOnly=False, lineNumber=True)

clipboard = ttk.TTkClipboard()

@ttk.pyTTkSlot(ttk.TTkString)
def _textSelected(text, te=te):
    te.setText("Selected Text in the terminal:")
    te.append( "------------------------------\n")
    te.append(text)

tnum = 0
@ttk.pyTTkSlot()
def _addTerminal():
    global tnum
    tnum+=1
    win  = ttk.TTkWindow(pos=(12,0), size=(100,30), title=f"Terminallo n.{tnum}", border=True, layout=ttk.TTkVBoxLayout(), flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint|ttk.TTkK.WindowFlag.WindowCloseButtonHint)
    term = ttk.TTkTerminal(parent=win)

    th = ttk.TTkTerminalHelper(term=term)
    th.terminalClosed.connect(win.close)

    term.bell.connect(lambda : ttk.TTkLog.debug("BELL!!! 🔔🔔🔔"))
    term.titleChanged.connect(win.setTitle)

    term.textSelected.connect(clipboard.setText)
    term.textSelected.connect(_textSelected)
    win.closed.connect(term.close)
    top.addWidget(win)
    term.setFocus()
    term.raiseWidget()

    th.runShell()

addBtn = ttk.TTkButton(pos=(0,7), text="New Term.", border=True)
addBtn.clicked.connect(_addTerminal)

top.addWidgets([quitBtn, addBtn, cb_c, cb_s, cb_z, cb_q, winT])

_addTerminal()

root.mainloop()