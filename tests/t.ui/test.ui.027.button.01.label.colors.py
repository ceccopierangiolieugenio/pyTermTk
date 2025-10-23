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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

root = ttk.TTk(title="pyTermTk Demo", mouseTrack=True)

ttk.TTkButton(parent=root, text="Button 1",          pos=(0,1))
ttk.TTkButton(parent=root, text="Button 2\nNewline", pos=(0,3))
ttk.TTkButton(parent=root, text="Button 2.2\nNewline\n  New Line",
                                                     pos=(0,7))
ttk.TTkButton(parent=root, text="Button 2.3\nNewline\n  New Line\n NL",
                                                     pos=(0,11))

ttk.TTkButton(parent=root, text="Button 3\nNewline", pos=(15,10), border=True)

ttk.TTkButton(parent=root, text="Button 4\n" +
                ttk.TTkString(color=ttk.TTkColor.fg("#ff0000") ,text="   L😎rem ipsum\n")+
                ttk.TTkString(color=ttk.TTkColor.fg("#00ff00") ,text="dolor sit amet,\n ⌚ ❤ 💙 🙋'\nYepp!!!"),
                                                     pos=(15,1), border=True)

ttk.TTkButton(parent=root, text="Button 5\n" +
                ttk.TTkString(color=ttk.TTkColor.fg("#ff0000") ,text="   L😎rem ipsum\n")+
                ttk.TTkString(color=ttk.TTkColor.fg("#00ff00") ,text="dolor sit amet,\n ⌚ ❤ 💙 🙋'\nYepp!!!"),
                                                     pos=(35,1), size=(20,10), border=True)

w = ttk.TTkWindow(parent=root, pos=(30,12), size=(20,11), layout=ttk.TTkGridLayout())
w.addWidget(ttk.TTkButton(text="Button 5\n" +
                ttk.TTkString(color=ttk.TTkColor.fg("#ff0000") ,text="   L😎rem ipsum\n")+
                ttk.TTkString(color=ttk.TTkColor.fg("#00ff00") ,text="dolor sit amet,\n ⌚ ❤ 💙 🙋'\nYepp!!!"),
                                                     pos=(35,1), size=(20,10), border=True, checkable=True ))


root.mainloop()