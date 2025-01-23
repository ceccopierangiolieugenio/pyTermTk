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

__all__ = ['Palette']

import TermTk as ttk

_defaultPalette = [
    [( 64,  0,  0),(102,  0,  0),(140,  0,  0),(178,  0,  0),(217,  0,  0),(255,  0,  0),(255, 51, 51),(255,102,102),  (  0, 48, 64),(  0, 77,102),(  0,105,140),(  0,134,178),(  0,163,217),(  0,191,255),( 51,204,255),(102,217,255)],
    [( 64, 16,  0),(102, 26,  0),(140, 35,  0),(178, 45,  0),(217, 54,  0),(255, 64,  0),(255,102, 51),(255,140,102),  (  0, 32, 64),(  0, 51,102),(  0, 70,140),(  0, 89,178),(  0,108,217),(  0,128,255),( 51,153,255),(102,178,255)],
    [( 64, 32,  0),(102, 51,  0),(140, 70,  0),(178, 89,  0),(217,108,  0),(255,128,  0),(255,153, 51),(255,178,102),  (  0,  0, 64),(  0,  0,102),(  0,  0,140),(  0,  0,178),(  0,  0,217),(  0,  0,255),( 51, 51,255),(102,102,255)],
    [( 64, 48,  0),(102, 77,  0),(140,105,  0),(178,134,  0),(217,163,  0),(255,191,  0),(255,204, 51),(255,217,102),  ( 16,  0, 64),( 26,  0,102),( 35,  0,140),( 45,  0,178),( 54,  0,217),( 64,  0,255),(102, 51,255),(140,102,255)],
    [( 64, 64,  0),(102,102,  0),(140,140,  0),(178,178,  0),(217,217,  0),(255,255,  0),(255,255, 51),(255,255,102),  ( 32,  0, 64),( 51,  0,102),( 70,  0,140),( 89,  0,178),(108,  0,217),(128,  0,255),(153, 51,255),(178,102,255)],
    [( 48, 64,  0),( 77,102,  0),(105,140,  0),(134,178,  0),(163,217,  0),(191,255,  0),(204,255, 51),(217,255,102),  ( 48,  0, 64),( 77,  0,102),(105,  0,140),(134,  0,178),(163,  0,217),(191,  0,255),(204, 51,255),(217,102,255)],
    [( 32, 64,  0),( 51,102,  0),( 70,140,  0),( 89,178,  0),(108,217,  0),(128,255,  0),(153,255, 51),(178,255,102),  ( 64,  0, 64),(102,  0,102),(140,  0,140),(178,  0,178),(217,  0,217),(255,  0,255),(255, 51,255),(255,102,255)],
    [(  0, 64,  0),(  0,102,  0),(  0,140,  0),(  0,178,  0),(  0,217,  0),(  0,255,  0),( 51,255, 51),(102,255,102),  ( 64,  0, 48),(102,  0, 77),(140,  0,105),(178,  0,134),(217,  0,163),(255,  0,191),(255, 51,204),(255,102,217)],
    [(  0, 64, 32),(  0,102, 51),(  0,140, 70),(  0,178, 89),(  0,217,108),(  0,255,128),( 51,255,153),(102,255,178),  ( 64,  0, 32),(102,  0, 51),(140,  0, 70),(178,  0, 89),(217,  0,108),(255,  0,128),(255, 51,153),(255,102,178)],
    [(  0, 64, 48),(  0,102, 77),(  0,140,105),(  0,178,134),(  0,217,163),(  0,255,191),( 51,255,204),(102,255,217),  ( 64,  0, 16),(102,  0, 26),(140,  0, 35),(178,  0, 45),(217,  0, 54),(255,  0, 64),(255, 51,102),(255,102,140)],
    [(  0, 64, 64),(  0,102,102),(  0,140,140),(  0,178,178),(  0,217,217),(  0,255,255),( 51,255,255),(102,255,255),  ( 26, 20, 13),( 51, 41, 26),( 77, 61, 38),(102, 82, 51),(128,102, 64),(158,134,100),(191,171,143),(222,211,195)],
    [(  0,  0,  0),( 19, 19, 19),( 39, 39, 39),( 58, 58, 58),( 78, 78, 78),( 98, 98, 98),(117,117,117),(137,137,137),  (156,156,156),(176,176,176),(196,196,196),(215,215,215),(235,235,235),(255,255,255),(  0,  0,  0),(  0,  0,  0)]]

