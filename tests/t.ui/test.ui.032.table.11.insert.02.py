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

from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

app = QApplication([])

# Create the model with 3 rows and 2 columns
model = QStandardItemModel(3, 2)
model.setHorizontalHeaderLabels(["Name", "Age"])

# Fill initial data
model.setItem(0, 0, QStandardItem("Alice"))
model.setItem(1, 0, QStandardItem("Bob"))
model.setItem(2, 0, QStandardItem("Charlie"))

model.setItem(0, 1, QStandardItem("25"))
model.setItem(1, 1, QStandardItem("30"))
model.setItem(2, 1, QStandardItem("22"))

# Insert a new column at index 2
model.insertColumn(2)

# Add items to the new column
roles = ["Engineer", "Designer", "Manager"]
for row, role in enumerate(roles):
    model.setItem(row, 2, QStandardItem(role))

# Set header for the new column
model.setHeaderData(2, Qt.Horizontal, "Role")

# Create and show the table view
view = QTableView()
view.setModel(model)
view.show()

app.exec()