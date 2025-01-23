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
# the hotSpot is set to define the offset from the mouse cursor

class DraggableFrame_FixedHotSpot(ttk.TTkFrame):
    # I save the hotSpot in the constructor to be used during the dragging operation
    def __init__(self, *, hotSpot ,**kwargs):
        self.hotSpot = hotSpot
        super().__init__(**kwargs)
        self.layout().addWidget(ttk.TTkLabel(text="Drag Me..."))

    def mouseDragEvent(self, evt:ttk. TTkMouseEvent) -> bool:
        button = ttk.TTkButton(text=f"{self.title()}", border=True, size=self.size())
        drag = ttk.TTkDrag()
        drag.setHotSpot(self.hotSpot)
        drag.setData(button)
        drag.setPixmap(button)
        ttk.TTkLog.debug(f"Drag ({self.title()}) -> {button.text()}, pos={evt.x},{evt.y}")
        # Start the drag operation
        drag.exec()
        return True

class DraggableFrame_RelativeHotSpot(ttk.TTkFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout().addWidget(ttk.TTkLabel(text="Drag Me..."))

    def mouseDragEvent(self, evt:ttk. TTkMouseEvent) -> bool:
        button = ttk.TTkButton(text=f"HotSpot at\nMouse relative Pos\n\n-->{(evt.x, evt.y)}<--", border=True, size=self.size())
        drag = ttk.TTkDrag()
        drag.setHotSpot((evt.x, evt.y))
        drag.setData(button)
        drag.setPixmap(self)
        ttk.TTkLog.debug(f"Drag ({self.title()}) -> {button.text()}, pos={evt.x},{evt.y}")
        # Start the drag operation
        drag.exec()
        return True

class DropFrame(ttk.TTkFrame):
    def dropEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        button:ttk.TTkButton = evt.data()
        self.layout().addWidget(button)
        # Since the frame by default has a padding of 1
        # I align the button to the mouse coordinates by subtracting the Top/Left padding size
        t,b,l,r = self.getPadding()
        hsx,hsy = evt.hotSpot()
        button.move(evt.x-l-hsx, evt.y-t-hsy)
        ttk.TTkLog.debug(f"Drop ({self.title()}) <- {button.text()}, pos={evt.x},{evt.y}")

        # This is not required in this example
        #
        # But I just add a logging feedback to the button
        # To show that the button has been clicked
        # Note: I highly recommend to avoid using lambda as a slot
        #       The correct way is to have a method in the class, marked as pyTTkSlot,
        #       capable of handling the signal
        button.clicked.connect(lambda: ttk.TTkLog.debug(f"Clicked: {button.text()}"))
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
root.layout().addWidget(df1 := DropFrame(title="DnD 1"),0,0,2,1)
root.layout().addWidget(       DropFrame(title="DnD 2"),0,1,1,1)
root.layout().addWidget(       DropFrame(title="DnD 3"),1,1,1,1)

df1.layout().addWidget(DraggableFrame_FixedHotSpot(pos=( 0, 0),size=(25,5),title="Fix HotSpot ( 0, 0)", hotSpot=( 0, 0)))
df1.layout().addWidget(DraggableFrame_FixedHotSpot(pos=( 0, 5),size=(25,5),title="Fix HotSpot ( 5, 0)", hotSpot=( 5, 0)))
df1.layout().addWidget(DraggableFrame_FixedHotSpot(pos=( 0,10),size=(25,5),title="Fix HotSpot ( 0, 3)", hotSpot=( 0, 3)))
df1.layout().addWidget(DraggableFrame_FixedHotSpot(pos=( 0,15),size=(25,5),title="Fix HotSpot ( 5, 3)", hotSpot=( 5, 3)))
df1.layout().addWidget(DraggableFrame_FixedHotSpot(pos=(25,10),size=(25,5),title="Fix HotSpot (-5,-3)", hotSpot=(-5,-3)))
df1.layout().addWidget(DraggableFrame_FixedHotSpot(pos=(25,15),size=(25,5),title="Fix HotSpot (10, 3)", hotSpot=(10, 3)))

df1.layout().addWidget(DraggableFrame_RelativeHotSpot(pos=(25,0),size=(25,10),title="Relative HotSpot"))

# Add a LogViewer at the bottom to display the log messages
# (Row 2, Col 0, RowSpan 1, ColSpan 2)
root.layout().addWidget(ttk.TTkLogViewer(follow=True),2,0,1,2)

root.mainloop()