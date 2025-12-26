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

'''savetools.py

Cross-platform file operations and clipboard management for pyTermTk.

This module provides a unified interface for file I/O operations that work seamlessly
across different platforms, including native desktop environments and web-based
Pyodide/WASM deployments. It automatically detects the runtime environment and
adapts its behavior accordingly.

Key Features:
    - **Cross-platform file operations**: Open, save, and saveAs methods that work
      identically on desktop and web platforms
    - **Multiple encoding support**: Text, JSON, and image formats with automatic
      decoding and encoding
    - **Drag and drop integration**: Native drag-drop support in web environments
    - **File dialog integration**: Automatic file picker dialogs on desktop with
      JavaScript-based file selection in browsers
    - **Image handling**: PIL/Pillow integration for image file operations
    - **Type-safe callbacks**: Protocol-based type hints for callback functions

Platform Detection:
    The module automatically detects whether it's running in a Pyodide/WASM environment
    by checking for the 'pyodideProxy' module. Based on this detection, it provides
    platform-specific implementations while maintaining a consistent API.

    - **Desktop mode**: Uses native file dialogs (:py:class:`TTkFileDialogPicker`) and
      standard Python file I/O
    - **Web mode**: Uses JavaScript interop via pyodideProxy for browser-based file
      selection and download

Usage Example:
    .. code-block:: python

        from TermTk.TTkCrossTools import TTkCrossTools

        # Open a text file
        def handle_open(data: TTkCrossTools.CB_Data_Open):
            print(f"Opened: {data.name}")
            print(f"Content: {data.data}")

        TTkCrossTools.open(
            path=".",
            encoding=TTkCrossTools.Encoding.TEXT_PLAIN,
            filter="Text Files (*.txt)",
            cb=handle_open
        )

        # Save a file
        TTkCrossTools.save(
            filePath="output.txt",
            content="Hello, World!",
            encoding=TTkCrossTools.Encoding.TEXT_PLAIN
        )

        # Save with dialog
        def handle_save(data: TTkCrossTools.CB_Data_Save):
            print(f"Saved to: {data.name}")

        TTkCrossTools.saveAs(
            filePath="output.json",
            content='{"key": "value"}',
            encoding=TTkCrossTools.Encoding.APPLICATION_JSON,
            filter="JSON Files (*.json)",
            cb=handle_save
        )

Supported Encodings:
    See :py:class:`TTkCrossTools.Encoding` for the full list of supported MIME types and
    encoding formats.

Callback Data Structures:
    - :py:class:`_CB_Data_Open`: Contains file name and decoded content
    - :py:class:`_CB_Data_Save`: Contains the saved file name

See Also:
    - :py:class:`TTkCrossTools`: Main API class
    - :py:class:`TTkCrossTools.Encoding`: Encoding type definitions
    - :py:class:`TTkFileDialogPicker`: Native file dialog widget
'''

from __future__ import annotations

__all__ = ['TTkCrossTools', '_TTkEncoding']

import os
import importlib.util
from enum import Enum
from dataclasses import dataclass

from typing import Callable,Optional,List,Tuple,Dict,Any,Protocol,Type

try:
    from typing import TypeAlias
except ImportError:
    # TODO: Remove this workaround for Python 3.9
    TypeAlias = type  # Fallback for Python < 3.10 without typing_extensions

from TermTk import pyTTkSlot, pyTTkSignal
from TermTk import TTkLog
from TermTk import TTkMessageBox, TTkFileDialogPicker, TTkHelper, TTkString, TTkK, TTkColor

class _TTkEncoding(str, Enum):
    ''' Encoding types for cross-platform file operations.

    Defines MIME types and encoding identifiers used by :py:class:`TTkCrossTools`
    for file operations. These encodings determine how file content is decoded
    when opening and encoded when saving.

    Text Encodings:
        - **TEXT**: Generic text encoding
        - **TEXT_PLAIN**: Plain text MIME type
        - **TEXT_PLAIN_UTF8**: UTF-8 encoded plain text

    Application Encodings:
        - **APPLICATION**: Generic application data
        - **APPLICATION_JSON**: JSON format with automatic parsing

    Image Encodings:
        - **IMAGE**: Generic image format
        - **IMAGE_PNG**: PNG image format
        - **IMAGE_SVG**: SVG vector image format
        - **IMAGE_JPG**: JPEG image format

    Note:
        Image encodings require PIL/Pillow to be installed. When opening image
        files, the decoded data will be a PIL Image object.
    '''
    TEXT             = "text"
    TEXT_PLAIN       = "text/plain"
    TEXT_PLAIN_UTF8  = "text/plain;charset=utf-8"
    APPLICATION      = 'application'
    APPLICATION_JSON = 'application/json'
    IMAGE     = 'image'
    IMAGE_PNG = 'image/png'
    IMAGE_SVG = 'image/svg+xml'
    IMAGE_JPG = 'image/jpeg'

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

