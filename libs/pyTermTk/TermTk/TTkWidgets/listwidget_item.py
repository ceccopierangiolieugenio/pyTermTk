# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkAbstractListItem', 'TTkListItem', 'TTkAbstractListItemType']

from typing import Union, Any

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.string import TTkString,TTkStringType

from TermTk.TTkAbstract.abstract_list_item import _TTkAbstractListItem

class TTkListItem(_TTkAbstractListItem):
    '''TTkListItem:

    Base class for items in a :py:class:`TTkListWidget`.

    This widget represents a single selectable item that can be highlighted,
    selected, and clicked. It supports custom styling for different states
    (default, highlighted, selected, hover, disabled).

    ::

        ┌────────────────────┐
        │ Normal Item        │  Default state
        │ Highlighted Item   │  Highlighted (navigation)
        │ Selected Item      │  Selected by user
        └────────────────────┘

    '''

    __slots__ = ('_text', '_data', '_lowerText')

    _text: TTkString
    _data: Any

    def __init__(self, *, text:TTkStringType='', data:Any=None) -> None:
        super().__init__()
        if isinstance(text,str):
            self._text = TTkString(text)
        elif isinstance(text, TTkString):
            self._text = text
        else:
            self._text = TTkString(str(text))
        self._lowerText = str(self._text).lower()
        self._data  = data

    def text(self) -> TTkString:
        '''
        Returns the item's display text.

        :return: The text displayed by this item
        :rtype: :py:class:`TTkString`
        '''
        return self._text

    def setText(self, text: str) -> None:
        '''
        Sets the item's display text.

        :param text: The new text to display
        :type text: str or :py:class:`TTkString`
        '''
        self._text = TTkString(text)
        self._lowerText = str(self._text).lower()
        self.dataChanged.emit()

    def data(self) -> Any:
        '''
        Returns the user data associated with this item.

        :return: The custom data object
        :rtype: Any
        '''
        return self._data

    def setData(self, data: Any) -> None:
        '''
        Sets the user data associated with this item.

        :param data: The custom data object to store
        :type data: Any
        '''
        if self._data == data: return
        self._data = data
        self.dataChanged.emit()

    def toTTkString(self):
        return self._text


class TTkAbstractListItem(TTkListItem):
    '''TTkAbstractListItem:

    .. warning::
        **DEPRECATED:** This concrete implementation is deprecated. In a future version,
        this class will become an abstract base class requiring implementation.
        Use :py:class:`TTkListItem` for the default implementation.

    This class currently provides a concrete implementation for backward compatibility.
    In future versions, it will be converted to an abstract interface that requires
    implementation of specific methods if you want custom behavior beyond the default
    :py:class:`TTkListItem` implementation.

    For new code:
        - Use :py:class:`TTkListItem` directly for the default list item implementation
        - Inherit from :py:class:`TTkListItem` for custom list items
        - Avoid using :py:class:`TTkAbstractListItem` directly

    .. deprecated:: 0.50.0
        Direct instantiation deprecated. Use :py:class:`TTkListItem` instead.
    '''
    def __init__(self, **kwargs):
        TTkLog.warn('TTkAbstractListItem direct usage is deprecated. This will become an abstract class in a future version. Use TTkListItem instead.')
        super().__init__(**kwargs)

TTkAbstractListItemType = Union[TTkAbstractListItem, Any]
