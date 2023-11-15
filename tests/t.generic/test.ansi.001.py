#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
import logging
import time

sys.path.append(os.path.join(sys.path[0],'../..'))
from TermTk import TTkLog
from TermTk.TTkCore import TTkColor
from TermTk.TTkCore import TTkHelper
from TermTk.TTkCore import TTkString
from TermTk.TTkCore import TTkTerm

def test(ansi):
    print(f"{ansi} Test Color \033[0m")
    print(f"result: {TTkHelper.Color.ansi2rgb(ansi)}")

# 24bit fg RED
test("\033[38;2;255;0;0m")
# 24bit bg GREEN
test("\033[48;2;0;255;0m")
# 24bit fg RED bg BLUE
test("\033[38;2;255;0;0;48;2;0;0;255m")

# 256 fg RED
test("\033[38;5;9m")
# 256 bg GREEN
test("\033[48;5;10m")
# 24bit fg RED bg BLUE
test("\033[38;5;9;48;5;4m")

test("\033[48;5;0m")
test("\033[48;5;1m")
test("\033[48;5;2m")
test("\033[48;5;3m")
test("\033[48;5;4m")
test("\033[48;5;5m")
test("\033[48;5;6m")
test("\033[48;5;7m")
test("\033[48;5;8m")
test("\033[48;5;9m")
test("\033[48;5;10m")
test("\033[48;5;11m")
test("\033[48;5;12m")
test("\033[48;5;13m")
test("\033[48;5;14m")
test("\033[48;5;15m")

test("\033[30m")
test("\033[31m")
test("\033[32m")
test("\033[33m")
test("\033[34m")
test("\033[35m")
test("\033[36m")
test("\033[37m")

test("\033[40m")
test("\033[41m")
test("\033[42m")
test("\033[43m")
test("\033[44m")
test("\033[45m")
test("\033[46m")
test("\033[47m")
