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

__all__ = ['TTkFancyTable']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.Fancy.tableview import TTkFancyTableView
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea

class TTkFancyTable(TTkAbstractScrollArea):
    __slots__ = (
        '_tableView', 'activated',
        # Forwarded Methods
        'setAlignment', 'setHeader', 'setColumnSize', 'setColumnColors', 'appendItem' )




    def __init__(self, *,
                 # TTkWidget init
                 parent:TTkWidget=None,
                 visible:bool=True,
                 # TTkFancyTableView init
                 columns:list[int]=None,
                 columnColors:list[TTkColor]=None,
                 selectColor:TTkColor=TTkColor.BOLD,
                 headerColor:TTkColor=TTkColor.BOLD,
                 showHeader:bool=True,
                 **kwargs) -> None:
        super().__init__(parent=parent, visible=visible, **kwargs)
        self._tableView = TTkFancyTableView(columns=columns, columnColors=columnColors, selectColor=selectColor, headerColor=headerColor, showHeader=showHeader, **kwargs)
        # Forward the signal
        self.activated = self._tableView.activated

        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._tableView)
        # Forwarded Methods
        self.setAlignment    = self._tableView.setAlignment
        self.setHeader       = self._tableView.setHeader
        self.setColumnSize   = self._tableView.setColumnSize
        self.setColumnColors = self._tableView.setColumnColors
        self.appendItem      = self._tableView.appendItem




