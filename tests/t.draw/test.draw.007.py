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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
from TermTk import TTkLog
from TermTk.TTkCore import TTkColor
from TermTk.TTkCore import TTkHelper
from TermTk.TTkCore import TTkString
from TermTk.TTkCore import TTkTerm
from TermTk.TTkCore import TTkCanvas


# TTkLog.use_default_file_logging()
TTkLog.use_default_stdout_logging()

# TTkTerm.init(mouse=False)
TTkLog.info("Starting")

s1 = TTkString("-😁😂😍😎----")
s2 = TTkString("--😐😁😂😍😎-")

zc1 = chr(0x07a6)
zc2 = chr(0x20D7)
zc3 = chr(0x065f)
s3 = TTkString(f"Zero Size: - o{zc1}  o{zc2}  o{zc3}  o{zc1}{zc2}  o{zc1}{zc2}{zc3} -")

s4 = TTkString("This is a normal string")

s5 = TTkString(f"-😁- o{zc1}  o{zc2}  o{zc3}  o{zc1}{zc2}  o{zc1}{zc2}{zc3} -")
s6 = TTkString(f"{zc1}  o{zc2}  o{zc3}  o{zc1}{zc2}  o{zc1}{zc2}{zc3} -")
TTkLog.debug(f"o{zc1}{zc2}{zc3} - Zero")
TTkLog.debug(f"{zc1}{zc2}{zc3} - Zero")

canvas = TTkCanvas(width=100,height=100)
canvas.drawTTkString(pos=(0,0),text=s1,width=4)
canvas.drawTTkString(pos=(0,0),text=s1,width=11)
canvas.drawTTkString(pos=(0,0),text=s5,width=8)
canvas.drawTTkString(pos=(0,0),text=s6,width=4)


TTkLog.info("Ending")
