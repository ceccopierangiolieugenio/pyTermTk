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
        # TBD
        # Override: 'name', 'radiogroup',
        # ro geometry if grid layout

        self._makeDetail(widget, *superWidget.getSuperProperties())

    def _makeDetail(self, domw, additions, exceptions, exclude):
        def _boundValue(_f,_w,_v):
            def _ret():
                _f(_w,_v)
                self._superWidget.updateAll()
            return _ret
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
        def _boundLineEdit(_f,_w,_te):
            def _ret(t):
                _v = str(t)
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
                    fcb = ttk.TTkCheckbox(text=f" 0x{flags[fl]:04X}", checked=bool(prop['get']['cb'](domw)&flags[fl]), height=1)
                    fcb.stateChanged.connect(_boundFlags(
                                prop['set']['cb'], prop['get']['cb'],
                                domw, lambda v: v==ttk.TTkK.Checked, flags[fl]))
                else:
                    fcb = ttk.TTkCheckbox(text=f" 0x{flags[fl]:04X}", checked=bool(prop['get']['cb'](domw)&flags[fl]), height=1, enabled=False)
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
            def _getter(_i, _p):
                def _ret(_w):
                    return _p['get']['cb'](_w)[_i]
                return _ret

            def _setter(_i, _p):
                def _ret(_w,_v):
                    __vals = list(_p['get']['cb'](_w))
                    __vals[_i]=_v
                    _p['set']['cb'](_w, *__vals)
                return _ret

            curVal = prop['get']['cb'](domw)
            value = ttk.TTkLabel(text=f"{curVal}")
            ret = ttk.TTkTreeWidgetItem([name,value])
            for _i, _prop in enumerate(prop['get']['type']):
                # Defining a proxy property to set or get a single value
                _newProp = {
                    'get' : { 'cb': _getter(_i, prop), 'type':_prop['type'] },
                    'set' : { 'cb': _setter(_i, prop), 'type':_prop['type'] }
                }
                # ret.addChild(ttk.TTkTreeWidgetItem([_prop['name'],f"{curVal[_i]}"]))
                ret.addChild(_processProp(_prop['name'], _newProp))
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
            value = ttk.TTkSpinBox(value=getval, height=1, maximum=0x10000, minimum=-0x10000)
            value.valueChanged.connect(_bound(prop['set']['cb'],domw,lambda v:v))
            return ttk.TTkTreeWidgetItem([name,value])
        # String Fields
        def _processStr(name, prop):
            getval = prop['get']['cb'](domw)
            value = ttk.TTkLineEdit(text=getval, height=len(getval.split('\n')))
            value.textChanged.connect(_boundLineEdit(prop['set']['cb'],domw,value))
            return ttk.TTkTreeWidgetItem([name,value])
        # String Fields
        def _processTTkString(name, prop, multiLine=True):
            getval = prop['get']['cb'](domw)
            value = ttk.TTkTextPicker(text=getval, height=len(getval.split('\n')), autoSize=True, multiLine=multiLine)
            value.textChanged.connect(_boundTextEdit(prop['set']['cb'],domw,value))
            return ttk.TTkTreeWidgetItem([name,value])
        # Color Fields
        def _processTTkColor(name, prop):
            getval = prop['get']['cb'](domw)
            value = ttk.TTkContainer(layout=ttk.TTkHBoxLayout(), height=1)
            value.layout().addWidget(_cb := ttk.TTkColorButtonPicker(color=getval, height=1))
            value.layout().addWidget(_rc := ttk.TTkButton(text=ttk.TTkString('x',ttk.TTkColor.fg('#FFAA00')),maxWidth=3))
            _cb.colorSelected.connect(_bound(prop['set']['cb'],domw,lambda v:v))
            _rc.clicked.connect(_boundValue(prop['set']['cb'],domw,ttk.TTkColor.RST))
            _rc.clicked.connect(lambda :_cb.setColor(ttk.TTkColor.RST))
            return ttk.TTkTreeWidgetItem([name,value])
        # Layout field
        def _processTTkLayout(name, prop):
            value = ttk.TTkComboBox(list=['TTkLayout','TTkGridLayout','TTkHBoxLayout','TTkVBoxLayout'], height=1)
            value.setCurrentText(prop['get']['cb'](domw).__class__.__name__)
            value.currentTextChanged.connect(_bound(prop['set']['cb'],domw, lambda v:globals()[v]()))
            return ttk.TTkTreeWidgetItem([name,value])
        # Add a button Control
        def _processButton(name, prop):
            value = ttk.TTkButton(text=f" {prop['get']['text']}", border=False)
            value.clicked.connect(lambda :prop['get']['cb'](domw))
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

        def _processProp(name, prop):
            if 'get' in prop:
                if prop['get']['type'] == 'multiflags':
                    return _processMultiFlag(name, prop)
                elif prop['get']['type'] == 'singleflag':
                    return _processSingleFlag(name, prop)
                elif prop['get']['type'] == bool and 'set' in prop:
                    return _processBool(name, prop)
                elif prop['get']['type'] == int and 'set' in prop:
                    return _processInt(name, prop)
                elif prop['get']['type'] == str and 'set' in prop:
                    return _processStr(name, prop)
                elif prop['get']['type'] == ttk.TTkString and 'set' in prop:
                    return _processTTkString(p,prop,multiLine=True)
                elif prop['get']['type'] == 'singleLineTTkString':
                    return _processTTkString(p,prop,multiLine=False)
                elif prop['get']['type'] == ttk.TTkColor and 'set' in prop:
                    return _processTTkColor(name, prop)
                elif prop['get']['type'] == ttk.TTkLayout and 'set' in prop:
                    return _processTTkLayout(name, prop)
                elif type(prop['get']['type']) == list:
                    return _processList(name, prop)
                elif type(prop['get']['type']) == dict:
                    return _processDict(name, prop)
                elif prop['get']['type'] == 'button':
                    return _processButton(p,prop)
                else:
                    return _processUnknown(name, prop)

        proplist = exclude
        self._detail.clear()
        for cc in reversed(type(domw).__mro__):
            # if hasattr(cc,'_ttkProperties'):
            if issubclass(cc, ttk.TTkWidget) or issubclass(cc, ttk.TTkLayout):
                ccName = cc.__name__
                classItem = ttk.TTkTreeWidgetItem([ccName,''], expanded=True)
                self._detail.addTopLevelItem(classItem)
                if ccName in ttk.TTkUiProperties:
                    if ccName in additions:
                        for p in additions[ccName]:
                            if p not in proplist:
                                proplist.append(p)
                                classItem.addChild(_processProp(p, additions[ccName][p]))
                    for p in ttk.TTkUiProperties[ccName]['properties']:
                        if p in exceptions:
                            prop = exceptions[p]
                        else:
                            prop = ttk.TTkUiProperties[ccName]['properties'][p]
                        if p not in proplist:
                            proplist.append(p)
                            classItem.addChild(_processProp(p, prop))
