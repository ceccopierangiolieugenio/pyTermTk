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

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()
root.setLayout(ttk.TTkHBoxLayout())

ttk.TTkTestWidget(parent=root,border=True, maxWidth=52)
rightframe = ttk.TTkFrame(parent=root, border=True, title="V Box Layout", titleColor=ttk.TTkColor.BOLD+ttk.TTkColor.fg('#8888dd'))
rightframe.setLayout(ttk.TTkVBoxLayout())

gridFrame = ttk.TTkFrame(parent=rightframe, border=True, title="Grid Layout", titleColor=ttk.TTkColor.fg('#88dd88'))
gridFrame.setLayout(ttk.TTkGridLayout())
ttk.TTkButton(parent=gridFrame, border=True, text="Button1")
ttk.TTkButton(parent=gridFrame, border=True, text="Button2")
gridFrame.layout().addWidget(ttk.TTkButton(border=True, text="Button (1,0)"),1,0)
ttk.TTkButton(parent=gridFrame, border=True, text="Button4")
gridFrame.layout().addWidget(ttk.TTkButton(border=True, text="Button (0,3)"),0,3)
gridFrame.layout().addWidget(ttk.TTkButton(border=True, text="Button (1,2)"),1,2)
# Test (add a widget to the same parent with a different layout params than the default)
gridFrame.layout().addWidget(ttk.TTkButton(parent=gridFrame, border=True, text="Button (2,1)"),2,1)
gridFrame.layout().addWidget(ttk.TTkButton(border=True, text="Button (5,5)"),5,5)

gridFrame.layout().addWidget(ttk.TTkFrame(border=True,title="Frame1"),0,5)
gridFrame.layout().addWidget(ttk.TTkFrame(border=True,title="Frame2"),2,3)
gridFrame.layout().addWidget(ttk.TTkFrame(border=True,title="Frame3"),5,3)
gridFrame.layout().addWidget(ttk.TTkFrame(border=True,title="Frame4"),5,1)


centerrightframe=ttk.TTkFrame(parent=rightframe, border=True, title="H Box Layout", titleColor=ttk.TTkColor.fg('#dd88dd'))
centerrightframe.setLayout(ttk.TTkHBoxLayout())
ttk.TTkTestWidget(parent=rightframe, border=True, title="Test Widget", titleColor=ttk.TTkColor.fg('#dddddd'))


smallframe = ttk.TTkFrame(parent=centerrightframe, border=True)
# smallframe.setLayout(ttk.TTkVBoxLayout())
ttk.TTkTestWidget(parent=centerrightframe, border=True)
ttk.TTkFrame(parent=centerrightframe, border=True)

ttk.TTkButton(parent=smallframe, x=3, y=1, width=20, height=1, text=" Ui.003 Button")
ttk.TTkTestWidget(parent=smallframe, x=3, y=2, width=50, height=8, border=True)
ttk.TTkTestWidget(parent=smallframe, x=-5, y=12, width=50, height=15, border=True)

root.mainloop()