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

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkWidgets.listwidget import TTkListWidget, TTkAbstractListItem
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

    __slots__ = ('_listView', *_ttk_forward.signals)

    def __init__(self, *,
                 listWidget:TTkListWidget=None,
                 selectionMode:int=TTkK.SingleSelection,
                 dragDropMode:TTkK.DragDropMode=TTkK.DragDropMode.NoDragDrop,
                 showSearch:bool=True,
                 **kwargs) -> None:
        '''
        :param listWidget: a custom List Widget to be used instead of the default one.
        :type listWidget: :py:class:`TTkListWidget`, optional
        '''
        self._listView = listWidget if listWidget else TTkListWidget(
                                                            selectionMode=selectionMode,
                                                            dragDropMode=dragDropMode,
                                                            showSearch=showSearch,
                                                            **kwargs|{'parent':None,'visible':True})
        super().__init__(**kwargs)
        self.setViewport(self._listView)

        for _attr in self._ttk_forward.signals:
            setattr(self,_attr,getattr(self._listView,_attr))

    #--FORWARD-AUTOGEN-START--#
    def items(self) -> list[TTkAbstractListItem]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.items`

        items
        '''
        return self._listView.items()
    def dragDropMode(self):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.dragDropMode`

        dragDropMode
        '''
        return self._listView.dragDropMode()
    def setDragDropMode(self, dndMode):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setDragDropMode`

        setDragDropMode
        '''
        return self._listView.setDragDropMode(dndMode=dndMode)
    def addItem(self, item, data=None):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.addItem`

        addItem
        '''
        return self._listView.addItem(item=item, data=data)
    def addItemAt(self, item, pos, data=None):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.addItemAt`

        addItemAt
        '''
        return self._listView.addItemAt(item=item, pos=pos, data=data)
    def addItems(self, items):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.addItems`

        addItems
        '''
        return self._listView.addItems(items=items)
    def addItemsAt(self, items, pos):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.addItemsAt`

        addItemsAt
        '''
        return self._listView.addItemsAt(items=items, pos=pos)
    def indexOf(self, item):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.indexOf`

        indexOf
        '''
        return self._listView.indexOf(item=item)
    def itemAt(self, pos):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.itemAt`

        itemAt
        '''
        return self._listView.itemAt(pos=pos)
    def moveItem(self, fr, to):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.moveItem`

        moveItem
        '''
        return self._listView.moveItem(fr=fr, to=to)
    def removeAt(self, pos):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.removeAt`

        removeAt
        '''
        return self._listView.removeAt(pos=pos)
    def removeItem(self, item):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.removeItem`

        removeItem
        '''
        return self._listView.removeItem(item=item)
    def removeItems(self, items):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.removeItems`

        removeItems
        '''
        return self._listView.removeItems(items=items)
    def selectionMode(self):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.selectionMode`

        selectionMode
        '''
        return self._listView.selectionMode()
    def setSelectionMode(self, mode):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setSelectionMode`

        setSelectionMode
        '''
        return self._listView.setSelectionMode(mode=mode)
    def selectedItems(self):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.selectedItems`

        selectedItems
        '''
        return self._listView.selectedItems()
    def selectedLabels(self):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.selectedLabels`

        selectedLabels
        '''
        return self._listView.selectedLabels()
    def search(self) -> str:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.search`

        search
        '''
        return self._listView.search()
    def setSearch(self, search:str) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setSearch`

        setSearch
        '''
        return self._listView.setSearch(search=search)
    def searchVisibility(self) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.searchVisibility`

        searchVisibility
        '''
        return self._listView.searchVisibility()
    def setSearchVisibility(self, visibility:bool) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setSearchVisibility`

        setSearchVisibility
        '''
        return self._listView.setSearchVisibility(visibility=visibility)
    def setCurrentRow(self, row):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setCurrentRow`

        setCurrentRow
        '''
        return self._listView.setCurrentRow(row=row)
    def setCurrentItem(self, item):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkListWidget.setCurrentItem`

        setCurrentItem
        '''
        return self._listView.setCurrentItem(item=item)
    #--FORWARD-AUTOGEN-END--#