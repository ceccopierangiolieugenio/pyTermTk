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
TTkButton - Styling and Customization

This example demonstrates how to customize button appearance with colors and styles.
It shows how to apply styling across different button states and create custom style dictionaries.

Key Features:
    - Observing default, disabled, and focus styling
    - Understanding state-based styling (default, hover, focus, disabled, checked, unchecked)
    - Color combinations with TTkColor: fg(), bg(), and text attributes
    - Creating custom style dictionaries for buttons
    - Combining foreground, background, and text attributes (BOLD, UNDERLINE)
    - Practical custom styling with green and cyan colors

Related concepts:
    - TTkColor for color manipulation
    - Style dictionaries with state keys
    - Theme system and widget appearance
    - Widget state styling and customization
'''

import TermTk as ttk

root = ttk.TTk(mouseTrack=True)

# Display information about button styling
ttk.TTkLabel(parent=root, pos=(2,1), text="Button Styling Information")
ttk.TTkLabel(parent=root, pos=(2,3), text="Button states: default, hover, focus, disabled, checked, unchecked")

# Create buttons showing different themes/styles through the style system
ttk.TTkLabel(parent=root, pos=(2,5), text="Default themed button")
btn_default = ttk.TTkButton(parent=root, pos=(2,6), text='Default Style', border=True)

ttk.TTkLabel(parent=root, pos=(45,5), text="Disabled button (automatic styling)")
btn_disabled = ttk.TTkButton(parent=root, pos=(45,6), text='Disabled', border=True)
btn_disabled.setEnabled(False)

# Create a checkable button showing unchecked/checked state styling
ttk.TTkLabel(parent=root, pos=(2,9), text="Checkable buttons show different styles")
ttk.TTkLabel(parent=root, pos=(2,10), text="Unchecked (click to toggle):")
btn_unchecked = ttk.TTkButton(parent=root, pos=(2,11), text='Toggle', border=True, checkable=True, checked=False)

ttk.TTkLabel(parent=root, pos=(45,10), text="Pre-checked button:")
btn_checked = ttk.TTkButton(parent=root, pos=(45,11), text='Checked', border=True, checkable=True, checked=True)

# Show button with focus styling
ttk.TTkLabel(parent=root, pos=(2,14), text="Focus on this button with Tab key")
ttk.TTkLabel(parent=root, pos=(2,15), text="to see focus style")
btn_focus = ttk.TTkButton(parent=root, pos=(2,16), text='Focusable', border=True)
btn_focus.setFocus()

# Display info about available colors
ttk.TTkLabel(parent=root, pos=(45,14), text="TTkColor provides:")
ttk.TTkLabel(parent=root, pos=(45,15), text="- fg() for foreground color")
ttk.TTkLabel(parent=root, pos=(45,16), text="- bg() for background color")
ttk.TTkLabel(parent=root, pos=(45,17), text="- BOLD, UNDERLINE attributes")

# Create a button with custom style
ttk.TTkLabel(parent=root, pos=(2,20), text="Custom styled button:")
btn_custom = ttk.TTkButton(parent=root, pos=(2,21), text='Custom', border=True)
# Override button style with custom colors
btn_custom.setStyle({
    'default': {
        'color': ttk.TTkColor.fg("#00ff00") + ttk.TTkColor.bg("#001100") + ttk.TTkColor.BOLD,
        'borderColor': ttk.TTkColor.GREEN,
        'grid':2
    },
    'hover': {'color': ttk.TTkColor.BLUE + ttk.TTkColor.STRIKETROUGH},
    'clicked': {
        'color': ttk.TTkColor.RED + ttk.TTkColor.BOLD, 
        'grid':1
    },
})

root.mainloop()
