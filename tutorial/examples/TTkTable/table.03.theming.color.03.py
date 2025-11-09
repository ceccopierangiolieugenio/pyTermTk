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

# This is a custom color modifier used to add a color pattern on each table line
class CustomColorModifier(ttk.TTkAlternateColor):
    # I am defining a list of colors used as a circle list in this class
    colors = (
        [ ttk.TTkColor.bg("#000066"), ttk.TTkColor.bg("#0000FF") ] * 3 +
        [ ttk.TTkColor.bg("#003300"), ttk.TTkColor.bg("#006600") ] +
        [ ttk.TTkColor.bg("#000066"), ttk.TTkColor.bg("#0000FF") ] * 3 +
        [ttk.TTkColor.RST] * 5 +
        [ #Rainbow-ish
            ttk.TTkColor.fgbg("#00FFFF","#880000") + ttk.TTkColor.BOLD,
            ttk.TTkColor.fgbg("#00FFFF","#FF0000") + ttk.TTkColor.BOLD,
            ttk.TTkColor.fgbg("#0000FF","#FFFF00") + ttk.TTkColor.BOLD,
            ttk.TTkColor.fgbg("#FF00FF","#00FF00") + ttk.TTkColor.BOLD,
            ttk.TTkColor.fgbg("#FF0000","#00FFFF") + ttk.TTkColor.BOLD,
            ttk.TTkColor.fgbg("#FFFF00","#0000FF") + ttk.TTkColor.BOLD,
            ttk.TTkColor.fgbg("#00FF00","#FF00FF") + ttk.TTkColor.BOLD,
            ttk.TTkColor.fgbg("#00FF00","#880088") + ttk.TTkColor.BOLD] +
        [ttk.TTkColor.RST] * 3 +
        [ttk.TTkColor.bg("#0000FF")] +
        [ttk.TTkColor.RST] * 2 +
        [ttk.TTkColor.bg("#0000FF")] +
        [ttk.TTkColor.RST] +
        [ttk.TTkColor.bg("#0000FF")] +
        [ttk.TTkColor.RST] +
        [ttk.TTkColor.bg("#0000FF")] * 2 +
        [ttk.TTkColor.RST] * 3 +
        [ttk.TTkColor.bg("#0000FF")] * 3 +
        [ttk.TTkColor.RST] * 5 +
        #Rainbow-ish 2
        [ttk.TTkColor.fgbg("#00FF00","#880088")] * 2 +
        [ttk.TTkColor.fgbg("#00FF00","#FF00FF")] * 2 +
        [ttk.TTkColor.fgbg("#FFFF00","#0000FF")] * 2 +
        [ttk.TTkColor.fgbg("#FF0000","#00FFFF")] * 2 +
        [ttk.TTkColor.fgbg("#FF00FF","#00FF00")] * 2 +
        [ttk.TTkColor.fgbg("#0000FF","#FFFF00")] * 2 +
        [ttk.TTkColor.fgbg("#00FFFF","#FF0000")] * 2 +
        [ttk.TTkColor.fgbg("#00FFFF","#880000")] * 2 +
        [ttk.TTkColor.RST] * 2
    )

    # the exec function is called at each table line ('y')
    def exec(self, x:int, y:int, base_color:ttk.TTkColor) -> ttk.TTkColor:
        c =  CustomColorModifier.colors
        return c[y%len(c)]


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

# Custom color styles

# As First Style, I am defining an empty style only to show that
# the missing fields are taken from the class default style values
tableStyle1 = {'default': {}}

# As Second Style, I am using as
# Cell color:
#   TTkColor Dark Green ("#006600") alternating with a darker green ("#003300") through the TTkAlternateColor modifier
# Selection Color:
#   TTkColor Brighter green ("#00AA00")
# Hover Color: (the cell color under the mouse)
#   TTkColor Cyan-ish ("#00AAAA")
tableStyle2 = {'default': {
                    'color': ttk.TTkColor.bg("#006600", modifier=ttk.TTkAlternateColor(alternateColor=ttk.TTkColor.bg("#003300"))),
                    'selectedColor': ttk.TTkColor.bg("#00AA00"),
                    'hoverColor':    ttk.TTkColor.bg("#00AAAA")} }

# The third style is useful to check the results of
# alternating a color with the RST (Reset='\033[m0') property (the default cell color)
tableStyle3 = {'default': {
                    'color': ttk.TTkColor.bg("#660066", modifier=ttk.TTkAlternateColor(alternateColor=ttk.TTkColor.RST))} }

# In the fourth and more flamboyant style
# I am using the CustomColorModifier (fefined few lines ago)
# which is supposed to return a different color for each line
# all the other fields I hope are self explainatory
tableStyle4 = {'default': {
                    'color': ttk.TTkColor.bg("#000000", modifier=CustomColorModifier()),
                    'lineColor':      ttk.TTkColor.fg("#FFFF00"),
                    'headerColor':    ttk.TTkColor.fg("#FFFF00")+ttk.TTkColor.bg("#880000"),
                    'hoverColor':     ttk.TTkColor.bg("#AAAAAA"),
                    'selectedColor':  ttk.TTkColor.bg("#FFAA66"),
                    'separatorColor': ttk.TTkColor.fg("#330055")+ttk.TTkColor.bg("#660066")} }

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
table1 = ttk.TTkTable(tableModel=basicTableModel, addStyle=tableStyle1)
table2 = ttk.TTkTable(tableModel=basicTableModel, addStyle=tableStyle2)
table3 = ttk.TTkTable(tableModel=basicTableModel, addStyle=tableStyle3)
table4 = ttk.TTkTable(tableModel=basicTableModel, addStyle=tableStyle4)

root.layout().addWidget(table1,0,0)
root.layout().addWidget(table2,0,1)
root.layout().addWidget(table3,1,0)
root.layout().addWidget(table4,1,1)

# Adding a little touch, resizing the cols to its content
table1.resizeColumnsToContents()

# Start the main thread
root.mainloop()
