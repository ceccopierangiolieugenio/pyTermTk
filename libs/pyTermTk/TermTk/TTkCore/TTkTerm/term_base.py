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

__all__ = ['TTkTermBase']

import os

class TTkTermBase():
    '''TTkTermBase'''
    CLEAR         = "\033[2J\033[0;0f" # Clear screen and set cursor to position 0,0
    ALT_SCREEN    = "\033[?1049h"                       #* Switch to alternate screen
    NORMAL_SCREEN = "\033[?1049l"                       #* Switch to normal screen

    SET_BRACKETED_PM   = "\033[?2004h" # Ps = 2 0 0 4  ⇒  Set bracketed paste mode, xterm.
    RESET_BRACKETED_PM = "\033[?2004l" # Ps = 2 0 0 4  ⇒  Reset bracketed paste mode, xterm.

    class Mouse(str):
        ON         = "\033[?1002h\033[?1006h" # Enable reporting of mouse position on click and release
        OFF        = "\033[?1002l\033[?1006l" # Disable mouse reporting
        DIRECT_ON  = "\033[?1003h"            # Enable reporting of mouse position at any movement
        DIRECT_OFF = "\033[?1003l"            # Disable direct mouse reporting

    class Cursor(str):
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
            TTkTermBase.push(cursorType)
            TTkTermBase.push(TTkTermBase.Cursor.SHOW)
        @staticmethod
        def hide():
            TTkTermBase.push(TTkTermBase.Cursor.HIDE)

    class Sigmask():
        CTRL_C = 0x0001
        CTRL_S = 0x0002
        CTRL_Z = 0x0004
        CTRL_Q = 0x0008
        CTRL_Y = 0x0010

    title: str = "TermTk"
    width: int = 0
    height: int = 0
    mouse: bool = True
    directMouse: bool = False

    _sigWinChCb = None

    @staticmethod
    def init(title: str = "TermTk", sigmask=0) -> None:
        TTkTermBase.title = title
        TTkTermBase.Cursor.hide()
        TTkTermBase.push(TTkTermBase.escTitle(TTkTermBase.title))
        TTkTermBase.push(TTkTermBase.ALT_SCREEN)
        TTkTermBase.push(TTkTermBase.SET_BRACKETED_PM)
        TTkTermBase.push(TTkTermBase.CLEAR + TTkTermBase.Cursor.HIDE)
        TTkTermBase.setEcho(False)
        TTkTermBase.CRNL(False)
        TTkTermBase.setSigmask(sigmask, False)

    @staticmethod
    def setMouse(mouse:bool=False, directMouse:bool=False) -> None:
        TTkTermBase.mouse = mouse | directMouse
        TTkTermBase.directMouse = directMouse
        if TTkTermBase.mouse:
            TTkTermBase.push(TTkTermBase.Mouse.DIRECT_OFF)
            TTkTermBase.push(TTkTermBase.Mouse.ON)
            if TTkTermBase.directMouse:
                TTkTermBase.push(TTkTermBase.Mouse.DIRECT_ON)
        else:
            TTkTermBase.push(TTkTermBase.Mouse.OFF)
            TTkTermBase.push(TTkTermBase.Mouse.DIRECT_OFF)

    @staticmethod
    def exit() -> None:
        TTkTermBase.push(TTkTermBase.Mouse.OFF + TTkTermBase.Mouse.DIRECT_OFF)
        TTkTermBase.push(TTkTermBase.CLEAR + TTkTermBase.NORMAL_SCREEN + TTkTermBase.RESET_BRACKETED_PM + TTkTermBase.Cursor.SHOW + TTkTermBase.escTitle())
        TTkTermBase.setEcho(True)
        TTkTermBase.CRNL(True)

    @staticmethod
    def stop() -> None:
        TTkTermBase.push(TTkTermBase.Mouse.OFF + TTkTermBase.Mouse.DIRECT_OFF)
        TTkTermBase.push(TTkTermBase.CLEAR + TTkTermBase.NORMAL_SCREEN + TTkTermBase.RESET_BRACKETED_PM + TTkTermBase.Cursor.SHOW + TTkTermBase.escTitle())
        TTkTermBase.setEcho(True)
        TTkTermBase.CRNL(True)

    @staticmethod
    def cont() -> None:
        TTkTermBase.push(TTkTermBase.ALT_SCREEN + TTkTermBase.SET_BRACKETED_PM + TTkTermBase.CLEAR + TTkTermBase.Cursor.HIDE + TTkTermBase.escTitle(TTkTermBase.title))
        TTkTermBase.setMouse(TTkTermBase.mouse, TTkTermBase.directMouse)
        TTkTermBase.setEcho(False)
        TTkTermBase.CRNL(False)

    @staticmethod
    def escTitle(txt = "") -> str:
        tt = os.environ.get("TERMINAL_TITLE", "")
        if tt and txt:
            return f'\033]0;{tt} {txt}\a'
        else:
            return f'\033]0;{tt}{txt}\a'

    # NOTE: Due to "I have no idea how to do it in a better way",
    # those methods are supposed to be overwritten with the
    # compatible one in "term_unix.py" or "term_pyodide.py"
    setSigmask = lambda *args: None
    getSigmask = lambda *args: 0x00
    push       = lambda *args: None
    flush      = lambda *args: None
    setEcho    = lambda *args: None
    CRNL       = lambda *args: None
    getTerminalSize  = lambda *args: (80,24)
    registerResizeCb = lambda *args: None