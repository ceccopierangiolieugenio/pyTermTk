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

from __future__ import annotations

__all__ = ['TTkCrossTools', '_TTkEncoding']

import os
import importlib.util
from enum import Enum
from dataclasses import dataclass

from typing import Callable,Optional,List,Tuple,Dict,Any,Protocol,Type,TypeAlias

from TermTk import pyTTkSlot, pyTTkSignal
from TermTk import TTkLog
from TermTk import TTkMessageBox, TTkFileDialogPicker, TTkHelper, TTkString, TTkK, TTkColor

class _TTkEncoding(str, Enum):
    TEXT             = "text"
    TEXT_PLAIN       = "text/plain"
    TEXT_PLAIN_UTF8  = "text/plain;charset=utf-8"
    APPLICATION      = 'application'
    APPLICATION_JSON = 'application/json'
    IMAGE     = 'image'
    IMAGE_PNG = 'image/png'
    IMAGE_SVG = 'image/svg+xml'
    IMAGE_JPG = 'image/jpeg'

@dataclass
class _CB_Data_Save():
    name:str

@dataclass
class _CB_Data_Open():
    name:str
    data:Any


if importlib.util.find_spec('pyodideProxy'):
    TTkLog.info("Using 'pyodideProxy' as clipboard manager")
    import pyodideProxy  # type: ignore[import-not-found]
    ttkDragOpen:Dict[_TTkEncoding,pyTTkSignal] = {}
    ttkFileOpen    = pyTTkSignal(_CB_Data_Open)

    def _open(path:str, encoding:_TTkEncoding, filter:str, cb: Optional[TTkCrossTools.TTkCross_Callback_Open] = None) -> None:
        if not cb: return
        ttkFileOpen.connect(cb)
        pyodideProxy.openFile(encoding)

    def _save(filePath: str, content: str, encoding: _TTkEncoding) -> None:
        pyodideProxy.saveFile(os.path.basename(filePath), content, encoding)

    def _saveAs(filePath:str, content:str, encoding:_TTkEncoding, filter:str, cb: Optional[TTkCrossTools.TTkCross_Callback_Save] = None) -> None:
        return _save(
            filePath=filePath,
            content=content,
            encoding=encoding
        )

    def _emitDragOpen(encoding: _TTkEncoding, data: _CB_Data_Open) -> None:
        if encoding.startswith(_TTkEncoding.IMAGE):
            from PIL import Image
            import io
            im = Image.open(io.BytesIO(data.data))
            data.data = im
        for _drag_open in [ttkDragOpen[e] for e in ttkDragOpen if encoding.startswith(e)]:
            _drag_open.emit(data)

    def _emitFileOpen(encoding: _TTkEncoding, data: _CB_Data_Open) -> None:
        if encoding.startswith(_TTkEncoding.IMAGE):
            from PIL import Image
            import io
            # TTkLog.debug(data['data'])
            # TTkLog.debug(type(data['data']))
            # Image.open(data['data'])
            im = Image.open(io.BytesIO(data.data))
            # TTkLog.debug(f"{im.size}")
            data.data = im
        ttkFileOpen.emit(data)
        ttkFileOpen.clear()

    def _connectDragOpen(encoding: _TTkEncoding, cb: TTkCrossTools.TTkCross_Callback_Open) -> None:
        if encoding not in ttkDragOpen:
            ttkDragOpen[encoding] = pyTTkSignal(_CB_Data_Open)
        return ttkDragOpen[encoding].connect(cb)

