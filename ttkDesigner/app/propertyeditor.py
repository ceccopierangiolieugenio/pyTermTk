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
        self._detail = ttk.TTkTree()
        self._detail.setHeaderLabels(["Property","Value"])
        self._widget = ttk.TTkWidget()
        self._superWidget = ttk.TTkWidget()
        self.addWidget(self._detail)

    @ttk.pyTTkSlot(ttk.TTkWidget, ttk.TTkWidget)
    def setDetail(self, widget, superWidget):
        self._widget = widget
        self._superWidget = superWidget
        self._makeDetail(widget)

    def _makeDetail(self, domw):
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
        def _boundTextEdit(_f,_w,_te):
            def _ret():
                _v = _te.getTTkString()
                _f(_w,_v)
                self._superWidget.updateAll()
            return _ret

        # Multi Flag Fields
        # ▼ Input Type     │ - (0x0001)
        #   • Text         │[X] 0x0001
        #   • Number       │[ ] 0x0002
        #   • Password     │[ ] 0x0004
        def _processMultiFlag(name, prop):
            flags = prop['get']['flags']
            ret = ttk.TTkTreeWidgetItem([name,f" - (0x{prop['get']['cb'](domw):04X})"],expanded=True)
            # value = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(), height=len(flags), border=False)
            for fl in flags:
                if 'set' in prop:
                    fcb = ttk.TTkCheckbox(text=f" 0x{flags[fl]:04X}", checked=bool(prop['get']['cb'](domw)&flags[fl]))
                    fcb.stateChanged.connect(_boundFlags(
                                prop['set']['cb'], prop['get']['cb'],
                                domw, lambda v: v==ttk.TTkK.Checked, flags[fl]))
                else:
                    fcb = ttk.TTkCheckbox(text=f" 0x{flags[fl]:04X}", checked=bool(prop['get']['cb'](domw)&flags[fl]), enabled=False)
                ret.addChild(ttk.TTkTreeWidgetItem([f"{fl}", fcb]))
            return ret

        # Single Flag Fields
        # • Check State  │[Partially Checked    ^]│
        #                │┌───────────────────┐   │
        #                ││Checked            │   │
        #                ││Unchecked          │   │
        #                ││Partially Checked  │   │
        #                │└───────────────────┘   │
        def _processSingleFlag(name, prop):
            flags = prop['get']['flags']
            items = [(k,v) for k,v in flags.items()]
            if 'set' in prop:
                value = ttk.TTkComboBox(list=[n for n,_ in items], height=1, textAlign=ttk.TTkK.LEFT_ALIGN)
                value.setCurrentIndex([cs for _,cs in items].index(prop['get']['cb'](domw)))
                value.currentTextChanged.connect(_bound(prop['set']['cb'],domw, lambda v:flags[v]))
            else:
                value = ttk.TTkLabel(text=items[[cs for _,cs in items].index(prop['get']['cb'](domw))][0])
            return ttk.TTkTreeWidgetItem([name,value])

        # List Fields
        # property in this format:
        #    'Position' : {
        #            'init': {'name':'pos', 'type': [
        #                            { 'name': 'x', 'type':int } ,
        #                            { 'name': 'y', 'type':int } ] },
        #            'get':  { 'cb':pos,    'type': [
        #                            { 'name': 'x', 'type':int } ,
        #                            { 'name': 'y', 'type':int } ] },
        #            'set':  { 'cb':move,   'type': [
        #                            { 'name': 'x', 'type':int } ,
        #                            { 'name': 'y', 'type':int } ] } },
        #
        def _processList(name, prop):
            curVal = prop['get']['cb'](domw)
            value = ttk.TTkLabel(text=f"{curVal}")
            ret = ttk.TTkTreeWidgetItem([name,value])
            for _i, _prop in enumerate(prop['get']['type']):
                _curVal = curVal[_i]
                # if
            return ret

        # Dict Fields
        def _processDict(name, prop):
            curVal = prop['get']['cb'](domw)
            value = ttk.TTkLabel(text=f"{curVal} - TBD")
            ret = ttk.TTkTreeWidgetItem([name,value])
            return ret

        # Boolean Fields
        def _processBool(name, prop):
            getval = prop['get']['cb'](domw)
            value = ttk.TTkCheckbox(text=f" {p}", checked=getval, height=1)
            value.stateChanged.connect(_bound(prop['set']['cb'],domw, lambda v:v==ttk.TTkK.Checked))
            return ttk.TTkTreeWidgetItem([name,value])
        # Integer Fields
        def _processInt(name, prop):
            getval = prop['get']['cb'](domw)
            value = ttk.TTkSpinBox(value=getval, height=1)
            value.valueChanged.connect(_bound(prop['set']['cb'],domw,lambda v:v))
            return ttk.TTkTreeWidgetItem([name,value])
        # String Fields
        def _processTTkString(name, prop):
            getval = prop['get']['cb'](domw)
            value = ttk.TTkTextPicker(text=getval, height=len(getval.split('\n')))
            value.textChanged.connect(_boundTextEdit(prop['set']['cb'],domw,value))
            return ttk.TTkTreeWidgetItem([name,value])
        # Color Fields
        def _processTTkColor(name, prop):
            getval = prop['get']['cb'](domw)
            value = ttk.TTkColorButtonPicker(color=getval, height=1)
            value.colorSelected.connect(_bound(prop['set']['cb'],domw,lambda v:v))
            return ttk.TTkTreeWidgetItem([name,value])

        # Unrecognised Field
        def _processUnknown(name, prop):
            getval = prop['get']['cb'](domw)
            if type(prop['get']['type']) == str:
                getval = f"{prop['get']['type']} = {getval}"
            elif issubclass(prop['get']['type'], ttk.TTkLayout):
                getval = getval.__class__.__name__
            value = ttk.TTkLabel(minSize=(30,1), maxHeight=1, text=f"{getval}", height=1)
            return ttk.TTkTreeWidgetItem([name,value])

        proplist = []
        self._detail.clear()
        for cc in reversed(type(domw).__mro__):
            # if hasattr(cc,'_ttkProperties'):
            if issubclass(cc, ttk.TTkWidget):
                ccName = cc.__name__
                classItem = ttk.TTkTreeWidgetItem([ccName,''], expanded=True)
                self._detail.addTopLevelItem(classItem)
                if ccName in ttk.TTkUiProperties:
                    for p in ttk.TTkUiProperties[ccName]:
                        prop = ttk.TTkUiProperties[ccName][p]
                        if prop not in proplist:
                            proplist.append(prop)
                            if 'get' in prop:
                                if prop['get']['type'] == 'multiflags':
                                    classItem.addChild(_processMultiFlag(p,prop))
                                elif prop['get']['type'] == 'singleflag':
                                    classItem.addChild(_processSingleFlag(p,prop))
                                elif prop['get']['type'] == bool and 'set' in prop:
                                    classItem.addChild(_processBool(p,prop))
                                elif prop['get']['type'] == int and 'set' in prop:
                                    classItem.addChild(_processInt(p,prop))
                                elif prop['get']['type'] == ttk.TTkString and 'set' in prop:
                                    classItem.addChild(_processTTkString(p,prop))
                                elif prop['get']['type'] == ttk.TTkColor and 'set' in prop:
                                    classItem.addChild(_processTTkColor(p,prop))
                                elif type(prop['get']['type']) == list:
                                    classItem.addChild(_processList(p,prop))
                                elif type(prop['get']['type']) == dict:
                                    classItem.addChild(_processDict(p,prop))
                                else:
                                    classItem.addChild(_processUnknown(p,prop))
