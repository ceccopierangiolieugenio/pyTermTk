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
TTkButton - Signal and Event Handling

This example demonstrates how to connect button signals to slot functions.
It shows the clicked signal and the toggled signal for checkable buttons.

Key Features:
    - Connecting to the clicked signal
    - Handling clicked events with @pyTTkSlot() decorator
    - Connecting to the toggled signal for checkable buttons
    - Maintaining state across multiple events
    - Type-safe signal-slot patterns

Related concepts:
    - pyTTkSignal and pyTTkSlot decorators
    - Signal emission and connection
    - Event-driven programming
'''

import TermTk as ttk

root = ttk.TTk()

# Create a label to display the status
status_label = ttk.TTkLabel(parent=root, pos=(2,1), text="Status: Not clicked yet")

# Create a button and connect it to the clicked signal
ttk.TTkLabel(parent=root, pos=(2,3), text="Simple button click event")
btn1 = ttk.TTkButton(parent=root, pos=(2,4), text='Click Me', border=True)

click_count = 0
@ttk.pyTTkSlot()
def on_click():
    global click_count
    click_count += 1
    status_label.setText(f"Status: Button clicked {click_count} times")

btn1.clicked.connect(on_click)

# Create a label to display the button state
state_label = ttk.TTkLabel(parent=root, pos=(45,1), text="State: Unchecked")

# Create a checkable button
ttk.TTkLabel(parent=root, pos=(45,3), text="Checkable button")
btn2 = ttk.TTkButton(parent=root, pos=(45,4), text='Toggle', border=True, checkable=True)

@ttk.pyTTkSlot(bool)
def on_toggled(checked):
    state_label.setText(f"State: {'Checked' if checked else 'Unchecked'}")

btn2.toggled.connect(on_toggled)

root.mainloop()
