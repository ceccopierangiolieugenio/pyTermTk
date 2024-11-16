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

def demoTextPicker(root=None):
    frame = ttk.TTkFrame(
        parent=root, border=False,
        addStyle={'default':{'fillColor':ttk.TTkColor.bg('#004400', modifier=ttk.TTkColorGradient(increment=-6))}})

    ttk.TTkLabel(parent=frame, pos=(0,0),text="[ No Autosize ]")
    ttk.TTkTextPicker(parent=frame, pos=( 0,1), size=(20, 1),autoSize=False, multiLine=False)
    ttk.TTkLabel(parent=frame, pos=(0,2),text="[ Multiline ]")
    ttk.TTkTextPicker(parent=frame, pos=( 0,3), size=(20, 1),autoSize=False, multiLine=True)
    ttk.TTkLabel(parent=frame, pos=(0,4),text="[ Autosize ]")
    ttk.TTkTextPicker(parent=frame, pos=( 0,5), size=(20, 1),autoSize=True, multiLine=True)

    ttk.TTkTextPicker(parent=frame, pos=(25,0), size=(20, 5),autoSize=True, multiLine=True)
    ttk.TTkTextPicker(parent=frame, pos=(50,0), size=(20,10),autoSize=True, multiLine=True)

    return frame


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkTheme.loadTheme(ttk.TTkTheme.NERD)

    root = ttk.TTk()
    if args.f:
        root.setLayout(ttk.TTkGridLayout())
        winColor1 = root
    else:
        winColor1 = ttk.TTkWindow(parent=root,pos = (0,0), size=(58,20), title="Test Text Picker", border=True, layout=ttk.TTkGridLayout())

    demoTextPicker(winColor1)

    winKP = ttk.TTkWindow(parent=root,pos = (5,25), size=(85,7), title="Captured Input")
    winKP.setLayout(ttk.TTkHBoxLayout())
    ttk.TTkKeyPressView(parent=winKP)

    root.mainloop()

if __name__ == "__main__":
    main()