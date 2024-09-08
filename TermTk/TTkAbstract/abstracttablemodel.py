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

__all__ = ['TTkAbstractTableModel']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot

class TTkAbstractTableModel():
    '''TTkAbstractTableModel'''
    __slots__ = (
        # Signals
        'dataChanged'
    )
    def __init__(self):
        self.dataChanged = pyTTkSignal()

    def rowCount(self) -> int:
        raise NotImplementedError()

    def columnCount(self) -> int:
        raise NotImplementedError()

    def data(self, row:int, col:int) -> object:
        return TTkString()

    def ttkStringData(self, row:int, col:int) -> TTkString:
        data = self.data(row,col)
        if isinstance(data,TTkString):
            return data
        elif type(data) == str:
            return TTkString(data)
        else:
            return TTkString(str(data))

    def setData(self, row:int, col:int, data:object):
        raise NotImplementedError()

    def headerData(self, pos:int, orientation:TTkK.Direction) -> TTkString:
        if orientation==TTkK.HORIZONTAL:
            return TTkString(str(pos))
        elif orientation==TTkK.VERTICAL:
            return TTkString(str(pos))
        return TTkString()

    def sort(self, col:int, order) -> None:
        pass
