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
import sys
import random
import argparse

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

sys.path.append(os.path.join(sys.path[0],'..'))
from showcase._showcasehelper import getUtfColoredSentence

class superSimpleHorizontalLine(ttk.TTkWidget):
    def paintEvent(self):
        w,h = self.size()
        self._canvas.drawText(pos=(0,h-1), text='┕'+('━'*(w-2))+'┙',color=ttk.TTkColor.fg("#888888"))


def demoTextEditRO(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)

    winTe = ttk.TTkWindow(parent=frame, title="Text Edit", pos=(20,3), size=(50,30), layout=ttk.TTkGridLayout())
    te = ttk.TTkTextEdit(parent=winTe, lineNumber=True)

    winAc = ttk.TTkWindow(parent=frame, title="Animation Controls", pos=(0,0), size=(50,30))
    animBtn = ttk.TTkButton(parent=winAc, text="Animate",border=True,pos=(0,0))

    anim = ttk.TTkPropertyAnimation(te.viewport(),'viewMoveTo')
    anim.setDuration(1)
    anim.setStartValue((0, 0))
    anim.setEndValue((  00, 70))
    # anim.setEasingCurve(ttk.TTkEasingCurve.OutQuad)
    anim.setEasingCurve(ttk.TTkEasingCurve.OutBounce)

    animBtn.clicked.connect(anim.start)

    # Initialize the textedit with come text

    te.setText(ttk.TTkString("Text Edit DEMO\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD+ttk.TTkColor.ITALIC))

    # Load ANSI input
    te.append(ttk.TTkString("ANSI Input Test\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'textedit.ANSI.txt')) as f:
        te.append(f.read())

    # Test Variable sized chars
    te.append(ttk.TTkString("Test Variable sized chars\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    te.append( "Emoticons: -😁😂😍😎----")
    te.append( "           --😐😁😂😍😎-")
    te.append("")

    te.append( "    UTF-8: £ @ £ ¬ ` 漢 _ _ あ _ _")
    te.append( "           |.|.|.|.|.||.|.|.||.|.|.")
    te.append("")


    zc1 = chr(0x07a6)
    zc2 = chr(0x20D7)
    zc3 = chr(0x065f)
    te.append( "           - |  |  |  |  | -")
    te.append(f"Zero Size: - o{zc1}  o{zc2}  o{zc3}  o{zc1}{zc2}  o{zc1}{zc2}{zc3} -")
    te.append( "           - |  |  |  |  | -")
    te.append("")

    te.append(f"Plus Tabs: -\t😁\t😍\to{zc1}{zc2}{zc3}\t😎\to{zc1}{zc2}{zc3}\t😂-")
    te.append("")

    # Test Tabs
    te.append(ttk.TTkString("Tabs Test\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    te.append("Word\tAnother Word\tYet more words")
    te.append("What a wonderful word\tOut of this word\tBattle of the words\tThe city of thousand words\tThe word is not enough\tJurassic word\n")
    te.append("tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("-tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("--tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("---tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("----tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("-----tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("------tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("-------tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\n")

    te.append(ttk.TTkString("Random TTkString Input Test\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    te.append(ttk.TTkString('\n').join([ getUtfColoredSentence(3,10) for _ in range(100)]))

    te.append(ttk.TTkString("-- The Very END --",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))

    # use the widget size to wrap
    # te.setLineWrapMode(ttk.TTkK.WidgetWidth)
    # te.setWordWrapMode(ttk.TTkK.WordWrap)

    # Use a fixed wrap size
    # te.setLineWrapMode(ttk.TTkK.FixedWidth)
    # te.setWrapWidth(100)





    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen (default)', action='store_true')
    parser.add_argument('-w', help='Windowed',    action='store_true')
    args = parser.parse_args()
    windowed = args.w

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if windowed:
        rootTree = ttk.TTkWindow(parent=root,pos = (0,0), size=(70,40), title="Test Text Edit", layout=ttk.TTkGridLayout(), border=True)
    else:
        rootTree = root
        root.setLayout(ttk.TTkGridLayout())
    demoTextEditRO(rootTree)
    root.mainloop()

if __name__ == "__main__":
    main()