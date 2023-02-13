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

import threading, time
import importlib

from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal


if importlib.util.find_spec('pyodideProxy'):
    import pyodideProxy
    class TTkTimer():
        _timers = {}
        _uid = 0

        __slots__ = (
            '_id', '_running',
            'timeout', '_timerEvent',
            '_delay', '_delayLock', '_quit',
            '_stopTime')

        def __init__(self):
            # Define Signals
            self.timeout = pyTTkSignal()
            self._running = True

            self._id = TTkTimer._uid
            TTkTimer._uid +=1
            TTkTimer._timers[self._id] = self

        @staticmethod
        def triggerTimerId(tid):
            if tid in TTkTimer._timers:
                TTkTimer._timers[tid].timeout.emit()

        @staticmethod
        def quitAll():
            pass

        @staticmethod
        def pyodideQuit():
            for timer in TTkTimer._timers:
                TTkTimer._timers[timer].timeout.clearAll()
                TTkTimer._timers[timer]._running = False
                TTkTimer._timers[timer].quit()
            TTkTimer._timers = {}

        def quit(self):
            pass

        def run(self):
            pass

        @pyTTkSlot(int)
        def start(self, sec=0):
            if self._running:
                pyodideProxy.setTimeout(int(sec*1000), self._id)

        @pyTTkSlot()
        def stop(self):
            pass
else:
    # from .log import TTkLog
    class TTkTimer():
        _timers = []
        __slots__ = ('timeout', '_timer')
        def __init__(self):
            # Define Signals
            self.timeout = pyTTkSignal()
            self._timer = None
            TTkTimer._timers.append(self)

        @staticmethod
        def quitAll():
            for timer in TTkTimer._timers:
                timer.quit()

        def quit(self):
            if self._timer:
                self._timer.cancel()

        @pyTTkSlot(int)
        def start(self, sec=0):
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(sec, self.timeout.emit)
            self._timer.start()

        @pyTTkSlot()
        def stop(self):
            if self._timer:
                self._timer.cancel()
