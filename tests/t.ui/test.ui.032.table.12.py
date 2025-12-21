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

# Demo inspired from:
# https://www.daniweb.com/programming/software-development/code/447834/applying-pyside-s-qabstracttablemodel

'''
TTkTable Cell Edit Flags Example
=================================

This example demonstrates controlling cell editability through ItemFlags.

Key Features:
- Custom flags() method to control cell behavior per column
- ItemIsEnabled: Cell can receive focus
- ItemIsEditable: Cell content can be edited
- ItemIsSelectable: Cell can be selected
- Column 0: Only enabled and selectable (not editable)
- Column 1: Enabled and editable (can modify content)
- Other columns: Use default flags

Useful for creating tables with mixed editable/read-only columns,
like forms where some fields are locked and others are user-editable.
'''

import os
import sys
import csv
import re
import argparse
import operator
import json
import random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Full Screen (default)', action='store_true')
parser.add_argument('-w', help='Windowed',    action='store_true')
# parser.add_argument('-t',    help='Track Mouse', action='store_true')
parser.add_argument('--csv', help='Open CSV File', type=argparse.FileType('r'))

args = parser.parse_args()

fullScreen = not args.w
mouseTrack = True

# csvData = []
# if args.csv:
#     sniffer = csv.Sniffer()
#     has_header = sniffer.has_header(args.csv.read(2048))
#     args.csv.seek(0)
#     csvreader = csv.reader(args.csv)
#     for row in csvreader:
#         csvData.append(row)


imagesFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../ansi.images.json')
with open(imagesFile) as f:
    d = json.load(f)
    # Image exported by the Dumb Paint Tool - Removing the extra '\n' at the end
    diamond  = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['diamond' ])[0:-1])
    fire     = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['fire'    ])[0:-1])
    fireMini = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['fireMini'])[0:-1])
    key      = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['key'     ])[0:-1])
    peach    = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['peach'   ])[0:-1])
    pepper   = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['pepper'  ])[0:-1])
    python   = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['python'  ])[0:-1])
    ring     = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['ring'    ])[0:-1])
    sword    = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['sword'   ])[0:-1])
    whip     = ttk.TTkString(ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['whip'    ])[0:-1])
    tiles  = [diamond,fire,key,peach,ring,sword,whip]
    images = [fireMini,pepper,python]


class CustomColorModifier(ttk.TTkAlternateColor):
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
    def __init__(self):
        super().__init__()

    def exec(self, x:int, y:int, base_color:ttk.TTkColor) -> ttk.TTkColor:
        c =  CustomColorModifier.colors
        return c[y%len(c)]


class MyTableModel(ttk.TTkTableModelList):
    def __init__(self, mylist, size=None):
        self.size=size
        super().__init__(data=mylist)

    def rowCount(self):        return super().rowCount()    if not self.size else self.size[0]
    def columnCount(self):     return super().columnCount() if not self.size else self.size[1]

    def headerData(self, num, orientation):
        if orientation == ttk.TTkK.HORIZONTAL:
            prefix = ['H-aa','H-bb','H-cc','H-dd','H-ee','H-ff','H-gg','Parodi','H-hh',]
            return f"{prefix[num%len(prefix)]}:{num:03}"
        if orientation == ttk.TTkK.VERTICAL:
            prefix = ['aa','bb','cc','dd','ee','ff','gg','Euge']
            return f"{prefix[num%len(prefix)]}:{num:03}"
        return super().headerData(num, orientation)

    # Control cell behavior through flags
    # This method determines what the user can do with each cell
    def flags(self, row: int, col: int) -> ttk.TTkConstant.ItemFlag:
        if col==0:
            # Column 0: Read-only, can be selected but not edited
            return (
                ttk.TTkK.ItemFlag.ItemIsEnabled  |   # Can receive focus
                ttk.TTkK.ItemFlag.ItemIsSelectable ) # Can be selected
        if col==1:
            # Column 1: Editable, user can modify content
            return (
                ttk.TTkK.ItemFlag.ItemIsEnabled  |   # Can receive focus
                ttk.TTkK.ItemFlag.ItemIsEditable )   # Can be edited
        # Other columns use default flags
        return super().flags(row, col)


txt1 = "Text"
txt2 = txt1*5
txt3 = 'M1: '+' -M1\n'.join([txt1*2]*3)
txt4 = 'M2: '+' -M2\n'.join([txt1*5]*5)
txt5 = ttk.TTkString(txt4, ttk.TTkColor.RED + ttk.TTkColor.BG_YELLOW)

# use numbers for numeric data to sort properly
p1 = 4
p2 = 2
p3 = 2
p4 = 2

data_list1 = [[f"{y:03}\npippo\npeppo-ooo"]+[str(x) for x in range(10) ] for y in range(20)]
data_list1[3][3] = "abc\ndef\nghi\njkl"

