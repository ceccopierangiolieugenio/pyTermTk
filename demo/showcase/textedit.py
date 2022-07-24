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

words = ["Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]
def randColor():
    return [
        ttk.TTkColor.RST,
        ttk.TTkColor.fg('#FFFF00'),
        ttk.TTkColor.fg('#00FFFF'),
        ttk.TTkColor.fg('#FF00FF'),
        ttk.TTkColor.fg('#0000FF')+ttk.TTkColor.bg('#00FF00'),
        ttk.TTkColor.fg('#00FF00')+ttk.TTkColor.UNDERLINE,
        ttk.TTkColor.fg('#FF0000')+ttk.TTkColor.STRIKETROUGH,
    ][random.randint(0,6)]
def getWords(n):
    www = [random.choice(words) for _ in range(n)]
    return ttk.TTkString(" ".join(www), randColor())
def getSentence(a,b,i):
    return ttk.TTkString(" ").join([f"{i} "]+[getWords(random.randint(1,4)) for i in range(0,random.randint(a,b))])

class superSimpleHorizontalLine(ttk.TTkWidget):
    def paintEvent(self):
        w,h = self.size()
        self._canvas.drawText(pos=(0,h-1), text='┕'+('━'*(w-2))+'┙',color=ttk.TTkColor.fg("#888888"))

def demoTextEditSecondary(root=None, document=None):
    te = ttk.TTkTextEdit(parent=root, document=document)
    te.setLineWrapMode(ttk.TTkK.WidgetWidth)
    te.setWordWrapMode(ttk.TTkK.WordWrap)
    te.setReadOnly(False)

def demoTextEdit(root=None, document=None):
    frame = ttk.TTkFrame(parent=root, border=False, layout=ttk.TTkGridLayout())

    # If no document is passed a default one is created,
    # In this showcase I want to be able to share the same
    # document among 2 textEdit widgets
    te = ttk.TTkTextEdit(document=document)

    te.setReadOnly(False)

    te.setText(ttk.TTkString("Text Edit DEMO\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD+ttk.TTkColor.ITALIC))

    # Load ANSI input
    te.append(ttk.TTkString("ANSI Input Test\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'textedit.ANSI.txt')) as f:
        te.append(f.read())

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
    te.append(ttk.TTkString('\n').join([ getSentence(3,10,i) for i in range(50)]))

    te.append(ttk.TTkString("-- The Very END --",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))

    # use the widget size to wrap
    # te.setLineWrapMode(ttk.TTkK.WidgetWidth)
    # te.setWordWrapMode(ttk.TTkK.WordWrap)

    # Use a fixed wrap size
    # te.setLineWrapMode(ttk.TTkK.FixedWidth)
    # te.setWrapWidth(100)

    frame.layout().addItem(wrapLayout := ttk.TTkGridLayout(), 0,0)
    frame.layout().addItem(fontLayout := ttk.TTkGridLayout(), 1,0)
    frame.layout().addWidget(te,2,0)

    wrapLayout.addWidget(ttk.TTkLabel(text="Wrap: ", maxWidth=6),0,0)
    wrapLayout.addWidget(lineWrap := ttk.TTkComboBox(list=['NoWrap','WidgetWidth','FixedWidth'], maxWidth=20),0,1)
    wrapLayout.addWidget(ttk.TTkLabel(text=" Type: ",maxWidth=7),0,2)
    wrapLayout.addWidget(wordWrap := ttk.TTkComboBox(list=['WordWrap','WrapAnywhere'], maxWidth=20, enabled=False),0,3)
    wrapLayout.addWidget(ttk.TTkLabel(text=" FixW: ",maxWidth=7),0,4)
    wrapLayout.addWidget(fixWidth := ttk.TTkSpinBox(value=te.wrapWidth(), maxWidth=5, maximum=500, minimum=10, enabled=False),0,5)
    wrapLayout.addWidget(ttk.TTkSpacer(),0,10)

    fontLayout.addWidget(cb_fg := ttk.TTkCheckbox(text=" FG"),0,0)
    fontLayout.addWidget(btn_fgColor := ttk.TTkColorButtonPicker(border=True, enabled=False, maxSize=(7,3)),1,0)
    # fontLayout.addWidget(ttk.TTkSpacer(maxWidth=3),0,1,2,1)
    fontLayout.addWidget(cb_bg := ttk.TTkCheckbox(text=" BG"),0,2)
    fontLayout.addWidget(btn_bgColor := ttk.TTkColorButtonPicker(border=True, enabled=False, maxSize=(7   ,3)),1,2)
    # fontLayout.addWidget(ttk.TTkSpacer(maxWidth=3),0,3,2,1)
    fontLayout.addWidget(btn_bold          := ttk.TTkButton(border=True, maxSize=(5,3), checkable=True, text=ttk.TTkString( 'a' , ttk.TTkColor.BOLD)        ),1,4)
    fontLayout.addWidget(btn_italic        := ttk.TTkButton(border=True, maxSize=(5,3), checkable=True, text=ttk.TTkString( 'a' , ttk.TTkColor.ITALIC)      ),1,5)
    fontLayout.addWidget(btn_underline     := ttk.TTkButton(border=True, maxSize=(5,3), checkable=True, text=ttk.TTkString(' a ', ttk.TTkColor.UNDERLINE)   ),1,6)
    fontLayout.addWidget(btn_strikethrough := ttk.TTkButton(border=True, maxSize=(5,3), checkable=True, text=ttk.TTkString(' a ', ttk.TTkColor.STRIKETROUGH)),1,7)
    fontLayout.addWidget(superSimpleHorizontalLine(),0,10,2,1)

    @ttk.pyTTkSlot(ttk.TTkColor)
    def _currentColorChangedCB(format):
        if fg := format.foreground():
            cb_fg.setCheckState(ttk.TTkK.Checked)
            btn_fgColor.setEnabled()
            btn_fgColor.setColor(fg.invertFgBg())
        else:
            cb_fg.setCheckState(ttk.TTkK.Unchecked)
            btn_fgColor.setDisabled()

        if bg := format.background():
            cb_bg.setCheckState(ttk.TTkK.Checked)
            btn_bgColor.setEnabled()
            btn_bgColor.setColor(bg)
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
            color += btn_fgColor.color().invertFgBg()
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

    cb_fg.stateChanged.connect(lambda x: btn_fgColor.setEnabled(x==ttk.TTkK.Checked))
    cb_bg.stateChanged.connect(lambda x: btn_bgColor.setEnabled(x==ttk.TTkK.Checked))
    cb_fg.clicked.connect(lambda _: _setStyle())
    cb_bg.clicked.connect(lambda _: _setStyle())

    btn_fgColor.colorSelected.connect(lambda _: _setStyle())
    btn_bgColor.colorSelected.connect(lambda _: _setStyle())

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

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if windowed:
        rootTree = ttk.TTkWindow(parent=root,pos = (0,0), size=(70,40), title="Test Text Edit", layout=ttk.TTkGridLayout(), border=True)
    else:
        rootTree = root
        root.setLayout(ttk.TTkGridLayout())
    split = ttk.TTkSplitter(parent=rootTree)
    document = ttk.TTkTextDocument()
    demoTextEdit(split, document)
    demoTextEditSecondary(split, document)
    rootTree.layout().addWidget(ttk.TTkKeyPressView(maxHeight=3),1,0)
    root.mainloop()

if __name__ == "__main__":
    main()