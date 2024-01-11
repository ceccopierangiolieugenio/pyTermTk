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
import TermTk as ttk

def QuickExport(data):
    newWindow = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../tui/quickExport.tui.json"))
    te = newWindow.getWidgetByName("TextEdit")

    ttk.pyTTkSlot()
    def _useNormmal():
        te.setLineWrapMode(ttk.TTkK.WidgetWidth)
        te.setWordWrapMode(ttk.TTkK.WordWrap)
        te.setText('from TermTk import TTkUtil, TTkUiLoader, TTk\n')
        te.append(f'# Data generated using ttkDesigner')
        te.append('widget = TTkUiLoader.loadDict(')
        te.append(str(data)+ ')')
        te.append('\nroot=TTk()\nroot.layout().addWidget(widget)\nroot.mainloop()\n')

    ttk.pyTTkSlot()
    def _useCompressed():
        te.setLineWrapMode(ttk.TTkK.NoWrap)
        b64str = ttk.TTkUtil.obj_inflate_2_base64(data)
        te.setText('from TermTk import TTkUtil, TTkUiLoader, TTk\n')
        te.append(f'# Data generated using ttkDesigner')
        te.append('widget = TTkUiLoader.loadDict(TTkUtil.base64_deflate_2_obj(')
        b64list = '    "' + '" +\n    "'.join([b64str[i:i+128] for i in range(0,len(b64str),128)]) + '"))'
        te.append(b64list)
        te.append('\nroot=TTk()\nroot.layout().addWidget(widget)\nroot.mainloop()\n')

    def _saveToFile(fileName):
        ttk.TTkLog.info(f"Saving to: {fileName}")
        with open(fileName,'w') as fp:
             fp.write(te.toPlainText())
        newWindow.close()

    ttk.pyTTkSlot(str)
    def _checkSaveFile(fileName):
        if os.path.exists(fileName):
            messageBox = ttk.TTkMessageBox(
                text= (
                    ttk.TTkString( f'A file named "{os.path.basename(fileName)}" already exists.\nDo you want to replace it?', ttk.TTkColor.BOLD) +
                    ttk.TTkString( f'\n\nReplacing it will overwrite its contents.') ),
                icon=ttk.TTkMessageBox.Icon.Warning,
                standardButtons=ttk.TTkMessageBox.StandardButton.Discard|ttk.TTkMessageBox.StandardButton.Save|ttk.TTkMessageBox.StandardButton.Cancel)
            messageBox.buttonSelected.connect(lambda btn : _saveToFile(fileName) if btn == ttk.TTkMessageBox.StandardButton.Save else None)
            ttk.TTkHelper.overlay(None, messageBox, 5, 5, True)
        else:
            _saveToFile(fileName)

    newWindow.getWidgetByName("BtnNormal").clicked.connect(_useNormmal)
    newWindow.getWidgetByName("BtnCompressed").clicked.connect(_useCompressed)
    newWindow.getWidgetByName("BtnSave").filePicked.connect(_checkSaveFile)
    _useCompressed()

    return newWindow
