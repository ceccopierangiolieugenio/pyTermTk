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
from TermTk.TTkWidgets.listwidget import TTkListWidget
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea

class TTkList(TTkAbstractScrollArea):
    __doc__ = '''
    :py:class:`TTkList` is a container widget which place :py:class:`TTkListWidget` in a scrolling area with on-demand scroll bars.

    ''' + TTkListWidget.__doc__

    __slots__ = tuple(
        ['_listView'] +
        (_forwardedSignals:=[ # Forwarded Signals From TTkTable
            'itemClicked', 'textClicked']) +
        (_forwardedMethods:=[ # Forwarded Methods From TTkTable
            'items',
            'dragDropMode', 'setDragDropMode',
            'addItem', 'addItemAt', 'addItems', 'addItemsAt',
            'indexOf', 'itemAt', 'moveItem',
            'removeAt', 'removeItem', 'removeItems',
            'selectionMode', 'setSelectionMode', 'selectedItems', 'selectedLabels',
            'setCurrentRow', 'setCurrentItem'])
        )
    _forwardWidget = TTkListWidget

    def __init__(self, *,
                 listWidget:TTkListWidget=None,
                 selectionMode:int=TTkK.SingleSelection,
                 dragDropMode:TTkK.DragDropMode=TTkK.DragDropMode.NoDragDrop,
                 **kwargs) -> None:
        '''
        :param listWidget: a custom List Widget to be used instead of the default one.
        :type listWidget: :py:class:`TTkListWidget`, optional
        '''
        self._listView = listWidget if listWidget else TTkListWidget(
                                                            selectionMode=selectionMode,
                                                            dragDropMode=dragDropMode,
                                                            **kwargs|{'parent':None,'visible':True})
        super().__init__(**kwargs)
        self.setViewport(self._listView)

        for _attr in self._forwardedSignals+self._forwardedMethods:
            setattr(self,_attr,getattr(self._listView,_attr))

