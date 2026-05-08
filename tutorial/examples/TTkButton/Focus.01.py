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
TTkButton - Focus and Keyboard Navigation

This example demonstrates keyboard focus handling and navigation between buttons.
It shows how buttons respond to Tab, Enter, and Space key events.

Key Features:
  - Focus policy and setFocusPolicy()
  - Tab navigation between buttons
  - Keyboard activation (Space and Enter keys)
  - Focus events (focusInEvent, focusOutEvent)
  - Visual feedback when a button has focus

Related concepts:
  - TTkK.ClickFocus, TTkK.TabFocus
  - Focus chain and widget navigation
  - Keyboard input handling
  - Focus visual indicators
'''

import TermTk as ttk

root = ttk.TTk()

# Display focus instructions
ttk.TTkLabel(parent=root, pos=(2,1), text="Keyboard Navigation with TTkButton")
ttk.TTkLabel(parent=root, pos=(2,3), text="Instructions:")
ttk.TTkLabel(parent=root, pos=(2,4), text="  - Use Tab/Shift+Tab to navigate between buttons")
ttk.TTkLabel(parent=root, pos=(2,5), text="  - Press Space or Enter to activate focused button")
ttk.TTkLabel(parent=root, pos=(2,6), text="  - Click button to focus it (ClickFocus)")

# Status label to show focus/click info
status_label = ttk.TTkLabel(parent=root, pos=(2,8), text="Status: Ready")

# Create buttons in a row for Tab navigation
ttk.TTkLabel(parent=root, pos=(2,10), text="Tab through these buttons:")

btn1 = ttk.TTkButton(parent=root, pos=(2,11), text='Button 1', border=True)
btn2 = ttk.TTkButton(parent=root, pos=(14,11), text='Button 2', border=True)
btn3 = ttk.TTkButton(parent=root, pos=(26,11), text='Button 3', border=True)

# Set focus policies (default is already ClickFocus + TabFocus for buttons)
btn1.setFocusPolicy(ttk.TTkK.ClickFocus | ttk.TTkK.TabFocus)
btn2.setFocusPolicy(ttk.TTkK.ClickFocus | ttk.TTkK.TabFocus)
btn3.setFocusPolicy(ttk.TTkK.ClickFocus | ttk.TTkK.TabFocus)

# Create signal handlers
@ttk.pyTTkSlot()
def on_btn1_click():
    status_label.setText("Status: Button 1 activated (by click or keyboard)")

@ttk.pyTTkSlot()
def on_btn2_click():
    status_label.setText("Status: Button 2 activated (by click or keyboard)")

@ttk.pyTTkSlot()
def on_btn3_click():
    status_label.setText("Status: Button 3 activated (by click or keyboard)")

# Connect signals
btn1.clicked.connect(on_btn1_click)
btn2.clicked.connect(on_btn2_click)
btn3.clicked.connect(on_btn3_click)

# Show focus chain information
ttk.TTkLabel(parent=root, pos=(2,14), text="Focus Information:")
ttk.TTkLabel(parent=root, pos=(2,15), text="  - Colored border indicates focused widget")
ttk.TTkLabel(parent=root, pos=(2,16), text="  - Use Tab to move focus to next button in order")
ttk.TTkLabel(parent=root, pos=(2,17), text="  - Use Shift+Tab to move focus to previous button")

root.mainloop()
