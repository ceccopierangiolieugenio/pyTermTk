
#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
import threading
import time

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk/'))
import TermTk as ttk

sys.path.append(os.path.join(sys.path[0],'../../demo'))
from showcase._showcasehelper import getSentence

texts = [
    ttk.TTkString('\n').join([ getSentence(3,10) for _ in range(100)]),
    ttk.TTkString('\n').join([ getSentence(3,10) for _ in range(50)]),
    ttk.TTkString('\n').join([ getSentence(3,10) for _ in range(10)]),
    ttk.TTkString('\n').join([ getSentence(3,10) for _ in range(50)]),
    ttk.TTkString('\n').join([ getSentence(3,10) for _ in range(100)]),
]

class superSimpleHorizontalLine(ttk.TTkWidget):
    def paintEvent(self, canvas):
        w,h = self.size()
        canvas.drawText(pos=(0,h-1), text='┕'+('━'*(w-2))+'┙',color=ttk.TTkColor.fg("#888888"))

def demoTextEdit(root=None):
    frame = ttk.TTkFrame(parent=root, border=False, layout=ttk.TTkGridLayout())

    te = ttk.TTkTextEdit(lineNumber=True, lineNumberStarting=1)
    te.setReadOnly(False)
    te.setText(texts[0])
    te.setLineWrapMode(ttk.TTkK.FixedWidth)
    te.setWordWrapMode(ttk.TTkK.WordWrap)

    frame.layout().addItem(wrapLayout := ttk.TTkHBoxLayout(), 0,0)
    frame.layout().addWidget(te,2,0)

    wrapLayout.addWidget(ttk.TTkLabel(text="Wrap: ", maxWidth=6))
    wrapLayout.addWidget(lineWrap := ttk.TTkComboBox(list=[_lw.name for _lw in ttk.TTkK.LineWrapMode], maxWidth=20))
    wrapLayout.addWidget(ttk.TTkLabel(text=" Type: ",maxWidth=7))
    wrapLayout.addWidget(wordWrap := ttk.TTkComboBox(list=[_wm.name for _wm in ttk.TTkK.WrapMode], maxWidth=20, enabled=False))
    wrapLayout.addWidget(ttk.TTkLabel(text=" Engine: ",maxWidth=9))
    wrapLayout.addWidget(wrapEngine := ttk.TTkComboBox(list=[_we.name for _we in ttk.TTkK.WrapEngine], maxWidth=20, index=1))
    wrapLayout.addWidget(ttk.TTkLabel(text=" FixW: ",maxWidth=7))
    wrapLayout.addWidget(fixWidth := ttk.TTkSpinBox(value=te.wrapWidth(), maxWidth=5, maximum=500, minimum=10, enabled=False))
    wrapLayout.addWidget(ttk.TTkSpacer(maxHeight=1))

    lineWrap.setCurrentText(ttk.TTkK.LineWrapMode.NoWrap.name)
    wordWrap.setCurrentText(ttk.TTkK.WrapMode.WrapAnywhere.name)

    fixWidth.valueChanged.connect(te.setWrapWidth)

    @ttk.pyTTkSlot(str)
    def _lineWrapCallback(_lineWrap:str):
        _wrapEngine = ttk.TTkK.WrapEngine[wrapEngine.currentText()]
        if _lineWrap == ttk.TTkK.LineWrapMode.NoWrap.name:
            te.setLineWrapMode(ttk.TTkK.NoWrap)
            wordWrap.setDisabled()
            fixWidth.setDisabled()
        elif _lineWrap == ttk.TTkK.LineWrapMode.WidgetWidth.name:
            te.setLineWrapMode(ttk.TTkK.WidgetWidth, wrapEngine=_wrapEngine)
            wordWrap.setEnabled()
            fixWidth.setDisabled()
        elif _lineWrap == ttk.TTkK.LineWrapMode.FixedWidth.name:
            te.setLineWrapMode(ttk.TTkK.FixedWidth, wrapEngine=_wrapEngine)
            te.setWrapWidth(fixWidth.value())
            wordWrap.setEnabled()
            fixWidth.setEnabled()

    lineWrap.currentTextChanged.connect(_lineWrapCallback)

    @ttk.pyTTkSlot(int)
    def _wordWrapCallback(_index):
        if _index == 0:
            te.setWordWrapMode(ttk.TTkK.WordWrap)
        else:
            te.setWordWrapMode(ttk.TTkK.WrapAnywhere)

    wordWrap.currentIndexChanged.connect(_wordWrapCallback)

    @ttk.pyTTkSlot(str)
    def _wrapEngineCallback(_wrapEngine:str):
        _wrapEngine = ttk.TTkK.WrapEngine[_wrapEngine]
        _lineWrap = ttk.TTkK.LineWrapMode[lineWrap.currentText()]
        te.setLineWrapMode(_lineWrap, wrapEngine=_wrapEngine)

    wrapEngine.currentTextChanged.connect(_wrapEngineCallback)

    def _thread():
        while True:
            for txt in texts:
                time.sleep(0.5)
                te.append(txt)
                te.clear()
                time.sleep(0.5)
                te.append(txt)
                time.sleep(0.5)
                te.setText(txt)

    threading.Thread(target=_thread).start()

    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen (default)', action='store_true')
    parser.add_argument('-w', help='Windowed',    action='store_true')
    args = parser.parse_args()
    windowed = args.w

    root = ttk.TTk()
    if windowed:
        rootTree = ttk.TTkWindow(parent=root,pos = (0,0), size=(70,40), title="Test Text Edit", layout=ttk.TTkVBoxLayout(), border=True)
    else:
        rootTree = root
        root.setLayout(ttk.TTkVBoxLayout())
    split = ttk.TTkSplitter()
    demoTextEdit(split)
    rootTree.layout().addWidget(split)
    rootTree.layout().addWidget(ttk.TTkLogViewer())
    root.mainloop()

if __name__ == "__main__":
    main()