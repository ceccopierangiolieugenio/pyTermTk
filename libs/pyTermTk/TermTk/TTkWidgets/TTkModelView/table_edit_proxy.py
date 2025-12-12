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

__all__ = [
    'TTkProxyEditDef',
    'TTkTableEditLeaving', 'TTkTableProxyEditFlag',
    'TTkTableProxyEdit', 'TTkTableProxyEditWidget',
    'TTkCellListTypeBase', 'TTkCellListType',
]


import datetime
from dataclasses import dataclass
from enum import Enum, Flag, auto
from typing import Union, Tuple, Type, List, Optional, Any, Callable

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString, TTkStringType
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent

from TermTk.TTkLayouts.gridlayout import TTkGridLayout

from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.resizableframe import TTkResizableFrame
from TermTk.TTkWidgets.texedit import TTkTextEdit, TTkTextEditView
from TermTk.TTkWidgets.spinbox import TTkSpinBox
from TermTk.TTkWidgets.list_ import TTkList
from TermTk.TTkWidgets.listwidget import TTkAbstractListItem
from TermTk.TTkWidgets.datetime_time import TTkTime
from TermTk.TTkWidgets.datetime_date import TTkDate
from TermTk.TTkWidgets.datetime_datetime import TTkDateTime
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

class TTkTableProxyEditFlag(Flag):
    NONE = 0x00
    BASE = 0x01
    RICH = 0x02
    ALL  = BASE | RICH
    # MODAL = 0x04

class TTkCellListTypeBase():
    def items(self) -> List[Any]:
        raise NotImplementedError()

    def value(self) -> Any:
        raise NotImplementedError()

    def serValue(self, val: Any) -> None:
        raise NotImplementedError()

    def factory(self, value:Any, items:List[Any]) -> TTkCellListTypeBase:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()

class TTkCellListType(TTkCellListTypeBase):
    __slots__ = ('_value', '_items')
    def __init__(self, value:Any, items:List[Any]):
        self._value = value
        self._items = items
        if value not in items:
            raise ValueError(f"{value=} not included in {items}")

    def items(self) -> List[Any]:
        return self._items

    def value(self) -> Any:
        return self._value

    def serValue(self, val: Any) -> None:
        '''
        Set the value

        :param val: The new value
        :type val: Any
        '''
        if val not in self._items:
            raise ValueError(f"{val} not included in {self._list}")
        self._value = val

    def factory(self, value:Any, items:List[Any]) -> TTkCellListTypeBase:
        return TTkCellListType(value=value, items=items)

    def __str__(self) -> str:
        return str(self._value)


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
        :rtype: :py:class:`TTkTableProxyEditWidget`
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

    def isModal(self) -> bool:
        return False


class _ListBaseProxy(TTkResizableFrame, TTkTableProxyEditWidget):
    ''' Numeric editor for table cells

    Extends :py:class:`TTkSpinBox` with table-specific signals
    for navigation and data change notification.
    '''
    __slots__ = ('leavingTriggered', 'dataChanged', '_list', '_items', '_value')

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

    _items:List[Any]
    _value:TTkCellListTypeBase

    def __init__(self, *, value:TTkCellListTypeBase, items:List[Any], **kwargs):
        ''' Initialize the spin box proxy
        '''
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        self._items = items
        self._value = value
        w = max(_i.termWidth() if isinstance(_i,TTkString) else len(str(_i)) for _i in self._items)
        h = len(self._items)
        super().__init__(**kwargs|{'size':(2+w,2+h), 'layout':TTkGridLayout()})
        self._list = TTkList(parent=self, items=self._items)
        index = self._list.indexOf(value.value())
        self._list.setCurrentRow(index)
        self._list.itemClicked.connect(self._itemClicked)

    @pyTTkSlot(TTkAbstractListItem)
    def _itemClicked(self, item:TTkAbstractListItem):
        self.dataChanged.emit(self._value.factory(value=item.data(), items=self._items))

    def isModal(self) -> bool:
        return True

    def setFocus(self) -> None:
        return self._list.setFocus()

    @staticmethod
    def editWidgetFactory(data: Any) -> TTkTableProxyEditWidget:
        ''' Factory method to create a spin box from numeric data

        :param data: The initial numeric value
        :type data: Union[int, float]
        :return: A new spin box instance
        :rtype: :py:class:`TTkTableProxyEditWidget`
        :raises ValueError: If data is not an int or float
        '''
        if not isinstance(data, TTkCellListTypeBase):
            raise ValueError(f"{data} is not instance of 'TTkCellListTypeBase'")
        sb = _ListBaseProxy(items=data.items(), value=data)
        return sb

    def getCellData(self) -> Union[float, int]:
        ''' Get the current numeric value from the editor

        :return: The current spin box value
        :rtype: Union[int, float]
        '''
        self.dataChanged.emit(self._value.factory(
            value=self._list.selectedItems()[0].data(),
            items=self._items))

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
                    self.leavingTriggered.emit(TTkTableEditLeaving.NONE)
                    return True
        return super().keyEvent(evt)

