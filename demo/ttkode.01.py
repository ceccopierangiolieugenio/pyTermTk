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
import TermTk as ttk

# ttk.TTkFileTree(parent=self, path=".")
class _KolorFrame(ttk.TTkFrame):
    __slots__ = ('_fillColor', '_text')
    def __init__(self, fillColor=ttk.TTkColor.RST, text:str="", **kwargs):
        self._text = text
        self._fillColor = fillColor
        ttk.TTkFrame.__init__(self, **kwargs)
        self.setFocusPolicy(ttk.TTkK.FocusPolicy.ClickFocus)

    def text(self):
        return self._text

    def setFillColor(self, color):
        self._fillColor = color

    def paintEvent(self, canvas):
        w,h = self.size()
        for y in range(h):
            canvas.drawText(pos=(0,y),text='',width=w,color=self._fillColor)
        canvas.drawText(pos=(2,2),text=self._text)
        return super().paintEvent(canvas)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkTheme.loadTheme(ttk.TTkTheme.NERD)

    root = ttk.TTk(title="ttkode", mouseTrack=True)
    layout = ttk.TTkGridLayout()
    if args.f:
        root.setLayout(layout)
        container = root
        border = False
    else:
        container = ttk.TTkWindow(
            parent=root,pos=(0,0), size=(100,40), title="pyTermTk Showcase", border=True, layout=layout,
            flags = ttk.TTkK.WindowFlag.WindowMaximizeButtonHint | ttk.TTkK.WindowFlag.WindowCloseButtonHint)
        border = False

    at = ttk.TTkAppTemplate(parent=container, border=border)
    kodeTab  = ttk.TTkKodeTab(border=False, barType=ttk.TTkBarType.NERD_1, closable=True)
    fileTree = ttk.TTkFileTree(path='.')

    at.setWidget(widget=fileTree, position=at.LEFT, size=15)
    at.setWidget(widget=kodeTab, position=at.MAIN)
    at.setWidget(widget=ttk.TTkLogViewer(), position=at.BOTTOM, size=3, title="Logs")

    kodeTab.addTab(_KolorFrame(fillColor=ttk.TTkColor.bg("#008800", modifier=ttk.TTkColorGradient(increment=-6)), title=" uno ")," uno ")
    kodeTab.addTab(_KolorFrame(fillColor=ttk.TTkColor.bg("#880000", modifier=ttk.TTkColorGradient(increment=-6)), title=" due ")," due ")
    kodeTab.addTab(_KolorFrame(fillColor=ttk.TTkColor.bg("#000088", modifier=ttk.TTkColorGradient(increment=-6)), title=" tre ")," tre ")
    kodeTab.addTab(_KolorFrame(fillColor=ttk.TTkColor.bg("#888800", modifier=ttk.TTkColorGradient(increment=-6)), title=" quattro ")," quattro ")
    kodeTab.addTab(_KolorFrame(fillColor=ttk.TTkColor.bg("#008888", modifier=ttk.TTkColorGradient(increment=-6)), title=" cinque ")," cinque ")
    kodeTab.addTab(_KolorFrame(fillColor=ttk.TTkColor.bg("#880088", modifier=ttk.TTkColorGradient(increment=-6)), title=" sei ")," sei ")
    # kodeTab.addTab(_KolorFrame(fillColor=ttk.TTkColor.bg("#888888", modifier=ttk.TTkColorGradient(increment=-6)), title=" sette ")," sette ")
    # kodeTab.addTab(_KolorFrame(fillColor=ttk.TTkColor.bg("#444444", modifier=ttk.TTkColorGradient(increment= 3)), title=" otto ")," otto ")

    m1 = kodeTab.addMenu('Test1')
    m2 = kodeTab.addMenu('Test2')

    m1.addMenu("Open",checkable=True)
    m1.addMenu("Save",checkable=True,checked=True)
    m1.addMenu("Save as").setDisabled()

    m2.addMenu("m2 Open",checkable=True)
    m2.addMenu("m2 Save",checkable=True,checked=True)
    m2.addMenu("m2 Save as").setDisabled()

    def _openFile(item):
        kt = _KolorFrame(
                text=item.path(),
                title=item.path(),
                fillColor=ttk.TTkColor.bg("#888888", modifier=ttk.TTkColorGradient(increment=-6)),)
        kt.focusChanged.connect(lambda _f, _p=item.path() : ttk.TTkLog.debug(f"Focus Changed ({_f}) -> {_p}"))
        kodeTab.addTab(kt, 'File')
        kodeTab.setCurrentWidget(kt)
        for wid in kodeTab.iterWidgets():
            ttk.TTkLog.debug(wid)
        kt.setFocus()

    fileTree.fileActivated.connect(_openFile)

    def _reportClose(tab:ttk.TTkTabWidget, num:int):
        ttk.TTkLog.debug(f"DEL: {num} - {tab} - {tab.widget(num).text()}")

    kodeTab.tabCloseRequested.connect(_reportClose)

    root.mainloop()

if __name__ == "__main__":
    main()