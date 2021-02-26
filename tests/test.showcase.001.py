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



ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()

btn1 = ttk.TTkButton(parent=root, pos=(0,0), size=(5,3), border=True, text='On')
btn2 = ttk.TTkButton(parent=root, pos=(5,0), size=(5,3), border=True, text='Off')
btn3 = ttk.TTkButton(parent=root, pos=(0,3), size=(5,3), border=True, text='On')
btn4 = ttk.TTkButton(parent=root, pos=(5,3), size=(5,3), border=True, text='Off')
btn5 = ttk.TTkButton(parent=root, pos=(0,6), size=(5,3), border=True, text='On')
btn6 = ttk.TTkButton(parent=root, pos=(5,6), size=(5,3), border=True, text='Off')
ttk.TTkLabel(parent=root, pos=(10,1), text='zOrder and max/min size')
ttk.TTkLabel(parent=root, pos=(10,4), text='Scollbars')
ttk.TTkLabel(parent=root, pos=(10,7), text='Basic Table')

# Testing Widgets from "test.ui.004.windows.py"
test_win1 = ttk.TTkWindow(parent=root,pos = (10,1), size=(70,35), title="Test Window 1", border=True)
test_win1.hide()
btn1.clicked.connect(test_win1.show)
btn2.clicked.connect(test_win1.hide)

test_win2_1 = ttk.TTkWindow(parent=test_win1,pos = (3,3), size=(40,20), title="Test Window 2.1", border=True)
test_win2_1.setLayout(ttk.TTkHBoxLayout())
ttk.TTkTestWidget(parent=test_win2_1, border=False)

test_win2_2 = ttk.TTkWindow(parent=test_win1,pos = (5,5), size=(40,20), title="Test Window 2.2", border=True)
test_win2_2.setLayout(ttk.TTkHBoxLayout())
ttk.TTkTestWidget(parent=test_win2_2, border=False)


test_win3 = ttk.TTkWindow(parent=root,pos = (20,5), size=(70,25), title="Test Window 3", border=True)
test_win3.hide()
test_win3.setLayout(ttk.TTkHBoxLayout())
btn1.clicked.connect(test_win3.show)
btn2.clicked.connect(test_win3.hide)

ttk.TTkTestWidget(parent=test_win3, border=True, maxWidth=30, minWidth=20)
rightFrame = ttk.TTkFrame(parent=test_win3, border=True)
rightFrame.setLayout(ttk.TTkVBoxLayout())

ttk.TTkTestWidget(parent=rightFrame, border=True, maxSize=(50,15), minSize=(30,8))
bottomrightframe = ttk.TTkFrame(parent=rightFrame,border=True)

test_win4 = ttk.TTkWindow(parent=bottomrightframe, pos = (3,3), size=(40,20), title="Test Window 4", border=True)
test_win4.setLayout(ttk.TTkHBoxLayout())
ttk.TTkTestWidget(parent=test_win4, border=False)


# Scroller window from test.ui.006.scroll.py
win_scroller = ttk.TTkWindow(parent=root,pos=(30,3), size=(50,30), title="Test Window 1", border=True)
win_scroller.hide()
btn3.clicked.connect(win_scroller.show)
btn4.clicked.connect(win_scroller.hide)
win_scroller.setLayout(ttk.TTkVBoxLayout())
top = ttk.TTkFrame(parent=win_scroller, layout=ttk.TTkHBoxLayout())
ttk.TTkScrollBar(parent=win_scroller, orientation=ttk.TTkK.HORIZONTAL, value=0,  color=ttk.TTkColor.bg('#990044')+ttk.TTkColor.fg('#ffff00'))
ttk.TTkScrollBar(parent=win_scroller, orientation=ttk.TTkK.HORIZONTAL, value=10, color=ttk.TTkColor.bg('#770044')+ttk.TTkColor.fg('#ccff00'))
ttk.TTkScrollBar(parent=win_scroller, orientation=ttk.TTkK.HORIZONTAL, value=50, color=ttk.TTkColor.bg('#660044')+ttk.TTkColor.fg('#88ff00'))
ttk.TTkScrollBar(parent=win_scroller, orientation=ttk.TTkK.HORIZONTAL, value=80, color=ttk.TTkColor.bg('#550044')+ttk.TTkColor.fg('#55ff00'))
ttk.TTkScrollBar(parent=win_scroller, orientation=ttk.TTkK.HORIZONTAL, value=99, color=ttk.TTkColor.bg('#330044')+ttk.TTkColor.fg('#33ff00'))


ttk.TTkScrollBar(parent=top, orientation=ttk.TTkK.VERTICAL, value=0)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTkK.VERTICAL, value=10)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTkK.VERTICAL, value=40)
ttk.TTkSpacer(parent=top)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTkK.VERTICAL, value=40, pagestep=3)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTkK.VERTICAL, value=50, pagestep=5)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTkK.VERTICAL, value=60, pagestep=20)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTkK.VERTICAL, value=70, pagestep=30)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTkK.VERTICAL, value=80, pagestep=60)
ttk.TTkSpacer(parent=top)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTkK.VERTICAL, value=80)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTkK.VERTICAL, value=90)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTkK.VERTICAL, value=99)


# Table window from test.ui.008.table.py
words = ["Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]
def getWord():
    return random.choice(words)
def getSentence():
    return " ".join([getWord() for i in range(0,random.randint(6, 20))])

win_table = ttk.TTkWindow(parent=root,pos = (10,0), size=(60,30), title="Test Table 1", layout=ttk.TTkHBoxLayout(), border=True)
win_table.hide()
btn5.clicked.connect(win_table.show)
btn6.clicked.connect(win_table.hide)
table = ttk.TTkTable(parent=win_table)

table.setColumnSize((20,-1,10,15))
table.appendItem(("","You see it's all clear, You were meant to be here, From the beginning","",""))
for i in range(0, 100):
    table.appendItem((str(i)+" - "+getWord(), getSentence(), getWord(), getWord()))
table.appendItem(("This is the end", "Beautiful friend, This is the end My only friend", "the end", "..."))




root.mainloop()