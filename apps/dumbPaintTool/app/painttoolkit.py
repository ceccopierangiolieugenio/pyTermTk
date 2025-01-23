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

import os

import TermTk as ttk

from .paintarea import *
from .glbls     import glbls
from .const     import ToolType

class PaintToolKit(ttk.TTkContainer):
    __slots__ = ('_rSelect', '_rPaint', '_lgliph',
                 '_btnPick',
                 '_cbFg', '_cbBg',
                 '_bpFg', '_bpBg', '_bpDef',
                 '_sbDx','_sbDy','_sbDw','_sbDh',
                 '_sbLx','_sbLy','_sbLw','_sbLh',
                 #Signals
                 'updatedTrans')
    def __init__(self, *args, **kwargs):
        ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../tui/paintToolKit.tui.json"),self)
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

        self._btnPick = self.getWidgetByName("btnPick")

        self._bpDef.setColor(ttk.TTkColor.bg('#FF00FF'))
        self._cbFg.toggled.connect(self._refreshColor)
        self._cbBg.toggled.connect(self._refreshColor)

        self._bpFg.colorSelected.connect(self._refreshColor)
        self._bpBg.colorSelected.connect(self._refreshColor)
        self._bpDef.colorSelected.connect(self.updatedTrans.emit)

        glbls.brush.glyphChanged.connect(  self._refreshColor)
        glbls.brush.colorChanged.connect(  self.setColor)
        glbls.layers.changed.connect(      self._layerChanged)
        glbls.layers.layerSelected.connect(self._layerChanged)

        # self._sbDx
        # self._sbDy
        # self._sbDw
        # self._sbDh
        self._sbLx.valueChanged.connect(self._pushLayerValues)
        self._sbLy.valueChanged.connect(self._pushLayerValues)
        self._sbLw.valueChanged.connect(self._pushLayerValues)
        self._sbLh.valueChanged.connect(self._pushLayerValues)

        self._refreshColor()

        @ttk.pyTTkSlot()
        def _pick():
            ttType = glbls.brush.toolType() & ~ToolType.PICKMASK
            glbls.brush.setToolType( ttType | ToolType.PICKGLYPH )

        self._btnPick.clicked.connect(_pick)

    @ttk.pyTTkSlot()
    def _pushLayerValues(self):
        if not (layer := glbls.layers.selected()): return
        nlx = self._sbLx.value()
        nly = self._sbLy.value()
        nlw = self._sbLw.value()
        nlh = self._sbLh.value()
        layer.move(nlx,nly)
        layer.superResize(nlx,nly,nlw,nlh)

    @ttk.pyTTkSlot()
    def _layerChanged(self):
        if not (layer := glbls.layers.selected()): return
        self.updateLayer(layer)

    @ttk.pyTTkSlot(CanvasLayer)
    def updateLayer(self, layer:CanvasLayer):
        lx,ly = layer.pos()
        lw,lh = layer.size()
        self._sbLx.valueChanged.disconnect(self._pushLayerValues)
        self._sbLy.valueChanged.disconnect(self._pushLayerValues)
        self._sbLw.valueChanged.disconnect(self._pushLayerValues)
        self._sbLh.valueChanged.disconnect(self._pushLayerValues)
        self._sbLx.setValue(lx)
        self._sbLy.setValue(ly)
        self._sbLw.setValue(lw)
        self._sbLh.setValue(lh)
        self._sbLx.valueChanged.connect(self._pushLayerValues)
        self._sbLy.valueChanged.connect(self._pushLayerValues)
        self._sbLw.valueChanged.connect(self._pushLayerValues)
        self._sbLh.valueChanged.connect(self._pushLayerValues)

    @ttk.pyTTkSlot()
    def _refreshColor(self):
        glyph = glbls.brush.glyph()
        color = self.color()
        self._lgliph.setText(
                ttk.TTkString("Glyph: '") +
                ttk.TTkString(glyph,color) +
                ttk.TTkString("'"))
        glbls.brush.setColor(color)

    def color(self):
        color = ttk.TTkColor()
        if self._cbFg.checkState() == ttk.TTkK.Checked:
            color += self._bpFg.color()
        if self._cbBg.checkState() == ttk.TTkK.Checked:
           color += self._bpBg.color()
        return color

    @ttk.pyTTkSlot(ttk.TTkColor)
    def setColor(self, color:ttk.TTkColor):
        if color.hasForeground():
            self._cbFg.setCheckState(ttk.TTkK.Checked)
            self._bpFg.setEnabled()
            self._bpFg.setColor(color.foreground())
        else:
            self._cbFg.setCheckState(ttk.TTkK.Unchecked)
            self._bpFg.setDisabled()

        if color.hasBackground():
            self._cbBg.setCheckState(ttk.TTkK.Checked)
            self._bpBg.setEnabled()
            self._bpBg.setColor(color.background())
        else:
            self._cbBg.setCheckState(ttk.TTkK.Unchecked)
            self._bpBg.setDisabled()
        self._refreshColor()
