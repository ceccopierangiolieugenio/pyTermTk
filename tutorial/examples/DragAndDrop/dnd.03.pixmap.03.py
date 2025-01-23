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

# Load the images from the ansi.images.json file
# Each entry is a compressed base64 encoded image as a multiline TTkString
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

# Calculate the size of the image, this is a simple helper function.
# Since the images are simple ANSI strings,
# the size is calculated by counting the lines and the max width of the lines
def imageSize(img:ttk.TTkString) -> int:
    lines = img.split('\n')
    return (
        max(line.termWidth() for line in lines),
        len(lines))

# This example show a showcase of the Drag and Drop pixmap functionality;
#
# Anytime a Drag and Drop operation is started, a random image is selected and used as Pixmap.
#
# In order to display the images after the drop event, the pixmaps are stored in a list
# and the paintEvent routine is used to draw them on the canvas.

class DragDrop(ttk.TTkFrame):
    def __init__(self, **kwargs):
        # The list of pixmaps to be drawn in the paintEvent routine
        self.pixmaps = []
        super().__init__(**kwargs)

    def mouseDragEvent(self, evt:ttk. TTkMouseEvent) -> bool:
        if evt.key == ttk. TTkMouseEvent.LeftButton:
            # Create a new drag object and
            # a random image is chosen
            imageString = random.choice([diamond,fire,key,peach,ring,sword,whip,pepper,python])

            # A canvas is created and the ANSI String is drawn on it line by line
            w,h = imageSize(imageString)
            pixmap = ttk.TTkCanvas(width=w, height=h+1)
            pixmap.setTransparent(True)
            pixmap.drawText(pos=(0,0), text=self.title())
            for y,line in enumerate(imageString.split('\n')):
                pixmap.drawTTkString(pos=(0,y+1), text=line)

            drag = ttk.TTkDrag()
            drag.setData(pixmap)
            drag.setPixmap(pixmap)
            ttk.TTkLog.debug(f"Drag ({self.title()}) -> pos={evt.x},{evt.y}")
            # Start the drag operation
            drag.exec()
        return True

    def dropEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        # When a drop event is received, the pixmap is stored in the list
        self.pixmaps.append((evt.x, evt.y, evt.data()))
        ttk.TTkLog.debug(f"Drop ({self.title()}) <- pos={evt.x},{evt.y}")
        self.update()
        return True

    def paintEvent(self, canvas:ttk.TTkCanvas) -> None:
        _,_,w,h = self.geometry()
        # Draw all the pixmaps on the canvas
        for x,y,pixmap in self.pixmaps:
            canvas.paintCanvas(pixmap, (x,y,w,h), (0,0,w,h), (0,0,w,h))
        # Call the base paintEvent to draw the frame on top of the pixmap
        super().paintEvent(canvas)

# Create the root application
# and set its layout to TTkGridLayout in order to
# place the widgets in the following way:
#
#          Col 0            Col 1
#         +----------------+----------------+
#   Row 0 | DragDrop 1     | DragDrop 2     |
#         +                +----------------+
#   Row 1 |                | DragDrop 3     |
#         +----------------+----------------+
#   Row 2 | Log Viewer                      |
#         +----------------+----------------+
#
root = ttk.TTk()
root.setLayout(ttk.TTkGridLayout())

# Add the DragDrop widgets to the root layout
root.layout().addWidget(DragDrop(title="DnD 1"),0,0,2,1)
root.layout().addWidget(DragDrop(title="DnD 2"),0,1,1,1)
root.layout().addWidget(DragDrop(title="DnD 3"),1,1,1,1)

# Add a LogViewer at the bottom to display the log messages
# (Row 2, Col 0, RowSpan 1, ColSpan 2)
root.layout().addWidget(ttk.TTkLogViewer(follow=True),2,0,1,2)

root.mainloop()