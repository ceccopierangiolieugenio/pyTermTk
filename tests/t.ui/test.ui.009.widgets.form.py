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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

words = ["Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]
def getWord():
    return random.choice(words)
def getSentence(a,b):
    return " ".join([getWord() for i in range(0,random.randint(a,b))])

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()
win_form1 = ttk.TTkWindow(parent=root,pos=(1,1), size=(60,40), title="Test Window 1", layout=ttk.TTkVBoxLayout(), border=True)
win_form1_grid_layout = ttk.TTkGridLayout(columnMinWidth=1)
ttk.TTkFrame(parent=win_form1, layout=win_form1_grid_layout)
ttk.TTkLogViewer(parent=win_form1)


win_form1_grid_layout.addWidget(ttk.TTkButton(text='Button 1'),0,0)
win_form1_grid_layout.addWidget(ttk.TTkButton(text='Button 2'),1,0)
win_form1_grid_layout.addWidget(ttk.TTkButton(text='Button 3'),0,2)
win_form1_grid_layout.addWidget(ttk.TTkButton(text='Button 4'),1,2)
row = 2

row +=1;  win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Combo Box'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkComboBox(list=['One','Two','Some Long Sentence That Is Not a Written Number','Three']),row,2)
row +=1;  win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Combo long Box'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkComboBox(list=[getSentence(1,4) for i in range(100)]),row,2)


row +=1;  win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Test 1'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text='Line Edit Test 1'),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Test 2'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text='Line Edit Test 2'),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Test 3'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text='Line Edit Test 3'),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Test 4'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text='Line Edit Test 4'),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Test 5'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text='Line Edit Test 5'),row,2)

row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Input Number'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text='123456', inputType=ttk.TTkK.Input_Number),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Input Wrong Number'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text='No num Text', inputType=ttk.TTkK.Input_Number),row,2)

row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Input Password'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text='Password', inputType=ttk.TTkK.Input_Password),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Number Password'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text='Password', inputType=ttk.TTkK.Input_Password+ttk.TTkK.Input_Number),row,2)

row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Checkbox'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkCheckbox(),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Checkbox Checked'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkCheckbox(checked=True),row,2)

row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Default)'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkRadioButton(),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Default)'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkRadioButton(),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Default)'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkRadioButton(),row,2)

row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Name One)'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkRadioButton(radiogroup="Name One"),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Name One)'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkRadioButton(radiogroup="Name One"),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Name Two)'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkRadioButton(radiogroup="Name Two"),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Name One)'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkRadioButton(radiogroup="Name One"),row,2)
row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Name Two)'),row,0)
win_form1_grid_layout.addWidget(ttk.TTkRadioButton(radiogroup="Name Two"),row,2)

# ttk.TTkResizableFrame(parent=root, pos=(20,3),size=(30,30))

#row += 1; win_form1_grid_layout.addWidget(ttk.TTkSpacer(),row,0)





root.mainloop()