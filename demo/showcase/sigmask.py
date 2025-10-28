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

import os
import sys
import argparse

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

def demoSigmask(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)
    frame.setLayout(grid:=ttk.TTkGridLayout())

    grid.addWidget(cb_c := ttk.TTkCheckbox(text="CTRL-C (VINTR) ", checked=ttk.TTkK.Checked),0,0,1,2)
    grid.addWidget(cb_s := ttk.TTkCheckbox(text="CTRL-S (VSTOP) ", checked=ttk.TTkK.Checked),1,0,1,2)
    grid.addWidget(cb_z := ttk.TTkCheckbox(text="CTRL-Z (VSUSP) ", checked=ttk.TTkK.Checked),2,0,1,2)
    grid.addWidget(cb_q := ttk.TTkCheckbox(text="CTRL-Q (VSTART)", checked=ttk.TTkK.Checked),3,0,1,2)

    grid.addWidget(btn_q := ttk.TTkButton(text="Quit", maxSize=(6,3), border=True),4,0)

    grid.addWidget(ttk.TTkKeyPressView(),5,0,1,3)

    btn_q.clicked.connect(ttk.TTkHelper.quit)

    cb_c.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_C,x==ttk.TTkK.Checked))
    cb_s.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_S,x==ttk.TTkK.Checked))
    cb_z.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_Z,x==ttk.TTkK.Checked))
    cb_q.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_Q,x==ttk.TTkK.Checked))

    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen (default)', action='store_true')
    parser.add_argument('-w', help='Windowed',    action='store_true')
    args = parser.parse_args()
    windowed = args.w

    root = ttk.TTk()

    if windowed:
        rootDemo = ttk.TTkWindow(parent=root, pos=(0,0), size=(70,20), title="Test Text Edit", layout=ttk.TTkGridLayout(), border=True)
    else:
        rootDemo = root
        root.setLayout(ttk.TTkGridLayout())
    demoSigmask(rootDemo)
    root.mainloop()

if __name__ == "__main__":
    main()