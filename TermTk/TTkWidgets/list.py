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
from TermTk.TTkWidgets.listwidget import TTkListWidget
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea

class TTkList(TTkAbstractScrollArea):
    __slots__ = (
        '_listView', 'itemClicked', 'textClicked',
        # Forwarded Methods
        'items', 'addItem', 'addItemAt', 'indexOf', 'itemAt', 
        'moveItem', 'removeAt', 'removeItem', 
        'setSelectionMode', 'selectedItems', 'selectedLabels', 
        'setCurrentRow', 'setCurrentItem',  )

    def __init__(self, *args, **kwargs):
        TTkAbstractScrollArea.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkList' )
        if 'parent' in kwargs: kwargs.pop('parent')
        self._listView = kwargs.get('listWidget',TTkListWidget(*args, **kwargs))
        self.setViewport(self._listView)
        self.itemClicked = self._listView.itemClicked
        self.textClicked = self._listView.textClicked
        # self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

        # Forwearded Methods
        self.items            = self._listView.items
        self.indexOf          = self._listView.indexOf
        self.itemAt           = self._listView.itemAt
        self.moveItem         = self._listView.moveItem
        self.removeAt         = self._listView.removeAt
        self.removeItem       = self._listView.removeItem
        self.addItem          = self._listView.addItem
        self.addItemAt        = self._listView.addItemAt
        self.setSelectionMode = self._listView.setSelectionMode
        self.selectedItems    = self._listView.selectedItems
        self.selectedLabels   = self._listView.selectedLabels
        self.setCurrentRow    = self._listView.setCurrentRow
        self.setCurrentItem   = self._listView.setCurrentItem