data_list2 = [
    [f"{x:04}"]+
    [txt1,txt2,txt3,txt4,txt5]+
    [random.choice(tiles*p1+images*p2+[txt1,txt2]*p3+[123,234,345,567,890,123.001,234.02,345.3,567.04,890.01020304,1]*p4)]+
    [random.choice(tiles*p1+images*p2+[txt1,txt2]*p3+[123,234,345,567,890,123.001,234.02,345.3,567.04,890.01020304,1]*p4)]+
    [random.choice(tiles*p1+images*p2+[txt1,txt2]*p3+[123,234,345,567,890,123.001,234.02,345.3,567.04,890.01020304,1]*p4)]+
    [random.choice(tiles*p1+images*p2+[txt1,txt2]*p3+[123,234,345,567,890,123.001,234.02,345.3,567.04,890.01020304,1]*p4)]+
    [random.choice(tiles*p1+images*p2+[txt1,txt2]*p3+[123,234,345,567,890,123.001,234.02,345.3,567.04,890.01020304,1]*p4)]+
    [y       for y in range(10)]+
    [y+0.123 for y in range(10)]
                 for x in range(5000)]

data_list3 = [
    [txt1,txt2,txt3]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [y       for y in range(10)]+
    [y+0.123 for y in range(10)]
                 for x in range(1000)]

data_list4 = [
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]+
    [random.choice(tiles*p1)]
                 for x in range(30)]


root = ttk.TTk(title="pyTermTk Table Demo",
               mouseTrack=mouseTrack,
               sigmask=(
                    ttk.TTkTerm.Sigmask.CTRL_Q |
                    ttk.TTkTerm.Sigmask.CTRL_S |
                    ttk.TTkTerm.Sigmask.CTRL_C |
                    ttk.TTkTerm.Sigmask.CTRL_Z ))

if fullScreen:
    rootTable = root
    root.setLayout(ttk.TTkGridLayout())
else:
    rootTable = ttk.TTkWindow(parent=root,pos = (0,0), size=(150,40), title="Test Table 1", layout=ttk.TTkGridLayout(), border=True)

splitter = ttk.TTkSplitter(parent=rootTable,orientation=ttk.TTkK.VERTICAL)



table_model1 = MyTableModel(data_list1)
table_model2 = MyTableModel(data_list2)
table_model3 = MyTableModel(data_list3)
table_model4 = MyTableModel(data_list4)
# table_model = MyTableModel(data_list, size=(15,10))

table = ttk.TTkTable(parent=splitter, tableModel=table_model1)
# table = ttk.TTkTable(parent=splitter)

# # set column width to fit contents (set font first!)
# table.resizeColumnsToContents()
# # enable sorting
# table.setSortingEnabled(True)

table.setSelection((0,0),(2,2),ttk.TTkK.TTkItemSelectionModel.Select)
table.setSelection((3,0),(1,2),ttk.TTkK.TTkItemSelectionModel.Select)

table.setSelection((1,3),(2,4),ttk.TTkK.TTkItemSelectionModel.Select)
table.setSelection((2,5),(2,4),ttk.TTkK.TTkItemSelectionModel.Select)
table.setSelection((0,9),(2,3),ttk.TTkK.TTkItemSelectionModel.Select)

table.setSelection((1,59),(1,2),ttk.TTkK.TTkItemSelectionModel.Select)
table.setSelection((3,59),(1,2),ttk.TTkK.TTkItemSelectionModel.Select)

controlAndLogsSplitter = ttk.TTkSplitter()

splitter.addWidget(controlAndLogsSplitter,size=7,title="LOGS")

controls  = ttk.TTkContainer()
debugView = ttk.TTkContainer()

defaultStyle = table.style()['default']

tableStyle1 = {'default': defaultStyle|{'color': ttk.TTkColor.RST} }
tableStyle2 = {'default': defaultStyle|{'color': ttk.TTkColor.bg("#000066", modifier=ttk.TTkAlternateColor(alternateColor=ttk.TTkColor.BG_BLUE))} }
tableStyle3 = {'default': defaultStyle|{
                    'color': ttk.TTkColor.bg("#006600", modifier=ttk.TTkAlternateColor(alternateColor=ttk.TTkColor.bg("#003300"))),
                    'selectedColor': ttk.TTkColor.bg("#00AA00"),
                    'hoverColor':    ttk.TTkColor.bg("#00AAAA")} }
