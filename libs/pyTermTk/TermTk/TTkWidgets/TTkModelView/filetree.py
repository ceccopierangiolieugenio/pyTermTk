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

__all__ = ['TTkFileTree']

from typing import List,Optional

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.TTkModelView.tree import TTkTree
from TermTk.TTkWidgets.TTkModelView.filetreewidget import TTkFileTreeWidget
from TermTk.TTkWidgets.TTkModelView.treewidgetitem import TTkTreeWidgetItem
from TermTk.TTkAbstract.abstractscrollarea import _ForwardData

class TTkFileTree(TTkTree):
    __doc__ = '''
    :py:class:`TTkFileTree` is a container widget which place :py:class:`TTkFileTreeWidget` in a scrolling area with on-demand scroll bars.

    ''' + TTkFileTreeWidget.__doc__

    _ttk_forward = _ForwardData(
        forwardClass=TTkFileTreeWidget,
        instance="self._fileTreeWidget",
        signals=[# Forwarded Signals from TTkFileTreeWidget
            *TTkTree._ttk_forward.signals,
            'fileClicked', 'folderClicked', 'fileDoubleClicked', 'folderDoubleClicked', 'fileActivated', 'folderActivated'],
        methods=[# Forwarded Methods From TTkTreeWidget
            *TTkTree._ttk_forward.methods,
            'openPath', 'getOpenPath',
            'setFilter']
    )

    __slots__ = ('_fileTreeWidget')

    def __init__(self, **kwargs) -> None:
        wkwargs = kwargs.copy()
        wkwargs.pop('parent',None)
        wkwargs.pop('visible',None)
        self._fileTreeWidget = TTkFileTreeWidget(**wkwargs)

        super().__init__(**kwargs, treeWidget=self._fileTreeWidget)

    #--FORWARD-AUTOGEN-START--#
    @property
    def itemActivated(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.itemActivated`

        This signal is emitted when the user activates an item by double-clicking
        or pressing a special key (e.g., Enter).
        
        :param item: the item that was clicked.
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column that was clicked.
        :type col: int
        '''
        return self._fileTreeWidget.itemActivated
    @property
    def itemChanged(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.itemChanged`

        This signal is emitted when the contents of the column in the specified item changes.
        
        :param item: the item reported by this signal
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column
        :type col: int
        '''
        return self._fileTreeWidget.itemChanged
    @property
    def itemClicked(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.itemClicked`

        This signal is emitted when the user clicks inside the widget.
        
        If no item was clicked, no signal will be emitted.
        
        :param item: the item that was clicked.
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column that was clicked.
        :type col: int
        '''
        return self._fileTreeWidget.itemClicked
    @property
    def itemExpanded(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.itemExpanded`

        This signal is emitted when the specified item is expanded so that all of its children are displayed.
        
        :param item: the item reported by this signal
        :type item: :py:class:`TTkTreeWidgetItem`
        '''
        return self._fileTreeWidget.itemExpanded
    @property
    def itemCollapsed(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.itemCollapsed`

        This signal is emitted when the specified item is collapsed so that none of its children are displayed.
        
        :param item: the item reported by this signal
        :type item: :py:class:`TTkTreeWidgetItem`
        '''
        return self._fileTreeWidget.itemCollapsed
    @property
    def itemDoubleClicked(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.itemDoubleClicked`

        This signal is emitted when the user double clicks inside the widget.
        
        If no item was double clicked, no signal will be emitted.
        
        :param item: the item that was clicked.
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column that was clicked.
        :type col: int
        '''
        return self._fileTreeWidget.itemDoubleClicked
    @property
    def fileClicked(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.fileClicked`

        This signal is emitted when a file is clicked
        
        :param file:
        :type  file: :py:class:`TTkFileTreeWidgetItem`
        '''
        return self._fileTreeWidget.fileClicked
    @property
    def folderClicked(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.folderClicked`

        This signal is emitted when a folder is clicked
        
        :param folder:
        :type  folder: :py:class:`TTkFileTreeWidgetItem`
        '''
        return self._fileTreeWidget.folderClicked
    @property
    def fileDoubleClicked(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.fileDoubleClicked`

        This signal is emitted when a file is doubleclicked
        
        :param file:
        :type  file: :py:class:`TTkFileTreeWidgetItem`
        '''
        return self._fileTreeWidget.fileDoubleClicked
    @property
    def folderDoubleClicked(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.folderDoubleClicked`

        This signal is emitted when a folder is doubleclicked
        
        :param folder:
        :type  folder: :py:class:`TTkFileTreeWidgetItem`
        '''
        return self._fileTreeWidget.folderDoubleClicked
    @property
    def fileActivated(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.fileActivated`

        This signal is emitted when a file is activated
        
        :param file:
        :type  file: :py:class:`TTkFileTreeWidgetItem`
        '''
        return self._fileTreeWidget.fileActivated
    @property
    def folderActivated(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.folderActivated`

        This signal is emitted when a fiilder is activated
        
        :param folder:
        :type  folder: :py:class:`TTkFileTreeWidgetItem`
        '''
        return self._fileTreeWidget.folderActivated
    def setHeaderLabels(self, labels:List[TTkString]) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.setHeaderLabels`

        Adds a column in the header for each item in the labels list, and sets the label for each column.

        :param labels: the list of labels
        :type labels: List[:py:class:`TTkString`]
        '''
        return self._fileTreeWidget.setHeaderLabels(labels=labels)
    def setColumnWidth(self, column:int, width: int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.setColumnWidth`

        Set the width of the column requested

        :param column: the column position
        :type column: int

        :rtype: int
        '''
        return self._fileTreeWidget.setColumnWidth(column=column, width=width)
    def resizeColumnToContents(self, column:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.resizeColumnToContents`

        rwsize the width of the column requestedto its content

        :param column: the column position
        :type column: int
        '''
        return self._fileTreeWidget.resizeColumnToContents(column=column)
    def sortColumn(self) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.sortColumn`

        Returns the column used to sort the contents of the widget.
        -1 in case no column sort is used

        :rtype: int
        '''
        return self._fileTreeWidget.sortColumn()
    def sortItems(self, col:int, order:TTkK.SortOrder) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.sortItems`

        Sorts the items in the widget in the specified order by the values in the given column.

        :param col: the column used as reference for the sorting
        :type col: int
        :param order: the sorting order
        :type order: :py:class:`TTkK.SortOrder`
        '''
        return self._fileTreeWidget.sortItems(col=col, order=order)
    def dragDropMode(self) -> TTkK.DragDropMode:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.dragDropMode`

        dragDropMode
        '''
        return self._fileTreeWidget.dragDropMode()
    def setDragDropMode(self, dndMode:TTkK.DragDropMode):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.setDragDropMode`

        setDragDropMode
        '''
        return self._fileTreeWidget.setDragDropMode(dndMode=dndMode)
    @pyTTkSlot()
    def expandAll(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.expandAll`

        Expands all expandable items.
        '''
        return self._fileTreeWidget.expandAll()
    @pyTTkSlot()
    def collapseAll(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.collapseAll`

        Collapse all collapsable items.
        '''
        return self._fileTreeWidget.collapseAll()
    def invisibleRootItem(self) -> TTkTreeWidgetItem:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.invisibleRootItem`

        Returns the tree widget's invisible root item.

        The invisible root item provides access to the tree widget's top-level items through the :py:class:`TTkTreeWidgetItem` API,
        making it possible to write functions that can treat top-level items and their children in a uniform way;
        for example, recursive functions.

        :return: the root Item
        :rtype: :py:class:`TTkTreeWidgetItem`
        '''
        return self._fileTreeWidget.invisibleRootItem()
    def addTopLevelItem(self, item:TTkTreeWidgetItem) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.addTopLevelItem`

        Appends the item as a top-level item in the widget.

        :param item: the item to be added.
        :type item: :py:class:`TTkTreeWidgetItem`
        '''
        return self._fileTreeWidget.addTopLevelItem(item=item)
    def addTopLevelItems(self, items:List[TTkTreeWidgetItem]) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.addTopLevelItems`

        Appends the list of items as a top-level items in the widget.

        :param item: the item to be added.
        :type item: List[:py:class:`TTkTreeWidgetItem`]
        '''
        return self._fileTreeWidget.addTopLevelItems(items=items)
    def takeTopLevelItem(self, index:int) -> Optional[TTkTreeWidgetItem]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.takeTopLevelItem`

        Removes the top-level item at the given index in the tree and returns it, otherwise returns None;

        :param index: the index of the item
        :type index: int

        :rtype: Optional[:py:class:`TTkTreeWidgetItem`]
        '''
        return self._fileTreeWidget.takeTopLevelItem(index=index)
    def topLevelItem(self, index) -> Optional[TTkTreeWidgetItem]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.topLevelItem`

        Returns the top level item at the given index, or None if the item does not exist.

        :param index: the index of the item
        :type index: int

        :rtype: Optional[:py:class:`TTkTreeWidgetItem`]
        '''
        return self._fileTreeWidget.topLevelItem(index=index)
    def indexOfTopLevelItem(self, item:TTkTreeWidgetItem) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.indexOfTopLevelItem`

        Returns the index of the given top-level item, or -1 if the item cannot be found.

        :rtype: int
        '''
        return self._fileTreeWidget.indexOfTopLevelItem(item=item)
    def selectedItems(self) -> List[TTkTreeWidgetItem]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.selectedItems`

        Returns a list of all selected non-hidden items.

        :rtype: List[:py:class:`TTkTreeWidgetItem`]
        '''
        return self._fileTreeWidget.selectedItems()
    def clear(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.clear`

        Clears the tree widget by removing all of its items and selections.
        '''
        return self._fileTreeWidget.clear()
    def openPath(self, path):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.openPath`

        '''
        return self._fileTreeWidget.openPath(path=path)
    def getOpenPath(self):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.getOpenPath`

        '''
        return self._fileTreeWidget.getOpenPath()
    def setFilter(self, filter):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.setFilter`

        '''
        return self._fileTreeWidget.setFilter(filter=filter)
    #--FORWARD-AUTOGEN-END--#