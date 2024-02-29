# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['PaintArea','PaintToolKit']

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk


class PaintToolKit(ttk.TTkGridLayout):
    __slots__ = ('_rSelect', '_rPaint', '_lgliph', '_cbFg', '_cbBg', '_bpFg', '_bpBg',
                 '_glyph',
                 #Signals
                 'updatedColor')
    def __init__(self, *args, **kwargs):
        self._glyph = 'X'
        super().__init__(*args, **kwargs)
        self.updatedColor = ttk.pyTTkSignal(ttk.TTkColor)
        self._rSelect = ttk.TTkRadioButton(text='Select '     , maxWidth=10)
        self._rPaint  = ttk.TTkRadioButton(text='Paint  '            )
        self._lgliph   = ttk.TTkLabel(text=""                 , maxWidth=8)
        self._cbFg    = ttk.TTkCheckbox(text="Fg"             , maxWidth= 6)
        self._cbBg    = ttk.TTkCheckbox(text="Bg"                    )
        self._bpFg    = ttk.TTkColorButtonPicker(enabled=False, maxWidth= 6)
        self._bpBg    = ttk.TTkColorButtonPicker(enabled=False,            )
        self.addWidget(self._rSelect ,0,0)
        self.addWidget(self._rPaint  ,1,0)
        self.addWidget(self._lgliph  ,0,1,2,1)
        self.addWidget(self._cbFg    ,0,2)
        self.addWidget(self._cbBg    ,1,2)
        self.addWidget(self._bpFg    ,0,3)
        self.addWidget(self._bpBg    ,1,3)
        self.addItem(ttk.TTkLayout() ,0,4,3,1)

        self._cbFg.toggled.connect(self._bpFg.setEnabled)
        self._cbBg.toggled.connect(self._bpBg.setEnabled)
        self._cbFg.toggled.connect(self._refreshColor)
        self._cbBg.toggled.connect(self._refreshColor)

        self._bpFg.colorSelected.connect(self._refreshColor)
        self._bpBg.colorSelected.connect(self._refreshColor)

        self._refreshColor(emit=False)

    @ttk.pyTTkSlot()
    def _refreshColor(self, emit=True):
        color =self.color()
        self._lgliph.setText(
                ttk.TTkString("Glyph\n '") +
                ttk.TTkString(self._glyph,color) +
                ttk.TTkString("'"))
        if emit:
            self.updatedColor.emit(color)


    @ttk.pyTTkSlot(ttk.TTkString)
    def glyphFromString(self, ch:ttk.TTkString):
        if len(ch)<=0: return
        self._glyph = ch.charAt(0)
        self.setColor(ch.colorAt(0))

    def color(self):
        color = ttk.TTkColor()
        if self._cbFg.checkState() == ttk.TTkK.Checked:
            color += self._bpFg.color().invertFgBg()
        if self._cbBg.checkState() == ttk.TTkK.Checked:
           color += self._bpBg.color()
        return color

    def setColor(self, color:ttk.TTkColor):
        if fg := color.foreground():
            self._cbFg.setCheckState(ttk.TTkK.Checked)
            self._bpFg.setEnabled()
            self._bpFg.setColor(fg.invertFgBg())
        else:
            self._cbFg.setCheckState(ttk.TTkK.Unchecked)
            self._bpFg.setDisabled()

        if bg := color.background():
            self._cbBg.setCheckState(ttk.TTkK.Checked)
            self._bpBg.setEnabled()
            self._bpBg.setColor(bg)
        else:
            self._cbBg.setCheckState(ttk.TTkK.Unchecked)
            self._bpBg.setDisabled()
        self._refreshColor(emit=False)

class PaintArea(ttk.TTkWidget):

    __slots__ = ('_canvasArea', '_canvasSize',
                 '_transparentColor',
                 '_mouseMove',
                 '_glyph', '_glyphColor')

    def __init__(self, *args, **kwargs):
        self._transparentColor = ttk.TTkColor.bg('#FF00FF')
        self._canvasSize = (0,0)
        self._canvasArea = {'data':[],'colors':[]}
        self._glyph = 'X'
        self._glyphColor = ttk.TTkColor.fg("#0000FF")
        self._mouseMove = None
        super().__init__(*args, **kwargs)
        self.resizeCanvas(80,25)
        self.setFocusPolicy(ttk.TTkK.ClickFocus + ttk.TTkK.TabFocus)

    def resizeCanvas(self, w, h):
        self._canvasSize = (w,h)
        self._canvasArea['data']   = (self._canvasArea['data']   + [[] for _ in range(h)])[:h]
        self._canvasArea['colors'] = (self._canvasArea['colors'] + [[] for _ in range(h)])[:h]
        for i in range(h):
            self._canvasArea['data'][i]   = (self._canvasArea['data'][i]   + [' '              for _ in range(w)])[:w]
            self._canvasArea['colors'][i] = (self._canvasArea['colors'][i] + [ttk.TTkColor.RST for _ in range(w)])[:w]
        self.update()

    def mouseMoveEvent(self, evt) -> bool:
        x,y = evt.x, evt.y
        w,h = self._canvasSize
        if 0<=x<w and 0<=y<h:
            self._mouseMove = (x, y)
            self.update()
            return True
        self._mouseMove = None
        self.update()
        return super().mouseMoveEvent(evt)

    def mouseDragEvent(self, evt) -> bool:
        if self._placeGlyph(evt.x, evt.y):
            return True
        return super().mouseDragEvent(evt)

    def mousePressEvent(self, evt) -> bool:
        if self._placeGlyph(evt.x, evt.y):
            return True
        return super().mousePressEvent(evt)

    @ttk.pyTTkSlot(ttk.TTkString)
    def glyphFromString(self, ch:ttk.TTkString):
        if len(ch)<=0: return
        self._glyph = ch.charAt(0)
        self._glyphColor = ch.colorAt(0)

    def glyph(self):
        return self._glyph
    def setGlyph(self, glyph):
        if len(glyph) <= 0: return
        if type(glyph)==str:
            self._glyph = glyph[0]
        if type(glyph)==ttk.TTkString:
            self._glyph = glyph.charAt(0)
            self._glyphColor = glyph.colorAt(0)

    def glyphColor(self):
        return self._glyphColor
    def setGlyphColor(self, color):
        self._glyphColor = color

    def _placeGlyph(self,x,y):
        self._mouseMove = None
        w,h = self._canvasSize
        data = self._canvasArea['data']
        colors = self._canvasArea['colors']
        if 0<=x<w and 0<=y<h:
            data[y][x] = self._glyph
            colors[y][x] = self._glyphColor
            self.update()
            return True
        return False

    def paintEvent(self, canvas: ttk.TTkCanvas):
        pw,ph = self._canvasSize
        cw,ch = canvas.size()
        w=min(cw,pw)
        h=min(ch,ph)
        data = self._canvasArea['data']
        colors = self._canvasArea['colors']
        tc = self._transparentColor
        for y in range(h):
            canvas._data[y][0:w] = data[y][0:w]
            for x in range(w):
                c = colors[y][x]
                canvas._colors[y][x] = c if c._bg else c+tc
        if self._mouseMove:
            x,y = self._mouseMove
            gc = self._glyphColor
            canvas._data[y][x] = self._glyph
            canvas._colors[y][x] = gc if gc._bg else gc+tc