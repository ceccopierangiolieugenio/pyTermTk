#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os, signal

try: import termios
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)

class TTkTerm():
    CLEAR         = "\033[2J\033[0;0f" # Clear screen and set cursor to position 0,0
    ALT_SCREEN    = "\033[?1049h"                       #* Switch to alternate screen
    NORMAL_SCREEN = "\033[?1049l"                       #* Switch to normal screen

    class Mouse():
        ON         = "\033[?1002h\033[?1015h\033[?1006h" # Enable reporting of mouse position on click and release
        OFF        = "\033[?1002l"                       # Disable mouse reporting
        DIRECT_ON  = "\033[?1003h"                       # Enable reporting of mouse position at any movement
        DIRECT_OFF = "\033[?1003l"                       # Disable direct mouse reporting

    class Cursor():
        # from:
        # https://superuser.com/questions/607478/how-do-you-change-the-xterm-cursor-to-an-i-beam-or-vertical-bar
        # echo -e -n "\x1b[\x30 q" # changes to blinking block
        # echo -e -n "\x1b[\x31 q" # changes to blinking block also
        # echo -e -n "\x1b[\x32 q" # changes to steady block
        # echo -e -n "\x1b[\x33 q" # changes to blinking underline
        # echo -e -n "\x1b[\x34 q" # changes to steady underline
        # echo -e -n "\x1b[\x35 q" # changes to blinking bar
        # echo -e -n "\x1b[\x36 q" # changes to steady bar
        BLINKING_BLOCK      = "\033[\x30 q"
        BLINKING_BLOCK_ALSO = "\033[\x31 q"
        STEADY_BLOCK        = "\033[\x32 q"
        BLINKING_UNDERLINE  = "\033[\x33 q"
        STEADY_UNDERLINE    = "\033[\x34 q"
        BLINKING_BAR        = "\033[\x35 q"
        STEADY_BAR          = "\033[\x36 q"

        HIDE = "\033[?25l"
        SHOW = "\033[?25h"

        @staticmethod
        def moveTo(y:int,x:int)->str: return f'\033[{y};{x}f'
        @staticmethod
        def moveRight(n:int)->str: return f'\033[{n}C'
        @staticmethod
        def moveLeft(n:int)->str:  return f'\033[{n}D'
        @staticmethod
        def modeUp(n:int)->str:    return f'\033[{n}A'
        @staticmethod
        def moveDown(n:int)->str:  return f'\033[{n}B'

        @staticmethod
        def show(cursorType):
            TTkTerm.push(cursorType)
            TTkTerm.push(TTkTerm.Cursor.SHOW)
        @staticmethod
        def hide():
            TTkTerm.push(TTkTerm.Cursor.HIDE)

    class Sigmask():
        CTRL_C = 0x0001
        CTRL_S = 0x0002
        CTRL_Z = 0x0004
        CTRL_Q = 0x0008

    title: str = "TermTk"
    mouse: bool = True
    width: int = 0
    height: int = 0

    _sigWinChCb = None

    # Save treminal attributes during the initialization in order to
    # restore later the original states
    _termAttr = termios.tcgetattr(sys.stdin)

    _termAttrBk = []
    @staticmethod
    def saveTermAttr():
        TTkTerm._termAttrBk.append(termios.tcgetattr(sys.stdin))

    @staticmethod
    def restoreTermAttr():
        if TTkTerm._termAttrBk:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, TTkTerm._termAttrBk.pop())
        else:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, TTkTerm._termAttr)

    @staticmethod
    def setSigmask(mask, value=True):
        attr = termios.tcgetattr(sys.stdin)
        if mask & TTkTerm.Sigmask.CTRL_C:
            attr[6][termios.VINTR]=  b'\x03' if value else 0
        if mask & TTkTerm.Sigmask.CTRL_S:
            attr[6][termios.VSTOP]=  b'\x13' if value else 0
        if mask & TTkTerm.Sigmask.CTRL_Z:
            attr[6][termios.VSUSP]=  b'\x1a' if value else 0
        if mask & TTkTerm.Sigmask.CTRL_Q:
            attr[6][termios.VSTART]= b'\x11' if value else 0
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, attr)

    @staticmethod
    def getSigmask():
        mask = 0x00
        attr = termios.tcgetattr(sys.stdin)
        mask |= TTkTerm.Sigmask.CTRL_C if attr[6][termios.VINTR]  else 0
        mask |= TTkTerm.Sigmask.CTRL_S if attr[6][termios.VSTOP]  else 0
        mask |= TTkTerm.Sigmask.CTRL_Z if attr[6][termios.VSUSP]  else 0
        mask |= TTkTerm.Sigmask.CTRL_Q if attr[6][termios.VSTART] else 0
        return mask

    @staticmethod
    def init(mouse: bool = True, title: str = "TermTk", sigmask=0):
        TTkTerm.title = title
        TTkTerm.mouse = mouse
        TTkTerm.push(TTkTerm.ALT_SCREEN + TTkTerm.CLEAR + TTkTerm.Cursor.HIDE + TTkTerm.escTitle(TTkTerm.title))
        if TTkTerm.mouse:
            TTkTerm.push(TTkTerm.Mouse.ON)
        TTkTerm.setEcho(False)
        TTkTerm.setSigmask(sigmask, False)

    @staticmethod
    def exit():
        TTkTerm.push(TTkTerm.Mouse.OFF + TTkTerm.Mouse.DIRECT_OFF)
        TTkTerm.push(TTkTerm.CLEAR + TTkTerm.NORMAL_SCREEN + TTkTerm.Cursor.SHOW + TTkTerm.escTitle())
        TTkTerm.setEcho(True)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, TTkTerm._termAttr)

    @staticmethod
    def stop():
        TTkTerm.push(TTkTerm.Mouse.OFF + TTkTerm.Mouse.DIRECT_OFF)
        TTkTerm.push(TTkTerm.CLEAR + TTkTerm.NORMAL_SCREEN + TTkTerm.Cursor.SHOW + TTkTerm.escTitle())
        TTkTerm.setEcho(True)

    @staticmethod
    def cont():
        TTkTerm.push(TTkTerm.ALT_SCREEN + TTkTerm.CLEAR + TTkTerm.Cursor.HIDE + TTkTerm.escTitle(TTkTerm.title))
        if TTkTerm.mouse:
            TTkTerm.push(TTkTerm.Mouse.ON)
        TTkTerm.setEcho(False)

    @staticmethod
    def escTitle(txt = "") -> str:
        tt = os.environ.get("TERMINAL_TITLE", "")
        if tt and txt:
            return f'\033]0;{tt} {txt}\a'
        else:
            return f'\033]0;{tt}{txt}\a'

    @staticmethod
    def push(*args):
        sys.stdout.write(str(*args))
        sys.stdout.flush()

    @staticmethod
    def flush():
        sys.stdout.flush()

    @staticmethod
    def setEcho(val: bool):
        # Set/Unset Terminal Input Echo
        (i,o,c,l,isp,osp,cc) = termios.tcgetattr(sys.stdin.fileno())
        if val: l |= termios.ECHO
        else:   l &= ~termios.ECHO
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, [i,o,c,l,isp,osp,cc])

    @staticmethod
    def getTerminalSize():
        return os.get_terminal_size()

    @staticmethod
    def _sigWinCh(signum, frame):
        TTkTerm.width, TTkTerm.height = TTkTerm.getTerminalSize()
        if TTkTerm._sigWinChCb is not None:
            TTkTerm._sigWinChCb(TTkTerm.width, TTkTerm.height)

    @staticmethod
    def registerResizeCb(callback):
        TTkTerm._sigWinChCb = callback
        # Dummy call to retrieve the terminal size
        TTkTerm._sigWinCh(signal.SIGWINCH, None)
        signal.signal(signal.SIGWINCH, TTkTerm._sigWinCh)