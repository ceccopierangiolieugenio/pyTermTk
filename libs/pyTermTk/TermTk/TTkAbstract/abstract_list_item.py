# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__  =['_TTkAbstractListItem']

from typing import Any

from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.string import TTkString

class _TTkAbstractListItem():
    '''_TTkAbstractListItem:

    .. note::
        This is the future abstract base interface for list items.

    This class defines the minimal interface that list items must implement.
    In a future version, :py:class:`TTkAbstractListItem` will be converted to
    inherit from this abstract interface, requiring custom implementations to
    provide these methods if they don't use the default :py:class:`TTkListItem`.

    Currently used as an internal marker for the planned architecture migration.
    '''
    __slots__ = ('dataChanged')

    def __init__(self):
       self.dataChanged = pyTTkSignal()

    def data(self) -> Any:
        '''
        Returns the user data associated with this item.

        :return: The custom data object
        :rtype: Any
        '''
        raise NotImplementedError

    def toTTkString(self) -> TTkString:
        return TTkString(str(self.data()))