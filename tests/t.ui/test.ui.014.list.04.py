#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

zc1 = chr(0x07a6) # Zero width chars oަ
zc2 = chr(0x20D7) # Zero width chars o⃗
zc3 = chr(0x065f) # Zero width chars oٟ
utfwords = [
    f"--Zero{zc1}{zc2}{zc3}-1-", f"--Zero-2{zc1}{zc2}{zc3}-", f"--Ze{zc1}{zc2}{zc3}ro-3-", f"{zc1}{zc2}{zc3}--Zero-4-",
    "d😮l😱r", "sit", "am😎t,", "c😱nsectetur", "t😜mpor", "inci😜di😜dunt", "u😜t", "l😜abore", "et", "d😜olore", "m😜a😜gna", "ali😜qua😜.", "Ut", "enim", "😜a😜d😜", "minim", "veniam,", "😜q😜uis", "😜nostrud", "exer😜c😜i😜tation", "ullamco", "labo😜ris", "n😜isi", "ut", "aliq😞ip", "e😜x😜", "ea", "comm😞do", "cons😿quat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "cul🙻a", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]
words    = ["Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]
def getWord():
    return random.choice(utfwords)
    # return random.choice(words)

parser = argparse.ArgumentParser()
parser.add_argument('-t', help='Track Mouse', action='store_true')
args = parser.parse_args()
mouseTrack = args.t

root = ttk.TTk(title="pyTermTk List Demo", mouseTrack=mouseTrack)

# Define the main Layout
frame1 = ttk.TTkWindow(parent=root, pos=( 0, 0), size=(30,30), title="Single List", border=0, layout=ttk.TTkVBoxLayout())
frame2 = ttk.TTkWindow(parent=root, pos=(30, 0), size=(30,30), title="Multi List", border=0, layout=ttk.TTkVBoxLayout())
frame3 = ttk.TTkWindow(parent=root, pos=(60, 0), size=(80,30), title="Log", border=0, layout=ttk.TTkVBoxLayout())

# Single Selection List
listWidgetSingle = ttk.TTkList(parent=frame1, maxWidth=40, minWidth=10)

# Multi Selection List
listWidgetMulti = ttk.TTkList(parent=frame2, maxWidth=40, minWidth=10, selectionMode=ttk.TTkK.MultiSelection)

# Log Viewer
label1 = ttk.TTkLabel(parent=root, pos=(10,30), text="[ list1 ]",maxHeight=2)
label2 = ttk.TTkLabel(parent=root, pos=(10,31), text="[ list2 ]",maxHeight=2)
ttk.TTkLogViewer(parent=frame3)#, border=True)

btn_mv1 = ttk.TTkButton(parent=root, pos=(0,30), text=" >> ")
btn_mv2 = ttk.TTkButton(parent=root, pos=(0,31), text=" << ")
btn_del = ttk.TTkButton(parent=root, pos=(0,32), text="Delete")

@ttk.pyTTkSlot(str)
def _listCallback1(label):
    ttk.TTkLog.info(f'Clicked label1: "{label}"')
    label1.setText(f'[ list1 ] clicked "{label}" - Selected: {[str(s) for s in listWidgetSingle.selectedLabels()]}')

@ttk.pyTTkSlot(str)
def _listCallback2(label):
    ttk.TTkLog.info(f'Clicked label2: "{label}" - selected: {[str(s) for s in listWidgetMulti.selectedLabels()]}')
    label2.setText(f'[ list2 ] clicked "{label}" - {[str(s) for s in listWidgetMulti.selectedLabels()]}')

@ttk.pyTTkSlot()
def _moveToRight2():
    for i in listWidgetSingle.selectedItems().copy():
        listWidgetSingle.removeItem(i)
        listWidgetMulti.addItemAt(i,0)

@ttk.pyTTkSlot()
def _moveToLeft1():
    for i in listWidgetMulti.selectedItems().copy():
        listWidgetMulti.removeItem(i)
        listWidgetSingle.addItemAt(i,0)

@ttk.pyTTkSlot()
def _delSelected():
    items = listWidgetMulti.selectedItems()
    listWidgetMulti.removeItems(items)
    items = listWidgetSingle.selectedItems()
    listWidgetSingle.removeItems(items)


btn_mv1.clicked.connect(_moveToRight2)
btn_mv2.clicked.connect(_moveToLeft1)
btn_del.clicked.connect(_delSelected)


# Connect the signals to the 2 slots defines
listWidgetSingle.textClicked.connect(_listCallback1)
listWidgetMulti.textClicked.connect(_listCallback2)

# populate the lists with random entries
for i in range(10):
    listWidgetSingle.addItem(f"S-{i}) {getWord()} {getWord()}")
    listWidgetMulti.addItem(f"M-{i}) {getWord()} {getWord()}")

root.mainloop()
