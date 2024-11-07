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
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkWidgets.TTkModelView.treewidget import TTkTreeWidget
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea

class TTkTree(TTkAbstractScrollArea):
    __doc__ = '''
    :py:class:`TTkTree` is a container widget which place :py:class:`TTkTreeWidget` in a scrolling area with on-demand scroll bars.

    ''' + TTkTreeWidget.__doc__

    __slots__ = tuple(
        ['_treeView'] +
        (_forwardedSignals:=[# Forwarded Signals From TTkTreeWidget
            'itemActivated', 'itemChanged', 'itemClicked', 'itemExpanded', 'itemCollapsed', 'itemDoubleClicked']) +
        (_forwardedMethods:=[# Forwarded Methods From TTkTreeWidget
            'setHeaderLabels',
            'setColumnWidth', 'resizeColumnToContents',
            'sortColumn', 'sortItems',
            # 'appendItem', 'setAlignment', 'setColumnColors', 'setColumnSize', 'setHeader',
            'addTopLevelItem', 'addTopLevelItems', 'takeTopLevelItem', 'topLevelItem', 'indexOfTopLevelItem', 'selectedItems', 'clear'])
        )
    _forwardWidget = TTkTreeWidget

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

        for _attr in self._forwardedSignals+self._forwardedMethods:
            setattr(self,_attr,getattr(self._treeView,_attr))
