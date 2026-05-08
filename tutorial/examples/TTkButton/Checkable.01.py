#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
TTkButton - Checkable Buttons and Toggle States

This example demonstrates how to create and manage checkable buttons with toggle states.
It shows how to set initial state, listen to state changes, and control the checkable property.

Key Features:
    - Creating checkable buttons with checkable=True parameter
    - Setting initial checked state with checked parameter
    - Getting checked state with isChecked()
    - Setting checked state with setChecked()
    - Dynamic property changes with setCheckable()
    - Handling the toggled signal with boolean parameter

Related concepts:
    - Binary state widgets (checked/unchecked)
    - State change notifications
    - Toggle functionality
'''

import TermTk as ttk

root = ttk.TTk()

# Left column: non-checkable and checkable examples
ttk.TTkLabel(parent=root, pos=(2,1), text="Non-checkable button (checkable=False)")
btn_not_checkable = ttk.TTkButton(parent=root, pos=(2,2), text='Click', border=True, checkable=False)

ttk.TTkLabel(parent=root, pos=(2,5), text="Checkable button (checkable=True)")
btn_checkable = ttk.TTkButton(parent=root, pos=(2,6), text='Check Me', border=True, checkable=True)

ttk.TTkLabel(parent=root, pos=(2,9), text="Initially checked button")
btn_checked = ttk.TTkButton(parent=root, pos=(2,10), text='Checked', border=True, checkable=True, checked=True)

# Right column: state management and dynamic properties
ttk.TTkLabel(parent=root, pos=(45,1), text="Get/Set checked state")
btn_state = ttk.TTkButton(parent=root, pos=(45,2), text='Toggle', border=True, checkable=True)
state_label = ttk.TTkLabel(parent=root, pos=(45,5), text=f"Checked: {btn_state.isChecked()}")

@ttk.pyTTkSlot(bool)
def update_state(checked):
    state_label.setText(f"Checked: {checked}")

btn_state.toggled.connect(update_state)

ttk.TTkLabel(parent=root, pos=(45,8), text="Change checkable property")
btn_toggle_checkable = ttk.TTkButton(parent=root, pos=(45,9), text='Button', border=True)
toggle_msg = ttk.TTkLabel(parent=root, pos=(45,12), text="")

@ttk.pyTTkSlot()
def toggle_checkable():
    btn_toggle_checkable.setCheckable(True)
    toggle_msg.setText("Now checkable!")

btn_toggle_checkable.clicked.connect(toggle_checkable)

root.mainloop()
