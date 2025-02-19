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

__all__ = ['TTkInput']

import re
from time import time

import threading, queue

from ..drivers import TTkInputDriver

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.TTkTerm.term   import TTkTerm
from TermTk.TTkCore.TTkTerm.inputkey   import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent


class TTkInput:
    inputEvent = pyTTkSignal(TTkKeyEvent, TTkMouseEvent)
    pasteEvent = pyTTkSignal(str)
    _pasteBuffer = ""
    _bracketedPaste = False
    _readInput = None
    _inputThread = None
    _inputQueue = None
    _leftLastTime = 0
    _midLastTime = 0
    _rightLastTime = 0
    _leftTap = 0
    _midTap = 0
    _rightTap = 0
    _mouse_re = re.compile(r"\033\[<(\d+);(\d+);(\d+)([mM])")

    class Mouse(int):
        ON = 0x01
        DIRECT = 0x02

    @staticmethod
    def init(mouse:bool=False, directMouse:bool=False) -> None:
        TTkInput._readInput = TTkInputDriver()
        TTkInput._inputThread = threading.Thread(target=TTkInput._run)
        TTkInput._inputQueue = queue.Queue()
        TTkTerm.setMouse(mouse, directMouse)

    @staticmethod
    def close() -> None:
        TTkTerm.setMouse(False, False)
        if TTkInput._readInput:
            TTkInput._readInput.close()

    @staticmethod
    def stop() -> None:
        pass

    @staticmethod
    def cont() -> None:
        if TTkInput._readInput:
            TTkInput._readInput.cont()

    @staticmethod
    def start() -> None:
        TTkInput._inputThread.start()
        while inq := TTkInput._inputQueue.get():
            kevt,mevt,paste = inq

            # Try to filter out the queued moved mouse events
            while (not kevt and
                   not paste and
                   mevt and mevt.evt == TTkK.Drag and
                   not TTkInput._inputQueue.empty() ):
                mevtOld = mevt
                kevt, mevt, paste = TTkInput._inputQueue.get()
                if (kevt  or
                    paste or
                    mevt and mevt.evt != TTkK.Drag):
                    TTkInput.inputEvent.emit(kevt, mevtOld)
                    break

            if kevt or mevt:
                TTkInput.inputEvent.emit(kevt, mevt)
            if paste:
                TTkInput.pasteEvent.emit(paste)
        TTkLog.debug("Close TTkInput")

    @staticmethod
    def _run():
        for stdinRead in TTkInput._readInput.read():
            outq = TTkInput.key_process(stdinRead)
            TTkInput._inputQueue.put(outq)
        TTkInput._inputQueue.put(None)

    @staticmethod
    def _handleBracketedPaste(stdinRead:str):
        if stdinRead.endswith("\033[201~"):
            TTkInput._pasteBuffer += stdinRead[:-6]
            TTkInput._bracketedPaste = False
            # due to the CRNL methos (don't ask me why) the terminal
            # is substituting all the \n with \r
            _paste = TTkInput._pasteBuffer.replace('\r','\n')
            TTkInput._pasteBuffer = ""
            return None, None, _paste
        else:
            TTkInput._pasteBuffer += stdinRead
        return None, None, None

    @staticmethod
    def key_process(stdinRead:str) -> None:
        if TTkInput._bracketedPaste:
            return TTkInput._handleBracketedPaste(stdinRead)

        mevt,kevt = None,None

        if not stdinRead.startswith("\033[<"):
            # Key Event
            kevt = TTkKeyEvent.parse(stdinRead)
        else:
            # Mouse Event
            m = TTkInput._mouse_re.match(stdinRead)
            if not m:
                # TODO: Return Error
                hex = [f"0x{ord(x):02x}" for x in stdinRead]
                TTkLog.error("UNHANDLED (mouse): "+stdinRead.replace("\033","<ESC>") + " - "+",".join(hex))
                return None, None, None
            code = int(m.group(1))
            x = int(m.group(2))-1
            y = int(m.group(3))-1
            state = m.group(4)
            key = TTkMouseEvent.NoButton
            evt = TTkMouseEvent.Move
            tap = 0

            def _checkTap(lastTime, tap):
                if state=="M":
                    t = time()
                    if (t-lastTime) < 0.4:
                        return t, tap+1
                    else:
                        return t, 1
                return lastTime, tap

            mod = TTkK.NoModifier
            if code & 0x10:
                code &= ~0x10
                mod |= TTkK.ControlModifier
            if code & 0x08:
                code &= ~0x08
                mod |= TTkK.AltModifier

            if code == 0x00:
                TTkInput._leftLastTime, TTkInput._leftTap = _checkTap(TTkInput._leftLastTime, TTkInput._leftTap)
                tap = TTkInput._leftTap
                key = TTkMouseEvent.LeftButton
                evt = TTkMouseEvent.Press if state=="M" else TTkMouseEvent.Release
            elif code == 0x01:
                TTkInput._midLastTime, TTkInput._midTap = _checkTap(TTkInput._midLastTime, TTkInput._midTap)
                tap = TTkInput._midTap
                key = TTkMouseEvent.MidButton
                evt = TTkMouseEvent.Press if state=="M" else TTkMouseEvent.Release
            elif code == 0x02:
                TTkInput._rightLastTime, TTkInput._rightTap = _checkTap(TTkInput._rightLastTime, TTkInput._rightTap)
                tap = TTkInput._rightTap
                key = TTkMouseEvent.RightButton
                evt = TTkMouseEvent.Press if state=="M" else TTkMouseEvent.Release
            elif code == 0x20:
                key = TTkMouseEvent.LeftButton
                evt = TTkMouseEvent.Drag
            elif code == 0x21:
                key = TTkMouseEvent.MidButton
                evt = TTkMouseEvent.Drag
            elif code == 0x22:
                key = TTkMouseEvent.RightButton
                evt = TTkMouseEvent.Drag
            elif code == 0x40:
                key = TTkMouseEvent.Wheel
                evt = TTkMouseEvent.Up
            elif code == 0x41:
                key = TTkMouseEvent.Wheel
                evt = TTkMouseEvent.Down
            elif code == 0x42:
                key = TTkMouseEvent.Wheel
                evt = TTkMouseEvent.Left
            elif code == 0x43:
                key = TTkMouseEvent.Wheel
                evt = TTkMouseEvent.Right
            elif code == 0x23:
                evt = TTkMouseEvent.Move
            elif code == 0x27:
                mod |= TTkK.ShiftModifier
                evt = TTkMouseEvent.Move

            mevt = TTkMouseEvent(x, y, key, evt, mod, tap, m.group(0).replace("\033", "<ESC>"))
        if kevt or mevt:
            return kevt, mevt, None

        if stdinRead.startswith("\033[200~"):
            TTkInput._bracketedPaste = True
            return TTkInput._handleBracketedPaste(stdinRead[6:])

        hex = [f"0x{ord(x):02x}" for x in stdinRead]
        TTkLog.error("UNHANDLED: "+stdinRead.replace("\033","<ESC>") + " - "+",".join(hex))
