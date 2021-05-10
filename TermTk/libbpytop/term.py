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

try: import termios
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)

class Mv:
    """Class with collection of cursor movement functions: .t[o](line, column) | .r[ight](columns) | .l[eft](columns) | .u[p](lines) | .d[own](lines) | .save() | .restore()"""
    @staticmethod
    def to(line: int, col: int) -> str:
        return f'\033[{line};{col}f' #* Move cursor to line, column
    @staticmethod
    def right(x: int) -> str:        #* Move cursor right x columns
        return f'\033[{x}C'
    @staticmethod
    def left(x: int) -> str:         #* Move cursor left x columns
        return f'\033[{x}D'
    @staticmethod
    def up(x: int) -> str:           #* Move cursor up x lines
        return f'\033[{x}A'
    @staticmethod
    def down(x: int) -> str:         #* Move cursor down x lines
        return f'\033[{x}B'

    save: str = "\033[s"             #* Save cursor position
    restore: str = "\033[u"          #* Restore saved cursor postion
    t = to
    r = right
    l = left
    u = up
    d = down

class Term:
    """Terminal info and commands"""
    title: str = "TermTk"
    mouse: bool = True
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

    # from:
    # https://superuser.com/questions/607478/how-do-you-change-the-xterm-cursor-to-an-i-beam-or-vertical-bar
    # echo -e -n "\x1b[\x30 q" # changes to blinking block
    # echo -e -n "\x1b[\x31 q" # changes to blinking block also
    # echo -e -n "\x1b[\x32 q" # changes to steady block
    # echo -e -n "\x1b[\x33 q" # changes to blinking underline
    # echo -e -n "\x1b[\x34 q" # changes to steady underline
    # echo -e -n "\x1b[\x35 q" # changes to blinking bar
    # echo -e -n "\x1b[\x36 q" # changes to steady bar

    cursor_blinking_block      = "\033[\x30 q"
    cursor_blinking_block_also = "\033[\x31 q"
    cursor_steady_block        = "\033[\x32 q"
    cursor_blinking_underline  = "\033[\x33 q"
    cursor_steady_underline    = "\033[\x34 q"
    cursor_blinking_bar        = "\033[\x35 q"
    cursor_steady_bar          = "\033[\x36 q"

    _sigWinChCb = None

    @staticmethod
    def showCursor(cursor):
        Term.push(cursor)
        Term.push(Term.show_cursor)
    @staticmethod
    def hideCursor():
        Term.push(Term.hide_cursor)

    @staticmethod
    def init(mouse: bool = True, title: str = "TermTk"):
        Term.title = title
        Term.mouse = mouse
        Term.push(Term.alt_screen, Term.clear, Term.hide_cursor, Term.escTitle(Term.title))
        if Term.mouse:
            Term.push(Term.mouse_on)
        Term.echo(False)

    @staticmethod
    def stop():
        Term.push(Term.mouse_off, Term.mouse_direct_off)
        Term.push(Term.clear, Term.normal_screen, Term.show_cursor, Term.escTitle())
        Term.echo(True)

    @staticmethod
    def cont():
        Term.push(Term.alt_screen, Term.clear, Term.hide_cursor, Term.escTitle(Term.title))
        if Term.mouse:
            Term.push(Term.mouse_on)
        Term.echo(False)

    @staticmethod
    def exit():
        Term.push(Term.mouse_off, Term.mouse_direct_off)
        Term.push(Term.clear, Term.normal_screen, Term.show_cursor, Term.escTitle())
        Term.echo(True)


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
    def escTitle(text: str = "") -> str:
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
        # Dummy call to retrieve the terminal size
        Term._sigWinCh(signal.SIGWINCH, None)
        signal.signal(signal.SIGWINCH, Term._sigWinCh)
