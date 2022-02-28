#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import TermTk as ttk

# Create a root object (it is a widget that represent the terminal)
root = ttk.TTk()

# Create a window and attach it to the root (parent=root)
calculatorWin = ttk.TTkWindow(
    parent=root, pos=(1, 1), size=(30, 17), title="My first Calculator"
)

# Create a grid layout and set it as default for the window
winLayout = ttk.TTkGridLayout()
calculatorWin.setLayout(winLayout)

# Define the Label and attach it to the grid layout at
# Position (Row/Col) (0,0) and (Row/Col)Span (1,4)
# I force the Max Height to 1 in order to avoid this widget to resize vertically
resLabel = ttk.TTkLabel(text="Results", maxHeight=1)
winLayout.addWidget(resLabel, 0, 0, 1, 4)

# Define the Numeric Buttons and attach them to the grid layout
btn1 = ttk.TTkButton(border=True, text="1")
btn2 = ttk.TTkButton(border=True, text="2")
btn3 = ttk.TTkButton(border=True, text="3")
btn4 = ttk.TTkButton(border=True, text="4")
btn5 = ttk.TTkButton(border=True, text="5")
btn6 = ttk.TTkButton(border=True, text="6")
btn7 = ttk.TTkButton(border=True, text="7")
btn8 = ttk.TTkButton(border=True, text="8")
btn9 = ttk.TTkButton(border=True, text="9")

winLayout.addWidget(btn1, 1, 0)  # Colspan/Rowspan are defaulted to 1 if not specified
winLayout.addWidget(btn2, 1, 1)
winLayout.addWidget(btn3, 1, 2)
winLayout.addWidget(btn4, 2, 0)
winLayout.addWidget(btn5, 2, 1)
winLayout.addWidget(btn6, 2, 2)
winLayout.addWidget(btn7, 3, 0)
winLayout.addWidget(btn8, 3, 1)
winLayout.addWidget(btn9, 3, 2)

# Adding the "0" button on the bottom which alignment is
# Position (Row/Col) (4,0) (Row/Col)span (1,2)
# Just to show off I am using another way to attach it to the grid layout
winLayout.addWidget(btn0 := ttk.TTkButton(border=True, text="0"), 4, 0, 1, 2)

# Define the 2 algebric buttons
winLayout.addWidget(btnAdd := ttk.TTkButton(border=True, text="+"), 1, 3)
winLayout.addWidget(btnSub := ttk.TTkButton(border=True, text="-"), 2, 3)

# The Enter "=" button (2 rows wide)
winLayout.addWidget(btnRes := ttk.TTkButton(border=True, text="="), 3, 3, 2, 1)

# Last but not least an extrabutton just for fun
winLayout.addWidget(mysteryButton := ttk.TTkButton(border=True, text="?"), 4, 2)

# Start the Main loop
root.mainloop()