@dataclass
class _CB_Data_Save():
    ''' Callback data for save operations.

    :param name: The full path or name of the saved file
    :type name: str
    '''
    name:str

@dataclass
class _CB_Data_Open():
    ''' Callback data for open/load operations.

    :param name: The full path or name of the opened file
    :type name: str
    :param data: The decoded file content. Type depends on the encoding:
                 - Text encodings: str
                 - JSON encodings: str (raw JSON content)
                 - Image encodings: PIL.Image.Image object
    :type data: Any
    '''
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
    ''' Cross-platform file operations and clipboard management.

    Provides a unified API for file I/O operations across desktop and web platforms.
    Automatically adapts to the runtime environment (native Python or Pyodide/WASM)
    and provides appropriate file dialogs and file handling mechanisms.

    Class Attributes:
        Encoding: Alias for :py:class:`_TTkEncoding` enum
        CB_Data_Save: Type alias for save callback data
        CB_Data_Open: Type alias for open callback data
        TTkCross_Callback: Generic callback type
        TTkCross_Callback_Open: Callback type for open operations
        TTkCross_Callback_Save: Callback type for save operations

    Methods:
        open: Open a file with automatic dialog and decoding
        save: Save content to a file
        saveAs: Save with file picker dialog
        ttkEmitDragOpen: Emit drag-drop open events (web only)
        ttkEmitFileOpen: Emit file open events (web only)
        ttkConnectDragOpen: Connect to drag-drop events (web only)

    Platform Behavior:
        **Desktop Mode**:
            - Uses :py:class:`TTkFileDialogPicker` for file selection
            - Direct filesystem access via Python's built-in file operations
            - Automatic confirmation dialogs for overwrite operations

        **Web Mode (Pyodide)**:
            - Uses JavaScript file input elements via pyodideProxy
            - Downloads trigger browser's save dialog
            - Drag-drop integration for file loading

    Usage Example:
        .. code-block:: python

            # Open a text file
            def on_open(data: TTkCrossTools.CB_Data_Open):
                print(f"File: {data.name}")
                print(f"Content: {data.data}")

            TTkCrossTools.open(
                path="/home/user",
                encoding=TTkCrossTools.Encoding.TEXT_PLAIN,
                filter="Text Files (*.txt);;All Files (*)",
                cb=on_open
            )

            # Save with confirmation
            def on_save(data: TTkCrossTools.CB_Data_Save):
                print(f"Saved to: {data.name}")

            TTkCrossTools.saveAs(
                filePath="document.txt",
                content="Hello, World!",
                encoding=TTkCrossTools.Encoding.TEXT_PLAIN,
                filter="Text Files (*.txt)",
                cb=on_save
            )

            # Open an image
            def on_image(data: TTkCrossTools.CB_Data_Open):
                pil_image = data.data  # PIL.Image.Image object
                print(f"Image size: {pil_image.size}")

            TTkCrossTools.open(
                path=".",
                encoding=TTkCrossTools.Encoding.IMAGE_PNG,
                filter="PNG Images (*.png)",
                cb=on_image
            )

    Note:
        Image operations require PIL/Pillow to be installed. The library will
        gracefully handle missing dependencies by skipping image operations.
    '''
    Encoding = _TTkEncoding
    CB_Data_Save: TypeAlias = _CB_Data_Save
    CB_Data_Open: TypeAlias = _CB_Data_Open

    # Type alias for callback functions that receive file data
    TTkCross_Callback: TypeAlias = Callable[[Dict[str, Any]], None]
    TTkCross_Callback_Open: TypeAlias = Callable[[CB_Data_Open], None]
    TTkCross_Callback_Save: TypeAlias = Callable[[CB_Data_Save], None]



    open: _OpenProtocol = _open
    save: _SaveProtocol = _save
    saveAs: _SaveAsProtocol = _saveAs
    ttkEmitDragOpen: _EmitDragOpenProtocol = _emitDragOpen
    ttkEmitFileOpen: _EmitFileOpenProtocol = _emitFileOpen
    ttkConnectDragOpen: _ConnectDragOpenProtocol = _connectDragOpen
