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

import sys, os
import random

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

from  showcase.layout      import demoLayout
from  showcase.table       import demoTable
from  showcase.tab         import demoTab
from  showcase.tree        import demoTree
from  showcase.splitter    import demoSplitter
from  showcase.windows     import demoWindows
from  showcase.formwidgets import demoFormWidgets

words = ["Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]
def getWord():
    return random.choice(words)
def getSentence(a,b):
    return " ".join([getWord() for i in range(0,random.randint(a,b))])

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()

winTabbed1 = ttk.TTkWindow(parent=root,pos=(1,1), size=(100,40), title="Test Tab", border=True, layout=ttk.TTkGridLayout())
tabWidget1 = ttk.TTkTabWidget(parent=winTabbed1, border=True)
tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.1"), "Label 1.1")
tabWidget1.addTab(ttk.TTkTestWidget(border=True, title="Frame1.2"), "Label Test 1.2")
tabWidget1.addTab(demoLayout(),      "Layout Test")
tabWidget1.addTab(demoFormWidgets(), "Form Test")
tabWidget1.addTab(demoTable(),       "Table Test")
tabWidget1.addTab(demoTree(),        "Tree Test")
tabWidget1.addTab(demoSplitter(),    "Splitter Test")
tabWidget1.addTab(demoWindows(),     "Windows Test")
tabWidget1.addTab(demoTab(),         "Tab Test")



root.mainloop()
