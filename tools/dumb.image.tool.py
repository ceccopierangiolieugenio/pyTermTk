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
from PIL import Image
import zlib, pickle, base64

import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

ttk.TTkTheme.loadTheme(ttk.TTkTheme.NERD)

class Ansieditor(ttk.TTkGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._te = ttk.TTkTextEdit(lineNumber=True, readOnly=False)
        self._te.setText(ttk.TTkString("Ansi editor\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD+ttk.TTkColor.ITALIC))

        self.addItem(wrapLayout := ttk.TTkGridLayout(), 0,0)
        self.addItem(fontLayout := ttk.TTkGridLayout(columnMinWidth=1), 1,0)
        self.addWidget(self._te,2,0,1,2)

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
        fontLayout.addWidget(btn_undo := ttk.TTkButton(border=True, maxSize=(8,3), enabled=self._te.isUndoAvailable(), text=' UNDO '),1,9 )
        fontLayout.addWidget(btn_redo := ttk.TTkButton(border=True, maxSize=(8,3), enabled=self._te.isRedoAvailable(), text=' REDO '),1,10)
        # Undo/Redo events
        self._te.undoAvailable.connect(btn_undo.setEnabled)
        self._te.redoAvailable.connect(btn_redo.setEnabled)
        btn_undo.clicked.connect(self._te.undo)
        btn_redo.clicked.connect(self._te.redo)

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

        self._te.currentColorChanged.connect(_currentColorChangedCB)

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
            cursor = self._te.textCursor()
            cursor.applyColor(color)
            cursor.setColor(color)
            self._te.setFocus()

        cb_fg.stateChanged.connect(lambda x: btn_fgColor.setEnabled(x==ttk.TTkK.Checked))
        cb_bg.stateChanged.connect(lambda x: btn_bgColor.setEnabled(x==ttk.TTkK.Checked))
        cb_fg.clicked.connect(lambda _: _setStyle())
        cb_bg.clicked.connect(lambda _: _setStyle())

        cb_linenumber.stateChanged.connect(lambda x: self._te.setLineNumber(x==ttk.TTkK.Checked))

        btn_fgColor.colorSelected.connect(lambda _: _setStyle())
        btn_bgColor.colorSelected.connect(lambda _: _setStyle())

        btn_bold.clicked.connect(_setStyle)
        btn_italic.clicked.connect(_setStyle)
        btn_underline.clicked.connect(_setStyle)
        btn_strikethrough.clicked.connect(_setStyle)

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

    def te(self):
        return self._te

class SigmaskTool(ttk.TTkGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.addWidget(cb_c := ttk.TTkCheckbox(text="CTRL-C (VINTR) ", checked=ttk.TTkK.Checked),1,0)
        self.addWidget(cb_s := ttk.TTkCheckbox(text="CTRL-S (VSTOP) ", checked=ttk.TTkK.Checked),2,0)
        self.addWidget(cb_z := ttk.TTkCheckbox(text="CTRL-Z (VSUSP) ", checked=ttk.TTkK.Checked),3,0)
        self.addWidget(cb_q := ttk.TTkCheckbox(text="CTRL-Q (VSTART)", checked=ttk.TTkK.Checked),4,0)

        cb_c.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_C,x==ttk.TTkK.Checked))
        cb_s.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_S,x==ttk.TTkK.Checked))
        cb_z.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_Z,x==ttk.TTkK.Checked))
        cb_q.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_Q,x==ttk.TTkK.Checked))

        self.addWidget(quitBtn := ttk.TTkButton(text="QUIT", border=True, maxHeight=3),5,0)
        quitBtn.clicked.connect(ttk.TTkHelper.quit)



root = ttk.TTk(title="Image Tool", layout=ttk.TTkGridLayout())

