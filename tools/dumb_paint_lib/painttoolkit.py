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

__all__ = ['PaintToolKit']

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .paintarea import *

class PaintToolKit(ttk.TTkContainer):
    __slots__ = ('_rSelect', '_rPaint', '_lgliph',
                 '_cbFg', '_cbBg',
                 '_bpFg', '_bpBg', '_bpDef',
                 '_sbDx','_sbDy','_sbDw','_sbDh',
                 '_sbLx','_sbLy','_sbLw','_sbLh',
                 '_glyph',
                 #Signals
                 'updatedColor', 'updatedTrans')
    def __init__(self, *args, **kwargs):
        ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"tui/paintToolKit.tui.json"),self)
        self._glyph = 'X'
        self.updatedColor = ttk.pyTTkSignal(ttk.TTkColor)
        self.updatedTrans = ttk.pyTTkSignal(ttk.TTkColor)
        self._lgliph  = self.getWidgetByName("lglyph")
        self._cbFg    = self.getWidgetByName("cbFg")
        self._cbBg    = self.getWidgetByName("cbBg")
        self._bpFg    = self.getWidgetByName("bpFg")
        self._bpBg    = self.getWidgetByName("bpBg")
        self._bpDef   = self.getWidgetByName("bpDef")

        self._sbDx = self.getWidgetByName("sbDx")
        self._sbDy = self.getWidgetByName("sbDy")
        self._sbDw = self.getWidgetByName("sbDw")
        self._sbDh = self.getWidgetByName("sbDh")
        self._sbLx = self.getWidgetByName("sbLx")
        self._sbLy = self.getWidgetByName("sbLy")
        self._sbLw = self.getWidgetByName("sbLw")
        self._sbLh = self.getWidgetByName("sbLh")

        self._bpDef.setColor(ttk.TTkColor.bg('#FF00FF'))
        self._cbFg.toggled.connect(self._refreshColor)
        self._cbBg.toggled.connect(self._refreshColor)

        self._bpFg.colorSelected.connect(self._refreshColor)
        self._bpBg.colorSelected.connect(self._refreshColor)
        self._bpDef.colorSelected.connect(self.updatedTrans.emit)

        self._refreshColor(emit=False)

    @ttk.pyTTkSlot(CanvasLayer)
    def updateLayer(self, layer:CanvasLayer):
        lx,ly = layer.pos()
        lw,lh = layer.size()
        self._sbLx.setValue(lx)
        self._sbLy.setValue(ly)
        self._sbLw.setValue(lw)
        self._sbLh.setValue(lh)

    @ttk.pyTTkSlot()
    def _refreshColor(self, emit=True):
        color =self.color()
        self._lgliph.setText(
                ttk.TTkString("Glyph: '") +
                ttk.TTkString(self._glyph,color) +
                ttk.TTkString("'"))
        if emit:
            self.updatedColor.emit(color)

    @ttk.pyTTkSlot(ttk.TTkString)
    def glyphFromString(self, ch:ttk.TTkString):
        if len(ch)<=0: return
        self._glyph = ch.charAt(0)
        self._refreshColor()
        # self.setColor(ch.colorAt(0))

    def color(self):
        color = ttk.TTkColor()
        if self._cbFg.checkState() == ttk.TTkK.Checked:
            color += self._bpFg.color().invertFgBg()
        if self._cbBg.checkState() == ttk.TTkK.Checked:
           color += self._bpBg.color()
        return color

    @ttk.pyTTkSlot(ttk.TTkColor)
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
