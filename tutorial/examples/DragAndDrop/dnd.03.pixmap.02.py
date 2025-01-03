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

# Those 2 lines are required to use the TermTk library in the main folder
import sys, os
sys.path.append(os.path.join(sys.path[0],'../../..'))

import TermTk as ttk

# This example show more advance Drag and Drop pixmap usage;
#
# When the Drag and Drop operation is started, a TTkLabel widget is created
# but a new canvas is built to be used as pixmap.
# This approach increase the flexibility on the styling of the full drag and drop operation

class DragDrop(ttk.TTkFrame):
    def mouseDragEvent(self, evt:ttk. TTkMouseEvent) -> bool:
        # Create a new drag object, a new TTkLabel as DnD Data and 
        # a custom Pixmap drawn as a titled box of fixed sizes around
        # a snippet of the label's text
        label = ttk.TTkLabel(text="Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit,\nsed do eiusmod tempor incididunt ut\nlabore et dolore magna aliqua.", size=(10,1))
        
        pixmap = ttk.TTkCanvas(width=17,height=5)
        pixmap.drawText(pos=(0,0),text="╭───────────────╮")
        pixmap.drawText(pos=(2,0),text=f"╼ {self.title()} ╾") # Here for simplicity I am writing the title over the top border
        pixmap.drawText(pos=(0,1),text="│Lorem ipsum dol│")
        pixmap.drawText(pos=(0,2),text="│consectetur adi│")
        pixmap.drawText(pos=(0,3),text="│sed do eiusmod │")
        pixmap.drawText(pos=(0,4),text="╰───────────────╯")

        # The next condition is meant to show that you can 
        # handle also the Drag and Drop with the Right or Middle mouse buttons.
        if   evt.key == ttk. TTkMouseEvent.LeftButton:
            pixmap.drawText(pos=(0,4),text="╰───────╼ Left ╾╯")
        elif evt.key == ttk. TTkMouseEvent.RightButton:
            pixmap.drawText(pos=(0,4),text="╰──────╼ Right ╾╯")
        elif evt.key == ttk. TTkMouseEvent.MidButton:
            pixmap.drawText(pos=(0,4),text="╰────╼ Eugenio ╾╯")

        drag = ttk.TTkDrag()
        drag.setData(label)
        drag.setPixmap(pixmap)
        ttk.TTkLog.debug(f"Drag ({self.title()}) -> pos={evt.x},{evt.y}")
        # Start the drag operation
        drag.exec()
        return True

    def dropEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        # Similar to the previous example
        # I am retrieving the TTkLabel widget used as Drag'nDrop data
        # and I am placing it inside the current Frame
        # This time I am not removing the padding sizes from the 
        # position due to the frame I draw in the pixmap that 
        # already changed the offset of the text being aligned to the final 
        # dropped Label position.
        # BTW, I am not a genious that can figure out all of this upfront, 
        # this is just the result of trial and errors
        label:ttk.TTkLabel = evt.data()
        self.layout().addWidget(label)
        label.move(evt.x, evt.y)
        ttk.TTkLog.debug(f"Drop ({self.title()}) <- pos={evt.x},{evt.y}")
        return True

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