#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
import multiprocessing
import time

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

@ttk.pyTTkSlot()
def _raise():
    raise Exception('_raise FAIL!!!')

class Fail(ttk.TTkWidget):
    fail_state:bool = False
    def mousePressEvent(self, evt):
        Fail.fail_state = True
        self.update()
        return True
    def paintEvent(self, canvas):
        if Fail.fail_state:
            raise Exception('Fail FAIL!!!')
        canvas.fill(color=ttk.TTkColor.BG_RED)
        canvas.drawText(text='💀 Draw', pos=(2,1))

def _multiprocess_task():
    process = multiprocessing.current_process()
    print(f"Task: {process.daemon=}", file=sys.stderr)
    for i in range(100):
        ttk.TTkLog.warn(f"{i=}")
        print(f"{i=}",flush=True, file=sys.stderr)
        time.sleep(0.3)

timer = ttk.TTkTimer()
timer.timeout.connect(_raise)

context = multiprocessing.get_context(method="spawn")
ctx = context.Process(target=_multiprocess_task, daemon=True)

root = ttk.TTk()

# simulate error

# Fail in the main Thread
ttk.TTkButton(parent=root,pos=(0,0),text='💀 Main',border=True).clicked.connect(_raise)
# Fail in the draw Thread
Fail(parent=root,pos=(9,0), size=(10,3))
# Generic Failure on a generic thread
ttk.TTkButton(parent=root,pos=(19,0),text='💀 a Thread',border=True).clicked.connect(lambda:threading.Thread(target=_raise).start())
# Generic Failure on a TTkTimer
ttk.TTkButton(parent=root,pos=(32,0),text='💀 a TTkTimer',border=True).clicked.connect(lambda:timer.start())

# Generic Quit
ttk.TTkButton(parent=root,pos=(50,0),text='root.Quit',border=True).clicked.connect(root.quit)
ttk.TTkButton(parent=root,pos=(61,0),text='helper.Quit',border=True).clicked.connect(ttk.TTkHelper.quit)

# Test Multiprocessing
ttk.TTkButton(parent=root,pos=(75,0),text='multiprocess',border=True).clicked.connect(ctx.start)

win=ttk.TTkWindow(parent=root, pos=(0,3), size=(100,30), border=True, layout=ttk.TTkGridLayout())
ttk.TTkLogViewer(parent=win)

if __name__ == '__main__':
    root.mainloop()
    if ctx.is_alive():
        ctx.join()
