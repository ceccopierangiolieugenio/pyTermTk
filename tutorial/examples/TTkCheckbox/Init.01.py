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
TTkCheckbox - Basic Initialization

This example demonstrates the basic creation and initialization of TTkCheckbox widgets.
It shows checkboxes with different initial states and a disabled checkbox.

Key Features:
    - Creating a basic checkbox with a label
    - Setting initial checked state with checked=True
    - Disabling a checkbox using setEnabled(False)
    - Minimal sizing based on text length

Related concepts:
    - text parameter for checkbox label
    - checked parameter for initial state
    - setEnabled() for disabling interaction
'''

import TermTk as ttk

root = ttk.TTk()

ttk.TTkLabel(parent=root, pos=(2,1), text="Unchecked checkbox (default)")
ttk.TTkCheckbox(parent=root, pos=(2,2), text='Option A')

ttk.TTkLabel(parent=root, pos=(2,4), text="Checked checkbox")
ttk.TTkCheckbox(parent=root, pos=(2,5), text='Option B', checked=True)

ttk.TTkLabel(parent=root, pos=(2,7), text="Disabled unchecked")
cb_dis1 = ttk.TTkCheckbox(parent=root, pos=(2,8), text='Disabled')
cb_dis1.setEnabled(False)

ttk.TTkLabel(parent=root, pos=(2,10), text="Disabled checked")
cb_dis2 = ttk.TTkCheckbox(parent=root, pos=(2,11), text='Disabled checked', checked=True)
cb_dis2.setEnabled(False)

root.mainloop()
