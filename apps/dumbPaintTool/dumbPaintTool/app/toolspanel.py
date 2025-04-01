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

import os

import TermTk as ttk

from .palette      import Palette
from .const        import ToolType
from .glbls        import glbls

class ToolsPanel(ttk.TTkVBoxLayout):
    __slots__ = ('_palette',
                 '_glyph','_color',
                 '_la_brush_g', '_ta_brush_a'
                 '_cb_p_fg', '_cb_p_bg',
                 # Signals
                 'pickArea', 'toolSelected','areaChanged')
    def __init__(self, *args, **kwargs):
        self.pickArea = ttk.pyTTkSignal()
        self.areaChanged = ttk.pyTTkSignal(ttk.TTkString)
        self.toolSelected = ttk.pyTTkSignal(ToolType)
        self._color = ttk.TTkColor.RST
        super().__init__(*args, **kwargs)
        self._palette  = Palette(maxHeight=12)
        self.addWidget(self._palette)

        # Layout for the toggle buttons
        lToggleFgBg = ttk.TTkHBoxLayout()
        cb_p_fg = ttk.TTkCheckbox(text="-FG-", checked=ttk.TTkK.Checked)
        cb_p_bg = ttk.TTkCheckbox(text="-BG-", checked=ttk.TTkK.Checked)
        cb_p_gl = ttk.TTkCheckbox(text="Glyph", checked=ttk.TTkK.Checked)
        lToggleFgBg.addWidgets([cb_p_fg,cb_p_bg,cb_p_gl])
        lToggleFgBg.addItem(ttk.TTkLayout())
        cb_p_fg.toggled.connect(self._palette.enableFg)
        cb_p_bg.toggled.connect(self._palette.enableBg)
        cb_p_gl.toggled.connect(glbls.brush.setGlyphEnabled)
        self.addItem(lToggleFgBg)

        # Toolset
        lTools = ttk.TTkGridLayout()
        main_toolset = ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../tui/tools.tui.json"))

        ra_move   = main_toolset.getWidgetByName("ra_move")
        ra_brush  = main_toolset.getWidgetByName("ra_brush")
        ra_line   = main_toolset.getWidgetByName("ra_line")
        ra_rect   = main_toolset.getWidgetByName("ra_rect")
        ra_oval   = main_toolset.getWidgetByName("ra_oval")

        ra_rect_f = main_toolset.getWidgetByName("ra_rect_f")
        ra_rect_e = main_toolset.getWidgetByName("ra_rect_e")

        ra_brush_g = main_toolset.getWidgetByName("ra_brush_g")
        ra_brush_a = main_toolset.getWidgetByName("ra_brush_a")

        cb_move_r = main_toolset.getWidgetByName("cb_move_r")

        la_brush_g = ttk.TTkLabel(   maxHeight=1, minHeight=1)
        btn_pick_a = ttk.TTkButton(  maxHeight=1, minHeight=1, visible=False, text='Pick Area')
        cb_trans_a = ttk.TTkCheckbox(maxHeight=1, minHeight=1, visible=False, text='Transparent')
        ta_brush_a = ttk.TTkTextEdit(                          visible=False, lineNumber=True, readOnly=False)

        spacer = ttk.TTkSpacer()
        # spacer = ttk.TTkFrame(border=True)

        self._la_brush_g = la_brush_g
        self._ta_brush_a = ta_brush_a
        self._cb_p_fg    = cb_p_fg
        self._cb_p_bg    = cb_p_bg

        @ttk.pyTTkSlot()
        def _checkTools():
            tool = ToolType.BRUSH | ToolType.GLYPH
            if ra_move.isChecked():
                tool  = ToolType.MOVE
                if cb_move_r.isChecked():
                    tool |= ToolType.RESIZE
            elif ra_brush.isChecked():
                tool = ToolType.BRUSH
                if ra_brush_g.isChecked():
                    tool |= ToolType.GLYPH
                else:
                    tool |= ToolType.AREA
                    if cb_trans_a.isChecked():
                        tool |= ToolType.TRANSPARENT
            elif ra_rect.isChecked():
                if ra_rect_e.isChecked():
                    tool = ToolType.RECTEMPTY
                else:
                    tool = ToolType.RECTFILL

            spacer.show()
            la_brush_g.hide()
            cb_trans_a.hide()
            btn_pick_a.hide()
            ta_brush_a.hide()
            if tool & ToolType.GLYPH:
                la_brush_g.show()
                spacer.show()
            elif tool & ToolType.AREA:
                cb_trans_a.show()
                btn_pick_a.show()
                ta_brush_a.show()
                spacer.hide()

            glbls.brush.setToolType(tool)
            lTools.update()
            self.update()

        @ttk.pyTTkSlot(bool)
        def _emitTool(checked):
            if not checked: return
            _checkTools()

        @ttk.pyTTkSlot()
        def _pick():
            glbls.brush.setToolType(
                ToolType.BRUSH |
                ToolType.AREA  |
                ToolType.PICKAREA )

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

        # lTools.addWidget(ra_move    ,0,0)
        # lTools.addWidget(cb_move_r  ,0,1)
        # lTools.addWidget(ra_select  ,1,0)
        # lTools.addWidget(ra_brush   ,2,0)
        # lTools.addWidget(ra_brush_g ,2,1)
        # lTools.addWidget(ra_brush_a ,2,2)
        # lTools.addWidget(ra_line    ,3,0)
        # lTools.addWidget(ra_rect    ,4,0)
        # lTools.addWidget(ra_rect_f  ,4,1)
        # lTools.addWidget(ra_rect_e  ,4,2)
        # lTools.addWidget(ra_oval    ,5,0)
        lTools.addWidget(main_toolset ,1,0,1,3)
        lTools.addWidget(la_brush_g ,6,0)
        lTools.addWidget(btn_pick_a ,7,2,1,1)
        lTools.addWidget(cb_trans_a ,7,0,1,2)
        lTools.addWidget(ta_brush_a ,8,0,1,3)
        lTools.addWidget(spacer     ,9,0,1,3)

        self.addItem(lTools)

        self._palette.colorSelected.connect(glbls.brush.setColor)

        glbls.brush.glyphChanged.connect(self._refreshColor)
        glbls.brush.glyphEnabledChanged.connect(self._refreshColor)
        glbls.brush.areaChanged.connect( self.setArea)
        glbls.brush.colorChanged.connect(self._refreshColor)
        glbls.brush.colorChanged.connect(self._palette.setColor)
        glbls.brush.setColor(self._palette.color())

        _checkTools()
        self._refreshColor()

        # brush
        # line
        # rettangle [empty,fill]
        # oval [empty,fill]

    @ttk.pyTTkSlot()
    def _refreshColor(self):
        color = glbls.brush.color()
        glyph = glbls.brush.glyph()
        self._la_brush_g.setText(
                ttk.TTkString("Glyph: '") +
                ttk.TTkString(glyph,color) +
                ttk.TTkString("'"))
        self._cb_p_fg.setChecked(color.hasForeground())
        self._cb_p_bg.setChecked(color.hasBackground())

    @ttk.pyTTkSlot(ttk.TTkColor)
    def setColor(self, color:ttk.TTkColor):
        self._refreshColor()

    @ttk.pyTTkSlot(ttk.TTkString)
    def setArea(self, area:ttk.TTkString):
        self._ta_brush_a.setText(area)
