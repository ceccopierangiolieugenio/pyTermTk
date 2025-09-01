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


def demoFilePicker(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)

    # winFP = ttk.TTkWindow(parent=frame,pos = (0,0), size=(20,10), title="Test File Pickers", border=True)
    btn1 = ttk.TTkButton( parent=frame, pos=(0,0),  border=True, text='File' )
    btn2 = ttk.TTkButton( parent=frame, pos=(8,0),  border=True, text='Directory' )
    btn3 = ttk.TTkButton( parent=frame, pos=(21,0), border=True, text='Existing File')
    btn4 = ttk.TTkButton( parent=frame, pos=(38,0), border=True, text='Existing Files', enabled=False )
    label = ttk.TTkLabel(parent=frame,  pos=(1,5),  text="...")


    def _showDialog(fm):
        filePicker = ttk.TTkFileDialogPicker(pos = (3,3), size=(75,24), caption="Pick Something", path=".", fileMode=fm ,filter="All Files (*);;Python Files (*.py);;Bash scripts (*.sh);;Markdown Files (*.md)")
        filePicker.pathPicked.connect(label.setText)
        ttk.TTkHelper.overlay(frame, filePicker, 2, 1, True)

    btn1.clicked.connect(lambda : _showDialog(ttk.TTkK.FileMode.AnyFile))
    btn2.clicked.connect(lambda : _showDialog(ttk.TTkK.FileMode.Directory))
    btn3.clicked.connect(lambda : _showDialog(ttk.TTkK.FileMode.ExistingFile))

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
        winColor1 = ttk.TTkWindow(parent=root,pos = (0,0), size=(58,20), title="Test File/Folder Picker", border=True, layout=ttk.TTkGridLayout())

    demoFilePicker(winColor1)

    root.mainloop()

if __name__ == "__main__":
    main()