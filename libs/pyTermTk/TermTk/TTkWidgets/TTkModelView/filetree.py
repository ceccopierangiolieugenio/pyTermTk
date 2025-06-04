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
    def setHeaderLabels(self, labels:TTkString) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.setHeaderLabels`

        setHeaderLabels
        '''
        return self._fileTreeWidget.setHeaderLabels(labels=labels)
    def setColumnWidth(self, column:int, width: int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.setColumnWidth`

        setColumnWidth
        '''
        return self._fileTreeWidget.setColumnWidth(column=column, width=width)
    def resizeColumnToContents(self, column:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.resizeColumnToContents`

        resizeColumnToContents
        '''
        return self._fileTreeWidget.resizeColumnToContents(column=column)
    def sortColumn(self):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.sortColumn`

        Returns the column used to sort the contents of the widget.
        '''
        return self._fileTreeWidget.sortColumn()
    def sortItems(self, col:int, order:TTkK.SortOrder) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.sortItems`

        Sorts the items in the widget in the specified order by the values in the given column.
        '''
        return self._fileTreeWidget.sortItems(col=col, order=order)
    def dragDropMode(self):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.dragDropMode`

        dragDropMode
        '''
        return self._fileTreeWidget.dragDropMode()
    def setDragDropMode(self, dndMode):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.setDragDropMode`

        setDragDropMode
        '''
        return self._fileTreeWidget.setDragDropMode(dndMode=dndMode)
    @pyTTkSlot()
    def expandAll(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.expandAll`

        expandAll
        '''
        return self._fileTreeWidget.expandAll()
    @pyTTkSlot()
    def collapseAll(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.collapseAll`

        collapseAll
        '''
        return self._fileTreeWidget.collapseAll()
    def addTopLevelItem(self, item:TTkTreeWidgetItem) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.addTopLevelItem`

        addTopLevelItem
        '''
        return self._fileTreeWidget.addTopLevelItem(item=item)
    def addTopLevelItems(self, items:TTkTreeWidgetItem) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.addTopLevelItems`

        addTopLevelItems
        '''
        return self._fileTreeWidget.addTopLevelItems(items=items)
    def takeTopLevelItem(self, index) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.takeTopLevelItem`

        takeTopLevelItem
        '''
        return self._fileTreeWidget.takeTopLevelItem(index=index)
    def topLevelItem(self, index) -> TTkTreeWidgetItem:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.topLevelItem`

        topLevelItem
        '''
        return self._fileTreeWidget.topLevelItem(index=index)
    def indexOfTopLevelItem(self, item:TTkTreeWidgetItem) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.indexOfTopLevelItem`

        indexOfTopLevelItem
        '''
        return self._fileTreeWidget.indexOfTopLevelItem(item=item)
    def selectedItems(self) -> list[TTkTreeWidgetItem]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.selectedItems`

        selectedItems
        '''
        return self._fileTreeWidget.selectedItems()
    def clear(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkFileTreeWidget.clear`

        clear
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