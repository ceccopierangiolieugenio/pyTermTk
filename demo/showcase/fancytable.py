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


table_ii = 1000


def demoFancyTable(root=None):
    frame = ttk.TTkFrame(parent=root, border=False, layout=ttk.TTkVBoxLayout())
    top = ttk.TTkFrame(parent=frame, border=False, layout=ttk.TTkHBoxLayout())
    btn1 = ttk.TTkButton(parent=top, maxHeight=3, border=True, text="Add")
    btn2 = ttk.TTkButton(parent=top, maxHeight=3, border=True, text="Add Many")

    table1 = ttk.TTkFancyTable(parent=frame, selectColor=ttk.TTkColor.bg("#882200"))

    table1.setColumnSize((5, 10, -1, 10, 20))
    table1.setAlignment(
        (
            ttk.TTkK.LEFT_ALIGN,
            ttk.TTkK.RIGHT_ALIGN,
            ttk.TTkK.LEFT_ALIGN,
            ttk.TTkK.LEFT_ALIGN,
            ttk.TTkK.CENTER_ALIGN,
        )
    )
    table1.setHeader(("id", "Name", "Sentence", "Word", "center"))
    table1.setColumnColors(
        (
            ttk.TTkColor.fg("#888800", modifier=ttk.TTkColorGradient(increment=6)),
            ttk.TTkColor.RST,
            ttk.TTkColor.fg("#00dddd", modifier=ttk.TTkColorGradient(increment=-4)),
            ttk.TTkColor.RST,
            ttk.TTkColor.fg("#cccccc", modifier=ttk.TTkColorGradient(increment=-2)),
        )
    )
    table1.appendItem(
        (
            " - ",
            "",
            "You see it's all clear, You were meant to be here, From the beginning",
            "",
            "",
        )
    )
    for i in range(0, 5):
        table1.appendItem((str(i), getWord(), getSentence(8, 30), getWord(), getWord()))
    table1.appendItem(
        (
            " - ",
            "This is the end",
            "Beautiful friend, This is the end My only friend",
            "the end",
            "...",
        )
    )

    # Attach the add Event

    def add():
        global table_ii
        table_ii += 1
        table1.appendItem(
            (str(table_ii), getWord(), getSentence(8, 30), getWord(), getWord())
        )

    btn1.clicked.connect(add)

    def addMany():
        global table_ii
        for i in range(0, 500):
            table_ii += 1
            table1.appendItem(
                (str(table_ii), getWord(), getSentence(8, 30), getWord(), getWord())
            )
        table1.appendItem(
            (
                " - ",
                "This is the end",
                "Beautiful friend, This is the end My only friend",
                "the end",
                "...",
            )
        )

    btn2.clicked.connect(addMany)

    return frame


def main():
    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    win_table = ttk.TTkWindow(
        parent=root,
        pos=(3, 3),
        size=(150, 40),
        title="Test Table 1",
        layout=ttk.TTkHBoxLayout(),
        border=True,
    )
    demoFancyTable(win_table)
    root.mainloop()


if __name__ == "__main__":
    main()
