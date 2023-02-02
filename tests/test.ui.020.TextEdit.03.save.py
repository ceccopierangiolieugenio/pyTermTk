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

import os
import sys

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

def main():
    root = ttk.TTk()

    win1 = ttk.TTkWindow(parent=root, pos=(15,0),  size=(80,30), title="Te1", layout=ttk.TTkGridLayout())
    win2 = ttk.TTkWindow(parent=root, pos=(15,30), size=(80,15), title="Te2", layout=ttk.TTkGridLayout())
    # win3 = ttk.TTkWindow(parent=root, pos=(0,3), size=(30,10))

    te1 = ttk.TTkTextEdit(parent=win1, readOnly=False, lineNumber=True)
    te2 = ttk.TTkTextEdit(parent=win2, readOnly=False, lineNumber=True)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'textedit.ANSI.txt')) as f:
        te1.append(f.read())

    btn1 = ttk.TTkButton(parent=root, pos=(0,0), border=True, text="Txt  to Te2")
    btn2 = ttk.TTkButton(parent=root, pos=(0,3), border=True, text="Raw  to Te2")
    btn3 = ttk.TTkButton(parent=root, pos=(0,6), border=True, text="ANSI to Te2")
    btn4 = ttk.TTkButton(parent=root, pos=(0,9), border=True, text="Quit n' Print")

    global edited
    edited = 0
    lbl1 = ttk.TTkLabel(parent=root,  pos=(2,12), text="Edited:0" )
    def _textChanged():
        global edited
        edited += 1
        lbl1.setText(f"Edited:{edited}")
    te1.textChanged.connect(_textChanged)

    btn1.clicked.connect(lambda : te2.setText(te1.toPlainText()))
    btn2.clicked.connect(lambda : te2.setText(te1.toRawText()))
    btn3.clicked.connect(lambda : te2.setText(te1.toAnsi()))


    global text
    global ansi
    global raw
    text = ""
    ansi = ""
    raw =  ""

    def _quitAndPrint():
        global text
        global ansi
        global raw
        text = te1.toPlainText()
        ansi = te1.toAnsi()
        raw  = te1.toRawText()
        ttk.TTkHelper.quit()

    btn4.clicked.connect(_quitAndPrint)

    root.mainloop()

    print("\nTxt:")
    print(text)
    print("\nANSI:")
    print(ansi)
    print("\nRaw:")
    print(raw)

if __name__ == "__main__":
    main()