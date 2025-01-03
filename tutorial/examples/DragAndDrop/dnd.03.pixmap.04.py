#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import json
import random

# Those 2 lines are required to use the TermTk library in the main folder
import sys, os
sys.path.append(os.path.join(sys.path[0],'../../..'))

import TermTk as ttk

# This example is another showcase of the Drag Pixmap;
# It is basically a lazy collection of the previous examples
# No drop routine is implemented in this example.

imagesFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../ansi.images.json')
with open(imagesFile) as f:
    d = json.load(f)
    # Image exported by the Dumb Paint Tool - Removing the extra '\n' at the end
    diamond  = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['diamond' ])[0:-1])
    fire     = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['fire'    ])[0:-1])
    key      = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['key'     ])[0:-1])
    peach    = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['peach'   ])[0:-1])
    pepper   = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['pepper'  ])[0:-1])
    python   = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['python'  ])[0:-1])
    ring     = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['ring'    ])[0:-1])
    sword    = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['sword'   ])[0:-1])
    whip     = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['whip'    ])[0:-1])

def imageSize(img:ttk.TTkString) -> int:
    lines = img.split('\n')
    return (
        max(line.termWidth() for line in lines),
        len(lines))

class DragDropBase(ttk.TTkFrame):
    def mouseDragEvent(self, evt:ttk. TTkMouseEvent) -> bool:
        drag = ttk.TTkDrag()
        drag.exec()
        return True

class DragDropWidget(ttk.TTkFrame):
    def mouseDragEvent(self, evt:ttk. TTkMouseEvent) -> bool:
        button = ttk.TTkButton(text=f"DnD: ({self.title()})", border=True, size=(25,5))
        drag = ttk.TTkDrag()
        drag.setPixmap(button)
        drag.exec()
        return True

class DragDropTxt(ttk.TTkFrame):
    def mouseDragEvent(self, evt:ttk. TTkMouseEvent) -> bool:
        pixmap = ttk.TTkCanvas(width=17,height=5)
        pixmap.drawText(pos=(0,0),text="╭╼ TXT ╾────────╮")
        pixmap.drawText(pos=(0,1),text="│Lorem ipsum dol│")
        pixmap.drawText(pos=(0,2),text="│consectetur adi│")
        pixmap.drawText(pos=(0,3),text="│sed do eiusmod │")

        # The next condition is meant to show that you can 
        # handle also the Drag and Drop with the Right or Middle mouse buttons.
        if   evt.key == ttk. TTkMouseEvent.LeftButton:
            pixmap.drawText(pos=(0,4),text="╰───────╼ Left ╾╯")
        elif evt.key == ttk. TTkMouseEvent.RightButton:
            pixmap.drawText(pos=(0,4),text="╰──────╼ Right ╾╯")
        elif evt.key == ttk. TTkMouseEvent.MidButton:
            pixmap.drawText(pos=(0,4),text="╰────╼ Eugenio ╾╯")

        drag = ttk.TTkDrag()
        drag.setPixmap(pixmap)
        drag.exec()
        return True

class DragDropImg(ttk.TTkFrame):
    def mouseDragEvent(self, evt:ttk. TTkMouseEvent) -> bool:
        if evt.key == ttk. TTkMouseEvent.LeftButton:
            imageString = random.choice([diamond,fire,key,peach,ring,sword,whip,pepper,python])

            # A canvas is created and the ANSI String is drawn on it line by line
            w,h = imageSize(imageString)
            pixmap = ttk.TTkCanvas(width=w, height=h+1)
            pixmap.setTransparent(True)
            pixmap.drawText(pos=(0,0), text=self.title())
            for y,line in enumerate(imageString.split('\n')):
                pixmap.drawTTkString(pos=(0,y+1), text=line)

            drag = ttk.TTkDrag()
            drag.setPixmap(pixmap)
            drag.exec()
        return True

root = ttk.TTk()
 
root.layout().addWidget(DragDropBase(  pos=( 0,  0), size=(25,10), title="Pixmap: Default"))
root.layout().addWidget(DragDropWidget(pos=( 0, 10), size=(25,10), title="Pixmap: Widget"))
root.layout().addWidget(DragDropTxt(   pos=(50,  0), size=(25,10), title="Pixmap: Txt"))
root.layout().addWidget(DragDropImg(   pos=(50, 10), size=(25,10), title="Pixmap: Img"))

root.mainloop()