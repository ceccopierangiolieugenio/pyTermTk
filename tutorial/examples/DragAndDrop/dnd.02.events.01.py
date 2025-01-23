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

# This example show the basic Drag and Drop functionality;
#
# Each TTkWidget include 4 methods to handle the Drag and Drop events:
# - dragEnterEvent
# - dragLeaveEvent
# - dragMoveEvent
# - dropEvent
# Overriding any of those methods in a subclass will allow the widget to handle the DnD events
#
# To start a Drag and Drop operation, the TTkDrag object must be created and executed.
# The Drag and Drop operation is usually started after a mouseDragEvent as shown in
# this example, but it can be started after any other events/methods or signals.

class DragDrop(ttk.TTkFrame):
    def mouseDragEvent(self, evt:ttk. TTkMouseEvent) -> bool:
        if evt.key == ttk. TTkMouseEvent.LeftButton:
            # Create a new drag object and set some text as DnD Data
            drag = ttk.TTkDrag()
            drag.setData(f"Test DnD ({self.title()})")
            ttk.TTkLog.debug(f"Drag ({self.title()}) -> {drag.data()}, pos={evt.pos()}")
            # Start the drag operation
            drag.exec()
        return True

    def dragEnterEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        ttk.TTkLog.debug(f"Drag Enter ({self.title()}) - {evt.data()}, pos={evt.pos()}")
        return True

    def dragLeaveEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        ttk.TTkLog.debug(f"Drag Leave ({self.title()}) - {evt.data()}, pos={evt.pos()}")
        return True

    def dragMoveEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        ttk.TTkLog.debug(f"Drag Move ({self.title()}) - {evt.data()}, pos={evt.pos()}")
        return True

    def dropEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        ttk.TTkLog.debug(f"Drop ({self.title()}) <- {evt.data()}, pos={evt.pos()}")
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