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
    def setHeaderLabels(self, labels:TTkString) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.setHeaderLabels`

        setHeaderLabels
        '''
        return self._treeView.setHeaderLabels(labels=labels)
    def setColumnWidth(self, column:int, width: int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.setColumnWidth`

        setColumnWidth
        '''
        return self._treeView.setColumnWidth(column=column, width=width)
    def resizeColumnToContents(self, column:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.resizeColumnToContents`

        resizeColumnToContents
        '''
        return self._treeView.resizeColumnToContents(column=column)
    def sortColumn(self):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.sortColumn`

        Returns the column used to sort the contents of the widget.
        '''
        return self._treeView.sortColumn()
    def sortItems(self, col:int, order:TTkK.SortOrder) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.sortItems`

        Sorts the items in the widget in the specified order by the values in the given column.
        '''
        return self._treeView.sortItems(col=col, order=order)
    def dragDropMode(self):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.dragDropMode`

        dragDropMode
        '''
        return self._treeView.dragDropMode()
    def setDragDropMode(self, dndMode):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.setDragDropMode`

        setDragDropMode
        '''
        return self._treeView.setDragDropMode(dndMode=dndMode)
    @pyTTkSlot()
    def expandAll(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.expandAll`

        expandAll
        '''
        return self._treeView.expandAll()
    @pyTTkSlot()
    def collapseAll(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.collapseAll`

        collapseAll
        '''
        return self._treeView.collapseAll()
    def addTopLevelItem(self, item:TTkTreeWidgetItem) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.addTopLevelItem`

        addTopLevelItem
        '''
        return self._treeView.addTopLevelItem(item=item)
    def addTopLevelItems(self, items:TTkTreeWidgetItem) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.addTopLevelItems`

        addTopLevelItems
        '''
        return self._treeView.addTopLevelItems(items=items)
    def takeTopLevelItem(self, index) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.takeTopLevelItem`

        takeTopLevelItem
        '''
        return self._treeView.takeTopLevelItem(index=index)
    def topLevelItem(self, index) -> TTkTreeWidgetItem:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.topLevelItem`

        topLevelItem
        '''
        return self._treeView.topLevelItem(index=index)
    def indexOfTopLevelItem(self, item:TTkTreeWidgetItem) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.indexOfTopLevelItem`

        indexOfTopLevelItem
        '''
        return self._treeView.indexOfTopLevelItem(item=item)
    def selectedItems(self) -> list[TTkTreeWidgetItem]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.selectedItems`

        selectedItems
        '''
        return self._treeView.selectedItems()
    def clear(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTreeWidget.clear`

        clear
        '''
        return self._treeView.clear()
    #--FORWARD-AUTOGEN-END--#