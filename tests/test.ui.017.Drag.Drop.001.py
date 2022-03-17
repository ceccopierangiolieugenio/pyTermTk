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

import sys, os

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

class DragDrop(ttk.TTkFrame):
    def mouseDragEvent(self, evt) -> bool:
        ttk.TTkLog.debug("Start DnD")
        drag = ttk.TTkDrag()
        drag.setData(f"Test Drag ({self.title()})")
        drag.exec()
        return True

    def dragEnterEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Drag Enter ({self.title()}) -> {evt.data()}, pos={evt.pos()}")
        return True

    def dragLeaveEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Drag Leave ({self.title()}) -> {evt.data()}, pos={evt.pos()}")
        return True

    def dragMoveEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Drag Move ({self.title()}) -> {evt.data()}, pos={evt.pos()}")
        return True

    def dropEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Drop ({self.title()}) -> {evt.data()}, pos={evt.pos()}")
        return True

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()

win1 = ttk.TTkWindow(parent=root,pos = (1,1), size=(100,30), title="Test Window 1", border=True)
win1.setLayout(ttk.TTkGridLayout())

win1.layout().addWidget(DragDrop(title="DnD 1"),0,0,2,1)
win1.layout().addWidget(DragDrop(title="DnD 2"),0,1,1,1)
win1.layout().addWidget(DragDrop(title="DnD 3"),1,1,1,1)
# Add a debug window at the bottom to display the messages
win1.layout().addWidget(ttk.TTkLogViewer(follow=True),2,0,1,2)

root.mainloop()