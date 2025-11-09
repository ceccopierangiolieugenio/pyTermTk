#!/usr/bin/env python3

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

import sys, os, math
from dataclasses import dataclass

sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))
import TermTk as ttk

@dataclass
class BreakOutParams():
    colors = {
        'lines': [
            ttk.TTkColor.fg("#FF0000"),
            ttk.TTkColor.fg("#FF0000"),
            ttk.TTkColor.fg("#FF8800"),
            ttk.TTkColor.fg("#FF8800"),
            ttk.TTkColor.fg("#00FF00"),
            ttk.TTkColor.fg("#00FF00"),
            ttk.TTkColor.fg("#FFFF00"),
            ttk.TTkColor.fg("#FFFF00")],
        'bar'  : ttk.TTkColor.fg("#0088FF"),
    }
    delay: float = 0.05
    lineBlocks: int = 14
    blocksOffset: int = 5
    size: tuple([int,int]) = (lineBlocks*8-1, blocksOffset+8+17)
    # The ball use a float
    # It ijs rasterized in the paint
    ballPos = [[20,blocksOffset+10],[math.sin(math.pi/4),math.cos(math.pi/4)]]
    barSize: int = 20
    barPos: int = (size[0]-barSize)//2

class BreakOutDisplay(ttk.TTkWidget):
    _params = BreakOutParams()
    _blocks = []

    def __init__(self, **kwargs):
        size = self._params.size
        self._initBlocks()
        super().__init__(**kwargs|{"size":size,"minSize":size,"maxSize":size})
        self._timer = ttk.TTkTimer()
        self._timer.timeout.connect(self._timerEvent)
        self._timer.start(self._params.delay)

    def _initBlocks(self):
        self._blocks = [
            [True for _ in range(self._params.lineBlocks)]
                for _ in range(8)]

    @ttk.pyTTkSlot()
    def _timerEvent(self):
        w,h = self._params.size
        [posx,posy],[vx,vy] = self._params.ballPos
        newposx=posx+vx
        newposy=posy+vy
        lineBlocks = self._params.lineBlocks
        blocksOffset = self._params.blocksOffset
        barPos  = self._params.barPos
        barSize = self._params.barSize

        # Check if the border is hit:
        if newposx >= w:   vx=-abs(vx)
        elif newposx <= 0: vx= abs(vx)
        if newposy >= h:   vy=-abs(vy)
        elif newposy <= 0: vy= abs(vy)

        # Check if a block is hit:
        # get the block
        bx, by = int(newposx)//8, int(newposy)-blocksOffset
        if 0 <= by < 8:
            if 0 <= bx < lineBlocks:
                if self._blocks[by][bx]:
                    self._blocks[by][bx] = False
                    # check if coming from down:
                    if vy < 0 and by==7 or (by<7 and not self._blocks[by+1][bx]):
                        vy=abs(vy)
                    # check if coming from up:
                    elif vy > 0 and by==0 or (by>0 and not self._blocks[by-1][bx]):
                        vy=-abs(vy)
                    # check if coming from left:
                    elif vx > 0 and bx==0 or (bx>0 and not self._blocks[by][bx-1]):
                        vx=-abs(vx)
                    else:
                        vx= abs(vx)

        # Check if the bar is hit:
        if newposy >= h-1:
            if barPos < newposx < barPos+barSize:
                poff = newposx-barPos
                prel = poff-barSize/2
                delta = prel/barSize
                vx =  math.sin(math.pi*delta)
                vy = -math.cos(math.pi*delta)
                # Force a cap on the vertical speed
                vy = min(-1,vy)

        posx=posx+vx
        posy=posy+vy

        self._params.ballPos = [[posx,posy],[vx,vy]]
        self._timer.start(self._params.delay)
        self.update()


    def mouseMoveEvent(self, evt) -> bool:
        w = self._params.size[0]
        barsize = self._params.barSize
        self._params.barPos = min(max(0,evt.x-barsize//2),w-barsize)
        self.update()

    def paintEvent(self, canvas: ttk.TTkCanvas):
        colors = self._params.colors
        w,h = self._params.size
        lineBlocks = self._params.lineBlocks
        blocksOffset = self._params.blocksOffset
        barPos = self._params.barPos
        barSize = self._params.barSize
        posx,posy = self._params.ballPos[0]
        posx = int(posx)
        posy = int(posy)

        for by in range(8):
            for bx in range(lineBlocks):
                if self._blocks[by][bx]:
                    canvas.drawText(pos=(bx*8,by+blocksOffset),
                        text='▇'*7,
                        color=colors['lines'][by])

        canvas.drawText(
            pos=(barPos,h-1),
            text='▛'+'▀'*(barSize-2)+'▜',
            color=colors['bar'])

        ball = ['▘','▝',
                '▖','▗'][(posx%2)+2*(posy%2)]

        canvas.drawText(
            pos=(posx,posy),
            text=ball)
root = ttk.TTk(title="breakout Demo", layout=ttk.TTkGridLayout())

frame = ttk.TTkFrame(layout=ttk.TTkGridLayout(), title="BreakOuTTk")
breakout = BreakOutDisplay(parent=frame)

root.layout().addWidget(frame,1,1)
root.layout().addItem(ttk.TTkLayout(),0,0)
root.layout().addItem(ttk.TTkLayout(),2,0)
root.layout().addItem(ttk.TTkLayout(),0,2)
root.layout().addItem(ttk.TTkLayout(),2,2)

root.mainloop()
