# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkSignalDriver','TTkInputDriver']

import sys
import os
import re
import signal
from select import select

import ctypes

try: import fcntl, termios, tty
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)

from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot


'''
    #define GPM_MAGIC 0x47706D4C /* "GpmL" */
    typedef struct Gpm_Connect {
      unsigned short eventMask, defaultMask;
      unsigned short minMod, maxMod;
      int pid;
      int vc;
    }              Gpm_Connect;
'''
class _Gpm_Connect(ctypes.Structure):
    _fields_ = [
        ("eventMask",   ctypes.c_ushort),
        ("defaultMask", ctypes.c_ushort),
        ("minMod", ctypes.c_ushort),
        ("maxMod", ctypes.c_ushort),
        ("pid", ctypes.c_int),
        ("vc",  ctypes.c_int)]

'''
    enum Gpm_Etype {
        GPM_MOVE=1,
        GPM_DRAG=2,   /* exactly one of the bare ones is active at a time */
        GPM_DOWN=4,
        GPM_UP=  8,

    #define GPM_BARE_EVENTS(type) ((type)&(0x0f|GPM_ENTER|GPM_LEAVE))

        GPM_SINGLE=16,            /* at most one in three is set */
        GPM_DOUBLE=32,
        GPM_TRIPLE=64,            /* WARNING: I depend on the values */

        GPM_MFLAG=128,            /* motion during click? */
        GPM_HARD=256,             /* if set in the defaultMask, force an already
                                     used event to pass over to another handler */

        GPM_ENTER=512,            /* enter event, user in Roi's */
        GPM_LEAVE=1024            /* leave event, used in Roi's */
    };

    enum Gpm_Margin {GPM_TOP=1, GPM_BOT=2, GPM_LFT=4, GPM_RGT=8};

    typedef struct Gpm_Event {
        unsigned char buttons, modifiers;  /* try to be a multiple of 4 */
        unsigned short vc;
        short dx, dy, x, y; /* displacement x,y for this event, and absolute x,y */
        enum Gpm_Etype type;
        /* clicks e.g. double click are determined by time-based processing */
        int clicks;
        enum Gpm_Margin margin;
        /* wdx/y: displacement of wheels in this event. Absolute values are not
        * required, because wheel movement is typically used for scrolling
        * or selecting fields, not for cursor positioning. The application
        * can determine when the end of file or form is reached, and not
        * go any further.
        * A single mouse will use wdy, "vertical scroll" wheel. */
        short wdx, wdy;
    }              Gpm_Event;
'''
class _Gpm_Event(ctypes.Structure):
    _fields_ = [
        ("buttons",   ctypes.c_ubyte),
        ("modifiers", ctypes.c_ubyte),
        ("vc", ctypes.c_short),
        ("dx", ctypes.c_short),
        ("dy", ctypes.c_short),
        ("x",  ctypes.c_short),
        ("y",  ctypes.c_short),
        ("type",   ctypes.c_int),
        ("clicks", ctypes.c_int),
        ("margin", ctypes.c_int),
        ("wdx", ctypes.c_short),
        ("wdy", ctypes.c_short)]


_GPM_HANDLER_FUNC = ctypes.CFUNCTYPE(
                        ctypes.c_int,
                        ctypes.POINTER(_Gpm_Event),
                        ctypes.POINTER(ctypes.c_void_p))

