#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import argparse
import os
import sys
import time


sys.path.append(os.path.join(sys.path[0],'..'))
from TermTk import TTk, TTkLog, TTkHelper
from TermTk import TTkGridLayout, TTkFileTree, TTkWidget, TTkFrame
from TermTk import TTkWindow, TTkColor, TTkColorGradient, TTkRadioButton, TTkSpacer
from TermTk import TTkTheme, TTkK, TTkSplitter, TTkTabWidget, TTkKodeTab

# TTkFileTree(parent=self, path=".")
class _KolorFrame(TTkFrame):
    __slots__ = ('_fillColor')
    def __init__(self, *args, **kwargs):
        TTkFrame.__init__(self, *args, **kwargs)
        self._fillColor = kwargs.get('fillColor', TTkColor.RST)

    def setFillColor(self, color):
        self._fillColor = color

    def paintEvent(self, canvas):
        w,h = self.size()
        for y in range(h):
            canvas.drawText(pos=(0,y),text='',width=w,color=self._fillColor)
        return super().paintEvent(canvas)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    TTkTheme.loadTheme(TTkTheme.NERD)

    root = TTk(title="ttkode")
    layout = TTkGridLayout()
    if args.f:
        root.setLayout(layout)
        container = root
        border = False
    else:
        container = TTkWindow(
            parent=root,pos=(0,0), size=(100,40), title="pyTermTk Showcase", border=True, layout=layout,
            flags = TTkK.WindowFlag.WindowMaximizeButtonHint | TTkK.WindowFlag.WindowCloseButtonHint)
        border = True

    splitter = TTkSplitter(parent=container)
    splitter.addWidget(fileTree:=TTkFileTree(path='.'), 15)

    hSplitter = TTkSplitter(parent=splitter,  orientation=TTkK.HORIZONTAL)
    kt = TTkKodeTab(parent=hSplitter, border=False, closable=True)

    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#008800", modifier=TTkColorGradient(increment=-6)), title="uno"),"uno")
    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#880000", modifier=TTkColorGradient(increment=-6)), title="due"),"due")
    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#000088", modifier=TTkColorGradient(increment=-6)), title="tre"),"tre")
    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#888800", modifier=TTkColorGradient(increment=-6)), title="quattro"),"quattro")
    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#008888", modifier=TTkColorGradient(increment=-6)), title="cinque"),"cinque")
    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#880088", modifier=TTkColorGradient(increment=-6)), title="sei"),"sei")

    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#888888", modifier=TTkColorGradient(increment=-6)), title="sette"),"sette")
    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#444444", modifier=TTkColorGradient(increment= 3)), title="otto"),"otto")

    m1 = kt.addMenu('Test1')
    m2 = kt.addMenu('Test2')

    m1.addMenu("Open",checkable=True)
    m1.addMenu("Save",checkable=True,checked=True)
    m1.addMenu("Save as").setDisabled()

    m2.addMenu("m2 Open",checkable=True)
    m2.addMenu("m2 Save",checkable=True,checked=True)
    m2.addMenu("m2 Save as").setDisabled()

    fileTree.fileActivated.connect(lambda item:kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#888888", modifier=TTkColorGradient(increment=-6)), title=item.path()),"File")
)

    root.mainloop()

if __name__ == "__main__":
    main()