#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the"Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED"AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import pty
import sys
import threading
import argparse
from select import select


sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkTestWidgets.logviewer import _TTkLogViewer


from wblib import *

# parser = argparse.ArgumentParser()
# parser.add_argument('-d', help='Debug (Add LogViewer Panel)',    action='store_true')
# args = parser.parse_args()

# class WBWindow(ttk.TTkWindow):

class WorkBench(ttk.TTkContainer):
    __slots__ = ('_barSelected', '_barPosition', '_backLayout')
    def __init__(self, *args, **kwargs):
        self._barselected = False
        self._barPosition = 0
        self._backLayout = ttk.TTkLayout()
        self._backLayout.setGeometry(0,0,0,0)
        self._barSelected = False
        super().__init__(*args, **kwargs)
        self.setPadding(1,0,0,0)
        self.setFocusPolicy(ttk.TTkK.ClickFocus)
        self.rootLayout().addItem(self._backLayout)

        _win = ttk.TTkWindow(pos=(10,0), size=(100,30),title=f"Loader Demo", layout=ttk.TTkGridLayout())
        WBLoader(parent=_win)
        self._backLayout.addWidget(_win)

        if os.path.isfile(_fileName := os.path.join(sys.path[0],"dontsavethisfile.txt")):
            with open(_fileName,'r') as f:
                data = ttk.TTkUtil.base64_deflate_2_obj(f.read())
                _win = ttk.TTkWindow(pos=(10,0), size=(100,30),title=f"Guru Meditation", layout=ttk.TTkGridLayout())
                _sa = ttk.TTkScrollArea(parent=_win)
                ttk.TTkImage(parent=_sa.viewport(), data=data, rasteriser=ttk.TTkImage.QUADBLOCK)
                self._backLayout.addWidget(_win)

    def mousePressEvent(self, evt):
        self._barSelected = evt.y == self._barPosition
        return True

    def mouseReleaseEvent(self, evt) -> bool:
        self._barSelected = False
        return True

    def mouseDragEvent(self, evt):
        if not self._barSelected: return True
        w,h = self.size()
        y = max(0,min(evt.y,h-1))
        self.setPadding(y+1,0,0,0)
        self._barPosition = y
        self._backLayout.setGeometry(0,0,w,y)
        self.update()
        return True

    def paintEvent(self, canvas: TTkCanvas):
        w,h = self.size()

        canvas.fill(size=(w,self._barPosition))
        canvas.fill(pos=(0,self._barPosition),color=bgBLUE)
        # draw the title
        canvas.drawText(
            pos=(0,self._barPosition),
            text=" pyTermTk Workbench.  Version 1.0   plenty of free memory",
            width=w,
            color=bgWHITE+fgBLUE)

        canvas.drawText(
            pos=(w-5,self._barPosition),
            text="│◪│◩│",
            color=bgWHITE+fgBLUE)

class TTkWorkbench(ttk.TTk):
    def paintEvent(self, canvas: TTkCanvas):
        canvas.fill(color=bgBLUE)

logWin = WBScrollWin(pos=(10,10), size=(60,20),
                whiteBg=False,
                title=f"Key Press Viewer",layout=ttk.TTkVBoxLayout())
logWin.setViewport(_TTkLogViewer())

root = TTkWorkbench(layout=ttk.TTkGridLayout(), mouseTrack=True)
root.setPadding(3,3,15,10)

wbl = WBLoader(size=root.size())
root.rootLayout().addWidget(wbl)

wb = WorkBench(parent=root)

clipboard = ttk.TTkClipboard()

ttk.pyTTkSlot()
def _openTerminal(term=[]):
    _x,_y = 15,5
    while (_x,_y) in [_t['pos'] for _t in term]:
        _x += 4
        _y += 2
    _win  = WBScrollWin(parent=wb, pos=(_x,_y), size=(60,20),
                    whiteBg=False,
                    title=f"Terminallo n.{len(term)+1}",layout=ttk.TTkVBoxLayout())
    _win.setViewport(_term := ttk.TTkTerminalView())
    _th4 = ttk.TTkTerminalHelper(term=_term)
    _th4.runShell()
    _term.bell.connect(lambda : ttk.TTkLog.debug("BELL!!! 🔔🔔🔔"))
    _term.titleChanged.connect(_win.setTitle)
    _term.textSelected.connect(clipboard.setText)
    term.append({'pos':(_x,_y),'term':_term,'win':_win})
    _win.raiseWidget()

