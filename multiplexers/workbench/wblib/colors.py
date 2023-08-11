#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the"Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED"AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

# Colors:
# Blue:   0055aa
# Orange: ff8800

__all__ = [
    'fgBLUE','fgORANGE','fgBLACK','fgWHITE',
    'bgBLUE','bgORANGE','bgBLACK','bgWHITE']

fgBLUE   = ttk.TTkColor.fg('#0055aa')
fgORANGE = ttk.TTkColor.fg('#0055aa')
fgBLACK  = ttk.TTkColor.fg('#000000')
fgWHITE  = ttk.TTkColor.fg('#ffffff')
bgBLUE   = ttk.TTkColor.bg('#0055aa')
bgORANGE = ttk.TTkColor.bg('#0055aa')
bgBLACK  = ttk.TTkColor.bg('#000000')
bgWHITE  = ttk.TTkColor.bg('#ffffff')
