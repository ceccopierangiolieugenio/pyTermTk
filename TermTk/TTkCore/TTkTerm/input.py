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

if platform.system() == "Linux":
    from TermTk.TTkCore.TTkTerm.readinputlinux import *
elif platform.system() == "Darwin":
    from TermTk.TTkCore.TTkTerm.readinputlinux import *
elif platform.system() == "Windows":
    raise NotImplementedError("Windows OS not yet supported")
elif platform.system() == "Emscripten":
    raise NotImplementedError("Pyodide not yet supported")

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.TTkTerm.inputkey import KeyEvent


class TTkMouseEvent:
    # Keys
    NoButton = (
        TTkK.NoButton
    )  # The button state does not refer to any button (see QMouseEvent::button()).
    AllButtons = (
        TTkK.AllButtons
    )  # This value corresponds to a mask of all possible mouse buttons. Use to set the 'acceptedButtons' property of a MouseArea to accept ALL mouse buttons.
    LeftButton = (
        TTkK.LeftButton
    )  # The left button is pressed, or an event refers to the left button. (The left button may be the right button on left-handed mice.)
    RightButton = TTkK.RightButton  # The right button.
    MidButton = TTkK.MidButton  # The middle button.
    MiddleButton = TTkK.MiddleButton  # The middle button.
    Wheel = TTkK.Wheel

    # Events
    NoEvent = TTkK.NoEvent
    Press = TTkK.Press
    Release = TTkK.Release
    Drag = TTkK.Drag
    Move = TTkK.Move
    Up = TTkK.WHEEL_Up
    Down = TTkK.WHEEL_Down

    __slots__ = ("x", "y", "key", "evt", "tap", "raw")

    def __init__(self, x: int, y: int, key: int, evt: int, tap: int, raw: str):
        self.x = x
        self.y = y
        self.key = key
        self.evt = evt
        self.raw = raw
        self.tap = tap

    def clone(self, pos=None, evt=None):
        x, y = pos or (self.x, self.y)
        evt = evt or self.evt
        return TTkMouseEvent(x, y, self.key, evt, self.tap, self.raw)

    def key2str(self):
        return {
            TTkMouseEvent.NoButton: "NoButton",
            TTkMouseEvent.AllButtons: "AllButtons",
            TTkMouseEvent.LeftButton: "LeftButton",
            TTkMouseEvent.RightButton: "RightButton",
            TTkMouseEvent.MidButton: "MidButton",
            TTkMouseEvent.MiddleButton: "MiddleButton",
            TTkMouseEvent.Wheel: "Wheel",
        }.get(self.key, "Undefined")

    def evt2str(self):
        return {
            TTkMouseEvent.NoEvent: "NoEvent",
            TTkMouseEvent.Press: "Press",
            TTkMouseEvent.Release: "Release",
            TTkMouseEvent.Drag: "Drag",
            TTkMouseEvent.Move: "Move",
            TTkMouseEvent.Up: "Up",
            TTkMouseEvent.Down: "Down",
        }.get(self.evt, "Undefined")

    def __str__(self):
        return f"MouseEvent ({self.x},{self.y}) {self.key2str()} {self.evt2str()} tap:{self.tap} - {self.raw}"


class TTkInput:
    _leftLastTime = 0
    _midLastTime = 0
    _rightLastTime = 0
    _leftTap = 0
    _midTap = 0
    _rightTap = 0

    @staticmethod
    def get_key(callback=None):
        mouse_re = re.compile(r"\033\[<(\d+);(\d+);(\d+)([mM])")
        while not False:
            stdinRead = readInput()

            mevt = None
            kevt = KeyEvent.parse(stdinRead)
            if kevt is None and stdinRead.startswith("\033[<"):
                # Mouse Event
                m = mouse_re.match(stdinRead)
                if not m:
                    # TODO: Return Error
                    TTkLog.error("UNHANDLED: " + stdinRead.replace("\033", "<ESC>"))
                    continue
                code = int(m.group(1))
                x = int(m.group(2)) - 1
                y = int(m.group(3)) - 1
                state = m.group(4)
                key = TTkMouseEvent.NoButton
                evt = TTkMouseEvent.NoEvent
                tap = 0

                def _checkTap(lastTime, tap):
                    if state == "M":
                        t = time()
                        if (t - lastTime) < 0.4:
                            return t, tap + 1
                        else:
                            return t, 1
                    return lastTime, tap

                if code == 0x00:
                    TTkInput._leftLastTime, TTkInput._leftTap = _checkTap(
                        TTkInput._leftLastTime, TTkInput._leftTap
                    )
                    tap = TTkInput._leftTap
                    key = TTkMouseEvent.LeftButton
                    evt = TTkMouseEvent.Press if state == "M" else TTkMouseEvent.Release
                elif code == 0x01:
                    TTkInput._midLastTime, TTkInput._midTap = _checkTap(
                        TTkInput._midLastTime, TTkInput._midTap
                    )
                    tap = TTkInput._midTap
                    key = TTkMouseEvent.MidButton
                    evt = TTkMouseEvent.Press if state == "M" else TTkMouseEvent.Release
                elif code == 0x02:
                    TTkInput._rightLastTime, TTkInput._rightTap = _checkTap(
                        TTkInput._rightLastTime, TTkInput._rightTap
                    )
                    tap = TTkInput._rightTap
                    key = TTkMouseEvent.RightButton
                    evt = TTkMouseEvent.Press if state == "M" else TTkMouseEvent.Release
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
                mevt = TTkMouseEvent(
                    x, y, key, evt, tap, m.group(0).replace("\033", "<ESC>")
                )

            if kevt is None and mevt is None:
                TTkLog.error("UNHANDLED: " + stdinRead.replace("\033", "<ESC>"))

            if callback is not None:
                if not callback(kevt, mevt):
                    break


def main():
    print("Retrieve Keyboard, Mouse press/drag/wheel Events")
    print("Press q or <ESC> to exit")
    import term as t

    t.Term.push(t.Term.mouse_on)
    t.Term.echo(False)

    def callback(kevt=None, mevt=None):
        if kevt is not None:
            print(f"Key Event: {kevt}")
        if mevt is not None:
            print(f"Mouse Event: {mevt}")

    TTkInput.get_key(callback)

    t.Term.push(t.Term.mouse_off, t.Term.mouse_direct_off)
    t.Term.echo(True)


if __name__ == "__main__":
    main()
