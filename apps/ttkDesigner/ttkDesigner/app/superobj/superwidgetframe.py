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
import ttkDesigner.app.superobj as so
from ttkDesigner.app.menuBarEditor import MenuBarEditor

class SuperWidgetFrame(so.SuperWidgetContainer):
    def getSuperProperties(self):
        additions, exceptions, exclude = super().getSuperProperties()
        additions |= {
            ttk.TTkFrame.__name__ : {
                'Menu Bar' : {
                    'get':  {'cb':MenuBarEditor.spawnMenuBarEditor(self._designer), 'type':'button', 'text':'Edit'},
                    'set':  {'cb':MenuBarEditor.spawnMenuBarEditor(self._designer), 'type':'button', 'text':'Edit'} },
            }
        }
        return additions, exceptions, exclude

    def dumpDict(self):
        def _dumpMenuBarItem(_mbi:ttk.TTkMenuButton):
            if not issubclass(type(_mbi),ttk.TTkMenuButton):
                return "spacer"

            ret = {'params': {
                        'Name':      _mbi.name(),
                        'ToolTip':   _mbi.toolTip().toAnsi(True),
                        'Text':      _mbi.text().toAnsi(True),
                        'Checkable': _mbi.isCheckable(),
                        'Checked':   _mbi.isChecked(),
                    }
                }
            if _sm := _dumpMenuBarItems(_mbi._submenu):
                ret |= {'submenu': _sm}
            return ret

        def _dumpMenuBarItems(_mbis):
            return [_dumpMenuBarItem(_i) for _i in _mbis]

        def _dumpMenuBar(_mb):
            ret = {}
            if _mbis := _mb._mbItems(ttk.TTkK.LEFT_ALIGN).children():
                ret |= {'left':_dumpMenuBarItems([_i.widget() for _i in _mbis])}
            if _mbis := _mb._mbItems(ttk.TTkK.CENTER_ALIGN).children():
                ret |= {'center':_dumpMenuBarItems([_i.widget() for _i in _mbis])}
            if _mbis := _mb._mbItems(ttk.TTkK.RIGHT_ALIGN).children():
                ret |= {'right':_dumpMenuBarItems([_i.widget() for _i in _mbis])}
            return ret

        ret = super().dumpDict()
        barTop    = self._wid.menuBar(ttk.TTkK.TOP)
        barBottom = self._wid.menuBar(ttk.TTkK.BOTTOM)
        if barTop or barBottom:
            ret |= {'menuBar' : {}}
            if barTop:
                ret['menuBar']['top'] = _dumpMenuBar(barTop)
            if barBottom:
                ret['menuBar']['bottom'] = _dumpMenuBar(barBottom)
        return ret
