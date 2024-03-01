#!/usr/bin/env python3

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

import sys, os, argparse

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

from dumb_paint_lib import *

ttk.TTkTheme.loadTheme(ttk.TTkTheme.NERD)

class LeftPanel(ttk.TTkVBoxLayout):
    __slots__ = ('_palette',
                 # Signals
                 'toolSelected')
    def __init__(self, *args, **kwargs):
        self.toolSelected = ttk.pyTTkSignal(PaintArea.Tool)
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
        ra_brush  = ttk.TTkRadioButton(radiogroup="tools", text="Brush", checked=True)
        ra_line   = ttk.TTkRadioButton(radiogroup="tools", text="Line", enabled=False)
        ra_rect   = ttk.TTkRadioButton(radiogroup="tools", text="Rect")
        ra_oval   = ttk.TTkRadioButton(radiogroup="tools", text="Oval", enabled=False)

        ra_rect_f = ttk.TTkRadioButton(radiogroup="toolsRectFill", text="Fill" , enabled=False, checked=True)
        ra_rect_e = ttk.TTkRadioButton(radiogroup="toolsRectFill", text="Empty", enabled=False)

        @ttk.pyTTkSlot(bool)
        def _emitTool(checked):
            if not checked: return
            tool = PaintArea.Tool.BRUSH
            if ra_brush.isChecked():
                tool = PaintArea.Tool.BRUSH
            elif ra_rect.isChecked():
                if ra_rect_e.isChecked():
                    tool = PaintArea.Tool.RECTEMPTY
                else:
                    tool = PaintArea.Tool.RECTFILL
            self.toolSelected.emit(tool)

        ra_rect.toggled.connect(ra_rect_f.setEnabled)
        ra_rect.toggled.connect(ra_rect_e.setEnabled)

        ra_brush.toggled.connect(  _emitTool)
        ra_line.toggled.connect(   _emitTool)
        ra_rect.toggled.connect(   _emitTool)
        ra_rect_f.toggled.connect( _emitTool)
        ra_rect_e.toggled.connect( _emitTool)
        ra_oval.toggled.connect(   _emitTool)

        lTools.addWidget(ra_brush,0,0)
        lTools.addWidget(ra_line,1,0)
        lTools.addWidget(ra_rect,2,0)
        lTools.addWidget(ra_rect_f,2,1)
        lTools.addWidget(ra_rect_e,2,2)
        lTools.addWidget(ra_oval,3,0)
        self.addItem(lTools)

        # brush
        # line
        # rettangle [empty,fill]
        # oval [empty,fill]
        self.addItem(ttk.TTkLayout())



    def palette(self):
        return self._palette


class PaintTemplate(ttk.TTkAppTemplate):
    def __init__(self, border=False, **kwargs):
        super().__init__(border, **kwargs)
        parea    = PaintArea()
        ptoolkit = PaintToolKit()
        tarea    = TextArea()

        leftPanel = LeftPanel()
        palette = leftPanel.palette()

        self.setItem(leftPanel , self.LEFT,  size=16*2)
        self.setWidget(parea   , self.MAIN)
        self.setItem(ptoolkit  , self.TOP,   size=3, fixed=True)
        self.setItem(tarea     , self.RIGHT, size=50)

        self.setMenuBar(appMenuBar:=ttk.TTkMenuBarLayout(), self.TOP)
        fileMenu      = appMenuBar.addMenu("&File")
        buttonOpen    = fileMenu.addMenu("&Open")
        buttonClose   = fileMenu.addMenu("&Save")
        buttonClose   = fileMenu.addMenu("Save &As...")
        fileMenu.addSpacer()
        fileMenu.addMenu("Load Palette")
        fileMenu.addMenu("Save Palette")
        fileMenu.addSpacer()
        buttonExit    = fileMenu.addMenu("E&xit")
        buttonExit.menuButtonClicked.connect(ttk.TTkHelper.quit)

        # extraMenu = appMenuBar.addMenu("E&xtra")
        # extraMenu.addMenu("Scratchpad").menuButtonClicked.connect(self.scratchpad)
        # extraMenu.addSpacer()

        helpMenu = appMenuBar.addMenu("&Help", alignment=ttk.TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked
        helpMenu.addMenu("About tlogg").menuButtonClicked

        palette.colorSelected.connect(parea.setGlyphColor)
        palette.colorSelected.connect(ptoolkit.setColor)
        ptoolkit.updatedColor.connect(parea.setGlyphColor)
        tarea.charSelected.connect(ptoolkit.glyphFromString)
        tarea.charSelected.connect(parea.glyphFromString)
        leftPanel.toolSelected.connect(parea.setTool)

        parea.setGlyphColor(palette.color())
        ptoolkit.setColor(palette.color())


root = ttk.TTk(
        title="Dumb Paint Tool",
        layout=ttk.TTkGridLayout(),
        mouseTrack=True,
        sigmask=(
            # ttk.TTkTerm.Sigmask.CTRL_C |
            ttk.TTkTerm.Sigmask.CTRL_Q |
            ttk.TTkTerm.Sigmask.CTRL_S |
            ttk.TTkTerm.Sigmask.CTRL_Z ))

PaintTemplate(parent=root)

root.mainloop()