tableStyle4 = {'default': defaultStyle|{'color': ttk.TTkColor.bg("#660066", modifier=ttk.TTkAlternateColor(alternateColor=ttk.TTkColor.RST))} }
tableStyle5 = {'default': defaultStyle|{
                    'color': ttk.TTkColor.bg("#000000", modifier=CustomColorModifier()),
                    'lineColor':      ttk.TTkColor.fg("#FFFF00"),
                    'headerColor':    ttk.TTkColor.fg("#FFFF00")+ttk.TTkColor.bg("#660066"),
                    'hoverColor':     ttk.TTkColor.bg("#AAAAAA"),
                    'selectedColor':  ttk.TTkColor.bg("#FFAA66"),
                    'separatorColor': ttk.TTkColor.fg("#330055")+ttk.TTkColor.bg("#660066")} }


#########################
# Define the Controls   #
#########################

quitBtn = ttk.TTkButton(parent=controls, pos=(0,0), size=(5,6), text="Q\nU\nI\nT")
quitBtn.clicked.connect(root.quit)

offsetQuit = 6

# Header Checkboxes
ttk.TTkLabel(parent=controls, pos=(offsetQuit,0), text="Header:")
ht = ttk.TTkCheckbox(parent=controls, pos=( offsetQuit  ,1), size=(8,1), text=' Top ',checked=True)
hl = ttk.TTkCheckbox(parent=controls, pos=( offsetQuit+9,1), size=(8,1), text=' Left',checked=True)

ht.toggled.connect(table.horizontalHeader().setVisible)
hl.toggled.connect(table.verticalHeader().setVisible)

# Lines/Separator Checkboxes
ttk.TTkLabel(parent=controls, pos=(offsetQuit,2), text="Lines:")
vli = ttk.TTkCheckbox(parent=controls, pos=(offsetQuit  ,3), size=(5,1), text=' V',checked=True)
hli = ttk.TTkCheckbox(parent=controls, pos=(offsetQuit+9,3), size=(5,1), text=' H',checked=True)

vli.toggled.connect(table.setVSeparatorVisibility)
hli.toggled.connect(table.setHSeparatorVisibility)


# Themes Control
t1 = ttk.TTkRadioButton(parent=controls, pos=(offsetQuit+19,1), size=(11,1), text=' Theme 1', radiogroup='Themes', checked=True)
t2 = ttk.TTkRadioButton(parent=controls, pos=(offsetQuit+19,2), size=(11,1), text=' Theme 2', radiogroup='Themes')
t3 = ttk.TTkRadioButton(parent=controls, pos=(offsetQuit+19,3), size=(11,1), text=' Theme 3', radiogroup='Themes')
t4 = ttk.TTkRadioButton(parent=controls, pos=(offsetQuit+19,4), size=(11,1), text=' Theme 4', radiogroup='Themes')
t5 = ttk.TTkRadioButton(parent=controls, pos=(offsetQuit+19,5), size=(11,1), text=' Theme 5', radiogroup='Themes')

t1.clicked.connect(lambda : table.mergeStyle(tableStyle1))
t2.clicked.connect(lambda : table.mergeStyle(tableStyle2))
t3.clicked.connect(lambda : table.mergeStyle(tableStyle3))
t4.clicked.connect(lambda : table.mergeStyle(tableStyle4))
t5.clicked.connect(lambda : table.mergeStyle(tableStyle5))


# Model Picker
m1 = ttk.TTkRadioButton(parent=controls, pos=(offsetQuit+32,0), size=(11,1), text=' Model 1', radiogroup='Models', checked=True)
m2 = ttk.TTkRadioButton(parent=controls, pos=(offsetQuit+32,1), size=(11,1), text=' Model 2', radiogroup='Models')
m3 = ttk.TTkRadioButton(parent=controls, pos=(offsetQuit+32,2), size=(11,1), text=' Model 3', radiogroup='Models')
m4 = ttk.TTkRadioButton(parent=controls, pos=(offsetQuit+32,3), size=(11,1), text=' Model 4', radiogroup='Models')

m1.clicked.connect(lambda : table.setModel(table_model1))
m2.clicked.connect(lambda : table.setModel(table_model2))
m3.clicked.connect(lambda : table.setModel(table_model3))
m4.clicked.connect(lambda : table.setModel(table_model4))

if args.csv:
    table_model_csv = ttk.TTkTableModelCSV(fd=args.csv)
    m_csv = ttk.TTkRadioButton(parent=controls, pos=(offsetQuit+32,4), size=(11,1), text=' CSV', radiogroup='Models')
    m_csv.clicked.connect(lambda : table.setModel(table_model_csv))



# Resize Button
rcb = ttk.TTkButton(parent=controls, pos=(offsetQuit  ,5), size=( 3,1), text="C", border=False)
rrb = ttk.TTkButton(parent=controls, pos=(offsetQuit+3,5), size=( 3,1), text="R", border=False)
rb  = ttk.TTkButton(parent=controls, pos=(offsetQuit+6,5), size=(11,1), text="Resize", border=False)

