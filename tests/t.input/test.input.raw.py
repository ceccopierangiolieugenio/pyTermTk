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

import sys, os, select, signal
import logging

try: import fcntl, termios, tty
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)

print("Retrieve Keyboard, Mouse press/drag/wheel Events")
print("Press q or <ESC> to exit")

def termPush(*args):
    try:
        sys.stdout.write(str(*args))
        sys.stdout.flush()
    except BlockingIOError as e:
        print(f"{e=} {e.characters_written=}")
    except Exception as e:
        print(e)

def reset():
    # Reset
    termPush("\033[?1000l")
    termPush("\033[?1002l")
    termPush("\033[?1003l")
    termPush("\033[?1005l")
    termPush("\033[?1006l")
    termPush("\033[?1015l")
    termPush("\033[?1049l") # Switch to normal screen
    termPush("\033[?2004l") # Paste Bracketed mode

reset()

# termPush("\033[?2004h") # Paste Bracketed mode

# termPush("\033[?1000h") # Send Mouse X & Y on button press and release.
# termPush("\033[?1002h") # Use Cell Motion Mouse Tracking, xterm.
termPush("\033[?1003h") # Use All Motion Mouse Tracking, xterm.

termPush("\033[?1005h") # Enable UTF-8 Mouse Mode, xterm.
# termPush("\033[?1006h") # Enable SGR Mouse Mode, xterm.
# termPush("\033[?1015h") # Enable urxvt Mouse Mode.

# termPush("\033[?1049h") # Switch to alternate screen
# termPush(TTkTerm.Mouse.ON)
# termPush(TTkTerm.Mouse.DIRECT_ON)
# TTkTerm.setEcho(False)

# Init
_attr = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

# Capture Terminal Resize:
def _sigwinch(a,b):
    print(f"SIGWINCH: {os.get_terminal_size()=} {a=} {b=}")

signal.signal(signal.SIGWINCH, _sigwinch)

def read():
    rlist, _, _ = select.select( [sys.stdin], [], [] )

    _fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, _fl | os.O_NONBLOCK) # Set the input as NONBLOCK to read the full sequence
    if (stdinRead := sys.stdin.read(10000))[0] == "\033":  # Check if the stream start with an escape sequence
        # stdinRead += sys.stdin.read(20)       # Check if the stream start with an escape sequence
        # if stdinRead.startswith("\033[<"):    # Clear the buffer if this is a mouse code
        #     sys.stdin.read(0x40)
        pass
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, _fl)
    print(f"{len(stdinRead)=}")
    return stdinRead

def read_new():
    stdinRead = ''
    while rlist := select.select( [sys.stdin], [], [] )[0]:
        _fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
        fcntl.fcntl(sys.stdin, fcntl.F_SETFL, _fl | os.O_NONBLOCK) # Set the input as NONBLOCK to read the full sequence
        stdinRead = sys.stdin.buffer.read()
        fcntl.fcntl(sys.stdin, fcntl.F_SETFL, _fl)
        try:
            stdinRead = stdinRead.decode()
        except Exception as e:
            yield f"bin: {stdinRead}"
            continue
        print(f"{len(stdinRead)=}")
        if '\033' in stdinRead:
            stdinSplit = stdinRead.split('\033')
            for ansi in stdinSplit[1:]:
                print(f"{ansi=}")
                yield '<ESC>'+ansi
        else:
            for ch in stdinRead:
                yield ch

try:
    for stdinRead in read_new():
        print(f"{stdinRead=}")
finally:
    # Reset
    reset()
    termios.tcsetattr(sys.stdin, termios.TCSANOW, _attr)
