#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os
sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

class WindowThatHandleKeypress(ttk.TTkWindow):
    def keyEvent(self, evt) -> bool:
        if evt.mod==ttk.TTkK.ControlModifier:
            if evt.key == ttk.TTkK.Key_F:
                ttk.TTkLog.debug("Pressed Key CTRL F inside the Window")
                return True
        return super().keyEvent(evt)

def setMenu(curMenu:ttk.TTkMenuButton):
    curMenu.addMenu("New File")
    curMenu.addMenu("Old File")
    curMenu.addSpacer()
    curMenu.addMenu("Open",checkable=True)
    curMenu.addMenu("Save",checkable=True,checked=True)
    curMenu.addMenu("Save as").setDisabled()
    curMenu.addSpacer()
    exportFileMenu = curMenu.addMenu("E&xport")
    txtExportFileMenu = exportFileMenu.addMenu("t&xt")
    txtExportFileMenu.addMenu("ASCII")
    txtExportFileMenu.addMenu("URF-8")
    txtExportFileMenu.addMenu("PETSCII")
    exportFileMenu = curMenu.addMenu("E&xport 2")
    txtExportFileMenu = exportFileMenu.addMenu("t&xt 2")
    txtExportFileMenu.addMenu("ASCII 2")
    txtExportFileMenu.addMenu("URF-8 2")
    txtExportFileMenu.addMenu("PETSCII 2")
    exportFileMenu.addMenu("&json")
    exportFileMenu.addMenu("&yaml")
    curMenu.addSpacer()
    curMenu.addMenu("Closeeeeeeeee1234567890")
    curMenu.addMenu("Close")
    curMenu.addSpacer()
    curMenu.addMenu("Exit")

root = ttk.TTk(mouseTrack=True)

window = ttk.TTkWindow(title="Test MenuBar", parent=root,pos=(30,1), size=(60,10), border=True)
menuTop = ttk.TTkMenuBarLayout()
setMenu(menuTop.addMenu("&File"))
window.setMenuBar(menuTop)
#menuBottom = ttk.TTkMenuBarLayout()
#setMenu(menuBottom.addMenu("&Fi&le"))
#window.setMenuBar(menuBottom, ttk.TTkK.BOTTOM)

window = WindowThatHandleKeypress(title="Handle CTRL F if focused", parent=root, pos=(0,5), size=(40,10))
#menuTop = ttk.TTkMenuBarLayout()
#setMenu(menuTop.addMenu("&File"))
#window.setMenuBar(menuTop)
#menuBottom = ttk.TTkMenuBarLayout()
#setMenu(menuBottom.addMenu("&Fi&le"))
#window.setMenuBar(menuBottom, ttk.TTkK.BOTTOM)

logWin = ttk.TTkWindow(title="LOG", parent=root, pos=(20,10), size=(100,20), border=True, layout=ttk.TTkGridLayout())
ttk.TTkLogViewer(parent=logWin)

WindowThatHandleKeypress(title="Handle CTRL F if focused", parent=root, pos=(0,15), size=(40,10))

sc = ttk.TTkShortcut(ttk.TTkK.ALT | ttk.TTkK.Key_A)
sc.activated.connect(lambda : ttk.TTkLog.debug("Pressed Key Alt A"))

sc = ttk.TTkShortcut(ttk.TTkK.ALT | ttk.TTkK.Key_B)
sc.activated.connect(lambda : ttk.TTkLog.debug("Pressed Key Alt B"))

sc = ttk.TTkShortcut(ttk.TTkK.CTRL | ttk.TTkK.Key_F)
sc.activated.connect(lambda : ttk.TTkLog.debug("Pressed Key CTRL F"))

sc = ttk.TTkShortcut(ttk.TTkK.CTRL | ttk.TTkK.ALT | ttk.TTkK.Key_F)
sc.activated.connect(lambda : ttk.TTkLog.debug("Pressed Key CTRL ALT F"))

sc = ttk.TTkShortcut(ttk.TTkK.CTRL | ttk.TTkK.ALT | ttk.TTkK.SHIFT | ttk.TTkK.Key_D) # it depend on the terminal used
sc.activated.connect(lambda : ttk.TTkLog.debug("Pressed Key CTRL ALT SHIFT D")) # it depend if the terminal allows it

root.mainloop()