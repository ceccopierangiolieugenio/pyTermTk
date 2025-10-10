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

__all__ = ['TTkTree']

from typing import List,Optional

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkWidgets.TTkModelView.treewidget import TTkTreeWidget
from TermTk.TTkWidgets.TTkModelView.treewidgetitem import TTkTreeWidgetItem
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea, _ForwardData

class TTkTree(TTkAbstractScrollArea):
    __doc__ = '''
    :py:class:`TTkTree` is a container widget which place :py:class:`TTkTreeWidget` in a scrolling area with on-demand scroll bars.

    ''' + TTkTreeWidget.__doc__

    _ttk_forward = _ForwardData(
        forwardClass=TTkTreeWidget ,
        instance="self._treeView",
        signals=[# Forwarded Signals From TTkTreeWidget
            'itemActivated', 'itemChanged', 'itemClicked', 'itemExpanded', 'itemCollapsed', 'itemDoubleClicked'],
        methods=[# Forwarded Methods From TTkTreeWidget
            'setHeaderLabels',
            'setColumnWidth', 'resizeColumnToContents',
            'sortColumn', 'sortItems',
            'dragDropMode', 'setDragDropMode',
            'expandAll', 'collapseAll',
            'invisibleRootItem',
            # 'appendItem', 'setAlignment', 'setColumnColors', 'setColumnSize', 'setHeader',
            'addTopLevelItem', 'addTopLevelItems', 'takeTopLevelItem', 'topLevelItem', 'indexOfTopLevelItem', 'selectedItems', 'clear']
    )

    __slots__ = ('_treeView')

    def __init__(self, *,
                 treeWidget:TTkTreeWidget=None,
                 **kwargs) -> None:
        '''
        :param treeWidget: a custom Tree Widget to be used instead of the default one.
        :type treeWidget: :py:class:`TTkTreeWidget`, optional
        '''
        super().__init__(**kwargs)
        kwargs.pop('parent',None)
        kwargs.pop('visible',None)
        self._treeView:TTkTreeWidget = treeWidget if treeWidget else TTkTreeWidget(**kwargs)
        self.setViewport(self._treeView)
        self.setFocusPolicy(TTkK.ClickFocus)

    #--FORWARD-AUTOGEN-START--#
    @property
    def itemActivated(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.itemActivated`

        This signal is emitted when the user activates an item by double-clicking
        or pressing a special key (e.g., Enter).
        
        :param item: the item that was clicked.
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column that was clicked.
        :type col: int
        '''
        return self._treeView.itemActivated
    @property
    def itemChanged(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.itemChanged`

        This signal is emitted when the contents of the column in the specified item changes.
        
        :param item: the item reported by this signal
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column
        :type col: int
        '''
        return self._treeView.itemChanged
    @property
    def itemClicked(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.itemClicked`

        This signal is emitted when the user clicks inside the widget.
        
        If no item was clicked, no signal will be emitted.
        
        :param item: the item that was clicked.
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column that was clicked.
        :type col: int
        '''
        return self._treeView.itemClicked
    @property
    def itemExpanded(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.itemExpanded`

        This signal is emitted when the specified item is expanded so that all of its children are displayed.
        
        :param item: the item reported by this signal
        :type item: :py:class:`TTkTreeWidgetItem`
        '''
        return self._treeView.itemExpanded
    @property
    def itemCollapsed(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.itemCollapsed`

        This signal is emitted when the specified item is collapsed so that none of its children are displayed.
        
        :param item: the item reported by this signal
        :type item: :py:class:`TTkTreeWidgetItem`
        '''
        return self._treeView.itemCollapsed
    @property
    def itemDoubleClicked(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.itemDoubleClicked`

        This signal is emitted when the user double clicks inside the widget.
        
        If no item was double clicked, no signal will be emitted.
        
        :param item: the item that was clicked.
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column that was clicked.
        :type col: int
        '''
        return self._treeView.itemDoubleClicked
    def setHeaderLabels(self, labels:List[TTkString]) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.setHeaderLabels`

        Adds a column in the header for each item in the labels list, and sets the label for each column.

        :param labels: the list of labels
        :type labels: List[:py:class:`TTkString`]
        '''
        return self._treeView.setHeaderLabels(labels=labels)
    def setColumnWidth(self, column:int, width: int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.setColumnWidth`

        Set the width of the column requested

        :param column: the column position
        :type column: int

        :rtype: int
        '''
        return self._treeView.setColumnWidth(column=column, width=width)
    def resizeColumnToContents(self, column:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.resizeColumnToContents`

        rwsize the width of the column requestedto its content

        :param column: the column position
        :type column: int
        '''
        return self._treeView.resizeColumnToContents(column=column)
    def sortColumn(self) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.sortColumn`

        Returns the column used to sort the contents of the widget.
        -1 in case no column sort is used

        :rtype: int
        '''
        return self._treeView.sortColumn()
    def sortItems(self, col:int, order:TTkK.SortOrder) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.sortItems`

        Sorts the items in the widget in the specified order by the values in the given column.

        :param col: the column used as reference for the sorting
        :type col: int
        :param order: the sorting order
        :type order: :py:class:`TTkK.SortOrder`
        '''
        return self._treeView.sortItems(col=col, order=order)
    def dragDropMode(self) -> TTkK.DragDropMode:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.dragDropMode`

        dragDropMode
        '''
        return self._treeView.dragDropMode()
    def setDragDropMode(self, dndMode:TTkK.DragDropMode):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.setDragDropMode`

        setDragDropMode
        '''
        return self._treeView.setDragDropMode(dndMode=dndMode)
    @pyTTkSlot()
    def expandAll(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.expandAll`

        Expands all expandable items.
        '''
        return self._treeView.expandAll()
    @pyTTkSlot()
    def collapseAll(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.collapseAll`

        Collapse all collapsable items.
        '''
        return self._treeView.collapseAll()
    def invisibleRootItem(self) -> TTkTreeWidgetItem:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.invisibleRootItem`

        Returns the tree widget's invisible root item.

        The invisible root item provides access to the tree widget's top-level items through the :py:class:`TTkTreeWidgetItem` API,
        making it possible to write functions that can treat top-level items and their children in a uniform way;
        for example, recursive functions.

        :return: the root Item
        :rtype: :py:class:`TTkTreeWidgetItem`
        '''
        return self._treeView.invisibleRootItem()
    def addTopLevelItem(self, item:TTkTreeWidgetItem) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.addTopLevelItem`

        Appends the item as a top-level item in the widget.

        :param item: the item to be added.
        :type item: :py:class:`TTkTreeWidgetItem`
        '''
        return self._treeView.addTopLevelItem(item=item)
    def addTopLevelItems(self, items:List[TTkTreeWidgetItem]) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.addTopLevelItems`

        Appends the list of items as a top-level items in the widget.

        :param item: the item to be added.
        :type item: List[:py:class:`TTkTreeWidgetItem`]
        '''
        return self._treeView.addTopLevelItems(items=items)
    def takeTopLevelItem(self, index:int) -> Optional[TTkTreeWidgetItem]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.takeTopLevelItem`

        Removes the top-level item at the given index in the tree and returns it, otherwise returns None;

        :param index: the index of the item
        :type index: int

        :rtype: Optional[:py:class:`TTkTreeWidgetItem`]
        '''
        return self._treeView.takeTopLevelItem(index=index)
    def topLevelItem(self, index) -> Optional[TTkTreeWidgetItem]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.topLevelItem`

        Returns the top level item at the given index, or None if the item does not exist.

        :param index: the index of the item
        :type index: int

        :rtype: Optional[:py:class:`TTkTreeWidgetItem`]
        '''
        return self._treeView.topLevelItem(index=index)
    def indexOfTopLevelItem(self, item:TTkTreeWidgetItem) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.indexOfTopLevelItem`

        Returns the index of the given top-level item, or -1 if the item cannot be found.

        :rtype: int
        '''
        return self._treeView.indexOfTopLevelItem(item=item)
    def selectedItems(self) -> List[TTkTreeWidgetItem]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.selectedItems`

        Returns a list of all selected non-hidden items.

        :rtype: List[:py:class:`TTkTreeWidgetItem`]
        '''
        return self._treeView.selectedItems()
    def clear(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.clear`

        Clears the tree widget by removing all of its items and selections.
        '''
        return self._treeView.clear()
    #--FORWARD-AUTOGEN-END--#