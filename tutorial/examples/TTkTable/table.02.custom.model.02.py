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

# Any table model is an extension of the TTkAbstractTableMode interface
# Those methods must be defined in order to have a basic implamentation:
#       rowCount(self) -> int
#       columnCount(self) -> int
#       data(self, row:int, col:int) -> object

class MyTableModel(ttk.TTkAbstractTableModel):
    def __init__(self):
        # For testing purposes, this model include a 2d array of strings
        self._mylist = [[f"Cell:{(row,col)}" for col in range(8)] for row in range(50)]
        # I am adding also an int, float, multiline string, multiline Coloured TTkString
        self._mylist[3][5] = 1234
        self._mylist[4][5] = 1234.1234
        self._mylist[5][5] = "Line1\nLine2"
        self._mylist[6][5] = ttk.TTkString("Line1\nLine2\nLine3",ttk.TTkColor.YELLOW)
        super().__init__()

    def rowCount(self) -> int:
        return len(self._mylist)

    def columnCount(self) -> int:
        return len(self._mylist[0])

    def data(self, row:int, col:int) -> None:
        return self._mylist[row][col]

    # I need to define the setData method if I want to include the editable
    # feature for this custom table model
    def setData(self, row: int, col: int, data: object) -> bool:
        self._mylist[row][col] = data
        return True

    # Header Data is not a mandatory field,
    # I am overriding it with a custom value displayed
    # in the top and left headers
    def headerData(self, pos:int, orientation:ttk.TTkK.Direction) -> ttk.TTkString:
        if orientation == ttk.TTkK.HORIZONTAL:
            return f"H:0x{pos:02x}"
        if orientation == ttk.TTkK.VERTICAL:
            return f"V:0x{pos:02x}"
        return super().headerData(pos, orientation)

    # By default any cell is enabled and selectable
    # I am overriding this function to disable the selectable field from
    # the colummn n.1 (the second column)
    # and allow all the columns except the first one to be editable
    def flags(self, row: int, col: int) -> ttk.TTkConstant.ItemFlag:
        if col==0:
            return (
                ttk.TTkK.ItemFlag.ItemIsEnabled  |
                ttk.TTkK.ItemFlag.ItemIsSelectable )
        if col==1:
            return (
                ttk.TTkK.ItemFlag.ItemIsEnabled  |
                ttk.TTkK.ItemFlag.ItemIsEditable )
        return (
            ttk.TTkK.ItemFlag.ItemIsEnabled  |
            ttk.TTkK.ItemFlag.ItemIsEditable |
            ttk.TTkK.ItemFlag.ItemIsSelectable )

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

# Table initialization:
#   parent = root
#     In this example the root terminal (TTk) has this table as the only child
#     since it is using a gridlayout, the child will be resized to occupy the entire
#     area available
#   tableModel = MyTableModel
#     I am using an instance of the custom table model

table = ttk.TTkTable(parent=root, tableModel=MyTableModel())

# Adding a little touch, resizing the cols to its content
table.resizeColumnsToContents()
table.resizeRowsToContents()

# Start the main thread
root.mainloop()
