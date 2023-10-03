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

__all__ = ['TTkFancyTreeWidgetItem']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal

class TTkFancyTreeWidgetItem():
    __slots__ = ('_parent', '_data', '_children', '_expand', '_childIndicatorPolicy',
        # Signals
        'refreshData')
    def __init__(self, *args, **kwargs):
        # Signals
        self.refreshData = pyTTkSignal(TTkFancyTreeWidgetItem)
        self._data = args[0]
        self._children = []
        self._childIndicatorPolicy = kwargs.get('childIndicatorPolicy', TTkK.DontShowIndicatorWhenChildless)
        self._expand = False
        self._parent = kwargs.get("parent", None)

    def childIndicatorPolicy(self):
        return self._childIndicatorPolicy

    def setChildIndicatorPolicy(self, policy):
        self._childIndicatorPolicy = policy

    def refresh(self):
        self.refreshData.emit(self)

    def setExpand(self, status):
        self._expand = status

    def expand(self):
        return self._expand

    def addChild(self, item):
        self._children.append(item)
        item._parent = self

    def data(self):
        return self._data

    def parent(self):
        return self._parent

    def children(self):
        return self._children