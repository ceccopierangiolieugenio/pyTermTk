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

sys.path.append(os.path.join(sys.path[0],'../../tmp'))
sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

# Testing Window with a checkbox to enable/disable any control button
class WindowFlagsTest(ttk.TTkWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rb   = ttk.TTkCheckbox(
                    parent=self, pos=(0,0), size=(20,1), text='Reduce   Button',
                    checked=bool(self.windowFlag()&ttk.TTkK.WindowFlag.WindowReduceButtonHint))
        minb = ttk.TTkCheckbox(
                    parent=self, pos=(0,1), size=(20,1), text='Minimize Button',
                    checked=bool(self.windowFlag()&ttk.TTkK.WindowFlag.WindowMinimizeButtonHint))
        maxb = ttk.TTkCheckbox(
                    parent=self, pos=(0,2), size=(20,1), text='Maximize Button',
                    checked=bool(self.windowFlag()&ttk.TTkK.WindowFlag.WindowMaximizeButtonHint))
        cb   = ttk.TTkCheckbox(
                    parent=self, pos=(0,3), size=(20,1), text='Close    Button',
                    checked=bool(self.windowFlag()&ttk.TTkK.WindowFlag.WindowCloseButtonHint))

        # Set the window flag/field based on the checkbox state
        def _cbStateChanged(state,field):
            if state==ttk.TTkK.Checked:
                self.setWindowFlag(self.windowFlag()|field)
            else:
                self.setWindowFlag(self.windowFlag()&(~field))

        rb.stateChanged.connect(  lambda x: _cbStateChanged(x,ttk.TTkK.WindowFlag.WindowReduceButtonHint))
        minb.stateChanged.connect(lambda x: _cbStateChanged(x,ttk.TTkK.WindowFlag.WindowMinimizeButtonHint))
        maxb.stateChanged.connect(lambda x: _cbStateChanged(x,ttk.TTkK.WindowFlag.WindowMaximizeButtonHint))
        cb.stateChanged.connect(  lambda x: _cbStateChanged(x,ttk.TTkK.WindowFlag.WindowCloseButtonHint))



def demoWindowsFlags(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)

    # Standard window (the close button is enabled by default)
    WindowFlagsTest(parent=frame, pos = (0,0), size=(40,8), title="Test Window 1")
    # Enable Max anc Close button
    WindowFlagsTest(parent=frame, pos = (2,2), size=(40,8), title="Test Window 2",
                    flags = ttk.TTkK.WindowFlag.WindowMaximizeButtonHint | ttk.TTkK.WindowFlag.WindowCloseButtonHint)
    # Disable all the control buttons
    WindowFlagsTest(parent=frame, pos = (4,4), size=(40,8), title="Test Window 3",
                    flags = ttk.TTkK.WindowFlag.NONE)
    # Enable only the Max and Min Buttons
    WindowFlagsTest(parent=frame, pos = (6,6), size=(40,8), title="Test Window 4",
                    flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
    # Enable only the Minimize button
    WindowFlagsTest(parent=frame, pos = (8,8), size=(40,8), title="Test Window 5",
                    flags = ttk.TTkK.WindowFlag.WindowReduceButtonHint)

    return frame



def main():
    root = ttk.TTk()
    win1 = ttk.TTkWindow(parent=root,pos = (1,1), size=(60,30), title="Test Window Flags", border=True, layout=ttk.TTkGridLayout(), flags=ttk.TTkK.NONE)
    demoWindowsFlags(win1)
    root.mainloop()

if __name__ == "__main__":
    main()