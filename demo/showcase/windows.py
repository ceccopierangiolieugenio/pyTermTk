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
sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk


def demoWindows(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)

    win2_1 = ttk.TTkWindow(parent=frame,pos = (0,0), size=(50,30), title="Test Window 1", border=True)
    win2_1.setLayout(ttk.TTkHBoxLayout())
    ttk.TTkTestWidget(parent=win2_1, border=False)

    win2_2 = ttk.TTkWindow(parent=frame,pos = (15,4), size=(87,20), title="Log Window", border=True)
    win2_2.setLayout(ttk.TTkHBoxLayout())
    ttk.TTkLogViewer(parent=win2_2, follow=True )

    win2_3 = ttk.TTkWindow(parent=frame,pos = (5,25), size=(85,7), title="Captured Input", border=True)
    win2_3.setLayout(ttk.TTkHBoxLayout())
    ttk.TTkKeyPressView(parent=win2_3)

    ttk.TTkAbout(parent=frame, pos=(5,7))

    return frame



def main():
    ttk.TTkLog.use_default_file_logging()
    root = ttk.TTk()
    win1 = ttk.TTkWindow(parent=root,pos = (1,1), size=(60,35), title="Test Window 1", border=True, layout=ttk.TTkGridLayout())
    demoWindows(win1)
    root.mainloop()

if __name__ == "__main__":
    main()