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

sys.path.append(os.path.join(sys.path[0],'../..'))
from TermTk import TTkLog, TTkK, TTkTerm
from TermTk.TTkCore.TTkTerm.input import TTkInput

def message_handler(mode, context, message):
    log = logging.debug
    if mode == TTkLog.InfoMsg:       log = logging.info
    elif mode == TTkLog.WarningMsg:  log = logging.warning
    elif mode == TTkLog.CriticalMsg: log = logging.critical
    elif mode == TTkLog.FatalMsg:    log = logging.fatal
    elif mode == TTkLog.ErrorMsg:    log = logging.error
    log(f"{context.file} {message}")

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s:(%(threadName)-9s) %(message)s',)
TTkLog.installMessageHandler(message_handler)

TTkLog.info("Retrieve Keyboard, Mouse press/drag/wheel Events")
TTkLog.info("Press q or <ESC> to exit")

TTkTerm.push(TTkTerm.Mouse.ON)
TTkTerm.push(TTkTerm.Mouse.DIRECT_ON)
TTkTerm.push(TTkTerm.SET_BRACKETED_PM)
TTkTerm.setEcho(False)

def winCallback(width, height):
    TTkLog.info(f"Resize: w:{width}, h:{height}")

TTkTerm.registerResizeCb(winCallback)


def keyCallback(kevt=None, mevt=None):
    if mevt is not None:
        TTkLog.info(f"Mouse Event: {mevt}")
    if kevt is not None:
        if kevt.type == TTkK.Character:
            TTkLog.info(f"Key Event: char '{kevt.key}' {kevt}")
        else:
            TTkLog.info(f"Key Event: Special '{kevt}'")
        if kevt.key == "q":
            TTkInput.close()
            return False
    return True

def pasteCallback(txt:str):
    TTkLog.info(f"PASTE = {txt}")
    return True

TTkInput.inputEvent.connect(keyCallback)
TTkInput.pasteEvent.connect(pasteCallback)
TTkInput.init(mouse=True, directMouse=True)
# TTkInput.init(mouse=True, directMouse=False)
try:
    TTkInput.start()
finally:
    TTkInput.close()
    TTkTerm.setEcho(True)
