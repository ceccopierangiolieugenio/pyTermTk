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

import weakref

import TermTk as ttk
import ttkDesigner.app.superobj as so

class SuperWidgetMenuButton(so.SuperWidget):
    _menuButtons = weakref.WeakKeyDictionary()
    def __init__(self, designer, wid, *args, **kwargs):
        # ttk.TTkWidget.__init__(self)
        super().__init__(designer, wid, pos=(0,0.),**kwargs)

    def hasControlWidget(self):
        return False

    def getSuperProperties(self):
        additions, exceptions, exclude = super().getSuperProperties()
        exclude += ['Layout', 'Position', 'Size', 'Min Width', 'Min Height', 'Max Width', 'Max Height', 'Padding', 'Layout', 'Visible', 'Enabled']
        return additions, exceptions, exclude

    @staticmethod
    def _swFromWidget(wid, swClass, *args, **kwargs):
        sw = swClass(wid=wid, *args, **kwargs)
        return sw

    @staticmethod
    def factoryGetSuperWidgetMenuButton(wid:ttk.TTkMenuButton, designer):
        if wid not in SuperWidgetMenuButton._menuButtons:
            SuperWidgetMenuButton._menuButtons[wid] =  weakref.ref(so.SuperWidget.swFromWidget(wid=wid, designer=designer))
        return SuperWidgetMenuButton._menuButtons[wid]()

