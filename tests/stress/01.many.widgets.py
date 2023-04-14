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

import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))

import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk(layout=ttk.TTkGridLayout())

root.layout().addWidget(btn:=ttk.TTkButton(text="Add Buttons",border=True,maxHeight=3),0,0)
root.layout().addWidget(sa:=ttk.TTkScrollArea(),1,0,1,2)
root.layout().addWidget(ttk.TTkLogViewer(maxHeight=10),2,0,1,2)

sa.viewport().setLayout(ttk.TTkVBoxLayout())

class DelButton(ttk.TTkButton):
    def __del__(self):
        ttk.TTkLog.info(f"DEL: {self._text}")
        return super().__del__()

buttons = []
def _addMany():
    ttk.TTkLog.info("Start Stress!!!")
    dl = sa.viewport().layout()
    sa.viewport().setLayout(ttk.TTkVBoxLayout())
    layouts = []
    for i in range(50):
        layout = ttk.TTkHBoxLayout()
        btns = []
        for ii in range(50):
            buttons.append(btnx := DelButton(text=f"btn:{i:03}-{ii:03}",border=True))
            btnx.setMinimumWidth(random.randint(10,40))
            btns.append(btnx)
            # layout.addWidget(btnx)
        layout.addWidgets(btns)
        layouts.append(layout)
        # sa.viewport().layout().addItem(layout)
        ttk.TTkLog.debug(f"{len(layouts)=}")
    # ll = ttk.TTkGridLayout()
    # ll.addItems(layouts)
    # sa.viewport().setLayout(ll)
    sa.viewport().layout().addItems(layouts)
    ttk.TTkLog.debug(f"{len(layouts)=}")

    # layout = ttk.TTkLayout()
    # layout.addWidget(DelButton())
    del dl

    ttk.TTkLog.info("End Stress!!!")

btn.clicked.connect(_addMany)

a = DelButton()
del a

root.mainloop()
