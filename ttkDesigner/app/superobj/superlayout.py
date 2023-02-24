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

class SuperLayout(ttk.TTkWidget):
    def __init__(self, lay, weModified, widgetSelected, *args, **kwargs):
        self.weModified = weModified
        self.widgetSelected = widgetSelected
        self._lay = lay
        self._superRootWidget = kwargs.get('superRootWidget',False)
        self._selectable = kwargs.get('selectable', False)

        # kwargs['pos']  = (x,y) = lay.pos()
        x,y = kwargs.get('pos',lay.pos())
        kwargs['size'] = (w,h) = lay.size()
        self._lay.setGeometry(x,y,w,h)

        super().__init__(*args, **kwargs)

        self.getCanvas().setTransparent(True)
        # r,g,b = randint(0,0xFF),randint(0,0xFF),randint(0,0xFF)
        # self._layoutColor    = ttk.TTkColor.bg(f"#{r:02X}{g:02X}{b:02X}")
        self.setFocusPolicy(ttk.TTkK.ClickFocus)
        so.SuperWidget.toggleHighlightLayout.connect(self._toggleHighlightLayout)

    @ttk.pyTTkSlot(bool)
    def _toggleHighlightLayout(self, state):
        so.SuperWidget._showLayout = state
        self.update()

    def dumpDict(self):
        ret = {}
        return ret

    def updateAll(self):
        self.resize(*(self._lay.size()))
        self.move(*(self._lay.pos()))
        # self.setPadding(*(self._lay.getPadding()))
        self.setMaximumSize(*(self._lay.maximumSize()))
        self.setMinimumSize(*(self._lay.minimumSize()))
        self.update()

    def mousePressEvent(self, evt) -> bool:
        return self._selectable and not self._superRootWidget

    def pushSuperControlWidget(self):
        if self._superRootWidget or not self._selectable: return False
        scw = so.SuperControlWidget(self)
        ttk.TTkHelper.removeOverlay()
        ttk.TTkHelper.overlay(self, scw, -1,-1, forceBoundaries=False)

    def mouseReleaseEvent(self, evt) -> bool:
        if self._superRootWidget or not self._selectable: return False
        self.pushSuperControlWidget()
        # self.widgetSelected.emit(self._lay,self)
        return True

    def mouseDragEvent(self, evt) -> bool:
        if self._superRootWidget or not self._selectable: return False
        drag = ttk.TTkDrag()
        data = self
        canvas = self.getCanvas()
        canvas.clean()
        ttk.TTkWidget._paintChildCanvas(canvas, self._lay, self._lay.geometry(), self._lay.offset())
        drag.setHotSpot(evt.x, evt.y)
        drag.setPixmap(canvas)
        drag.setData(data)
        drag.exec()
        self.parentWidget().layout().removeWidget(self)
        self.parentWidget().update()
        return True

    def dropEvent(self, evt) -> bool:
        data = evt.data()
        hsx,hsy = evt.hotSpot()
        ttk.TTkLog.debug(f"Drop ({data.__class__.__name__}) -> pos={evt.pos()}")
        if issubclass(type(data),ttk.TTkLayout):
            self.layout().addWidget(sw := so.SuperLayout(lay=data, weModified=self.weModified, widgetSelected=self.widgetSelected, pos=(evt.x-hsx, evt.y-hsy), selectable=True))
            self._lay.addItem(data)
        elif issubclass(type(data), so.SuperLayout):
            sw = data
            self.layout().addWidget(sw)
            data = data._lay
            self._lay.addItem(data)
            sw.show()
            sw.move(evt.x-hsx, evt.y-hsy)
        elif issubclass(type(data), so.SuperWidget):
            sw = data
            self.layout().addWidget(sw)
            data = data._wid
            sw.move(evt.x-hsx, evt.y-hsy)
            sw.show()
            self._lay.addWidget(data)
            data.move(evt.x-hsx, evt.y-hsy)
        elif issubclass(type(data),ttk.TTkWidget):
            self.layout().addWidget(sw := so.SuperWidget(wid=data, weModified=self.weModified, widgetSelected=self.widgetSelected, pos=(evt.x-hsx, evt.y-hsy)))
            self._lay.addWidget(data)
            data.move(evt.x-hsx, evt.y-hsy)
        else:
            return False
        self.update()
        self.weModified.emit()
        return True

    def move(self, x: int, y: int):
        w,h = self._lay.size()
        self._lay.setGeometry(x,y,w,h)
        # self.update()
        return super().move(x, y)

    def resizeEvent(self, w, h):
        x,y = self._lay.pos()
        self._lay.setGeometry(x,y,w,h)
        return super().resizeEvent(w, h)

    def paintEvent(self):
        if self._selectable:
            if so.SuperWidget._showLayout:
                w,h = self.size()
                self._canvas.drawBox(pos=(0,0),size=(w,h), color=ttk.TTkColor.fg('#88DD88', modifier=ttk.TTkColorGradient(increment=+1)))
            else:
                w,h = self.size()
                self._canvas.drawBox(pos=(0,0),size=(w,h), color=ttk.TTkColor.fg('#223322', modifier=ttk.TTkColorGradient(increment=+1)))
