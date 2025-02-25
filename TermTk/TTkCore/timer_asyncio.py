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

from TermTk.TTkCore.drivers import TTkAsyncio
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.helper import TTkHelper

class TTkTimer():
    __slots__ = (
        'timeout', '_timerHandle')
    def __init__(self):
        self.timeout = pyTTkSignal()
        self._timerHandle = None
        super().__init__()
        TTkHelper.quitEvent.connect(self.quit)

    def quit(self):
        TTkHelper.quitEvent.disconnect(self.quit)
        if self._timerHandle:
            self._timerHandle.cancel()
        self.timeout.clear()

    # def run(self):
    #     self.timeout.emit()

    @pyTTkSlot(float)
    def start(self, sec=0.0):
        self._timerHandle = TTkAsyncio.loop.call_later(sec, self.timeout.emit)

    @pyTTkSlot()
    def stop(self):
        # delay = self._timerHandle.when() - TTkAsyncio.loop.time()
        if self._timerHandle:
            self._timerHandle.cancel()

