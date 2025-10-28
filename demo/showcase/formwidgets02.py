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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

sys.path.append(os.path.join(sys.path[0],'..'))
from showcase._showcasehelper import getUtfSentence, zc1

def demoFormWidgets(root=None):
    win_form1_grid_layout = ttk.TTkGridLayout(columnMinWidth=1)
    frame = ttk.TTkFrame(parent=root, layout=win_form1_grid_layout, border=0)

    win_form1_grid_layout.addWidget(_b1 := ttk.TTkButton(text='Button 1', border=True, maxHeight=3),0,0)
    win_form1_grid_layout.addWidget(_b2 := ttk.TTkButton(text='Button 2'),1,0)
    win_form1_grid_layout.addWidget(_b3 := ttk.TTkButton(text='Checkable 1', checkable=True, border=True),0,2)
    win_form1_grid_layout.addWidget(_b4 := ttk.TTkButton(text='Checkable 2', checkable=True),1,2)

    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True, maxWidth=11),1,3)
    _en_dis_cb.clicked.connect(_b1.setEnabled)
    _en_dis_cb.clicked.connect(_b2.setEnabled)
    _en_dis_cb.clicked.connect(_b3.setEnabled)
    _en_dis_cb.clicked.connect(_b4.setEnabled)

    row = 2

    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Combo Box'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkComboBox(list=['One','Two','Some Long Sentence That Is Not a Written Number','Three']),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Combo long Box'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkComboBox(list=[getUtfSentence(1,4) for i in range(100)]),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Combo Box Edit. Bottom Insert'),row,0)
    win_form1_grid_layout.addWidget(comboEdit1 := ttk.TTkComboBox(list=[getUtfSentence(1,4) for i in range(10)]),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(comboEdit1.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Combo Box Edit. Top Insert'),row,0)
    win_form1_grid_layout.addWidget(comboEdit2 := ttk.TTkComboBox(list=[getUtfSentence(1,4) for i in range(10)]),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(comboEdit2.setEnabled)

    comboEdit1.setEditable(True)
    comboEdit2.setEditable(True)
    comboEdit2.setInsertPolicy(ttk.TTkK.InsertAtTop)

    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Test 1'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkLineEdit(text='Line Edit Test 1'),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Test 2'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkLineEdit(text='Line Edit Test 2 😎 -'),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Test 3'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkLineEdit(text=f'Line Edit Test 3 o{zc1}-'),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)

    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Input Number'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkLineEdit(text='123456', inputType=ttk.TTkK.Input_Number),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Input Wrong Number'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkLineEdit(text='No num Text', inputType=ttk.TTkK.Input_Number),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)

    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Input Password'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkLineEdit(text='Password', inputType=ttk.TTkK.Input_Password),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Line Edit Number Password'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkLineEdit(text='Password', inputType=ttk.TTkK.Input_Password+ttk.TTkK.Input_Number),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)

    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Spinbox (default [0,99])'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkSpinBox(),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Spinbox (-20, [-50,+50])'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkSpinBox(value=-20, maximum=50, minimum=-50),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)

    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Checkbox'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkCheckbox(text='CheckBox 1'),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Checkbox Checked'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkCheckbox(text='CheckBox 2', checked=True),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Checkbox Tristate'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkCheckbox(text='CheckBox 3', checkStatus=ttk.TTkK.PartiallyChecked, tristate=True),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)

    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Default)'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkRadioButton(text='RadioButton   1'),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Default)'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkRadioButton(text='RadioButton   2'),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Default)'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkRadioButton(text='RadioButton   3'),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)

    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Name One) 1'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkRadioButton(text='RadioButton A', radiogroup="Name One"),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Name One) 1'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkRadioButton(text='RadioButton B', radiogroup="Name One"),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Name Two)   2'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkRadioButton(text='RadioButton  x',radiogroup="Name Two"),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Name One) 1'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkRadioButton(text='RadioButton C', radiogroup="Name One"),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkLabel(text='Radio Button (Name Two)   2'),row,0)
    win_form1_grid_layout.addWidget(_wid := ttk.TTkRadioButton(text='RadioButton  y',radiogroup="Name Two"),row,2)
    win_form1_grid_layout.addWidget(_en_dis_cb := ttk.TTkCheckbox(text=" en/dis", checked=True),row,3); _en_dis_cb.clicked.connect(_wid.setEnabled)
    row += 1; win_form1_grid_layout.addWidget(ttk.TTkSpacer(),row,0)
    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    parser.add_argument('-t', help='Track Mouse', action='store_true')
    args = parser.parse_args()

    mouseTrack = args.t

    root = ttk.TTk(title="pyTermTk Form Demo", mouseTrack=mouseTrack)
    if args.f:
        rootForm = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootForm = ttk.TTkWindow(parent=root,pos=(1,1), size=(100,40), title="Test List", border=True, layout=ttk.TTkGridLayout())
    demoFormWidgets(rootForm)
    root.mainloop()

if __name__ == "__main__":
    main()