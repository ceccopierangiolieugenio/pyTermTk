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
    ''' Base protocol for list-based cell data types

    Defines the interface for cell values that can be selected from a list of items.
    Implementations must provide methods to get/set values and available items.
    '''
    def items(self) -> List[Any]:
        ''' Get the list of available items

        :return: List of available items
        :rtype: List[Any]
        :raises NotImplementedError: Must be implemented by subclasses
        '''
        raise NotImplementedError()

    def value(self) -> Any:
        ''' Get the current selected value

        :return: The current value
        :rtype: Any
        :raises NotImplementedError: Must be implemented by subclasses
        '''
        raise NotImplementedError()

    def setValue(self, val: Any) -> None:
        ''' Set the current value

        :param val: The new value to set
        :type val: Any
        :raises NotImplementedError: Must be implemented by subclasses
        '''
        raise NotImplementedError()

    def factory(self, value:Any, items:List[Any]) -> TTkCellListTypeBase:
        ''' Create a new instance with the given value and items

        :param value: The initial value
        :type value: Any
        :param items: The list of available items
        :type items: List[Any]
        :return: A new instance
        :rtype: TTkCellListTypeBase
        :raises NotImplementedError: Must be implemented by subclasses
        '''
        raise NotImplementedError()

    def __str__(self) -> str:
        ''' Return string representation of the current value

        :return: String representation
        :rtype: str
        :raises NotImplementedError: Must be implemented by subclasses
        '''
        raise NotImplementedError()

class TTkCellListType(TTkCellListTypeBase):
    ''' Concrete implementation of list-based cell data type

    Represents a value that can be selected from a predefined list of items.
    Used in table cells to provide dropdown-like selection behavior.

    Example::

        items = ['Option A', 'Option B', 'Option C']
        cell_value = TTkCellListType(value='Option A', items=items)
        print(cell_value.value())  # 'Option A'
        cell_value.setValue('Option B')

    :param value: The initial selected value (must be in items)
    :type value: Any
    :param items: List of available options
    :type items: List[Any]
    :raises ValueError: If value is not in items list
    '''
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
        ''' Create a new TTkCellListType instance

        :param value: The initial value
        :type value: Any
        :param items: The list of available items
        :type items: List[Any]
        :return: A new TTkCellListType instance
        :rtype: TTkCellListTypeBase
        '''
        return TTkCellListType(value=value, items=items)

    def __str__(self) -> str:
        ''' Return string representation of the current value

        :return: String representation of the value
        :rtype: str
        '''
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
    ''' List-based editor for table cells

    Extends :py:class:`TTkResizableFrame` with a list widget for selecting
    values from a predefined set of options. Used for :py:class:`TTkCellListTypeBase` data.
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
        ''' Initialize the list-based proxy editor

        :param value: The cell value with list data
        :type value: TTkCellListTypeBase
        :param items: The list of available items
        :type items: List[Any]
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
        ''' Handle item click event from the list

        :param item: The clicked list item
        :type item: TTkAbstractListItem
        '''
        self.dataChanged.emit(self._value.factory(value=item.data(), items=self._items))

    def isModal(self) -> bool:
        ''' Check if this editor should be displayed modally

        :return: True (list editors are modal)
        :rtype: bool
        '''
        return True

    def setFocus(self) -> None:
        ''' Set focus to the internal list widget
        '''
        return self._list.viewport().setFocus()

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        return self._list.keyEvent(evt=evt)

    @staticmethod
    def editWidgetFactory(data: Any) -> TTkTableProxyEditWidget:
        ''' Factory method to create a list proxy from cell list data

        :param data: The initial list-based cell value
        :type data: TTkCellListTypeBase
        :return: A new list proxy instance
        :rtype: :py:class:`TTkTableProxyEditWidget`
        :raises ValueError: If data is not instance of TTkCellListTypeBase
        '''
        if not isinstance(data, TTkCellListTypeBase):
            raise ValueError(f"{data} is not instance of 'TTkCellListTypeBase'")
        sb = _ListBaseProxy(items=data.items(), value=data)
        return sb

    def getCellData(self) -> Union[float, int]:
        ''' Get the current selected value from the list

        :return: The selected item value
        :rtype: Union[float, int]
        '''
        self.dataChanged.emit(self._value.factory(
            value=self._list.selectedItems()[0].data(),
            items=self._items))

class _BoolListProxy(_ListBaseProxy):
    ''' Boolean editor for table cells

    Specialized list proxy that presents True/False choices for boolean cell values.
    Displays as a compact 2-item list.
    '''

    @pyTTkSlot(TTkAbstractListItem)
    def _itemClicked(self, item:TTkAbstractListItem):
        ''' Handle boolean item selection

        :param item: The clicked list item (True or False)
        :type item: TTkAbstractListItem
        '''
        self.dataChanged.emit(item.data())

    @staticmethod
    def editWidgetFactory(data: Any) -> TTkTableProxyEditWidget:
        ''' Factory method to create a boolean editor from bool data

        :param data: The initial boolean value
        :type data: bool
        :return: A new boolean list proxy instance
        :rtype: :py:class:`TTkTableProxyEditWidget`
        :raises ValueError: If data is not a boolean
        '''
        if not isinstance(data, bool):
            raise ValueError(f"{data} is not a boolean")
        value = TTkCellListType(value=data, items=[True,False])
        sb = _BoolListProxy(value=value, items=[True,False])
        return sb

    def getCellData(self) -> Union[float, int]:
        ''' Get the current boolean value from the list

        :return: The selected boolean value (True or False)
        :rtype: bool
        '''
        return self._list.selectedItems()[0].data()

