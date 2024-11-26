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

__all__ = ['TTkTimer']

import threading

from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.helper import TTkHelper

class TTkTimer(threading.Thread):
    __slots__ = (
        'timeout', '_delay',
        '_timer', '_quit', '_start')
    def __init__(self):
        self.timeout = pyTTkSignal()
        self._delay = 0
        self._quit  = threading.Event()
        self._start = threading.Event()
        self._timer = threading.Event()
        super().__init__()
        TTkHelper.quitEvent.connect(self.quit)

    def quit(self):
        TTkHelper.quitEvent.disconnect(self.quit)
        self.timeout.clear()
        self._quit.set()
        self._timer.set()
        self._start.set()

    def run(self):
        while not self._quit.is_set():
            self._start.wait()
            self._start.clear()
            if not self._timer.wait(self._delay):
                self.timeout.emit()

    @pyTTkSlot(float)
    def start(self, sec=0.0):
        self._delay = sec
        self._timer.set()
        self._timer.clear()
        self._start.set()
        if not self.native_id:
            super().start()

    @pyTTkSlot()
    def stop(self):
        self._timer.set()

