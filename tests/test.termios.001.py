#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, termios

attr = termios.tcgetattr(sys.stdin)

print(f"{termios.VDISCARD=} -> {attr[6][termios.VDISCARD]}")
print(f"{termios.VEOL2=} -> {attr[6][termios.VEOL2]}")
print(f"{termios.VKILL=} -> {attr[6][termios.VKILL]}")
print(f"{termios.VQUIT=} -> {attr[6][termios.VQUIT]}")
print(f"{termios.VSTOP=} -> {attr[6][termios.VSTOP]}")
print(f"{termios.VSWTCH=} -> {attr[6][termios.VSWTCH]}")
print(f"{termios.VTDLY=} -> XXX")
print(f"{termios.VEOF=} -> {attr[6][termios.VEOF]}")
print(f"{termios.VERASE=} -> {attr[6][termios.VERASE]}")
print(f"{termios.VLNEXT=} -> {attr[6][termios.VLNEXT]}")
print(f"{termios.VREPRINT=} -> {attr[6][termios.VREPRINT]}")
print(f"{termios.VSUSP=} -> {attr[6][termios.VSUSP]}")
print(f"{termios.VT0=} -> {attr[6][termios.VT0]}")
print(f"{termios.VTIME=} -> {attr[6][termios.VTIME]}")
print(f"{termios.VEOL=} -> {attr[6][termios.VEOL]}")
print(f"{termios.VINTR=} -> {attr[6][termios.VINTR]}")
print(f"{termios.VMIN=} -> {attr[6][termios.VMIN]}")
print(f"{termios.VSTART=} -> {attr[6][termios.VSTART]}")
print(f"{termios.VSWTC=} -> {attr[6][termios.VSWTC]}")
print(f"{termios.VT1=} -> XXX")
print(f"{termios.VWERASE=} -> {attr[6][termios.VWERASE]}")
