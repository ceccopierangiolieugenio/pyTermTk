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

sys.path.append(os.path.join(sys.path[0], "../.."))
import TermTk as ttk

words = [
    "Lorem",
    "ipsum",
    "dolor",
    "sit",
    "amet,",
    "consectetur",
    "adipiscing",
    "elit,",
    "sed",
    "do",
    "eiusmod",
    "tempor",
    "incididunt",
    "ut",
    "labore",
    "et",
    "dolore",
    "magna",
    "aliqua.",
    "Ut",
    "enim",
    "ad",
    "minim",
    "veniam,",
    "quis",
    "nostrud",
    "exercitation",
    "ullamco",
    "laboris",
    "nisi",
    "ut",
    "aliquip",
    "ex",
    "ea",
    "commodo",
    "consequat.",
    "Duis",
    "aute",
    "irure",
    "dolor",
    "in",
    "reprehenderit",
    "in",
    "voluptate",
    "velit",
    "esse",
    "cillum",
    "dolore",
    "eu",
    "fugiat",
    "nulla",
    "pariatur.",
    "Excepteur",
    "sint",
    "occaecat",
    "cupidatat",
    "non",
    "proident,",
    "sunt",
    "in",
    "culpa",
    "qui",
    "officia",
    "deserunt",
    "mollit",
    "anim",
    "id",
    "est",
    "laborum.",
]


def getWord():
    return random.choice(words)


def getSentence(a, b):
    return " ".join([getWord() for i in range(0, random.randint(a, b))])


def demoFormWidgets(root=None):
    win_form1_grid_layout = ttk.TTkGridLayout(columnMinWidth=1)
    frame = ttk.TTkFrame(parent=root, layout=win_form1_grid_layout, border=0)

    win_form1_grid_layout.addWidget(ttk.TTkButton(text="Button 1"), 0, 0)
    win_form1_grid_layout.addWidget(ttk.TTkButton(text="Button 2"), 1, 0)
    win_form1_grid_layout.addWidget(ttk.TTkButton(text="Button 3"), 0, 2)
    win_form1_grid_layout.addWidget(ttk.TTkButton(text="Button 4"), 1, 2)
    row = 2

    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Combo Box"), row, 0)
    win_form1_grid_layout.addWidget(
        ttk.TTkComboBox(
            list=[
                "One",
                "Two",
                "Some Long Sentence That Is Not a Written Number",
                "Three",
            ]
        ),
        row,
        2,
    )
    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Combo long Box"), row, 0)
    win_form1_grid_layout.addWidget(
        ttk.TTkComboBox(list=[getSentence(1, 4) for i in range(100)]), row, 2
    )
    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Combo Box Edit. Bottom Insert"), row, 0
    )
    win_form1_grid_layout.addWidget(
        comboEdit1 := ttk.TTkComboBox(list=[getSentence(1, 4) for i in range(10)]),
        row,
        2,
    )
    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Combo Box Edit. Top Insert"), row, 0
    )
    win_form1_grid_layout.addWidget(
        comboEdit2 := ttk.TTkComboBox(list=[getSentence(1, 4) for i in range(10)]),
        row,
        2,
    )

    comboEdit1.setEditable(True)
    comboEdit2.setEditable(True)
    comboEdit2.setInsertPolicy(ttk.TTkK.InsertAtTop)

    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Line Edit Test 1"), row, 0)
    win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text="Line Edit Test 1"), row, 2)
    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Line Edit Test 2"), row, 0)
    win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text="Line Edit Test 2"), row, 2)
    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Line Edit Test 3"), row, 0)
    win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text="Line Edit Test 3"), row, 2)
    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Line Edit Test 4"), row, 0)
    win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text="Line Edit Test 4"), row, 2)
    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Line Edit Test 5"), row, 0)
    win_form1_grid_layout.addWidget(ttk.TTkLineEdit(text="Line Edit Test 5"), row, 2)

    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Line Edit Input Number"), row, 0)
    win_form1_grid_layout.addWidget(
        ttk.TTkLineEdit(text="123456", inputType=ttk.TTkK.Input_Number), row, 2
    )
    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Line Edit Input Wrong Number"), row, 0
    )
    win_form1_grid_layout.addWidget(
        ttk.TTkLineEdit(text="No num Text", inputType=ttk.TTkK.Input_Number), row, 2
    )

    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Line Edit Input Password"), row, 0
    )
    win_form1_grid_layout.addWidget(
        ttk.TTkLineEdit(text="Password", inputType=ttk.TTkK.Input_Password), row, 2
    )
    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Line Edit Number Password"), row, 0
    )
    win_form1_grid_layout.addWidget(
        ttk.TTkLineEdit(
            text="Password", inputType=ttk.TTkK.Input_Password + ttk.TTkK.Input_Number
        ),
        row,
        2,
    )

    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Spinbox (default [0,99])"), row, 0
    )
    win_form1_grid_layout.addWidget(ttk.TTkSpinBox(), row, 2)
    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Spinbox (-20, [-50,+50])"), row, 0
    )
    win_form1_grid_layout.addWidget(
        ttk.TTkSpinBox(value=-20, maximum=50, minimum=-50), row, 2
    )

    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Checkbox"), row, 0)
    win_form1_grid_layout.addWidget(ttk.TTkCheckbox(text="CheckBox 1"), row, 2)
    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Checkbox Checked"), row, 0)
    win_form1_grid_layout.addWidget(
        ttk.TTkCheckbox(text="CheckBox 2", checked=True), row, 2
    )

    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Radio Button (Default)"), row, 0)
    win_form1_grid_layout.addWidget(ttk.TTkRadioButton(text="RadioButton   1"), row, 2)
    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Radio Button (Default)"), row, 0)
    win_form1_grid_layout.addWidget(ttk.TTkRadioButton(text="RadioButton   2"), row, 2)
    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkLabel(text="Radio Button (Default)"), row, 0)
    win_form1_grid_layout.addWidget(ttk.TTkRadioButton(text="RadioButton   3"), row, 2)

    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Radio Button (Name One) 1"), row, 0
    )
    win_form1_grid_layout.addWidget(
        ttk.TTkRadioButton(text="RadioButton A", name="Name One"), row, 2
    )
    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Radio Button (Name One) 1"), row, 0
    )
    win_form1_grid_layout.addWidget(
        ttk.TTkRadioButton(text="RadioButton B", name="Name One"), row, 2
    )
    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Radio Button (Name Two)   2"), row, 0
    )
    win_form1_grid_layout.addWidget(
        ttk.TTkRadioButton(text="RadioButton  x", name="Name Two"), row, 2
    )
    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Radio Button (Name One) 1"), row, 0
    )
    win_form1_grid_layout.addWidget(
        ttk.TTkRadioButton(text="RadioButton C", name="Name One"), row, 2
    )
    row += 1
    win_form1_grid_layout.addWidget(
        ttk.TTkLabel(text="Radio Button (Name Two)   2"), row, 0
    )
    win_form1_grid_layout.addWidget(
        ttk.TTkRadioButton(text="RadioButton  y", name="Name Two"), row, 2
    )
    row += 1
    win_form1_grid_layout.addWidget(ttk.TTkSpacer(), row, 0)
    return frame


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="Full Screen", action="store_true")
    args = parser.parse_args()

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if args.f:
        rootForm = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootForm = ttk.TTkWindow(
            parent=root,
            pos=(1, 1),
            size=(100, 40),
            title="Test List",
            border=True,
            layout=ttk.TTkGridLayout(),
        )
    demoFormWidgets(rootForm)
    root.mainloop()


if __name__ == "__main__":
    main()
