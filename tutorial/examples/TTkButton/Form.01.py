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
sys.path.append(os.path.join(sys.path[0],'../../..'))
##########

'''
TTkButton - Buttons in Form Context

This example demonstrates how to use buttons in a realistic form scenario.
It shows buttons integrated with other widgets for practical user interactions.

Key Features:
  - Buttons in form layouts
  - Submit/Cancel button patterns
  - Button click actions affecting other widgets
  - Form validation feedback
  - Multi-widget event handling

Related concepts:
  - Form patterns
  - Widget interaction
  - User input processing
  - Dialog-like interfaces
'''

import TermTk as ttk

root = ttk.TTk()

# Create a simple form
ttk.TTkLabel(parent=root, pos=(2,1), text="Simple Form Example")

# Input fields
ttk.TTkLabel(parent=root, pos=(2,3), text="Name:")
name_input = ttk.TTkLineEdit(parent=root, pos=(10,3), size=(20,1))

ttk.TTkLabel(parent=root, pos=(2,5), text="Email:")
email_input = ttk.TTkLineEdit(parent=root, pos=(10,5), size=(20,1))

ttk.TTkLabel(parent=root, pos=(2,7), text="Subscribe:")
subscribe_checkbox = ttk.TTkCheckBox(parent=root, pos=(13,7), text="Yes", size=(6,1))

# Result label
result_label = ttk.TTkLabel(parent=root, pos=(2,13), text="Form Status: Ready")

# Submit button
submit_button = ttk.TTkButton(parent=root, pos=(10,9), text='Submit', border=True, maxHeight=3)

# Clear button
clear_button = ttk.TTkButton(parent=root, pos=(22,9), text='Clear', border=True, maxHeight=3)

# Cancel button
cancel_button = ttk.TTkButton(parent=root, pos=(32,9), text='Cancel', border=True, maxHeight=3)

# Form handlers
@ttk.pyTTkSlot()
def on_submit():
    name = name_input.text()
    email = email_input.text()
    subscribed = subscribe_checkbox.isChecked()
    
    if not name or not email:
        result_label.setText("Form Status: Please fill all fields!")
    else:
        status = f"Form Status: Submitted! Name={name}, Email={email}, Subscribe={subscribed}"
        result_label.setText(status)

@ttk.pyTTkSlot()
def on_clear():
    name_input.setText("")
    email_input.setText("")
    subscribe_checkbox.setChecked(False)
    result_label.setText("Form Status: Cleared")

@ttk.pyTTkSlot()
def on_cancel():
    result_label.setText("Form Status: Cancelled")
    name_input.setText("")
    email_input.setText("")

# Connect button signals
submit_button.clicked.connect(on_submit)
clear_button.clicked.connect(on_clear)
cancel_button.clicked.connect(on_cancel)

root.mainloop()
