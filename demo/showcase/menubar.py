#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk


def demoMenuBar(root=None):
    frame       = ttk.TTkFrame(parent=root, border=False, layout=ttk.TTkVBoxLayout())
    frameTop    = ttk.TTkFrame(parent=frame, border=False)
    frameBottom = ttk.TTkFrame(parent=frame, border=True,layout=ttk.TTkVBoxLayout())

    fileMenu = frameTop.newMenubarTop().addMenu("&File")
    fileMenu.addMenu("Open")
    fileMenu.addMenu("Close")
    fileMenu.addMenu("Exit")

    frameTop.newMenubarTop().addMenu("&Edit")
    frameTop.newMenubarTop().addMenu("&Selection")

    frameTop.newMenubarTop().addMenu("&Center 1", alignment=ttk.TTkK.CENTER_ALIGN)
    frameTop.newMenubarTop().addMenu("Cen&te&r 2", alignment=ttk.TTkK.CENTER_ALIGN)

    frameTop.newMenubarTop().addMenu("_", alignment=ttk.TTkK.RIGHT_ALIGN)
    frameTop.newMenubarTop().addMenu("^", alignment=ttk.TTkK.RIGHT_ALIGN)
    frameTop.newMenubarTop().addMenu("X", alignment=ttk.TTkK.RIGHT_ALIGN)

    window = ttk.TTkWindow(title="Test MenuBar", parent=frameTop,pos=(1,1), size=(60,10), border=True)
    fileMenu2 = window.newMenubarTop().addMenu("&Fi&le")
    fileMenu2.addMenu("New File")
    fileMenu2.addMenu("Old File")
    fileMenu2.addSpacer()
    fileMenu2.addMenu("Open")
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

    editMenu2 = window.newMenubarTop().addMenu("&E&dit")
    editMenu2.addMenu("Undo")
    editMenu2.addMenu("Redo")
    editMenu2.addMenu("Cut")
    editMenu2.addMenu("Copy")
    editMenu2.addMenu("Paste")
    editMenu2.addMenu("Find")
    editMenu2.addMenu("Replace")

    window.newMenubarTop().addMenu("&Selection")

    window.newMenubarTop().addMenu("&Center 3", alignment=ttk.TTkK.CENTER_ALIGN)

    window.newMenubarTop().addMenu("X", alignment=ttk.TTkK.RIGHT_ALIGN)


    fileMenu3 = frameBottom.newMenubarTop().addMenu("&File 2")
    fileMenu3.addMenu("Open")
    fileMenu3.addMenu("Close")
    fileMenu3.addMenu("Exit")

    frameBottom.newMenubarTop().addMenu("&Edit 2")
    frameBottom.newMenubarTop().addMenu("&Selection 2")

    ttk.TTkLogViewer(parent=frameBottom)

    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    root = ttk.TTk()
    if args.f:
        rootLayout = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootLayout = ttk.TTkWindow(title="Test MenuBar", parent=root,pos=(1,1), size=(100,40), border=True, layout=ttk.TTkGridLayout())
    demoMenuBar(rootLayout)
    root.mainloop()

if __name__ == "__main__":
    main()