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

import asyncio
import inspect
import sys, os
import time
from datetime import datetime

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

root = ttk.TTk(layout=(rgl:=ttk.TTkGridLayout()))

rgl.addWidget(button_add   := ttk.TTkButton(maxSize=(8,3), border=True, text="+")                     , 0, 0)
rgl.addWidget(button_call  := ttk.TTkButton(maxSize=(8,3), border=True, text="Call")                  , 1, 0)
rgl.addWidget(button_call2 := ttk.TTkButton(maxSize=(8,3), border=True, text="Call2", checkable=True) , 2, 0)
button_add.clicked.connect(lambda: num.setText(int(num.text()) + 1))

rgl.addWidget(res := ttk.TTkLabel(test='out...'), 0 , 1)
rgl.addWidget(num := ttk.TTkLabel(text='1')     , 1 , 1)

rgl.addWidget(qb := ttk.TTkButton(border=True, maxWidth=8, text="Quit"), 0,2,3,1)
qb.clicked.connect(ttk.TTkHelper.quit)

rgl.addWidget(ttk.TTkLogViewer(), 3, 0, 1, 3)


# normal slot with a bolocking call
@ttk.pyTTkSlot()
def call0():
    now = datetime.now().strftime("[%Y-%m-%d]-[%H:%M:%S]")
    res.setText(f"{now} 0 Calling...")
    ttk.TTkLog.info(f"{now} 0 Calling...")
    time.sleep(1)
    res.setText(f"{now} 0 Calling... - DONE")
    ttk.TTkLog.info(f"{now} 0 Calling... - DONE")

# async call wothout slot decorator
async def call1():
    now = datetime.now().strftime("[%Y-%m-%d]-[%H:%M:%S]")
    res.setText(f"{now} 1 Calling...")
    ttk.TTkLog.info(f"{now} 1 Calling...")
    await asyncio.sleep(3)
    res.setText(f"{now} 1 Calling... - DONE")
    ttk.TTkLog.info(f"{now} 1 Calling... - DONE")

# async call with slot decorator
@ttk.pyTTkSlot()
async def call2():
    now = datetime.now().strftime("[%Y-%m-%d]-[%H:%M:%S]")
    res.setText(f"{now} 2 Calling...")
    ttk.TTkLog.info(f"{now} 2 Calling...")
    await asyncio.sleep(4)
    res.setText(f"{now} 2 Calling... - DONE")
    ttk.TTkLog.info(f"{now} 2 Calling... - DONE")

# async call with slot decorator and arguments
@ttk.pyTTkSlot(bool)
async def call3(val):
    now = datetime.now().strftime("[%Y-%m-%d]-[%H:%M:%S]")
    res.setText(f"{now} 3 Calling... {val}")
    ttk.TTkLog.info(f"{now} 3 Calling... {val}")
    await asyncio.sleep(5)
    res.setText(f"{now} 3 Calling... {val} - DONE")
    ttk.TTkLog.info(f"{now} 3 Calling... {val} - DONE")

print(inspect.iscoroutinefunction(call0))
print(inspect.iscoroutinefunction(call1))
print(inspect.iscoroutinefunction(call2))
print(inspect.iscoroutinefunction(call3))

button_call.clicked.connect(call0)
button_call.clicked.connect(call1)
button_call.clicked.connect(call2)

# button_call2.toggled.connect(call0)
button_call2.toggled.connect(call1)
button_call2.toggled.connect(call2)
button_call2.toggled.connect(call3)

root.mainloop()