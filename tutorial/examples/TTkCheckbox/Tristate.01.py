#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

##########
# Those 2 lines are required to use the TermTk library straight from the main folder
import sys, os
sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))
##########

'''
TTkCheckbox - Tristate Checkboxes

This example demonstrates TTkCheckbox in tristate mode, which adds a third
PartiallyChecked state in addition to the usual Checked and Unchecked states.

Key Features:
    - Enabling tristate mode with tristate=True
    - Cycling through Unchecked -> PartiallyChecked -> Checked states
    - Setting PartiallyChecked state via checkStatus parameter
    - Setting PartiallyChecked state via setCheckState()
    - Observing all three states with the stateChanged signal

Related concepts:
    - TTkK.CheckState.PartiallyChecked
    - checkStatus parameter for explicit initial state
    - setTristate() to toggle tristate mode at runtime
'''

import TermTk as ttk

root = ttk.TTk()

# Standard two-state checkbox for comparison
ttk.TTkLabel(parent=root, pos=(2,1), text="Standard (two-state) checkbox:")
ttk.TTkCheckbox(parent=root, pos=(2,2), text='Two-state')

# Tristate checkbox — cycles Unchecked -> PartiallyChecked -> Checked
ttk.TTkLabel(parent=root, pos=(2,4), text="Tristate checkbox (click to cycle states):")
cb_tri = ttk.TTkCheckbox(parent=root, pos=(2,5), text='Tristate', tristate=True)
label_tri = ttk.TTkLabel(parent=root, pos=(2,6), text=f"state: {cb_tri.checkState()}")

@ttk.pyTTkSlot(ttk.TTkK.CheckState)
def on_tri_changed(state: ttk.TTkK.CheckState) -> None:
    label_tri.setText(f"state: {state}")

cb_tri.stateChanged.connect(on_tri_changed)

# Initially PartiallyChecked via checkStatus parameter
ttk.TTkLabel(parent=root, pos=(2,8), text="Initially PartiallyChecked:")
ttk.TTkCheckbox(parent=root, pos=(2,9), text='Partial', tristate=True,
                checkStatus=ttk.TTkK.PartiallyChecked)

# Programmatically set PartiallyChecked state
ttk.TTkLabel(parent=root, pos=(2,11), text="Set PartiallyChecked via setCheckState():")
cb_prog = ttk.TTkCheckbox(parent=root, pos=(2,12), text='Programmatic', tristate=True)
label_prog = ttk.TTkLabel(parent=root, pos=(2,13), text=f"state: {cb_prog.checkState()}")

btn_partial = ttk.TTkButton(parent=root, pos=(2,14), text='Set Partial', border=True)
btn_checked = ttk.TTkButton(parent=root, pos=(16,14), text='Set Checked', border=True)
btn_unchecked = ttk.TTkButton(parent=root, pos=(30,14), text='Set Unchecked', border=True)

@ttk.pyTTkSlot()
def set_partial() -> None:
    cb_prog.setCheckState(ttk.TTkK.PartiallyChecked)
    label_prog.setText(f"state: {cb_prog.checkState()}")

@ttk.pyTTkSlot()
def set_checked() -> None:
    cb_prog.setCheckState(ttk.TTkK.Checked)
    label_prog.setText(f"state: {cb_prog.checkState()}")

@ttk.pyTTkSlot()
def set_unchecked() -> None:
    cb_prog.setCheckState(ttk.TTkK.Unchecked)
    label_prog.setText(f"state: {cb_prog.checkState()}")

btn_partial.clicked.connect(set_partial)
btn_checked.clicked.connect(set_checked)
btn_unchecked.clicked.connect(set_unchecked)

root.mainloop()
