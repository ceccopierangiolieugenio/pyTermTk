# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkTable']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkWidgets.TTkModelView.tablewidget import TTkTableWidget
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstracttablemodel import TTkAbstractTableModel

class TTkTable(TTkAbstractScrollArea):
    __doc__ = '''
    :py:class:`TTkTable` is a container widget which place :py:class:`TTkTableWidget` in a scrolling area with on-demand scroll bars.

    ''' + TTkTableWidget.__doc__

    classStyle = TTkTableWidget.classStyle

    __slots__ = tuple(
        ['_tableView'] +
        (_forwardedSignals:=[ # Forwarded Signals From TTkTable
            # 'cellActivated',
            'cellChanged',
            'cellClicked', 'cellDoubleClicked',
            'cellEntered', # 'cellPressed',
            'currentCellChanged']) +
        (_forwardedMethods:=[ # Forwarded Methods From TTkTable
            'undo', 'redo',
            'isUndoAvailable','isRedoAvailable',
            'copy', 'cut', 'paste',
            'setSortingEnabled', 'isSortingEnabled', 'sortByColumn',
            'clearSelection', 'selectAll', 'setSelection',
            'selectRow', 'selectColumn', 'unselectRow', 'unselectColumn',
            'rowCount', 'currentRow', 'columnCount', 'currentColumn',
            'verticalHeader', 'horizontalHeader',
            'hSeparatorVisibility', 'vSeparatorVisibility', 'setHSeparatorVisibility', 'setVSeparatorVisibility',
            'model', 'setModel',
            'setColumnWidth', 'resizeColumnToContents', 'resizeColumnsToContents',
            'setRowHeight', 'resizeRowToContents', 'resizeRowsToContents'])
        )
    _forwardWidget = TTkTableWidget

    def __init__(self, *,
                 tableWidget:TTkTableWidget=None,
                 tableModel:TTkAbstractTableModel=None,
                 vSeparator:bool=True,
                 hSeparator:bool=True,
                 vHeader:bool=True,
                 hHeader:bool=True,
                 sortingEnabled=False,
                 dataPadding=1,
                 **kwargs) -> None:
        '''
        :param tableWidget: a custom Table Widget to be used instead of the default one.
        :type tableWidget: :py:class:`TTkTableWidget`, optional
        '''
        self._tableView = None
        self._tableView:TTkTableWidget = tableWidget if tableWidget else TTkTableWidget(
                                                                                tableModel=tableModel,
                                                                                vSeparator=vSeparator,
                                                                                hSeparator=hSeparator,
                                                                                vHeader=vHeader,
                                                                                hHeader=hHeader,
                                                                                sortingEnabled=sortingEnabled,
                                                                                dataPadding=dataPadding,
                                                                                **kwargs|{'parent':None,'visible':True})
        super().__init__(**kwargs)
        self.setViewport(self._tableView)
        # self.setFocusPolicy(TTkK.ClickFocus)

        for _attr in self._forwardedSignals+self._forwardedMethods:
            setattr(self,_attr,getattr(self._tableView,_attr))

    def style(self):
        if self._tableView:
            return self._tableView.style()
        return super().style()

    def setStyle(self, style):
        if self._tableView:
            self._tableView.setStyle(style)
        return super().setStyle(style)

    def mergeStyle(self, style):
        if self._tableView:
            self._tableView.mergeStyle(style)
        return super().mergeStyle(style)