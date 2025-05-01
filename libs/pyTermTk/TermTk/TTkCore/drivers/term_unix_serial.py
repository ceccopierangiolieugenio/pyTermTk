# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkTerm']

from ..TTkTerm.term_base import TTkTermBase
from .term_unix_linux import *

class _TTkTermSerial():
    @staticmethod
    def _getTerminalSizeSerial():
        import sys, os, tty, select, re
        try: import termios, fcntl
        except Exception as e:
            print(f'ERROR: {e}')
            exit(1)
        _attr = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)
        def _read_new():
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
                        yield ansi
                else:
                    for ch in stdinRead:
                        yield ch
        w,h = 80,24
        try:
            sys.stdout.write('\033[s\033[999;999H\033[6n\033[u')
            sys.stdout.flush()
            for stdinRead in _read_new():
                if m := re.match(r"\[(\d+);(\d+)R",stdinRead):
                    h = int(m.group(1))
                    w = int(m.group(2))
                break
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSANOW, _attr)
        return w,h
    _w, _h = None,None

    @staticmethod
    def _getTerminalSize():
        if _TTkTermSerial._w is None:
            _TTkTermSerial._w, _TTkTermSerial._h = _TTkTermSerial._getTerminalSizeSerial()
        return _TTkTermSerial._w, _TTkTermSerial._h

    TTkTermBase.getTerminalSize = _getTerminalSize



