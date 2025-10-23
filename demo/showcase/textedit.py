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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk/'))
import TermTk as ttk

sys.path.append(os.path.join(sys.path[0],'..'))
from showcase._showcasehelper import getUtfColoredSentence, zc1, zc2, zc3

class superSimpleHorizontalLine(ttk.TTkWidget):
    def paintEvent(self, canvas):
        w,h = self.size()
        canvas.drawText(pos=(0,h-1), text='┕'+('━'*(w-2))+'┙',color=ttk.TTkColor.fg("#888888"))

def demoTextEditSecondary(root=None, document=None):
    te = ttk.TTkTextEdit(parent=root, document=document, lineNumber=True)
    te.setLineWrapMode(ttk.TTkK.WidgetWidth)
    te.setWordWrapMode(ttk.TTkK.WordWrap)
    te.setReadOnly(False)
    # print the document events for debugging purposes
    document.contentsChange.connect(lambda line,rem,add: ttk.TTkLog.debug(f"{line=} {rem=} {add=}"))

def demoTextEdit(root=None, document=None):
    frame = ttk.TTkFrame(parent=root, border=False, layout=ttk.TTkGridLayout())

    # If no document is passed a default one is created,
    # In this showcase I want to be able to share the same
    # document among 2 textEdit widgets
    te = ttk.TTkTextEdit(document=document, lineNumber=True, lineNumberStarting=1)

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
    te.append(ttk.TTkString('\n').join([ getUtfColoredSentence(3,10) for _ in range(50)]))

    te.append(ttk.TTkString("-- The Very END --",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))

    # use the widget size to wrap
    # te.setLineWrapMode(ttk.TTkK.WidgetWidth)
    # te.setWordWrapMode(ttk.TTkK.WordWrap)

    # Use a fixed wrap size
    # te.setLineWrapMode(ttk.TTkK.FixedWidth)
    # te.setWrapWidth(100)

    frame.layout().addItem(wrapLayout := ttk.TTkGridLayout(), 0,0)
    frame.layout().addItem(fontLayout := ttk.TTkGridLayout(columnMinWidth=1), 1,0)
    frame.layout().addWidget(te,2,0)

    wrapLayout.addWidget(ttk.TTkLabel(text="Wrap: ", maxWidth=6),0,0)
    wrapLayout.addWidget(lineWrap := ttk.TTkComboBox(list=['NoWrap','WidgetWidth','FixedWidth'], maxWidth=20),0,1)
    wrapLayout.addWidget(ttk.TTkLabel(text=" Type: ",maxWidth=7),0,2)
    wrapLayout.addWidget(wordWrap := ttk.TTkComboBox(list=['WordWrap','WrapAnywhere'], maxWidth=20, enabled=False),0,3)
    wrapLayout.addWidget(ttk.TTkLabel(text=" FixW: ",maxWidth=7),0,4)
    wrapLayout.addWidget(fixWidth := ttk.TTkSpinBox(value=te.wrapWidth(), maxWidth=5, maximum=500, minimum=10, enabled=False),0,5)
    wrapLayout.addWidget(ttk.TTkSpacer(),0,10)

    # Empty columns/cells are 1 char wide due to "columnMinWidth=1" parameter in the GridLayout
    #           1       3                    8                11
    #    0       2       4    5    6    7     9       10       12
    # 0  [ ] FG  [ ] BG  [ ] LineNumber [  0]Starting Number
    # 1  ┌─────┐ ┌─────┐ ╒═══╕╒═══╕╒═══╕╒═══╕ ┌──────┐┌──────┐
    # 2  │     │ │     │ │ a ││ a ││ a ││ a │ │ UNDO ││ REDO │
    # 3  └─────┘ └─────┘ └───┘└───┘└───┘└───┘ ╘══════╛└──────┘ ┕━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┙

    # Char Fg/Bg buttons
    fontLayout.addWidget(cb_fg := ttk.TTkCheckbox(text=" FG"),0,0)
    fontLayout.addWidget(btn_fgColor := ttk.TTkColorButtonPicker(border=True, enabled=False, maxSize=(7,3), returnType=ttk.TTkK.ColorPickerReturnType.Foreground),1,0)

    fontLayout.addWidget(cb_bg := ttk.TTkCheckbox(text=" BG"),0,2)
    fontLayout.addWidget(btn_bgColor := ttk.TTkColorButtonPicker(border=True, enabled=False, maxSize=(7,3), returnType=ttk.TTkK.ColorPickerReturnType.Background),1,2)

    fontLayout.addWidget(cb_linenumber := ttk.TTkCheckbox(text=" LineNumber", checked=True),0,4,1,3)
    fontLayout.addWidget(sb_linenumber := ttk.TTkSpinBox(value=1, maxWidth=5, maximum=10000, minimum=-10000, enabled=True),0,7,1,1)

    # Char style buttons
    fontLayout.addWidget(btn_bold          := ttk.TTkButton(border=True, maxSize=(5,3), checkable=True, text=ttk.TTkString( 'a' , ttk.TTkColor.BOLD)        ),1,4)
    fontLayout.addWidget(btn_italic        := ttk.TTkButton(border=True, maxSize=(5,3), checkable=True, text=ttk.TTkString( 'a' , ttk.TTkColor.ITALIC)      ),1,5)
    fontLayout.addWidget(btn_underline     := ttk.TTkButton(border=True, maxSize=(5,3), checkable=True, text=ttk.TTkString(' a ', ttk.TTkColor.UNDERLINE)   ),1,6)
    fontLayout.addWidget(btn_strikethrough := ttk.TTkButton(border=True, maxSize=(5,3), checkable=True, text=ttk.TTkString(' a ', ttk.TTkColor.STRIKETROUGH)),1,7)

    # Undo/Redo buttons
    fontLayout.addWidget(btn_undo := ttk.TTkButton(border=True, maxSize=(8,3), enabled=te.isUndoAvailable(), text=' UNDO '),1,9 )
    fontLayout.addWidget(btn_redo := ttk.TTkButton(border=True, maxSize=(8,3), enabled=te.isRedoAvailable(), text=' REDO '),1,10)
    # Undo/Redo events
    te.undoAvailable.connect(btn_undo.setEnabled)
    te.redoAvailable.connect(btn_redo.setEnabled)
    btn_undo.clicked.connect(te.undo)
    btn_redo.clicked.connect(te.redo)

    # Useless custom horizontal bar for aestetic reason
    fontLayout.addWidget(superSimpleHorizontalLine(),0,12,2,1)

    @ttk.pyTTkSlot(ttk.TTkColor)
    def _currentColorChangedCB(format:ttk.TTkColor):
        if format.hasForeground():
            cb_fg.setCheckState(ttk.TTkK.Checked)
            btn_fgColor.setEnabled()
            btn_fgColor.setColor(format.foreground())
        else:
            cb_fg.setCheckState(ttk.TTkK.Unchecked)
            btn_fgColor.setDisabled()

        if format.hasBackground():
            cb_bg.setCheckState(ttk.TTkK.Checked)
            btn_bgColor.setEnabled()
            btn_bgColor.setColor(format.background())
        else:
            cb_bg.setCheckState(ttk.TTkK.Unchecked)
            btn_bgColor.setDisabled()

        btn_bold.setChecked(format.bold())
        btn_italic.setChecked(format.italic())
        btn_underline.setChecked(format.underline())
        btn_strikethrough.setChecked(format.strikethrough())
        # ttk.TTkLog.debug(f"{fg=} {bg=} {bold=} {italic=} {underline=} {strikethrough=   }")

    te.currentColorChanged.connect(_currentColorChangedCB)

    def _setStyle():
        color = ttk.TTkColor()
        if cb_fg.checkState() == ttk.TTkK.Checked:
            color += btn_fgColor.color()
        if cb_bg.checkState() == ttk.TTkK.Checked:
            color += btn_bgColor.color()
        if btn_bold.isChecked():
            color += ttk.TTkColor.BOLD
        if btn_italic.isChecked():
            color += ttk.TTkColor.ITALIC
        if btn_underline.isChecked():
            color += ttk.TTkColor.UNDERLINE
        if btn_strikethrough.isChecked():
            color += ttk.TTkColor.STRIKETROUGH
        cursor = te.textCursor()
        cursor.applyColor(color)
        cursor.setColor(color)
        te.setFocus()

    cb_fg.toggled.connect(btn_fgColor.setEnabled)
    cb_bg.toggled.connect(btn_bgColor.setEnabled)
    cb_fg.clicked.connect(_setStyle)
    cb_bg.clicked.connect(_setStyle)

    cb_linenumber.toggled.connect(te.setLineNumber)
    cb_linenumber.toggled.connect(sb_linenumber.setEnabled)
    sb_linenumber.valueChanged.connect(te.setLineNumberStarting)

    btn_fgColor.colorSelected.connect(_setStyle)
    btn_bgColor.colorSelected.connect(_setStyle)

    btn_bold.clicked.connect(_setStyle)
    btn_italic.clicked.connect(_setStyle)
    btn_underline.clicked.connect(_setStyle)
    btn_strikethrough.clicked.connect(_setStyle)

    lineWrap.setCurrentIndex(0)
    wordWrap.setCurrentIndex(1)

    fixWidth.valueChanged.connect(te.setWrapWidth)

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
            te.setWrapWidth(fixWidth.value())
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
    parser.add_argument('-f', help='Full Screen (default)', action='store_true')
    parser.add_argument('-w', help='Windowed',    action='store_true')
    args = parser.parse_args()
    windowed = args.w

    root = ttk.TTk(sigmask=(
                    ttk.TTkTerm.Sigmask.CTRL_Q |
                    ttk.TTkTerm.Sigmask.CTRL_S |
                    ttk.TTkTerm.Sigmask.CTRL_Z |
                    ttk.TTkTerm.Sigmask.CTRL_C ))
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
    quitbtn.clicked.connect(root.quit)
    root.mainloop()

if __name__ == "__main__":
    main()