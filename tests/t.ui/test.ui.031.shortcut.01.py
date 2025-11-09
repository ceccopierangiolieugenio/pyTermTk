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

class WindowThatHandleKeypress(ttk.TTkWindow):
    def keyEvent(self, evt) -> bool:
        if evt.mod==ttk.TTkK.ControlModifier:
            if evt.key == ttk.TTkK.Key_F:
                ttk.TTkLog.debug("Pressed Key CTRL F inside the Window")
                return True
        return super().keyEvent(evt)

root = ttk.TTk()

logWin = ttk.TTkWindow(title="LOG", parent=root, pos=(20,0), size=(100,20), border=True, layout=ttk.TTkGridLayout())
ttk.TTkLogViewer(parent=logWin)

WindowThatHandleKeypress(title="Handle CTRL F if focused", parent=root, pos=(0,5), size=(40,10))

sc = ttk.TTkShortcut(ttk.TTkK.ALT | ttk.TTkK.Key_A)
sc.activated.connect(lambda : ttk.TTkLog.debug("Pressed Key Alt A"))

sc = ttk.TTkShortcut(ttk.TTkK.ALT | ttk.TTkK.Key_B)
sc.activated.connect(lambda : ttk.TTkLog.debug("Pressed Key Alt B"))

sc = ttk.TTkShortcut(ttk.TTkK.CTRL | ttk.TTkK.Key_F)
sc.activated.connect(lambda : ttk.TTkLog.debug("Pressed Key CTRL F"))

sc = ttk.TTkShortcut(ttk.TTkK.CTRL | ttk.TTkK.ALT | ttk.TTkK.Key_F)
sc.activated.connect(lambda : ttk.TTkLog.debug("Pressed Key CTRL ALT F"))

sc = ttk.TTkShortcut(ttk.TTkK.CTRL | ttk.TTkK.ALT | ttk.TTkK.SHIFT | ttk.TTkK.Key_D) # it depend on the terminal used
sc.activated.connect(lambda : ttk.TTkLog.debug("Pressed Key CTRL ALT SHIFT D")) # it depend if the terminal allows it

root.mainloop()