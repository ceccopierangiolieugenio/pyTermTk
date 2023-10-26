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

import sys, os
from threading import Thread, Lock

from ..TTkTerm.term_base import TTkTermBase
from TermTk.TTkCore.log import TTkLog
from .windows import *

class TTkTerm(TTkTermBase):
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
    def _getTerminalSize():
       try:
           return os.get_terminal_size()
       except OSError as e:
           print(f'ERROR: {e}')
    TTkTermBase.getTerminalSize = _getTerminalSize

    _sigWinChMutex = Lock()

    @staticmethod
    def _sigWinCh(w,h):
        def _sigWinChThreaded():
            if not TTkTerm._sigWinChMutex.acquire(blocking=False): return
            while (TTkTerm.width, TTkTerm.height) != (wh:=TTkTerm.getTerminalSize()):
                TTkTerm.width, TTkTerm.height = wh
                if TTkTerm._sigWinChCb is not None:
                    TTkTerm._sigWinChCb(TTkTerm.width, TTkTerm.height)
            TTkTerm._sigWinChMutex.release()
        Thread(target=_sigWinChThreaded).start()

    @staticmethod
    def _registerResizeCb(callback):
        TTkTerm._sigWinChCb = callback
        TTkInputDriver.windowResized.connect(TTkTerm._sigWinCh)
    TTkTermBase.registerResizeCb = _registerResizeCb