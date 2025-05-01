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

__all__ = ['_TTkTerm']

import sys, os, signal
from threading import Thread, Lock

try: import termios
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)

from ..TTkTerm.term_base import TTkTermBase
from TermTk.TTkCore.log import TTkLog

class _TTkTerm(TTkTermBase):
    _sigWinChCb = None

    # Save treminal attributes during the initialization in order to
    # restore later the original states

    if os.isatty(sys.stdin.fileno()):
        _termAttr = termios.tcgetattr(sys.stdin)
    else:
        _termAttr = None

    _termAttrBk = []
    @staticmethod
    def saveTermAttr():
        _TTkTerm._termAttrBk.append(termios.tcgetattr(sys.stdin))

    @staticmethod
    def restoreTermAttr():
        if _TTkTerm._termAttrBk:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, _TTkTerm._termAttrBk.pop())
        elif _TTkTerm._termAttr:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, _TTkTerm._termAttr)

    @staticmethod
    def exit():
        TTkTermBase.exit()
        if _TTkTerm._termAttr:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, _TTkTerm._termAttr)

    @staticmethod
    def _push(*args):
        try:
            sys.stdout.write(str(*args))
            sys.stdout.flush()
        except BlockingIOError as e:
            TTkLog.fatal(f"{e=} {e.characters_written=}")
        except Exception as e:
            TTkLog.fatal(e)
    TTkTermBase.push = _push

    @staticmethod
    def _flush():
        sys.stdout.flush()
    TTkTermBase.flush = _flush

    @staticmethod
    def _setEcho(val: bool):
        # Set/Unset Terminal Input Echo
        (i,o,c,l,isp,osp,cc) = termios.tcgetattr(sys.stdin.fileno())
        if val: l |= termios.ECHO
        else:   l &= ~termios.ECHO
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, [i,o,c,l,isp,osp,cc])
    TTkTermBase.setEcho = _setEcho

    @staticmethod
    def _CRNL(val: bool):
        #Translate carriage return to newline on input (unless IGNCR is set).
        # '\n' CTRL-J
        # '\r' CTRL-M (Enter)
        (i,o,c,l,isp,osp,cc) = termios.tcgetattr(sys.stdin.fileno())
        if val: i |= termios.ICRNL
        else:    i &= ~termios.ICRNL
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, [i,o,c,l,isp,osp,cc])
    TTkTermBase.CRNL = _CRNL

    @staticmethod
    def _getTerminalSize():
       try:
           return os.get_terminal_size()
       except OSError as e:
           print(f'ERROR: {e}')
    TTkTermBase.getTerminalSize = _getTerminalSize

    _sigWinChMutex = Lock()

    @staticmethod
    def _sigWinChThreaded():
        if not _TTkTerm._sigWinChMutex.acquire(blocking=False): return
        while (_TTkTerm.width, _TTkTerm.height) != (wh:=_TTkTerm.getTerminalSize()):
            _TTkTerm.width, _TTkTerm.height = wh
            if _TTkTerm._sigWinChCb is not None:
                _TTkTerm._sigWinChCb(_TTkTerm.width, _TTkTerm.height)
        _TTkTerm._sigWinChMutex.release()

    @staticmethod
    def _sigWinCh(signum, frame):
        Thread(target=_TTkTerm._sigWinChThreaded).start()

    @staticmethod
    def _registerResizeCb(callback):
        _TTkTerm._sigWinChCb = callback
        # Dummy call to retrieve the terminal size
        _TTkTerm._sigWinCh(signal.SIGWINCH, None)
        signal.signal(signal.SIGWINCH, _TTkTerm._sigWinCh)
    TTkTermBase.registerResizeCb = _registerResizeCb
