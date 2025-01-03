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

# This example show the basic Drag and Drop pixmap usage;
#
# Anytime a Drag and Drop operation is started, a new TTkButton is created
# and used as DnD Data and Pixmap.
# The same data object is added to the frame in the dropEvent and moved to the mouse coordinates.

class DragDrop(ttk.TTkFrame):
    def mouseDragEvent(self, evt:ttk. TTkMouseEvent) -> bool:
        if evt.key == ttk. TTkMouseEvent.LeftButton:
            # Create a new drag object and 
            # a new TTkButton as DnD Data and Pixmap
            # the default TTkButton canvas will be used as Pixmap
            button = ttk.TTkButton(text=f"Test DnD ({self.title()})", border=True, size=(20,3))
            drag = ttk.TTkDrag()
            drag.setData(button)
            drag.setPixmap(button)
            ttk.TTkLog.debug(f"Drag ({self.title()}) -> {button.text()}, pos={evt.x},{evt.y}")
            # Start the drag operation
            drag.exec()
        return True

    def dropEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        button:ttk.TTkButton = evt.data()
        self.layout().addWidget(button)
        # Since the frame by default has a padding of 1
        # I align the button to the mouse coordinates by subtracting the Top/Left padding size
        t,b,l,r = self.getPadding()
        button.move(evt.x-l, evt.y-t)
        ttk.TTkLog.debug(f"Drop ({self.title()}) <- {button.text()}, pos={evt.x},{evt.y}")
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