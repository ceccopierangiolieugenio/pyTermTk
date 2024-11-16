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

__all__ = ['TTkFancyTree']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkWidgets.Fancy.treewidget import TTkFancyTreeWidget
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea

class TTkFancyTree(TTkAbstractScrollArea):
    __slots__ = (
        '_treeView', 'activated',
        # Forwarded Methods
        'setAlignment', 'setHeader', 'setHeaderLabels', 'setColumnSize', 'setColumnColors', 'appendItem', 'addTopLevelItem' )

    def __init__(self, **kwargs) -> None:
        TTkAbstractScrollArea.__init__(self, **kwargs)
        kwargs.pop('parent',None)
        kwargs.pop('visible',None)
        self._treeView = TTkFancyTreeWidget(**kwargs)
        # Forward the signal
        self.activated = self._treeView.activated

        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._treeView)

        # Forwarded Methods
        self.setAlignment    = self._treeView.setAlignment
        self.setHeader       = self._treeView.setHeader
        self.setHeaderLabels = self._treeView.setHeaderLabels
        self.setColumnSize   = self._treeView.setColumnSize
        self.setColumnColors = self._treeView.setColumnColors
        self.appendItem      = self._treeView.appendItem
        self.addTopLevelItem = self._treeView.addTopLevelItem



