#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import os
import re
import sys, os
import random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

def filtersFormLayout():
    '''
    This form is inspired by glogg "Filters..." form
    '''

    leftRightLayout = ttk.TTkHBoxLayout()
    leftLayout = ttk.TTkGridLayout()
    rightLayout = ttk.TTkGridLayout()
    leftRightLayout.addItem(leftLayout)
    leftRightLayout.addItem(rightLayout)

    frameFilters = ttk.TTkFrame(border=True, layout=ttk.TTkGridLayout())
    leftLayout.addWidget(frameFilters,0,0,1,5)

    listFilters = ttk.TTkList(parent=frameFilters)

    addButton    = ttk.TTkButton(text="+",maxWidth=3)
    removeButton = ttk.TTkButton(text="-",maxWidth=3)
    upButton     = ttk.TTkButton(text="▲",maxWidth=3)
    downButton   = ttk.TTkButton(text="▼",maxWidth=3)

    leftLayout.addWidget(addButton       ,1,0)
    leftLayout.addWidget(removeButton    ,1,1)
    leftLayout.addWidget(ttk.TTkSpacer() ,1,2)
    leftLayout.addWidget(upButton        ,1,3)
    leftLayout.addWidget(downButton      ,1,4)

    listFilters.addItem(f"Pythone|python")
    listFilters.addItem(f"Pythone|python1")
    listFilters.addItem(f"Pythone|python2")
    listFilters.addItem(f"Pythone|python3")
    listFilters.addItem(f"Pythone|python4")
    listFilters.addItem(f"Pythone|python4")
    listFilters.addItem(f"Pythone|python4")
    listFilters.addItem(f"Pythone|python4")
    listFilters.addItem(f"Pythone|python4")
    listFilters.addItem(f"Pythone|python4")
    listFilters.addItem(f"Pythone|python4")
    listFilters.addItem(f"Pythone|python4")
    listFilters.addItem(f"Pythone|python4")
    listFilters.addItem(f"Pythone|python4")

    return leftRightLayout

def preferencesForm(root=None):
    preferencesLayout = ttk.TTkGridLayout(columnMinWidth=1)
    frame = ttk.TTkFrame(parent=root, layout=preferencesLayout, border=0)

    frameFilters = ttk.TTkFrame(border=True, title="Filters...", layout=filtersFormLayout())
    preferencesLayout.addWidget(frameFilters,0,0)

    return frame