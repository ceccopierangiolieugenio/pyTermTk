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

__all__ = ['TTkTerminalHelper']

import os, pty, threading
import struct, fcntl, termios
from select import select

from TermTk.TTkCore.signal import pyTTkSignal,pyTTkSlot
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkWidgets.TTkTerminal.terminal import TTkTerminal

class TTkTerminalHelper():
    '''
    :py:class:`TTkTerminalHelper` is a convenience class that simplify the initilization and the handling of a `pty <https://docs.python.org/3/library/pty.html>`__ terminal session

    .. note::
        This helper is available only on Linux and Mac

    Quickstart:

    .. code-block:: python

        import TermTk as ttk

        root = ttk.TTk(mouseTrack=True)

        win = ttk.TTkWindow(parent=root, title="Terminal", size=(80+2,24+4), layout=ttk.TTkGridLayout())

        term = ttk.TTkTerminal(parent=win)

        th = ttk.TTkTerminalHelper(term=term)
        th.runShell()

        root.mainloop()

    '''

    dataOut:pyTTkSignal
    '''
    This signal is emitted when some data is available in the pty interface

    :param data: the pty data
    :type data: str
    '''

    terminalClosed:pyTTkSignal
    '''
    This signal is emitted when the pty session ends
    '''

    __slots__ = ('_shell', '_fd', '_inout', '_pid',
                 '_quit_pipe', '_size', '_term',
                 #Signals
                 'terminalClosed', 'dataOut')
    def __init__(self, *,
                 term:TTkTerminal=None) -> None:
        '''
        :param term: The terminal handled by this helper.
        :type term: :py:class:`TTkTerminal`
        '''
        self.dataOut = pyTTkSignal(str)
        self.terminalClosed = pyTTkSignal()
        self._shell = [os.environ.get('SHELL', 'sh')]
        self._fd = None
        self._inout = None
        self._pid = None
        self._quit_pipe = None
        self._term = None
        self._size = (80,24)
        TTkHelper.quitEvent.connect(self._quit)
        if term:
            self.attachTTkTerminal(term)

    def attachTTkTerminal(self, term:TTkTerminal) -> None:
        '''
        Attach a :py:class:`TTkTerminal` to this helper.

        :param term: The terminal handled by this helper.
        :type term: :py:class:`TTkTerminal`
        '''

        self._term = term
        self.dataOut.connect(term.termWrite)
        term.termData.connect(self.push)
        term.termResized.connect(self.resize)
        term.closed.connect(self._quit)

    def runShell(self, program:str=None) -> None:
        '''
        Run a "program" attaching it the the pty session linked to this terminal.

        :param program: The program required to run, defaults to the cmd defined bu the "SHELL" env variable or "sh" if missing
        :type program: str, optional
        '''
        self._shell = program if program else self._shell
        if isinstance(self._shell, str):
            self._shell = [self._shell]
        elif type(self._shell) not in [list,tuple]:
            raise TypeError(f"Program type '{type(self._shell)}' of '{self._shell}' not accepted")

        self._pid, self._fd = pty.fork()

        if self._pid == 0:
            def _spawnTerminal(argv=self._shell, env=os.environ):
                env=env.copy()
                env.pop("TERMTK_GPM",None)
                env.pop("TERMTK_MOUSE",None)
                env['TERM']='screen'
                os.execvpe(argv[0], argv, env)
            # threading.Thread(target=_spawnTerminal).start()
            # TTkHelper.quit()
            _spawnTerminal()
            import sys
            sys.exit()
        else:
            self._inout = os.fdopen(self._fd, "w+b", 0)
            # name = os.ttyname(self._fd)
            TTkLog.debug(f"{self._pid=} {self._fd=}")

            self._quit_pipe = os.pipe()

            threading.Thread(target=self.loop).start()
            threading.Thread(target=lambda pid=self._pid:os.waitpid(pid,0)).start()

            if self._term:
                self.resize(*self._term.termSize())
                self._term = None

    @pyTTkSlot(int, int)
    def resize(self, width: int, height: int) -> None:
        '''
        Send a resize "`TIOCSWINSZ <https://docs.python.org/3/library/termios.html#termios.tcgetwinsize>`__" ioctl to the pty session

        :param width: the new width
        :type width: int
        :param height: the new height
        :type height: int
        '''
        # if w<=0 or h<=0: return
        # if self._fd:
        #     s = struct.pack('HHHH', h, w, 0, 0)
        #     t = fcntl.ioctl(self._fd, termios.TIOCSWINSZ, s)
        if self._fd and self._size != (width,height):
            self._size = (width,height)
            if width<=0 or height<=0: return
            s = struct.pack('HHHH', height, width, 0, 0)
            t = fcntl.ioctl(self._fd, termios.TIOCSWINSZ, s)

    @pyTTkSlot(str)
    def push(self, data:str) -> None:
        '''
        Send the data to the pty session

        :param data: the data
        :type data: str
        '''
        self._inout.write(data)

    @pyTTkSlot()
    def _quit(self):
        TTkHelper.quitEvent.disconnect(self._quit)
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

    def loop(self) -> None:
        '''
        This is the main loop routine responsible of handling the pty and terminal events,
        for example, forwarding the input codes to the pty session and the pty output to the terminal emulator.

        ::

            TTkTerminal
            ╔═══════╗                                                       pty
            ║ C:\   ║ --[ KeyPresses, MouseEvents, ResizeSignal, ... ]--> ┌──── ── ─  ─
            ║       ║ <---------[ Output, Ansi escape codes, ... ]------- │ bash, sh, ...
            ╚═══════╝                                                     └──── ── ─  ─

        .. caution:: Do not touch this! (unless you know what you are doing)
        '''

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
