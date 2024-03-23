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

__all__ = ['ToolsPanel']

import sys, os, json

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .canvaslayer  import CanvasLayer
from .palette      import Palette

class ToolsPanel(ttk.TTkVBoxLayout):
    __slots__ = ('_palette',
                 '_glyph','_color',
                 '_la_brush_g', '_ta_brush_a'
                 # Signals
                 'toolSelected','areaChanged')
    def __init__(self, *args, **kwargs):
        self.pickArea = ttk.pyTTkSignal()
        self.areaChanged = ttk.pyTTkSignal(ttk.TTkString)
        self.toolSelected = ttk.pyTTkSignal(CanvasLayer.Tool)
        self._color = ttk.TTkColor.RST
        super().__init__(*args, **kwargs)
        self._palette  = Palette(maxHeight=12)
        self.addWidget(self._palette)

        # Layout for the toggle buttons
        lToggleFgBg = ttk.TTkHBoxLayout()
        cb_p_fg = ttk.TTkCheckbox(text="-FG-", checked=ttk.TTkK.Checked)
        cb_p_bg = ttk.TTkCheckbox(text="-BG-", checked=ttk.TTkK.Checked)
        lToggleFgBg.addWidgets([cb_p_fg,cb_p_bg])
        lToggleFgBg.addItem(ttk.TTkLayout())
        cb_p_fg.toggled.connect(self._palette.enableFg)
        cb_p_bg.toggled.connect(self._palette.enableBg)
        self.addItem(lToggleFgBg)

        # Toolset
        lTools = ttk.TTkGridLayout()
        ra_move   = ttk.TTkRadioButton(radiogroup="tools", text="Sel/Move",  enabled=True)
        ra_select = ttk.TTkRadioButton(radiogroup="tools", text="Select",enabled=False)
        ra_brush  = ttk.TTkRadioButton(radiogroup="tools", text="Brush", checked=True)
        ra_line   = ttk.TTkRadioButton(radiogroup="tools", text="Line",  enabled=False)
        ra_rect   = ttk.TTkRadioButton(radiogroup="tools", text="Rect")
        ra_oval   = ttk.TTkRadioButton(radiogroup="tools", text="Oval",  enabled=False)

        ra_rect_f = ttk.TTkRadioButton(radiogroup="toolsRectFill", text="Fill" , enabled=False, checked=True)
        ra_rect_e = ttk.TTkRadioButton(radiogroup="toolsRectFill", text="Empty", enabled=False)

        ra_brush_g = ttk.TTkRadioButton(radiogroup="toolsBrush", text="Glyph", enabled=True, checked=True)
        ra_brush_a = ttk.TTkRadioButton(radiogroup="toolsBrush", text="Area",  enabled=True )

        cb_move_r = ttk.TTkCheckbox(text="Resize", enabled=False)

        la_brush_g = ttk.TTkLabel(   maxHeight=1, minHeight=1)
        btn_pick_a = ttk.TTkButton(  maxHeight=1, minHeight=1, visible=False, text='Pick Area')
        cb_trans_a = ttk.TTkCheckbox(maxHeight=1, minHeight=1, visible=False, text='Transparent')
        ta_brush_a = ttk.TTkTextEdit(                          visible=False, lineNumber=True, readOnly=False)

        spacer = ttk.TTkSpacer()
        # spacer = ttk.TTkFrame(border=True)

        self._la_brush_g = la_brush_g
        self._ta_brush_a = ta_brush_a

        @ttk.pyTTkSlot()
        def _checkTools():
            tool = CanvasLayer.Tool.BRUSH
            if ra_move.isChecked():
                tool  = CanvasLayer.Tool.MOVE
                if cb_move_r.isChecked():
                    tool |= CanvasLayer.Tool.RESIZE
            elif ra_brush.isChecked():
                tool = CanvasLayer.Tool.BRUSH
                if ra_brush_g.isChecked():
                    tool |= CanvasLayer.Tool.GLYPH
                else:
                    tool |= CanvasLayer.Tool.AREA
                    if cb_trans_a.isChecked():
                        tool |= CanvasLayer.Tool.TRANSPARENT
            elif ra_rect.isChecked():
                if ra_rect_e.isChecked():
                    tool = CanvasLayer.Tool.RECTEMPTY
                else:
                    tool = CanvasLayer.Tool.RECTFILL

            spacer.show()
            la_brush_g.hide()
            cb_trans_a.hide()
            btn_pick_a.hide()
            ta_brush_a.hide()
            if tool & CanvasLayer.Tool.GLYPH:
                la_brush_g.show()
                spacer.show()
            elif tool & CanvasLayer.Tool.AREA:
                cb_trans_a.show()
                btn_pick_a.show()
                ta_brush_a.show()

            self.toolSelected.emit(tool)
            lTools.update()
            self.update()

        @ttk.pyTTkSlot(bool)
        def _emitTool(checked):
            if not checked: return
            _checkTools()

        @ttk.pyTTkSlot()
        def _pick():
            self.toolSelected.emit(
                CanvasLayer.Tool.BRUSH |
                CanvasLayer.Tool.AREA |
                CanvasLayer.Tool.PICK )

        btn_pick_a.clicked.connect(_pick)

        ra_rect.toggled.connect(ra_rect_f.setEnabled)
        ra_rect.toggled.connect(ra_rect_e.setEnabled)
        ra_move.toggled.connect(cb_move_r.setEnabled)
        ra_brush.toggled.connect(ra_brush_g.setEnabled)
        ra_brush.toggled.connect(ra_brush_a.setEnabled)
        # ra_brush_g.toggled.connect(la_brush_g.setVisible)
        # ra_brush_a.toggled.connect(btn_pick_a.setVisible)
        # ra_brush_a.toggled.connect(ta_brush_a.setVisible)
        ra_brush_g.toggled.connect(self.update)
        ra_brush_a.toggled.connect(self.update)

        ra_move.toggled.connect(   _emitTool)
        ra_select.toggled.connect( _emitTool)
        ra_brush.toggled.connect(  _emitTool)
        ra_line.toggled.connect(   _emitTool)
        ra_rect.toggled.connect(   _emitTool)
        ra_rect_f.toggled.connect( _emitTool)
        ra_rect_e.toggled.connect( _emitTool)
        ra_oval.toggled.connect(   _emitTool)
        ra_brush_g.toggled.connect(_emitTool)
        ra_brush_a.toggled.connect(_emitTool)
        cb_trans_a.toggled.connect(_checkTools)
        cb_move_r.toggled.connect( _checkTools)

        ta_brush_a.textChanged.connect(lambda : self.areaChanged.emit(ta_brush_a.toRawText()))

        lTools.addWidget(ra_move    ,0,0)
        lTools.addWidget(cb_move_r  ,0,1)
        lTools.addWidget(ra_select  ,1,0)
        lTools.addWidget(ra_brush   ,2,0)
        lTools.addWidget(ra_brush_g ,2,1)
        lTools.addWidget(ra_brush_a ,2,2)
        lTools.addWidget(ra_line    ,3,0)
        lTools.addWidget(ra_rect    ,4,0)
        lTools.addWidget(ra_rect_f  ,4,1)
        lTools.addWidget(ra_rect_e  ,4,2)
        lTools.addWidget(ra_oval    ,5,0)
        lTools.addWidget(la_brush_g ,6,0)
        lTools.addWidget(btn_pick_a ,7,2,1,1)
        lTools.addWidget(cb_trans_a ,7,0,1,2)
        lTools.addWidget(ta_brush_a ,8,0,1,3)
        lTools.addWidget(spacer     ,9,0,1,3)

        self.addItem(lTools)

        self._palette.colorSelected.connect(self.setColor)

        # brush
        # line
        # rettangle [empty,fill]
        # oval [empty,fill]

    @ttk.pyTTkSlot(ttk.TTkString)
    def glyphFromString(self, ch:ttk.TTkString):
        if len(ch)<=0: return
        self._glyph = ch.charAt(0)
        self._refreshColor()

    @ttk.pyTTkSlot()
    def _refreshColor(self):
        color =self._color
        self._la_brush_g.setText(
                ttk.TTkString("Glyph: '") +
                ttk.TTkString(self._glyph,color) +
                ttk.TTkString("'"))

    @ttk.pyTTkSlot(ttk.TTkColor)
    def setColor(self, color:ttk.TTkColor):
        self._color = color
        self._refreshColor()

    @ttk.pyTTkSlot(CanvasLayer)
    def setAreaLayer(self, layer:CanvasLayer):
        self._ta_brush_a.setText(layer.toTTkString())

    def palette(self):
        return self._palette