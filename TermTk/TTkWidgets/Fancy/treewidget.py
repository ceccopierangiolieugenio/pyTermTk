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

__all__ = ['TTkFancyTreeWidget']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.checkbox import TTkCheckbox
from TermTk.TTkWidgets.Fancy.tableview import TTkFancyTableView
from TermTk.TTkWidgets.Fancy.treewidgetitem import TTkFancyTreeWidgetItem

class _TTkDisplayedTreeItemControl(TTkCheckbox):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setMinimumSize(1, 1)

    def paintEvent(self, canvas):
        if self.isChecked():
            canvas.drawText(pos=(0,0), text="▼")
        else:
            canvas.drawText(pos=(0,0), text="▶")


class _TTkDisplayedTreeItem(TTkContainer):
    __slots__ = ('_depth', '_control', '_text', '_id', '_clicked', '_treeWidgetItem', '_isLeaf' )
    def __init__(self, *,
                  id:int=0,
                  text:TTkString='',
                  depth:int=0,
                  treeWidgetItem:TTkFancyTreeWidgetItem=None,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        #Signals
        self._clicked = pyTTkSignal(bool, _TTkDisplayedTreeItem, TTkFancyTreeWidgetItem)

        self._depth = depth
        self._text = TTkString(text)
        self._id = id
        self._treeWidgetItem = treeWidgetItem
        self._isLeaf  = self._treeWidgetItem.childIndicatorPolicy() == TTkK.DontShowIndicator
        self._isLeaf |= self._treeWidgetItem.childIndicatorPolicy() == TTkK.DontShowIndicatorWhenChildless and not self._treeWidgetItem.children()
        if self._isLeaf:
            self._control = None
        else:
            self._control = _TTkDisplayedTreeItemControl(parent=self, checked=self._treeWidgetItem.expand())
            self._control.setGeometry(self._depth, 0, 1, 1)
            self._control.clicked.connect(self._controlClicked)

    @pyTTkSlot(bool)
    def _controlClicked(self, status):
        self._clicked.emit(status, self, self._treeWidgetItem)

    def paintEvent(self, canvas):
        if self._isLeaf:
            canvas.drawText(pos=(self._depth, 0), text="•")
        canvas.drawText(pos=(self._depth+2, 0), text=self._text)


class TTkFancyTreeWidget(TTkFancyTableView):
    __slots__ = ( '_topLevelItems')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._topLevelItems = TTkFancyTreeWidgetItem(None)
        self.doubleClicked.connect(self._doubleClickItem)
        # kwargs.pop('parent',None)
        # kwargs.pop('visible',None)

    def _expand(self, item, depth):
        item.setExpand(True)
        item.refresh()
        toExpand = []
        index = self.indexOf(item.data())+1
        if index != 0:
            for child in item.children():
                self._addTreeWidgetItem(item=child, depth=depth, index=index)
                index+=1
                if child.expand():
                    toExpand.append(child)
        for child in toExpand:
            self._expand(item=child, depth=(depth+1))


    def _shrink(self, item):
        item.setExpand(False)
        item.refresh()
        index = self.indexOf(item.data())
        parent = item.parent()
        if item == parent.children()[-1]:
            self.removeItemsFrom(index+1)
        else:
            nextItemIndex = parent.children().index(item)
            nextItem = parent.children()[nextItemIndex+1]
            indexTo = self.indexOf(nextItem.data())
            for id in reversed(range(index+1,indexTo)):
                self.removeItemAt(id)

    @pyTTkSlot(int)
    def _doubleClickItem(self, index):
        if not (item := self.itemAt(index)): return
        if item[0]._isLeaf: return
        if not item[0]._treeWidgetItem.expand(): # we need to expand the TTkFancyTreeWidgetItem
            self._expand(item=item[0]._treeWidgetItem, depth=item[0]._depth+1)
        else: # we need to shrink the TTkFancyTreeWidgetItem
            self._shrink(item=item[0]._treeWidgetItem)


    @pyTTkSlot(bool, _TTkDisplayedTreeItem, TTkFancyTreeWidgetItem)
    def _controlClicked(self, status, widget, item):
        TTkLog.debug(f"{status} {widget._name}")
        if status: # we need to expand the TTkFancyTreeWidgetItem
            self._expand(item=item, depth=(widget._depth+1))
        else: # we need to shrink the TTkFancyTreeWidgetItem
            self._shrink(item=item)

    def _addTreeWidgetItem(self, item, depth=0, index=-1):
        if not isinstance(item, TTkFancyTreeWidgetItem):
            raise TypeError("TTkFancyTreeWidgetItem is required in TTkFancyTreeWidget.addTopLevelItem(item)")
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
