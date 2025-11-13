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

import sys, os
from random import randint

sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))
import TermTk as ttk

from bolib import *

class WinParams(ttk.TTkWindow):
    __slots__ = ('_breakout')
    def __init__(self, breakout:BreakOutDisplay, **kwargs):
        self._breakout = breakout
        super().__init__(**kwargs|{'layout':ttk.TTkGridLayout()})
        layout = self.layout()
        self._rows    = ttk.TTkSpinBox(value=8,  minimum=5, maximum=15)
        self._cols    = ttk.TTkSpinBox(value=14, minimum=5, maximum=20)
        self._offset  = ttk.TTkSpinBox(value=5,  minimum=3, maximum=10)
        self._barsize = ttk.TTkSpinBox(value=20,  minimum=5, maximum=30)
        self._brickSize = ttk.TTkSpinBox(value=8, minimum=4, maximum=12)

        self._rows.valueChanged.connect(self.reParams)
        self._cols.valueChanged.connect(self.reParams)
        self._offset.valueChanged.connect(self.reParams)
        self._barsize.valueChanged.connect(self.reParams)
        self._brickSize.valueChanged.connect(self.reParams)

        layout.addWidget(ttk.TTkLabel(text="Rows"),_r:=0,0)
        layout.addWidget(self._rows,_r,1)
        layout.addWidget(ttk.TTkLabel(text="Cols"),_r:=_r+1,0)
        layout.addWidget(self._cols,_r,1)
        layout.addWidget(ttk.TTkLabel(text="Brick"),_r:=_r+1,0)
        layout.addWidget(self._brickSize,_r,1)
        layout.addWidget(ttk.TTkLabel(text="Offset"),_r:=_r+1,0)
        layout.addWidget(self._offset,_r,1)
        layout.addWidget(ttk.TTkLabel(text="Bar Size"),_r:=_r+1,0)
        layout.addWidget(self._barsize,_r,1)
        numLines = len(BreakOutParams.colors['lines'])

        self._colors = []
        for i in range(numLines):
            layout.addWidget(ttk.TTkLabel(text=f"Line{i}"),_r:=_r+1,0)
            layout.addWidget(_color := ttk.TTkColorButtonPicker(color=BreakOutParams.colors['lines'][i]),_r,1)
            _color.colorSelected.connect(self.reParams)
            self._colors.append(_color)

        layout.addWidget(_btn_shuffle := ttk.TTkButton(text='Shuffle',border=True),_r:=_r+1,0,1,2)
        layout.addWidget(_btn_play    := ttk.TTkButton(text='PLAY',border=True),_r:=_r+1,0,1,2)

        _btn_shuffle.clicked.connect(self.shuffle)
        _btn_play.clicked.connect(self._breakout.play)

    @ttk.pyTTkSlot()
    def shuffle(self):
        for _color  in self._colors:
            h,s,l = randint(0,359),100,randint(60,80)
            r,g,b = ttk.TTkColor.hsl2rgb(((h+5)%360,s,l))
            _color.setColor(ttk.TTkColor.fg("#000000")+ttk.TTkColor.bg(f"#{r:02X}{g:02X}{b:02X}"))
        self._rows.setValue(     randint(5,15))
        self._cols.setValue(     randint(5,20))
        self._barsize.setValue(  randint(5,30))
        self._brickSize.setValue(randint(3,10))
        self._offset.setValue(   randint(4,12))
        self.reParams()

    @ttk.pyTTkSlot()
    def reParams(self):
        newParams = BreakOutParams()
        newParams.colors['lines'] = [ttk.TTkColor.fg("#000000")+_color.color() for _color in self._colors]
        newParams.wallRows = self._rows.value()
        newParams.wallCols = self._cols.value()
        newParams.barSize  = self._barsize.value()
        newParams.brickSize = self._brickSize.value()
        newParams.blocksOffset = self._offset.value()
        # _wallCols: int = 14
        # _wallRows: int = 8
        # _brickSize: int = 8
        # _blocksOffset: int = 5
        # _barSize: int = 20
        self._breakout.setParams(newParams)


root = ttk.TTk(title="Breakout - The Roguelike", layout=ttk.TTkGridLayout())

frame = ttk.TTkFrame(layout=ttk.TTkGridLayout(), title="BreakOuTTk - The Roguelike")
breakout = BreakOutDisplay(parent=frame)

root.layout().addWidget(frame,1,1)
root.layout().addItem(ttk.TTkLayout(),0,0)
root.layout().addItem(ttk.TTkLayout(),2,0)
root.layout().addItem(ttk.TTkLayout(),0,2)
root.layout().addItem(ttk.TTkLayout(),2,2)

winParams = WinParams(breakout,
                      title="Params",
                      flags = ttk.TTkK.WindowFlag.WindowReduceButtonHint | ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
ttk.TTkHelper.overlay(None, winParams, 2, 2, toolWindow=True)
winParams.resize(30,20)

root.mainloop()
