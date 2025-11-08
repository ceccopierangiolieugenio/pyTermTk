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
from typing import Union, Tuple, Type, List, Optional, Any

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString, TTkStringType
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent

from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.texedit import TTkTextEdit, TTkTextEditView
from TermTk.TTkWidgets.spinbox import TTkSpinBox
from TermTk.TTkWidgets.TTkPickers.textpicker import TTkTextPicker

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
    def editWidgetFactory(data: object) -> TTkTableProxyEditWidget:
        ''' Factory method to create an editor widget from data

        :param data: The initial data value for the editor
        :type data: object
        :return: A new editor widget instance
        :rtype: TTkTableProxyEditWidget
        :raises NotImplementedError: Must be implemented by subclasses
        '''
        raise NotImplementedError()

    def getCellData(self) -> object:
        ''' Get the current data value from the editor

        :return: The current cell data
        :rtype: object
        :raises NotImplementedError: Must be implemented by subclasses
        '''
        raise NotImplementedError()

    def proxyDispose(self) -> None:
        ''' Clean up the editor widget and disconnect signals
        '''
        self.leavingTriggered.clear()
        self.dataChanged.clear()
        self.close()

class _TextEditViewProxy(TTkTextEditView, TTkTableProxyEditWidget):
    ''' Text editor view for table cells

    Extends :py:class:`TTkTextEditView` with table-specific signals
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
    This signal is emitted when the text content changes

    :param data: The new text value
    :type data: Union[str, TTkString]
    '''

    def __init__(self, **kwargs):
        ''' Initialize the text edit view proxy

        :param kwargs: Additional keyword arguments passed to parent
        :type kwargs: dict
        '''
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        super().__init__(**kwargs)
        self.textChanged.connect(self._emitDataChanged)

    def keyEvent(self, evt: TTkKeyEvent) -> bool:
        ''' Handle keyboard events for navigation and data entry

        :param evt: The keyboard event
        :type evt: TTkKeyEvent
        :return: True if event was handled, False otherwise
        :rtype: bool
        '''
        if (evt.type == TTkK.SpecialKey):
            _cur = self.textCursor()
            _doc = self.document()
            _line = _cur.anchor().line
            _pos  = _cur.anchor().pos
            _lineCount = _doc.lineCount()
            if evt.mod == TTkK.NoModifier:
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
                    if _lineCount == 1 and _pos == len(_doc.toPlainText()):
                        self.leavingTriggered.emit(TTkTableEditLeaving.RIGHT)
                        return True
            elif (evt.type == TTkK.SpecialKey and
                  evt.mod == TTkK.ControlModifier | TTkK.AltModifier and
                  evt.key == TTkK.Key_M):
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

    Extends :py:class:`TTkTextEdit` with table-specific signals
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
    This signal is emitted when the text content changes

    :param data: The new text value
    :type data: Union[str, TTkString]
    '''

    def __init__(self, **kwargs):
        ''' Initialize the text edit proxy

        :param kwargs: Additional keyword arguments passed to parent
        :type kwargs: dict
        '''
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        tew = _TextEditViewProxy()
        super().__init__(**kwargs | {'textEditView': tew})
        tew.leavingTriggered.connect(self.leavingTriggered.emit)
        tew.dataChanged.connect(self.dataChanged.emit)

    @staticmethod
    def editWidgetFactory(data: Any) -> TTkTableProxyEditWidget:
        ''' Factory method to create a text editor from string data

        :param data: The initial text value
        :type data: Union[str, TTkString]
        :return: A new text editor instance
        :rtype: TTkTableProxyEditWidget
        :raises ValueError: If data is not a string or TTkString
        '''
        if not isinstance(data, (TTkString, str)):
            raise ValueError(f"{data} is not a TTkStringType")
        te = _TextEditProxy()
        te.setText(data)
        return te

    def getCellData(self) -> TTkStringType:
        ''' Get the current text value from the editor

        :return: The current text content
        :rtype: Union[str, TTkString]
        '''
        txt = self.toRawText()
        val = str(txt) if txt.isPlainText() else txt
        return val

class _SpinBoxProxy(TTkSpinBox, TTkTableProxyEditWidget):
    ''' Numeric editor for table cells

    Extends :py:class:`TTkSpinBox` with table-specific signals
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
        ''' Initialize the spin box proxy

        :param kwargs: Additional keyword arguments passed to parent
        :type kwargs: dict
        '''
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        super().__init__(**kwargs)
        self.valueChanged.connect(self.dataChanged.emit)

    @staticmethod
    def editWidgetFactory(data: Any) -> TTkTableProxyEditWidget:
        ''' Factory method to create a spin box from numeric data

        :param data: The initial numeric value
        :type data: Union[int, float]
        :return: A new spin box instance
        :rtype: TTkTableProxyEditWidget
        :raises ValueError: If data is not an int or float
        '''
        if not isinstance(data, (int, float)):
            raise ValueError(f"{data} is not a int or float")
        sb = _SpinBoxProxy(
            minimum=-1000000,
            maximum=1000000,
            value=data)
        return sb

    def getCellData(self) -> Union[float, int]:
        ''' Get the current numeric value from the editor

        :return: The current spin box value
        :rtype: Union[int, float]
        '''
        return self.value()

    def keyEvent(self, evt: TTkKeyEvent) -> bool:
        ''' Handle keyboard events for navigation

        :param evt: The keyboard event
        :type evt: TTkKeyEvent
        :return: True if event was handled, False otherwise
        :rtype: bool
        '''
        if (evt.type == TTkK.SpecialKey):
            if evt.mod == TTkK.NoModifier:
                if evt.key == TTkK.Key_Enter:
                    self.leavingTriggered.emit(TTkTableEditLeaving.RIGHT)
                    return True
        return super().keyEvent(evt)


