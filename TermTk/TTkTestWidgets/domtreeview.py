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
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkWidgets.label import TTkLabel
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.splitter import TTkSplitter
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.scrollarea import TTkScrollArea, TTkAbstractScrollView
from TermTk.TTkWidgets.TTkModelView.tree import TTkTree
from TermTk.TTkWidgets.TTkModelView.treewidgetitem import TTkTreeWidgetItem

class _DetailGridView(TTkAbstractScrollView):
    __slots__ = ('_gridLayout')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gridLayout = TTkGridLayout()
        self.rootLayout().addItem(self._gridLayout)
        self.viewChanged.connect(self._viewChangedHandler)

    def gridLayout(self):
        return self._gridLayout

    def resizeEvent(self, w, h):
        self._gridLayout.setGeometry(0,0,w,h)
        return super().resizeEvent(w, h)

    @pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self._gridLayout.setOffset(-x,-y)

    def viewFullAreaSize(self) -> (int, int):
        _,_,w,h = self._gridLayout.fullWidgetAreaGeometry()
        return w , h

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

class _TTkDomTreeWidgetItem(TTkTreeWidgetItem):
    __slots__ = ('_domWidget')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._domWidget = kwargs.get('domWidget')
    def domWidget(self):
        return self._domWidget

class TTkDomTreeView(TTkWidget):
    __slots__ = ('_domTree','_detail','_splitter')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = TTkGridLayout()
        self.setLayout(layout)

        self._domTree = TTkTree()
        self._domTree.setHeaderLabels(["Object", "Class", "Visibility", "Layout"])
        self._domTree.addTopLevelItem(TTkDomTreeView._getDomTreeItem(TTkHelper._rootWidget._widgetItem))

        self._detail = TTkFrame()

        self._splitter = TTkSplitter(orientation=TTkK.VERTICAL)
        self._splitter.addWidget(self._domTree)
        self._splitter.addWidget(self._detail)

        btnRefresh = TTkButton(text="refresh")
        btnRefresh.clicked.connect(self._refresh)

        layout.addWidget(btnRefresh, 0,0)
        layout.addWidget(self._splitter, 1,0)

        self._domTree.itemActivated.connect(self._setDetail)

    @pyTTkSlot()
    def _refresh(self):
        self._domTree.clear()
        self._domTree.addTopLevelItem(TTkDomTreeView._getDomTreeItem(TTkHelper._rootWidget._widgetItem))

    @pyTTkSlot(_TTkDomTreeWidgetItem, int)
    def _setDetail(self, widget, _):
        if domw :=  widget.domWidget():
            self._detail = TTkScrollArea(verticalScrollBarPolicy=TTkK.ScrollBarAlwaysOn)
            dgv = _DetailGridView()
            gl = dgv.gridLayout()
            self._detail.setViewport(dgv)
            i = 0
            proplist = []
            for cc in reversed(type(domw).__mro__):
                if hasattr(cc,'_ttkProperties'):
                    gl.addWidget(TTkLabel(
                            minSize=(30,1), maxHeight=1,
                            color=TTkColor.bg('#000099')+TTkColor.fg('#ffff00'),
                            text=f"{cc.__name__}"),i,0,1,2)
                    i+=1
                    for p in cc._ttkProperties:
                        prop = cc._ttkProperties[p]
                        if prop not in proplist:
                            proplist.append(prop)
                            if 'get' in prop:
                                value = prop['get']['cb'](domw)
                                gl.addWidget(TTkLabel(
                                        minSize=(30,1), maxHeight=1,
                                        color=TTkColor.bg('#222222')+TTkColor.fg('#88ffff'),
                                        text=f" - {p}"),i,0)
                                gl.addWidget(TTkLabel(minSize=(30,1), maxHeight=1, text=f"{value}"),i,1)
                                i+=1
        else:
            self._detail = TTkFrame(title=f"None")
        self._splitter.replaceWidget(1,self._detail)

    @staticmethod
    def _getDomTreeItem(layoutItem):
        if layoutItem.layoutItemType == TTkK.WidgetItem:
            widget = layoutItem.widget()
            top = _TTkDomTreeWidgetItem([
                        widget._name,   widget.__class__.__name__,
                        str(widget.isVisible()),
                        widget.layout().__class__.__name__],
                        domWidget=widget)
            for c in widget.layout().children():
                top.addChild(TTkDomTreeView._getDomTreeItem(c))

            for c in widget.rootLayout().children():
                if c == widget.layout(): continue
                top.addChild(tc:=_TTkDomTreeWidgetItem(["layout (Other)", c.__class__.__name__, ""]))
                for cc in c.children():
                    tc.addChild(TTkDomTreeView._getDomTreeItem(cc))
            return top

        if layoutItem.layoutItemType == TTkK.LayoutItem:
            top = _TTkDomTreeWidgetItem(["layout", layoutItem.__class__.__name__,"",layoutItem.__class__.__name__])
            for c in layoutItem.children():
                top.addChild(TTkDomTreeView._getDomTreeItem(c))
            return top

        return _TTkDomTreeWidgetItem(["ERROR!!!", "None"])


