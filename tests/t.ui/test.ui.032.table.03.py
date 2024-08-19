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

import os
import sys
import argparse
import operator
import json

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

imagesFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'ansi.images.json')
with open(imagesFile) as f:
    d = json.load(f)
    # Image exported by the Dumb Paint Tool
    pepper   = ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['pepper'])
    python   = ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['python'])
    fire     = ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['fire'])
    fireMini = ttk.TTkUtil.base64_deflate_2_obj(d['compressed']['fireMini'])


class MyTableModel(ttk.TTkAbstractTableModel):
    def __init__(self, mylist, header, *args):
        super().__init__(*args)
        self.mylist = mylist
        self.header = header
    def rowCount(self):
        return len(self.mylist)
    def columnCount(self):
        return len(self.mylist[0])
    def data(self, row, col):
        return self.mylist[row][col]
    def headerData(self, num, orientation):
        if orientation == ttk.TTkK.HORIZONTAL:
            return self.header[num]
        if orientation == ttk.TTkK.VERTICAL:
            prefix = ['aa','bb','cc','dd','ee','ff','gg','Euge']
            return f"{prefix[num%len(prefix)]}:{num:03}"
        return super().headerData(num, orientation)
    def sort(self, col, order):
        """sort table by given column number col"""
        # self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == ttk.TTkK.DescendingOrder:
            self.mylist.reverse()
        self.dataChanged.emit()
        # self.layoutChanged.emit()
        # self.emit(SIGNAL("layoutChanged()"))

