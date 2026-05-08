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
TTkButton - Layout Management with Grid

This example demonstrates how to organize buttons within a TTkGridLayout.
It shows buttons arranged in a grid pattern with varying heights, all contained in a framed container.

Key Features:
    - Using TTkGridLayout to arrange buttons in rows and columns
    - Button positioning with addWidget(widget, row, col)
    - Varying button heights using maxHeight parameter
    - Container widgets (TTkFrame) for layout management
    - Connecting buttons from a layout to a shared signal handler

Related concepts:
    - TTkLayout and grid-based positioning
    - TTkFrame and container organization
    - Widget sizing with maxHeight
'''

import TermTk as ttk

root = ttk.TTk()

# Create a frame to hold the buttons
frame = ttk.TTkFrame(parent=root, pos=(2,1), size=(40,15), border=True, title="Button Layout Example")

# Create a grid layout
layout = ttk.TTkGridLayout()

frame.setLayout(layout)

# Add a status label
status_label = ttk.TTkLabel(parent=root, pos=(2,17), text="Status: Ready")

# Connect buttons to status updates
@ttk.pyTTkSlot()
def on_any_button_click():
    status_label.setText("Status: Button clicked from layout!")

# Add buttons in a grid pattern
buttons = [
    ('Button 1', 0, 0, 3),
    ('Button 2', 0, 1, 3),
    ('Button 3', 0, 2, 3),
    ('Button 4', 1, 0, 10),
    ('Button 5', 1, 1, 10),
    ('Button 6', 1, 2, 10),
]

for text, row, col, maxHeight in buttons:
    btn = ttk.TTkButton(text=text, border=True, maxHeight=maxHeight)
    btn.clicked.connect(on_any_button_click)
    layout.addWidget(btn, row, col)

root.mainloop()
