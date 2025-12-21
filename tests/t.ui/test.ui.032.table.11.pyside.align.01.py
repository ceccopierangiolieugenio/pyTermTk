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

'''
PySide6 QTableView Alignment Example (for comparison)
======================================================

This is a PySide6/Qt reference example showing how text alignment works
in QTableView. It's provided for comparison with TTkTable alignment.

Key Concepts:
- QAbstractTableModel for data handling
- Qt.DisplayRole for showing data
- Qt.TextAlignmentRole for alignment
- Combining flags: Qt.AlignLeft | Qt.AlignTop

Alignment Options in Qt:
- Horizontal: AlignLeft, AlignCenter, AlignRight, AlignJustify
- Vertical: AlignTop, AlignVCenter, AlignBottom

Compare this with TTkTable alignment in test.ui.032.table.13.alignment.*.py
to see how pyTermTk implements similar functionality in a terminal UI.
'''

from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtCore import Qt, QAbstractTableModel

class MyTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        value = self._data[index.row()][index.column()]

        if role == Qt.DisplayRole:
            return value


        if role == Qt.TextAlignmentRole:
            if index.column() == 0:
                return Qt.AlignLeft | Qt.AlignTop
            elif index.column() == 1:
                return Qt.AlignCenter
            elif index.column() == 2:
                return Qt.AlignRight | Qt.AlignVCenter

        return None

app = QApplication([])

data = [
    ["Left", "Center\npippo", "Right"],
    ["Apple", "Banana\npippo", "Cherry"],
    ["Dog", "Elephant\npippo", "Fox"]
]

model = MyTableModel(data)
view = QTableView()
view.setModel(model)
view.show()

app.exec()