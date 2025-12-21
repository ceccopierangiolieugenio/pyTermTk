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
TTkTableModelSQLite3 Example
=============================

This example demonstrates using TTkTableModelSQLite3 to display data
directly from an SQLite3 database.

Key Features:
- Direct SQLite3 database integration with TTkTableModelSQLite3
- Automatic table loading from database
- Database creation if file doesn't exist
- Column sorting support
- Automatic column resizing
- No need to load all data into memory (efficient for large tables)

Usage:
  python test.ui.032.table.10.sqlite.py mydatabase.db  # Use existing DB
  python test.ui.032.table.10.sqlite.py newfile.db     # Create new DB

The database will be created with sample user data if it doesn't exist.
'''

import os
import sys
import csv
import re
import argparse
import operator
import json
import random
import sqlite3

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

words = [
    "Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed",
    "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna",
    "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation",
    "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat.",
    "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit",
    "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum."]


parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Full Screen (default)', action='store_true')
parser.add_argument('-w', help='Windowed',    action='store_true')
# parser.add_argument('-t',    help='Track Mouse', action='store_true')
parser.add_argument('file', help='Open SQlite3 File', type=str)

args = parser.parse_args()

fullScreen = not args.w
mouseTrack = True
path = args.file

# Helper function to create a sample SQLite database with test data
def _createDB(fileName):
    # Connect to a database (creates the file if it doesn't exist)
    conn = sqlite3.connect(fileName)

    # Create a cursor object for executing SQL commands
    cur = conn.cursor()

    # Create a users table with various column types
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name     TEXT,
                    surname  TEXT,
                    location TEXT,
                    code  INTEGER,
                    age   INTEGER)''')
    # Insert sample data using parameterized queries (prevents SQL injection)
    sqlDef = "INSERT INTO users (name, surname, location, code, age) VALUES (?, ?, ?, ?, ?)"
    # Generate 20 rows of random data
    for _ in range(20):
        cur.execute(sqlDef,
                (random.choice(words), random.choice(words),  # Random name and surname
                 random.choice(words),                         # Random location
                 random.randint(0x10000,0x100000000), random.randint(18,70)))  # Random code and age

    # Commit changes to the database
    conn.commit()
    # Close the connection
    conn.close()

# Create the database file with sample data if it doesn't already exist
if not os.path.exists(path):
    _createDB(path)

root = ttk.TTk(title="pyTermTk Table Demo",
               mouseTrack=mouseTrack,
               sigmask=(
                    ttk.TTkTerm.Sigmask.CTRL_Q |
                    ttk.TTkTerm.Sigmask.CTRL_S |
                    # ttk.TTkTerm.Sigmask.CTRL_C |
                    ttk.TTkTerm.Sigmask.CTRL_Z ))

if fullScreen:
    rootTable = root
    root.setLayout(ttk.TTkGridLayout())
else:
    rootTable = ttk.TTkWindow(parent=root,pos = (0,0), size=(150,40), title="Test Table", layout=ttk.TTkGridLayout(), border=True)

# Create a table model that connects directly to the SQLite database
# This model reads data on-demand, making it efficient for large tables
basicTableModel = ttk.TTkTableModelSQLite3(fileName=path, table='users')

# Create the table widget with the SQLite model and enable sorting
table = ttk.TTkTable(parent=root, tableModel=basicTableModel, sortingEnabled=True)

# Automatically resize columns to fit their content
table.resizeColumnsToContents()

root.mainloop()