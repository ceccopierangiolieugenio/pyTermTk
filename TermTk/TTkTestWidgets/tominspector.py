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

__all__ = ['TTkTomInspector']

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.TTkTerm.input import TTkInput
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkLayouts.boxlayout import TTkVBoxLayout
from TermTk.TTkWidgets.label import TTkLabel
from TermTk.TTkWidgets.lineedit import TTkLineEdit
from TermTk.TTkWidgets.combobox import TTkComboBox
from TermTk.TTkWidgets.checkbox import TTkCheckbox
from TermTk.TTkWidgets.spinbox import TTkSpinBox
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.splitter import TTkSplitter
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.scrollarea import TTkScrollArea, TTkAbstractScrollView
from TermTk.TTkWidgets.TTkModelView.tree import TTkTree
from TermTk.TTkWidgets.TTkModelView.treewidgetitem import TTkTreeWidgetItem
from TermTk.TTkWidgets.TTkPickers.colorpicker import TTkColorButtonPicker

class _DetailGridView(TTkAbstractScrollView):
    __slots__ = ('_gridLayout')
    def __init__(self, *args, **kwargs) -> None:
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

    def viewFullAreaSize(self) -> tuple[int,int]:
        _,_,w,h = self._gridLayout.fullWidgetAreaGeometry()
        return w , h

