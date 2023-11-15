#!/usr/bin/env python3

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

import sys, os
import threading

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

root = ttk.TTk(title="pyTermTk Timer Test")

class TimerV2():
    __slots__ = ('timeout', '_timer')
    def __init__(self):
        # Define Signals
        self.timeout = ttk.pyTTkSignal()
        self._timer = None

    def quit(self):
        if self._timer:
            self._timer.cancel()

    @ttk.pyTTkSlot(float)
    def start(self, sec=0.0):
        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(sec, self.timeout.emit)
        self._timer.start()

    @ttk.pyTTkSlot()
    def stop(self):
        if self._timer:
            self._timer.cancel()

class TimerV3(threading.Thread):
    __slots__ = ('timeout', '_timer', '_quit', '_delay')
    def __init__(self):
        self.timeout = ttk.pyTTkSignal()
        self._delay = 0
        self._quit  = threading.Event()
        self._start = threading.Event()
        self._timer = threading.Event()
        super().__init__()
        super().start()

    def quit(self):
        self._quit.set()
        self._timer.set()
        self._start.set()

    def run(self):
        while not self._quit.is_set():
            # ttk.TTkLog.info(f"t3-2 _start.wait")
            self._start.wait()
            self._start.clear()

            # ttk.TTkLog.info(f"t3-3 _timer.wait {self._delay=}")
            if not self._timer.wait(self._delay):
                # ttk.TTkLog.info(f"t3-5 (EMIT)")
                self.timeout.emit()
            #ttk.TTkLog.info(f"t3-6")
        self._quit.set()
        #ttk.TTkLog.info(f"t3-7")

    # def run(self):
    #     self.finished.wait(self.interval)
    #     if not self.finished.is_set():
    #         self.function(*self.args, **self.kwargs)
    #     self.finished.set()

    @ttk.pyTTkSlot(float)
    def start(self, sec=0.0):
        self._delay = sec
        self._timer.set()
        self._timer.clear()
        self._start.set()

    @ttk.pyTTkSlot()
    def stop(self):
        self._timer.set()

sb = ttk.TTkSpinBox(parent=root, pos=(0,1), size=(10,1), value=2)
bStart = ttk.TTkButton(parent=root, text="Start", pos=(0,2), size=(10,3), border=True)
bStop  = ttk.TTkButton(parent=root, text="Stop",  pos=(0,5), size=(10,3), border=True)
# ttk.TTkButton(parent=root, text="Button 2", pos=(0,2), size=(10,3),  toolTip="TT Button 2", border=True)
# ttk.TTkButton(parent=root, text="Button 2", pos=(0,2), size=(10,3),  toolTip="TT Button 2", border=True)

w1 = ttk.TTkWindow(parent=root, title="LOG", pos=(0,10), size=(90,20), layout=ttk.TTkGridLayout(), toolTip="TT Log Window\n  With\nLogDump")
ttk.TTkLogViewer(parent=w1)

t2 = TimerV2()
t2.timeout.connect(lambda : ttk.TTkLog.debug(f"timeout (t2)"))
t3 = TimerV3()
t3.timeout.connect(lambda : ttk.TTkLog.debug(f"timeout (t3)"))

t3_loop = TimerV3()

@ttk.pyTTkSlot()
def _loop():
    ttk.TTkLog.debug(f"timeout (t3) LOOP")
    t3_loop.start(1)

t3_loop.timeout.connect(_loop)
t3_loop.start(1)


@ttk.pyTTkSlot()
def _start():
    v = sb.value()
    ttk.TTkLog.debug(f"start : {v=}")
    t2.start(v)
    t3.start(v)

@ttk.pyTTkSlot()
def _stop():
    t2.stop()
    t3.stop()

bStart.clicked.connect(_start)
bStop.clicked.connect(_stop)


root.mainloop()