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

__all__ = ['Brush']

import TermTk as ttk

from ..const import ToolType

# Due to the variety of widgets that depends
# on the brush state, I am defining this class
# with all the signals required to broadcast
# all the changes to the widgets that require it
class Brush():
    __slots__ = ['_color','_glyph','_area','_toolType',
                 '_fgEnabled','_bgEnabled','_glyphEnabled',
                 '_transparentArea',
                 #signals
                 'colorChanged', 'glyphChanged', 'areaChanged',
                 'toolTypeChanged',
                 'fgEnabledChanged','bgEnabledChanged','glyphEnabledChanged'
                 ]
    def __init__(self) -> None:
        self.fgEnabledChanged    = ttk.pyTTkSignal(bool)
        self.bgEnabledChanged    = ttk.pyTTkSignal(bool)
        self.glyphEnabledChanged = ttk.pyTTkSignal(bool)
        self.areaChanged      = ttk.pyTTkSignal(ttk.TTkString)
        self.colorChanged     = ttk.pyTTkSignal(ttk.TTkColor)
        self.glyphChanged     = ttk.pyTTkSignal(str)
        self.toolTypeChanged  = ttk.pyTTkSignal(ToolType)

        self._area  : ttk.TTkString = ttk.TTkString()
        self._color : ttk.TTkColor  = ttk.TTkColor.RST
        self._glyph : str = 'X'
        self._fgEnabled:     bool= True
        self._bgEnabled:     bool= True
        self._glyphEnabled:  bool= True
        self._toolType: ToolType = ToolType.BRUSH | ToolType.GLYPH

    def toolType(self) -> ToolType:
        return self._toolType

    def setToolType(self, ty:ToolType) -> None:
        if self._toolType == ty: return
        self._toolType = ty
        self.toolTypeChanged.emit(ty)

    def color(self) -> ttk.TTkColor:
        return self._color

    def setColor(self, color:ttk.TTkColor) -> None:
        if self._color == color: return
        self._color = color
        self.colorChanged.emit(color)

    def glyph(self) -> str:
        return self._glyph

    def setGlyph(self, glyph:str) -> None:
        if self._glyph == glyph: return
        self._glyph = glyph
        self.glyphChanged.emit(glyph)

    def area(self) -> ttk.TTkString:
        return self._area

    def setArea(self, area:ttk.TTkString) -> None:
        if self._area.toAnsi() == area.toAnsi(): return
        self._area = area
        self.areaChanged.emit(area)

    def glyphEnabled(self) -> bool:
        return self._glyphEnabled

    def setFgEnabled(self, enabled:bool) -> None:
        if self._fgEnabled == enabled: return
        self._fgEnabled = enabled
        self.fgEnabledChanged.emit(enabled)

    def fgEnabled(self) -> bool:
        return self._fgEnabled

    def setBgEnabled(self, enabled:bool) -> None:
        if self._bgEnabled == enabled: return
        self._bgEnabled = enabled
        self.bgEnabledChanged.emit(enabled)

    def bgEnabled(self) -> bool:
        return self._bgEnabled

    def setGlyphEnabled(self, enabled:bool) -> None:
        if self._glyphEnabled == enabled: return
        self._glyphEnabled = enabled
        self.glyphEnabledChanged.emit(enabled)
