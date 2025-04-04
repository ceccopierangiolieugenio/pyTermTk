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

__all__ = ['NotePad']

import TermTk as ttk

class SuperSimpleHorizontalLine(ttk.TTkWidget):
    def paintEvent(self, canvas):
        w,h = self.size()
        canvas.drawText(pos=(0,h-1), text='┕'+('━'*(w-2))+'┙',color=ttk.TTkColor.fg("#888888"))

class NotePad(ttk.TTkGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        te = ttk.TTkTextEdit(readOnly=False, lineNumber=True)

        self.addItem(wrapLayout := ttk.TTkGridLayout(), 0,0)
        self.addItem(fontLayout := ttk.TTkGridLayout(columnMinWidth=1), 1,0)
        self.addWidget(te,2,0)

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
        # 0  [ ] FG  [ ] BG  [ ] LineNumber
        # 1  ┌─────┐ ┌─────┐ ╒═══╕╒═══╕╒═══╕╒═══╕ ┌──────┐┌──────┐
        # 2  │     │ │     │ │ a ││ a ││ a ││ a │ │ UNDO ││ REDO │
        # 3  └─────┘ └─────┘ └───┘└───┘└───┘└───┘ ╘══════╛└──────┘ ┕━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┙

        # Char Fg/Bg buttons
        fontLayout.addWidget(cb_fg := ttk.TTkCheckbox(text=" FG"),0,0)
        fontLayout.addWidget(btn_fgColor := ttk.TTkColorButtonPicker(border=True, enabled=False, maxSize=(7,3)),1,0)

        fontLayout.addWidget(cb_bg := ttk.TTkCheckbox(text=" BG"),0,2)
        fontLayout.addWidget(btn_bgColor := ttk.TTkColorButtonPicker(border=True, enabled=False, maxSize=(7   ,3)),1,2)

        fontLayout.addWidget(cb_linenumber := ttk.TTkCheckbox(text=" LineNumber", checked=True),0,4,1,3)

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
        fontLayout.addWidget(SuperSimpleHorizontalLine(),0,12,2,1)

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

        cb_linenumber.stateChanged.connect(lambda x: te.setLineNumber(x==ttk.TTkK.Checked))

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


