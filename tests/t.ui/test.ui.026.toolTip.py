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

import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

root = ttk.TTk(title="pyTermTk Demo", mouseTrack=True)

ttk.TTkLabel( parent=root, text="Label 1",  pos=(0,0),  size=(10,1), toolTip="TT Label 1")
ttk.TTkButton(parent=root, text="Button 1", pos=(0,1), size=(10,1),  toolTip="TT Button 1")
ttk.TTkButton(parent=root, text="Button 2", pos=(0,2), size=(10,3),  toolTip="TT Button 2", border=True)
ttk.TTkButton(parent=root, text="Button 3", pos=(0,5), size=(20,3),  toolTip="TT Button 3\n\nNewline", border=True)
ttk.TTkButton(parent=root, text="Button 3", pos=(21,0), size=(20,10), border=True,
    toolTip=
        ttk.TTkString(color=ttk.TTkColor.fg("#ff0000") ,text="   L😎rem ipsum\n")+
        ttk.TTkString(color=ttk.TTkColor.fg("#00ff00") ,text="dolor sit amet,\n ⌚ ❤ 💙 🙋'\nYepp!!!"))

w1 = ttk.TTkWindow(parent=root, title="LOG", pos=(0,10), size=(90,20), layout=ttk.TTkGridLayout(), toolTip="TT Log Window\n  With\nLogDump")
ttk.TTkLogViewer(parent=w1)
w2 = ttk.TTkWindow(parent=root, title="KeyLogger", pos=(0,30), size=(60,7), layout=ttk.TTkGridLayout())
ttk.TTkKeyPressView(parent=w2, toolTip="This is a\nKey Logger Widget")

root.mainloop()