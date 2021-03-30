#!/usr/bin/env python3

# Copyright 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
# Copyright 2020 Aristocratos (https://github.com/aristocratos/bpytop)
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os, sys, io, threading, signal, re, subprocess, logging, logging.handlers, argparse
import re
import queue
from select import select
from time import time, sleep, strftime, localtime
from typing import TextIO, List, Set, Dict, Tuple, Optional, Union, Any, Callable, ContextManager, Iterable, Type, NamedTuple

try: import fcntl, termios, tty
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.libbpytop.inputkey import *

class MouseEvent:
    # Keys
    NoButton      = TTkK.NoButton     # The button state does not refer to any button (see QMouseEvent::button()).
    AllButtons    = TTkK.AllButtons   # This value corresponds to a mask of all possible mouse buttons. Use to set the 'acceptedButtons' property of a MouseArea to accept ALL mouse buttons.
    LeftButton    = TTkK.LeftButton   # The left button is pressed, or an event refers to the left button. (The left button may be the right button on left-handed mice.)
    RightButton   = TTkK.RightButton  # The right button.
    MidButton     = TTkK.MidButton    # The middle button.
    MiddleButton  = TTkK.MiddleButton # The middle button.
    Wheel         = TTkK.Wheel

    # Events
    NoEvent = TTkK.NoEvent
    Press   = TTkK.Press
    Release = TTkK.Release
    Drag    = TTkK.Drag
    Move    = TTkK.Move
    Up      = TTkK.WHEEL_Up
    Down    = TTkK.WHEEL_Down

    __slots__ = ('x','y','key','evt','raw')
    def __init__(self, x: int, y: int, key: int, evt: int, raw: str):
        self.x = x
        self.y = y
        self.key = key
        self.evt = evt
        self.raw = raw

    def clone(self, pos=None, evt=None):
        x,y = pos or (self.x, self.y)
        evt = evt or self.evt
        return MouseEvent(x, y, self.key, evt, self.raw)

    def key2str(self):
        return {
            MouseEvent.NoButton     : "NoButton",
            MouseEvent.AllButtons   : "AllButtons",
            MouseEvent.LeftButton   : "LeftButton",
            MouseEvent.RightButton  : "RightButton",
            MouseEvent.MidButton    : "MidButton",
            MouseEvent.MiddleButton : "MiddleButton",
            MouseEvent.Wheel        : "Wheel",
        }.get(self.key, "Undefined")

    def evt2str(self):
        return {
            MouseEvent.NoEvent : "NoEvent",
            MouseEvent.Press   : "Press",
            MouseEvent.Release : "Release",
            MouseEvent.Drag    : "Drag",
            MouseEvent.Move    : "Move",
            MouseEvent.Up      : "Up",
            MouseEvent.Down    : "Down",
        }.get(self.evt, "Undefined")

    def __str__(self):
        return f"MouseEvent ({self.x},{self.y}) {self.key2str()} {self.evt2str()} - {self.raw}"

class Input:
    class _nonblocking(object):
        """Set nonblocking mode for device"""
        def __init__(self, stream: TextIO):
            self.stream = stream
            self.fd = self.stream.fileno()
        def __enter__(self):
            self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)
        def __exit__(self, *args):
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)

    class _raw(object):
        """Set raw input mode for device"""
        def __init__(self, stream: TextIO):
            self.stream = stream
            self.fd = self.stream.fileno()
        def __enter__(self):
            self.original_stty = termios.tcgetattr(self.stream)
            tty.setcbreak(self.stream)
        def __exit__(self, type, value, traceback):
            termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)

    @staticmethod
    def get_key(callback=None):
        input_key: str = ""
        mouse_re = re.compile(r"\033\[<(\d+);(\d+);(\d+)([mM])")

        while not False:
            with Input._raw(sys.stdin):
                #if not select([sys.stdin], [], [], 0.1)[0]:     #* Wait 100ms for input on stdin then restart loop to check for stop flag
                #    continue
                input_key += sys.stdin.read(1)                  #* Read 1 key safely with blocking on
                if input_key == "\033":                         #* If first character is a escape sequence keep reading
                    with Input._nonblocking(sys.stdin):                #* Set non blocking to prevent read stall
                        input_key += sys.stdin.read(20)
                        if input_key.startswith("\033[<"):
                            _ = sys.stdin.read(1000)
                # TTkLog.debug("INPUT: "+input_key.replace("\033","<ESC>"))
                mevt = None
                kevt = KeyEvent.parse(input_key)
                if kevt is None and \
                   input_key.startswith("\033[<"):
                    # Mouse Event
                    m = mouse_re.match(input_key)
                    if not m:
                        # TODO: Return Error
                        TTkLog.error("UNHANDLED: "+input_key.replace("\033","<ESC>"))
                        continue
                    code = int(m.group(1))
                    x = int(m.group(2))-1
                    y = int(m.group(3))-1
                    state = m.group(4)
                    key = MouseEvent.NoButton
                    evt = MouseEvent.NoEvent
                    if code == 0x00:
                        key = MouseEvent.LeftButton
                        evt = MouseEvent.Press if state=="M" else MouseEvent.Release
                    elif code == 0x01:
                        key = MouseEvent.MidButton
                        evt = MouseEvent.Press if state=="M" else MouseEvent.Release
                    elif code == 0x02:
                        key = MouseEvent.RightButton
                        evt = MouseEvent.Press if state=="M" else MouseEvent.Release
                    elif code == 0x20:
                        key = MouseEvent.LeftButton
                        evt = MouseEvent.Drag
                    elif code == 0x21:
                        key = MouseEvent.MidButton
                        evt = MouseEvent.Drag
                    elif code == 0x22:
                        key = MouseEvent.RightButton
                        evt = MouseEvent.Drag
                    elif code == 0x40:
                        key = MouseEvent.Wheel
                        evt = MouseEvent.Up
                    elif code == 0x41:
                        key = MouseEvent.Wheel
                        evt = MouseEvent.Down
                    mevt = MouseEvent(x, y, key, evt, m.group(0).replace("\033", "<ESC>"))
                if kevt is None and mevt is None:
                    TTkLog.error("UNHANDLED: "+input_key.replace("\033","<ESC>"))
                input_key = ""
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

    Input.get_key(callback)

    t.Term.push(t.Term.mouse_off, t.Term.mouse_direct_off)
    t.Term.echo(True)

if __name__ == "__main__":
    main()