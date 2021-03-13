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
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.checkbox import TTkCheckbox
from TermTk.TTkWidgets.tableview import TTkTableView
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkTypes.treewidgetitem import TTkTreeWidgetItem

class _TTkDisplayedTreeItemControl(TTkCheckbox):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkDisplayedTreeItemControl' )
        self.setMinimumSize(1, 1)

    def paintEvent(self):
        if self._checked:
            self._canvas.drawText(pos=(0,0), text="▼")
        else:
            self._canvas.drawText(pos=(0,0), text="▶")


class _TTkDisplayedTreeItem(TTkWidget):
    __slots__ = ('_depth', '_control', '_text', '_id', '_clicked', '_treeWidgetItem', '_isLeaf' )
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        #Signals
        self._clicked = pyTTkSignal(bool, _TTkDisplayedTreeItem, TTkTreeWidgetItem)

        self._name = kwargs.get('name' , '_TTkDisplayedTreeItem' )
        self._depth = kwargs.get('depth' , 0 )
        self._text = kwargs.get('text' , "" )
        self._id = kwargs.get('id' , 0 )
        self._treeWidgetItem = kwargs.get('treeWidgetItem', None)
        self._isLeaf = len(self._treeWidgetItem.childs())==0
        if self._isLeaf:
            self._control = None
        else:
            self._control = _TTkDisplayedTreeItemControl(parent=self, checked=self._treeWidgetItem.expand())
            self._control.setGeometry(self._depth, 0, 1, 1)
            self._control.clicked.connect(self._controlClicked)

    @pyTTkSlot(bool)
    def _controlClicked(self, status):
        self._clicked.emit(status, self, self._treeWidgetItem)
        pass

    def paintEvent(self):
        if self._isLeaf:
            self._canvas.drawText(pos=(self._depth, 0), text="•")
        self._canvas.drawText(pos=(self._depth+2, 0), text=self._text)


class TTkTreeWidget(TTkTableView):
    __slots__ = ( '_topLevelItems')

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTreeView' )
        self._topLevelItems = TTkTreeWidgetItem(None)
        # if 'parent' in kwargs: kwargs.pop('parent')

    def _expand(self, item, depth):
        item.setExpand(True)
        toExpand = []
        index = self.indexOf(item.data())+1
        if index != 0:
            for child in item.childs():
                self._addTreeWidgetItem(item=child, depth=depth, index=index)
                index+=1
                if child.expand():
                    toExpand.append(child)
        for child in toExpand:
            self._expand(item=child, depth=(depth+1))


    def _shrink(self, item):
        item.setExpand(False)
        index = self.indexOf(item.data())
        parent = item.parent()
        if item == parent.childs()[-1]:
            self.removeItemsFrom(index+1)
        else:
            nextItemIndex = parent.childs().index(item)
            nextItem = parent.childs()[nextItemIndex+1]
            indexTo = self.indexOf(nextItem.data())
            for id in reversed(range(index+1,indexTo)):
                self.removeItemAt(id)


    @pyTTkSlot(bool, _TTkDisplayedTreeItem, TTkTreeWidgetItem)
    def _controlClicked(self, status, widget, item):
        TTkLog.debug(f"{status} {widget._name}")
        if status: # we need to expand the TtkTreeWidgetItem
            self._expand(item=item, depth=(widget._depth+1))
        else: # we need to shrink the TtkTreeWidgetItem
            self._shrink(item=item)



    def _addTreeWidgetItem(self, item, depth=0, index=-1):
        if not isinstance(item, TTkTreeWidgetItem):
            raise TypeError("TTkTreeWidgetItem is required in TTkTreeWidget.addTopLevelItem(item)")
        if item.parent() is None:
            self._topLevelItems.addChild(item)
        displayedItems = item.data().copy()
        displayTreeItem = _TTkDisplayedTreeItem(text=displayedItems[0], id=0, depth=depth, treeWidgetItem=item)
        displayTreeItem._clicked.connect(self._controlClicked)
        displayedItems[0] = displayTreeItem
        if index == -1:
            self.appendItem(item=displayedItems, id=item.data())
        else:
            self.insertItem(item=displayedItems, id=item.data(), index=index, )

    def addTopLevelItem(self, item):
        self._addTreeWidgetItem(item)

    def setHeaderLabels(self, labels):
        columns = [-1]*len(labels)
        self.setColumnSize(columns)
        self.setHeader(labels)
