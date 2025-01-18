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

import os
import sys
import random
import argparse

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

def demoTextEdit(root, filename):
    frame = ttk.TTkFrame(parent=root, border=False, layout=ttk.TTkGridLayout())

    te = ttk.TTkTextEdit()
    te.setReadOnly(False)

    with open(filename, 'r') as f:
        content = f.read()
        doc = ttk.TextDocumentHighlight(text=content)
        te.setDocument(doc)

    # use the widget size to wrap
    # te.setLineWrapMode(ttk.TTkK.WidgetWidth)
    # te.setWordWrapMode(ttk.TTkK.WordWrap)

    # Use a fixed wrap size
    # te.setLineWrapMode(ttk.TTkK.FixedWidth)
    # te.setWrapWidth(100)

    frame.layout().addWidget(te,1,0,1,10)
    frame.layout().addWidget(ttk.TTkLabel(text="Wrap: ", maxWidth=6),0,0)
    frame.layout().addWidget(lineWrap := ttk.TTkComboBox(list=['NoWrap','WidgetWidth','FixedWidth']),0,1)
    frame.layout().addWidget(ttk.TTkLabel(text=" Type: ",maxWidth=7),0,2)
    frame.layout().addWidget(wordWrap := ttk.TTkComboBox(list=['WordWrap','WrapAnywhere'], enabled=False),0,3)
    frame.layout().addWidget(ttk.TTkLabel(text=" FixW: ",maxWidth=7),0,4)
    frame.layout().addWidget(fixWidth := ttk.TTkSpinBox(value=te.wrapWidth(), maximum=500, minimum=10, enabled=False),0,5)
    frame.layout().addWidget(ttk.TTkLabel(text=" Lexer: ",maxWidth=8),0,6)
    frame.layout().addWidget(lexers   := ttk.TTkComboBox(list=ttk.TextDocumentHighlight.getLexers()),0,7)
    frame.layout().addWidget(ttk.TTkLabel(text=" Style: ",maxWidth=8),0,8)
    frame.layout().addWidget(styles   := ttk.TTkComboBox(list=ttk.TextDocumentHighlight.getStyles()),0,9)


    lineWrap.setCurrentIndex(0)
    wordWrap.setCurrentIndex(1)

    fixWidth.valueChanged.connect(te.setWrapWidth)
    lexers.currentTextChanged.connect(doc.setLexer)
    styles.currentTextChanged.connect(doc.setStyle)

    @ttk.pyTTkSlot(int)
    def _lineWrapCallback(index):
        if index == 0:
            te.setLineWrapMode(ttk.TTkK.NoWrap)
            wordWrap.setDisabled()
            fixWidth.setDisabled()
        elif index == 1:
            te.setLineWrapMode(ttk.TTkK.WidgetWidth)
            wordWrap.setEnabled()
            fixWidth.setDisabled()
        else:
            te.setLineWrapMode(ttk.TTkK.FixedWidth)
            wordWrap.setEnabled()
            fixWidth.setEnabled()

    lineWrap.currentIndexChanged.connect(_lineWrapCallback)

    @ttk.pyTTkSlot(int)
    def _wordWrapCallback(index):
        if index == 0:
            te.setWordWrapMode(ttk.TTkK.WordWrap)
        else:
            te.setWordWrapMode(ttk.TTkK.WrapAnywhere)

    wordWrap.currentIndexChanged.connect(_wordWrapCallback)

    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, nargs='+',
                    help='the filename/s')
    args = parser.parse_args()

    root = ttk.TTk()
    for file in args.filename:
        win = ttk.TTkWindow(parent=root,pos = (0,0), size=(100,40), title="Test Text Edit", layout=ttk.TTkGridLayout(), border=True)
        demoTextEdit(win, file)

    root.mainloop()

if __name__ == "__main__":
    main()