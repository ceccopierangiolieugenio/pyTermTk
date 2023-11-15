#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the"Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED"AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This test is based on:
#   pty — Pseudo-terminal utilities¶
#   https://docs.python.org/3/library/pty.html#example
#
#   Using a pseudo-terminal to interact with interactive Python in a subprocess
#   by Thomas Billinger
#   https://gist.github.com/thomasballinger/7979808

import os
import pty
import tty
import sys
import time
import subprocess
import threading
from select import select


sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

class TermThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.shell = os.environ.get('SHELL', 'sh')
        self.master, self.slave = pty.openpty()
        self.p = subprocess.Popen(
            [self.shell],
            stdin=self.slave,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        self.pin = os.fdopen(self.master, 'w')

        name = os.ttyname(self.master)
        ttk.TTkLog.debug(f"{self.master=} {name}")

        name = os.ttyname(self.slave)
        ttk.TTkLog.debug(f"{self.slave=} {name}")

    def setTextEdit(self, te):
        self.textEdit = te

    def run(self):
        msg = ''
        errmsg = ''

        while True:
            rs, ws, es = select([self.p.stdout, self.p.stderr], [], [])
            for r in rs:
                if r is self.p.stdout:
                    while l := self.p.stdout.readline():
                        ttk.TTkLog.debug(f'Eugenio->{l}')
                        self.textEdit.append(l[:-1].decode('ascii'))
                elif r is self.p.stderr:
                    errmsg += self.p.stderr.read(1)
                    ttk.TTkLog.debug(f'ERR~{errmsg}')
                    if errmsg.endswith('>>> '):
                        errmsg = errmsg[:-4]
                    if errmsg.endswith('\n'):
                        errmsg = ''

class TerminalView(ttk.TTkTextEditView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.termThread = kwargs.get('termThread')

    def mousePressEvent(self, evt):
        return True

    def keyEvent(self, evt):
        if evt.type == ttk.TTkK.SpecialKey:
            if evt.key == ttk.TTkK.Key_Enter:
                ttk.TTkLog.debug(f"Key: {evt}")
                self.termThread.pin.write('\n')
        else: # Input char
            ttk.TTkLog.debug(f"Key: {evt.key}")
            self.termThread.pin.write(evt.key)
        return True

ttk.TTkLog.use_default_file_logging()
root = ttk.TTk()

wlog = ttk.TTkWindow(parent=root,pos = (15,4), size=(87,20), title="Log Window", flags=ttk.TTkK.WindowFlag.WindowCloseButtonHint)
wlog.setLayout(ttk.TTkHBoxLayout())
ttk.TTkLogViewer(parent=wlog, follow=True )


win = ttk.TTkWindow(parent=root, pos=(1,1), size=(70,15), title="Terminallo", border=True, layout=ttk.TTkVBoxLayout())

tt = TermThread()

te = ttk.TTkTextEdit(lineNumber=True, textEditView=TerminalView(termThread=tt))
le = ttk.TTkLineEdit()

win.layout().addWidget(te)
win.layout().addWidget(le)

tt.setTextEdit(te)
tt.start()

def _sendCrap():
    ttk.TTkLog.debug(f"Sending: {le.text()}")
    tt.pin.write(f"{le.text()}\n")
le.returnPressed.connect(_sendCrap)
# le.setFocus()

root.mainloop()