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

sys.path.append(os.path.join(sys.path[0],'..'))
from TermTk import TTkLog
from TermTk.TTkCore import TTkColor
from TermTk.TTkCore import TTkHelper
from TermTk.TTkCore import TTkString
from TermTk.TTkCore import TTkTerm


TTkLog.use_default_file_logging()

TTkTerm.init(mouse=False)
TTkLog.info("Starting")

color1 = TTkColor.fg("#88ffff")
color2 = TTkColor.bg("#005555")
color3 = TTkColor.UNDERLINE + TTkColor.fg("#00ff00" ) + TTkColor.bg("#555500")
color4 = TTkColor.RST
color5 = TTkColor.bg("#555500")+TTkColor.STRIKETROUGH

base = TTkString() + color1 + "TestXYZ" + color2 + "012345ABCDEFXYZ" + color3 + "0123456" + color4 + "pyTermTk"

s1 = base
s2 = base.replace("ABCD",     "__PierCecco__")
s3 = base.replace("XYZ012345","CeccoPierangioliEugenio")
s4 = base.replace("XYZ012345","Parodi")
s5 = base.setColor(color5,    "XYZ0123")
s6 = base.setColor(color5)

TTkTerm.push(
        TTkTerm.Cursor.moveTo(2,4) +
        s1.toAansi() )
time.sleep(0.5)
TTkLog.info("next : 4")

TTkTerm.push(
        TTkTerm.Cursor.moveDown(1) + TTkTerm.Cursor.moveLeft(30) +
        s2.toAansi() )
time.sleep(0.5)
TTkLog.info("next : 3")

TTkTerm.push(
        TTkTerm.Cursor.moveDown(1) + TTkTerm.Cursor.moveLeft(30) +
        s3.toAansi() )
time.sleep(0.5)
TTkLog.info("next : 2")

TTkTerm.push(
        TTkTerm.Cursor.moveDown(1) + TTkTerm.Cursor.moveLeft(30) +
        s4.toAansi() )
time.sleep(0.5)
TTkLog.info("next : 1")

TTkTerm.push(
        TTkTerm.Cursor.moveDown(1) + TTkTerm.Cursor.moveLeft(30) +
        s5.toAansi() )
time.sleep(0.5)
TTkLog.info("next : 0")

TTkTerm.push(
        TTkTerm.Cursor.moveDown(1) + TTkTerm.Cursor.moveLeft(30) +
        s6.toAansi() )
time.sleep(3)
TTkLog.info("Ending")

TTkTerm.exit()