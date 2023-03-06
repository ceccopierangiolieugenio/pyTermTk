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

class SuperLayoutGrid(SuperLayout):
    def __init__(self, *args, **kwargs):
        kwargs['layout'] = ttk.TTkGridLayout()
        super().__init__(*args, **kwargs)
        self._dragOver = None
        self._orientation = ttk.TTkK.HORIZONTAL|ttk.TTkK.VERTICAL

    def dragEnterEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Enter")
        _, __, ___, self._dragOver = self._processDragOver(evt.x,evt.y)
        return True
    def dragLeaveEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Leave")
        self._dragOver = None
        return True
    def dragMoveEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Move")
        _, __, ___, self._dragOver = self._processDragOver(evt.x,evt.y)
        return True
    def dropEvent(self, evt) -> bool:
        self._dragOver = None
        self._pushRow, self._pushCol, self._direction, self._dragOver = self._processDragOver(evt.x,evt.y)
        return super().dropEvent(evt)

    def addSuperWidget(self, sw):
        self._dragOver = None
        if self._direction == ttk.TTkK.HORIZONTAL:
            self.layout().insertColumn(self._pushCol)
        elif self._direction == ttk.TTkK.VERTICAL:
            self.layout().insertRow(self._pushRow)
        self.layout().addWidget(sw, self._pushRow, self._pushCol)

    def _processDragOver(self, x, y):
        # cehck the closest edge
        col, row, dir = 0,0,None
        ret = None
        w,h = self.size()
        dist = w+h
        # Retrieve a list of widths,heights
        hSizes = []
        vSizes = []
        cmw = self.layout().columnMinWidth()
        rmh = self.layout().rowMinHeight()
        gridItems = self.layout().gridItems()
        if not gridItems or not gridItems[0]: return col,row,dir,ret
        for r,rows in enumerate(gridItems):
            hh = rmh
            hSizes += [cmw]*(len(rows)-len(hSizes))
            for c,item in enumerate(rows):
                if not item: continue
                ix,iy,iw,ih = item.geometry()
                hh = max(hh,ih)
                hSizes[c] = max(hSizes[c],iw)
            vSizes.append(hh)

        # Get the position of any split col
        hPos = [(sum(hSizes[:i]),sum(hSizes[:i+1])) for i in range(len(hSizes))]
        vPos = [(sum(vSizes[:i]),sum(vSizes[:i+1])) for i in range(len(vSizes))]

        # Find the row/col where the pointer is in
        ttk.TTkLog.debug(hPos)
        ttk.TTkLog.debug(vPos)
        for col,(a,b) in enumerate(hPos):
            if a <= x < b:
                ttk.TTkLog.debug(f"{col=} {x=} in {(a,b)=}")
                break
        for row,(a,b) in enumerate(vPos):
            if a <= y < b:
                ttk.TTkLog.debug(f"{row=} {y=} in {(a,b)=}")
                break

        ix,ixb = hPos[col]
        iy,iyb = vPos[row]
        iw = hSizes[col]
        ih = vSizes[row]

        if gridItems[row][col] == None:
            ret = (ix, iy, iw, ih)
        else:
            #Top
            if dd := y-iy <= dist and (self._orientation & ttk.TTkK.VERTICAL):
                dist = dd
                dir = ttk.TTkK.VERTICAL
                ret = (ix,    iy,    iw, 1)
            #Bottom
            if dd := iyb-y <= dist and (self._orientation & ttk.TTkK.VERTICAL):
                dist = dd
                dir = ttk.TTkK.VERTICAL
                ret = (ix,    iyb-1, iw, 1)
            #Left
            if dd := x-ix <= dist and (self._orientation & ttk.TTkK.HORIZONTAL):
                dist = dd
                dir = ttk.TTkK.HORIZONTAL
                ret = (ix,    iy,    1, ih)
            #Right
            if dd := ixb-x <= dist and (self._orientation & ttk.TTkK.HORIZONTAL):
                dist = dd
                dir = ttk.TTkK.HORIZONTAL
                ret = (ixb-1, iy,    1, ih)

            # If we are on the edge of the item push to the next spot
            if dir == ttk.TTkK.HORIZONTAL and ixb-x == dist:
                col+=1
            if dir == ttk.TTkK.VERTICAL   and iyb-y == dist:
                row+=1

        ttk.TTkLog.debug(f"{row=} {self._dragOver=}")
        self.update()
        return row, col, dir, ret

    # Stupid hack to paint on top of the child widgets
    def paintChildCanvas(self):
        super().paintChildCanvas()
        if self._dragOver is not None:
            x,y,w,h = self._dragOver
            if h==1 and w==1:
                self.getCanvas().drawText(text='◉', pos=(x,y), color=ttk.TTkColor.fg("FFFF00"))
            elif w==1:
                self.getCanvas().drawText(text='╽', pos=(x,y),     color=ttk.TTkColor.fg("FFFF00"))
                self.getCanvas().drawText(text='╿', pos=(x,y+h-1), color=ttk.TTkColor.fg("FFFF00"))
                for yy in range(y+1,y+h-1):
                    self.getCanvas().drawText(text='┃', pos=(x, yy), color=ttk.TTkColor.fg("FFFF00"))
            elif h==1:
                txt = '╼'+'━'*(w-2)+'╾'
                self.getCanvas().drawText(text=txt, pos=(x,y), width=w, color=ttk.TTkColor.fg("FFFF00"))
            else:
                self.getCanvas().drawBox(pos=(x,y), size=(w,h), color=ttk.TTkColor.fg("FFFF00"))
