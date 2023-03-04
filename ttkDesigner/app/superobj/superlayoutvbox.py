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
from .superlayout import SuperLayout

class SuperLayoutVBox(SuperLayout):
    def __init__(self, *args, **kwargs):
        kwargs['layout'] = ttk.TTkVBoxLayout()
        super().__init__(*args, **kwargs)
        self._dragOver = None

    def dragEnterEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Enter")
        _, self._dragOver = self._processDragOver(evt.x,evt.y)
        return True
    def dragLeaveEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Leave")
        self._dragOver = None
        return True
    def dragMoveEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Move")
        _, self._dragOver = self._processDragOver(evt.x,evt.y)
        return True
    def dropEvent(self, evt) -> bool:
        self._dragOver = None
        self._pushRow,_ = self._processDragOver(evt.x,evt.y)
        return super().dropEvent(evt)

    def addSuperWidget(self, sw):
        row = self._pushRow
        afterWidgets = sorted(
                [ c for c in self.layout().children() if c._row >= row ],
                key=lambda x: x._row)
        self.layout().removeItems(afterWidgets)
        afterWidgets.insert(0,sw.widgetItem())
        self.layout().addItems(afterWidgets)

    def _processDragOver(self, x, y):
        # cehck the closest edge
        row = 0
        ret = None
        w,h = self.size()
        for c in self.layout().children():
            cx,cy,cw,ch = c.geometry()
            if cy==y:
                row = c._row
                ret = (max(0,y-1),y)
                break
            if cy+ch-1 == y:
                row = c._row+1
                ret = (y,min(y+1,h-1))
                break
        ttk.TTkLog.debug(f"{row=} {self._dragOver=}")
        self.update()
        return row, ret

    # Stupid hack to paint on top of the child widgets
    def paintChildCanvas(self):
        super().paintChildCanvas()
        if self._dragOver is not None:
            a,b = self._dragOver
            w = self.width()
            if a==b:
                txt = '╼'+'━'*(w-2)+'╾'
                self.getCanvas().drawText(text=txt, pos=(0,a), width=w, color=ttk.TTkColor.fg("FFFF00"))
            else:
                txt = '┍'+'━'*(w-2)+'┑'
                self.getCanvas().drawText(text=txt, pos=(0,a), width=w, color=ttk.TTkColor.fg("FFFF00"))
                txt = '┕'+'━'*(w-2)+'┙'
                self.getCanvas().drawText(text=txt, pos=(0,b), width=w, color=ttk.TTkColor.fg("FFFF00"))

