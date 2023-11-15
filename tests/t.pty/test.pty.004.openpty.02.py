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
#
#   Run interactive Bash with popen and a dedicated TTY Python
#   https://stackoverflow.com/questions/41542960/run-interactive-bash-with-popen-and-a-dedicated-tty-python

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
        pty.spawn(self.shell, self.read_pty)
        # self.p = subprocess.Popen(
        #     [self.shell],
        #     shell=True,
        #     # preexec_fn=os.setsid,
        #     # universal_newlines=True,
        #     stdin=self.slave,
        #     stdout=self.slave,
        #     stderr=self.slave)
        self.pin = os.fdopen(self.master, 'w')

        name = os.ttyname(self.master)
        ttk.TTkLog.debug(f"{self.master=} {name}")

        name = os.ttyname(self.slave)
        ttk.TTkLog.debug(f"{self.slave=} {name}")

    def read_pty(self, fds):
        pass

    def setTextEdit(self, te):
        self.textEdit = te

    def run(self):
        while self.p.poll() is None:
            rs, ws, es = select([self.master], [], [])
            ttk.TTkLog.debug(f"Select - {rs=}")
            for r in rs:
                if r is self.master:
                    o = os.read(self.master, 10240)
                    if o:
                        # ttk.TTkLog.debug(f'Eugenio->{o}')
                        # self.textEdit.append(o.decode('utf-8').replace('\r','').replace('\033[?2004h','').replace('\033[?2004l',''))
                        cursor = self.textEdit.textCursor()
                        cursor.insertText(o.decode('utf-8').replace('\r','').replace('\033[?2004h','').replace('\033[?2004l',''))
                        cursor.movePosition(ttk.TTkTextCursor.End)
                        self.textEdit.textEditView()._updateSize()
                        self.textEdit.textEditView().viewMoveTo(0, cursor.position().line)



class TerminalView(ttk.TTkTextEditView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.termThread = kwargs.get('termThread')
        self.setReadOnly(False)

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

win1 = ttk.TTkWindow(parent=root, pos=(1,1), size=(70,15), title="Terminallo n.1", border=True, layout=ttk.TTkVBoxLayout(), flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
tt1 = TermThread()
te1 = ttk.TTkTextEdit(lineNumber=True, textEditView=TerminalView(termThread=tt1))
win1.layout().addWidget(te1)
tt1.setTextEdit(te1)
tt1.start()

win2 = ttk.TTkWindow(parent=root, pos=(10,5), size=(70,15), title="Terminallo n.2", border=True, layout=ttk.TTkVBoxLayout(), flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
tt2 = TermThread()
te2 = ttk.TTkTextEdit(lineNumber=True, textEditView=TerminalView(termThread=tt2))
win2.layout().addWidget(te2)
tt2.setTextEdit(te2)
tt2.start()

wlog = ttk.TTkWindow(parent=root,pos = (32,12), size=(90,20), title="Log Window", flags=ttk.TTkK.WindowFlag.WindowCloseButtonHint)
wlog.setLayout(ttk.TTkHBoxLayout())
ttk.TTkLogViewer(parent=wlog, follow=True )

root.mainloop()