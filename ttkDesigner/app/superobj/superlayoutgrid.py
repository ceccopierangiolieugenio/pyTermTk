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

class _superExpandButton(ttk.TTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._direction = ttk.TTkK.TOP

    def setDirection(self, d):
        self._direction = d

    def _processInput(self, kevt, mevt):
        if not mevt:
            self.hide()
            return
        ax,ay = ttk.TTkHelper.absPos(self)
        w,h = self.size()
        mx,my = mevt.x, mevt.y
        if ( not (0 <= (mx-ax) < w) or
             not (0 <= (my-ay) < h) ) :
             self.hide()

    def show(self):
        ttk.TTkHelper._rootWidget._input.inputEvent.connect(self._processInput)
        return super().show()

    def hide(self):
        ttk.TTkHelper._rootWidget._input.inputEvent.disconnect(self._processInput)
        return super().hide()

    def paintEvent(self):
        canvas = self.getCanvas()
        # '▶','◀','▼','▲'
        w,h = self.size()
        if w==1:
            self.getCanvas().drawText(text='╽', pos=(0,0),     color=ttk.TTkColor.fg("FFFF00"))
            self.getCanvas().drawText(text='╿', pos=(0,h-1), color=ttk.TTkColor.fg("FFFF00"))
            for yy in range(1,h-1):
                self.getCanvas().drawText(text='┃', pos=(0, yy), color=ttk.TTkColor.fg("FFFF00"))
        elif h==1:
            txt = '╼'+'━'*(w-2)+'╾'
            self.getCanvas().drawText(text=txt, pos=(0,0), width=w, color=ttk.TTkColor.fg("FFFF00"))

        ch = {
            ttk.TTkK.TOP    : '▲',
            ttk.TTkK.BOTTOM : '▼',
            ttk.TTkK.LEFT   : '◀',
            ttk.TTkK.RIGHT  : '▶',
        }.get(self._direction, 'X')

        x,y = 0,0
        if w==1 and h>4:
            y = h//2-2
            h = 4
        elif h==1 and w>4:
            x = w//2-2
            w = 4
        canvas.fill(pos=(x,y), size=(w,h), char=ch, color=ttk.TTkColor.fg("#FF0000")+ttk.TTkColor.bg("#FFFF44"))

class SuperLayoutGrid(SuperLayout):
    def __init__(self, *args, **kwargs):
        kwargs['layout'] = ttk.TTkGridLayout()
        super().__init__(*args, **kwargs)
        self._expandButton = _superExpandButton()
        self.rootLayout().addWidget(self._expandButton)
        self._expandButton.hide()
        self._expandButton.clicked.connect(self._clickExpand)
        self._dragOver = None
        self._expandStuff = None
        self._orientation = ttk.TTkK.HORIZONTAL|ttk.TTkK.VERTICAL

    def dragEnterEvent(self, evt) -> bool:
        # ttk.TTkLog.debug(f"Enter")
        _, __, ___, self._dragOver = self._processDragOver(evt.x,evt.y)
        return True
    def dragLeaveEvent(self, evt) -> bool:
        # ttk.TTkLog.debug(f"Leave")
        self._dragOver = None
        self.update()
        return True
    def dragMoveEvent(self, evt) -> bool:
        # ttk.TTkLog.debug(f"Move")
        _, __, ___, self._dragOver = self._processDragOver(evt.x,evt.y)
        return True
    def dropEvent(self, evt) -> bool:
        self._dragOver = None
        self._pushRow, self._pushCol, self._direction, self._dragOver = self._processDragOver(evt.x,evt.y)
        return super().dropEvent(evt)

    # def mouseDragEvent(self, evt) -> bool:
    #     if ret := super().mouseDragEvent(evt):
    #         # removed unallocated rows/cols
    #         self.parentWidget().layout().repack()
    #     return ret

    def removeSuperWidget(self, sw):
        super().removeSuperWidget(sw)
        self.layout().repack()

    def mouseMoveEvent(self, evt) -> bool:
        # ttk.TTkLog.debug(f"Move {evt}")
        dir, wid = self._processMouseOver(evt.x, evt.y)
        if not wid or not dir:
            self._expandButton.hide()
            return super().mouseMoveEvent(evt)
        x,y,w,h = wid.geometry()
        ebs = {
            ttk.TTkK.TOP    : (x,     y,     w, 1),
            ttk.TTkK.BOTTOM : (x,     y+h-1, w, 1),
            ttk.TTkK.LEFT   : (x,     y,     1, h),
            ttk.TTkK.RIGHT  : (x+w-1, y,     1, h),
        }.get(dir, None)

        if not ebs:
            self._expandButton.hide()
        else:
            self._expandButton.setGeometry(*ebs)
            self._expandButton.setDirection(dir)
            self._expandButton.raiseWidget(raiseParent=False)
            self._expandButton.show()
        self._expandStuff = (dir,wid)
        return True

    def addSuperWidget(self, sw):
        self._dragOver = None
        if self._direction == ttk.TTkK.HORIZONTAL or self._orientation == ttk.TTkK.HORIZONTAL:
            self.layout().insertColumn(self._pushCol)
        elif self._direction == ttk.TTkK.VERTICAL or self._orientation == ttk.TTkK.VERTICAL:
            self.layout().insertRow(self._pushRow)
        self.layout().addWidget(sw, self._pushRow, self._pushCol,1,1)

    ttk.pyTTkSlot()
    def _clickExpand(self):
        if not self._expandButton.isVisible(): return
        self._expandButton.hide()
        dir, wid = self._expandStuff
        row = wid._row
        col = wid._col
        rowspan = wid._rowspan
        colspan = wid._colspan
        self.layout().removeItem(wid)
        if ttk.TTkK.TOP and row==0:
            self.layout().insertRow(0)
            row+=1
        elif ttk.TTkK.LEFT and col==0:
            self.layout().insertColumn(0)
            col+=1
        rc = {
            ttk.TTkK.TOP    : (row-1,col,  rowspan+1,colspan),
            ttk.TTkK.BOTTOM : (row,  col,  rowspan+1,colspan),
            ttk.TTkK.LEFT   : (row,  col-1,rowspan,colspan+1),
            ttk.TTkK.RIGHT  : (row,  col,  rowspan,colspan+1),
        }.get(dir, (row,col,rowspan,colspan))
        self.layout().addItem(wid,*rc)

    def _processMouseOver(self, x, y):
        # cehck the closest edge
        col, row, dir = 0,0,None
        wid = None

        if type(self.layout()) != ttk.TTkGridLayout:
            return dir,wid

        # Retrieve a list of widths,heights
        rows,cols = self.layout().gridSize()
        if not rows or not cols: return dir,wid

        horSizes, verSizes = self.layout().getSizes()

        # Find the row/col where the pointer is in
        for col,(a,b) in enumerate(horSizes):
            if a <= x < a+b: break
        for row,(a,b) in enumerate(verSizes):
            if a <= y < a+b: break

        ix, iw = horSizes[col]
        iy, ih = verSizes[row]

        wid = self.layout().itemAtPosition(row,col)
        if wid == None:
            return dir,wid

        col = wid._col
        row = wid._row
        rowspan = wid._rowspan
        colspan = wid._colspan

        maxw,maxh = wid.maximumSize()

        #

        #Top
        if (( y==iy ) and maxh>1 and
              not any([self.layout().itemAtPosition(row-1,col+cs) for cs in range(colspan)])):
            dir = ttk.TTkK.TOP
        #Bottom
        elif ((iy+ih==y+1) and maxh>1 and
              not any([self.layout().itemAtPosition(row+rowspan,col+cs) for cs in range(colspan)])):
            dir = ttk.TTkK.BOTTOM
        #Left
        elif ((x==ix) and maxw>1 and
              not any([self.layout().itemAtPosition(row+rs,col-1) for rs in range(rowspan)])):
            dir = ttk.TTkK.LEFT
        #Right
        elif ((ix+iw==x+1) and maxw>1 and
              not any([self.layout().itemAtPosition(row+rs,col+colspan) for rs in range(rowspan)])):
            dir = ttk.TTkK.RIGHT

        # ttk.TTkLog.debug(f"Move {dir} {wid}")

        # ttk.TTkLog.debug(f"{horSizes=}")
        # ttk.TTkLog.debug(f"{verSizes=}")
        # ttk.TTkLog.debug(f"{row=} {col=} {dir=} {self._dragOver=}")
        self.update()
        return dir, wid

    def _processDragOver(self, x, y):
        # cehck the closest edge
        col, row, dir = 0,0,None
        ret = None

        # Retrieve a list of widths,heights
        rows,cols = self.layout().gridSize()
        if not rows or not cols: return col,row,dir,ret

        horSizes, verSizes = self.layout().getSizes()

        # Find the row/col where the pointer is in
        for col,(a,b) in enumerate(horSizes):
            if a <= x < a+b: break
        for row,(a,b) in enumerate(verSizes):
            if a <= y < a+b: break

        ix, iw = horSizes[col]
        iy, ih = verSizes[row]

        if self.layout().itemAtPosition(row,col) == None:
            ret = (ix, iy, iw, ih)
        else:
            #Top
            if ((y==iy) and (self._orientation & ttk.TTkK.VERTICAL) and
                (  row==0 or
                 ( row>0 and self.layout().itemAtPosition(row,col) != self.layout().itemAtPosition(row-1,col)))):
                dir = ttk.TTkK.VERTICAL
                if row>0 and self.layout().itemAtPosition(row-1,col):
                    ret = (ix,    iy-1,    iw, 2)
                else:
                    ret = (ix,    iy,    iw, 1)
            #Bottom
            if ((iy+ih==y+1) and (self._orientation & ttk.TTkK.VERTICAL) and
                self.layout().itemAtPosition(row,col) != self.layout().itemAtPosition(row+1,col)):
                dir = ttk.TTkK.VERTICAL
                if row<rows-1 and self.layout().itemAtPosition(row+1,col):
                    ret = (ix,    iy+ih-1, iw, 2)
                else:
                    ret = (ix,    iy+ih-1, iw, 1)
            #Left
            if ((x==ix) and (self._orientation & ttk.TTkK.HORIZONTAL) and
                (  col==0 or
                 ( col>0 and self.layout().itemAtPosition(row,col) != self.layout().itemAtPosition(row,col-1)))):
                dir = ttk.TTkK.HORIZONTAL
                if col>0 and self.layout().itemAtPosition(row,col-1):
                    ret = (ix-1,  iy,    2, ih)
                else:
                    ret = (ix,    iy,    1, ih)
            #Right
            if ((ix+iw==x+1) and (self._orientation & ttk.TTkK.HORIZONTAL) and
                self.layout().itemAtPosition(row,col) != self.layout().itemAtPosition(row,col+1)):
                dir = ttk.TTkK.HORIZONTAL
                if col<cols-1 and self.layout().itemAtPosition(row,col+1):
                    ret = (ix+iw-1, iy,    2, ih)
                else:
                    ret = (ix+iw-1, iy,    1, ih)

            # If we are on the edge of the item push to the next spot
            if dir == ttk.TTkK.HORIZONTAL and ix+iw==x+1:
                col+=1
            if dir == ttk.TTkK.VERTICAL   and iy+ih==y+1:
                row+=1

        # ttk.TTkLog.debug(f"{horSizes=}")
        # ttk.TTkLog.debug(f"{verSizes=}")
        # ttk.TTkLog.debug(f"{row=} {col=} {dir=} {self._dragOver=}")
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
