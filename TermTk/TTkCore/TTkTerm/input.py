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

import platform

if platform.system() == 'Linux':
    from .readinputlinux import ReadInput
    # from .readinputlinux_thread import ReadInput
elif platform.system() == 'Darwin':
    from .readinputlinux import ReadInput
elif platform.system() == 'Windows':
    raise NotImplementedError('Windows OS not yet supported')

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.TTkTerm.inputkey   import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

class TTkInput:
    __slots__ = (
            '_readInput',
            '_leftLastTime', '_midLastTime', '_rightLastTime',
            '_leftTap', '_midTap', '_rightTap',
            '_pasteBuffer', '_bracketedPaste',
            # Signals
            'inputEvent', 'pasteEvent'
            )

    def __init__(self):
        self.inputEvent = pyTTkSignal(TTkKeyEvent, TTkMouseEvent)
        self.pasteEvent = pyTTkSignal(str)
        self._pasteBuffer = ""
        self._bracketedPaste = False
        self._readInput = None
        self._leftLastTime = 0
        self._midLastTime = 0
        self._rightLastTime = 0
        self._leftTap = 0
        self._midTap = 0
        self._rightTap = 0

    def close(self):
        if self._readInput:
            self._readInput.close()

    def stop(self):
        pass

    def cont(self):
        if self._readInput:
            self._readInput.cont()

    def start(self):
        self._readInput = ReadInput()
        for stdinRead in self._readInput.read():
            self.key_process(stdinRead)
        TTkLog.debug("Close TTkInput")

    mouse_re = re.compile(r"\033\[<(\d+);(\d+);(\d+)([mM])")
    def key_process(self, stdinRead):
        if self._bracketedPaste:
            if stdinRead.endswith("\033[201~"):
                self._pasteBuffer += stdinRead[:-6]
                self._bracketedPaste = False
                # due to the CRNL methos (don't ask me why) the terminal
                # is substituting all the \n with \r
                self.pasteEvent.emit(self._pasteBuffer.replace('\r','\n'))
                self._pasteBuffer = ""
            else:
                self._pasteBuffer += stdinRead
            return

        mevt,kevt = None, None

        if not stdinRead.startswith("\033[<"):
            # Key Event
            kevt = TTkKeyEvent.parse(stdinRead)
        else:
            # Mouse Event
            m = self.mouse_re.match(stdinRead)
            if not m:
                # TODO: Return Error
                hex = [f"0x{ord(x):02x}" for x in stdinRead]
                TTkLog.error("UNHANDLED (mouse): "+stdinRead.replace("\033","<ESC>") + " - "+",".join(hex))
                return None, None
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
                self._leftLastTime, self._leftTap = _checkTap(self._leftLastTime, self._leftTap)
                tap = self._leftTap
                key = TTkMouseEvent.LeftButton
                evt = TTkMouseEvent.Press if state=="M" else TTkMouseEvent.Release
            elif code == 0x01:
                self._midLastTime, self._midTap = _checkTap(self._midLastTime, self._midTap)
                tap = self._midTap
                key = TTkMouseEvent.MidButton
                evt = TTkMouseEvent.Press if state=="M" else TTkMouseEvent.Release
            elif code == 0x02:
                self._rightLastTime, self._rightTap = _checkTap(self._rightLastTime, self._rightTap)
                tap = self._rightTap
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
            elif code == 0x23:
                evt = TTkMouseEvent.Move
            elif code == 0x27:
                mod |= TTkK.ShiftModifier
                evt = TTkMouseEvent.Move

            mevt = TTkMouseEvent(x, y, key, evt, mod, tap, m.group(0).replace("\033", "<ESC>"))
        if kevt or mevt:
            self.inputEvent.emit(kevt, mevt)
            return

        if stdinRead.startswith("\033[200~"):
            self._pasteBuffer = stdinRead[6:]
            self._bracketedPaste = True
            return

        hex = [f"0x{ord(x):02x}" for x in stdinRead]
        TTkLog.error("UNHANDLED: "+stdinRead.replace("\033","<ESC>") + " - "+",".join(hex))


def main():
    print("Retrieve Keyboard, Mouse press/drag/wheel Events")
    print("Press q or <ESC> to exit")
    from term import TTkTerm

    TTkTerm.push(TTkTerm.Mouse.ON)
    TTkTerm.setEcho(False)

    def callback(kevt=None, mevt=None):
        if kevt is not None:
            print(f"Key Event: {kevt}")
        if mevt is not None:
            print(f"Mouse Event: {mevt}")

    testInput = TTkInput()
    testInput.get_key(callback)

    TTkTerm.push(TTkTerm.Mouse.OFF + TTkTerm.Mouse.DIRECT_OFF)
    TTkTerm.setEcho(True)

if __name__ == "__main__":
    main()
