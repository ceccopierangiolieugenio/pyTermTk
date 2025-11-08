# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkTableProxyEdit', 'TTkTableEditLeaving', 'TTkTableProxyEditWidget']

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Protocol, Union, Tuple, Type, List, Optional, Any

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString, TTkStringType
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent

from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.texedit import TTkTextEdit, TTkTextEditView
from TermTk.TTkWidgets.spinbox import TTkSpinBox
from TermTk.TTkWidgets.TTkPickers.textpicker import TTkTextPicker

from TermTk.TTkGui.textcursor import TTkTextCursor

if TYPE_CHECKING:
    from TermTk.TTkWidgets.TTkModelView.tablewidget import TTkTableWidget

class TTkTableEditLeaving(Enum):
    ''' Enum indicating the direction the user is leaving the table cell editor

    Used by :py:class:`TTkTableProxyEditWidget` to signal navigation intent
    '''
    NONE   = auto()
    TOP    = auto()
    BOTTOM = auto()
    LEFT   = auto()
    RIGHT  = auto()


class TTkTableProxyEditWidget(TTkWidget):
    ''' Protocol for table cell editor widgets

    Any widget implementing these signals can be used as a table cell editor.
    The protocol ensures consistent behavior across different editor types.

    Example implementation::

        class MyEditor(TTkLineEdit):
            __slots__ = ('leavingTriggered', 'dataChanged')

            def __init__(self, **kwargs):
                self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
                self.dataChanged = pyTTkSignal(object)
                super().__init__(**kwargs)
                self.textChanged.connect(self.dataChanged.emit)
    '''

    leavingTriggered: pyTTkSignal
    '''
    This signal is emitted when the user navigates out of the editor

    :param direction: The direction of navigation
    :type direction: TTkTableEditLeaving
    '''

    dataChanged: pyTTkSignal
    '''
    This signal is emitted when the editor data changes

    :param data: The new data value
    :type data: object
    '''

    @staticmethod
    def editWidgetFactory( data:object) -> TTkTableProxyEditWidget:
        raise NotImplementedError()
    def getCellData(self) -> object:
        raise NotImplementedError()
    # def setCellData(self, data:object) -> None:
    #     raise NotImplementedError()
    def proxyDispose(self) -> None:
        self.leavingTriggered.clear()
        self.dataChanged.clear()
        self.close()

class _TextEditViewProxy(TTkTextEditView, TTkTableProxyEditWidget):
    ''' Text editor for table cells

    Extends :py:class:`~TermTk.TTkWidgets.texedit.TTkTextEdit` with table-specific signals
    for navigation and data change notification.
    '''
    __slots__ = ('leavingTriggered', 'dataChanged')

    leavingTriggered: pyTTkSignal
    '''
    This signal is emitted when the user navigates out of the editor

    :param direction: The direction of navigation
    :type direction: TTkTableEditLeaving
    '''

    setDataChanged: pyTTkSignal
    '''
    This signal is emitted when the text content changes

    :param data: The new text value
    :type data: Union[str, TTkString]
    '''

    def __init__(self, **kwargs):
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        super().__init__(**kwargs)
        self.textChanged.connect(self._emitDataChanged)

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        if ( evt.type == TTkK.SpecialKey):
            _cur = self.textCursor()
            _doc = self.document()
            _line = _cur.anchor().line
            _pos  = _cur.anchor().pos
            _lineCount = _doc.lineCount()
            # _lineLen
            if evt.mod==TTkK.NoModifier:
                if evt.key == TTkK.Key_Enter:
                    self.leavingTriggered.emit(TTkTableEditLeaving.BOTTOM)
                    return True
                elif evt.key == TTkK.Key_Up:
                    if _line == 0:
                        self.leavingTriggered.emit(TTkTableEditLeaving.TOP)
                        return True
                elif evt.key == TTkK.Key_Down:
                    if _lineCount == 1:
                        self.leavingTriggered.emit(TTkTableEditLeaving.BOTTOM)
                        return True
                elif evt.key == TTkK.Key_Left:
                    if _pos == _line == 0:
                        self.leavingTriggered.emit(TTkTableEditLeaving.LEFT)
                        return True
                elif evt.key == TTkK.Key_Right:
                    if _lineCount == 1 and _pos==len(_doc.toPlainText()):
                        self.leavingTriggered.emit(TTkTableEditLeaving.RIGHT)
                        return True
            elif ( evt.type == TTkK.SpecialKey and
                    evt.mod==TTkK.ControlModifier|TTkK.AltModifier and
                    evt.key == TTkK.Key_M ):
                evt.mod = TTkK.NoModifier
                evt.key = TTkK.Key_Enter
        return super().keyEvent(evt)

    @pyTTkSlot()
    def _emitDataChanged(self) -> None:
        ''' Emit dataChanged signal when text changes
        '''
        txt = self.toRawText()
        val = str(txt) if txt.isPlainText() else txt
        self.dataChanged.emit(val)