class _DetailLazyFormView(TTkAbstractScrollView):
    __slots__ = ('_gridLayout', '_lazyRows', '_lastRow')
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setPadding(1,0,0,0)
        self._lastRow = 0
        self._lazyRows = []
        self.viewChanged.connect(self._viewChangedHandler)

    def resizeEvent(self, w, h):
        for row in self._lazyRows:
            if len(row) == 1:
                _w = [w]
                _x = [0]
            else:
                _w = [w//2,w//2]
                _x = [0,w//2]
            for i,wid in enumerate(row):
                wx, wy, ww, wh = wid.geometry()
                wid.setGeometry(_x[i],wy,_w[i],wh)
        return super().resizeEvent(w, h)

    def addFormRow(self, *args):
        w = self.width()
        x = 0
        h = 0
        row = []
        for wid in args:
            ww,wh = wid.size()
            row.append(wid)
            self.layout().addWidget(wid)
            wid.setGeometry(x,self._lastRow,w//len(args),wh)
            x+=w//len(args)
            h = max(h,wh)
        self._lazyRows.append(row)
        self._lastRow+=h

    @pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def viewFullAreaSize(self) -> tuple[int,int]:
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w , h+1

    def paintEvent(self, canvas):
        x,y = self.getViewOffsets()
        w,h = self.size()
        tt = TTkCfg.theme.tree
        header=["Property","Value"]
        columnsPos = [self.width()//2,self.width()]

        for i,l in enumerate(header):
            hx  = 0 if i==0 else columnsPos[i-1]+1
            hx1 = columnsPos[i]
            canvas.drawText(pos=(hx-x,0), text=l, width=hx1-hx, color=TTkCfg.theme.treeHeaderColor)

class _TTkDomTreeWidgetItem(TTkTreeWidgetItem):
    __slots__ = ('_domWidget')
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._domWidget = kwargs.get('domWidget')
    def domWidget(self):
        return self._domWidget

class TTkTomInspector(TTkContainer):
    __slots__ = ('_domTree','_detail','_splitter')
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        layout = TTkGridLayout()
        self.setLayout(layout)

        self._domTree = TTkTree()
        self._domTree.setHeaderLabels(["Object", "Class", "Visibility", "Layout"])
        self._domTree.addTopLevelItem(TTkTomInspector._getTomTreeItem(TTkHelper._rootWidget._widgetItem))

        self._detail = TTkFrame()

        self._splitter = TTkSplitter(orientation=TTkK.VERTICAL)
        self._splitter.addWidget(self._domTree)
        self._splitter.addWidget(self._detail)

        btnRefresh = TTkButton(text="Refresh")
        btnRefresh.clicked.connect(self._refresh)

        btnPick = TTkButton(text="Pick 🔍")
        btnPick.clicked.connect(self._btnPickCb)

        layout.addWidget(btnPick,    0,0)
        layout.addWidget(btnRefresh, 0,1,1,2)
        layout.addWidget(self._splitter, 1,0,1,3)

        self._domTree.itemClicked.connect(self._setDetail)

    @staticmethod
    def _findWidget(evt, layout):
        ''' .. caution:: Don't touch this! '''
        x, y = evt.x, evt.y
        lx,ly,lw,lh =layout.geometry()
        lox, loy = layout.offset()
        lx,ly,lw,lh = lx+lox, ly+loy, lw-lox, lh-loy
        # opt of bounds
        if x<lx or x>=lx+lw or y<ly or y>=lh+ly: return None
        x-=lx
        y-=ly
        for item in reversed(layout.zSortedItems):
        # for item in layout.zSortedItems:
            if item.layoutItemType() == TTkK.WidgetItem and not item.isEmpty():
                widget = item.widget()
                if not widget._visible: continue
                if isinstance(evt, TTkMouseEvent):
                    wx,wy,ww,wh = widget.geometry()
                    # Skip the mouse event if outside this widget
                    if wx <= x < wx+ww and wy <= y < wy+wh:
                        wevt = evt.clone(pos=(x-wx, y-wy))
                        return TTkTomInspector._findWidget(wevt,widget.rootLayout())
                    continue

            elif item.layoutItemType() == TTkK.LayoutItem:
                levt = evt.clone(pos=(x, y))
                if (wid:=TTkTomInspector._findWidget(levt, item)):
                    return wid
        return layout.parentWidget()

    @pyTTkSlot(TTkKeyEvent, TTkMouseEvent)
    def _processInput(self, kevt, mevt):
        TTkLog.debug(f"{kevt} {mevt}")
        if mevt.evt == TTkK.Press:
            # TTkHelper._rootWidget.setEnabled(True)
            # TTkInput.inputEvent.connect(TTkHelper._rootWidget._processInput)
            TTkInput.inputEvent.disconnect(self._processInput)
            widget = TTkTomInspector._findWidget(mevt,TTkHelper._rootWidget.rootLayout())
            TTkLog.debug(f"{widget=}")
            if widget:
                self._makeDetail(widget)
            else:
                self._detail = TTkFrame(title=f"None")
            self._splitter.replaceWidget(1,self._detail)
            self._refresh(widget)

    @pyTTkSlot()
    def _btnPickCb(self):
        # TTkHelper._rootWidget.setEnabled(True)
        # TTkInput.inputEvent.disconnect(TTkHelper._rootWidget._processInput)
        TTkInput.inputEvent.connect(self._processInput)

    @pyTTkSlot()
    def _refresh(self, widget=None):
        self._domTree.clear()
        self._domTree.addTopLevelItem(TTkTomInspector._getTomTreeItem(TTkHelper._rootWidget._widgetItem, widget))

    @pyTTkSlot(_TTkDomTreeWidgetItem, int)
    def _setDetail(self, widget, _):
        if domw :=  widget.domWidget():
            self._makeDetail(domw)
        else:
            self._detail = TTkFrame(title=f"None")
        self._splitter.replaceWidget(1,self._detail)

    def _makeDetail(self, domw):
        self._detail = TTkScrollArea(verticalScrollBarPolicy=TTkK.ScrollBarAlwaysOn)
        dlfv =_DetailLazyFormView()
        self._detail.setViewport(dlfv)
        proplist = []
        for cc in reversed(type(domw).__mro__):
            if hasattr(cc,'_ttkProperties'):
                dlfv.addFormRow(TTkLabel(
                        minSize=(30,1), maxHeight=1,
                        color=TTkColor.bg('#000099')+TTkColor.fg('#ffff00'),
                        text=f"{cc.__name__}"))
                for p in cc._ttkProperties:
                    prop = cc._ttkProperties[p]
                    if prop not in proplist:
                        proplist.append(prop)
                        if 'get' in prop:
                            def _bound(_f,_w,_l):
                                def _ret(_v):
                                    _f(_w,_l(_v))
                                return _ret
                            def _boundFlags(_f,_g,_w,_l,_flag):
                                def _ret(_v):
                                    _val = _g(_w)
                                    _val = _val|_flag if _l(_v) else _val&~_flag
                                    _f(_w,_val)
                                return _ret
                            getval = prop['get']['cb'](domw)
                            if prop['get']['type'] == 'multiflags':
                                flags = prop['get']['flags']
                                value = TTkFrame(layout=TTkVBoxLayout(), height=len(flags), border=False)
                                for fl in flags:
                                    if 'set' in prop:
                                        value.layout().addWidget(fcb := TTkCheckbox(text=f" {fl}", checked=bool(prop['get']['cb'](domw)&flags[fl])))
                                        fcb.stateChanged.connect(_boundFlags(
                                                    prop['set']['cb'], prop['get']['cb'],
                                                    domw, lambda v: v==TTkK.Checked, flags[fl]))
                                    else:
                                        value.layout().addWidget(fcb := TTkCheckbox(text=f" {fl}", checked=bool(prop['get']['cb'](domw)&flags[fl]), enabled=False))
                            elif prop['get']['type'] == 'singleflag':
                                flags = prop['get']['flags']
                                items = [(k,v) for k,v in flags.items()]
                                if 'set' in prop:
                                    value = TTkComboBox(list=[n for n,_ in items], height=1, textAlign=TTkK.LEFT_ALIGN)
                                    value.setCurrentIndex([cs for _,cs in items].index(getval))
                                    value.currentTextChanged.connect(_bound(prop['set']['cb'],domw, lambda v:flags[v]))
                                else:
                                    value = TTkLabel(text=items[[cs for _,cs in items].index(getval)][0])
                            elif prop['get']['type'] == bool and 'set' in prop:
                                value = TTkCheckbox(text=f" {p}", checked=getval, height=1)
                                value.stateChanged.connect(_bound(prop['set']['cb'],domw, lambda v:v==TTkK.Checked))
                            elif prop['get']['type'] == int and 'set' in prop:
                                value = TTkSpinBox(value=getval, height=1)
                                value.valueChanged.connect(_bound(prop['set']['cb'],domw,lambda v:v))
                            elif prop['get']['type'] == TTkString and 'set' in prop:
                                value = TTkLineEdit(text=getval, height=1)
                                value.textEdited.connect(_bound(prop['set']['cb'],domw,lambda v:v))
                            elif prop['get']['type'] == TTkColor and 'set' in prop:
                                value = TTkColorButtonPicker(color=getval, height=1)
                                value.colorSelected.connect(_bound(prop['set']['cb'],domw,lambda v:v))
                            elif type(prop['get']['type']) == dict:
                                curVal = prop['get']['cb'](domw)
                                value = TTkLabel(text=f"{curVal}")
                            else:
                                if type(prop['get']['type']) == str:
                                    getval = f"{prop['get']['type']} = {getval}"
                                elif issubclass(prop['get']['type'], TTkLayout):
                                    getval = getval.__class__.__name__
                                value = TTkLabel(minSize=(30,1), maxHeight=1, text=f"{getval}", height=1)
                            dlfv.addFormRow(
                                TTkLabel(
                                    minSize=(30,1), maxHeight=1,
                                    color=TTkColor.bg('#222222')+TTkColor.fg('#88ffff'),
                                    text=f" - {p}"),
                                value,)


    @staticmethod
    def _getTomTreeItem(layoutItem, widSelected=None):
        if layoutItem.layoutItemType() == TTkK.WidgetItem:
            widget = layoutItem.widget()
            expanded = TTkHelper.isParent(widSelected,widget) if widSelected else False
            top = _TTkDomTreeWidgetItem([
                        widget._name,   widget.__class__.__name__,
                        str(widget.isVisible()),
                        widget.layout().__class__.__name__],
                        domWidget=widget,
                        expanded=expanded)
            for c in widget.layout().children():
                top.addChild(TTkTomInspector._getTomTreeItem(c,widSelected))

            for c in widget.rootLayout().children():
                if c == widget.layout(): continue
                if c.layoutItemType() == TTkK.LayoutItem:
                    top.addChild(tc:=_TTkDomTreeWidgetItem(["layout (Other)", c.__class__.__name__, ""]))
                    for cc in c.children():
                        tc.addChild(TTkTomInspector._getTomTreeItem(cc,widSelected))
            return top

        if layoutItem.layoutItemType() == TTkK.LayoutItem:
            top = _TTkDomTreeWidgetItem(["layout", layoutItem.__class__.__name__,"",layoutItem.__class__.__name__])
            for c in layoutItem.children():
                top.addChild(TTkTomInspector._getTomTreeItem(c,widSelected))
            return top

        return _TTkDomTreeWidgetItem(["ERROR!!!", "None"])


