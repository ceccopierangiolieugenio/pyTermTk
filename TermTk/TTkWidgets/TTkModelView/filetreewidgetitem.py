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

import re

from TermTk.TTkCore.color import TTkColor

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.TTkModelView.treewidgetitem import TTkTreeWidgetItem
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal


class TTkFileTreeWidgetItem(TTkTreeWidgetItem):
    FILE = 0x00
    DIR = 0x01

    __slots__ = ("_path", "_type", "_raw")

    def __init__(self, *args, **kwargs):
        TTkTreeWidgetItem.__init__(self, *args, **kwargs)
        self._path = kwargs.get("path", ".")
        self._type = kwargs.get("type", TTkFileTreeWidgetItem.FILE)
        self._raw = kwargs.get("raw")
        self.setTextAlignment(1, TTkK.RIGHT_ALIGN)

    def setFilter(self, filter):
        for c in self._children:
            c.dataChanged.disconnect(self.emitDataChanged)
            c._processFilter(filter)
            c.setFilter(filter)
            c.dataChanged.connect(self.emitDataChanged)
        self.dataChanged.emit()

    def _processFilter(self, filter):
        if self.getType() == TTkFileTreeWidgetItem.FILE:
            filterRe = "^" + filter.replace(".", "\.").replace("*", ".*") + "$"
            if re.match(filterRe, self._raw[0]):
                self.setHidden(False)
            else:
                self.setHidden(True)

    def sortData(self, col):
        return self._raw[col]

    def path(self):
        return self._path

    def getType(self):
        return self._type
