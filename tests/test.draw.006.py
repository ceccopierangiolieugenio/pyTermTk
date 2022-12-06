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

s5 = TTkString(f"-😁😂😍😎- o{zc1}  o{zc2}  o{zc3}  o{zc1}{zc2}  o{zc1}{zc2}{zc3} -")
s6 = TTkString(f"{zc1}  o{zc2}  o{zc3}  o{zc1}{zc2}  o{zc1}{zc2}{zc3} -")
print(f"o{zc1}{zc2}{zc3} - Zero")
print(f"{zc1}{zc2}{zc3} - Zero")


# Examples from:
#    https://github.com/luchr/WidthInTerminals
print( "🔧   = \U0001F527                                              ")
print(f"👩   = {chr(0x1F469)}                                          ")
print(f"👩🔧 = {chr(0x1F469)}{chr(0x1F527)}                            ")
print(f"👩‍🔧   = {chr(0x1F469)}{chr(0x0200D)}{chr(0x1F527)}              ")
print(f"👩🏻‍🔧   = {chr(0x1F469)}{chr(0x1F3FB)}{chr(0x0200D)}{chr(0x1F527)}")
print(f"👩🏻‍🔧   = {chr(0x1F469)}{chr(0x1F3FB)}{chr(0x0200D)}{chr(0x1F527)}")
print(f"👩🏼‍🔧   = {chr(0x1F469)}{chr(0x1F3FC)}{chr(0x0200D)}{chr(0x1F527)}")
print(f"👩🏽‍🔧   = {chr(0x1F469)}{chr(0x1F3FD)}{chr(0x0200D)}{chr(0x1F527)}")
print(f"👩🏾‍🔧   = {chr(0x1F469)}{chr(0x1F3FE)}{chr(0x0200D)}{chr(0x1F527)}")
print(f"👩🏿‍🔧   = {chr(0x1F469)}{chr(0x1F3FF)}{chr(0x0200D)}{chr(0x1F527)}")

s01 = TTkString(f"🔧   = {chr(0x1F527)}                                          ") # 1F527                  : 🔧
s01 = TTkString(f"👩   = {chr(0x1F469)}                                          ") # 1F469                  : 👩
s01 = TTkString(f"👩🔧 = {chr(0x1F469)}{chr(0x1F527)}                            ") # 1F469 1F527            : 👩🔧
s01 = TTkString(f"👩‍🔧   = {chr(0x1F469)}{chr(0x0200D)}{chr(0x1F527)}              ") # 1F469 200D 1F527       : 👩‍🔧
s01 = TTkString(f"👩🏻‍🔧   = {chr(0x1F469)}{chr(0x1F3FB)}{chr(0x0200D)}{chr(0x1F527)}") # 1F469 1F3FB 200D 1F527 : 👩🏻‍🔧
s01 = TTkString(f"👩🏻‍🔧   = {chr(0x1F469)}{chr(0x1F3FB)}{chr(0x0200D)}{chr(0x1F527)}") # 1F469 1F3FB 200D 1F527 : 👩🏻‍🔧
s01 = TTkString(f"👩🏼‍🔧   = {chr(0x1F469)}{chr(0x1F3FC)}{chr(0x0200D)}{chr(0x1F527)}") # 1F469 1F3FC 200D 1F527 : 👩🏼‍🔧
s01 = TTkString(f"👩🏽‍🔧   = {chr(0x1F469)}{chr(0x1F3FD)}{chr(0x0200D)}{chr(0x1F527)}") # 1F469 1F3FD 200D 1F527 : 👩🏽‍🔧
s01 = TTkString(f"👩🏾‍🔧   = {chr(0x1F469)}{chr(0x1F3FE)}{chr(0x0200D)}{chr(0x1F527)}") # 1F469 1F3FE 200D 1F527 : 👩🏾‍🔧
s01 = TTkString(f"👩🏿‍🔧   = {chr(0x1F469)}{chr(0x1F3FF)}{chr(0x0200D)}{chr(0x1F527)}") # 1F469 1F3FF 200D 1F527 : 👩🏿‍🔧



print(s1.getData()[0])
print(s2.getData()[0])
print(s3.getData()[0])
print(s4.getData()[0])
print(s5.getData()[0])
print(s6.getData()[0])

s5.tabCharPos(1,tabSpaces=4)
s5.tabCharPos(5,tabSpaces=4)
s5.tabCharPos(9,tabSpaces=4)

# time.sleep(5)

TTkLog.info("Ending")

# TTkTerm.exit()