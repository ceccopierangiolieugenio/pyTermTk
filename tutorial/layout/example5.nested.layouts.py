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

import TermTk as ttk

    # Set the GridLayout as default in the terminal widget
root = ttk.TTk()

gridLayout = ttk.TTkGridLayout()
root.setLayout(gridLayout)

    # Attach 2 buttons to the root widget using the default method
    # this will append them to the first row
    # NOTE: it is not recommended to use this legacy method in a gridLayout
ttk.TTkButton(parent=root, border=True, text="Button1")
ttk.TTkButton(parent=root, border=True, text="Button2")
    # Attach 2 buttons to a specific position in the grid
gridLayout.addWidget(ttk.TTkButton(border=True, text="Button3"), 1,2)
gridLayout.addWidget(ttk.TTkButton(border=True, text="Button4"), 2,4)

    # Create a VBoxLayout and add it to the gridLayout
vboxLayout = ttk.TTkVBoxLayout()
gridLayout.addItem(vboxLayout,1,3)
    # Attach 2 buttons to the vBoxLayout
vboxLayout.addWidget(ttk.TTkButton(border=True, text="Button5"))
vboxLayout.addWidget(ttk.TTkButton(border=True, text="Button6"))

root.mainloop()