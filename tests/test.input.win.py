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

sys.path.append(os.path.join(sys.path[0],'..'))
from TermTk import TTkLog, TTkK, TTkGridLayout, TTk, TTkLogViewer, TTkHelper

def keyCallback(kevt=None, mevt=None):
    if mevt is not None:
        TTkLog.info(f"Mouse Event: {mevt}")
    if kevt is not None:
        if kevt.type == TTkK.Character:
            TTkLog.info(f"Key Event: char '{kevt.key}' {kevt}")
        else:
            TTkLog.info(f"Key Event: Special '{kevt}'")
        if kevt.key == "q":
            input.close()
            return False
    return True

def pasteCallback(txt:str):
    TTkLog.info(f"PASTE:")
    for s in txt.split('\n'):
        TTkLog.info(f" | {s}")
    return True

root = TTk(layout=TTkGridLayout())

TTkLogViewer(parent=root)

TTkHelper._rootWidget._input.inputEvent.connect(keyCallback)
TTkHelper._rootWidget._input.pasteEvent.connect(pasteCallback)

root.mainloop()
