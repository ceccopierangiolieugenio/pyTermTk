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

import os
import sys
import random
import argparse

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

class DragThing(ttk.TTkFrame):
    def __init__(self, *args, **kwargs):
        ttk.TTkFrame.__init__(self, *args, **kwargs)
        # Define and place 4 images with different Hue Color rotation
        ttk.TTkImage(parent=self, pos=( 0, 0), data=ttk.TTkAbout.peppered, rasteriser=ttk.TTkImage.QUADBLOCK)
        ttk.TTkImage(parent=self, pos=( 0,10), data=ttk.TTkAbout.peppered, rasteriser=ttk.TTkImage.QUADBLOCK).rotHue(60)
        ttk.TTkImage(parent=self, pos=(15, 0), data=ttk.TTkAbout.peppered, rasteriser=ttk.TTkImage.QUADBLOCK).rotHue(90)
        ttk.TTkImage(parent=self, pos=(15,10), data=ttk.TTkAbout.peppered, rasteriser=ttk.TTkImage.QUADBLOCK).rotHue(200)
        self.setMaximumWidth(30)
        self.setMinimumWidth(30)

    def mouseDragEvent(self, evt) -> bool:
        ttk.TTkLog.debug("Start DnD")
        drag = ttk.TTkDrag()
        data = ttk.TTkImage(data=ttk.TTkAbout.peppered, rasteriser=ttk.TTkImage.QUADBLOCK)
        # Change color if the drag start over the side images,
        # based on the same Hue rotation defined in the init
        if   evt.x <= 15 and evt.y >  10: data.rotHue(60)
        elif evt.x  > 15 and evt.y <= 10: data.rotHue(90)
        elif evt.x  > 15 and evt.y >  10: data.rotHue(200)
        drag.setPixmap(data)
        drag.setData(data)
        drag.exec()
        return True

class DropThings(ttk.TTkFrame):
    def dropEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Drop ({self.title()}) -> pos={evt.pos()}")
        data = evt.data()
        if issubclass(type(data),ttk.TTkWidget):
            self.layout().addWidget(data)
            data.move(evt.x,evt.y)
            self.update()
            return True
        return False

def demoDnD(root=None):
    dndlayout = ttk.TTkGridLayout()
    frame = ttk.TTkFrame(parent=root, layout=dndlayout, border=0)
    dndlayout.addWidget(DragThing( title="Drag")  ,0,0,2,1)
    dndlayout.addWidget(DropThings(title="Drop 1"),0,1,1,2)
    dndlayout.addWidget(DropThings(title="Drop 2"),0,3,1,1)
    dndlayout.addWidget(DropThings(title="Drop 3"),1,1,1,1)
    dndlayout.addWidget(DropThings(title="Drop 4"),1,2,1,2)

    # Add a debug window at the bottom to display the messages
    dndlayout.addWidget(ttk.TTkLogViewer(follow=True),2,0,1,4)
    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    root = ttk.TTk()
    if args.f:
        rootTree = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootTree = ttk.TTkWindow(parent=root,pos = (0,0), size=(80,40), title="Test Drag'n Drop", layout=ttk.TTkGridLayout(), border=True)
    demoDnD(rootTree)
    root.mainloop()

if __name__ == "__main__":
    main()