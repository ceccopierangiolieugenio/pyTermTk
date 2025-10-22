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


sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
from TermTk import TTkColor,TTkString

text = 'Link1abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ Test ░▒▓█▁▂▃▄▅▆▇█ Color\nLink1abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ Test ░▒▓█▁▂▃▄▅▆▇█ Color'
print(TTkColor.RST, end='')
print(TTkColor.RST, end='') ; print(TTkString(text, TTkColor.YELLOW).toAnsi())
print(TTkColor.RST, end='') ; print(TTkString(text, TTkColor.BG_MAGENTA).toAnsi())
print(TTkColor.RST, end='') ; print(TTkString(text, TTkColor.BG_YELLOW + TTkColor.RED).toAnsi())
print(TTkColor.RST, end='') ; print(TTkString(text, TTkColor.GREEN + TTkColor.STRIKETROUGH).toAnsi())
print(TTkColor.RST, end='') ; print(TTkString(text, TTkColor.ITALIC + TTkColor.BLUE).toAnsi())
print(TTkColor.RST, end='') ; print(TTkString(text, TTkColor.ITALIC + TTkColor.RED + TTkColor.UNDERLINE).toAnsi())
print(TTkColor.RST, end='') ; print(TTkString(text, TTkColor.ITALIC + TTkColor.BG_RED + TTkColor.UNDERLINE + TTkColor.YELLOW).toAnsi())
print(TTkColor.RST, end='') ; print(TTkString(text, TTkColor.ITALIC + TTkColor.BG_RED + TTkColor.UNDERLINE + TTkColor.YELLOW + TTkColor.BOLD).toAnsi())
print(TTkColor.RST, end='') ; print(TTkString(text, TTkColor.fg('#FF8800', link="https://github.com/ceccopierangiolieugenio/pyTermTk")).toAnsi())
print(TTkColor.RST, end='') ; print(TTkString(text, TTkColor.ITALIC + TTkColor.fg('#0088FF', link="http://www.google.com")).toAnsi())
print(TTkColor.RST, end='') ; print(TTkString(text, TTkColor.fg('#880088', link="https://ceccopierangiolieugenio.itch.io/dumb-paint-tool") + TTkColor.UNDERLINE + TTkColor.BG_YELLOW).toAnsi())

print(TTkColor.RST - TTkColor.fg('#FFFF00',  link="http://www.google.com"))

print(TTkString("RESET", TTkColor.RST).toAnsi())