class Palette(ttk.TTkWidget):
    __slots__ = ('_bg', '_fg', '_mouseMove', '_palette',
                 '_enabledFg', '_enabledBg',
                 #signals
                 'colorSelected')
    def __init__(self, *args, **kwargs):
        self.colorSelected = ttk.pyTTkSignal(ttk.TTkColor)
        self._fg = (5,3)
        self._bg = (9,2)
        self._enabledFg = True
        self._enabledBg = True
        self._mouseMove = None
        self.setPalette(_defaultPalette)
        super().__init__(*args, **kwargs)
        self.setFocusPolicy(ttk.TTkK.ClickFocus)

    def setPalette(self, palette):
        self._palette = []
        for row in palette:
            colors = []
            for r,g,b in row:
                colors.append((
                        ttk.TTkColor.fg(f"#{r<<16|g<<8|b:06x}"),
                        ttk.TTkColor.bg(f"#{r<<16|g<<8|b:06x}")))
            self._palette.append(colors)
        self.update()

    def color(self):
        palette = self._palette
        fx,fy = self._fg
        bx,by = self._bg
        fg = palette[fy][fx][0]
        bg = palette[by][bx][1]
        if self._enabledFg and self._enabledBg:
            return fg+bg
        elif self._enabledFg:
            return fg
        elif self._enabledBg:
            return bg
        else:
            return ttk.TTkColor.RST

    ttk.pyTTkSlot(ttk.TTkColor)
    def setColor(self, color:ttk.TTkColor) -> None:
        fg = color.foreground()
        bg = color.background()
        self.enableFg(fg!=ttk.TTkColor.RST)
        self.enableBg(bg!=ttk.TTkColor.RST)
        def _getPos(col):
            for y,row in enumerate(self._palette):
                for x,c in enumerate(row):
                    if c[0] == col or c[1] == col:
                        return x,y
            return None
        pw, ph = len(self._palette[0]),len(self._palette)
        if fg!=ttk.TTkColor.RST:
            if (pos:=_getPos(fg)) != None:
                self._fg = pos
            else:
                self._fg = (pw-2,ph-1)
                self._palette[ph-1][pw-2] = (fg,fg.invertFgBg())

        if bg!=ttk.TTkColor.RST:
            if (pos:=_getPos(bg)) != None:
                self._bg = pos
            else:
                self._bg = (pw-1,ph-1)
                self._palette[ph-1][pw-1] = (bg.invertFgBg(),bg)
        self.update()

    @ttk.pyTTkSlot(bool)
    def enableFg(self, enable=True):
        self._enabledFg = enable
        self.colorSelected.emit(self.color())
        self.update()

    @ttk.pyTTkSlot(bool)
    def enableBg(self, enable=True):
        self._enabledBg = enable
        self.colorSelected.emit(self.color())
        self.update()

    def mousePressEvent(self, evt) -> bool:
        x,y = evt.x, evt.y
        self._mouseMove = None
        if 0<=x<32 and 0<=y<12:
            if evt.key == ttk.TTkK.RightButton:
                self._bg = (x//2,y)
            elif evt.key == ttk.TTkK.LeftButton:
                self._fg = (x//2,y)
            self.colorSelected.emit(self.color())
            self.update()
            return True
        self.update()
        return super().mousePressEvent(evt)

    def leaveEvent(self, evt):
        self._mouseMove = None
        self.update()
        return super().leaveEvent(evt)

    def mouseMoveEvent(self, evt) -> bool:
        x,y = evt.x, evt.y
        if 0<=x<32 and 0<=y<12:
            self._mouseMove = (x//2, y)
            self.update()
            return True
        self._mouseMove = None
        self.update()
        return super().mouseMoveEvent(evt)

    def paintEvent(self, canvas: ttk.TTkCanvas):
        palette = self._palette
        for y,row in enumerate(palette):
            for x,col in enumerate(row):
                canvas.drawText(pos=(x*2,y),text='  ',color=col[1])
        # Draw Mouse Move
        if self._mouseMove:
            x,y = self._mouseMove
            r,g,b = palette[y][x][0].fgToRGB()
            chc = ttk.TTkColor.fg('#000000') if r+b+g > (100*3) else ttk.TTkColor.fg('#FFFFFF')
            color = palette[y][x][1] + chc
            canvas.drawText(pos=(x*2,y), text="◀▶", color=color)
        # Draw FG Ref
        x,y = self._fg
        r,g,b = palette[y][x][0].fgToRGB()
        if self._enabledFg:
            chc = ttk.TTkColor.fg('#000000') if r+b+g > (128*3) else ttk.TTkColor.fg('#FFFFFF')
        else:
            chc = ttk.TTkColor.fg('#666666') if r+b+g > (128*3) else ttk.TTkColor.fg('#999999')
        color = palette[y][x][1] + chc
        canvas.drawChar(pos=(x*2,y), char="F", color=color)
        # Draw BG ref
        x,y = self._bg
        r,g,b = palette[y][x][0].fgToRGB()
        if self._enabledBg:
            chc = ttk.TTkColor.fg('#000000') if r+b+g > (128*3) else ttk.TTkColor.fg('#FFFFFF')
        else:
            chc = ttk.TTkColor.fg('#666666') if r+b+g > (128*3) else ttk.TTkColor.fg('#999999')
        color = palette[y][x][1] + chc
        canvas.drawChar(pos=(x*2+1,y), char="B", color=color)