class _TextEditProxy(TTkTextEdit, TTkTableProxyEditWidget):
    ''' Text editor for table cells

    Extends :py:class:`~TermTk.TTkWidgets.texedit.TTkTextEdit` with table-specific signals
    for navigation and data change notification.
    '''
    __slots__ = ('leavingTriggered', 'dataChanged')

    leavingTriggered: pyTTkSignal
    '''
    This signal is emitted when the user navigates out of the editor

    :param direction: The direction of navigation
    :type direction: TTkTableEditLeaving
    '''

    setDataChanged: pyTTkSignal
    '''
    This signal is emitted when the text content changes

    :param data: The new text value
    :type data: Union[str, TTkString]
    '''

    def __init__(self, **kwargs):
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        tew = _TextEditViewProxy()
        super().__init__(**kwargs|{'textEditView':tew})
        tew.leavingTriggered.connect(self.leavingTriggered.emit)
        tew.dataChanged.connect(self.dataChanged.emit)

    @staticmethod
    def editWidgetFactory( data:Any) -> TTkTableProxyEditWidget:
        if not isinstance(data, (TTkString,str)):
            raise ValueError(f"{data} is not a TTkStringType")
        te = _TextEditProxy()
        te.setText(data)
        return te

    def getCellData(self) -> TTkStringType:
        txt = self.toRawText()
        val = str(txt) if txt.isPlainText() else txt
        return val

    # def setCellData(self, data:TTkStringType) -> None:
    #     self.setText(data)

class _SpinBoxProxy(TTkSpinBox, TTkTableProxyEditWidget):
    ''' Numeric editor for table cells

    Extends :py:class:`~TermTk.TTkWidgets.spinbox.TTkSpinBox` with table-specific signals
    for navigation and data change notification.
    '''
    __slots__ = ('leavingTriggered', 'dataChanged')

    leavingTriggered: pyTTkSignal
    '''
    This signal is emitted when the user navigates out of the editor

    :param direction: The direction of navigation
    :type direction: TTkTableEditLeaving
    '''

    dataChanged: pyTTkSignal
    '''
    This signal is emitted when the numeric value changes

    :param data: The new numeric value
    :type data: Union[int, float]
    '''

    def __init__(self, **kwargs):
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        super().__init__(**kwargs)
        self.valueChanged.connect(self.dataChanged.emit)

    @staticmethod
    def editWidgetFactory( data:Any) -> TTkTableProxyEditWidget:
        if not isinstance(data, (int,float)):
            raise ValueError(f"{data} is not a int or float")
        sb = _SpinBoxProxy(
            minimum=-1000000,
            maximum=1000000,
            value=data)
        return sb

    def getCellData(self) -> Union[float,int]:
        return self.value()

    # def setCellData(self, data:Union[float,int]) -> None:
    #     self.setValue(data)

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        if ( evt.type == TTkK.SpecialKey):
            if evt.mod==TTkK.NoModifier:
                if evt.key == TTkK.Key_Enter:
                    self.leavingTriggered.emit(TTkTableEditLeaving.RIGHT)
                    return True
        return super().keyEvent(evt)


