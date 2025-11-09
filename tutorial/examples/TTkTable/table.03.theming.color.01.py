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
dataList = [[f"{(row,col)}" for col in range(10)] for row in range(101)]
basicTableModel = ttk.TTkTableModelList(data=dataList)

# I am using as a style for the table a cell color with a
# TTkColor Dark Blue ("#000066") + a modifier which alternate the color with a standard BG_BLUE (="#0000FF")
tableStyle = {'default': {'color': ttk.TTkColor.bg("#000066", modifier=ttk.TTkAlternateColor(alternateColor=ttk.TTkColor.BG_BLUE))} }

# Table initialization:
#   parent = root
#     In this example the root terminal (TTk) has this table as the only child
#     since it is using a gridlayout, the child will be resized to occupy the entire
#     area available
#
#   tableModel = basicTableModel
#     I guess this is self explainatory
#
#   addStyle
#     merge the new style with the default one
#     this mergge is required to keep the default object theming values
#     not explictly overridden  (i.e. header/separators colors)
table = ttk.TTkTable(parent=root, tableModel=basicTableModel, addStyle=tableStyle)

# Adding a little touch, resizing the cols to its content
table.resizeColumnsToContents()

# Start the main thread
root.mainloop()
