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
TTkButton - Getting and Setting Text

This example demonstrates how to get and set the text property of TTkButton widgets.
It shows how to retrieve the current text and dynamically update it at runtime.

Key Features:
	- Getting button text with text()
	- Setting button text with setText()
	- Checking button properties with border()
	- Dynamic text updates triggered by button clicks

Related concepts:
	- TTkString and text handling
	- Property getters and setters
	- Widget state inspection
'''

import TermTk as ttk

root = ttk.TTk()

# Create a button with initial text
ttk.TTkLabel(parent=root, pos=(2,1), text="Getting button text")
btn1 = ttk.TTkButton(parent=root, pos=(2,2), text='Original Text', border=True)

# Display the current text
ttk.TTkLabel(parent=root, pos=(2,5), text=f"Button text: {btn1.text()}")

# Create a button and change its text
ttk.TTkLabel(parent=root, pos=(2,6), text="Setting button text")
btn2 = ttk.TTkButton(parent=root, pos=(2,7), text='Click Me', border=True)
btn2.setText('Text Changed!')

# Display the updated text
ttk.TTkLabel(parent=root, pos=(2,10), text=f"New button text: {btn2.text()}")

# Check if button has border
ttk.TTkLabel(parent=root, pos=(45,1), text="Checking button properties")
btn3 = ttk.TTkButton(parent=root, pos=(45,2), text='No Border Button')
ttk.TTkLabel(parent=root, pos=(45,5), text=f"Has border: {btn3.border()}")

btn4 = ttk.TTkButton(parent=root, pos=(45,6), text='Border Button', border=True)
ttk.TTkLabel(parent=root, pos=(45,9), text=f"Has border: {btn4.border()}")

root.mainloop()

root.mainloop()
