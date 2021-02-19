#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import TermTk.libbpytop as lbt
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.helper import *

class TTkCanvas:
    '''
    TTkCanvas
    canvas window primitives
    ...
    Attributes
    ----------
    Methods
    -------
    __init__({})
      input obj{ width, height}

    resize(w, h)
      - resize the canvas keeping or cutting the current one
      in  w = the width of the new canvas
      in  h = the height of the new canvas
    '''
    def __init__(self, *args, **kwargs):
        self._widget = kwargs.get('widget', None)
        self._width = kwargs.get('width', 0 )
        self._height = kwargs.get('height', 0 )
        self.resize(self._width, self._height)
        TTkLog.debug((self._width, self._height))

    def getWidget(self): return self._widget

    def move(self, x, y):
        npos = TTkHelper.absParentPos(self._widget)
        # CuTCore.cuDebug("Move: x:"+str(nx+x)+" y:"+str(ny+y))
        # self._bufPaint['move']={'x':npos.x()+x, 'y':npos.y()+y}
        TTkHelper.addPaintBuffer(self)

    def resize(self, w, h):
        # TTkLog.debug(f"CanvasResize:{(w,h)}")
        self._data = [[]]*h
        self._colors = [[]]*h
        for i in range(0,h):
            self._data[i] = [' ']*w
            self._colors[i] = [None]*w
        self._width  = w
        self._height = h
        TTkHelper.addPaintBuffer(self)

    def zTop(self):
        # TODO: Figure out how to use this
        pass

    def drawBox(self, x, y, w, h):
        def _set(_y,_x,_c):
            if _y<self._height and _x < self._width:
                self._data[_y][_x] = _c
        # 4 corners
        _set(y,     x,     "╔")
        _set(y,     x+w-1, "╗")
        _set(y+h-1, x,     "╚")
        _set(y+h-1, x+w-1, "╝")
        if w > 2:
            for i in range(x+1,x+w-1):
                _set(y,   i, "═")
                _set(y+h-1, i, "═")
        if h > 2:
            for i in range(y+1,y+h-1):
                _set(i, x,   "║")
                _set(i, x+w-1, "║")
        TTkHelper.addPaintBuffer(self)

    def execPaint(self, winw, winh):
        pass

    def paintCanvas(self, canvas, x, y, w, h):
        # TTkLog.debug(f"PaintCanvas:{(x,y,w,h)}")
        x = x if x<self._width    else self._width-1
        y = y if y<self._height   else self._height-1
        w = w if x+w<self._width  else self._width-x
        h = h if y+h<self._height else self._height-y
        for iy in range(0,h):
            for ix in range(0,w):
                self._data[y+iy][x+ix]   = canvas._data[iy][ix]
                self._colors[y+iy][x+ix] = canvas._colors[iy][ix]

    def pushToTerminal(self, x, y, w, h):
        TTkLog.debug("pushToTerminal")
        ansi = ""
        for y in range(0, self._height):
            s = lbt.Mv.t(y+1,1)
            for x in range(0, self._width):
                c = self._data[y][x]
                s+=c
            ansi += s

        lbt.Term.push(ansi)
