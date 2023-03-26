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

root = ttk.TTk(title="Image Tool", layout=ttk.TTkGridLayout())

splitter = ttk.TTkSplitter(parent=root)
splitter.addWidget(fileTree:=ttk.TTkFileTree(path='tmp'), 15)
splitter.addWidget(mainSplitter := ttk.TTkSplitter(orientation=ttk.TTkK.VERTICAL))
mainSplitter.addWidget(sa := ttk.TTkScrollArea())
mainSplitter.addWidget(controlsWidget := ttk.TTkWidget(layout=ttk.TTkGridLayout()),6)
mainSplitter.addWidget(te := ttk.TTkTextEdit(lineNumber=True))
mainSplitter.addWidget(ttk.TTkLogViewer(),6)

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

propertiesFrame.layout().addWidget(ttk.TTkLabel(text='Resolution:'),0,0)
propertiesFrame.layout().addWidget(cb_resolution := ttk.TTkComboBox(),0,1)
propertiesFrame.layout().addWidget(b_export := ttk.TTkButton(text="\nExport",),1,0,1,2)
# propertiesFrame.layout().addItem(ttk.TTkLayout(),3,0,1,2)

cb_resolution.addItems(['FULLBLOCK','HALFBLOCK','QUADBLOCK'])
cb_resolution.setCurrentIndex(2)


# te.setLineWrapMode(ttk.TTkK.WidgetWidth)
# te.setWordWrapMode(ttk.TTkK.WordWrap)
te.setReadOnly(False)

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
    rgbList = [(r*a//255,g*a//255,b*a//255) for r,g,b,a in data]

    imageList = [rgbList[i:i+width] for i in range(0, len(rgbList), width)]
    ttkImage.setData(imageList)

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
    rgbList = [(r*a//255,g*a//255,b*a//255) for r,g,b,a in data]
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

    #pilImage.size
    #pilImage.size

fileTree.fileActivated.connect(lambda x: _openFile(x.path()))

root.mainloop()