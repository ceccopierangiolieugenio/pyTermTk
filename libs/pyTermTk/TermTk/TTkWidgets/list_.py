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

from typing import List,Any,Optional

from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkWidgets.listwidget import TTkListWidget, TTkAbstractListItem, TTkAbstractListItemType
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea, _ForwardData

class TTkList(TTkAbstractScrollArea):
    __doc__ = '''
    :py:class:`TTkList` is a container widget which place :py:class:`TTkListWidget` in a scrolling area with on-demand scroll bars.

    ''' + TTkListWidget.__doc__

    _ttk_forward = _ForwardData(
        forwardClass=TTkListWidget ,
        instance="self._listView",
        signals=[ # Forwarded Signals From TTkTable
            'itemClicked', 'textClicked', 'searchModified'],
        methods=[
            'items',
            'dragDropMode', 'setDragDropMode',
            'addItem', 'addItemAt', 'addItems', 'addItemsAt',
            'indexOf', 'itemAt', 'moveItem',
            'removeAt', 'removeItem', 'removeItems',
            'selectionMode', 'setSelectionMode', 'selectedItems', 'selectedLabels',
            'search', 'setSearch', 'searchVisibility', 'setSearchVisibility',
            'setCurrentRow', 'setCurrentItem'
            ]
    )

    __slots__ = ('_listView')

    def __init__(self, *,
                 items:List[TTkAbstractListItemType]=[],
                 listWidget:Optional[TTkListWidget]=None,
                 selectionMode:TTkK.SelectionMode=TTkK.SingleSelection,
                 dragDropMode:TTkK.DragDropMode=TTkK.DragDropMode.NoDragDrop,
                 showSearch:bool=True,
                 **kwargs) -> None:
        '''
        :param listWidget: a custom List Widget to be used instead of the default one.
        :type listWidget: :py:class:`TTkListWidget`, optional
        '''
        self._listView = listWidget if listWidget else TTkListWidget(
                                                            items=items,
                                                            selectionMode=selectionMode,
                                                            dragDropMode=dragDropMode,
                                                            showSearch=showSearch,
                                                            **kwargs|{'parent':None,'visible':True})
        super().__init__(**kwargs)
        self.setViewport(self._listView)

    #--FORWARD-AUTOGEN-START--#
    @property
    def itemClicked(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.itemClicked`

        This signal is emitted whenever an item is clicked.
        
        :param item: the item selected
        :type item: :py:class:`TTkAbstractListItem`
        '''
        return self._listView.itemClicked
    @property
    def textClicked(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.textClicked`

        This signal is emitted whenever an item is clicked.
        
        :param text: the text of the item selected
        :type text: str
        '''
        return self._listView.textClicked
    @property
    def searchModified(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.searchModified`

        This signal is emitted whenever the search text is modified.
        
        :param text: the search text
        :type text: str
        '''
        return self._listView.searchModified
    def items(self) -> List[TTkAbstractListItem]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.items`

        Returns all items in the list.

        :return: Complete list of items
        :rtype: list[:py:class:`TTkAbstractListItem`]
        '''
        return self._listView.items()
    def dragDropMode(self) -> TTkK.DragDropMode:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.dragDropMode`

        Returns the current drag-drop mode.

        :return: The drag-drop behavior setting
        :rtype: :py:class:`TTkK.DragDropMode`
        '''
        return self._listView.dragDropMode()
    def setDragDropMode(self, dndMode:TTkK.DragDropMode) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setDragDropMode`

        Sets the drag-drop mode for this list.

        :param dndMode: The new drag-drop behavior
        :type dndMode: :py:class:`TTkK.DragDropMode`
        '''
        return self._listView.setDragDropMode(dndMode=dndMode)
    def addItem(self, item:TTkAbstractListItemType, data:Any=None) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.addItem`

        Appends a single item to the end of the list.

        :param item: The item to add (string or :py:class:`TTkAbstractListItem`)
        :type item: str or :py:class:`TTkAbstractListItem`
        :param data: Optional user data to associate with the item
        :type data: Any, optional
        '''
        return self._listView.addItem(item=item, data=data)
    def addItemAt(self, item:TTkAbstractListItemType, pos:int, data:Any=None) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.addItemAt`

        Inserts a single item at the specified position.

        :param item: The item to insert (string or :py:class:`TTkAbstractListItem`)
        :type item: str or :py:class:`TTkAbstractListItem`
        :param pos: The index position to insert at
        :type pos: int
        :param data: Optional user data to associate with the item
        :type data: Any, optional
        '''
        return self._listView.addItemAt(item=item, pos=pos, data=data)
    def addItems(self, items:List[TTkAbstractListItemType]) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.addItems`

        Appends multiple items to the end of the list.

        :param items: List of items to add (strings or :py:class:`TTkAbstractListItem` objects)
        :type items: list
        '''
        return self._listView.addItems(items=items)
    def addItemsAt(self, items:List[TTkAbstractListItemType], pos:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.addItemsAt`

        Inserts multiple items at the specified position.

        :param items: List of items to insert (strings or :py:class:`TTkAbstractListItem` objects)
        :type items: list
        :param pos: The index position to insert at
        :type pos: int
        '''
        return self._listView.addItemsAt(items=items, pos=pos)
    def indexOf(self, item:TTkAbstractListItemType) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.indexOf`

        Returns the index of the given item.

        :param item: The item to find
        :type item: :py:class:`TTkAbstractListItem` or the data or the text to be searched
        :return: The index of the item, or -1 if not found
        :rtype: int
        '''
        return self._listView.indexOf(item=item)
    def itemAt(self, pos:int) -> TTkAbstractListItem:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.itemAt`

        Returns the item at the specified index.

        :param pos: The index position
        :type pos: int
        :return: The item at that position
        :rtype: :py:class:`TTkAbstractListItem`
        '''
        return self._listView.itemAt(pos=pos)
    def moveItem(self, fr:int, to:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.moveItem`

        Moves an item from one position to another.

        :param fr: The source index
        :type fr: int
        :param to: The destination index
        :type to: int
        '''
        return self._listView.moveItem(fr=fr, to=to)
    def removeAt(self, pos:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.removeAt`

        Removes the item at the specified index.

        :param pos: The index of the item to remove
        :type pos: int
        '''
        return self._listView.removeAt(pos=pos)
    def removeItem(self, item:TTkAbstractListItem) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.removeItem`

        Removes a single item from the list.

        :param item: The item to remove
        :type item: :py:class:`TTkAbstractListItem`
        '''
        return self._listView.removeItem(item=item)
    def removeItems(self, items:List[TTkAbstractListItem]) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.removeItems`

        Removes multiple items from the list.

        :param items: List of items to remove
        :type items: list[:py:class:`TTkAbstractListItem`]
        '''
        return self._listView.removeItems(items=items)
    def selectionMode(self) -> TTkK.SelectionMode:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.selectionMode`

        Returns the current selection mode.

        :return: The selection behavior setting
        :rtype: :py:class:`TTkK.SelectionMode`
        '''
        return self._listView.selectionMode()
    def setSelectionMode(self, mode:TTkK.SelectionMode) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setSelectionMode`

        Sets the selection mode for this list.

        :param mode: The new selection behavior (SingleSelection or MultiSelection)
        :type mode: :py:class:`TTkK.SelectionMode`
        '''
        return self._listView.setSelectionMode(mode=mode)
    def selectedItems(self) -> List[TTkAbstractListItem]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.selectedItems`

        Returns the list of currently selected items.

        :return: List of selected item widgets
        :rtype: list[:py:class:`TTkAbstractListItem`]
        '''
        return self._listView.selectedItems()
    def selectedLabels(self) -> List[str]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.selectedLabels`

        Returns the text of all selected items.

        :return: List of selected item texts
        :rtype: list[str]
        '''
        return self._listView.selectedLabels()
    def search(self) -> str:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.search`

        Returns the current search text.

        :return: The active search filter string
        :rtype: str
        '''
        return self._listView.search()
    def setSearch(self, search:str) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setSearch`

        Sets the search text to filter items.

        :param search: The search string to filter by
        :type search: str
        '''
        return self._listView.setSearch(search=search)
    def searchVisibility(self) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.searchVisibility`

        Returns whether the search hint is visible.

        :return: True if search hint is shown
        :rtype: bool
        '''
        return self._listView.searchVisibility()
    def setSearchVisibility(self, visibility:bool) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setSearchVisibility`

        Sets the visibility of the search hint at the top of the list.

        :param visibility: True to show search hint, False to hide
        :type visibility: bool
        '''
        return self._listView.setSearchVisibility(visibility=visibility)
    def setCurrentRow(self, row:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setCurrentRow`

        Selects the item at the specified row.

        :param row: The row index to select
        :type row: int
        '''
        return self._listView.setCurrentRow(row=row)
    def setCurrentItem(self, item:TTkAbstractListItem) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setCurrentItem`

        Selects the specified item and emits the itemClicked signal.

        :param item: The item to select
        :type item: :py:class:`TTkAbstractListItem`
        '''
        return self._listView.setCurrentItem(item=item)
    #--FORWARD-AUTOGEN-END--#