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

__all__ = ['']

import collections
import unicodedata

from TermTk.TTkCore.canvas import TTkCanvas

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkGui.clipboard import TTkClipboard
from TermTk.TTkGui.textwrap1 import TTkTextWrap
from TermTk.TTkGui.textcursor import TTkTextCursor
from TermTk.TTkGui.textdocument import TTkTextDocument
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView, TTkAbstractScrollViewGridLayout
from TermTk.TTkWidgets.widget import TTkWidget

from .terminal_screen_CSI import _TTkTerminalScreen_CSI
from .terminal_screen_C1  import _TTkTerminalScreen_C1

class _TTkTerminalScreen(_TTkTerminalScreen_CSI, _TTkTerminalScreen_C1):
    __slots__ = ('_lines', '_terminalCursor',
                 '_scrollingRegion',
                 '_bufferSize', '_bufferedLines',
                 '_w', '_h', '_color', '_canvas',
                 '_last',
                 # Signals
                 'bell'
                 )
    def __init__(self, w=80, h=24, bufferSize=1000, color=TTkColor.RST) -> None:
        self.bell = pyTTkSignal()
        self._w = w
        self._h = h
        self._last = None
        self._bufferSize = bufferSize
        self._bufferedLines = collections.deque(maxlen=bufferSize)
        self._terminalCursor = (0,0)
        self._scrollingRegion = (0,h)
        self._color = color
        self._canvas = TTkCanvas(width=w, height=h)

    def color(self):
        return self._color

    def setColor(self, color):
        self._color = color

    def getCursor(self):
        return self._terminalCursor

    def resize(self, w, h):
        ow, oh = self._w, self._h
        self._w, self._h = w, h
        st,sb = self._scrollingRegion
        # if oh <= h: # Terminal height decreasing
        #     sb = min(h,oh)
        # else:# Terminal height increasing
        #     sb = h-oh+sb
        # self._scrollingRegion = (st,sb)
        self._scrollingRegion = (0,h)
        newCanvas = TTkCanvas(width=w, height=h)
        s = (0,0,w,h)
        newCanvas.paintCanvas(self._canvas,s,s,s)

        self._canvas = newCanvas
        x,y = self._terminalCursor
        self._terminalCursor = (min(x,w-1),min(y,h-1))

    def _pushTxt(self, txt:str, irm:bool=False):
        x,y = self._terminalCursor
        w,h = self._w, self._h
        st,sb = self._scrollingRegion
        self._last = txt[-1] if txt else None

        for bi, tout in enumerate(txt.split('\a')): # grab the bells
            if bi:
                self.bell.emit()

            # I check the size of each char in order to draw
            # it in the correct position
            for ch in tout:
                if ord(ch) < 0x20:
                    # TTkLog.error(f"Unhandled ASCII: 0x{ord(ch):02x}")
                    continue
                l = TTkString._getWidthText(ch)
                # Scroll up if we are at the right border
                if l+x > w:
                    x=0
                    y+=1
                    if y >= sb:
                        self._CSI_S_SU(y-sb+1, None) # scroll up
                        y=sb-1
                    self._terminalCursor = (x,y)
                if l==1:   # push normal char
                    if irm:
                        self._canvas._data[y][x:x] = [ch]
                        self._canvas._colors[y][x:x] = [self._color]
                        # self._canvas._data[y].insert(x,ch)
                        # self._canvas._colors[y].insert(x,self._color)
                        self._canvas._data[y].pop()
                        self._canvas._colors[y].pop()
                    else:
                        self._canvas._data[y][x]   = ch
                        self._canvas._colors[y][x] = self._color
                elif l > 1: # push wide char
                    if irm:
                        self._canvas._data[y][x:x] = [ch,'']
                        self._canvas._colors[y][x:x] = [self._color,self._color]
                        # self._canvas._data[y].insert(x,ch)
                        # self._canvas._colors[y].insert(x,self._color)
                        self._canvas._data[y].pop()
                        self._canvas._data[y].pop()
                        self._canvas._colors[y].pop()
                        self._canvas._colors[y].pop()
                    else:
                        self._canvas._data[y][x]   = ch
                        self._canvas._data[y][x+1] = ''
                        self._canvas._colors[y][x]   = self._color
                        self._canvas._colors[y][x+1] = self._color
                else: # l==0 # push zero sized char
                    if x>0 and self._canvas._data[y][x-1] != '':
                        self._canvas._data[y][x-1]  += ch
                    elif x>1:
                        self._canvas._data[y][x-2]  += ch
                x+=l
                self._terminalCursor = (x+l,y)
            self._terminalCursor = (x,y)

    def pushLine(self, line:str, irm:bool=False):
        if not line: return
        w,h = self._w, self._h
        st,sb = self._scrollingRegion

        lines = line.split('\n')
        for i,l in enumerate(lines):
            if i:
                x,y = self._terminalCursor
                y+=1
                if y >= sb:
                    self._CSI_S_SU(y-sb+1, None) # scroll up
                    y=sb-1
                self._terminalCursor = (x,y)
            ls = l.split('\r')
            for ii,ll in enumerate(ls):
                if ii:
                    x,y = self._terminalCursor
                    self._terminalCursor = (0,y)
                lls = ll.split('\b') # 0x08 = Backspace
                for iii,lll in enumerate(lls):
                    if iii:
                        x,y = self._terminalCursor
                        x = max(0,x-1)
                        self._terminalCursor = (x,y)
                    self._pushTxt(lll,irm)

    def paintEvent(self, canvas: TTkCanvas, w:int, h:int, ox:int=0, oy:int=0) -> None:
        w,h = self._w, self._h
        s = (0,0,w,h)
        canvas.paintCanvas(self._canvas,s,s,s)
        # TTkLog.debug("Paint")
