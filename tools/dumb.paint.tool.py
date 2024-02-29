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

class PaintTemplate(ttk.TTkAppTemplate):
    def __init__(self, border=False, **kwargs):
        super().__init__(border, **kwargs)

        self.setWidget(pa:=PaintArea()   , self.MAIN)
        self.setItem( ptk:=PaintToolKit(), self.TOP,   size=3, fixed=True)
        self.setItem(  ta:=TextArea()    , self.RIGHT, size=50)

        self.setMenuBar(appMenuBar:=ttk.TTkMenuBarLayout(), self.TOP)
        fileMenu      = appMenuBar.addMenu("&File")
        buttonOpen    = fileMenu.addMenu("&Open")
        buttonClose   = fileMenu.addMenu("&Save")
        buttonClose   = fileMenu.addMenu("Save &As...")
        fileMenu.addSpacer()
        buttonExit    = fileMenu.addMenu("E&xit")
        buttonExit.menuButtonClicked.connect(ttk.TTkHelper.quit)

        # extraMenu = appMenuBar.addMenu("E&xtra")
        # extraMenu.addMenu("Scratchpad").menuButtonClicked.connect(self.scratchpad)
        # extraMenu.addSpacer()

        helpMenu = appMenuBar.addMenu("&Help", alignment=ttk.TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked
        helpMenu.addMenu("About tlogg").menuButtonClicked

        ptk.updatedColor.connect(pa.setGlyphColor)
        ta.charSelected.connect(ptk.glyphFromString)
        ta.charSelected.connect(pa.glyphFromString)



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