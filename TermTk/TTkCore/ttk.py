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
import os
import signal
import time
import threading, queue

import TermTk.libbpytop as lbt
from TermTk.TTkCore.constant import TTkConstant, TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.canvas import *
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkWidgets.widget import *

class TTkTimer(threading.Thread):
    def __init__(self, callback, waitTime=1, event=None):
        threading.Thread.__init__(self)
        self.stopped = threading.Event()
        self._waitTime = waitTime
        self._callback = callback
        self._event = event

    def quit(self):
        self.stopped.set()

    def run(self):
        while not self.stopped.wait(self._waitTime):
            if self._event is not None:
                self._event.wait()
                self._event.clear()
            self._callback()

class TTk(TTkWidget):
    running: bool = False
    events = None
    key_events = None
    mouse_events = None
    screen_events = None

    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self.events = queue.Queue()
        self.key_events = queue.Queue()
        self.mouse_events = queue.Queue()
        self.screen_events = queue.Queue()
        self.setFocusPolicy(TTkWidget.ClickFocus)
        TTkHelper.registerRootCanvas(self._canvas)

    frame = 0
    time = time.time()
    def _fps(self):
        curtime = time.time()
        self.frame+=1
        delta = curtime - self.time
        if delta > 3:
            TTkLog.debug(f"fps: {int(self.frame/delta)}")
            self.frame = 0
            self.time  = curtime

    def mainloop(self):
        TTkLog.debug("Starting Main Loop...")
        # Register events
        try:
            signal.signal(signal.SIGTSTP, self._SIGSTOP) # Ctrl-Z
            signal.signal(signal.SIGCONT, self._SIGCONT) # Resume
            signal.signal(signal.SIGINT,  self._SIGINT)  # Ctrl-C
        except Exception as e:
            TTkLog.error(f"{e}")
            exit(1)
        else:
            TTkLog.debug("Signal Event Registered")

        lbt.Term.registerResizeCb(self._win_resize_cb)
        threading.Thread(target=self._input_thread, daemon=True).start()
        self._timerEvent = threading.Event()
        self._timerEvent.set()
        self._timer = TTkTimer(self._time_event, 0.03, self._timerEvent)
        self._timer.start()

        self.running = True
        lbt.Term.init()
        while self.running:
            # Main Loop
            evt = self.events.get()
            if   evt is TTkK.MOUSE_EVENT:
                mevt = self.mouse_events.get()
                focusWidget = TTkHelper.getFocus()
                if focusWidget is not None and mevt.evt != TTkK.Press:
                    x,y = TTkHelper.absPos(focusWidget)
                    nmevt = mevt.clone(pos=(mevt.x-x, mevt.y-y))
                    focusWidget.mouseEvent(nmevt)
                else:
                    self.mouseEvent(mevt)
            elif evt is TTkK.KEY_EVENT:
                kevt = self.key_events.get()
                self.keyEvent(kevt)
                # TTkLog.info(f"Key Event: {kevt}")
                pass
            elif evt is TTkK.TIME_EVENT:
                TTkHelper.paintAll()
                self._timerEvent.set()
                self._fps()
                pass
            elif evt is TTkK.SCREEN_EVENT:
                self.setGeometry(0,0,TTkGlbl.term_w,TTkGlbl.term_h)
                #TTkLog.info(f"Resize: w:{TTkGlbl.term_w}, h:{TTkGlbl.term_h}")
            elif evt is TTkK.QUIT_EVENT:
                TTkLog.debug(f"Quit.")
                break
            else:
                TTkLog.error(f"Unhandled Event {evt}")
                break

        lbt.Term.exit()
        pass

    def _time_event(self):
        self.events.put(TTkK.TIME_EVENT)

    def _win_resize_cb(self, width, height):
        TTkGlbl.term_w = int(width)
        TTkGlbl.term_h = int(height)
        self.events.put(TTkK.SCREEN_EVENT)

    def _input_thread(self):
        def _inputCallback(kevt=None, mevt=None):
            if kevt is not None:
                self.key_events.put(kevt)
                self.events.put(TTkK.KEY_EVENT)
            if mevt is not None:
                self.mouse_events.put(mevt)
                self.events.put(TTkK.MOUSE_EVENT)
            return self.running
        # Start input key loop
        lbt.Input.get_key(_inputCallback)

    def _canvas_thread(self):
        pass

    def quit(self):
        self.events.put(TTkK.QUIT_EVENT)
        self._timer.quit()
        self.running = False

    def _SIGSTOP(self, signum, frame):
        """Reset terminal settings and stop background input read before putting to sleep"""
        TTkLog.debug("Captured SIGSTOP <CTRL-z>")
        lbt.Term.stop()
        # TODO: stop the threads
        os.kill(os.getpid(), signal.SIGSTOP)

    def _SIGCONT(self, signum, frame):
        """Set terminal settings and restart background input read"""
        TTkLog.debug("Captured SIGCONT 'fg/bg'")
        lbt.Term.cont()
        # TODO: Restart threads
        # TODO: Redraw the screen

    def _SIGINT(self, signum, frame):
        TTkLog.debug("Captured SIGINT <CTRL-C>")
        # Deregister the handler
        # so CTRL-C can be redirected to the default handler if the app does not exit
        signal.signal(signal.SIGINT,  signal.SIG_DFL)
        self.quit()
