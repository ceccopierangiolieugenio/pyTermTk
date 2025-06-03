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

    __slots__ = ('_fileTreeWidget', *_ttk_forward.signals)

    def __init__(self, **kwargs) -> None:
        wkwargs = kwargs.copy()
        wkwargs.pop('parent',None)
        wkwargs.pop('visible',None)
        self._fileTreeWidget = TTkFileTreeWidget(**wkwargs)

        super().__init__(**kwargs, treeWidget=self._fileTreeWidget)

        for _attr in self._ttk_forward.signals:
            setattr(self,_attr,getattr(self._fileTreeWidget,_attr))

    #--FORWARD-AUTOGEN-START--#
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