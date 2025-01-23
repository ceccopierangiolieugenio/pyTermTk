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

import argparse

from TermTk import TTk, TTkTheme, TTkTerm
from TermTk import TTkGridLayout, TTkKeyPressView

from .designer import TTkDesigner

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, nargs='?', help='the file to open')
    parser.add_argument('-k', '--showkeys', action='store_true', help='display the keypresses and mouse interactions')
    args = parser.parse_args()

    TTkTheme.loadTheme( TTkTheme.NERD )

    root = TTk(
            title="TTk Designer",
            mouseTrack=True,
            layout=TTkGridLayout(),
            sigmask=(
                TTkTerm.Sigmask.CTRL_C |
                TTkTerm.Sigmask.CTRL_Q |
                TTkTerm.Sigmask.CTRL_S |
                TTkTerm.Sigmask.CTRL_Z ))

    root.layout().addWidget(_d:=TTkDesigner(fileName=args.filename))

    if args.showkeys:
        _d.setWidget(widget=TTkKeyPressView(maxHeight=3), position=_d.FOOTER, size=3)
        _d.setFixed(fixed=True, position=_d.FOOTER)

    root.mainloop()
