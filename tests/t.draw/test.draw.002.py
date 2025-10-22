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
import logging
import time

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
from TermTk import TTkLog
from TermTk.TTkCore import TTkColor
from TermTk.TTkCore import TTkHelper, TTkTerm

TTkLog.use_default_file_logging()

TTkTerm.init()
TTkTerm.setMouse(mouse=False)
TTkLog.info("Starting")
TTkTerm.push(
        TTkTerm.Cursor.moveTo(2,4) +
        str(TTkColor.fg("#ff0000")) +
        "Test Text 3"
    )
time.sleep(1)
TTkLog.info("next : 2")

TTkTerm.push(
        TTkTerm.Cursor.moveDown(1) + TTkTerm.Cursor.moveLeft(3) +
        str(TTkColor.bg("#550088")) +
        "Test Text 2"
    )
time.sleep(1)
TTkLog.info("next : 1")

TTkTerm.push(
        TTkTerm.Cursor.moveDown(1) + TTkTerm.Cursor.moveLeft(3) +  # FIXME
        TTkColor.fg("#00ff00") +
        TTkColor.bg("#555500") +
        "Test Text 1"
    )
time.sleep(1)
TTkLog.info("Ending")

TTkTerm.exit()