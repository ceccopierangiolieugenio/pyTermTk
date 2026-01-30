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

__all__ = []

from typing import Optional,Callable

import threading

from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.timer_interface import _TTkTimer_Interface

class _TTkTimer_Unix(threading.Thread, _TTkTimer_Interface):
    __slots__ = (
        'timeout', '_delay',
        '_timer', '_quit', '_start',
        '_excepthook'
        )
    timeout:pyTTkSignal
    _delay:float
    _excepthook:Optional[Callable[[Exception],None]]
    def __init__(
            self,
            name:Optional[str]=None,
            excepthook:Optional[Callable[[Exception],None]]=None):
        self._excepthook = excepthook
        self.timeout = pyTTkSignal()
        self._delay = 0
        self._quit  = threading.Event()
        self._start = threading.Event()
        self._timer = threading.Event()
        super().__init__(name=name)
        TTkHelper.quitEvent.connect(self.quit)

    def quit(self) -> None:
        TTkHelper.quitEvent.disconnect(self.quit)
        self.timeout.clear()
        self._quit.set()
        self._timer.set()
        self._start.set()

    def run(self) -> None:
        try:
            while not self._quit.is_set():
                self._start.wait()
                self._start.clear()
                if not self._timer.wait(self._delay):
                    self.timeout.emit()
        except Exception as e:
            TTkHelper.quitEvent.disconnect(self.quit)
            if self._excepthook:
                self._excepthook(e)
            else:
                raise e

    @pyTTkSlot(float)
    def start(self, sec:float=0.0) -> None:
        self._delay = sec
        self._timer.set()
        self._timer.clear()
        self._start.set()
        if not self.native_id:
            super().start()

    @pyTTkSlot()
    def stop(self) -> None:
        self._timer.set()
