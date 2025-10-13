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

from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem

app = QApplication([])

# Create a table with 3 rows and 2 columns
table = QTableWidget(3, 2)
table.setHorizontalHeaderLabels(["Name", "Age"])

# Fill initial data
table.setItem(0, 0, QTableWidgetItem("Alice"))
table.setItem(1, 0, QTableWidgetItem("Bob"))
table.setItem(2, 0, QTableWidgetItem("Charlie"))

table.setItem(0, 1, QTableWidgetItem("25"))
table.setItem(1, 1, QTableWidgetItem("30"))
table.setItem(2, 1, QTableWidgetItem("22"))

# Create items for the new column
new_items1 = [
    QTableWidgetItem("Engineer"),
    QTableWidgetItem("Designer"),
    QTableWidgetItem("Manager"),
    QTableWidgetItem("Pippo")
]

new_items2 = [
    QTableWidgetItem("Engineer"),
    QTableWidgetItem("Designer"),
    QTableWidgetItem("Manager"),
    QTableWidgetItem("Pippo")
]

# Insert new column at index 2 with items
table.insertColumn(2)
for row, item in enumerate(new_items1):
    table.setItem(row, 2, item)

table.setHorizontalHeaderItem(2, QTableWidgetItem("Role"))

table.show()
app.exec()