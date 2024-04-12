#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['main']

import argparse

import TermTk as ttk

from .maintemplate import PaintTemplate

ttk.TTkTheme.loadTheme(ttk.TTkTheme.NERD)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, nargs='?', help='the file to open')
    # parser.add_argument('-k', '--showkeys', action='store_true', help='display the keypresses and mouse interactions')
    args = parser.parse_args()

    root = ttk.TTk(
            title="Dumb Paint Tool",
            layout=ttk.TTkGridLayout(),
            mouseTrack=True,
            sigmask=(
                ttk.TTkTerm.Sigmask.CTRL_C |
                ttk.TTkTerm.Sigmask.CTRL_Q |
                ttk.TTkTerm.Sigmask.CTRL_S |
                ttk.TTkTerm.Sigmask.CTRL_Z ))

    PaintTemplate(parent=root,fileName=args.filename)

    root.mainloop()

if __name__ == '__main__':
    main()