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

# Those 2 lines are required to use the TermTk library straight from the main folder
import sys, os
sys.path.append(os.path.join(sys.path[0],'../../..'))

import TermTk as ttk

root=ttk.TTk()

btn1 = ttk.TTkButton(parent=root, pos=(5,2), text='Button 1 - unfocussed')
btn2 = ttk.TTkButton(parent=root, pos=(5,3), text='Button 2 - unfocussed')
btn3 = ttk.TTkButton(parent=root, pos=(5,4), text='Button 3 - unfocussed')
btn4 = ttk.TTkButton(parent=root, pos=(5,5), text='Button 4 - focussed')
btn5 = ttk.TTkButton(parent=root, pos=(5,6), text='Button 5 - unfocussed')

# Force the focus on the button 4
btn4.setFocus()

root.mainloop()