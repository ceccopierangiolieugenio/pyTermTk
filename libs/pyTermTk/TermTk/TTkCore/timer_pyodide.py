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

from __future__ import annotations

__all__ = []

from typing import Optional,Callable,Dict

from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.timer_interface import _TTkTimer_Interface

import pyodideProxy  # type: ignore[import-not-found]

class _TTkTimer_Pyodide(_TTkTimer_Interface):
    _timers:Dict[int,_TTkTimer_Pyodide] = {}
    _uid = 0

    __slots__ = (
        '_id', '_running', '_timer',
        'timeout', '_timerEvent',
        '_delay', '_delayLock', '_quit',
        '_stopTime')
    timeout:pyTTkSignal
    def __init__(
            self,
            name:Optional[str]=None,
            excepthook:Optional[Callable[[Exception],None]]=None):
        # Define Signals
        self.timeout = pyTTkSignal()
        self._running = True
        self._timer = None

        self._id = _TTkTimer_Pyodide._uid
        _TTkTimer_Pyodide._uid +=1
        _TTkTimer_Pyodide._timers[self._id] = self

    @staticmethod
    def triggerTimerId(tid) -> None:
        if tid in _TTkTimer_Pyodide._timers:
            # Little hack to avoid deadloop in pyodide
            if rw := TTkHelper._rootWidget:
                rw._paintEvent.set()
            _TTkTimer_Pyodide._timers[tid].timeout.emit()

    @staticmethod
    def pyodideQuit() -> None:
        for timer in _TTkTimer_Pyodide._timers:
            _TTkTimer_Pyodide._timers[timer].timeout.clearAll()
            _TTkTimer_Pyodide._timers[timer]._running = False
            _TTkTimer_Pyodide._timers[timer].quit()
        _TTkTimer_Pyodide._timers = {}

    def quit(self) -> None:
        pass

    @pyTTkSlot(float)
    def start(self, sec=0.0) -> None:
        self.stop()
        if self._running:
            self._timer = pyodideProxy.setTimeout(int(sec*1000), self._id)
            # pyodideProxy.consoleLog(f"Timer {self._timer}")

    @pyTTkSlot()
    def stop(self) -> None:
        # pyodideProxy.consoleLog(f"Timer {self._timer}")
        if self._timer:
            pyodideProxy.stopTimeout(self._timer)
            self._timer = None

    def join(self) -> None:
        pass