else:
    def _crossDecoder_text(fileName: str) -> str:
        with open(fileName) as fp:
            return fp.read()

    def _crossDecoder_json(fileName: str) -> str:
        with open(fileName) as fp:
            # return json.load(fp)
            return fp.read()

    def _crossDecoder_image(fileName: str) -> Any:
        from PIL import Image
        pilImage = Image.open(fileName)
        # pilImage = pilImage.convert('RGBA')
        # pilData = List(pilImage.getdata())
        # data = ImageData()
        # w,h = data.size = pilImage.size
        # data.data = [pilData[i:i+w] for i in range(0, len(pilData), w)]
        return pilImage

    _crossDecoder = {
        _TTkEncoding.TEXT             : _crossDecoder_text ,
        _TTkEncoding.TEXT_PLAIN       : _crossDecoder_text ,
        _TTkEncoding.TEXT_PLAIN_UTF8  : _crossDecoder_text ,
        _TTkEncoding.APPLICATION      : _crossDecoder_json ,
        _TTkEncoding.APPLICATION_JSON : _crossDecoder_json ,
        _TTkEncoding.IMAGE            : _crossDecoder_image ,
        _TTkEncoding.IMAGE_PNG        : _crossDecoder_image ,
        _TTkEncoding.IMAGE_SVG        : _crossDecoder_image ,
        _TTkEncoding.IMAGE_JPG        : _crossDecoder_image ,
    }

    def _open(path:str, encoding:_TTkEncoding, filter:str, cb: Optional[TTkCrossTools.TTkCross_Callback_Open] = None) -> None:
        if not cb: return
        if encoding.startswith(_TTkEncoding.IMAGE):
            if not importlib.util.find_spec('PIL'): return
        def __openFile(fileName: str) -> None:
            _decoder = _crossDecoder.get(encoding,lambda _:None)
            content = _decoder(fileName)
            cb(TTkCrossTools.CB_Data_Open(name=fileName, data=content))
        filePicker = TTkFileDialogPicker(pos = (3,3), size=(100,30), caption="Open", path=path, fileMode=TTkK.FileMode.ExistingFile ,filter=filter)
        filePicker.pathPicked.connect(__openFile)
        TTkHelper.overlay(None, filePicker, 5, 5, True)

    def _save(filePath:str, content:str, encoding:_TTkEncoding) -> None:
        TTkLog.info(f"Saving to: {filePath}")
        with open(filePath,'w') as fp:
            fp.write(content)

    def _saveAs(filePath:str, content:str, encoding:_TTkEncoding, filter:str, cb: Optional[TTkCrossTools.TTkCross_Callback_Save] = None) -> None:
        def _approveFile(fileName: str) -> None:
            if os.path.exists(fileName):
                @pyTTkSlot(TTkMessageBox.StandardButton)
                def _cb(btn):
                    if btn == TTkMessageBox.StandardButton.Save:
                        _save(fileName,content,encoding)
                    elif btn == TTkMessageBox.StandardButton.Cancel:
                        return
                    if cb:
                        cb(TTkCrossTools.CB_Data_Save(name=fileName))
                messageBox = TTkMessageBox(
                    text= (
                        TTkString( f'A file named "{os.path.basename(fileName)}" already exists.\nDo you want to replace it?', TTkColor.BOLD) +
                        TTkString( f'\n\nReplacing it will overwrite its contents.') ),
                    icon=TTkMessageBox.Icon.Warning,
                    standardButtons=TTkMessageBox.StandardButton.Discard|TTkMessageBox.StandardButton.Save|TTkMessageBox.StandardButton.Cancel)
                messageBox.buttonSelected.connect(_cb)
                TTkHelper.overlay(None, messageBox, 5, 5, True)
            else:
                _save(fileName,content,encoding)
                if cb:
                    cb(TTkCrossTools.CB_Data_Save(name=fileName))
        filePicker = TTkFileDialogPicker(
                        size=(100,30), path=filePath,
                        acceptMode=TTkK.AcceptMode.AcceptSave,
                        caption="Save As...",
                        fileMode=TTkK.FileMode.AnyFile ,
                        filter=filter)
        filePicker.pathPicked.connect(_approveFile)
        TTkHelper.overlay(None, filePicker, 5, 5, True)

    def _emitDragOpen(encoding: _TTkEncoding, data: _CB_Data_Open) -> None:
        pass

    def _emitFileOpen(encoding: _TTkEncoding, data: _CB_Data_Open) -> None:
        pass

    def _connectDragOpen(encoding: _TTkEncoding, cb: TTkCrossTools.TTkCross_Callback_Open) -> None:
        pass


class TTkCrossTools():
    Encoding = _TTkEncoding
    CB_Data_Save: TypeAlias = _CB_Data_Save
    CB_Data_Open: TypeAlias = _CB_Data_Open

    # Type alias for callback functions that receive file data
    TTkCross_Callback: TypeAlias = Callable[[Dict[str, Any]], None]
    TTkCross_Callback_Open: TypeAlias = Callable[[CB_Data_Open], None]
    TTkCross_Callback_Save: TypeAlias = Callable[[CB_Data_Save], None]

    class _OpenProtocol(Protocol):
        def __call__(
                self,
                path: str,
                encoding: _TTkEncoding,
                filter: str,
                cb: Optional[TTkCrossTools.TTkCross_Callback_Open] = None
            ) -> None: ...

    class _SaveProtocol(Protocol):
        def __call__(
                self,
                filePath: str,
                content: str,
                encoding: _TTkEncoding
            ) -> None: ...

    class _SaveAsProtocol(Protocol):
        def __call__(
                self,
                filePath: str,
                content: str,
                encoding: _TTkEncoding,
                filter: str,
                cb: Optional[TTkCrossTools.TTkCross_Callback_Save] = None
            ) -> None: ...

    class _EmitDragOpenProtocol(Protocol):
        def __call__(
                self,
                encoding: _TTkEncoding,
                data: _CB_Data_Open
            ) -> None: ...

    class _EmitFileOpenProtocol(Protocol):
        def __call__(
                self,
                encoding: _TTkEncoding,
                data: _CB_Data_Open
            ) -> None: ...

    class _ConnectDragOpenProtocol(Protocol):
        def __call__(
                self,
                encoding: _TTkEncoding,
                cb: TTkCrossTools.TTkCross_Callback_Open
            ) -> None: ...

    open: _OpenProtocol = _open
    save: _SaveProtocol = _save
    saveAs: _SaveAsProtocol = _saveAs
    ttkEmitDragOpen: _EmitDragOpenProtocol = _emitDragOpen
    ttkEmitFileOpen: _EmitFileOpenProtocol = _emitFileOpen
    ttkConnectDragOpen: _ConnectDragOpenProtocol = _connectDragOpen