splitter = ttk.TTkSplitter(parent=root)
# splitter.addWidget(fileTree:=ttk.TTkFileTree(path='tmp'), 15)
splitter.addWidget(smt := SigmaskTool(), 25)
splitter.addWidget(mainSplitter := ttk.TTkSplitter(orientation=ttk.TTkK.VERTICAL))
mainSplitter.addWidget(imageSplitter := ttk.TTkSplitter(orientation=ttk.TTkK.HORIZONTAL))
mainSplitter.addWidget(controlsWidget := ttk.TTkWidget(layout=ttk.TTkGridLayout()),6)
mainSplitter.addWidget(te := ttk.TTkTextEdit(lineNumber=True, readOnly=False))
mainSplitter.addWidget(ttk.TTkLogViewer(),6)

smt.addWidget(fileTree:=ttk.TTkFileTree(path='tmp'),0,0)




imageSplitter.addWidget(sa       := ttk.TTkScrollArea())
imageSplitter.addWidget(ansiEdit := Ansieditor())

controlsWidget.layout().addWidget(resizeFrame := ttk.TTkFrame(title='Resize',layout=ttk.TTkGridLayout()))
controlsWidget.layout().addWidget(propertiesFrame := ttk.TTkFrame(title='Image Properties',layout=ttk.TTkGridLayout()))

resizeFrame.layout().addWidget(ttk.TTkLabel(text='Width:'   ),0,0)
resizeFrame.layout().addWidget(b_width  := ttk.TTkSpinBox(maximum=0x1000),0,1)
resizeFrame.layout().addWidget(ttk.TTkLabel(text='Height:'  ),1,0)
resizeFrame.layout().addWidget(b_height := ttk.TTkSpinBox(maximum=0x1000),1,1)
resizeFrame.layout().addWidget(ttk.TTkLabel(text='Resample:'),2,0)
resizeFrame.layout().addWidget(cb_resample := ttk.TTkComboBox(),2,1)

resizeFrame.layout().addWidget(b_ttkAR  := ttk.TTkButton(text='TermTk A/R', border=True),0,2,3,1)
resizeFrame.layout().addWidget(b_resize := ttk.TTkButton(text='Resize', border=True),    0,3,3,1)

cb_resample.addItems(['NEAREST','BOX','BILINEAR','HAMMING','BICUBIC','LANCZOS'])
cb_resample.setCurrentIndex(0)

propertiesFrame.layout().addWidget(ttk.TTkLabel(text='Resolution:'),        0,0)
propertiesFrame.layout().addWidget(cb_resolution := ttk.TTkComboBox(),      0,1)
propertiesFrame.layout().addWidget(ttk.TTkLabel(text='BgColor:'),           1,0)
propertiesFrame.layout().addWidget(b_color  := ttk.TTkColorButtonPicker(color=ttk.TTkColor.fg("#000000")),  1,1)
propertiesFrame.layout().addWidget(b_export := ttk.TTkButton(text="Export"),2,0,1,2)
# propertiesFrame.layout().addItem(ttk.TTkLayout(),3,0,1,2)

cb_resolution.addItems(['FULLBLOCK','HALFBLOCK','QUADBLOCK'])
cb_resolution.setCurrentIndex(2)

# te.setLineWrapMode(ttk.TTkK.WidgetWidth)
# te.setWordWrapMode(ttk.TTkK.WordWrap)

te.setText("Select an Image")

ttkImage = ttk.TTkImage(parent=sa.viewport(), pos=(0,0))
pilImage = None

