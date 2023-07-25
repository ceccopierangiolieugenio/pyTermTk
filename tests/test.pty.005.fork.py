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
#   pyte - In memory VTXXX-compatible terminal emulator.
#          Terminal Emulator Example
#   https://github.com/selectel/pyte/blob/master/examples/terminal_emulator.py
#
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
import sys
import threading
from select import select


sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

class TermThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._shell = os.environ.get('SHELL', 'sh')

        # This slice is loosely inspired by:
        # https://github.com/selectel/pyte/blob/b40cf6261fdf7a05a7d7fd04ea7d9b0ea1743269/examples/terminal_emulator.py#L109-L115
        pid, self._fd = pty.fork()
        if pid == 0:
            argv = [self._shell]
            env = dict(TERM="screen", DISPLAY=":1")
            os.execvpe(argv[0], argv, env)

        self._inout = os.fdopen(self._fd, "w+b", 0)

        name = os.ttyname(self._fd)
        ttk.TTkLog.debug(f"{self._fd=} {name}")

    def setTextEdit(self, te):
        self.textEdit = te

    def run(self):
        while rs := select( [self._inout], [], [])[0]:
            ttk.TTkLog.debug(f"Select - {rs=}")
            for r in rs:
                if r is self._inout:
                    try:
                        o = self._inout.read(10240)
                    except Exception as e:
                        ttk.TTkLog.error(f"Error: {e=}")
                        return
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
                self.termThread._inout.write(b'\n')
        else: # Input char
            ttk.TTkLog.debug(f"Key: {evt.key}")
            self.termThread._inout.write(evt.key.encode())
        return True

ttk.TTkLog.use_default_file_logging()
root = ttk.TTk()

wlog = ttk.TTkWindow(parent=root,pos = (32,12), size=(90,20), title="Log Window", flags=ttk.TTkK.WindowFlag.WindowCloseButtonHint)
wlog.setLayout(ttk.TTkHBoxLayout())
ttk.TTkLogViewer(parent=wlog, follow=True )

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


root.mainloop()