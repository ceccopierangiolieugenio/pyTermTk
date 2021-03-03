#!/usr/bin/env python3

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

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal


class TTkTimer(threading.Thread):
    _timers = []
    __slots__ = (
        'timeout', '_timerEvent',
        '_delay', '_delayLock', '_quit',
        '_stopTime')
    def __init__(self):
        # Define Signals
        self.timeout = pyTTkSignal()

        self._timerEvent = threading.Event()
        self._quit = threading.Event()
        self._stopTime = 0
        self._delay=0
        self._delayLock = threading.Lock()
        threading.Thread.__init__(self)
        TTkTimer._timers.append(self)
        threading.Thread.start(self)

    @staticmethod
    def quitAll():
        for timer in TTkTimer._timers:
            timer.quit()

    def quit(self):
        self._quit.set()
        self._timerEvent.set()

    def run(self):
        while self._timerEvent.wait():
            self._timerEvent.clear()
            while self._delay > 0:
                # self._delayLock.acquire()
                delay = self._delay
                self._delay = 0
                # self._delayLock.release()
                if self._quit.wait(delay):
                    return
            self.timeout.emit()

    @pyTTkSlot(int)
    def start(self, sec=0):
        self._lastTime = time.time()
        self._delay = sec
        self._timerEvent.set()

    @pyTTkSlot()
    def stop(self):
        # TODO: Timer.stop()
        self._stopTime = time.time()
