
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

    frame.layout().addItem(wrapLayout := ttk.TTkGridLayout(), 0,0)
    frame.layout().addItem(fontLayout := ttk.TTkGridLayout(columnMinWidth=1), 1,0)
    frame.layout().addWidget(te,2,0)

    wrapLayout.addWidget(ttk.TTkLabel(text="Wrap: ", maxWidth=6),0,0)
    wrapLayout.addWidget(lineWrap := ttk.TTkComboBox(list=['NoWrap','WidgetWidth','FixedWidth'], index=2, maxWidth=20),0,1)
    wrapLayout.addWidget(ttk.TTkLabel(text=" Type: ",maxWidth=7),0,2)
    wrapLayout.addWidget(wordWrap := ttk.TTkComboBox(list=['WordWrap','WrapAnywhere'], maxWidth=20),0,3)
    wrapLayout.addWidget(ttk.TTkLabel(text=" FixW: ",maxWidth=7),0,4)
    wrapLayout.addWidget(fixWidth := ttk.TTkSpinBox(value=te.wrapWidth(), maxWidth=5, maximum=500, minimum=10),0,5)
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

    lineWrap.setCurrentIndex(2)
    wordWrap.setCurrentIndex(0)

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