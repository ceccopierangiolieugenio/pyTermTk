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

class _DetailLazyFormView(ttk.TTkAbstractScrollView):
    __slots__ = ('_gridLayout', '_lazyRows', '_lastRow')
    def __init__(self, *args, **kwargs):
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

    @ttk.pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def viewFullAreaSize(self) -> (int, int):
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w , h+1

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def paintEvent(self):
        x,y = self.getViewOffsets()
        w,h = self.size()
        tt = ttk.TTkCfg.theme.tree
        header=["Property","Value"]
        columnsPos = [self.width()//2,self.width()]

        for i,l in enumerate(header):
            hx  = 0 if i==0 else columnsPos[i-1]+1
            hx1 = columnsPos[i]
            self._canvas.drawText(pos=(hx-x,0), text=l, width=hx1-hx, color=ttk.TTkCfg.theme.treeHeaderColor)

class PropertyEditor(ttk.TTkGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._detail = ttk.TTkFrame()
        self._widget = ttk.TTkWidget()
        self._superWidget = ttk.TTkWidget()
        self.addWidget(self._detail)

    @ttk.pyTTkSlot(ttk.TTkWidget, ttk.TTkWidget)
    def setDetail(self, widget, superWidget):
        self._widget = widget
        self._superWidget = superWidget
        self.removeWidget(self._detail)
        self._makeDetail(widget)
        self.addWidget(self._detail)

    def _makeDetail(self, domw):
        self._detail = ttk.TTkScrollArea(verticalScrollBarPolicy=ttk.TTkK.ScrollBarAlwaysOn)
        dlfv =_DetailLazyFormView()
        self._detail.setViewport(dlfv)
        proplist = []
        for cc in reversed(type(domw).__mro__):
            if hasattr(cc,'_ttkProperties'):
                dlfv.addFormRow(ttk.TTkLabel(
                        minSize=(30,1), maxHeight=1,
                        color=ttk.TTkColor.bg('#000099')+ttk.TTkColor.fg('#ffff00'),
                        text=f"{cc.__name__}"))
                for p in cc._ttkProperties:
                    prop = cc._ttkProperties[p]
                    if prop not in proplist:
                        proplist.append(prop)
                        if 'get' in prop:
                            def _bound(_f,_w,_l):
                                def _ret(_v):
                                    _f(_w,_l(_v))
                                    self._superWidget.updateAll()
                                return _ret
                            def _boundFlags(_f,_g,_w,_l,_flag):
                                def _ret(_v):
                                    _val = _g(_w)
                                    _val = _val|_flag if _l(_v) else _val&~_flag
                                    _f(_w,_val)
                                    self._superWidget.updateAll()
                                return _ret
                            getval = prop['get']['cb'](domw)
                            if prop['get']['type'] == 'multiflags':
                                flags = prop['get']['flags']
                                value = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(), height=len(flags), border=False)
                                for fl in flags:
                                    if 'set' in prop:
                                        value.layout().addWidget(fcb := ttk.TTkCheckbox(text=f" {fl}", checked=bool(prop['get']['cb'](domw)&flags[fl])))
                                        fcb.stateChanged.connect(_boundFlags(
                                                    prop['set']['cb'], prop['get']['cb'],
                                                    domw, lambda v: v==ttk.TTkK.Checked, flags[fl]))
                                    else:
                                        value.layout().addWidget(fcb := ttk.TTkCheckbox(text=f" {fl}", checked=bool(prop['get']['cb'](domw)&flags[fl]), enabled=False))
                            elif prop['get']['type'] == 'singleflag':
                                flags = prop['get']['flags']
                                items = [(k,v) for k,v in flags.items()]
                                if 'set' in prop:
                                    value = ttk.TTkComboBox(list=[n for n,_ in items], height=1, textAlign=ttk.TTkK.LEFT_ALIGN)
                                    value.setCurrentIndex([cs for _,cs in items].index(getval))
                                    value.currentTextChanged.connect(_bound(prop['set']['cb'],domw, lambda v:flags[v]))
                                else:
                                    value = ttk.TTkLabel(text=items[[cs for _,cs in items].index(getval)][0])
                            elif prop['get']['type'] == bool and 'set' in prop:
                                value = ttk.TTkCheckbox(text=f" {p}", checked=getval, height=1)
                                value.stateChanged.connect(_bound(prop['set']['cb'],domw, lambda v:v==ttk.TTkK.Checked))
                            elif prop['get']['type'] == int and 'set' in prop:
                                value = ttk.TTkSpinBox(value=getval, height=1)
                                value.valueChanged.connect(_bound(prop['set']['cb'],domw,lambda v:v))
                            elif prop['get']['type'] == ttk.TTkString and 'set' in prop:
                                value = ttk.TTkLineEdit(text=getval, height=1)
                                value.textEdited.connect(_bound(prop['set']['cb'],domw,lambda v:v))
                            elif prop['get']['type'] == ttk.TTkColor and 'set' in prop:
                                value = ttk.TTkColorButtonPicker(color=getval, height=1)
                                value.colorSelected.connect(_bound(prop['set']['cb'],domw,lambda v:v))
                            elif type(prop['get']['type']) == dict:
                                curVal = prop['get']['cb'](domw)
                                value = ttk.TTkLabel(text=f"{curVal}")
                            else:
                                if type(prop['get']['type']) == str:
                                    getval = f"{prop['get']['type']} = {getval}"
                                elif issubclass(prop['get']['type'], ttk.TTkLayout):
                                    getval = getval.__class__.__name__
                                value = ttk.TTkLabel(minSize=(30,1), maxHeight=1, text=f"{getval}", height=1)
                            dlfv.addFormRow(
                                ttk.TTkLabel(
                                    minSize=(30,1), maxHeight=1,
                                    color=ttk.TTkColor.bg('#222222')+ttk.TTkColor.fg('#88ffff'),
                                    text=f" - {p}"),
                                value,)