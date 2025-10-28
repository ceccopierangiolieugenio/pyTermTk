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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk


def demoColorPicker(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)

    lcol = ttk.TTkLabel(parent=frame, pos=(0,0), text="Test ░▒▓█▁▂▃▄▅▆▇█ Color")
    lfg  = ttk.TTkLabel(parent=frame, pos=(0,1), text="Test ░▒▓█▁▂▃▄▅▆▇█ Color FG")
    lbg  = ttk.TTkLabel(parent=frame, pos=(0,2), text="Test ░▒▓█▁▂▃▄▅▆▇█ Color BG")

    winCP = ttk.TTkWindow(parent=frame,pos = (0,3), size=(30,17), title="Test Color Pickers", border=True)
    ttk.TTkLabel(parent=winCP, pos=( 1,0), text="BG")
    ttk.TTkLabel(parent=winCP, pos=(11,0), text="FG")
    cbp01 = ttk.TTkColorButtonPicker(parent=winCP, pos=( 0, 1), size=(8,3), border=True, color=ttk.TTkColor.bg('#88ffff') )
    cbp02 = ttk.TTkColorButtonPicker(parent=winCP, pos=( 0, 4), size=(8,3), border=True, color=ttk.TTkColor.bg('#ff88ff') ,returnType=ttk.TTkK.ColorPickerReturnType.Default)
    cbp03 = ttk.TTkColorButtonPicker(parent=winCP, pos=( 0, 7), size=(8,3), border=True, color=ttk.TTkColor.fg('#ffff88') ,returnType=ttk.TTkK.ColorPickerReturnType.Background)
    cbp04 = ttk.TTkColorButtonPicker(parent=winCP, pos=( 0,10), size=(8,3), border=True, color=ttk.TTkColor.bg('#8888ff') ,returnType=ttk.TTkK.ColorPickerReturnType.Background)

    cbp05 = ttk.TTkColorButtonPicker(parent=winCP, pos=(10, 1), size=(8,3), border=True, color=ttk.TTkColor.fg('#00ffff') )
    cbp06 = ttk.TTkColorButtonPicker(parent=winCP, pos=(10, 4), size=(8,3), border=True, color=ttk.TTkColor.fg('#ff00ff') ,returnType=ttk.TTkK.ColorPickerReturnType.Default)
    cbp07 = ttk.TTkColorButtonPicker(parent=winCP, pos=(10, 7), size=(8,3), border=True, color=ttk.TTkColor.fg('#ffff00') ,returnType=ttk.TTkK.ColorPickerReturnType.Foreground)
    cbp08 = ttk.TTkColorButtonPicker(parent=winCP, pos=(10,10), size=(8,3), border=True, color=ttk.TTkColor.bg('#0000ff') ,returnType=ttk.TTkK.ColorPickerReturnType.Foreground)

    cbp09 = ttk.TTkColorButtonPicker(parent=winCP, pos=(20, 1), size=(8,3), border=True, color=ttk.TTkColor.fg('#ffffff') ,returnType=ttk.TTkK.ColorPickerReturnType.Foreground)
    cbp10 = ttk.TTkColorButtonPicker(parent=winCP, pos=(20, 4), size=(8,3), border=True, color=ttk.TTkColor.bg('#ffffff') ,returnType=ttk.TTkK.ColorPickerReturnType.Foreground)
    cbp11 = ttk.TTkColorButtonPicker(parent=winCP, pos=(20, 7), size=(8,3), border=True, color=ttk.TTkColor.fg('#ffffff') ,returnType=ttk.TTkK.ColorPickerReturnType.Background)
    cbp12 = ttk.TTkColorButtonPicker(parent=winCP, pos=(20,10), size=(8,3), border=True, color=ttk.TTkColor.bg('#ffffff') ,returnType=ttk.TTkK.ColorPickerReturnType.Background)

    def _register(cbp:ttk.TTkColorButtonPicker):
        cbp.colorSelected.connect(lcol.setColor)
        cbp.colorSelectedFG.connect(lfg.setColor)
        cbp.colorSelectedBG.connect(lbg.setColor)

    for cbp in [cbp01,cbp02,cbp03,cbp04,cbp05,cbp06,cbp07,cbp08,cbp09,cbp10,cbp11,cbp12]:
        _register(cbp)

    # win2_1 = ttk.TTkColorDialogPicker(parent=frame,pos = (3,3), size=(110,40), title="Test Color Picker", border=True)

    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    root = ttk.TTk()
    if args.f:
        root.setLayout(ttk.TTkGridLayout())
        winColor1 = root
    else:
        winColor1 = ttk.TTkWindow(parent=root,pos = (0,0), size=(80,30), title="Test Color Picker", border=True, layout=ttk.TTkGridLayout())

    demoColorPicker(winColor1)

    root.mainloop()

if __name__ == "__main__":
    main()