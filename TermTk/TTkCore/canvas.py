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

import math

import TermTk.libbpytop as lbt
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg, TTkGlbl
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.helper import TTkHelper

class TTkCanvas:
    ''' Init the Canvas object

    :param  width: the width of the Canvas
    :param  height: the height of the Canvas
    '''
    __slots__ = (
        '_widget',
        '_width', '_height', '_newWidth', '_newHeight',
        '_theme',
        '_data', '_colors',
        '_bufferedData', '_bufferedColors',
        '_visible', '_doubleBuffer')
    def __init__(self, *args, **kwargs):
        self._widget = kwargs.get('widget', None)
        self._visible = True
        self._doubleBuffer = False
        self._width = 0
        self._height = 0
        self._data = [[0]]
        self._colors = [[TTkColor.RST]]
        self._newWidth = kwargs.get('width', 0 )
        self._newHeight = kwargs.get('height', 0 )
        self.updateSize()
        # self.resize(self._width, self._height)
        # TTkLog.debug((self._width, self._height))

    def getWidget(self): return self._widget

    def enableDoubleBuffer(self):
        self._doubleBuffer = True
        self._bufferedData, self._bufferedColors = self.copy()

    def updateSize(self):
        if not self._visible: return
        w,h = self._newWidth, self._newHeight
        if w  == self._width and h == self._height:
            return
        self._data = [[]]*h
        self._colors = [[]]*h
        for i in range(0,h):
            self._data[i] = [' ']*w
            self._colors[i] = [TTkColor.RST]*w
        if self._doubleBuffer:
            self._bufferedData = [[]]*h
            self._bufferedColors = [[]]*h
            for i in range(0,h):
                self._bufferedData[i] = ['']*w
                self._bufferedColors[i] = [TTkColor.RST]*w
        self._height = h
        self._width  = w

    def resize(self, w, h):
        ''' resize the canvas keeping or cutting the current one

        :param  w: the width of the new canvas
        :param  h: the height of the new canvas
        '''
        self._newWidth = w
        self._newHeight = h

    def clean(self, pos=(0, 0), size=None):
        if not self._visible: return
        x,y = pos
        w,h = size or (self._width, self._height)
        for iy in range(y,y+h):
            for ix in range(x,x+w):
                self._data[iy][ix] = ' '
                self._colors[iy][ix] = TTkColor.RST

    def copy(self):
        w,h = self._width, self._height
        retData = [[]]*h
        retColors = [[]]*h
        for iy in range(h):
            retData[iy] = [' ']*w
            retColors[iy] = [TTkColor.RST]*w
            for ix in range(w):
                retData[iy][ix] = self._data[iy][ix]
                retColors[iy][ix] = self._colors[iy][ix]
        return retData, retColors

    def hide(self):
        self._visible = False

    def show(self):
        self._visible = True

    def _set(self, _y, _x, _ch, _col=TTkColor.RST):
        if 0 <= _y < self._height and \
           0 <= _x < self._width  :
            self._data[_y][_x] = _ch
            self._colors[_y][_x] = _col.mod(_x,_y)

    def drawVLine(self, pos, size, color=TTkColor.RST):
        if size == 0: return
        x,y = pos
        ln = TTkCfg.theme.vline
        self._set(y, x, ln[0], color)
        self._set(y+size-1, x, ln[2], color)
        if size > 2:
            for i in range(1,size-1):
                self._set(y+i, x, ln[1], color)

    def drawHLine(self, pos, size, color=TTkColor.RST):
        if size == 0: return
        x,y = pos
        ln = TTkCfg.theme.hline
        if size == 1:
            txt = ln[0]
        elif size == 2:
            txt = ln[0]+ln[2]
        else:
            txt = ln[0]+(ln[1]*(size-2))+ln[2]
        self.drawText(pos=pos, text=txt, color=color)

    '''
        pos = (x:int, y:int)
        items      = [str] # list of str to be written (for each column)
        size       = [int] # list of output sizes (for each column)
        colors     = [TTkColor] # list of colors (for each column)
        alignments = [TTkK.alignment] # list of txtalignments (for each column)
    '''
    def drawTableLine(self, pos, items, sizes, colors, alignments ):
        x,y = pos
        for i in range(0,len(items)):
            txt = items[i]
            w = sizes[i]
            color = colors[i]
            align = alignments[i]
            if w > 0:
                line = ""
                lentxt = len(txt)
                if lentxt > w:
                    line += txt[0:w]
                else:
                    pad = w-lentxt
                    if align in [TTkK.NONE,TTkK.LEFT_ALIGN]:
                        line += txt + " "*pad
                    elif align == TTkK.RIGHT_ALIGN:
                        line += " "*pad + txt
                    elif align == TTkK.CENTER_ALIGN:
                        p1 = pad//2
                        p2 = pad-p1
                        line += " "*p1 + txt+" "*p2
                    elif align == TTkK.JUSTIFY:
                        # TODO: Text Justification
                        line += txt + " "*pad
                self.drawText(pos=(x,y), text=line, color=color)
                x += w + 1

    def drawChar(self, pos, char, color=TTkColor.RST):
        if not self._visible: return
        x,y = pos
        self._set(y, x, char, color)

    def drawText(self, pos, text, width=None, color=TTkColor.RST, alignment=TTkK.NONE):
        '''
            NOTE:
            drawText is one of the most abused functions,
            there is some reduntant code here in order to reduce the footprint
        '''
        if not self._visible: return

        # Check the size and bounds
        x,y = pos
        if y<0 or y>=self._height : return

        lentxt = len(text)
        if width is None or width<0:
            width = lentxt

        if x+width<0 or x>=self._width : return

        if isinstance(text, TTkString):
            text = text.align(width=width, alignment=alignment, color=color)
            txt, colors = text.getData()
            for i in range(0, min(len(txt),self._width-x)):
                #self._set(y, x+i, txt[i-x], colors[i-x])
                self._data[y][x+i] = txt[i]
                self._colors[y][x+i] =  colors[i].mod(x+i,y)
        else:
            if lentxt < width:
                pad = width-lentxt
                if alignment in [TTkK.NONE, TTkK.LEFT_ALIGN]:
                    text = text + " "*pad
                elif alignment == TTkK.RIGHT_ALIGN:
                    text = " "*pad + text
                elif alignment == TTkK.CENTER_ALIGN:
                    p1 = pad//2
                    p2 = pad-p1
                    text = " "*p1 + text+" "*p2
                elif alignment == TTkK.JUSTIFY:
                    # TODO: Text Justification
                    text = text + " "*pad
            else:
                text=text[:width]

            arr = list(text)
            for i in range(0, min(len(arr),self._width-x)):
                self._set(y, x+i, arr[i], color)

    def drawBoxTitle(self, pos, size, text, align=TTkK.CENTER_ALIGN, color=TTkColor.RST, colorText=TTkColor.RST, grid=0):
        if not self._visible: return
        x,y = pos
        w,h = size
        if w < 4: return
        gg = TTkCfg.theme.grid[grid]

        if len(text) > w-4:
            text = text[:w-4]
        if align == TTkK.CENTER_ALIGN:
            l = (w-2-len(text))//2
        elif align == TTkK.LEFT_ALIGN:
            l=1
        else:
            l = w-2-len(text)
        r = l+len(text)+1

        self._set(y,l, gg[7], color)
        self._set(y,r, gg[6], color)
        self.drawText(pos=(l+1,y),text=text,color=colorText)



    def drawBox(self, pos, size, color=TTkColor.RST, grid=0):
        self.drawGrid(pos=pos, size=size, color=color, grid=grid)

    def drawButtonBox(self, pos, size, color=TTkColor.RST, grid=0):
        if not self._visible: return
        x,y = pos
        w,h = size
        gg = TTkCfg.theme.buttonBox[grid]
        # 4 corners
        self._set(y,     x,     gg[0], color)
        self._set(y,     x+w-1, gg[2], color)
        self._set(y+h-1, x,     gg[6], color)
        self._set(y+h-1, x+w-1, gg[8], color)
        if w > 2:
            for i in range(x+1,x+w-1):
                self._set(y,     i, gg[1], color)
                self._set(y+h-1, i, gg[7], color)
        if h > 2:
            for i in range(y+1,y+h-1):
                self._set(i, x,     gg[3], color)
                self._set(i, x+w-1, gg[5], color)

    def drawGrid(self, pos, size, hlines=[], vlines=[], color=TTkColor.RST, grid=0):
        if not self._visible: return
        x,y = pos
        w,h = size
        gg = TTkCfg.theme.grid[grid]
        # 4 corners
        self._set(y,     x,     gg[0x00], color)
        self._set(y,     x+w-1, gg[0x03], color)
        self._set(y+h-1, x,     gg[0x0C], color)
        self._set(y+h-1, x+w-1, gg[0x0F], color)
        if w > 2:
            # Top/Bottom Line
            for i in range(x+1,x+w-1):
                self._set(y,   i, gg[0x01], color)
                self._set(y+h-1, i, gg[0x0D], color)
        if h > 2:
            # Left/Right Line
            for i in range(y+1,y+h-1):
                self._set(i, x,   gg[0x04], color)
                self._set(i, x+w-1, gg[0x07], color)
        # Draw horizontal lines
        for iy in hlines:
            iy += y
            if not (0 < iy < h): continue
            self._set(iy, x,     gg[0x08], color)
            self._set(iy, x+w-1, gg[0x0B], color)
            if w > 2:
                for ix in range(x+1,x+w-1):
                    self._set(iy, ix, gg[0x09], color)
        # Draw vertical lines
        for ix in vlines:
            ix+=x
            if not (0 < ix < w): continue
            self._set(y,     ix, gg[0x02], color)
            self._set(y+h-1, ix, gg[0x0E], color)
            if h > 2:
                for iy in range(y+1,y+h-1):
                    self._set(iy, ix, gg[0x06], color)
        # Draw intersections
        for iy in hlines:
            for ix in vlines:
                self._set(y+iy, x+ix, gg[0x0A], color)

    def drawScroll(self, pos, size, slider, orientation, color=TTkColor.RST):
        if not self._visible: return
        x,y = pos
        f,t = slider # slider from-to position
        if orientation == TTkK.HORIZONTAL:
            for i in range(x+1,x+size-1): # H line
                self._set(y,x+i, TTkCfg.theme.hscroll[1], color)
            for i in range(f,t): # Slider
                self._set(y,x+i, TTkCfg.theme.hscroll[2], color)
            self._set(y,x, TTkCfg.theme.hscroll[0], color)        # Left Arrow
            self._set(y,x+size-1, TTkCfg.theme.hscroll[3], color) # Right Arrow
        else:
            for i in range(y+1,y+size-1): # V line
                self._set(y+i,x, TTkCfg.theme.vscroll[1], color)
            for i in range(f,t): # Slider
                self._set(y+i,x, TTkCfg.theme.vscroll[2], color)
            self._set(y,x, TTkCfg.theme.vscroll[0], color)        # Up Arrow
            self._set(y+size-1,x, TTkCfg.theme.vscroll[3], color) # Down Arrow
        pass

    def drawTabMenuButton(
            self, pos, size, text, slim=False,
            color=TTkColor.RST, borderColor=TTkColor.RST,
            sideBorder=TTkK.LEFT|TTkK.RIGHT):
        x,y = pos
        w,h = size
        textPos = pos
        tt = TTkCfg.theme.tab
        # phase 0 - Draw the Bottom bar
        if slim:
            borderLeft  = tt[18] if sideBorder & TTkK.LEFT  else  tt[19]
            borderRight = tt[20] if sideBorder & TTkK.RIGHT else  tt[19]
            bottomBar = borderLeft+tt[19]*(w-2)+borderRight
            self.drawText(pos=(x,y+1), text=bottomBar, color=borderColor)
        else:
            borderLeft  = tt[27] if sideBorder & TTkK.LEFT  else  tt[12]
            borderRight = tt[28] if sideBorder & TTkK.RIGHT else  tt[12]
            bottomBar = borderLeft+tt[12]*(w-2)+borderRight
            self.drawText(pos=(x,y+2), text=bottomBar, color=borderColor)
            textPos = (x,y+1)
        self.drawText(pos=textPos, text=text, color=color)

    def drawTab(
            self, pos, size,
            labels, labelsPos, selected,
            offset,  leftScroller, rightScroller, slim=False, menu=False,
            color=TTkColor.RST, borderColor=TTkColor.RST, selectColor=TTkColor.RST, offsetColor=TTkColor.RST,
            sideBorder=TTkK.LEFT|TTkK.RIGHT):
        x,y = pos
        w,h = size
        tt = TTkCfg.theme.tab
        # phase 0 - Draw the Bottom bar
        if slim:
            borderLeft  = tt[18] if sideBorder & TTkK.LEFT  else tt[29] if leftScroller  else tt[19]
            borderRight = tt[20] if sideBorder & TTkK.RIGHT else tt[29] if rightScroller else tt[19]
            bottomBar = borderLeft+tt[19]*(w-2)+borderRight
            bottomPos = y+1
        else:
            borderLeft  = tt[11] if sideBorder & TTkK.LEFT  else tt[13] if leftScroller  else tt[12]
            borderRight = tt[15] if sideBorder & TTkK.RIGHT else tt[13] if rightScroller else tt[12]
            bottomBar = borderLeft+tt[12]*(w-2)+borderRight
            bottomPos = y+2
        self.drawText(pos=(x,bottomPos),text=bottomBar, color=borderColor)
        # phase 1 - Draw From left  to 'Selected'
        # phase 2 - Draw From right to 'Selected'
        def _drawTabSlim(x,y,a,b,c,d,e,txt,txtColor,borderColor):
            lentext = len(txt)
            center = a+txt+b
            bottom = c+d*(lentext)+e
            self.drawText(pos=(x,y),text=center, color=borderColor)
            self.drawText(pos=(x+1,y),text=txt, color=txtColor)
            self.drawText(pos=(x,y+1),text=bottom, color=borderColor)
        def _drawTab(x,y,a,b,c,d,e,f,g,h,i,j,k,l,m,txt,txtColor,borderColor,slim):
            if slim: return _drawTabSlim(x,y,i,j,k,l,m,txt,txtColor,borderColor)
            lentext = len(txt)
            top =    a+b*lentext+c
            center = d+txt+e
            bottom = f+g*(lentext)+h
            self.drawText(pos=(x,y+0),text=top, color=borderColor)
            self.drawText(pos=(x,y+1),text=center, color=borderColor)
            self.drawText(pos=(x+1,y+1),text=txt, color=txtColor)
            self.drawText(pos=(x,y+2),text=bottom, color=borderColor)

        for i in list(         range(offset              )) + \
                 list(reversed(range(offset+1, len(labels)) )):
            text = labels[i]
            posx = labelsPos[i]
            _drawTab(x+posx,y,tt[0],tt[1],tt[3],tt[9],tt[9],tt[12],tt[12],tt[12],tt[9],tt[9],tt[23],tt[19],tt[24], text, color, borderColor, slim)
        # phase 3 - Draw 'Selected'
        if selected != -1:
            i = selected
            text = labels[i]
            posx = labelsPos[i]
            _drawTab(x+posx,y,tt[4],tt[5],tt[6],tt[10],tt[10],tt[14],tt[12],tt[14],tt[10],tt[10],tt[21],tt[12],tt[22], text, selectColor, borderColor, slim)
        if selected != offset:
            i = offset
            text = labels[i]
            posx = labelsPos[i]
            _drawTab(x+posx,y,tt[0],tt[1],tt[3],tt[9],tt[9],tt[13],tt[12],tt[13],tt[9],tt[9],tt[18],tt[19],tt[20], text, offsetColor, borderColor, slim)
        # phase 4 - Draw left right tilt
        if leftScroller:
            top =    tt[7]+tt[1]
            center = tt[9]+tt[31]
            if slim:
                self.drawText(pos=(x,y),text=center, color=borderColor)
            else:
                self.drawText(pos=(x,y+0),text=top, color=borderColor)
                self.drawText(pos=(x,y+1),text=center, color=borderColor)
        if rightScroller:
            top =    tt[1]+tt[8]
            center = tt[32]+tt[9]
            if slim:
                self.drawText(pos=(x+w-2,y),text=center, color=borderColor)
            else:
                self.drawText(pos=(x+w-2,y+0),text=top, color=borderColor)
                self.drawText(pos=(x+w-2,y+1),text=center, color=borderColor)

    def drawHChart(self, pos, values, zoom=1.0, color=TTkColor.RST):
        x,y=pos
        v1,v2 = values
        gb=TTkCfg.theme.braille

        '''
        loop       0   1   2   3   = range(0,1+maxt//4)
        v1    13  |---|---|---|--|
        v2    10  |---|---|-|
        maxt  13  |---|---|---|--|
        out        4,4 4,4 4,2 3,0 0,0
        o1 = 4 if v1-4 > i*4 else v1-i*4
        '''
        # TTkLog.debug(f"{(v1,v2)} z{zoom}")
        zl1 = [ int(i*zoom) for i in v1 ]
        zl2 = [ int(i*zoom) for i in v2 ]
        maxz = max(max(zl1),max(zl2),0)
        minz = min(min(zl1),min(zl2),0)
        filled = True
        for i in range(int(minz//4),int(maxz//4)+2):
            ts1 = i*4
            ts2 = i*4+4
            '''
                Braille bits:
                o2  o1 = 4 bits each

                1   5   Braille dots
                2   6
                3   7
                4   8

                TTkTheme.braille[( o1<<4 | o2 )] = Braille UTF-8 char
            '''
            braille = 0x00
            for ii in range(len(zl1)):
                z1 = zl1[ii]
                z2 = zl2[ii]
                o1,o2 = 0,0
                #TTkLog.debug
                if not filled or ii>0:
                    if ts1 <= z1 < ts2: o1 = 0x80>>max(0,int(z1-ts1))
                    if ts1 <= z2 < ts2: o2 = 0x08>>max(0,int(z2-ts1))
                else:
                    if (0<=ts1<z1)or(0>ts1>z1): o1 = 0xf0
                    if (0<=ts1<z2)or(0>ts1>z2): o2 = 0x0f
                    k1 = 0x0f80 if z1>=0 else 0x00f0
                    k2 = 0x00f8 if z2>=0 else 0x000f
                    if ts1 <= z1 < ts2: o1 = 0xf0&(k1>>max(0,int(z1-ts1)))
                    if ts1 <= z2 < ts2: o2 = 0x0f&(k2>>max(0,int(z2-ts1)))
                braille ^= (o1|o2)
                # braille &= 0xff
            #TTkLog.debug(f"z:{zl1,zl2}, ts:{ts1,ts2},{o1,o2}")
            #if braille<0 or braille>0xff:
            #    TTkLog.debug(f"z:{zl1,zl2},t:{t1,t2},i:{i} {t1-i*4} {t2-i*4} o:{o1,o2}, {hex(braille)}")
            self._set(y-i-1,x, gb[braille], color)

    def drawMenuBarBg(self, pos, size, color=TTkColor.RST ):
        mb = TTkCfg.theme.menuBar
        self.drawText(pos, text=f"{mb[3]}{mb[1]*(size-2)}{mb[4]}", color=color)

    def drawMenuBarButton(self, pos, width, text, border=True, submenu=False, shortcuts=[], color=TTkColor.RST, borderColor=TTkColor.RST, shortcutColor=TTkColor.UNDERLINE ):
        mb = TTkCfg.theme.menuBar
        x,y = pos
        if border:
            self.drawText(pos=(x,y), color=borderColor ,text=mb[2])
            self.drawText(pos=(x+1+len(text),y), color=borderColor ,text=mb[0])
            self.drawText(pos=(x+1,y), color=color ,text=text)
            off = 1
        else:
            self.drawText(pos=(x,y), width=width, color=color ,text=text)
            if submenu:
                self._set(y,x+width-1, mb[5], color)
            off = 0
        for i in shortcuts:
            self._set(y,x+i+off, text[i], shortcutColor)

    def execPaint(self, winw, winh):
        pass

    '''
    geom  = (x,y,w,h)
    bound = (x,y,w,h)

                    x                       x+w
    canvas:         |xxxxxxxxxxxxxxxxxxxxxxx|
    slice:                     |-----------|
                             bx       bx+bw
    bound:                   |--------|
                          0                      self._width
    self._canvas:         |----|xxxxxx|----------|
    '''
    def paintCanvas(self, canvas, geom, slice, bound):
        # TTkLog.debug(f"PaintCanvas:{(x,y,w,h)}")
        x, y, w, h  = geom
        bx,by,bw,bh = bound
        # out of bound
        if not self._visible: return
        if not canvas._visible: return
        if canvas._width==0 or canvas._height==0: return
        if x+w < bx or y+h<by or bx+bw-1<x or by+bh-1<y:
            return

        x = min(x,self._width-1)
        y = min(y,self._height-1)
        w = min(w,self._width-x)
        h = min(h,self._height-y)

        # if x>=self._width:    x=self._width-1
        # if y>=self._height:   y=self._height-1
        # if w>=self._width-x:  w=self._width-x
        # if h>=self._height-y: h=self._height-y

        xoffset = 0 if x>=bx else bx-x
        yoffset = 0 if y>=by else by-y
        wslice = w if x+w < bx+bw else bx+bw-x
        hslice = h if y+h < by+bh else by+bh-y


        for iy in range(yoffset,hslice):
            for ix in range(xoffset,wslice):
                #TTkLog.debug(f"PaintCanvas:{(ix,iy)}")
                if iy > len(canvas._data)-1:
                    TTkLog.debug(f"{canvas._width, canvas._height} - {(yoffset,hslice)}, {(xoffset,wslice)}, {slice}")
                b = canvas._data[iy]
                a = b[ix]
                self._data[y+iy][x+ix]   = a # canvas._data[iy][ix]
                self._colors[y+iy][x+ix] = canvas._colors[iy][ix]

    def pushToTerminal(self, x, y, w, h):
        # TTkLog.debug("pushToTerminal")
        lastcolor = TTkColor.RST
        for y in range(0, self._height):
            ansi = TTkColor.RST+lbt.Mv.t(y+1,1)
            for x in range(0, self._width):
                ch = self._data[y][x]
                color = self._colors[y][x]
                if color != lastcolor:
                    ansi += color-lastcolor
                    lastcolor = color
                ansi+=ch
            lbt.Term.push(ansi)

    def pushToTerminalBuffered(self, x, y, w, h):
        # TTkLog.debug("pushToTerminal")
        oldData, oldColors = self._bufferedData, self._bufferedColors
        lastcolor = TTkColor.RST
        empty = True
        ansi = ""
        for y in range(0, self._height):
            for x in range(0, self._width):
                if self._data[y][x] == oldData[y][x] and \
                   self._colors[y][x] == oldColors[y][x]:
                    if not empty:
                        lbt.Term.push(ansi)
                        empty=True
                    continue
                ch = self._data[y][x]
                color = self._colors[y][x]
                if empty:
                    ansi = color+lbt.Mv.t(y+1,x+1)
                    #lastcolor = color
                    empty = False
                if color != lastcolor:
                    ansi += color-lastcolor
                    lastcolor = color
                ansi+=ch
            if not empty:
                lbt.Term.push(ansi)
                empty=True
        # Reset the color at the end
        lbt.Term.push(TTkColor.RST)
        # Switch the buffer
        self._bufferedData, self._bufferedColors = self._data, self._colors
        self._data, self._colors = oldData, oldColors
