# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.TTkModelView.tree import TTkTree
from TermTk.TTkWidgets.TTkModelView.treewidgetitem import TTkTreeWidgetItem

class TTkDomTreeView(TTkWidget):
    __slots__ = ('_domTree')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = TTkGridLayout()
        self.setLayout(layout)


        self._domTree = TTkTree()
        self._domTree.setHeaderLabels(["Object", "Class", "Visibility", "Layout"])
        self._domTree.addTopLevelItem(TTkDomTreeView._getDomTreeItem(TTkHelper._rootWidget._widgetItem))

        btnRefresh = TTkButton(text="refresh")
        btnRefresh.clicked.connect(self._refresh)

        layout.addWidget(btnRefresh, 0,0)
        layout.addWidget(self._domTree, 1,0)

    @pyTTkSlot()
    def _refresh(self):
        self._domTree.clear()
        self._domTree.addTopLevelItem(TTkDomTreeView._getDomTreeItem(TTkHelper._rootWidget._widgetItem))

    @staticmethod
    def _getDomTreeItem(layoutItem):
        if layoutItem.layoutItemType == TTkK.WidgetItem:
            widget = layoutItem.widget()
            top = TTkTreeWidgetItem([
                        widget._name,   widget.__class__.__name__,
                        str(widget.isVisible()),
                        widget.layout().__class__.__name__])
            for c in widget.layout().children():
                top.addChild(TTkDomTreeView._getDomTreeItem(c))

            for c in widget.rootLayout().children():
                if c == widget.layout(): continue
                top.addChild(tc:=TTkTreeWidgetItem(["layout (Other)", c.__class__.__name__, ""]))
                for cc in c.children():
                    tc.addChild(TTkDomTreeView._getDomTreeItem(cc))
            return top

        if layoutItem.layoutItemType == TTkK.LayoutItem:
            top = TTkTreeWidgetItem(["layout", layoutItem.__class__.__name__,"",layoutItem.__class__.__name__])
            for c in layoutItem.children():
                top.addChild(TTkDomTreeView._getDomTreeItem(c))
            return top

        return TTkTreeWidgetItem(["ERROR!!!", "None"])


