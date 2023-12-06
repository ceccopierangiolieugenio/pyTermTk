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

__all__ = ['BreakOutDisplay']

import sys, os, math

sys.path.append(os.path.join(sys.path[0],'../../..'))
import TermTk as ttk

from .boparams import BreakOutParams

class BreakOutDisplay(ttk.TTkWidget):
    __slots__ = ('_params','_blocks','_ballPos','_barPos')
    def __init__(self, **kwargs):
        self._params = BreakOutParams()
        self._blocks = []
        self._initBlocks()
        size = (self._params.wallCols*self._params.brickSize-1,
                self._params.blocksOffset+self._params.wallRows+17)
        super().__init__(**kwargs|{"size":size,"minSize":size,"maxSize":size})
        self._timer = ttk.TTkTimer()
        self._timer.timeout.connect(self._timerEvent)

    def setParams(self, params:BreakOutParams):
        self._params = params
        self._blocks = []
        self._initBlocks()
        size = (self._params.wallCols*self._params.brickSize-1,
                self._params.blocksOffset+self._params.wallRows+17)
        self.resize(*size)
        self.setMaximumSize(*size)
        self.setMinimumSize(*size)
        self.update()
        # Little hack to autoresize the frame
        self.parentWidget().update(updateParent=True,updateLayout=True)

    def _initBlocks(self):
        self._ballPos = [[20,self._params.blocksOffset+10],[math.sin(math.pi/4),math.cos(math.pi/4)]]
        self._barPos: int = (self._params.wallCols*self._params.brickSize-1-self._params.barSize)//2
        self._blocks = [
            [True for _ in range(self._params.wallCols)]
                for _ in range(self._params.wallRows)]

    @ttk.pyTTkSlot()
    def play(self):
        w,h = self.size()
        self._params.ballPos =[
            [20,((self._params.blocksOffset+self._params.wallRows)*3+h)//4],
            [math.sin(math.pi/4),math.cos(math.pi/4)]]
        self._initBlocks()
        self._timer.start(self._params.delay)

    @ttk.pyTTkSlot()
    def _timerEvent(self):
        w,h = self.size()
        [posx,posy],[vx,vy] = self._ballPos
        newposx=posx+vx
        newposy=posy+vy
        wallCols = self._params.wallCols
        wallRows = self._params.wallRows
        brickSize = self._params.brickSize
        blocksOffset = self._params.blocksOffset
        barPos  = self._barPos
        barSize = self._params.barSize

        # Check if the border is hit:
        if newposx >= w:   vx=-abs(vx)
        elif newposx <= 0: vx= abs(vx)
        if newposy >= h:   return
        elif newposy <= 0: vy= abs(vy)

        # Check if a block is hit:
        # get the block
        bx, by = int(newposx)//brickSize, int(newposy)-blocksOffset
        if 0 <= by < wallRows:
            if 0 <= bx < wallCols:
                if self._blocks[by][bx]:
                    self._blocks[by][bx] = False
                    # check if coming from down:
                    if vy < 0 and by==wallRows-1 or (by<wallRows-1 and not self._blocks[by+1][bx]):
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

        self._ballPos = [[posx,posy],[vx,vy]]
        self._timer.start(self._params.delay)
        self.update()

    def mouseMoveEvent(self, evt) -> bool:
        w,_ = self.size()
        barsize = self._params.barSize
        self._barPos = min(max(0,evt.x-barsize//2),w-barsize)
        self.update()

    def paintEvent(self, canvas: ttk.TTkCanvas):
        colors = self._params.colors
        w,h = self.size()
        wallCols = self._params.wallCols
        blocksOffset = self._params.blocksOffset
        barPos = self._barPos
        barSize = self._params.barSize
        posx,posy = self._ballPos[0]
        posx = int(posx)
        posy = int(posy)

        colors = self._params.colors['lines']
        numColors    = len(colors)

        wallRows     = self._params.wallRows
        wallCols     = self._params.wallCols
        bricksize    = self._params.brickSize
        blocksOffset = self._params.blocksOffset

        for by in range(wallRows):
            for bx in range(wallCols):
                if self._blocks[by][bx]:
                    canvas.drawText(pos=(bx*bricksize,by+blocksOffset),
                        text='_'*(bricksize-1),
                        color=colors[by*numColors//wallRows])

        canvas.drawText(
            pos=(barPos,h-1),
            text='▛'+'▀'*(barSize-2)+'▜',
            color=self._params.colors['bar'])

        ball = ['▘','▝',
                '▖','▗'][(posx%2)+2*(posy%2)]

        canvas.drawText(
            pos=(posx,posy),
            text=ball)