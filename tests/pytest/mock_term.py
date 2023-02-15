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
# SOFTWARE.import sys

# Thanks to: https://stackoverflow.com/questions/43162722/mocking-a-module-import-in-pytest

import sys

class Mock_TTkTerm():
    CLEAR         = None
    ALT_SCREEN    = None
    NORMAL_SCREEN = None

    class Mouse():
        ON         = None
        OFF        = None
        DIRECT_ON  = None
        DIRECT_OFF = None

    class Cursor():
        BLINKING_BLOCK      = None
        BLINKING_BLOCK_ALSO = None
        STEADY_BLOCK        = None
        BLINKING_UNDERLINE  = None
        STEADY_UNDERLINE    = None
        BLINKING_BAR        = None
        STEADY_BAR          = None

        HIDE = None
        SHOW = None

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
        def show(cursorType): pass
        @staticmethod
        def hide(): pass

    class Sigmask():
        CTRL_C = 0x0001
        CTRL_S = 0x0002
        CTRL_Z = 0x0004
        CTRL_Q = 0x0008

    @staticmethod
    def push(*args):
        sys.stdout.write(str(*args))
        sys.stdout.flush()

    @staticmethod
    def registerResizeCb(_): pass
    @staticmethod
    def exit(): pass
    @staticmethod
    def init(title,sigmask,mouse,directMouse): pass
    @staticmethod
    def getTerminalSize():
        return 250,70
