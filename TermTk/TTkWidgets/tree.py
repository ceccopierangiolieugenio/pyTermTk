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
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.treewidget import TTkTreeWidget
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea

class TTkTree(TTkAbstractScrollArea):
    __slots__ = (
        '_treeView', 'activated',
        # Forwarded Methods
        'setAlignment', 'setHeader', 'setHeaderLabels', 'setColumnSize', 'setColumnColors', 'appendItem', 'addTopLevelItem' )

    def __init__(self, *args, **kwargs):
        TTkAbstractScrollArea.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTree' )
        if 'parent' in kwargs: kwargs.pop('parent')
        self._treeView = TTkTreeWidget(*args, **kwargs)
        # Forward the signal
        self.activated = self._treeView.activated

        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._treeView)

        # Forwarded Methods
        self.setAlignment    = self._treeView.setAlignment
        self.setHeader       = self._treeView.setHeader
        self.setHeaderLabels = self._treeView.setHeaderLabels
        self.setColumnSize   = self._treeView.setColumnSize
        self.setColumnColors = self._treeView.setColumnColors
        self.appendItem      = self._treeView.appendItem
        self.addTopLevelItem = self._treeView.addTopLevelItem