class _TextPickerProxy(TTkTextPicker, TTkTableProxyEditWidget):
    ''' Rich text editor for table cells

    Extends :py:class:`~TermTk.TTkWidgets.TTkPickers.textpicker.TTkTextPicker` with table-specific signals
    for navigation and data change notification.
    '''
    __slots__ = ('leavingTriggered', 'dataChanged')

    leavingTriggered: pyTTkSignal
    '''
    This signal is emitted when the user navigates out of the editor

    :param direction: The direction of navigation
    :type direction: TTkTableEditLeaving
    '''

    dataChanged: pyTTkSignal
    '''
    This signal is emitted when the rich text content changes

    :param data: The new TTkString value
    :type data: TTkString
    '''

    def __init__(self, **kwargs):
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        super().__init__(**kwargs)
        self.textChanged.connect(self._textChanged)

    @pyTTkSlot()
    def _textChanged(self):
        self.dataChanged.emit(self.getCellData())

    @staticmethod
    def editWidgetFactory( data:Any) -> TTkTableProxyEditWidget:
        if not isinstance(data, (TTkString,str)):
            raise ValueError(f"{data} is not a TTkStringType")
        te = _TextPickerProxy(
            text=data,
            autoSize=False,
            wrapMode=TTkK.NoWrap)
        return te

    def getCellData(self) -> TTkString:
        return self.getTTkString()

    # def setCellData(self, data:TTkStringType) -> None:
    #     self.setT(data)

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        if ( evt.type == TTkK.SpecialKey):
            if evt.mod==TTkK.NoModifier:
                if evt.key == TTkK.Key_Enter:
                    self.leavingTriggered.emit(TTkTableEditLeaving.RIGHT)
                    return True
        return super().keyEvent(evt)

@dataclass
class TTkProxyEditDef():
    ''' Definition for table cell editor proxy

    :param types: Tuple of data types this editor handles (e.g., (int, float))
    :type types: Tuple[type, ...]
    :param class_def: Widget class implementing TTkTableProxyEditWidget protocol
    :type class_def: Type[TTkTableProxyEditWidget]
    :param rich: Whether this editor supports rich text formatting
    :type rich: bool
    '''
    types: Tuple[type, ...]
    class_def: Type[TTkTableProxyEditWidget]
    rich: bool = False

class TTkTableProxyEdit():
    ''' Proxy class for managing table cell editors

    Creates and configures appropriate editor widgets based on cell data type.
    All editors implement the :py:class:`TTkTableProxyEditWidget` protocol.

    Example usage::

        proxy = TTkTableProxyEdit()
        proxy.editCell(
            geometry=(10, 5, 20, 3),
            row=2, col=1,
            table=myTable
        )
    '''
    __slots__ = ('_proxies')
    _proxies:List[TTkProxyEditDef]
    def __init__(self):
        self._proxies = [
            TTkProxyEditDef( class_def=_SpinBoxProxy,    types=(int,float)     ),
            TTkProxyEditDef( class_def=_TextEditProxy,   types=(str,TTkString) ),
            TTkProxyEditDef( class_def=_TextEditProxy,   types=(str),       rich=True ),
            TTkProxyEditDef( class_def=_TextPickerProxy, types=(TTkString), rich=True ),
        ]

    def getProxyWidget(self, data, rich:bool=False) -> Optional[TTkTableProxyEditWidget]:
        for proxy in self._proxies:
            if proxy.rich==rich and isinstance(data, proxy.types):
                return proxy.class_def.editWidgetFactory(data)
        for proxy in self._proxies:
            if isinstance(data, proxy.types):
                return proxy.class_def.editWidgetFactory(data)
        return None