class _BoolListProxy(TTkResizableFrame, TTkTableProxyEditWidget):
    ''' Numeric editor for table cells

    Extends :py:class:`TTkSpinBox` with table-specific signals
    for navigation and data change notification.
    '''
    __slots__ = ('leavingTriggered', 'dataChanged', '_list')

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
        '''
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        super().__init__(**kwargs|{'size':(7,4), 'layout':TTkGridLayout()})
        self._list = TTkList(parent=self, items=[True,False])
        self._list.itemClicked.connect(self._itemClicked)

    @pyTTkSlot(TTkAbstractListItem)
    def _itemClicked(self, item:TTkAbstractListItem):
        self.dataChanged.emit(item.data())

    def isModal(self) -> bool:
        return True

    def setFocus(self) -> None:
        return self._list.setFocus()

    @staticmethod
    def editWidgetFactory(data: Any) -> TTkTableProxyEditWidget:
        ''' Factory method to create a spin box from numeric data

        :param data: The initial numeric value
        :type data: Union[int, float]
        :return: A new spin box instance
        :rtype: :py:class:`TTkTableProxyEditWidget`
        :raises ValueError: If data is not an int or float
        '''
        if not isinstance(data, bool):
            raise ValueError(f"{data} is not a boolean")
        sb = _BoolListProxy()
        sb._list.setCurrentRow(0 if data else 1)
        return sb

    def getCellData(self) -> Union[float, int]:
        ''' Get the current numeric value from the editor

        :return: The current spin box value
        :rtype: Union[int, float]
        '''
        return self._list.selectedItems()[0].data()

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
                    self.leavingTriggered.emit(TTkTableEditLeaving.NONE)
                    return True
        return super().keyEvent(evt)

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
        :rtype: :py:class:`TTkTableProxyEditWidget`
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
        :rtype: :py:class:`TTkTableProxyEditWidget`
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


class _DateTime_KeyGeneric():
    ''' Mixin class for datetime widget keyboard navigation

    Provides common keyboard event handling for datetime-based editors,
    including arrow key navigation and Enter key handling.
    '''

    leavingTriggered: pyTTkSignal
    dataChanged: pyTTkSignal

    def newKeyEvent(self, evt: TTkKeyEvent, cb:Callable[[TTkKeyEvent],bool]) -> bool:
        ''' Handle keyboard events with custom callback and navigation

        :param evt: The keyboard event
        :type evt: TTkKeyEvent
        :param cb: Callback function for additional key handling
        :type cb: Callable[[TTkKeyEvent], bool]
        :return: True if event was handled, False otherwise
        :rtype: bool
        '''
        if (evt.type == TTkK.SpecialKey):
            if evt.mod == TTkK.NoModifier:
                if evt.key == TTkK.Key_Enter:
                    self.leavingTriggered.emit(TTkTableEditLeaving.RIGHT)
                    return True
        if cb(evt):
            return True
        if (evt.type == TTkK.SpecialKey):
            if evt.mod == TTkK.NoModifier:
                if evt.key == TTkK.Key_Up:
                    self.leavingTriggered.emit(TTkTableEditLeaving.TOP)
                    return True
                elif evt.key == TTkK.Key_Down:
                    self.leavingTriggered.emit(TTkTableEditLeaving.BOTTOM)
                    return True
                elif evt.key == TTkK.Key_Left:
                    self.leavingTriggered.emit(TTkTableEditLeaving.LEFT)
                    return True
                elif evt.key == TTkK.Key_Right:
                    self.leavingTriggered.emit(TTkTableEditLeaving.RIGHT)
                    return True
        return False

class _DateTime_TimeProxy(TTkTime, TTkTableProxyEditWidget, _DateTime_KeyGeneric):
    ''' Time editor for table cells

    Extends :py:class:`TTkTime` with table-specific signals
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
    This signal is emitted when the time value changes

    :param data: The new time value
    :type data: datetime.time
    '''

    def __init__(self, **kwargs):
        ''' Initialize the time editor proxy
        '''
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        super().__init__(**kwargs)
        self.timeChanged.connect(self.dataChanged.emit)

    @staticmethod
    def editWidgetFactory(data: Any) -> TTkTableProxyEditWidget:
        ''' Factory method to create a time editor from time data

        :param data: The initial time value
        :type data: datetime.time
        :return: A new time editor instance
        :rtype: :py:class:`TTkTableProxyEditWidget`
        :raises ValueError: If data is not a datetime.time
        '''
        if not isinstance(data, datetime.time):
            raise ValueError(f"{data} is not a int or float")
        tp = _DateTime_TimeProxy(time=data)
        return tp

    def getCellData(self) -> datetime.time:
        ''' Get the current time value from the editor

        :return: The current time
        :rtype: datetime.time
        '''
        return self.time()

    def keyEvent(self, evt: TTkKeyEvent) -> bool:
        ''' Handle keyboard events for navigation

        :param evt: The keyboard event
        :type evt: TTkKeyEvent
        :return: True if event was handled, False otherwise
        :rtype: bool
        '''
        return self.newKeyEvent(evt,super().keyEvent)


class _DateTime_DateProxy(TTkDate, TTkTableProxyEditWidget, _DateTime_KeyGeneric):
    ''' Date editor for table cells

    Extends :py:class:`TTkDate` with table-specific signals
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
    This signal is emitted when the date value changes

    :param data: The new date value
    :type data: datetime.date
    '''

    def __init__(self, **kwargs):
        ''' Initialize the date editor proxy
        '''
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        super().__init__(**kwargs)
        self.dataChanged.connect(self.dataChanged.emit)

    @staticmethod
    def editWidgetFactory(data: Any) -> TTkTableProxyEditWidget:
        ''' Factory method to create a date editor from date data

        :param data: The initial date value
        :type data: datetime.date
        :return: A new date editor instance
        :rtype: :py:class:`TTkTableProxyEditWidget`
        :raises ValueError: If data is not a datetime.date
        '''
        if not isinstance(data, datetime.date):
            raise ValueError(f"{data} is not a int or float")
        dp = _DateTime_DateProxy(date=data)
        return dp

    def getCellData(self) -> datetime.date:
        ''' Get the current date value from the editor

        :return: The current date
        :rtype: datetime.date
        '''
        return self.date()

    def keyEvent(self, evt: TTkKeyEvent) -> bool:
        ''' Handle keyboard events for navigation

        :param evt: The keyboard event
        :type evt: TTkKeyEvent
        :return: True if event was handled, False otherwise
        :rtype: bool
        '''
        return self.newKeyEvent(evt,super().keyEvent)


class _DateTime_DateTimeProxy(TTkDateTime, TTkTableProxyEditWidget, _DateTime_KeyGeneric):
    ''' DateTime editor for table cells

    Extends :py:class:`TTkDateTime` with table-specific signals
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
    This signal is emitted when the datetime value changes

    :param data: The new datetime value
    :type data: datetime.datetime
    '''

    def __init__(self, **kwargs):
        ''' Initialize the datetime editor proxy
        '''
        self.leavingTriggered = pyTTkSignal(TTkTableEditLeaving)
        self.dataChanged = pyTTkSignal(object)
        super().__init__(**kwargs)
        self.datetimeChanged.connect(self.dataChanged.emit)

    @staticmethod
    def editWidgetFactory(data: Any) -> TTkTableProxyEditWidget:
        ''' Factory method to create a datetime editor from datetime data

        :param data: The initial datetime value
        :type data: datetime.datetime
        :return: A new datetime editor instance
        :rtype: :py:class:`TTkTableProxyEditWidget`
        :raises ValueError: If data is not a datetime.datetime
        '''
        if not isinstance(data, datetime.datetime):
            raise ValueError(f"{data} is not a int or float")
        dtp = _DateTime_DateTimeProxy(datetime=data)
        return dtp

    def getCellData(self) -> datetime.datetime:
        ''' Get the current datetime value from the editor

        :return: The current datetime
        :rtype: datetime.datetime
        '''
        return self.datetime()

    def keyEvent(self, evt: TTkKeyEvent) -> bool:
        ''' Handle keyboard events for navigation

        :param evt: The keyboard event
        :type evt: TTkKeyEvent
        :return: True if event was handled, False otherwise
        :rtype: bool
        '''
        return self.newKeyEvent(evt,super().keyEvent)

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
        :rtype: :py:class:`TTkTableProxyEditWidget`
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
    flags: TTkTableProxyEditFlag = TTkTableProxyEditFlag.ALL

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
            TTkProxyEditDef(class_def=_ListBaseProxy,       types=(TTkCellListTypeBase)),
            TTkProxyEditDef(class_def=_BoolListProxy,   types=(bool)),
            TTkProxyEditDef(class_def=_SpinBoxProxy,    types=(int, float)),
            TTkProxyEditDef(class_def=_TextEditProxy,   types=(str,)),
            TTkProxyEditDef(class_def=_TextEditProxy,   types=(TTkString,), flags=TTkTableProxyEditFlag.BASE),
            TTkProxyEditDef(class_def=_TextPickerProxy, types=(TTkString,), flags=TTkTableProxyEditFlag.RICH),
            # Datetime go first because
            #   datetime is instance of date as well
            TTkProxyEditDef(class_def=_DateTime_DateTimeProxy, types=(datetime.datetime)),
            TTkProxyEditDef(class_def=_DateTime_TimeProxy, types=(datetime.time)),
            TTkProxyEditDef(class_def=_DateTime_DateProxy, types=(datetime.date)),
        ]

    def addProxy(self, proxy:TTkProxyEditDef) -> None:
        self._proxies.insert(0,proxy)

    def getProxyWidget(self, data, flags: TTkTableProxyEditFlag = TTkTableProxyEditFlag.BASE) -> Optional[TTkTableProxyEditWidget]:
        ''' Get an appropriate editor widget for the given data

        :param data: The data value to edit
        :type data: object
        :param rich: Whether rich text editing is required
        :type rich: bool
        :return: An editor widget instance, or None if no suitable editor found
        :rtype: Optional[TTkTableProxyEditWidget]
        '''
        for proxy in self._proxies:
            if ( proxy.flags & flags ) and isinstance(data, proxy.types):
                return proxy.class_def.editWidgetFactory(data)
        return None
