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

class SuperControlWidget(ttk.TTkResizableFrame):
    def __init__(self, wid, *args, **kwargs):
        self._wid = wid
        self._widPos = self._wid.pos()
        self._draggable = False
        self._mouseDelta = (0,0)
        kwargs['maxSize'] = [v+2 for v in wid.maximumSize()]
        kwargs['minSize'] = [v+2 for v in wid.minimumSize()]
        kwargs['size']    = [v+2 for v in wid.size()       ]
        super().__init__(*args, **kwargs)

    def _alignWidToPos(self, pos):
        x,y = self.pos()
        ox,oy = pos
        wx,wy = self._wid.pos()
        self._wid.move(wx+x-ox, wy+y-oy)
        self.update()
        return super().move(x,y)

    def resizeEvent(self, w, h):
        self._wid.resize(w-2,h-2)
        self._wid._canvas.updateSize()
        return super().resizeEvent(w, h)

    def mouseReleaseEvent(self, evt) -> bool:
        self._draggable = False
        return super().mouseReleaseEvent(evt)

    def mousePressEvent(self, evt):
        self._draggable = False
        self._mouseDelta = (evt.x, evt.y)
        w,h = self.size()
        x,y = evt.x, evt.y
        if x==0 or x==w-1 or y==0 or y==h-1:
            return super().mousePressEvent(evt)
        self._draggable = True
        return True

    def mouseDragEvent(self, evt):
        bkPos = self.pos()
        if self._draggable:
            x,y = self.pos()
            dx = evt.x-self._mouseDelta[0]
            dy = evt.y-self._mouseDelta[1]
            self.move(x+dx, y+dy)
            self._alignWidToPos(bkPos)
            return True
        ret = super().mouseDragEvent(evt)
        self._alignWidToPos(bkPos)
        return ret

    def paintEvent(self):
        w,h = self.size()
        self._wid.paintEvent()
        self._canvas.paintCanvas(
                self._wid.getCanvas(),
                (    1,     1, w, h), # geometry
                (    0,     0, w, h), # slice
                (    0,     0, w, h)) # bound
        self._canvas.drawBox(pos=(0,0),size=self.size())
        self._canvas.drawChar(pos=(  0,   0), char='▛')
        self._canvas.drawChar(pos=(w-1,   0), char='▜')
        self._canvas.drawChar(pos=(  0, h-1), char='▙')
        self._canvas.drawChar(pos=(w-1, h-1), char='▟')

class SuperWidget(ttk.TTkWidget):
    def __init__(self, wid, *args, **kwargs):
        self._wid = wid
        self._wid.move(*kwargs['pos'])
        self._wid._canvas.show()
        kwargs['maxSize'] = wid.maximumSize()
        kwargs['minSize'] = wid.minimumSize()
        kwargs['size']    = wid.size()
        super().__init__(*args, **kwargs)
        #self.resize(*self._wid.size())

    def updateAll(self):
        self.update()

    def dropEvent(self, evt) -> bool:
        data = evt.data()
        ttk.TTkLog.debug(f"Drop ({data.__class__.__name__}) -> pos={evt.pos()}")
        if issubclass(type(data),ttk.TTkWidget):
            self.layout().addWidget(sw := SuperWidget(wid=data, pos=(evt.x, evt.y)))
            sw.weModified = self.weModified
            sw.widgetSelected = self.widgetSelected
            self.update()
            self.weModified.emit()
            return True
        return False

    def move(self, x: int, y: int):
        self._wid.move(x,y)
        self.update()
        return super().move(x, y)

    def resizeEvent(self, w, h):
        self._wid.resize(w,h)
        self._wid._canvas.updateSize()
        return super().resizeEvent(w, h)

    def mousePressEvent(self, evt):
        scw = SuperControlWidget(self)
        ttk.TTkHelper.removeOverlay()
        ttk.TTkHelper.overlay(self, scw, -1,-1, forceBoundaries=False)
        self.widgetSelected.emit(self._wid,self)
        return True

    def paintEvent(self):
        w,h = self.size()
        self._wid.paintEvent()
        self._canvas.paintCanvas(
                self._wid.getCanvas(),
                (    0,     0, w, h), # geometry
                (    0,     0, w, h), # slice
                (    0,     0, w, h)) # bound

class WindowEditorView(ttk.TTkAbstractScrollView):
    def __init__(self, *args, **kwargs):
        self.weModified = ttk.pyTTkSignal()
        self.widgetSelected = ttk.pyTTkSignal(ttk.TTkWidget, ttk.TTkWidget)
        super().__init__(*args, **kwargs)
        self.viewChanged.connect(self._viewChangedHandler)

    def dropEvent(self, evt) -> bool:
        data = evt.data()
        ttk.TTkLog.debug(f"Drop ({data.__class__.__name__}) -> pos={evt.pos()}")
        if issubclass(type(data),ttk.TTkWidget):
            self.layout().addWidget(sw := SuperWidget(wid=data, pos=(evt.x, evt.y)))
            sw.weModified = self.weModified
            sw.widgetSelected = self.widgetSelected
            self.update()
            self.weModified.emit()
            self.viewChanged.emit()
            return True
        return False

    @ttk.pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def viewFullAreaSize(self):
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w+1, h+1

    def viewDisplayedSize(self):
        return self.size()

    # def paintEvent(self):
    #     _,_,w,h = self.layout().fullWidgetAreaGeometry()
    #     self._canvas.drawBox(pos=(0,0),size=(w,h))

class WindowEditor(ttk.TTkAbstractScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setViewport(WindowEditorView())

