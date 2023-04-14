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

# Yaml is not included by default
# import yaml
import os, json

from TermTk import TTkLog
from TermTk import TTkCfg
from TermTk.TTkLayouts import TTkLayout, TTkGridLayout, TTkVBoxLayout, TTkHBoxLayout
from TermTk.TTkWidgets import *
from TermTk.TTkTestWidgets import *
from TermTk.TTkUiTools.uiproperties import TTkUiProperties

class TTkUiLoader():
    @staticmethod
    def loadFile(filePath):
        with open(filePath) as f:
            return TTkUiLoader.loadJson(f.read())
        return None

    @staticmethod
    def loadJson(text):
        return TTkUiLoader.loadDict(json.loads(text))

    @staticmethod
    def _loadDict_1_0_0(ui):
        def _getWidget(widProp):
            properties = {}
            ttkClass = globals()[widProp['class']]
            for cc in reversed(ttkClass.__mro__):
                if cc.__name__ in TTkUiProperties:
                    properties |= TTkUiProperties[cc.__name__]['properties']
            # Init params used in the constructors
            kwargs = {}
            # Init params to be configured with the setter
            setters = []
            layout = _getLayout(widProp['layout']) if 'layout' in widProp else TTkLayout()
            for pname in widProp['params']:
                if 'init' in properties[pname]:
                    initp = properties[pname]['init']
                    name = initp['name']
                    if initp['type'] is TTkLayout:
                        value = layout
                    elif initp['type'] is TTkColor:
                        value = TTkColor.ansi(widProp['params'][pname])
                    else:
                        value = widProp['params'][pname]
                    # TTkLog.debug(f"{name=} {value=}")
                    kwargs |= {name: value}
                elif 'set' in properties[pname]:
                    setp = properties[pname]['set']
                    setcb = setp['cb']
                    if setp['type'] is TTkLayout:
                        value = layout
                    elif setp['type'] is TTkColor:
                        value = TTkColor.ansi(widProp['params'][pname])
                    else:
                        value = widProp['params'][pname]
                    setters.append({
                                'cb':setcb,
                                'value': value,
                                'multi':type(setp['type']) is list})
            widget = ttkClass(**kwargs)
            # Init params that don't have a constrictor
            for s in setters:
                if s['multi']:
                    s['cb'](widget, *s['value'])
                else:
                    s['cb'](widget, s['value'])
            TTkLog.debug(widget)
            # for c in widProp['children']:
            #     widget.layout().addWidget(_getWidget(c))
            return widget

        def _getLayout(layprop):
            properties = {}
            ttkClass = globals()[layprop['class']]
            for cc in reversed(ttkClass.__mro__):
                if cc.__name__ in TTkUiProperties:
                    properties |= TTkUiProperties[cc.__name__]['properties']

            setters = []
            for pname in layprop['params']:
                if 'set' in properties[pname]:
                    setp = properties[pname]['set']
                    setcb = setp['cb']
                    if setp['type'] is TTkLayout:
                        value = layout
                    elif setp['type'] is TTkColor:
                        value = TTkColor.ansi(layprop['params'][pname])
                    else:
                        value = layprop['params'][pname]
                    setters.append({
                                'cb':setcb,
                                'value': value,
                                'multi':type(setp['type']) is list})

            layout = globals()[layprop['class']]()
            # Init params that don't have a constrictor
            for s in setters:
                if s['multi']:
                    s['cb'](layout, *s['value'])
                else:
                    s['cb'](layout, s['value'])

            for c in layprop['children']:
                row = c.get('row', 0)
                col = c.get('col', 0)
                rowspan = c.get('rowspan', 1)
                colspan = c.get('colspan', 1)
                if   issubclass(ttkClass,TTkGridLayout):
                    if issubclass(globals()[c['class']],TTkLayout):
                        l = _getLayout(c)
                        TTkGridLayout.addItem(layout,l,row,col,rowspan,colspan)
                    else:
                        w = _getWidget(c)
                        TTkGridLayout.addWidget(layout,w,row,col,rowspan,colspan)
                else:
                    if issubclass(globals()[c['class']],TTkLayout):
                        l = _getLayout(c)
                        l._row, l._col = row, col
                        l._rowspan, l._colspan = rowspan, colspan
                        layout.addItem(l)
                    else:
                        w = _getWidget(c)
                        w._row, w._col = row, col
                        w._rowspan, w._colspan = rowspan, colspan
                        layout.addWidget(w)
            return layout

        TTkLog.debug(ui)

        if issubclass(globals()[ui['tui']['class']],TTkLayout):
            widget =  _getLayout(ui['tui'])
        else:
            widget =  _getWidget(ui['tui'])

        def _getSignal(sender, name):
            for cc in reversed(type(sender).__mro__):
                if cc.__name__ in TTkUiProperties:
                    if not name in TTkUiProperties[cc.__name__]['signals']:
                        continue
                    signame = TTkUiProperties[cc.__name__]['signals'][name]['name']
                    return getattr(sender,signame)
            return None

        def _getSlot(receiver, name):
            for cc in reversed(type(receiver).__mro__):
                if cc.__name__ in TTkUiProperties:
                    if not name in TTkUiProperties[cc.__name__]['slots']:
                        continue
                    slotname = TTkUiProperties[cc.__name__]['slots'][name]['name']
                    return getattr(receiver,slotname)
            return None


        for conn in ui['connections']:
            sender   = widget.getWidgetByName(conn['sender'])
            receiver = widget.getWidgetByName(conn['receiver'])
            signal = conn['signal']
            slot = conn['slot']
            if None in (sender,receiver): continue
            _getSignal(sender,signal).connect(_getSlot(receiver,slot))

        return widget

    @staticmethod
    def loadDict(ui):
        cb = {'1.0.0' : TTkUiLoader._loadDict_1_0_0
              }.get(ui['version'], None)
        if cb:
            return cb(ui)
        msg = (f"The used pyTermTk ({TTkCfg.version}) is not able to load this tui version ({ui['version']})")
        raise NotImplementedError(msg)

