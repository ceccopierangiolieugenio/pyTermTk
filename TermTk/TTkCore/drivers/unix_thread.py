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

__all__ = []

import sys, os
from select import select
import threading
import queue

try: import fcntl, termios, tty
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)


class ReadInput():
    __slots__ = ('_readPipe', '_inputs')

    def __init__(self):
        self._readPipe = os.pipe()
        self._inputs = queue.Queue()
        threading.Thread(target=self._pullInputThread).start()

    def cont(self):
        tty.setcbreak(sys.stdin)

    def _pullInputThread(self):
        _fn = sys.stdin
        _attr = termios.tcgetattr(_fn)
        tty.setcbreak(_fn)

        while True:
            rlist, _, _ = select( [sys.stdin, self._readPipe[0]], [], [] )

            if self._readPipe[0] in rlist:
                break

            if (stdinRead := sys.stdin.read(1)) == "\033":  # Check if the stream start with an escape sequence
                _fl = fcntl.fcntl(_fn, fcntl.F_GETFL)
                fcntl.fcntl(_fn, fcntl.F_SETFL, _fl | os.O_NONBLOCK) # Set the input as NONBLOCK to read the full sequence
                stdinRead += sys.stdin.read(20)       # Check if the stream start with an escape sequence
                if stdinRead.startswith("\033[<"):    # Clear the buffer if this is a mouse code
                    sys.stdin.read(0x40)
                fcntl.fcntl(_fn, fcntl.F_SETFL, _fl)

            self._inputs.put(stdinRead)

        termios.tcsetattr(_fn, termios.TCSANOW, _attr)
        self._inputs.put(None)


    def close(self):
        os.write(self._readPipe[1], b'quit')

    def _read_old(self):
        _fn = sys.stdin.fileno()
        _attr = termios.tcgetattr(_fn)
        tty.setcbreak(_fn)
        rlist, _, _ = select.select( [sys.stdin, self._readPipe[0]], [], [] )

        if self._readPipe[0] in rlist:
            return None

        if (stdinRead := sys.stdin.read(1)) == "\033":  # Check if the stream start with an escape sequence
            _fl = fcntl.fcntl(_fn, fcntl.F_GETFL)
            fcntl.fcntl(_fn, fcntl.F_SETFL, _fl | os.O_NONBLOCK) # Set the input as NONBLOCK to read the full sequence
            stdinRead += sys.stdin.read(20)       # Check if the stream start with an escape sequence
            if stdinRead.startswith("\033[<"):    # Clear the buffer if this is a mouse code
                sys.stdin.read(0x40)
            fcntl.fcntl(_fn, fcntl.F_SETFL, _fl)
        termios.tcsetattr(_fn, termios.TCSANOW, _attr)
        return stdinRead

    def read(self):
        return self._inputs.get()
