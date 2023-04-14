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


sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

class thread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        pass

shell = os.environ.get('SHELL', 'sh')

master,slave = pty.openpty()
p = subprocess.Popen([shell], stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pin = os.fdopen(master, 'w')
tty.setcbreak(sys.stdin)

# pin.write('ls -la\n')

msg = ''
errmsg = ''

while True:
    rs, ws, es = select([sys.stdin, p.stdout, p.stderr], [], [])
    for r in rs:
        if r is sys.stdin:
            c = r.read(1)
            if c == '\n':
                pin.write(msg+'\n')
                print(f'\r>>> {msg}')
                msg = ''
            else:
                msg += c
                print(f'>>> {msg}')
                sys.stdout.flush()
        elif r is p.stdout:
            l = p.stdout.readline()
            print(f'Eugenio->{l}')
            sys.stderr.flush()
        elif r is p.stderr:
            errmsg += p.stderr.read(1)
            if errmsg.endswith('>>> '):
                errmsg = errmsg[:-4]
            if errmsg.endswith('\n'):
                print(f'ERR~{errmsg}')
                errmsg = ''