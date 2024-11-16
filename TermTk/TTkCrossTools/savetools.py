# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = [
        'ttkCrossOpen',
        'ttkCrossSave', 'ttkCrossSaveAs',
        'TTkEncoding', 'ImageData',
        'ttkConnectDragOpen',
        'ttkEmitDragOpen', 'ttkEmitFileOpen']

import os
import importlib.util
import json
from dataclasses import dataclass

from TermTk import pyTTkSlot, pyTTkSignal
from TermTk import TTkLog
from TermTk import TTkMessageBox, TTkFileDialogPicker, TTkHelper, TTkString, TTkK, TTkColor

class ImageData:
    size:list[int,int] = (0,0)
    data:list[list[list[int,int,int,int]]] = []

ttkCrossOpen       = None
ttkCrossSave       = None
ttkCrossSaveAs     = None
ttkEmitDragOpen    = None
ttkEmitFileOpen    = None
ttkConnectDragOpen = None

class TTkEncoding(str):
    TEXT             = "text"
    TEXT_PLAIN       = "text/plain"
    TEXT_PLAIN_UTF8  = "text/plain;charset=utf-8"
    APPLICATION      = 'application'
    APPLICATION_JSON = 'application/json'
    IMAGE     = 'image'
    IMAGE_PNG = 'image/png'
    IMAGE_SVG = 'image/svg+xml'
    IMAGE_JPG = 'image/jpeg'

if importlib.util.find_spec('pyodideProxy'):
    TTkLog.info("Using 'pyodideProxy' as clipboard manager")
    import pyodideProxy
    ttkDragOpen    = {}
    ttkFileOpen    = pyTTkSignal(dict)

    def _open(path, encoding, filter, cb=None):
        if not cb: return
        ttkFileOpen.connect(cb)
        pyodideProxy.openFile(encoding)

    def _save(filePath, content, encoding, filter=None, cb=lambda _d:None):
        pyodideProxy.saveFile(os.path.basename(filePath), content, encoding)

    def _connectDragOpen(encoding, cb):
        if encoding not in ttkDragOpen:
            ttkDragOpen[encoding] = pyTTkSignal(dict)
        return ttkDragOpen[encoding].connect(cb)

    def _emitDragOpen(encoding, data):
        if encoding.startswith(TTkEncoding.IMAGE):
            from PIL import Image
            import io
            im = Image.open(io.BytesIO(data['data']))
            data['data'] = im
        for do in [ttkDragOpen[e] for e in ttkDragOpen if encoding.startswith(e)]:
            do.emit(data)

    def _emitFileOpen(encoding, data):
        if encoding.startswith(TTkEncoding.IMAGE):
            from PIL import Image
            import io
            # TTkLog.debug(data['data'])
            # TTkLog.debug(type(data['data']))
            # Image.open(data['data'])
            im = Image.open(io.BytesIO(data['data']))
            # TTkLog.debug(f"{im.size}")
            data['data'] = im
        ttkFileOpen.emit(data)
        ttkFileOpen.clear()

    ttkCrossOpen    = _open
    ttkCrossSave    = _save
    ttkCrossSaveAs  = _save
    ttkEmitDragOpen = _emitDragOpen
    ttkEmitFileOpen = _emitFileOpen
    ttkConnectDragOpen  = _connectDragOpen

else:
    def _crossDecoder_text(fileName) :
        with open(fileName) as fp:
            return fp.read()
    def _crossDecoder_json(fileName) :
        with open(fileName) as fp:
            # return json.load(fp)
            return fp.read()
    def _crossDecoder_image(fileName):
        from PIL import Image
        pilImage = Image.open(fileName)
        # pilImage = pilImage.convert('RGBA')
        # pilData = list(pilImage.getdata())
        # data = ImageData()
        # w,h = data.size = pilImage.size
        # data.data = [pilData[i:i+w] for i in range(0, len(pilData), w)]
        return pilImage

    _crossDecoder = {
        TTkEncoding.TEXT             : _crossDecoder_text ,
        TTkEncoding.TEXT_PLAIN       : _crossDecoder_text ,
        TTkEncoding.TEXT_PLAIN_UTF8  : _crossDecoder_text ,
        TTkEncoding.APPLICATION      : _crossDecoder_json ,
        TTkEncoding.APPLICATION_JSON : _crossDecoder_json ,
        TTkEncoding.IMAGE            : _crossDecoder_image ,
        TTkEncoding.IMAGE_PNG        : _crossDecoder_image ,
        TTkEncoding.IMAGE_SVG        : _crossDecoder_image ,
        TTkEncoding.IMAGE_JPG        : _crossDecoder_image ,
    }

    def _open(path, encoding:TTkEncoding, filter:str, cb=None):
        if not cb: return
        if encoding.startswith(TTkEncoding.IMAGE):
            if not importlib.util.find_spec('PIL'): return
        def __openFile(fileName):
            _decoder = _crossDecoder.get(encoding,lambda _:None)
            content = _decoder(fileName)
            cb({'name':fileName, 'data':content})
        filePicker = TTkFileDialogPicker(pos = (3,3), size=(100,30), caption="Open", path=path, fileMode=TTkK.FileMode.ExistingFile ,filter=filter)
        filePicker.pathPicked.connect(__openFile)
        TTkHelper.overlay(None, filePicker, 5, 5, True)

    def _save(filePath, content, encoding):
        TTkLog.info(f"Saving to: {filePath}")
        with open(filePath,'w') as fp:
            fp.write(content)

    def _saveAs(filePath, content, encoding, filter, cb=lambda _d:None):
        def _approveFile(fileName):
            if os.path.exists(fileName):
                @pyTTkSlot(TTkMessageBox.StandardButton)
                def _cb(btn):
                    if btn == TTkMessageBox.StandardButton.Save:
                        ttkCrossSave(fileName,content,encoding)
                    elif btn == TTkMessageBox.StandardButton.Cancel:
                        return
                    if cb:
                        cb({'name':fileName})
                messageBox = TTkMessageBox(
                    text= (
                        TTkString( f'A file named "{os.path.basename(fileName)}" already exists.\nDo you want to replace it?', TTkColor.BOLD) +
                        TTkString( f'\n\nReplacing it will overwrite its contents.') ),
                    icon=TTkMessageBox.Icon.Warning,
                    standardButtons=TTkMessageBox.StandardButton.Discard|TTkMessageBox.StandardButton.Save|TTkMessageBox.StandardButton.Cancel)
                messageBox.buttonSelected.connect(_cb)
                TTkHelper.overlay(None, messageBox, 5, 5, True)
            else:
                ttkCrossSave(fileName,content,encoding)
                if cb:
                    cb({'name':fileName})
        filePicker = TTkFileDialogPicker(
                        size=(100,30), path=filePath,
                        acceptMode=TTkK.AcceptMode.AcceptSave,
                        caption="Save As...",
                        fileMode=TTkK.FileMode.AnyFile ,
                        filter=filter)
        filePicker.pathPicked.connect(_approveFile)
        TTkHelper.overlay(None, filePicker, 5, 5, True)

    ttkCrossOpen       = _open
    ttkCrossSave       = _save
    ttkCrossSaveAs     = _saveAs
    ttkEmitDragOpen    = lambda a:None
    ttkEmitFileOpen    = lambda a:None
    ttkConnectDragOpen = lambda a,b:None
