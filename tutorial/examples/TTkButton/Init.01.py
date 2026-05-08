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
TTkButton - Basic Initialization

This example demonstrates the basic creation and initialization of TTkButton widgets.
It shows different button styles: with and without borders, disabled buttons, and custom sizing.

Key Features:
	- Creating simple buttons with and without borders
	- Disabling buttons using setEnabled()
	- Custom button sizing
	- Positioning buttons in the terminal

Related concepts:
	- border parameter for visual appearance
	- setEnabled() for enabling/disabling interaction
	- size parameter for custom dimensions
'''

import TermTk as ttk

root = ttk.TTk()

ttk.TTkLabel(parent=root, pos=(2,1), text="Button without border")
ttk.TTkButton(parent=root, pos=(2,2), text='Click me!')

ttk.TTkLabel(parent=root, pos=(2,4), text="Button with border")
ttk.TTkButton(parent=root, pos=(2,5), text='Click me!', border=True)

ttk.TTkLabel(parent=root, pos=(2,8), text="Disabled button")
button_disabled = ttk.TTkButton(parent=root, pos=(2,9), text='Disabled', border=True)
button_disabled.setEnabled(False)

ttk.TTkLabel(parent=root, pos=(45,1), text="Button with custom size")
ttk.TTkButton(parent=root, pos=(45,2), size=(15,3), text='Large Button', border=True)

ttk.TTkLabel(parent=root, pos=(45,6), text="Button with max height")
ttk.TTkButton(parent=root, pos=(45,7), text='Button', border=True, maxHeight=3)

root.mainloop()
