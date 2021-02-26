#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os
import random

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()
win_form1 = ttk.TTkWindow(parent=root,pos=(1,1), size=(60,30), title="Test Window 1", border=True)

ttk.TTkButton(parent=win_form1, pos=(1,3), size=(15,1), text='Button 1')
ttk.TTkButton(parent=win_form1, pos=(1,4), size=(15,1), text='Button 2')

ttk.TTkLineEdit(parent=win_form1, pos=(1,5), size=(20,1), text='Line Edit Test 1')
ttk.TTkLineEdit(parent=win_form1, pos=(1,6), size=(50,1), text='Line Edit Test 2')
ttk.TTkLineEdit(parent=win_form1, pos=(1,7), size=(50,1), text='Line Edit Test 3')
ttk.TTkLineEdit(parent=win_form1, pos=(1,8), size=(50,1), text='Line Edit Test 4')

root.mainloop()