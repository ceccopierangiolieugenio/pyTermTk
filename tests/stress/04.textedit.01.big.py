
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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk/'))
import TermTk as ttk

sys.path.append(os.path.join(sys.path[0],'../../demo'))
from showcase._showcasehelper import getUtfColoredSentence, zc1, zc2, zc3

class superSimpleHorizontalLine(ttk.TTkWidget):
    def paintEvent(self, canvas):
        w,h = self.size()
        canvas.drawText(pos=(0,h-1), text='┕'+('━'*(w-2))+'┙',color=ttk.TTkColor.fg("#888888"))

def demoTextEditSecondary(root=None, document=None):
    te = ttk.TTkTextEdit(parent=root, document=document, lineNumber=True)
    te.setLineWrapMode(ttk.TTkK.WidgetWidth, wrapEngine=ttk.TTkK.WrapEngine.FastWrap)
    te.setWordWrapMode(ttk.TTkK.WordWrap)
    te.setReadOnly(False)
    # print the document events for debugging purposes
    document.contentsChange.connect(lambda line,rem,add: ttk.TTkLog.debug(f"{line=} {rem=} {add=}"))

def demoTextEdit(root=None, document=None):
    frame = ttk.TTkFrame(parent=root, border=False, layout=ttk.TTkGridLayout())

    # If no document is passed a default one is created,
    # In this showcase I want to be able to share the same
    # document among 2 textEdit widgets
    te = ttk.TTkTextEdit(document=document, lineNumber=True)

    te.setReadOnly(False)

    te.setText(ttk.TTkString("Text Edit DEMO\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD+ttk.TTkColor.ITALIC))

    # Load ANSI input
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'textedit.ANSI.txt')):
        te.append(ttk.TTkString("ANSI Input Test\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'textedit.ANSI.txt')) as f:
            te.append(f.read())

    # Test Variable sized chars
    te.append(ttk.TTkString("Test Variable sized chars\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    te.append( "Emoticons: -😁😂😍😎----")
    te.append( "           --😐😁😂😍😎-")
    te.append("")

    te.append( "    UTF-8: £ @ £ ¬ ` 漢 _ _ あ _ _")
    te.append( "           |.|.|.|.|.||.|.|.||.|.|.")
    te.append("")

    te.append( "           - |  |  |  |  | -")
    te.append(f"Zero Size: - o{zc1}  o{zc2}  o{zc3}  o{zc1}{zc2}  o{zc1}{zc2}{zc3} -")
    te.append( "           - |  |  |  |  | -")
    te.append("")

    te.append(f"Plus Tabs: -\t😁\t😍\to{zc1}{zc2}{zc3}\t😎\to{zc1}{zc2}{zc3}\t😂-")
    te.append("")

    # Test Tabs
    te.append(ttk.TTkString("Tabs Test\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    te.append("Word\tAnother Word\tYet more words")
    te.append("What a wonderful word\tOut of this word\tBattle of the words\tThe city of thousand words\tThe word is not enough\tJurassic word\n")
    te.append("tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("-tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("--tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("---tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("----tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("-----tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("------tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("-------tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\n")

    te.append(ttk.TTkString("Random TTkString Input Test\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    _sss = ttk.TTkString('\n').join([ ttk.TTkString(f"{i} <- ") + getUtfColoredSentence(3,10) + ttk.TTkString(f" -> {i} ")for i in range(500)])
    for _ in range(20):
        te.append(_sss)

    te.append(ttk.TTkString("-- The Very END --",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))

    # use the widget size to wrap
    # te.setLineWrapMode(ttk.TTkK.WidgetWidth)
    # te.setWordWrapMode(ttk.TTkK.WordWrap)

    # Use a fixed wrap size
    # te.setLineWrapMode(ttk.TTkK.FixedWidth)
    # te.setWrapWidth(100)

    frame.layout().addItem(wrapLayout := ttk.TTkHBoxLayout(), 0,0)
    frame.layout().addWidget(te,2,0)

    wrapLayout.addWidget(ttk.TTkLabel(text="Wrap: ", maxWidth=6))
    wrapLayout.addWidget(lineWrap := ttk.TTkComboBox(list=[_lw.name for _lw in ttk.TTkK.LineWrapMode], maxWidth=20))
    wrapLayout.addWidget(ttk.TTkLabel(text=" Type: ",maxWidth=7))
    wrapLayout.addWidget(wordWrap := ttk.TTkComboBox(list=[_wm.name for _wm in ttk.TTkK.WrapMode], maxWidth=20, enabled=False))
    wrapLayout.addWidget(ttk.TTkLabel(text=" Engine: ",maxWidth=9))
    wrapLayout.addWidget(wrapEngine := ttk.TTkComboBox(list=[_we.name for _we in ttk.TTkK.WrapEngine], maxWidth=20, index=2))
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

    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen (default)', action='store_true')
    parser.add_argument('-w', help='Windowed',    action='store_true')
    args = parser.parse_args()
    windowed = args.w

    root = ttk.TTk()
    if windowed:
        rootTree = ttk.TTkWindow(parent=root,pos = (0,0), size=(70,40), title="Test Text Edit", layout=ttk.TTkGridLayout(), border=True)
    else:
        rootTree = root
        root.setLayout(ttk.TTkGridLayout())
    split = ttk.TTkSplitter()
    document = ttk.TTkTextDocument()
    demoTextEdit(split, document)
    demoTextEditSecondary(split, document)
    rootTree.layout().addWidget(split,0,0,1,2)
    rootTree.layout().addWidget(quitbtn := ttk.TTkButton(border=True, text="Quit", maxWidth=6),1,0)
    rootTree.layout().addWidget(ttk.TTkKeyPressView(maxHeight=3),1,1)
    rootTree.layout().addWidget(ttk.TTkLogViewer(),2,0,1,2)
    quitbtn.clicked.connect(root.quit)
    root.mainloop()

if __name__ == "__main__":
    main()