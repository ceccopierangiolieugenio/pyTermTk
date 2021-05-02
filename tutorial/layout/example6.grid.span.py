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

    # Set the GridLayout as defaut in the terminal widget
root = ttk.TTk()

gridLayout = ttk.TTkGridLayout()
root.setLayout(gridLayout)

# | x = 0   | x = 1 | x = 2   |
# |         |       |         |
# ┌────────────────┐┌─────────┐ ──────
# │y=0 x=0 h=1 w=2 ││y=0 x=2  │  y = 0
# │    Button1     ││h=2 w=1  │
# ╘════════════════╛│         │ ──────
# ┌─────────┐       │ Button2 │  y = 1
# │y=1 x=0  │       ╘═════════╛
# │h=2 w=1  │┌────────────────┐ ──────
# │         ││y=2 x=1 h=1 w=2 |  y = 2
# │ Button3 ││    Button4     │
# ╘═════════╛╘════════════════╛ ──────

gridLayout.addWidget(ttk.TTkButton(border=True, text="Button1"), 0,0, 1,2)
gridLayout.addWidget(ttk.TTkButton(border=True, text="Button2"), 0,2, 2,1)
gridLayout.addWidget(ttk.TTkButton(border=True, text="Button3"), 1,0, 2,1)
# It is possible to expand the names
gridLayout.addWidget(ttk.TTkButton(border=True, text="Button4"), row=2, col=1, rowspan=1, colspan=2)

root.mainloop()