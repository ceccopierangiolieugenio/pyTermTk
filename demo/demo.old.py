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

import sys, os, argparse
import random

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

from  showcase.layout_basic  import demoLayout
from  showcase.layout_nested import demoLayoutNested
from  showcase.layout_span   import demoLayoutSpan
from  showcase.table         import demoTable
from  showcase.tab           import demoTab
from  showcase.tree          import demoTree
from  showcase.graph         import demoGraph
from  showcase.splitter      import demoSplitter
from  showcase.windows       import demoWindows
from  showcase.formwidgets   import demoFormWidgets
from  showcase.scrollarea    import demoScrollArea
from  showcase.list_         import demoList
from  showcase.menubar       import demoMenuBar
from  showcase.colorpicker   import demoColorPicker

words = ["Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]
def getWord():
    return random.choice(words)
def getSentence(a,b):
    return " ".join([getWord() for i in range(0,random.randint(a,b))])

def demoShowcase(root=None, border=True):
    tabWidget1 = ttk.TTkTabWidget(parent=root, border=border)
    tabWidget1.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.1"), " Label 1.1 ")
    tabWidget1.addTab(ttk.TTkTestWidget(border=True, title="Frame1.2"), " Label Test 1.2 ")
    tabWidget1.addTab(demoLayout(),      " Layout Test ")
    tabWidget1.addTab(demoLayoutNested()," Nested Layout Test ")
    tabWidget1.addTab(demoLayoutSpan(),  " Layout Span Test ")
    tabWidget1.addTab(demoMenuBar(),     " MenuBar Test ")
    tabWidget1.addTab(demoFormWidgets(), " Form Test ")
    tabWidget1.addTab(demoList(),        " List Test ")
    tabWidget1.addTab(demoColorPicker(), " Color Picker ")
    tabWidget1.addTab(demoGraph(),       " Graph Test ")
    tabWidget1.addTab(demoTable(),       " Table Test ")
    tabWidget1.addTab(demoTree(),        " Tree Test ")
    tabWidget1.addTab(demoSplitter(),    " Splitter Test ")
    tabWidget1.addTab(demoWindows(),     " Windows Test ")
    tabWidget1.addTab(demoTab(),         " Tab Test ")
    tabWidget1.addTab(demoScrollArea(),  " Scroll Area ")

    return tabWidget1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if args.f:
        root.setLayout(ttk.TTkGridLayout())
        winTabbed1 = root
        border = False
    else:
        winTabbed1 = ttk.TTkWindow(parent=root,pos=(0,0), size=(120,40), title="Test Tab", border=True, layout=ttk.TTkGridLayout())
        border = True

    demoShowcase(winTabbed1, border)

    root.mainloop()

if __name__ == "__main__":
    main()

def test_demo():
    root = ttk.TTk()
    assert demoShowcase(root) != None
    root.quit()