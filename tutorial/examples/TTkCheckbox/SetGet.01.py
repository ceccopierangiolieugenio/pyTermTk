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
TTkCheckbox - Set/Get API

This example demonstrates the programmatic set/get API of TTkCheckbox.
It shows how to read and write the checkbox state and label text at runtime.

Key Features:
    - Reading the label with text()
    - Updating the label with setText()
    - Reading checked state with isChecked()
    - Toggling checked state with setChecked()
    - Reading raw CheckState with checkState()
    - Setting raw CheckState with setCheckState()

Related concepts:
    - TTkK.CheckState enum (Checked / Unchecked)
    - Programmatic state control without signals
'''

import TermTk as ttk

root = ttk.TTk()

# --- text() / setText() ---
ttk.TTkLabel(parent=root, pos=(2,1), text="text() / setText()")
cb_text = ttk.TTkCheckbox(parent=root, pos=(2,2), text='Original label')
label_text = ttk.TTkLabel(parent=root, pos=(2,3), text=f"text(): '{cb_text.text()}'")

btn_rename = ttk.TTkButton(parent=root, pos=(2,4), text='Rename label', border=True)

@ttk.pyTTkSlot()
def rename_label():
    cb_text.setText('Renamed label')
    label_text.setText(f"text(): '{cb_text.text()}'")

btn_rename.clicked.connect(rename_label)

# --- isChecked() / setChecked() ---
ttk.TTkLabel(parent=root, pos=(30,1), text="isChecked() / setChecked()")
cb_state = ttk.TTkCheckbox(parent=root, pos=(30,2), text='Toggle me', checked=True)
label_state = ttk.TTkLabel(parent=root, pos=(30,3), text=f"isChecked(): {cb_state.isChecked()}")

btn_toggle = ttk.TTkButton(parent=root, pos=(30,4), text='Toggle via setChecked()', border=True)

@ttk.pyTTkSlot()
def toggle_checked():
    cb_state.setChecked(not cb_state.isChecked())
    label_state.setText(f"isChecked(): {cb_state.isChecked()}")

btn_toggle.clicked.connect(toggle_checked)

# --- checkState() / setCheckState() ---
ttk.TTkLabel(parent=root, pos=(2,7), text="checkState() / setCheckState()")
cb_raw = ttk.TTkCheckbox(parent=root, pos=(2,8), text='Raw state')
label_raw = ttk.TTkLabel(parent=root, pos=(2,9), text=f"checkState(): {cb_raw.checkState()}")

btn_check = ttk.TTkButton(parent=root, pos=(2,10), text='Set Checked', border=True)
btn_uncheck = ttk.TTkButton(parent=root, pos=(16,10), text='Set Unchecked', border=True)

@ttk.pyTTkSlot()
def set_checked():
    cb_raw.setCheckState(ttk.TTkK.Checked)
    label_raw.setText(f"checkState(): {cb_raw.checkState()}")

@ttk.pyTTkSlot()
def set_unchecked():
    cb_raw.setCheckState(ttk.TTkK.Unchecked)
    label_raw.setText(f"checkState(): {cb_raw.checkState()}")

btn_check.clicked.connect(set_checked)
btn_uncheck.clicked.connect(set_unchecked)

root.mainloop()
