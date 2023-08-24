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

from random import randint

import TermTk as ttk

import ttkDesigner.app.superobj as so
from .superobj import SuperObject

class SuperWidgetContainer(so.SuperWidget):
    __slots__ = ('_superLayout')
    def __init__(self, designer, wid, *args, **kwargs):

        self._superLayout = so.SuperLayout(designer=designer, lay=wid.layout(),)
        self._superRootWidget = kwargs.get('superRootWidget',False)
        kwargs['layout'] = ttk.TTkGridLayout()
        kwargs['layout'].addWidget(self._superLayout)

        padt, padb, padl, padr = wid.getPadding()
        kwargs['paddingTop'] = padt
        kwargs['paddingBottom'] = padb
        kwargs['paddingLeft'] = padl
        kwargs['paddingRight'] = padr
        super().__init__(designer, wid, *args, **kwargs)

    def getSuperProperties(self):
        additions, exceptions, exclude = super().getSuperProperties()
        exceptions |= {
            'Layout' : {
                'get':  { 'cb': lambda _: self._superLayout.layout().__class__ , 'type':'singleflag',
                    'flags': {
                        'TTkLayout'     : ttk.TTkLayout     ,
                        'TTkGridLayout' : ttk.TTkGridLayout ,
                        'TTkVBoxLayout' : ttk.TTkVBoxLayout ,
                        'TTkHBoxLayout' : ttk.TTkHBoxLayout } },
                'set':  { 'cb': lambda _,l: self.changeSuperLayout(l) , 'type':'singleflag',
                    'flags': {
                        'TTkLayout'     : ttk.TTkLayout     ,
                        'TTkGridLayout' : ttk.TTkGridLayout ,
                        'TTkVBoxLayout' : ttk.TTkVBoxLayout ,
                        'TTkHBoxLayout' : ttk.TTkHBoxLayout } },
            }
        }
        return additions, exceptions, exclude

    def dumpDict(self):
        ret = super().dumpDict()
        ret |= {
            'layout': self._superLayout.dumpDict()
        }
        return ret

    @staticmethod
    def _swFromWidget(wid, swClass, *args, **kwargs):
        sw = swClass(wid=wid, *args, **kwargs)
        sw.changeSuperLayout(type(wid.layout()))
        return sw

    def dropEvent(self, evt) -> bool:
        padt, padb, padl, padr = self._wid.getPadding()
        # evt = evt.copy()
        evt.x-=padl
        evt.y-=padt
        return self._superLayout.dropEvent(evt)

    def changeSuperLayout(self, layout):
        sl = self._superLayout
        self.layout().removeWidget(sl)
        if layout == ttk.TTkVBoxLayout:
            sl = so.SuperLayoutVBox(designer=self._designer, lay=self._wid.layout(), selectable=False)
        elif layout == ttk.TTkHBoxLayout:
            sl = so.SuperLayoutHBox(designer=self._designer, lay=self._wid.layout(), selectable=False)
        elif layout == ttk.TTkGridLayout:
            sl = so.SuperLayoutGrid(designer=self._designer, lay=self._wid.layout(), selectable=False)
        else:
            sl = so.SuperLayout(    designer=self._designer, lay=self._wid.layout(), selectable=False)
        self._superLayout = sl
        self._wid.setLayout(layout())
        self.layout().addWidget(sl)
        self._designer.weModified.emit()

    def updateAll(self):
        self.setPadding(*(self._wid.getPadding()))
        super().updateAll()

    def paintEvent(self, canvas):
        w,h = self.size()
        if so.SuperWidget._showLayout:
            t,b,l,r = self._wid.getPadding()
            for y in range(h):
                canvas.drawText(pos=(0,y),text='',width=w,color=self._layoutColor)
            for y in range(t,h-b):
                canvas.drawText(pos=(l,y),text='',width=w-r-l,color=self._layoutPadColor)
            # canvas.fill(color=self._layoutColor)
            # canvas.fill(pos=(l,t), size=(w-r-l,h-b-t), color=self._layoutPadColor)
        else:
            self._wid.getCanvas().updateSize()
            self._wid.paintEvent(self._wid.getCanvas())
            canvas.paintCanvas(
                    self._wid.getCanvas(),
                    (    0,     0, w, h), # geometry
                    (    0,     0, w, h), # slice
                    (    0,     0, w, h)) # bound