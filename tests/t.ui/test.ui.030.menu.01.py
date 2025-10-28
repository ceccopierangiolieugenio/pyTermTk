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

ttk.TTkTheme.loadTheme(ttk.TTkTheme.NERD)

root = ttk.TTk(mouseTrack=True)


class RightClickFrame(ttk.TTkResizableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = ttk.TTkMenu(parent=root)
        self.menu.addMenu("New File")
        self.menu.addMenu("Old File")
        af = self.menu.addMenu("Average File")
        af.addMenu("New File",checkable=True)
        af.addMenu("Old File",checkable=True,checked=True)
        af1 = af.addMenu("Average File")
        af1.addMenu("New File")
        af1.addMenu("Old File")
        af2 = af1.addMenu("Average File")

    def paintEvent(self, canvas:ttk.TTkCanvas):
        canvas.drawText(pos=(1,1), text="RightClick")
        return super().paintEvent(canvas)
    def mousePressEvent(self, evt):
        if evt.key == ttk.TTkK.RightButton:
            ttk.TTkHelper.overlay(self, self.menu, evt.x, evt.y)
        return super().mousePressEvent(evt)


ttk.TTkButton(parent=root, pos=(0,0), border=True, text='BTN', size=(20,7))

RightClickFrame(parent=root, pos=(35,10), size=(20,5), border=True)

fileMenu = ttk.TTkMenu(parent=root, pos=(2,2), size=(30,10))

fileMenu.addMenu("New File")
fileMenu.addMenu("Old File")
fileMenu.addSpacer()
fileMenu.addMenu("Open")
fileMenu.addMenu("Save")
fileMenu.addMenu("Save as").setDisabled()
fileMenu.addSpacer()
exportFileMenu = fileMenu.addMenu("Export")
txtExportFileMenu = exportFileMenu.addMenu("t&xt")
txtExportFileMenu.addMenu("ASCII")
txtExportFileMenu.addMenu("URF-8")
txtExportFileMenu.addMenu("PETSCII")
exportFileMenu.addMenu("&json")
exportFileMenu.addMenu("&yaml")
fileMenu.addSpacer()
fileMenu.addMenu("Closeeeeeeeee1234567890")
fileMenu.addMenu("Close")
fileMenu.addSpacer()
fileMenu.addMenu("Exit")

fileMenu = ttk.TTkMenu(parent=root, pos=(8,6), size=(20,12))

fileMenu.addMenu("New File")
fileMenu.addMenu("Old File")
fileMenu.addSpacer()
fileMenu.addMenu("Open",checkable=True)
fileMenu.addMenu("Save",checkable=True,checked=True)
fileMenu.addMenu("Save as").setDisabled()
fileMenu.addSpacer()
exportFileMenu = fileMenu.addMenu("E&xport")
txtExportFileMenu = exportFileMenu.addMenu("t&xt")
txtExportFileMenu.addMenu("ASCII")
txtExportFileMenu.addMenu("URF-8")
txtExportFileMenu.addMenu("PETSCII")
exportFileMenu.addMenu("&json")
exportFileMenu.addMenu("&yaml")
fileMenu.addSpacer()
fileMenu.addMenu("Closeeeeeeeee1234567890")
fileMenu.addMenu("Close")
fileMenu.addSpacer()
fileMenu.addMenu("Exit")

window = ttk.TTkWindow(title="Test MenuBar", parent=root,pos=(30,1), size=(60,10), border=True)
fileMenu2 = window.newMenubarTop().addMenu("&Fi&le")
fileMenu2.addMenu("New File")
fileMenu2.addMenu("Old File")
fileMenu2.addSpacer()
fileMenu2.addMenu("Open",checkable=True)
fileMenu2.addMenu("Save")
fileMenu2.addMenu("Save as")
fileMenu2.addSpacer()
exportFileMenu2 = fileMenu2.addMenu("Export")
txtExportFileMenu2 = exportFileMenu2.addMenu("t&xt")
txtExportFileMenu2.addMenu("ASCII")
txtExportFileMenu2.addMenu("URF-8")
txtExportFileMenu2.addMenu("PETSCII")
exportFileMenu2.addMenu("&json")
exportFileMenu2.addMenu("&yaml")
fileMenu2.addSpacer()
fileMenu2.addMenu("Close")
fileMenu2.addSpacer()
fileMenu2.addMenu("Exit")

window = ttk.TTkWindow(title="LOG", parent=root, pos=(0,20), size=(100,10), border=True, layout=ttk.TTkGridLayout())
ttk.TTkLogViewer(parent=window)

root.mainloop()