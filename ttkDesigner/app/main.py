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

from TermTk import TTk, TTkLog, TTkTheme, TTkTerm

from .designer import TTkDesigner

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-c', help=f'config folder (default: "{TTKodeCfg.pathCfg}")', default=TTKodeCfg.pathCfg)
    parser.add_argument('filename', type=str, nargs='?', help='the file to open')
    args = parser.parse_args()

    # TTkLog.use_default_file_logging()
    TTkTheme.loadTheme( TTkTheme.NERD )

    root = TTk(
            title="TTk Designer",
            mouseTrack=True,
            sigmask=(
                TTkTerm.Sigmask.CTRL_C |
                TTkTerm.Sigmask.CTRL_Q |
                TTkTerm.Sigmask.CTRL_S |
                TTkTerm.Sigmask.CTRL_Z ))
    root.setLayout(TTkDesigner(fileName=args.filename))
    root.mainloop()
