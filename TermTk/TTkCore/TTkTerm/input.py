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

import re
from time import time

import platform

if platform.system() == 'Linux':
    from TermTk.TTkCore.TTkTerm.readinputlinux import ReadInput
elif platform.system() == 'Darwin':
    from TermTk.TTkCore.TTkTerm.readinputlinux import ReadInput
elif platform.system() == 'Windows':
    raise NotImplementedError('Windows OS not yet supported')
elif platform.system() == 'Emscripten':
    raise NotImplementedError('Pyodide not yet supported')

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.TTkTerm.inputkey   import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

class TTkInput:
    __slots__ = ('_readInput', '_leftLastTime', '_midLastTime', '_rightLastTime', '_leftTap', '_midTap', '_rightTap')

    def __init__(self):
        self._readInput = ReadInput()
        self._leftLastTime = 0
        self._midLastTime = 0
        self._rightLastTime = 0
        self._leftTap = 0
        self._midTap = 0
        self._rightTap = 0

    def close(self):
        self._readInput.close()

    def get_key(self, callback=None):
        mouse_re = re.compile(r"\033\[<(\d+);(\d+);(\d+)([mM])")
        while stdinRead := self._readInput.read():
            mevt = None
            kevt = TTkKeyEvent.parse(stdinRead)
            if kevt is None and \
               stdinRead.startswith("\033[<"):
                # Mouse Event
                m = mouse_re.match(stdinRead)
                if not m:
                    # TODO: Return Error
                    TTkLog.error("UNHANDLED: "+stdinRead.replace("\033","<ESC>"))
                    continue
                code = int(m.group(1))
                x = int(m.group(2))-1
                y = int(m.group(3))-1
                state = m.group(4)
                key = TTkMouseEvent.NoButton
                evt = TTkMouseEvent.NoEvent
                tap = 0

                def _checkTap(lastTime, tap):
                    if state=="M":
                        t = time()
                        if (t-lastTime) < 0.4:
                            return t, tap+1
                        else:
                            return t, 1
                    return lastTime, tap

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
                mevt = TTkMouseEvent(x, y, key, evt, tap, m.group(0).replace("\033", "<ESC>"))

            if kevt is None and mevt is None:
                TTkLog.error("UNHANDLED: "+stdinRead.replace("\033","<ESC>"))

            if callback is not None:
                if not callback(kevt, mevt):
                    break
        TTkLog.debug("Close TTkInput")

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
