#!/usr/bin/env python3

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

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkAbstract.abstractitemmodel import TTkAbstractItemModel


class TTkTreeWidgetItem(TTkAbstractItemModel):
    __slots__ = ('_parent', '_data', '_children', '_expanded', '_selected',
                 '_childIndicatorPolicy',
        # Signals
        'refreshData')

    def __init__(self, *args, **kwargs):
        # Signals
        self.refreshData = pyTTkSignal(TTkTreeWidgetItem)
        super().__init__(self, *args, **kwargs)
        self._children = []
        self._data = args[0] if len(args)>0 and type(args[0])==list else None
        self._parent = kwargs.get('parent', None)
        self._childIndicatorPolicy = kwargs.get('childIndicatorPolicy', TTkK.DontShowIndicatorWhenChildless)
        self._expanded = False
        self._selected = False
        self._parent = kwargs.get("parent", None)

    def addChild(self, child):
        self._children.append(child)
        child._parent = self
        child.dataChanged.connect(self.emitDataChanged)
        self.dataChanged.emit()

    def addChildren(self, children):
        for child in children:
            self.addChild(child)

    def child(self, index):
        if 0 <= index < len(self._children):
            return self._children[index]
        return None

    def children(self):
        return self._children

    def data(self, column, role=None):
        if column >= len(self._data):
            return None
        return self._data[column]

    @pyTTkSlot()
    def emitDataChanged(self):
        self.dataChanged.emit()

    # def setDisabled(disabled):
    #    pass

    def setExpanded(self, expand):
        self._expanded = expand
        self.emitDataChanged()

    def setSelected(self, select):
        self._selected = select

    # def isDisabled():
    #     pass

    def isExpanded(self):
        return self._expanded

    def isSelected(self):
        return self._selected

    def size(self):
        if self._expanded:
            return 1 + sum([c.size() for c in self._children])
        else:
            return 1
