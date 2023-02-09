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

import yaml

from TermTk import TTkLog
from TermTk.TTkLayouts import TTkLayout, TTkGridLayout, TTkVBoxLayout, TTkHBoxLayout
from TermTk.TTkWidgets import *
from TermTk.TTkUiTools.uiproperties import TTkUiProperties

class TTkUiLoader():
    @staticmethod
    def loadYaml(text):
        def _getWidget(widProp):
            properties = {}
            ttkClass = globals()[widProp['class']]
            for cc in reversed(ttkClass.__mro__):
                if cc.__name__ in TTkUiProperties:
                    properties |= TTkUiProperties[cc.__name__]
            kwargs = {}
            for pname in widProp['params']:
                if 'init' in properties[pname]:
                    initp = properties[pname]['init']
                    name = initp['name']
                    if initp['type'] is TTkLayout:
                        value = globals()[widProp['params'][pname]]()
                    elif initp['type'] is TTkColor:
                        value = TTkColor.ansi(widProp['params'][pname])
                    else:
                        value = widProp['params'][pname]
                    TTkLog.debug(f"{name=} {value=}")
                    kwargs |= {name: value}
            widget = ttkClass(**kwargs)
            TTkLog.debug(widget)
            for c in widProp['children']:
                widget.layout().addWidget(_getWidget(c))
            return widget

        widgetProperty = yaml.safe_load(text)
        TTkLog.debug(widgetProperty)
        # Yaml=
        #   params:
        #     Name: TTkButton
        #     Position:
        #     - 16
        #     - 5
        #
        # widgetProperty =
        # { 'children': [],
        #   'class': 'TTkWidget',
        #   'params': {
        #      'Enabled': True,
        #      'Layout': 'TTkLayout',
        #      'Name': 'TTk',
        #      'Padding': [0, 0, 0, 0],
        #      'Position': [4, 2],
        #      'Size': [73, 28],
        #      'Visible': True}}

        return _getWidget(widgetProperty)