rrb.clicked.connect(table.resizeRowsToContents)
rcb.clicked.connect(table.resizeColumnsToContents)
rb.clicked.connect( table.resizeRowsToContents)
rb.clicked.connect( table.resizeColumnsToContents)

cbs = ttk.TTkCheckbox(parent=controls, pos=(offsetQuit+32,5), size=(8,1), text='-Sort', checked=False)

cbs.toggled.connect(table.setSortingEnabled)

wtb = ttk.TTkButton(parent=controls, pos=(offsetQuit+41,4), size=( 4,1), text="👌", border=False)
wkb = ttk.TTkButton(parent=controls, pos=(offsetQuit+41,5), size=( 4,1), text="🤌", border=False)

btn_ins_row = ttk.TTkButton(parent=controls, pos=(offsetQuit+45,0), size=( 4,1), text="❎", border=False)
btn_del_row = ttk.TTkButton(parent=controls, pos=(offsetQuit+45,1), size=( 4,1), text="❌", border=False)
btn_ins_col = ttk.TTkButton(parent=controls, pos=(offsetQuit+45,3), size=( 4,1), text="❎", border=False)
btn_del_col = ttk.TTkButton(parent=controls, pos=(offsetQuit+45,4), size=( 4,1), text="❌", border=False)

#########################
# Define the DebugView  #
#########################

debugViewLayout = ttk.TTkGridLayout()
debugView.setLayout(debugViewLayout)

debugViewLayout.addWidget(l_ch:=ttk.TTkLabel(text="Cell Changed: xxxx"),0,0)
debugViewLayout.addWidget(l_cl:=ttk.TTkLabel(text="Cell Clicked: xxxx"),1,0)
debugViewLayout.addWidget(l_dc:=ttk.TTkLabel(text="DoubleClked : xxxx"),2,0)
debugViewLayout.addWidget(l_ce:=ttk.TTkLabel(text="Cell Entered: xxxx"),3,0)
debugViewLayout.addWidget(l_cc:=ttk.TTkLabel(text="Changed:      xxxx"),4,0)
debugViewLayout.addWidget(t_ed:=ttk.TTkTextEdit(lineNumber=True),0,1,6,1)

table.cellChanged.connect(       lambda r,c:         l_ch.setText(f"Cell Changed: {r,c}"))
table.cellClicked.connect(       lambda r,c:         l_cl.setText(f"Cell Clicked: {r,c}"))
table.cellEntered.connect(       lambda r,c:         l_ce.setText(f"Cell Entered: {r,c}"))
table.cellDoubleClicked.connect( lambda r,c:         l_dc.setText(f"DoubleClked : {r,c}"))
table.currentCellChanged.connect(lambda cr,cc,pr,pc: l_cc.setText(f"Changed:{cr,cc}<-{pr,pc}"))

table.cellEntered.connect(       lambda r,c:         t_ed.setText(table.model().ttkStringData(r,c)))

controlAndLogsSplitter.addWidget(controls, size=55)
controlAndLogsSplitter.addWidget(debugView, size=60)
controlAndLogsSplitter.addWidget(ttk.TTkLogViewer())

@ttk.pyTTkSlot()
def _showWinKey():
    winKey = ttk.TTkWindow(title="KeyPress",layout=ttk.TTkGridLayout(), size=(80,7))
    winKey.layout().addWidget(ttk.TTkKeyPressView(maxHeight=3))
    ttk.TTkHelper.overlay(None, winKey, 10, 4, toolWindow=True)

wkb.clicked.connect(_showWinKey)

@ttk.pyTTkSlot()
def _showWinText():
    winText = ttk.TTkWindow(title="Notepad",layout=ttk.TTkGridLayout(), size=(80,7))
    winText.layout().addWidget(ttk.TTkTextEdit(lineNumber=True, readOnly=False))
    ttk.TTkHelper.overlay(None, winText, 50, 20, toolWindow=True)

@ttk.pyTTkSlot()
def _insertRows():
    _model = table.model()
    _model.insertRows(3,2)

@ttk.pyTTkSlot()
def _deleteRows():
    _model = table.model()
    _model.removeRows(0,5)

@ttk.pyTTkSlot()
def _insertCols():
    _model = table.model()
    _model.insertColumns(3,2)

@ttk.pyTTkSlot()
def _deleteCols():
    _model = table.model()
    _model.removeColumns(0,5)

btn_ins_row.clicked.connect(_insertRows)
btn_del_row.clicked.connect(_deleteRows)
btn_ins_col.clicked.connect(_insertCols)
btn_del_col.clicked.connect(_deleteCols)

wtb.clicked.connect(_showWinText)

table.setFocus()

root.mainloop()