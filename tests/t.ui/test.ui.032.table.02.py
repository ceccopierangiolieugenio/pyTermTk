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
TTkTable Advanced Example with Images and Multi-line Text
=========================================================

This example extends the basic table functionality by demonstrating:

Key Features:
- Displaying ANSI art images within table cells
- Multi-line text in cells
- Long text handling
- Custom vertical header labels with prefixes
- Mixed content types (text, numbers, and images)
- Custom color modifiers for alternating row colors

The table contains chemical solvents data with embedded images and
demonstrates how TTkTable handles complex cell content.
'''

import os
import sys
import argparse
import operator
import json

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

# Load ANSI art images from JSON file
# These images were created using the Dumb Paint Tool and can be displayed in table cells
imagesFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'ansi.images.json')
with open(imagesFile) as f:
    d = json.load(f)
    # Decompress base64-encoded ANSI art images
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
    # Provide custom header labels for both columns and rows
    def headerData(self, num, orientation):
        if orientation == ttk.TTkK.HORIZONTAL:
            return self.header[num]  # Column headers
        if orientation == ttk.TTkK.VERTICAL:
            # Create custom row headers with rotating prefixes
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
header = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)']
# use numbers for numeric data to sort properly
data_list = [
    ('ACETIC ACID', 117.9, 16.7, 1.049),
    ('ACETIC ANHYDRIDE', 140.1, -73.1, 1.087),
    ('ACETONE', 56.3, -94.7, 0.791),
    ('ACETONITRILE', 81.6, -43.8, 0.786),
    (python, 34.5, -116.2, fire),
    ('DIMETHYLACETAMIDE', 166.1, -20.0, fireMini),
    ('DIMETHYLFORMAMIDE', 153.3, pepper, 0.944),
    ('ANISOLE', 154.2, -37.0, 0.995),
    (' (1) Miultiline\nAnother Line\nAnd another\nAnd ANOTHER\nLast ONE ', 99.2, pepper, 0.692),
    ('BENZYL ALCOHOL', 205.4, -15.3, 1.045),
    ('BENZYL BENZOATE', 323.5, 19.4, 1.112),
    (' (2) Long Line Very Long Long Long Long Long Long ', 99.2, -107.4, 0.692),
    ('BUTYL ALCOHOL NORMAL', 117.7, -88.6, 0.81),
    ('BUTYL ALCOHOL SEC', 99.6, -114.7, 0.805),
    ('BUTYL ALCOHOL TERTIARY', 82.2, 25.5, 0.786),
    ('CHLOROBENZENE', 131.7, -45.6, 1.111),
    ('CYCLOHEXANE', 80.7, 6.6, 0.779),
    ('CYCLOHEXANOL', 161.1, 25.1, 0.971),
    ('CYCLOHEXANONE', 155.2, -47.0, 0.947),
    ('DICHLOROETHANE 1 2', 83.5, -35.7, 1.246),
    ('DICHLOROMETHANE', 39.8, -95.1, 1.325),
    ('DIETHYL ETHER', 34.5, -116.2, 0.715),
    ('DIMETHYLSULFOXIDE', 189.4, 18.5, 1.102),
    ('DIOXANE 1 4', 101.3, 11.8, 1.034),
    ('DIPHENYL ETHER', 258.3, 26.9, 1.066),
    ('ETHYL ACETATE', 77.1, -83.9, 0.902),
    ('ETHYL ALCOHOL', 78.3, -114.1, 0.789),
    ('ETHYL DIGLYME', 188.2, -45.0, 0.906),
    ('ETHYLENE CARBONATE', 248.3, 36.4, 1.321),
    ('ETHYLENE GLYCOL', 197.3, -13.2, 1.114),
    ('FORMIC ACID', 100.6, 8.3, 1.22),
    ('HEPTANE', 98.4, -90.6, 0.684),
    ('HEXAMETHYL PHOSPHORAMIDE', 233.2, 7.2, 1.027),
    ('HEXANE', 68.7, -95.3, 0.659),
    ('ISO OCTANE', 99.2, -107.4, 0.692),
    ('ISOPROPYL ACETATE', 88.6, -73.4, 0.872),
    ('ISOPROPYL ALCOHOL', 82.3, -88.0, 0.785),
    ('METHYL ALCOHOL', 64.7, -97.7, 0.791),
    ('METHYL ETHYLKETONE', 79.6, -86.7, 0.805),
    ('METHYL ISOBUTYL KETONE', 116.5, -84.0, 0.798),
    ('METHYL T-BUTYL ETHER', 55.5, -10.0, 0.74),
    ('METHYLPYRROLIDINONE N', 203.2, -23.5, 1.027),
    ('MORPHOLINE', 128.9, -3.1, 1.0),
    ('NITROBENZENE', 210.8, 5.7, 1.208),
    ('NITROMETHANE', 101.2, -28.5, 1.131),
    ('PENTANE', 36.1, -129.7, 0.626),
    ('PHENOL', 181.8, 40.9, 1.066),
    ('PROPANENITRILE', 97.1, -92.8, 0.782),
    ('PROPIONIC ACID', 141.1, -20.7, 0.993),
    ('PROPIONITRILE', 97.4, -92.8, 0.782),
    ('PROPYLENE GLYCOL', 187.6, -60.1, 1.04),
    ('PYRIDINE', 115.4, -41.6, 0.978),
    ('SULFOLANE', 287.3, 28.5, 1.262),
    ('TETRAHYDROFURAN', 66.2, -108.5, 0.887),
    ('TOLUENE', 110.6, -94.9, 0.867),
    ('TRIETHYL PHOSPHATE', 215.4, -56.4, 1.072),
    ('TRIETHYLAMINE', 89.5, -114.7, 0.726),
    ('TRIFLUOROACETIC ACID', 71.8, -15.3, 1.489),
    ('WATER', 100.0, 0.0, 1.0),
    ('XYLENES', 139.1, -47.8, 0.86),
    ('!!!END!!!', 123.4, -5432.1, 0.123)]

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
parser.add_argument('-f', help='Full Screen (default)', action='store_true')
parser.add_argument('-w', help='Windowed',    action='store_true')
parser.add_argument('-t', help='Track Mouse', action='store_true')
args = parser.parse_args()

fullScreen = not args.w
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