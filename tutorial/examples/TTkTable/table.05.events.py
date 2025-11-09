#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

# root
#   The root (TTk) widget is the main element of any pyTermTk apps
#   It is responsible of any terminal routine, the terminal update
#   and the events forwarded to any child widgets
#
# root initialization params used:
#
#   layout = GridLayout
#     I am using a grid layout in order to align/resize the table
#     to the root widget (the terminal area)

root = ttk.TTk(layout=ttk.TTkGridLayout())

# The TTkTable is the widget responsible of handling and displaying a table model
# There are several table models available, in this example I am using
# TTkTableModelList which require a simple 2d List with the table data

# I am initializing a simple list where any cell is a string representing its position (row,col) inside the list
dataList = [[f"{(row,col)}" for col in range(10)] for row in range(20)]
# I am adding also an int, float, multiline string, multiline Coloured TTkString
dataList[3][5] = 1234
dataList[4][5] = 1234.1234
dataList[5][5] = "Line1\nLine2"
dataList[6][5] = ttk.TTkString("Line1\nLine2\nLine3\nLine Four!!!",ttk.TTkColor.YELLOW)

basicTableModel = ttk.TTkTableModelList(data=dataList)

# Table initialization:
#   parent = root
#     In this example the root terminal (TTk) has this table as the only child
#     since it is using a gridlayout, the child will be resized to occupy the entire
#     area available
#
#   tableModel = basicTableModel
#     I guess this is self explainatory
#
table = ttk.TTkTable(tableModel=basicTableModel)

# I am using 5 label widgets to display the results of the
# Table events
l_ch = ttk.TTkLabel(text="Cell Changed: xxxx", maxWidth=30)
l_cl = ttk.TTkLabel(text="Cell Clicked: xxxx")
l_dc = ttk.TTkLabel(text="DoubleClked : xxxx")
l_ce = ttk.TTkLabel(text="Cell Entered: xxxx")
l_cc = ttk.TTkLabel(text="Changed:      xxxx")

# I am placing also a text editor to report the content of the cell selected
t_ed = ttk.TTkTextEdit(lineNumber=True, maxHeight=6)

# Yes, you can use lambda functions to process an event
# I don't recommend this and it is used in tbhis example only for testing purposes
table.cellChanged.connect(       lambda r,c:         l_ch.setText(f"Cell Changed: {r,c}"))
table.cellClicked.connect(       lambda r,c:         l_cl.setText(f"Cell Clicked: {r,c}"))
table.cellEntered.connect(       lambda r,c:         l_ce.setText(f"Cell Entered: {r,c}"))
table.cellDoubleClicked.connect( lambda r,c:         l_dc.setText(f"DoubleClked : {r,c}"))
table.currentCellChanged.connect(lambda cr,cc,pr,pc: l_cc.setText(f"Changed:{cr,cc}<-{pr,pc}"))

# In this Lambda function I am setting the text of the text editor to the content of the cell highlighted
table.cellEntered.connect(       lambda r,c:         t_ed.setText(table.model().ttkStringData(r,c)))

#          Col 0     Col 1
#        ┌──────────────────────────┐
#  row 0 │ TABLE                    │
#        │   rowspan = 1            │
#        │   colspan = 2            │
#        ├──────────┬───────────────┤
#  row 1 │ Label 1  │ Text Edit     │
#        ├──────────┤   rowspan = 6 │
#  row 2 │ Label 2  │   colspan = 1 │
#        ├──────────┤               │
#  row 3 │ Label 3  │               │
#        ├──────────┤               │
#  row 4 │ Label 4  │               │
#        ├──────────┤               │
#  row 5 │ Label 5  │               │
#        ├──────────┤               │
#  row 6 │ Label 6  │               │
#        └──────────┴───────────────┘

root.layout().addWidget(table,0,0,1,2)

root.layout().addWidget(l_ch, 1,0)
root.layout().addWidget(l_cl, 2,0)
root.layout().addWidget(l_dc, 3,0)
root.layout().addWidget(l_ce, 4,0)
root.layout().addWidget(l_cc, 5,0)
root.layout().addWidget(t_ed, 1,1,6,1)

# Adding a little touch, resizing the cols and the rows to its content
table.resizeColumnsToContents()
table.resizeRowsToContents()

# Start the main thread
root.mainloop()
