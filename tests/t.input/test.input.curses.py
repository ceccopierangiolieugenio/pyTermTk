#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os

import curses

print("Retrieve Keyboard, Mouse press/drag/wheel Events")
print("Press q or <ESC> to exit")

def reset():
    # Reset
    sys.stdout.write("\033[?1000l")
    sys.stdout.write("\033[?1002l")
    sys.stdout.write("\033[?1015l")
    sys.stdout.write("\033[?1006l")
    sys.stdout.write("\033[?1049l") # Switch to normal screen
    sys.stdout.write("\033[?2004l") # Paste Bracketed mode
    sys.stdout.flush()

stdscr = curses.initscr()

curses.curs_set(0)
stdscr.keypad(1)
curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
curses.mouseinterval(0)
print('\033[?1003h')

# reset()

while True:
    c = stdscr.getch()
    print(f"{c=}\r")
    if c == ord('q'):
        break  # Exit the while loop
    elif c == curses.KEY_HOME:
        print("HOME\r")
    elif c == curses.KEY_MOUSE:
        m = curses.getmouse()
        y, x = stdscr.getyx()
        print(f"Mouse {m=} {(x,y)=}\r")
    elif c == curses.KEY_RESIZE:
        print(f"Resize\r")

print('\033[?1003l')
curses.endwin()
curses.flushinp()