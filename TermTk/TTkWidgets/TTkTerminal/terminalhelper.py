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

import os, pty, threading
import struct, fcntl, termios
from select import select

from TermTk.TTkCore.signal import pyTTkSignal,pyTTkSlot
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.helper import TTkHelper

class TTkTerminalHelper():
    __slots__ = ('_shell', '_fd', '_inout', '_pid',
                 '_quit_pipe', '_size', '_term',
                 #Signals
                 'terminalClosed', 'dataOut')
    def __init__(self, term=None) -> None:
        self.dataOut = pyTTkSignal(str)
        self.terminalClosed = pyTTkSignal()
        self._shell = os.environ.get('SHELL', 'sh')
        self._fd = None
        self._inout = None
        self._pid = None
        self._quit_pipe = None
        self._term = None
        self._size = (80,24)
        TTkHelper.quitEvent.connect(self._quit)
        if term:
            self.attachTTkTerminal(term)

    def attachTTkTerminal(self, term):
        self._term = term
        self.dataOut.connect(term.termWrite)
        term.termData.connect(self.push)
        term.termResized.connect(self.resize)
        term.closed.connect(self._quit)

    def runShell(self, program=None):
        self._shell = program if program else self._shell

        self._pid, self._fd = pty.fork()

        if self._pid == 0:
            def _spawnTerminal(argv=[self._shell], env=os.environ):
                os.execvpe(argv[0], argv, env)
            # threading.Thread(target=_spawnTerminal).start()
            # TTkHelper.quit()
            _spawnTerminal()
            import sys
            sys.exit()
        else:
            self._inout = os.fdopen(self._fd, "w+b", 0)
            name = os.ttyname(self._fd)
            TTkLog.debug(f"{self._pid=} {self._fd=} {name}")

            self._quit_pipe = os.pipe()

            threading.Thread(target=self.loop).start()
            threading.Thread(target=lambda pid=self._pid:os.waitpid(pid,0)).start()

            if self._term:
                self.resize(*self._term.termSize())
                self._term = None

    @pyTTkSlot(int, int)
    def resize(self, w: int, h: int):
        # if w<=0 or h<=0: return
        # if self._fd:
        #     s = struct.pack('HHHH', h, w, 0, 0)
        #     t = fcntl.ioctl(self._fd, termios.TIOCSWINSZ, s)
        if self._fd and self._size != (w,h):
            self._size = (w,h)
            if w<=0 or h<=0: return
            s = struct.pack('HHHH', h, w, 0, 0)
            t = fcntl.ioctl(self._fd, termios.TIOCSWINSZ, s)

    @pyTTkSlot(str)
    def push(self, data:str):
        self._inout.write(data)

    @pyTTkSlot()
    def _quit(self):
        if pid := self._pid:
            try:
                os.kill(pid,0)
                os.kill(pid,15)
                # os.kill(pid,9)
            except:
                pass
        if self._quit_pipe:
            try:
                os.write(self._quit_pipe[1], b'quit')
            except:
                pass

    def loop(self):
        while rs := select( [self._inout,self._quit_pipe[0]], [], [])[0]:
            if self._quit_pipe[0] in rs:
                # os.close(self._quit_pipe[0])
                os.close(self._quit_pipe[1])
                # os.close(self._resize_pipe[0])
                os.close(self._fd)
                return

            if self._inout not in rs:
                continue

            # _termLog.debug(f"Select - {rs=}")
            for r in rs:
                if r is not self._inout:
                    continue

                try:
                    _fl = fcntl.fcntl(self._inout, fcntl.F_GETFL)
                    fcntl.fcntl(self._inout, fcntl.F_SETFL, _fl | os.O_NONBLOCK) # Set the input as NONBLOCK to read the full sequence
                    out = b""
                    while _out := self._inout.read():
                        out += _out
                    fcntl.fcntl(self._inout, fcntl.F_SETFL, _fl)
                except Exception as e:
                    TTkLog.error(f"Error: {e=}")
                    self._quit()
                    self.terminalClosed.emit()
                    return

                # out = out.decode('utf-8','ignore')
                try:
                    out = out.decode()
                except Exception as e:
                    TTkLog.error(f"{e=}")
                    TTkLog.error(f"Failed to decode {out}")
                    out = out.decode('utf-8','ignore')

                self.dataOut.emit(out)
