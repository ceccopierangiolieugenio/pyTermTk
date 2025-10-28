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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()

win1 = ttk.TTkWindow(parent=root,pos = (1,1), size=(100,50), title="Test Window 1", border=True)
win1.setLayout(ttk.TTkVBoxLayout())
ttk.TTkButton(parent=win1, border=True, text="BUTTON")
ttk.TTkLabel(parent=win1, text="Test Label 1")
ttk.TTkLabel(parent=win1, text="Test Label 2 Bold", color=ttk.TTkColor.BOLD)
ttk.TTkLabel(parent=win1, text="Test Label 3 Italic", color=ttk.TTkColor.ITALIC)
ttk.TTkLabel(parent=win1, text="Test Label 4 Underline", color=ttk.TTkColor.UNDERLINE)
ttk.TTkLabel(parent=win1, text="Test Label 5 StrikeTrough", color=ttk.TTkColor.STRIKETROUGH)
ttk.TTkLabel(parent=win1, text="Test Label 6 Mix", color=ttk.TTkColor.BOLD+ttk.TTkColor.ITALIC+ttk.TTkColor.UNDERLINE)
ttk.TTkLabel(parent=win1, text="Test Label 7")
ttk.TTkLabel(parent=win1, text="Test Very Long Label 8 - abcdefghihjlmno")
ttk.TTkLabel(parent=win1, text="Test Label 9")
ttk.TTkLabel(parent=win1, text="Test Label 10")
ttk.TTkLabel(parent=win1, text="Test Label 11")
ttk.TTkLabel(parent=win1, text="Test Label 12")
ttk.TTkLabel(parent=win1, text="Test Label 13")


root.mainloop()