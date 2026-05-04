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

__all__ = ['TextArea']

import TermTk as ttk

from .glbls import glbls

_StartingText = '''Ansi Editor:

─ ┌─┬┐  ┏━┳┓  ┎─┰┒  ┍━┯┑  ┏┭┲━┱┮┓
━ │ ││  ┃ ┃┃  ┃ ┃┃  │ ││  ┞╁╀┰╀╁┦
│ ├─┼┤  ┣━╋┫  ┠─╂┨  ┝━┿┥  ┟╄╈╇╈╃┧
┃ └─┴┘  ┗━┻┛  ┖─┸┚  ┕━┷┙  ┡┽╊┷╉┾┩
┄    ╴ ╵╷ ╸ ╹╻ ╼ ╽╿       ╽╵┞╼┩┕┙╻
┅    ╶    ╺    ╾          ╿╷┝╾┤┌┮╋╸
┆ ┌─┬┐  ╔═╦╗  ╓─╥╖  ╒═╤╕  ┢┽╆━╅┾┪╹
┇ │ ││  ║ ║║  ║ ║║  │ ││  ┗┵┺━┹┶┛
┈ ├─┼┤  ╠═╬╣  ╟─╫╢  ╞═╪╡  ┞ ┦ ┭ ┵ ┽ ╃ ╇
┉ └─┴┘  ╚═╩╝  ╙─╨╜  ╘═╧╛  ┟ ┧ ┮ ┶ ┾ ╄ ╈
┊ ╭───────────────────╮   ┡ ┩ ┱ ┹ ╀ ╅ ╉
┋ │  ╔═══╗ Some Text  │░  ┢ ┪ ┲ ┺ ╁ ╆ ╊
╌ │  ╚═╦═╝ in the box │▒
╍ ╞═╤══╩══╤═══════════╡▒      ╭─────╮
╎ │ ├──┬──┤           │▒    ╭ │╲ ╳ ╱│
╏ │ ╰──┴──╯           │▓    ╮ │ ╳╳╳ │
═ └───────────────────┘▓    ╯ ╰─────╯
║  ░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓█    ╰  ╱ ╲ ╳

▄ ▀ █ <- Half,Full
▁ ▂ ▃ ▄ ▅ ▆ ▇ █     Spaces: "    "

█ Full █ ▌ ▐ ▏ ▕  ▔ ▁
▉        ░ ▒ ▓ █
▊
▋        ▘ ▚ ▟
▌        ▝ ▞ ▙
▍        ▖ ▌ ▜
▎        ▗ ▐ ▛
▏ 1/8
  ◢ ◣ ◤ ◥  ■ □ ▢ ▣

Symbols for Legacy Computing
                     🬼   🭀
🬼 🭇 🭗 🭢  🭨  🭍 🭑 🬽  🭌 🬿 🭐 🭎
🬽 🭈 🭘 🭣  🭩
🬾 🭉 🭙 🭤  🭪
🬿 🭊 🭚 🭥  🭫
🭀 🭋 🭛 🭦  🭬
🭌 🭁 🭝 🭒  🭭
🭍 🭂 🭞 🭓  🭮
🭎 🭃 🭟 🭔  🭯
🭏 🭄 🭠 🭕  🮚
🭐 🭅 🭡 🭖  🮛
🭑 🭆 🭜 🭧

    🭇🬼
    🭃🭌🬿
    🭥🭒█🭏🬼
 🭋🭍🭑🬽🭢🭕█🭌🬿
 🭅███🭀 🭥🭒█🭏🬼
🭋████🭐  🭢🭕█🭌🬿
🭅██🭞🭜🭘 🭈🭆🭂███🭏🬼
🭣🭧🭚 🭈🭆🭂██████🭠🭗
       🭥🭒██🭝🭚
        🭢🭕🭠🭗

'''
class TextArea(ttk.TTkGridLayout):
    __slots__ = ('_te',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._te = ttk.TTkTextEdit(lineNumber=True, readOnly=False)
        self._te.setText(_StartingText)

        self.addItem(wrapLayout := ttk.TTkGridLayout(), 0,0)
        self.addItem(fontLayout := ttk.TTkGridLayout(columnMinWidth=1), 1,0)
        self.addWidget(self._te,2,0)

        wrapLayout.addWidget(ttk.TTkLabel(text="Wrap: ", maxWidth=6),0,0)
        wrapLayout.addWidget(lineWrap := ttk.TTkComboBox(list=['NoWrap','WidgetWidth','FixedWidth'], maxWidth=20),0,1)
        wrapLayout.addWidget(ttk.TTkLabel(text=" Type: ",maxWidth=7),0,2)
        wrapLayout.addWidget(wordWrap := ttk.TTkComboBox(list=['WordWrap','WrapAnywhere'], maxWidth=20, enabled=False),0,3)
        wrapLayout.addWidget(ttk.TTkLabel(text=" FixW: ",maxWidth=7),0,4)
        wrapLayout.addWidget(fixWidth := ttk.TTkSpinBox(value=self._te.wrapWidth(), maxWidth=5, maximum=500, minimum=10, enabled=False),0,5)
        wrapLayout.addWidget(ttk.TTkSpacer(),0,10)

        # Empty columns/cells are 1 char wide due to "columnMinWidth=1" parameter in the GridLayout
        #           1       3                    8                11
        #    0       2       4    5    6    7     9       10       12
        # 0  [ ] FG  [ ] BG  [ ] LineNumber
        # 1  ┌─────┐ ┌─────┐ ┌──────┐┌──────┐
        # 2  │     │ │     │ │ UNDO ││ REDO │
        # 3  └─────┘ └─────┘ ╘══════╛└──────┘ ┕━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┙

        # Char Fg/Bg buttons
        fontLayout.addWidget(cb_fg := ttk.TTkCheckbox(text=" FG"),0,0)
        fontLayout.addWidget(btn_fgColor := ttk.TTkColorButtonPicker(border=True, enabled=False, maxSize=(7,3), returnType=ttk.TTkK.ColorPickerReturnType.Foreground),1,0)

        fontLayout.addWidget(cb_bg := ttk.TTkCheckbox(text=" BG"),0,2)
        fontLayout.addWidget(btn_bgColor := ttk.TTkColorButtonPicker(border=True, enabled=False, maxSize=(7,3), returnType=ttk.TTkK.ColorPickerReturnType.Background),1,2)

        fontLayout.addWidget(cb_linenumber := ttk.TTkCheckbox(text=" LineNumber", checked=True),0,4,1,3)

        # Undo/Redo buttons
        fontLayout.addWidget(btn_undo := ttk.TTkButton(border=True, maxSize=(8,3), enabled=self._te.isUndoAvailable(), text=' UNDO '),1,4)
        fontLayout.addWidget(btn_redo := ttk.TTkButton(border=True, maxSize=(8,3), enabled=self._te.isRedoAvailable(), text=' REDO '),1,5)
        # Undo/Redo events
        self._te.undoAvailable.connect(btn_undo.setEnabled)
        self._te.redoAvailable.connect(btn_redo.setEnabled)
        btn_undo.clicked.connect(self._te.undo)
        btn_redo.clicked.connect(self._te.redo)

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

        self._te.currentColorChanged.connect(_currentColorChangedCB)

        def _setStyle():
            color = ttk.TTkColor()
            if cb_fg.checkState() == ttk.TTkK.Checked:
                color += btn_fgColor.color()
            if cb_bg.checkState() == ttk.TTkK.Checked:
                color += btn_bgColor.color()
            cursor = self._te.textCursor()
            cursor.applyColor(color)
            cursor.setColor(color)
            self._te.setFocus()

        cb_fg.toggled.connect(btn_fgColor.setEnabled)
        cb_bg.toggled.connect(btn_bgColor.setEnabled)
        cb_fg.clicked.connect(_setStyle)
        cb_bg.clicked.connect(_setStyle)

        cb_linenumber.toggled.connect(self._te.setLineNumber)

        btn_fgColor.colorSelected.connect(_setStyle)
        btn_bgColor.colorSelected.connect(_setStyle)

        lineWrap.setCurrentIndex(0)
        wordWrap.setCurrentIndex(1)

        fixWidth.valueChanged.connect(self._te.setWrapWidth)

        @ttk.pyTTkSlot(int)
        def _lineWrapCallback(index):
            if index == 0:
                self._te.setLineWrapMode(ttk.TTkK.NoWrap)
                wordWrap.setDisabled()
                fixWidth.setDisabled()
            elif index == 1:
                self._te.setLineWrapMode(ttk.TTkK.WidgetWidth)
                wordWrap.setEnabled()
                fixWidth.setDisabled()
            else:
                self._te.setLineWrapMode(ttk.TTkK.FixedWidth)
                self._te.setWrapWidth(fixWidth.value())
                wordWrap.setEnabled()
                fixWidth.setEnabled()

        lineWrap.currentIndexChanged.connect(_lineWrapCallback)

        @ttk.pyTTkSlot(int)
        def _wordWrapCallback(index):
            if index == 0:
                self._te.setWordWrapMode(ttk.TTkK.WordWrap)
            else:
                self._te.setWordWrapMode(ttk.TTkK.WrapAnywhere)

        wordWrap.currentIndexChanged.connect(_wordWrapCallback)

        self._te.document().cursorPositionChanged.connect(self._cursorPositionChanged)

    @ttk.pyTTkSlot(ttk.TTkTextCursor)
    def _cursorPositionChanged(self, cursor):
        ch = cursor.positionChar()
        # color = cursor.positionColor()
        glbls.brush.setGlyph(ch)

    def te(self):
        return self._te
