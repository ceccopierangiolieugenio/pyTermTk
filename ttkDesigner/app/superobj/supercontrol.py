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
        self.getCanvas().setTransparent(True)

    def _alignWidToPos(self, pos):
        x,y = self.pos()
        ox,oy = pos
        wx,wy = self._wid.pos()
        self._wid.move(wx+x-ox, wy+y-oy)
        self.update()
        return super().move(x,y)

    def resizeEvent(self, w, h):
        super().resizeEvent(w, h)
        self._wid.resize(w-2,h-2)
        self._wid._canvas.updateSize()

    def mouseMoveEvent(self, evt) -> bool:
        return True

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

    def keyEvent(self, evt):
        if evt.type == ttk.TTkK.SpecialKey:
            if ( evt.key in (ttk.TTkK.Key_Delete, ttk.TTkK.Key_Backspace) and
                 not self._wid.isRootWidget() ):
                self._wid.parentWidget().removeSuperWidget(self._wid)
                self._wid.close()
                self.close()
                self._wid._designer.weModified.emit()
                return True
            bkPos = self.pos()
            x,y = 0,0
            if   evt.key == ttk.TTkK.Key_Up:    y=-1
            elif evt.key == ttk.TTkK.Key_Down:  y= 1
            elif evt.key == ttk.TTkK.Key_Left:  x=-1
            elif evt.key == ttk.TTkK.Key_Right: x= 1
            else: return super().keyEvent(evt)
            if any((x,y)):
                self.move(bkPos[0]+x, bkPos[1]+y)
                self._alignWidToPos(bkPos)
            return True
        return super().keyEvent(evt)

    def paintEvent(self, canvas):
        w,h = self.size()
        self._wid.paintEvent(canvas)
        self._wid.paintChildCanvas()
        canvas.paintCanvas(
                self._wid.getCanvas(),
                (    1,     1, w, h), # geometry
                (    0,     0, w, h), # slice
                (    0,     0, w, h)) # bound
        canvas.drawBox(pos=(0,0),size=self.size())
        canvas.drawChar(pos=(  0,   0), char='▛')
        canvas.drawChar(pos=(w-1,   0), char='▜')
        canvas.drawChar(pos=(  0, h-1), char='▙')
        canvas.drawChar(pos=(w-1, h-1), char='▟')