class _TextPickerProxy(TTkTextPicker, TTkTableProxyEditWidget):
    ''' Rich text editor for table cells

    Extends :py:class:`TTkTextPicker` with table-specific signals
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
        ''' Initialize the text picker proxy

        :param kwargs: Additional keyword arguments passed to parent
        :type kwargs: dict
        '''
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        super().__init__(**kwargs)
        self.textChanged.connect(self._textChanged)

    @pyTTkSlot()
    def _textChanged(self):
        ''' Internal slot to emit dataChanged signal
        '''
        self.dataChanged.emit(self.getCellData())

    @staticmethod
    def editWidgetFactory(data: Any) -> TTkTableProxyEditWidget:
        ''' Factory method to create a text picker from string data

        :param data: The initial text value
        :type data: Union[str, TTkString]
        :return: A new text picker instance
        :rtype: TTkTableProxyEditWidget
        :raises ValueError: If data is not a string or TTkString
        '''
        if not isinstance(data, (TTkString, str)):
            raise ValueError(f"{data} is not a TTkStringType")
        te = _TextPickerProxy(
            text=data,
            autoSize=False,
            wrapMode=TTkK.NoWrap)
        return te

    def getCellData(self) -> TTkString:
        ''' Get the current rich text value from the editor

        :return: The current TTkString content
        :rtype: TTkString
        '''
        return self.getTTkString()

    def keyEvent(self, evt: TTkKeyEvent) -> bool:
        ''' Handle keyboard events for navigation

        :param evt: The keyboard event
        :type evt: TTkKeyEvent
        :return: True if event was handled, False otherwise
        :rtype: bool
        '''
        if (evt.type == TTkK.SpecialKey):
            if evt.mod == TTkK.NoModifier:
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

    Automatically selects the correct editor type:
    - :py:class:`_SpinBoxProxy` for int and float values
    - :py:class:`_TextEditProxy` for plain text strings
    - :py:class:`_TextPickerProxy` for rich text (TTkString with formatting)

    Example usage::

        proxy = TTkTableProxyEdit()
        editor = proxy.getProxyWidget(data=42, rich=False)
        if editor:
            editor.leavingTriggered.connect(handleNavigation)
            editor.dataChanged.connect(handleDataChange)
    '''
    __slots__ = ('_proxies',)
    _proxies: List[TTkProxyEditDef]

    def __init__(self):
        ''' Initialize the table proxy edit manager
        '''
        self._proxies = [
            TTkProxyEditDef(class_def=_SpinBoxProxy,    types=(int, float)),
            TTkProxyEditDef(class_def=_TextEditProxy,   types=(str, TTkString)),
            TTkProxyEditDef(class_def=_TextEditProxy,   types=(str,),       rich=True),
            TTkProxyEditDef(class_def=_TextPickerProxy, types=(TTkString,), rich=True),
        ]

    def getProxyWidget(self, data, rich: bool = False) -> Optional[TTkTableProxyEditWidget]:
        ''' Get an appropriate editor widget for the given data

        :param data: The data value to edit
        :type data: object
        :param rich: Whether rich text editing is required
        :type rich: bool
        :return: An editor widget instance, or None if no suitable editor found
        :rtype: Optional[TTkTableProxyEditWidget]
        '''
        for proxy in self._proxies:
            if proxy.rich == rich and isinstance(data, proxy.types):
                return proxy.class_def.editWidgetFactory(data)
        for proxy in self._proxies:
            if isinstance(data, proxy.types):
                return proxy.class_def.editWidgetFactory(data)
        return None
