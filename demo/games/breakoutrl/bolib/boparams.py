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

__all__ = ['BreakOutParams']

import sys, os
from dataclasses import dataclass

sys.path.append(os.path.join(sys.path[0],'../../..'))
import TermTk as ttk

@dataclass
class BreakOutParams():
    colors = {
        'lines': [
            ttk.TTkColor.fg("#000000")+ttk.TTkColor.bg("#FF0000"),
            ttk.TTkColor.fg("#000000")+ttk.TTkColor.bg("#FF8800"),
            ttk.TTkColor.fg("#000000")+ttk.TTkColor.bg("#00FF00"),
            ttk.TTkColor.fg("#000000")+ttk.TTkColor.bg("#FFFF00")],
        'bar'  : ttk.TTkColor.fg("#0088FF"),
    }
    delay: float = 0.05
    wallCols: int = 14
    wallRows: int = 8
    brickSize: int = 8
    blocksOffset: int = 5
    barSize: int = 20
