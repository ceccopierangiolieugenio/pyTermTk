#!/usr/bin/env python3

# Copyright 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
# Copyright 2020 Aristocratos (https://github.com/aristocratos/bpytop)
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os, sys, io, threading, signal, re, subprocess, logging, logging.handlers, argparse
import queue
from select import select
from time import time, sleep, strftime, localtime
from typing import List, Set, Dict, Tuple, Optional, Union, Any, Callable, ContextManager, Iterable, Type, NamedTuple

try: import fcntl, termios, tty, pwd
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)

class Term:
    """Terminal info and commands"""
    width: int = 0
    height: int = 0
    fg: str = ""                                           #* Default foreground color
    bg: str = ""                                           #* Default background color
    hide_cursor      = "\033[?25l"                         #* Hide terminal cursor
    show_cursor      = "\033[?25h"                         #* Show terminal cursor
    alt_screen       = "\033[?1049h"                       #* Switch to alternate screen
    normal_screen    = "\033[?1049l"                       #* Switch to normal screen
    clear            = "\033[2J\033[0;0f"                  #* Clear screen and set cursor to position 0,0
    mouse_on         = "\033[?1002h\033[?1015h\033[?1006h" #* Enable reporting of mouse position on click and release
    mouse_off        = "\033[?1002l"                       #* Disable mouse reporting
    mouse_direct_on  = "\033[?1003h"                       #* Enable reporting of mouse position at any movement
    mouse_direct_off = "\033[?1003l"                       #* Disable direct mouse reporting

    _sigWinChCb = None

    @staticmethod
    def echo(on: bool):
        """Toggle input echo"""
        (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr(sys.stdin.fileno())
        if on:
            lflag |= termios.ECHO # type: ignore
        else:
            lflag &= ~termios.ECHO # type: ignore
        new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, new_attr)

    @staticmethod
    def push(*args):
        try:
            print(*args, sep="", end="", flush=True)
        except BlockingIOError:
            pass
            print(*args, sep="", end="", flush=True)

    @staticmethod
    def title(text: str = "") -> str:
        out: str = f'{os.environ.get("TERMINAL_TITLE", "")}'
        if out and text: out += " "
        if text: out += f'{text}'
        return f'\033]0;{out}\a'

    @staticmethod
    def _sigWinCh(signum, frame):
        Term.width, Term.height = os.get_terminal_size()
        if Term._sigWinChCb is not None:
            Term._sigWinChCb(Term.width, Term.height)

    @staticmethod
    def registerResizeCb(callback):
        Term._sigWinChCb = callback
        signal.signal(signal.SIGWINCH, Term._sigWinCh)

