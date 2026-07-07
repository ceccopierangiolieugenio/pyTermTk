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

from __future__ import annotations

__all__ = ['TTkCanvas']

from typing import List, Optional, Tuple

from TermTk.TTkCore.TTkTerm.term import TTkTerm
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString

_CanvasDataBuffer = List[List[str]]
_CanvasColorBuffer = List[List[TTkColor]]

class TTkCanvas():
    ''' TTkCanvas:

    A low-level drawing surface that stores characters and colors before they
    are composed into widgets or flushed to the terminal.

    :param width: the width of the Canvas
    :type width: int
    :param height: the height of the Canvas
    :type height: int
    '''
    __slots__ = (
        '_width', '_height', '_newWidth', '_newHeight',
        '_data', '_colors',
        '_bufferedData', '_bufferedColors',
        '_visible', '_transparent', '_doubleBuffer')
    _data: _CanvasDataBuffer
    _colors: _CanvasColorBuffer
    _bufferedData: _CanvasDataBuffer
    _bufferedColors: _CanvasColorBuffer
    def __init__(self,
                 width:int=0,
                 height:int=0) -> None:
        self._visible = True
        self._transparent = False
        self._doubleBuffer = False
        self._width = 0
        self._height = 0
        self._data   = [[]]
        self._colors = [[]]
        self._newWidth = width
        self._newHeight = height
        self.updateSize()
        # self.resize(self._width, self._height)
        # TTkLog.debug((self._width, self._height))

    def transparent(self) -> bool:
        ''' Returns whether the canvas treats empty cells as transparent.

        :return: ``True`` when empty cells preserve the destination canvas
        :rtype: bool
        '''
        return self._transparent

    def setTransparent(self, tr:bool=True) -> None:
        ''' Enables or disables transparent composition for this canvas.

        :param tr: ``True`` to preserve destination cells where nothing is drawn
        :type tr: bool
        '''
        self._transparent = tr
        self.clean()

    def enableDoubleBuffer(self) -> None:
        ''' Initializes the secondary buffer used for buffered terminal updates.
        '''
        self._doubleBuffer = True
        self._bufferedData, self._bufferedColors = self.copyBuffers()

    def updateSize(self) -> None:
        ''' Rebuilds the internal buffers when the requested canvas size changes.
        '''
        if not self._visible: return
        w,h = self._newWidth, self._newHeight
        if w  == self._width and h == self._height:
            return
        if self._transparent:
            baseData = [None]*w
            baseColors = baseData
        else:
            baseData = [' ']*w
            baseColors = [TTkColor.RST]*w
        self._data   = [baseData.copy()   for _ in range(h)]
        self._colors = [baseColors.copy() for _ in range(h)]
        if self._doubleBuffer:
            self._bufferedData   = [baseData.copy()   for _ in range(h)]
            self._bufferedColors = [baseColors.copy() for _ in range(h)]
        self._height = h
        self._width  = w

    def size(self) -> Tuple[int,int]:
        ''' Returns the current canvas size.

        :return: the width and height of the canvas
        :rtype: tuple[int, int]
        '''
        return (self._width, self._height)

    def resize(self, w: int, h: int) -> None:
        ''' resize the canvas keeping or cutting the current one

        :param  w: the width of the new canvas
        :param  h: the height of the new canvas
        '''
        self._newWidth = w
        self._newHeight = h

    def clean(self) -> None:
        ''' Clears the canvas content using either blanks or transparent cells.
        '''
        if not self._visible: return
        w,h = self._width, self._height
        if self._transparent:
            baseData = [None]*w
            baseColors = baseData
        else:
            baseData = [' ']*w
            baseColors = [TTkColor.RST]*w
        self._data   = [baseData.copy()   for _ in range(h)]
        self._colors = [baseColors.copy() for _ in range(h)]

    def copy(self) -> TTkCanvas:
        ''' Creates a detached copy of the canvas content.

        :return: a new canvas with duplicated size and buffers
        :rtype: :py:class:`TTkCanvas`
        '''
        ret = TTkCanvas()
        ret._width = self._width
        ret._height = self._height
        ret._data, ret._colors = self.copyBuffers()
        return ret

    def copyBuffers(self) -> Tuple[_CanvasDataBuffer, _CanvasColorBuffer]:
        ''' Duplicates the current character and color buffers.

        :return: copies of the data and color buffers
        :rtype: tuple[list[list[str]], list[list[:py:class:`TTkColor`]]]
        '''
        h = self._height
        retData   = [self._data[i].copy()   for i in range(h)]
        retColors = [self._colors[i].copy() for i in range(h)]
        return retData, retColors

    def hide(self) -> None:
        ''' Marks the canvas as hidden so draw operations become no-ops.
        '''
        self._visible = False

    def show(self) -> None:
        ''' Marks the canvas as visible again.
        '''
        self._visible = True

    def _set(
            self,
            _y: int,
            _x: int,
            _ch: str,
            _col: TTkColor = TTkColor.RST) -> None:
        if 0 <= _y < self._height and \
           0 <= _x < self._width  :
            self._data[_y][_x] = _ch
            self._colors[_y][_x] = _col.mod(_x,_y)

    def fill(
            self,
            pos: Tuple[int,int] = (0,0),
            size: Optional[Tuple[int,int]] = None,
            char: str = ' ',
            color: TTkColor = TTkColor.RST) -> None:
        ''' Fills a rectangular region with a character and color.

        :param pos: the top-left position of the fill area
        :type pos: tuple[int, int]
        :param size: the width and height of the fill area, defaults to the full canvas
        :type size: tuple[int, int] | None
        :param char: the character written into each cell
        :type char: str
        :param color: the color applied to the filled cells
        :type color: :py:class:`TTkColor`
        '''
        w,h = self.size()
        if not size:
            size=(w,h)
        fxa,fya = pos
        fw,fh = size
        fxb,fyb = fxa+fw, fya+fh
        # the fill area is outside the boundaries
        if ( fxa >= w or fya >= h or
             fxb <= 0 or fyb <= 0): return

        fxa = max(0,fxa)
        fya = max(0,fya)
        fxb = min(w,fxb)
        fyb = min(h,fyb)

        fillCh    = [char]*(fxb-fxa)
        for iy in range(fya,fyb):
            self._data[iy][fxa:fxb]   = fillCh
        if color.colorType() & TTkK.ColorType.ColorModifier:
            for iy in range(fya,fyb):
                for ix in range(fxa,fxb):
                    self._colors[iy][ix] = color.mod(fxa+ix,fya+iy)
        else:
            fillColor = [color]*(fxb-fxa)
            for iy in range(fya,fyb):
                self._colors[iy][fxa:fxb] = fillColor

    def drawVLine(
            self,
            pos: Tuple[int,int],
            size: int,
            color: TTkColor = TTkColor.RST) -> None:
        ''' Draws a themed vertical line segment.

        :param pos: the top position of the line
        :type pos: tuple[int, int]
        :param size: the height of the line
        :type size: int
        :param color: the color used for the line glyphs
        :type color: :py:class:`TTkColor`
        '''
        if size == 0: return
        x,y = pos
        ln = TTkCfg.theme.vline
        self._set(y, x, ln[0], color)
        self._set(y+size-1, x, ln[2], color)
        if size > 2:
            for i in range(1,size-1):
                self._set(y+i, x, ln[1], color)

    def drawHLine(
            self,
            pos: Tuple[int,int],
            size: int,
            color: TTkColor = TTkColor.RST) -> None:
        ''' Draws a themed horizontal line segment.

        :param pos: the left position of the line
        :type pos: tuple[int, int]
        :param size: the width of the line
        :type size: int
        :param color: the color used for the line glyphs
        :type color: :py:class:`TTkColor`
        '''
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
    def drawTableLine(
            self,
            pos: Tuple[int,int],
            items: List[str],
            sizes: List[int],
            colors: List[TTkColor],
            alignments: List[TTkK.Alignment] ) -> None:
        ''' Draws a single row of table cells with per-column formatting.

        :param pos: the starting position of the first cell
        :type pos: tuple[int, int]
        :param items: the strings to render in each column
        :type items: list[str]
        :param sizes: the width of each column
        :type sizes: list[int]
        :param colors: the color used for each column
        :type colors: list[:py:class:`TTkColor`]
        :param alignments: the alignment used for each column
        :type alignments: list[:py:class:`TTkK.Alignment`]
        '''
        x,y = pos
        for i in range(0,len(items)):
            txt = items[i]
            w = sizes[i]
            color = colors[i]
            align = alignments[i]
            if w > 0:
                self.drawText(pos=(x,y), text=txt, width=w, color=color, alignment=align)
                x += w + 1

    def drawChar(
            self,
            pos: Tuple[int,int],
            char: str,
            color: TTkColor = TTkColor.RST) -> None:
        ''' Draws a single character at the given position.

        :param pos: the target position
        :type pos: tuple[int, int]
        :param char: the character to draw
        :type char: str
        :param color: the color applied to the character
        :type color: :py:class:`TTkColor`
        '''
        if not self._visible: return
        x,y = pos
        self._set(y, x, char, color)


    def drawTTkString(
            self,
            pos: Tuple[int,int],
            text: TTkString,
            width: Optional[int] = None,
            color: TTkColor = TTkColor.RST,
            alignment: TTkK.Alignment = TTkK.Alignment.NONE,
            forceColor: bool = False) -> None:
        ''' Draws a :py:class:`TTkString` with alignment and optional color override.

        This method keeps a dedicated fast path because text drawing is used in
        most widgets and needs to minimize conversion overhead.

        :param pos: the top-left position where the string is drawn
        :type pos: tuple[int, int]
        :param text: the formatted text object to render
        :type text: :py:class:`TTkString`
        :param width: the output width, defaults to the string terminal width
        :type width: int | None
        :param color: an additional color merged with the string colors
        :type color: :py:class:`TTkColor`
        :param alignment: the alignment used inside ``width``
        :type alignment: :py:class:`TTkK.Alignment`
        :param forceColor: ``True`` to ignore embedded string colors and use only ``color``
        :type forceColor: bool
        '''
        # NOTE:
        # drawText is one of the most abused functions,
        # there is some redundant code here in order to reduce the footprint
        if not self._visible: return

        # Check the size and bounds
        x,y = pos
        if y<0 or y>=self._height : return

        lentxt = text.termWidth()
        if width is None or width<0:
            width = lentxt

        if x+width<0 or x>=self._width : return

        text = text.align(width=width, alignment=alignment, color=color)
        txt, colors = text.tab2spaces().getData()
        a,b = max(0,-x), min(len(txt),self._width-x)
        self._data[y][x+a:x+b] = txt[a:b]
        if forceColor:
            colors=[color]*len(colors)
        else:
            for i in range(a,b):
                if color != TTkColor.RST:
                    self._colors[y][x+i] = (colors[i] | color).mod(x+i,y)
                else:
                    self._colors[y][x+i] = colors[i].mod(x+i,y)
        # Check the full wide chars on the edge of the two canvasses
        if ((0 <= (x+a) < self._width) and self._data[y][x+a] == ''):
            self._data[y][x+a]   = TTkCfg.theme.unicodeWideOverflowCh[0]
            self._colors[y][x+a] = TTkString.unicodeWideOverflowColor
        if ((0 <= (x+b-1) < self._width) and TTkString._isWideCharData(self._data[y][x+b-1])):
            self._data[y][x+b-1]   = TTkCfg.theme.unicodeWideOverflowCh[1]
            self._colors[y][x+b-1] = TTkString.unicodeWideOverflowColor

    def drawText(
            self,
            text: str = "",
            pos: Tuple[int,int] = (0,0),
            width: Optional[int] = None,
            color: TTkColor = TTkColor.RST,
            alignment: TTkK.Alignment = TTkK.Alignment.NONE,
            forceColor: bool = False) -> None:
        ''' Draws plain text with optional alignment and color.

        This method keeps a dedicated fast path because text drawing is used in
        most widgets and needs to minimize conversion overhead.

        :param text: the string to render
        :type text: str
        :param pos: the top-left position where the text is drawn
        :type pos: tuple[int, int]
        :param width: the output width, defaults to the text length
        :type width: int | None
        :param color: the color applied to the text
        :type color: :py:class:`TTkColor`
        :param alignment: the alignment used inside ``width``
        :type alignment: :py:class:`TTkK.Alignment`
        :param forceColor: kept for API parity with :py:meth:`drawTTkString`
        :type forceColor: bool
        '''
        # NOTE:
        # drawText is one of the most abused functions,
        # there is some redundant code here in order to reduce the footprint
        if not self._visible: return
        if isinstance(text, TTkString):
            return self.drawTTkString(pos, text, width, color, alignment, forceColor)

        # Check the size and bounds
        x,y = pos
        if y<0 or y>=self._height : return

        lentxt = len(text)
        if width is None or width<0:
            width = lentxt

        if x+width<0 or x>=self._width : return

        text = text.replace('\t','    ')
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

    def drawBoxTitle(
            self,
            pos: Tuple[int,int],
            size: Tuple[int,int],
            text: TTkString,
            align: TTkK.Alignment = TTkK.Alignment.CENTER_ALIGN,
            color: TTkColor = TTkColor.RST,
            colorText: TTkColor = TTkColor.RST) -> None:
        ''' Draws a titled label embedded into the top border of a box.

        :param pos: the top-left position of the surrounding box
        :type pos: tuple[int, int]
        :param size: the size of the surrounding box
        :type size: tuple[int, int]
        :param text: the title text to render
        :type text: :py:class:`TTkString`
        :param align: the title alignment along the top border
        :type align: :py:class:`TTkK.Alignment`
        :param color: the border color around the title
        :type color: :py:class:`TTkColor`
        :param colorText: the color of the title text
        :type colorText: :py:class:`TTkColor`
        '''
        if not self._visible: return
        x,y = pos
        w,h = size
        if w < 4: return

        if text.termWidth() > w-4:
            text = text.substring(to=w-4)
        if align == TTkK.CENTER_ALIGN:
            l = (w-2-text.termWidth())//2
        elif align == TTkK.LEFT_ALIGN:
            l=1
        else:
            l = w-3-text.termWidth()
        l+=x
        r = l+text.termWidth()+1

        self._set(y,l, '╸', color)
        self._set(y,r, '╺', color)
        self.drawTTkString(pos=(l+1,y), text=text, color=colorText)

    def drawBox(
            self,
            pos: Tuple[int,int],
            size: Tuple[int,int],
            color: TTkColor = TTkColor.RST,
            grid: int = 0) -> None:
        ''' Draws a rectangular box using the configured grid theme.

        :param pos: the top-left position of the box
        :type pos: tuple[int, int]
        :param size: the width and height of the box
        :type size: tuple[int, int]
        :param color: the color applied to the box border
        :type color: :py:class:`TTkColor`
        :param grid: the themed grid variant to use
        :type grid: int
        '''
        self.drawGrid(pos=pos, size=size, color=color, grid=grid)

    def drawButtonBox(
            self,
            pos: Tuple[int,int],
            size: Tuple[int,int],
            color: TTkColor = TTkColor.RST,
            grid: int =0) -> None:
        ''' Draws a button-style border using the button box theme.

        :param pos: the top-left position of the box
        :type pos: tuple[int, int]
        :param size: the width and height of the box
        :type size: tuple[int, int]
        :param color: the color applied to the border
        :type color: :py:class:`TTkColor`
        :param grid: the themed button box variant to use
        :type grid: int
        '''
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

    def drawGrid(
            self,
            pos: Tuple[int,int],
            size: Tuple[int,int],
            hlines: List[int] = [],
            vlines: List[int] = [],
            color: TTkColor = TTkColor.RST,
            grid: int = 0) -> None:
        ''' Draws a bordered grid with optional internal horizontal and vertical lines.

        :param pos: the top-left position of the grid
        :type pos: tuple[int, int]
        :param size: the width and height of the grid
        :type size: tuple[int, int]
        :param hlines: row offsets for inner horizontal separators
        :type hlines: list[int]
        :param vlines: column offsets for inner vertical separators
        :type vlines: list[int]
        :param color: the color applied to the grid glyphs
        :type color: :py:class:`TTkColor`
        :param grid: the themed grid variant to use
        :type grid: int
        '''
        if not self._visible: return
        x,y = pos
        w,h = size
        gg = TTkCfg.theme.grid[grid]

        if not gg:
            return

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

    def drawScroll(
            self,
            pos: Tuple[int,int],
            size: int,
            slider: Tuple[int,int],
            orientation: TTkK.Direction,
            color: TTkColor = TTkColor.RST) -> None:
        ''' Draws a horizontal or vertical scrollbar.

        :param pos: the top-left position of the scrollbar
        :type pos: tuple[int, int]
        :param size: the total length of the scrollbar including arrow cells
        :type size: int
        :param slider: the slider start and end positions relative to ``pos``
        :type slider: tuple[int, int]
        :param orientation: the scrollbar orientation
        :type orientation: :py:class:`TTkK.Direction`
        :param color: the color applied to the scrollbar glyphs
        :type color: :py:class:`TTkColor`
        '''
        if not self._visible: return
        x,y = pos
        f,t = slider # slider from-to position
        if orientation == TTkK.HORIZONTAL:
            for i in range(x+1,x+size-1): # H line
                self._set(y,x+i, TTkCfg.theme.hscroll[1], color)
            for i in range(f,t): # Slider
                self._set(y,x+i, TTkCfg.theme.hscroll[2], color)
            self._set(y,x+size-1, TTkCfg.theme.hscroll[3], color) # Right Arrow
            self._set(y,x, TTkCfg.theme.hscroll[0], color)        # Left Arrow
        else:
            for i in range(y+1,y+size-1): # V line
                self._set(y+i,x, TTkCfg.theme.vscroll[1], color)
            for i in range(f,t): # Slider
                self._set(y+i,x, TTkCfg.theme.vscroll[2], color)
            self._set(y+size-1,x, TTkCfg.theme.vscroll[3], color) # Down Arrow
            self._set(y,x, TTkCfg.theme.vscroll[0], color)        # Up Arrow

    def drawHChart(
            self,
            pos: Tuple[int,int],
            values: Tuple[List[int],List[int]],
            zoom: float = 1.0,
            color: TTkColor = TTkColor.RST) -> None:
        ''' Draws a compact two-series vertical chart using braille cells.

        :param pos: the baseline position of the chart
        :type pos: tuple[int, int]
        :param values: the two value series to combine into each braille cell
        :type values: tuple[list[int], list[int]]
        :param zoom: a scale factor applied before rasterizing the chart
        :type zoom: float
        :param color: the color applied to the chart glyphs
        :type color: :py:class:`TTkColor`
        '''
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

    def drawMenuBarBg(
            self,
            pos: Tuple[int,int],
            size: int,
            color: TTkColor = TTkColor.RST ) -> None:
        ''' Draws the themed background strip for a menu bar.

        :param pos: the starting position of the menu bar background
        :type pos: tuple[int, int]
        :param size: the total width of the menu bar background
        :type size: int
        :param color: the color applied to the background glyphs
        :type color: :py:class:`TTkColor`
        '''
        mb = TTkCfg.theme.menuBar
        self.drawText(pos=pos, text=f"{mb[3]}{mb[1]*(size-2)}{mb[4]}", color=color)

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
    def paintCanvas(
            self,
            canvas: TTkCanvas,
            geom: Tuple[int,int,int,int],
            _slice: Tuple[int,int,int,int],
            bound: Tuple[int,int,int,int]) -> None:
        ''' Paints another canvas onto this one inside the given geometry and bounds.

        :param canvas: the source canvas to compose onto this canvas
        :type canvas: :py:class:`TTkCanvas`
        :param geom: destination geometry as ``(x, y, width, height)``
        :type geom: tuple[int, int, int, int]
        :param _slice: reserved slice information for compatibility with callers
        :type _slice: tuple[int, int, int, int]
        :param bound: clipping bounds as ``(x, y, width, height)``
        :type bound: tuple[int, int, int, int]
        '''
        # TTkLog.debug(f"PaintCanvas:{geom=} {bound=} {self._widget._name=} {self._data[0] if self._data else 1234}")
        x, y, w, h  = geom
        bx,by,bw,bh = bound
        cw,ch = self.size()
        # out of bound
        if not self._visible: return
        if not canvas._visible: return
        if canvas._width<=0 or canvas._height<=0: return
        if bx+bw<0 or by+bh<0 or bx>=cw or by>=ch: return
        if x+w<=bx or y+h<=by or bx+bw<=x or by+bh<=y: return

        if (0,0,cw,ch)==geom==bound and (cw,ch)==canvas.size() and not canvas._transparent:
            # fast Copy
            # the canvas match exactly on top of the current one
            for y in range(h):
                self._data[y]   = canvas._data[y].copy()
                self._colors[y] = canvas._colors[y].copy()
            return

        x = min(x,cw-1)
        y = min(y,ch-1)
        w = min(w,cw-x)
        h = min(h,ch-y)

        xoffset = min(max(0,bx-x),canvas._width-1)
        yoffset = min(max(0,by-y),canvas._height-1)
        wslice = min(w if x+w < bx+bw else bx+bw-x,canvas._width)
        hslice = min(h if y+h < by+bh else by+bh-y,canvas._height)

        a, b = x+xoffset, x+wslice
        slice_ab  = slice(a,b)
        slice_off = slice(xoffset,wslice)
        if canvas._transparent:
            for iy in range(yoffset,hslice):
                if None in canvas._data[iy][slice_off]:
                    self._data[y+iy][slice_ab]   = [cca if cca is not None else ccb for cca,ccb in zip(canvas._data[iy][slice_off],self._data[y+iy][slice_ab])]
                else:
                    self._data[y+iy][slice_ab]   = canvas._data[iy][slice_off]
                if None in canvas._colors[iy][slice_off]:
                    self._colors[y+iy][slice_ab] = [cca if cca else ccb for cca,ccb in zip(canvas._colors[iy][slice_off],self._colors[y+iy][slice_ab])]
                else:
                    self._colors[y+iy][slice_ab] = canvas._colors[iy][slice_off]
        else:
            for iy in range(yoffset,hslice):
                self._data[y+iy][slice_ab]   = canvas._data[iy][slice_off]
                self._colors[y+iy][slice_ab] = canvas._colors[iy][slice_off]

        for iy in range(yoffset,hslice):
            # Check the full wide chars on the edge of the two canvasses
            if ((0 <= a < cw) and self._data[y+iy][a]==''):
                self._data[y+iy][a]   = TTkCfg.theme.unicodeWideOverflowCh[0]
                self._colors[y+iy][a] = TTkString.unicodeWideOverflowColor
            if ((0 < b <= cw) and self._data[y+iy][b-1] and TTkString._isWideCharData(self._data[y+iy][b-1])):
                self._data[y+iy][b-1]   = TTkCfg.theme.unicodeWideOverflowCh[1]
                self._colors[y+iy][b-1] = TTkString.unicodeWideOverflowColor
            if ((0 < a <= cw) and self._data[y+iy][a-1] and TTkString._isWideCharData(self._data[y+iy][a-1])):
                self._data[y+iy][a-1]   = TTkCfg.theme.unicodeWideOverflowCh[1]
                self._colors[y+iy][a-1] = TTkString.unicodeWideOverflowColor
            if ((0 <= b < cw) and self._data[y+iy][b]==''):
                self._data[y+iy][b]   = TTkCfg.theme.unicodeWideOverflowCh[0]
                self._colors[y+iy][b] = TTkString.unicodeWideOverflowColor

    def toAnsi(self) -> str:
        ''' Serializes the full canvas content into ANSI text.

        :return: the canvas rendered as newline-separated ANSI escape sequences
        :rtype: str
        '''
        # TTkLog.debug("pushToTerminal")
        ret = ""
        rstColor = str(TTkColor.RST)
        lastcolor = TTkColor.RST
        for y in range(0, self._height):
            ansi = str(lastcolor)
            for x in range(0, self._width):
                ch = self._data[y][x]
                color = self._colors[y][x]
                if color != lastcolor:
                    ansi += str(color-lastcolor)
                    lastcolor = color
                ansi+=ch
            if lastcolor != TTkColor.RST:
                ret += ansi + rstColor + '\n'
            else:
                ret += ansi + '\n'
        return ret

    def pushToTerminal(
            self,
            x: int,
            y: int,
            w: int,
            h: int) -> None:
        ''' Pushes the full canvas to the terminal without diffing.

        :param x: unused compatibility parameter for the destination x coordinate
        :type x: int
        :param y: unused compatibility parameter for the destination y coordinate
        :type y: int
        :param w: unused compatibility parameter for the destination width
        :type w: int
        :param h: unused compatibility parameter for the destination height
        :type h: int
        '''
        # TTkLog.debug("pushToTerminal")
        lastcolor = TTkColor.RST
        for y in range(0, self._height):
            ansi = str(lastcolor)+TTkTerm.Cursor.moveTo(y+1,1)
            for x in range(0, self._width):
                ch = self._data[y][x]
                color = self._colors[y][x]
                if color != lastcolor:
                    ansi += color-lastcolor
                    lastcolor = color
                ansi+=ch
            TTkTerm.push(ansi)

    def cleanBuffers(self) -> None:
        ''' Resets the secondary buffers used by buffered terminal painting.
        '''
        if not self._visible: return
        w,h = self._width, self._height
        baseData = [' ']*w
        baseColors = [TTkColor.RST]*w
        self._bufferedData   = [baseData.copy()   for _ in range(h)]
        self._bufferedColors = [baseColors.copy() for _ in range(h)]

    def pushToTerminalBuffered(
            self,
            x: int,
            y: int,
            w: int,
            h: int) -> None:
        ''' Pushes only changed cells to the terminal using the secondary buffer.

        :param x: unused compatibility parameter for the destination x coordinate
        :type x: int
        :param y: unused compatibility parameter for the destination y coordinate
        :type y: int
        :param w: unused compatibility parameter for the destination width
        :type w: int
        :param h: unused compatibility parameter for the destination height
        :type h: int
        '''
        # TTkLog.debug("pushToTerminal")
        data, colors = self._data, self._colors
        oldData, oldColors = self._bufferedData, self._bufferedColors
        lastcolor = TTkColor.RST
        empty = True
        ansi = ""
        for y,(lda, ldb, lca, lcb) in enumerate(zip(data, oldData, colors, oldColors)):
            for x,(da, db, ca, cb) in enumerate(zip(lda, ldb, lca, lcb)):
                if da==db and ca==cb:
                    if not empty:
                        TTkTerm.push(ansi)
                        empty=True
                    continue
                ch = da
                color = ca
                if empty:
                    ansi = TTkTerm.Cursor.moveTo(y+1,x+1)
                    empty = False
                if color != lastcolor:
                    ansi += color-lastcolor
                    lastcolor = color
                ansi+=ch
            if not empty:
                TTkTerm.push(ansi)
                empty=True
        # Reset the color at the end
        TTkTerm.push(TTkColor.RST-lastcolor)
        # TTkTerm.flush()
        # Switch the buffer
        self._bufferedData, self._bufferedColors = data, colors
        self._data,         self._colors         = oldData, oldColors

    def pushToTerminalBufferedNew(
            self,
            x: int,
            y: int,
            w: int,
            h: int) -> None:
        ''' Pushes buffered terminal updates with run-length compression.

        :param x: unused compatibility parameter for the destination x coordinate
        :type x: int
        :param y: unused compatibility parameter for the destination y coordinate
        :type y: int
        :param w: unused compatibility parameter for the destination width
        :type w: int
        :param h: unused compatibility parameter for the destination height
        :type h: int
        '''
        # TTkLog.debug("pushToTerminal")
        data, colors = self._data, self._colors
        oldData, oldColors = self._bufferedData, self._bufferedColors
        lastcolor = TTkColor.RST
        empty = True
        ansi = ""
        for y,(lda,ldb,lca,lcb) in enumerate(zip(data,oldData,colors,oldColors)):
            count = 0
            chBk = ''
            for x,(da,db,ca,cb) in enumerate(zip(lda,ldb,lca,lcb)):
                if da==db and ca==cb:
                    if not empty:
                        ansi += "" if not chBk else chBk*count if count<=4 else f"{chBk}\033[{count-1}b"
                        TTkTerm.push(ansi)
                        count = 0
                        chBk = ''
                        empty=True
                    continue
                ch = da
                color = ca
                if empty:
                    ansi = ("" if not chBk else chBk*count if count<=4 else f"{chBk}\033[{count-1}b") + TTkTerm.Cursor.moveTo(y+1,x+1)
                    empty = False
                    count = 0
                    chBk = ''
                if color != lastcolor:
                    ansi += ("" if not chBk else chBk*count if count<=4 else f"{chBk}\033[{count-1}b") + str(color-lastcolor)
                    lastcolor = color
                    count = 0
                    chBk = ''
                # "Collect the consecutive characters"
                if ch == chBk:
                    count+=1
                else:
                    ansi += "" if not chBk else chBk*count if count<=4 else f"{chBk}\033[{count-1}b"
                    chBk = ch
                    count=1
                # ansi+=ch
            if not empty:
                ansi += "" if not chBk else chBk*count if count<=4 else f"{chBk}\033[{count-1}b"
                TTkTerm.push(ansi)
                empty=True
        # Reset the color at the end
        TTkTerm.push(TTkColor.RST)
        if getattr(lastcolor, "_link", False):
            TTkTerm.push("\033]8;;\033\\")
        # Switch the buffer
        self._bufferedData, self._bufferedColors = data, colors
        self._data,         self._colors         = oldData, oldColors