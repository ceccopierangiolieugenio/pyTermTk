# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import TermTk as ttk

from .windoweditor import SuperWidget

class _TTkTomTreeWidgetItem(ttk.TTkTreeWidgetItem):
    __slots__ = ('_tomWidget','_tomSuperWidget')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tomWidget = kwargs.get('tomWidget')
        self._tomSuperWidget = kwargs.get('tomSuperWidget')
    def tomWidget(self):
        return self._tomWidget
    def tomSuperWidget(self):
        return self._tomSuperWidget

class TreeInspector(ttk.TTkGridLayout):
    def __init__(self, windowEditor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgetSelected = ttk.pyTTkSignal(ttk.TTkWidget, ttk.TTkWidget)
        self._windowEditor = windowEditor

        self._tomTree = ttk.TTkTree()
        self._tomTree.setHeaderLabels(["Object", "Class", "Visibility", "Layout"])
        self._tomTree.addTopLevelItem(TreeInspector._getTomTreeItem(windowEditor.getTTk().widgetItem()))

        @ttk.pyTTkSlot(_TTkTomTreeWidgetItem, int)
        def _itemSelected(wi, _):
            if tomw :=  wi.tomWidget():
                self.widgetSelected.emit(tomw, wi.tomSuperWidget())

        self._tomTree.itemClicked.connect(_itemSelected)

        btnRefresh = ttk.TTkButton(text="Refresh")
        btnRefresh.clicked.connect(self.refresh)

        btnPick = ttk.TTkButton(text="Pick 🔍")
        # btnPick.clicked.connect(self._btnPickCb)

        self.addWidget(self._tomTree, 1,0, 1,3)
        self.addWidget(btnPick,       0,0, 1,1)
        self.addWidget(btnRefresh,    0,1, 1,2)

    #@ttk.pyTTkSlot(ttk.TTkKeyEvent, ttk.TTkMouseEvent)
    #def _processInput(self, kevt, mevt):
    #    ttk.TTkLog.debug(f"{kevt} {mevt}")
    #    if mevt.evt == TTkK.Press:
    #        # TTkHelper._rootWidget.setEnabled(True)
    #        # TTkHelper._rootWidget._input.inputEvent.connect(TTkHelper._rootWidget._processInput)
    #        ttk.TTkHelper._rootWidget._input.inputEvent.disconnect(self._processInput)
    #        widget = TTkTomInspector._findWidget(mevt,ttk.TTkHelper._rootWidget.rootLayout())
    #        ttk.TTkLog.debug(f"{widget=}")
    #        if widget:
    #            self._makeDetail(widget)
    #        else:
    #            self._detail = ttk.TTkFrame(title=f"None")
    #        self._splitter.replaceWidget(1,self._detail)
    #        self._refresh(widget)

    @ttk.pyTTkSlot()
    def _btnPickCb(self):
        # ttk.TTkHelper._rootWidget._input.inputEvent.connect(self._processInput)
        pass

    @ttk.pyTTkSlot()
    def refresh(self, widget=None):
        self._tomTree.clear()
        self._tomTree.addTopLevelItem(TreeInspector._getTomTreeItem(self._windowEditor.getTTk().widgetItem()))

    @staticmethod
    def _getTomTreeItem(layoutItem, widSelected=None):
        if layoutItem.layoutItemType == ttk.TTkK.WidgetItem:
            superWidget = widget = layoutItem.widget()
            if type(superWidget) is SuperWidget:
                widget = widget._wid
            expanded = True # ttk.TTkHelper.isParent(widSelected,widget) if widSelected else False
            top = _TTkTomTreeWidgetItem([
                        widget._name,   widget.__class__.__name__,
                        str(widget.isVisible()),
                        widget.layout().__class__.__name__],
                        tomWidget=widget,
                        tomSuperWidget=superWidget,
                        expanded=expanded)
            for c in superWidget.layout().children():
                top.addChild(TreeInspector._getTomTreeItem(c,widSelected))

            for c in widget.rootLayout().children():
                if c == widget.layout(): continue
                if c.layoutItemType == ttk.TTkK.LayoutItem:
                    top.addChild(tc:=_TTkTomTreeWidgetItem(["layout (Other)", c.__class__.__name__, ""]))
                    for cc in c.children():
                        tc.addChild(TreeInspector._getTomTreeItem(cc,widSelected))
            return top

        if layoutItem.layoutItemType == ttk.TTkK.LayoutItem:
            top = _TTkTomTreeWidgetItem(["layout", layoutItem.__class__.__name__,"",layoutItem.__class__.__name__])
            for c in layoutItem.children():
                top.addChild(TreeInspector._getTomTreeItem(c,widSelected))
            return top

        return _TTkTomTreeWidgetItem(["ERROR!!!", "None"])