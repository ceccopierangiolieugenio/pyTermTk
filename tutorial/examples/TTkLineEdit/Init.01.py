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

import TermTk as ttk

root=ttk.TTk()

ttk.TTkLabel(   parent=root, pos=(2,1), text="No Input Type (default to Text)")
ttk.TTkLineEdit(parent=root, pos=(2,2), size=(20,1), text='Test Input 123')

ttk.TTkLabel(   parent=root, pos=(2,4), text="inputType = Input_Text")
ttk.TTkLineEdit(parent=root, pos=(2,5), size=(20,1), text='Test Input 123', inputType=ttk.TTkK.Input_Text)

ttk.TTkLabel(   parent=root, pos=(2,7), text="inputType = Input_Number")
ttk.TTkLineEdit(parent=root, pos=(2,8), size=(20,1), text='Test Input 123', inputType=ttk.TTkK.Input_Number)
ttk.TTkLineEdit(parent=root, pos=(2,9), size=(20,1), text='123',            inputType=ttk.TTkK.Input_Number)

ttk.TTkLabel(   parent=root, pos=(2,11), text="inputType = Input_Text | Input_Password")
ttk.TTkLineEdit(parent=root, pos=(2,12), size=(20,1), text='Test Input 123', inputType=ttk.TTkK.Input_Text|ttk.TTkK.Input_Password)

ttk.TTkLabel(   parent=root, pos=(2,14), text="inputType = Input_Number | Input_Password")
ttk.TTkLineEdit(parent=root, pos=(2,15), size=(20,1), text='Test Input 123', inputType=ttk.TTkK.Input_Number|ttk.TTkK.Input_Password)
ttk.TTkLineEdit(parent=root, pos=(2,16), size=(20,1), text='123',            inputType=ttk.TTkK.Input_Number|ttk.TTkK.Input_Password)

root.mainloop()