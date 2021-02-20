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
from TermTk.TTkCore.color import *
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
        # TTkLog.debug((self._width, self._height))

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
            self._colors[i] = [TTkColor.RST]*w
        self._width  = w
        self._height = h
        TTkHelper.addPaintBuffer(self)

    def clean(self, pos=(0, 0), size=None):
        x,y = pos
        w,h = size if size is not None else (self._width, self._height)
        for iy in range(y,y+h):
            for ix in range(x,x+w):
                self._data[iy][ix] = ' '
                self._colors[iy][ix] = TTkColor.RST

    def zTop(self):
        # TODO: Figure out how to use this
        pass

    def drawText(self, pos, text, color=TTkColor.RST):
        def _set(_y,_x,_c):
            if  _y < self._height  and \
                _x < self._width and \
                _x >= 0 and _y >=0 :
                self._data[_y][_x] = _c
                self._colors[_y][_x] = color
        x,y = pos
        arr = list(text)
        for i in range(0, len(arr)):
            _set(y, x+i, arr[i])


    def drawBox(self, pos, size, color=TTkColor.RST):
        x,y = pos
        w,h = size
        # TODO: Handle Clip/OutOfBorder
        def _set(_y,_x,_c):
            if  _y < self._height  and \
                _x < self._width and \
                _x >= 0 and _y >=0 :
                self._data[_y][_x] = _c
                self._colors[_y][_x] = color
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

    '''
    geom  = (x,y,w,h)
    bound = (x,y,w,h)
    '''
    def paintCanvas(self, canvas, geom, slice, bound):
        # TTkLog.debug(f"PaintCanvas:{(x,y,w,h)}")
        x, y, w, h  = geom
        bx,by,bw,bh = bound
        # out of bound
        if x+w < bx or y+h<by or bx+bw<x or by+bh<y:
            return
        if x>=self._width:    x=self._width-1
        if y>=self._height:   y=self._height-1
        if w>=self._width-x:  w=self._width-x
        if h>=self._height-y: h=self._height-y

        xoffset = 0 if x>=bx else bx-x
        yoffset = 0 if y>=by else by-y
        wslice = w if x+w < bx+bw else bx+bw-x
        hslice = h if y+h < by+bh else by+bh-y

        for iy in range(yoffset,hslice):
            for ix in range(xoffset,wslice):
                #TTkLog.debug(f"PaintCanvas:{(ix,iy)}")
                self._data[y+iy][x+ix]   = canvas._data[iy][ix]
                self._colors[y+iy][x+ix] = canvas._colors[iy][ix]

    def pushToTerminal(self, x, y, w, h):
        # TTkLog.debug("pushToTerminal")
        lastcolor = None
        for y in range(0, self._height):
            ansi = lbt.Mv.t(y+1,1)
            for x in range(0, self._width):
                ch = self._data[y][x]
                color = self._colors[y][x]
                if color != lastcolor:
                    ansi += color
                    lastcolor = color
                ansi+=ch
            lbt.Term.push(ansi)