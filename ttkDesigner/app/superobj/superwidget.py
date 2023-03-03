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

class SuperWidget(ttk.TTkWidget):
    def __init__(self, wid, weModified, thingSelected, *args, **kwargs):
        self.weModified = weModified
        self.thingSelected = thingSelected
        self._wid = wid
        self._wid.move(*kwargs['pos'])
        self._wid._canvas.show()
        self._superLayout = so.SuperLayout(lay=ttk.TTkLayout(), weModified=self.weModified, thingSelected=self.thingSelected,)
        self._superRootWidget = kwargs.get('superRootWidget',False)
        kwargs['layout'] = ttk.TTkGridLayout()
        kwargs['layout'].addWidget(self._superLayout)
        kwargs['maxSize'] = wid.maximumSize()
        kwargs['minSize'] = wid.minimumSize()
        kwargs['size']    = wid.size()
        padt, padb, padl, padr = wid.getPadding()
        kwargs['paddingTop'] = padt
        kwargs['paddingBottom'] = padb
        kwargs['paddingLeft'] = padl
        kwargs['paddingRight'] = padr
        super().__init__(*args, **kwargs)
        #self.resize(*self._wid.size())
        h,s,l = randint(0,359),100,randint(60,80)
        r,g,b = ttk.TTkColor.hsl2rgb(((h+5)%360,s,l))
        self._layoutColor    = ttk.TTkColor.bg(f"#{r:02X}{g:02X}{b:02X}", modifier=ttk.TTkColorGradient(increment=+2))
        r,g,b = ttk.TTkColor.hsl2rgb(((h+5)%360,s,l))
        self._layoutPadColor = ttk.TTkColor.bg(f"#{r:02X}{g:02X}{b:02X}", modifier=ttk.TTkColorGradient(increment=-2))
        self.setFocusPolicy(ttk.TTkK.ClickFocus)
        SuperWidget.toggleHighlightLayout.connect(self._toggleHighlightLayout)

    _showLayout = False
    toggleHighlightLayout = ttk.pyTTkSignal(bool)

    @ttk.pyTTkSlot(bool)
    def _toggleHighlightLayout(self, state):
        SuperWidget._showLayout = state
        self.update()

    def dumpDict(self):
        wid = self._wid
        ret = {
            'class'  : wid.__class__.__name__,
            'params' : SuperObject.dumpParams(wid),
            'layout': self._superLayout.dumpDict()
        }
        return ret

    def updateAll(self):
        self.resize(*(self._wid.size()))
        self.move(*(self._wid.pos()))
        self.setPadding(*(self._wid.getPadding()))
        self.setMaximumSize(*(self._wid.maximumSize()))
        self.setMinimumSize(*(self._wid.minimumSize()))
        self.update()

    def mousePressEvent(self, evt) -> bool:
        return True

    def pushSuperControlWidget(self):
        if self._superRootWidget: return False
        scw = so.SuperControlWidget(self)
        ttk.TTkHelper.removeOverlay()
        ttk.TTkHelper.overlay(self, scw, -1,-1, forceBoundaries=False)

    def mouseReleaseEvent(self, evt) -> bool:
        self.pushSuperControlWidget()
        self.thingSelected.emit(self._wid,self)
        return True

    def mouseDragEvent(self, evt) -> bool:
        if self._superRootWidget: return False
        drag = ttk.TTkDrag()
        data = self
        data.paintChildCanvas()
        drag.setHotSpot(evt.x, evt.y)
        drag.setPixmap(data.getCanvas())
        drag.setData(data)
        drag.exec()
        self.parentWidget()._lay.removeWidget(self._wid)
        self.parentWidget().layout().removeWidget(self)
        self.parentWidget().layout().update()
        self.parentWidget().update()
        return True

    def dropEvent(self, evt) -> bool:
        padt, padb, padl, padr = self._wid.getPadding()
        # evt = evt.copy()
        evt.x-=padl
        evt.y-=padt
        return self._superLayout.dropEvent(evt)

    def move(self, x: int, y: int):
        self._wid.move(x,y)
        self.update()
        return super().move(x, y)

    def resizeEvent(self, w, h):
        self._wid.resize(w,h)
        self._wid._canvas.updateSize()
        return super().resizeEvent(w, h)

    def paintEvent(self):
        w,h = self.size()
        if SuperWidget._showLayout:
            t,b,l,r = self._wid.getPadding()
            for y in range(h):
                self._canvas.drawText(pos=(0,y),text='',width=w,color=self._layoutColor)
            for y in range(t,h-b):
                self._canvas.drawText(pos=(l,y),text='',width=w-r-l,color=self._layoutPadColor)
            # self._canvas.fill(color=self._layoutColor)
            # self._canvas.fill(pos=(l,t), size=(w-r-l,h-b-t), color=self._layoutPadColor)
        else:
            self._wid.getCanvas().updateSize()
            self._wid.paintEvent()
            self._canvas.paintCanvas(
                    self._wid.getCanvas(),
                    (    0,     0, w, h), # geometry
                    (    0,     0, w, h), # slice
                    (    0,     0, w, h)) # bound