class _EnumListProxy(_BoolListProxy):
    ''' Enum editor for table cells

    Specialized list proxy that presents choices for enum cell values.
    '''

    @staticmethod
    def editWidgetFactory(data: Any) -> TTkTableProxyEditWidget:
        ''' Factory method to create a enum editor from enum data

        :param data: The initial enum value
        :type data: Enum
        :return: A new enum list proxy instance
        :rtype: :py:class:`TTkTableProxyEditWidget`
        :raises ValueError: If data is not a enum
        '''
        if not isinstance(data, Enum):
            raise ValueError(f"{data} is not an Enum")
        items = list(type(data))
        value = TTkCellListType(value=data, items=items)
        sb = _BoolListProxy(value=value, items=items)
        return sb

class _TextEditViewProxy(TTkTextEditView, TTkTableProxyEditWidget):
    ''' Text editor view for table cells

    Extends :py:class:`TTkTextEditView` with table-specific signals
    for navigation and data change notification. Handles both plain text
    and rich text (:py:class:`TTkString`) editing.
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
        ''' Emit dataChanged signal when text content changes

        Converts text to string or TTkString based on formatting.
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

    Provides common keyboard event handling for datetime-based editors
    (:py:class:`TTkDate`, :py:class:`TTkTime`, :py:class:`TTkDateTime`).
    Handles arrow key navigation between cells and Enter key submission.
    '''

    leavingTriggered: pyTTkSignal
    dataChanged: pyTTkSignal

    def newKeyEvent(self, evt: TTkKeyEvent, cb:Callable[[TTkKeyEvent],bool]) -> bool:
        ''' Handle keyboard events with custom callback and table navigation

        Processes Enter key for cell submission and arrow keys for navigation
        to adjacent cells. Falls back to widget-specific handling via callback.

        :param evt: The keyboard event
        :type evt: TTkKeyEvent
        :param cb: Callback function for widget-specific key handling
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

    - :py:class:`_BoolListProxy` for boolean values
    - :py:class:`_ListBaseProxy` for :py:class:`TTkCellListTypeBase` values
    - :py:class:`_SpinBoxProxy` for int and float values
    - :py:class:`_TextEditProxy` for plain text strings
    - :py:class:`_TextPickerProxy` for rich text (TTkString with formatting)
    - :py:class:`_DateTime_DateProxy` for datetime.date values
    - :py:class:`_DateTime_TimeProxy` for datetime.time values
    - :py:class:`_DateTime_DateTimeProxy` for datetime.datetime values

    Example usage::

        proxy = TTkTableProxyEdit()

        # Get editor for numeric data
        editor = proxy.getProxyWidget(data=42, flags=TTkTableProxyEditFlag.BASE)

        # Get editor for rich text
        rich_text = TTkString("Hello", TTkColor.BOLD)
        editor = proxy.getProxyWidget(data=rich_text, flags=TTkTableProxyEditFlag.RICH)

        if editor:
            editor.leavingTriggered.connect(handleNavigation)
            editor.dataChanged.connect(handleDataChange)
    '''

    __slots__ = ('_proxies',)
    _proxies: List[TTkProxyEditDef]

    def __init__(self):
        ''' Initialize the table proxy edit manager

        Sets up the default proxy definitions for all supported data types.
        Proxies are checked in order, with custom proxies taking precedence.
        '''
        self._proxies = [
            TTkProxyEditDef(class_def=_ListBaseProxy,   types=(TTkCellListTypeBase)),
            TTkProxyEditDef(class_def=_BoolListProxy,   types=(bool)),
            TTkProxyEditDef(class_def=_EnumListProxy,   types=(Enum)),
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
        ''' Add a custom proxy definition to the manager

        Custom proxies are inserted at the beginning of the list,
        so they take precedence over default proxies.

        :param proxy: The proxy definition to add
        :type proxy: TTkProxyEditDef
        '''
        self._proxies.insert(0,proxy)

    def getProxyWidget(self, data, flags: TTkTableProxyEditFlag = TTkTableProxyEditFlag.BASE) -> Optional[TTkTableProxyEditWidget]:
        ''' Get an appropriate editor widget for the given data

        Searches through registered proxy definitions to find one that
        matches the data type and requested flags. Returns the first match.

        :param data: The data value to edit
        :type data: object
        :param flags: Flags indicating editor capabilities (BASE or RICH)
        :type flags: TTkTableProxyEditFlag
        :return: An editor widget instance, or None if no suitable editor found
        :rtype: Optional[TTkTableProxyEditWidget]
        '''
        for proxy in self._proxies:
            if ( proxy.flags & flags ) and isinstance(data, proxy.types):
                return proxy.class_def.editWidgetFactory(data)
        return None
