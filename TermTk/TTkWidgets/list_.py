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

__all__ = ['TTkList']

from TermTk.TTkWidgets.listwidget import TTkListWidget
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea

class TTkList(TTkAbstractScrollArea):
    '''TTkList'''
    __slots__ = (
        '_listView', 'itemClicked', 'textClicked',
        # Forwarded Methods
        'items',
        'dragDropMode', 'setDragDropMode',
        'addItem', 'addItemAt', 'addItems', 'addItemsAt',
        'indexOf', 'itemAt', 'moveItem',
        'removeAt', 'removeItem', 'removeItems',
        'selectionMode', 'setSelectionMode', 'selectedItems', 'selectedLabels',
        'setCurrentRow', 'setCurrentItem',  )

    def __init__(self, *args, **kwargs):
        TTkAbstractScrollArea.__init__(self, *args, **kwargs)
        kwargs.pop('parent',None)
        kwargs.pop('visible',None)
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
        self.removeItems      = self._listView.removeItems
        self.addItem          = self._listView.addItem
        self.addItems         = self._listView.addItems
        self.addItemAt        = self._listView.addItemAt
        self.addItemsAt       = self._listView.addItemsAt
        self.selectionMode    = self._listView.selectionMode
        self.setSelectionMode = self._listView.setSelectionMode
        self.selectedItems    = self._listView.selectedItems
        self.selectedLabels   = self._listView.selectedLabels
        self.setCurrentRow    = self._listView.setCurrentRow
        self.setCurrentItem   = self._listView.setCurrentItem
        self.dragDropMode     = self._listView.dragDropMode
        self.setDragDropMode  = self._listView.setDragDropMode

