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

__all__ = ['TTkTerm']

import sys, os, signal
from threading import Thread, Lock

try: import termios
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)

from ..TTkTerm.term_base import TTkTermBase
from TermTk.TTkCore.log import TTkLog

class TTkTerm(TTkTermBase):
    _sigWinChCb = None

    # Save treminal attributes during the initialization in order to
    # restore later the original states
    _termAttr = termios.tcgetattr(sys.stdin)

    _termAttrBk = []
    @staticmethod
    def saveTermAttr():
        TTkTerm._termAttrBk.append(termios.tcgetattr(sys.stdin))

    @staticmethod
    def restoreTermAttr():
        if TTkTerm._termAttrBk:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, TTkTerm._termAttrBk.pop())
        else:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, TTkTerm._termAttr)

    @staticmethod
    def _setSigmask(mask, value=True):
        attr = termios.tcgetattr(sys.stdin)
        if mask & TTkTerm.Sigmask.CTRL_C:
            attr[6][termios.VINTR]=  b'\x03' if value else 0
        if mask & TTkTerm.Sigmask.CTRL_S:
            attr[6][termios.VSTOP]=  b'\x13' if value else 0
        if mask & TTkTerm.Sigmask.CTRL_Z:
            attr[6][termios.VSUSP]=  b'\x1a' if value else 0
        if mask & TTkTerm.Sigmask.CTRL_Q:
            attr[6][termios.VSTART]= b'\x11' if value else 0
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, attr)
    TTkTermBase.setSigmask = _setSigmask

    @staticmethod
    def getSigmask():
        mask = 0x00
        attr = termios.tcgetattr(sys.stdin)
        mask |= TTkTerm.Sigmask.CTRL_C if attr[6][termios.VINTR]  else 0
        mask |= TTkTerm.Sigmask.CTRL_S if attr[6][termios.VSTOP]  else 0
        mask |= TTkTerm.Sigmask.CTRL_Z if attr[6][termios.VSUSP]  else 0
        mask |= TTkTerm.Sigmask.CTRL_Q if attr[6][termios.VSTART] else 0
        return mask

    @staticmethod
    def exit():
        TTkTermBase.exit()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, TTkTerm._termAttr)

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
        if not TTkTerm._sigWinChMutex.acquire(blocking=False): return
        while (TTkTerm.width, TTkTerm.height) != (wh:=TTkTerm.getTerminalSize()):
            TTkTerm.width, TTkTerm.height = wh
            if TTkTerm._sigWinChCb is not None:
                TTkTerm._sigWinChCb(TTkTerm.width, TTkTerm.height)
        TTkTerm._sigWinChMutex.release()

    @staticmethod
    def _sigWinCh(signum, frame):
        Thread(target=TTkTerm._sigWinChThreaded).start()

    @staticmethod
    def _registerResizeCb(callback):
        TTkTerm._sigWinChCb = callback
        # Dummy call to retrieve the terminal size
        TTkTerm._sigWinCh(signal.SIGWINCH, None)
        signal.signal(signal.SIGWINCH, TTkTerm._sigWinCh)
    TTkTermBase.registerResizeCb = _registerResizeCb
