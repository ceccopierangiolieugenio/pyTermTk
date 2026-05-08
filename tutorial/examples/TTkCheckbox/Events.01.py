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
TTkCheckbox - Signal and Event Handling

This example demonstrates how to connect TTkCheckbox signals to slot functions.
It covers the three signals emitted by the checkbox: toggled, stateChanged, and clicked.

Key Features:
    - Connecting to the toggled signal (bool)
    - Connecting to the stateChanged signal (TTkK.CheckState)
    - Connecting to the clicked signal
    - Using @pyTTkSlot decorator for type-safe slots
    - Tracking event counts to observe signal emission order

Related concepts:
    - pyTTkSignal / pyTTkSlot type-safe patterns
    - Difference between toggled (bool) and stateChanged (CheckState)
    - Signal connection and emission
'''

import TermTk as ttk

root = ttk.TTk()

# --- toggled signal ---
ttk.TTkLabel(parent=root, pos=(2,1), text="toggled(bool) signal")
cb_toggled = ttk.TTkCheckbox(parent=root, pos=(2,2), text='Check me')
label_toggled = ttk.TTkLabel(parent=root, pos=(2,3), text="toggled: (not fired yet)")

@ttk.pyTTkSlot(bool)
def on_toggled(checked: bool) -> None:
    label_toggled.setText(f"toggled: checked={checked}")

cb_toggled.toggled.connect(on_toggled)

# --- stateChanged signal ---
ttk.TTkLabel(parent=root, pos=(2,5), text="stateChanged(CheckState) signal")
cb_state = ttk.TTkCheckbox(parent=root, pos=(2,6), text='Check me', tristate=True)
label_state = ttk.TTkLabel(parent=root, pos=(2,7), text="stateChanged: (not fired yet)")

@ttk.pyTTkSlot(ttk.TTkK.CheckState)
def on_state_changed(state: ttk.TTkK.CheckState) -> None:
    label_state.setText(f"stateChanged: state={state}")

cb_state.stateChanged.connect(on_state_changed)

# --- clicked signal ---
ttk.TTkLabel(parent=root, pos=(2,9), text="clicked() signal")
cb_clicked = ttk.TTkCheckbox(parent=root, pos=(2,10), text='Check me')
label_clicked = ttk.TTkLabel(parent=root, pos=(2,11), text="clicked: (not fired yet)")

click_count = 0

@ttk.pyTTkSlot(bool)
def on_clicked(checked: bool) -> None:
    global click_count
    click_count += 1
    label_clicked.setText(f"clicked: count={click_count}, checked={checked}")

cb_clicked.clicked.connect(on_clicked)

root.mainloop()