ttk.pyTTkSlot()
def _openInputViewer():
    _win  = WBWindow(parent=wb, pos=(10,10), size=(60,6),
                    whiteBg=False,
                    title=f"Key Press Viewer",layout=ttk.TTkVBoxLayout())
    ttk.TTkKeyPressView(parent=_win)
    _win.raiseWidget()

def _openPreferences():
    _style = {'default':     {'color': fgWHITE+bgBLUE},}
    _win  = WBWindow(parent=wb, pos=(10,10), size=(60,7),title=f"Preferences")
    ttk.TTkLabel(parent=_win, pos=(0,0), text="Padding").setStyle(_style)
    ttk.TTkLabel(parent=_win, pos=(2,1), text="Top"    ).setStyle(_style)
    ttk.TTkLabel(parent=_win, pos=(2,2), text="Bottom" ).setStyle(_style)
    ttk.TTkLabel(parent=_win, pos=(2,3), text="Left"   ).setStyle(_style)
    ttk.TTkLabel(parent=_win, pos=(2,4), text="Right"  ).setStyle(_style)

    ttk.TTkLabel(parent=_win, pos=(30,0), text="Style\nComing soon...\nOr Not").setStyle(_style)

    t,b,l,r = root.getPadding()
    _sbT = ttk.TTkSpinBox(parent=_win, pos=(10,1), size=(6,1), value=t, maximum=30, minimum=0)
    _sbB = ttk.TTkSpinBox(parent=_win, pos=(10,2), size=(6,1), value=b, maximum=30, minimum=0)
    _sbL = ttk.TTkSpinBox(parent=_win, pos=(10,3), size=(6,1), value=l, maximum=30, minimum=0)
    _sbR = ttk.TTkSpinBox(parent=_win, pos=(10,4), size=(6,1), value=r, maximum=30, minimum=0)

    _sbT.setStyle(_style)
    _sbB.setStyle(_style)
    _sbL.setStyle(_style)
    _sbR.setStyle(_style)

    def _updatePadding(_,_sbT=_sbT,_sbB=_sbB,_sbL=_sbL,_sbR=_sbR):
        root.setPadding(_sbT.value(),_sbB.value(),_sbL.value(),_sbR.value())

    _sbT.valueChanged.connect(_updatePadding)
    _sbB.valueChanged.connect(_updatePadding)
    _sbL.valueChanged.connect(_updatePadding)
    _sbR.valueChanged.connect(_updatePadding)

    _win.raiseWidget()



ttk.pyTTkSlot()
def _openLogViewer():
    wb.layout().addWidget(logWin)
    logWin.show()
    logWin.resize(80,30)
    logWin.raiseWidget()

winWb  = WBScrollWin(parent=wb, pos=(5,2), size=(50,15), title="euWorkbench")

winWb.viewport().addWidget(_bttn:=WBIconButton(pos=(3,0), icon=WBIconButton.IconTerminal,
            text="Terminal"))
_bttn.clicked.connect(_openTerminal)

winWb.viewport().addWidget(_bttn:=WBIconButton(pos=(18,0), icon=WBIconButton.IconInputLog,
            text="Input Viewer"))
_bttn.clicked.connect(_openInputViewer)

winWb.viewport().addWidget(_bttn:=WBIconButton(pos=(35,3), icon=WBIconButton.IconLogViewer,
             text="Log Viewer"))
_bttn.clicked.connect(_openLogViewer)

winWb.viewport().addWidget(_bttn:=WBIconButton(pos=(0,6), icon=WBIconButton.IconPreferences,
             text="Preferences"))
_bttn.clicked.connect(_openPreferences)

root.mainloop()