# the solvent data ...
header = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)','a','b','c','d','e','f','aa','bb','cc','dd','ee','ff','gg','hh','ii','jj']
# use numbers for numeric data to sort properly
data_list = [
    ('ACETIC ACID', 117.9, 16.7, 1.049,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ACETIC ANHYDRIDE', 140.1, -73.1, 1.087,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ACETONE', 56.3, -94.7, 0.791,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ACETONITRILE', 81.6, -43.8, 0.786,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    (python, 34.5, -116.2, fire,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('DIMETHYLACETAMIDE', 166.1, -20.0, fireMini,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('DIMETHYLFORMAMIDE', 153.3, pepper, 0.944,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ANISOLE', 154.2, -37.0, 0.995,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    (' (1) Miultiline\nAnother Line\nAnd another\nAnd ANOTHER\nLast ONE ', 99.2, pepper, 0.692,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('BENZYL ALCOHOL', 205.4, -15.3, 1.045,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('BENZYL BENZOATE', 323.5, 19.4, 1.112,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    (' (2) Long Line Very Long Long Long Long Long Long ', 99.2, -107.4, 0.692,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('BUTYL ALCOHOL NORMAL', 117.7, -88.6, 0.81,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('BUTYL ALCOHOL SEC', 99.6, -114.7, 0.805,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('BUTYL ALCOHOL TERTIARY', 82.2, 25.5, 0.786,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('CHLOROBENZENE', 131.7, -45.6, 1.111,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('CYCLOHEXANE', 80.7, 6.6, 0.779,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('CYCLOHEXANOL', 161.1, 25.1, 0.971,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('CYCLOHEXANONE', 155.2, -47.0, 0.947,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('DICHLOROETHANE 1 2', 83.5, -35.7, 1.246,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('DICHLOROMETHANE', 39.8, -95.1, 1.325,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('DIETHYL ETHER', 34.5, -116.2, 0.715,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('DIMETHYLSULFOXIDE', 189.4, 18.5, 1.102,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('DIOXANE 1 4', 101.3, 11.8, 1.034,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('DIPHENYL ETHER', 258.3, 26.9, 1.066,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ETHYL ACETATE', 77.1, -83.9, 0.902,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ETHYL ALCOHOL', 78.3, -114.1, 0.789,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ETHYL DIGLYME', 188.2, -45.0, 0.906,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ETHYLENE CARBONATE', 248.3, 36.4, 1.321,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ETHYLENE GLYCOL', 197.3, -13.2, 1.114,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('FORMIC ACID', 100.6, 8.3, 1.22,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('HEPTANE', 98.4, -90.6, 0.684,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('HEXAMETHYL PHOSPHORAMIDE', 233.2, 7.2, 1.027,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('HEXANE', 68.7, -95.3, 0.659,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ISO OCTANE', 99.2, -107.4, 0.692,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ISOPROPYL ACETATE', 88.6, -73.4, 0.872,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('ISOPROPYL ALCOHOL', 82.3, -88.0, 0.785,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('METHYL ALCOHOL', 64.7, -97.7, 0.791,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('METHYL ETHYLKETONE', 79.6, -86.7, 0.805,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('METHYL ISOBUTYL KETONE', 116.5, -84.0, 0.798,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('METHYL T-BUTYL ETHER', 55.5, -10.0, 0.74,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('METHYLPYRROLIDINONE N', 203.2, -23.5, 1.027,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('MORPHOLINE', 128.9, -3.1, 1.0,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('NITROBENZENE', 210.8, 5.7, 1.208,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('NITROMETHANE', 101.2, -28.5, 1.131,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('PENTANE', 36.1, -129.7, 0.626,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('PHENOL', 181.8, 40.9, 1.066,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('PROPANENITRILE', 97.1, -92.8, 0.782,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('PROPIONIC ACID', 141.1, -20.7, 0.993,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('PROPIONITRILE', 97.4, -92.8, 0.782,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('PROPYLENE GLYCOL', 187.6, -60.1, 1.04,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('PYRIDINE', 115.4, -41.6, 0.978,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('SULFOLANE', 287.3, 28.5, 1.262,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('TETRAHYDROFURAN', 66.2, -108.5, 0.887,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('TOLUENE', 110.6, -94.9, 0.867,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('TRIETHYL PHOSPHATE', 215.4, -56.4, 1.072,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('TRIETHYLAMINE', 89.5, -114.7, 0.726,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('TRIFLUOROACETIC ACID', 71.8, -15.3, 1.489,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('WATER', 100.0, 0.0, 1.0,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('XYLENES', 139.1, -47.8, 0.86,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0),
    ('!!!END!!!', 123.4, -5432.1, 0.123,123,123,123,123,123,123,1,2,3,4,5,6,7,8,9,0)]

class CustomColorModifier(ttk.TTkAlternateColor):
    colors = [
        ttk.TTkColor.bg("#000066"),
        ttk.TTkColor.bg("#0000FF"),
        ttk.TTkColor.bg("#000066"),
        ttk.TTkColor.bg("#0000FF"),
        ttk.TTkColor.bg("#003300"),
        ttk.TTkColor.bg("#006600"),
        ttk.TTkColor.bg("#000066"),
        ttk.TTkColor.bg("#0000FF"),
        ttk.TTkColor.bg("#000066"),
        ttk.TTkColor.RST,
        ttk.TTkColor.RST,
        ttk.TTkColor.RST,
        ttk.TTkColor.fgbg("#00FFFF","#880000") + ttk.TTkColor.BOLD,
        ttk.TTkColor.fgbg("#00FFFF","#FF0000") + ttk.TTkColor.BOLD,
        ttk.TTkColor.fgbg("#0000FF","#FFFF00") + ttk.TTkColor.BOLD,
        ttk.TTkColor.fgbg("#FF00FF","#00FF00") + ttk.TTkColor.BOLD,
        ttk.TTkColor.fgbg("#FF0000","#00FFFF") + ttk.TTkColor.BOLD,
        ttk.TTkColor.fgbg("#FFFF00","#0000FF") + ttk.TTkColor.BOLD,
        ttk.TTkColor.fgbg("#FFFF00","#0000FF") + ttk.TTkColor.BOLD,
        ttk.TTkColor.fgbg("#00FF00","#FF00FF") + ttk.TTkColor.BOLD,
        ttk.TTkColor.fgbg("#00FF00","#880088") + ttk.TTkColor.BOLD,
        ttk.TTkColor.RST,
        ttk.TTkColor.RST,
        ttk.TTkColor.bg("#0000FF"),
        ttk.TTkColor.RST,
        ttk.TTkColor.RST,
        ttk.TTkColor.bg("#0000FF"),
        ttk.TTkColor.RST,
        ttk.TTkColor.bg("#0000FF"),
        ttk.TTkColor.bg("#0000FF"),
        ttk.TTkColor.RST,
        ttk.TTkColor.RST,
        ttk.TTkColor.RST,
        ttk.TTkColor.bg("#0000FF"),
        ttk.TTkColor.bg("#0000FF"),
        ttk.TTkColor.bg("#0000FF"),
        ttk.TTkColor.RST,
        ttk.TTkColor.RST,
        ttk.TTkColor.RST,
        ttk.TTkColor.RST,
    ]
    def __init__(self):
        super().__init__()

    def exec(self, x:int, y:int, base_color:ttk.TTkColor) -> ttk.TTkColor:
        c =  CustomColorModifier.colors
        return c[y%len(c)]

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Full Screen', action='store_true')
parser.add_argument('-t', help='Track Mouse', action='store_true')
args = parser.parse_args()

fullScreen = args.f
mouseTrack = args.t

root = ttk.TTk(title="pyTermTk Table Demo", mouseTrack=mouseTrack)
if fullScreen:
    rootTable = root
    root.setLayout(ttk.TTkGridLayout())
else:
    rootTable = ttk.TTkWindow(parent=root,pos = (0,0), size=(150,40), title="Test Table 1", layout=ttk.TTkGridLayout(), border=True)

splitter = ttk.TTkSplitter(parent=rootTable,orientation=ttk.TTkK.VERTICAL)

tableStyle = {'default': {'color':ttk.TTkColor.bg("#000000", modifier=CustomColorModifier())} }

table_model = MyTableModel(data_list, header)

table = ttk.TTkTable(parent=splitter, tableModel=table_model)
table.mergeStyle(tableStyle)

# set column width to fit contents (set font first!)
table.resizeColumnsToContents()
# enable sorting
table.setSortingEnabled(True)

table.setSelection((0,0),(2,2),1)
table.setSelection((3,0),(1,2),1)

table.setSelection((1,3),(2,4),1)
table.setSelection((2,5),(2,4),1)
table.setSelection((0,9),(2,3),1)

table.setSelection((1,59),(1,2),1)
table.setSelection((3,59),(1,2),1)

splitter.addWidget(ttk.TTkLogViewer(),size=10,title="LOGS")

root.mainloop()