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

import sys, os, argparse

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk


def demoColorPicker(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)

    winCP = ttk.TTkWindow(parent=frame,pos = (0,0), size=(30,16), title="Test Color Pickers", border=True)
    ttk.TTkColorButtonPicker(parent=winCP, pos=(1,3),  size=(8,3), border=True, color=ttk.TTkColor.bg('#88ffff') )
    ttk.TTkColorButtonPicker(parent=winCP, pos=(1,6),  size=(8,3), border=True, color=ttk.TTkColor.bg('#ff88ff') )
    ttk.TTkColorButtonPicker(parent=winCP, pos=(1,9),  size=(8,3), border=True, color=ttk.TTkColor.bg('#ffff88') )
    ttk.TTkColorButtonPicker(parent=winCP, pos=(1,12), size=(8,3), border=True, color=ttk.TTkColor.bg('#8888ff') )
    ttk.TTkColorButtonPicker(parent=winCP, pos=(11,3), size=(8,3), border=True, color=ttk.TTkColor.fg('#00ffff') )
    ttk.TTkColorButtonPicker(parent=winCP, pos=(11,6), size=(8,3), border=True, color=ttk.TTkColor.fg('#ff00ff') )
    ttk.TTkColorButtonPicker(parent=winCP, pos=(11,9), size=(8,3), border=True, color=ttk.TTkColor.fg('#ffff00') )
    ttk.TTkColorButtonPicker(parent=winCP, pos=(11,12),size=(8,3), border=True, color=ttk.TTkColor.fg('#0000ff') )
    ttk.TTkColorButtonPicker(parent=winCP, pos=(21,3), size=(8,3), border=True, color=ttk.TTkColor.bg('#ffffff') )
    ttk.TTkColorButtonPicker(parent=winCP, pos=(21,6), size=(8,3), border=True, color=ttk.TTkColor.bg('#ffffff') )
    ttk.TTkColorButtonPicker(parent=winCP, pos=(21,9), size=(8,3), border=True, color=ttk.TTkColor.bg('#ffffff') )
    ttk.TTkColorButtonPicker(parent=winCP, pos=(21,12),size=(8,3), border=True, color=ttk.TTkColor.bg('#ffffff') )


    # win2_1 = ttk.TTkColorDialogPicker(parent=frame,pos = (3,3), size=(110,40), title="Test Color Picker", border=True)

    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if args.f:
        root.setLayout(ttk.TTkGridLayout())
        winColor1 = root
    else:
        winColor1 = ttk.TTkWindow(parent=root,pos = (0,0), size=(120,50), title="Test Color Picker", border=True, layout=ttk.TTkGridLayout())

    demoColorPicker(winColor1)

    root.mainloop()

if __name__ == "__main__":
    main()