def _export():
    if not ttkImage:
        return
    data = ttkImage._data
    te.setText("Image:")
    te.append("=============[Raw Data START]============")
    te.append(str(ttkImage._data).replace('],','],\n'))
    te.append("=============[Raw Data STOP]=============")
    # b64str = base64.b64encode(zlib.compress(bytearray(pickle.dumps(data)))).decode("ascii")
    b64str = ttk.TTkUtil.obj_inflate_2_base64(data)
    te.append('from TermTk import TTkUtil')
    te.append(f'# Data generated using {os.path.basename(__file__)}')
    te.append('data = TTkUtil.base64_deflate_2_obj(')
    b64list = '    "' + '" +\n    "'.join([b64str[i:i+128] for i in range(0,len(b64str),128)]) + '")'
    te.append(b64list)
    te.append(f'# ANSII {os.path.basename(__file__)}')
    # ansi = ttkImage.getCanvas().toAnsi()
    # te.append(ansi.replace('\033','<ESC>'))
    b64str = ttk.TTkUtil.obj_inflate_2_base64(ansiEdit.te().toAnsi())
    te.append('data = TTkUtil.base64_deflate_2_obj(')
    b64list = '    "' + '" +\n    "'.join([b64str[i:i+128] for i in range(0,len(b64str),128)]) + '")'
    te.append(b64list)

b_export.clicked.connect(_export)

def _resolutionChanged(res):
    newRes = {
        'FULLBLOCK' : ttk.TTkImage.FULLBLOCK,
        'HALFBLOCK' : ttk.TTkImage.HALFBLOCK,
        'QUADBLOCK' : ttk.TTkImage.QUADBLOCK
            }.get(res, ttk.TTkImage.QUADBLOCK)
    ttkImage.setRasteriser(newRes)

cb_resolution.currentTextChanged.connect(_resolutionChanged)


def _ttkAR():
    if not pilImage: return
    width, height = pilImage.size
    b_width.setValue(width)
    b_height.setValue(height//2)

b_ttkAR.clicked.connect(_ttkAR)

oldImages = []
def _resize():
    global pilImage
    if not pilImage: return
    width  = b_width.value()
    height = b_height.value()
    resample = {'NEAREST' : Image.NEAREST,
                'BOX' :     Image.BOX,
                'BILINEAR': Image.BILINEAR,
                'HAMMING' : Image.HAMMING,
                'BICUBIC' : Image.BICUBIC,
                'LANCZOS' : Image.LANCZOS}.get(
                    cb_resample.currentText,Image.NEAREST)
    pilImage = pilImage.resize((width,height),resample)
    data = list(pilImage.getdata())
    # rgbList = [(r,g,b) for r,g,b,a in data]
    br,bg,bb = b_color.color().bgToRGB()
    rgbList = [
        ((r*a+(255-a)*br)//255,
         (g*a+(255-a)*bg)//255,
         (b*a+(255-a)*bb)//255)
        for r,g,b,a in data]

    imageList = [rgbList[i:i+width] for i in range(0, len(rgbList), width)]
    ttkImage.setData(imageList)
    ansiEdit.te().setText(ttkImage.getCanvas().toAnsi())

b_resize.clicked.connect(_resize)

def _openFile(file):
    global pilImage
    pilImage = Image.open(file)
    pilImage = pilImage.convert('RGBA')
    te.setText(str(pilImage.size))
    te.append("data")
    #te.append(str(list(pilImage.getdata())))
    data = list(pilImage.getdata())
    # rgbList = list(zip(data[::3],data[1::3],data[2::3]))
    br,bg,bb = b_color.color().bgToRGB()
    rgbList = [
        ((r*a+(255-a)*br)//255,
         (g*a+(255-a)*bg)//255,
         (b*a+(255-a)*bb)//255)
        for r,g,b,a in data]
    te.append("rgbList")
    #te.append(str(rgbList))
    width, height = pilImage.size
    b_width.setValue(width)
    b_height.setValue(height)
    # imageList = [rgbList[i:i+width] for i in range(0, len(rgbList), width)]
    imageList = [rgbList[i:i+width] for i in range(0, len(rgbList), width)]
    te.append("imageList")
    #te.append(str(imageList))

    ttkImage.setData(imageList)
    ansiEdit.te().setText(ttkImage.getCanvas().toAnsi())

    #pilImage.size
    #pilImage.size

fileTree.fileActivated.connect(lambda x: _openFile(x.path()))

root.mainloop()