class TTkInputDriver():
    __slots__ = ('_readPipe', '_attr',
                '_libgpm', '_libc', '_cstdin')

    def __init__(self):
        self._libgpm = ctypes.CDLL('libgpm.so.2')
        self._libc = ctypes.cdll.LoadLibrary('libc.so.6')
        self._cstdin = ctypes.c_void_p.in_dll(self._libc, 'stdin')

        self._readPipe = os.pipe()
        self._attr = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)

    def close(self):
        termios.tcsetattr(sys.stdin, termios.TCSANOW, self._attr)
        os.write(self._readPipe[1], b'quit')

    def cont(self):
        tty.setcbreak(sys.stdin)

    def _gpm_handler(self, event:_Gpm_Event) -> str:
        code = 0x00
        state = 'M'

        x = event.x
        y = event.y

        # wdx = ec.wdx
        wdy = event.wdy # mouse wheel

        # Types:
        #   from: <https://github.com/telmich/gpm.git>/src/headers/gpm.h
        #   https://github.com/telmich/gpm/blob/master/src/headers/gpm.h
        #     MOVE = 0x0001
        #     DRAG = 0x0002
        #     DOWN = 0x0004
        #     UP   = 0x0008
        #
        #     SINGLE = 0x0010
        #     DOUBLE = 0x0020
        #     TRIPLE = 0x0040
        #     MFLAG  = 0x0080
        #     HARD   = 0x0100
        #     ENTER  = 0x0200
        #     LEAVE  = 0x0400
        #        # exactly one of the bare ones is active at a time
        #     BARE_EVENTS(type)     ((type)&(0x0f|ENTER|LEAVE))
        etype = event.type
        if etype & 0x0008: # UP
            state = 'm'

        # Buttons:
        #   from: <https://github.com/telmich/gpm.git>/src/headers/gpm.h
        #   https://github.com/telmich/gpm/blob/master/src/headers/gpm.h
        #     DOWN      0x20
        #     UP        0x10
        #     FOURTH    0x08
        #     LEFT      0x04
        #     MIDDLE    0x02
        #     RIGHT     0x01
        #     NONE      0x00
        buttons   = event.buttons
        if   wdy == 1: # Wheel UP(1)
            code |= 0x40
        elif wdy == -1: # Wheel DOWN(-1)
            code |= 0x41
        elif etype & (0x0004|0x0008): # DOWN/UP
            if   buttons & 0x04: # LEFT
                code |= 0x00
            elif buttons & 0x01: # RIGHT
                code |= 0x02
            elif buttons & 0x02: # MIDDLE
                code |= 0x01
        elif etype & (0x0002): # MOVE
            if   buttons & 0x04: # LEFT
                code |= 0x20
            elif buttons & 0x01: # RIGHT
                code |= 0x22
            elif buttons & 0x02: # MIDDLE
                code |= 0x21
        elif etype & (0x0001): # MOVE
                code |= 0x23

        # Modifiers:
        #   From: /usr/include/linux/keyboard.h
        #     SHIFT        0x01 << 0x00 = 0x0001
        #     CTRL         0x01 << 0x02 = 0x0004
        #     ALT          0x01 << 0x03 = 0x0008
        #     ALTGR        0x01 << 0x01 = 0x0002
        #     SHIFTL       0x01 << 0x04 = 0x0010
        #     KANASHIFT    0x01 << 0x04 = 0x0010
        #     SHIFTR       0x01 << 0x05 = 0x0020
        #     CTRLL        0x01 << 0x06 = 0x0040
        #     CTRLR        0x01 << 0x07 = 0x0080
        #     CAPSSHIFT    0x01 << 0x08 = 0x0100
        modifiers = event.modifiers
        if modifiers &  0x0001: # SHIFT
            code |= 0x27
        if modifiers &  0x0004: # CTRL
            code |= 0x10
        if modifiers & (0x0008|0x0002): # ALT/ALTGR
            code |= 0x08

        return f"\033[<{code};{x};{y}{state}"

    def read(self):
        rm = re.compile('(\033?[^\033]+)')

        _conn = _Gpm_Connect()
        _conn.eventMask   = ~0 # Want to know about all the events
        _conn.defaultMask =  0 # don't handle anything by default
        _conn.minMod      =  0 # want everything
        _conn.maxMod      = ~0 # all modifiers included

        if (_gpm_fd := self._libgpm.Gpm_Open(ctypes.pointer(_conn), 0)) == -1:
           raise Exception("Cannot connect to the mouse server")

        if _gpm_fd < 0:
            self._libgpm.Gpm_Close()
            raise Exception("Xterm GPM driver not supported")

        _ev = _Gpm_Event()

        with os.fdopen(_gpm_fd, "r") as gpm_file_obj:
            while self._readPipe[0] not in (_rlist := select( [sys.stdin, gpm_file_obj, self._readPipe[0]], [], [] )[0]):
                if gpm_file_obj in _rlist:
                    self._libgpm.Gpm_GetEvent(ctypes.pointer(_ev))
                    yield self._gpm_handler(_ev)

                if sys.stdin in _rlist:
                    # Read all the full input
                    _fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
                    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, _fl | os.O_NONBLOCK) # Set the input as NONBLOCK to read the full sequence
                    stdinRead = sys.stdin.read()
                    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, _fl)

                    # Split all the ansi sequences
                    # or yield any separate input char
                    if stdinRead == '\033':
                        yield '\033'
                        continue
                    for sr in rm.findall(stdinRead):
                        if '\033' == sr[0]:
                            yield sr
                        else:
                            for ch in sr:
                                yield ch

        self._libgpm.Gpm_Close()

class TTkSignalDriver():
    sigStop = pyTTkSignal()
    sigCont = pyTTkSignal()
    sigInt  = pyTTkSignal()

    @staticmethod
    def init():
        # Register events
        signal.signal(signal.SIGTSTP, TTkSignalDriver._SIGSTOP) # Ctrl-Z
        signal.signal(signal.SIGCONT, TTkSignalDriver._SIGCONT) # Resume
        signal.signal(signal.SIGINT,  TTkSignalDriver._SIGINT)  # Ctrl-C

    def exit():
        signal.signal(signal.SIGINT,  signal.SIG_DFL)

    def _SIGSTOP(signum, frame): TTkSignalDriver.sigStop.emit()
    def _SIGCONT(signum, frame): TTkSignalDriver.sigCont.emit()
    def _SIGINT( signum, frame): TTkSignalDriver.sigInt.emit()


def _main():
    inputDriver = TTkInputDriver()

    for stdinRead in inputDriver.read():
        out = stdinRead.replace('\033','<ESC>')
        print(f"Input: {out}")
        if stdinRead == 'q':
            print('Break')
            break

    inputDriver.close()

if __name__ == "__main__":
    _main()