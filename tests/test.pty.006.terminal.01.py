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

ttk.TTkLog.use_default_file_logging()
root = ttk.TTk()

wlog = ttk.TTkWindow(parent=root,pos = (32,12), size=(90,20), title="Log Window", flags=ttk.TTkK.WindowFlag.WindowCloseButtonHint|ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
wlog.setLayout(ttk.TTkHBoxLayout())
ttk.TTkLogViewer(parent=wlog, follow=False )

win1  = ttk.TTkWindow(parent=root, pos=(1,1), size=(70,15), title="Terminallo n.1", border=True, layout=ttk.TTkVBoxLayout(), flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
term1 = ttk.TTkTerminal(parent=win1)
term1.runShell()

win2  = ttk.TTkWindow(parent=root, pos=(10,5), size=(70,15), title="Terminallo n.2", border=True, layout=ttk.TTkVBoxLayout(), flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
term2 = ttk.TTkTerminal(parent=win2)
term2.runShell()


root.mainloop()