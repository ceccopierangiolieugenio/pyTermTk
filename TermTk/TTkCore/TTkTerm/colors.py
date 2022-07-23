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

# Ansi Escape Codes:
# https://conemu.github.io/en/AnsiEscapeCodes.html

import re

from .colors_ansi_map import ansiMap256, ansiMap16

class TTkTermColor():
    BOLD         = 0x01
    ITALIC       = 0x02
    UNDERLINE    = 0x04
    STRIKETROUGH = 0x08
    BLINKING     = 0x10

    @staticmethod
    def rgb2ansi(fg: tuple=None, bg:tuple=None, mod:int=0, clean:bool=False):
        ret = []

        if clean:
            ret.append(0)

        if fg:
            ret.append(f'38;2;{fg[0]};{fg[1]};{fg[2]}')
        if bg:
            ret.append(f'48;2;{bg[0]};{bg[1]};{bg[2]}')

        if mod & TTkTermColor.BOLD:
            ret.append('1')
        if mod & TTkTermColor.ITALIC:
            ret.append('3')
        if mod & TTkTermColor.UNDERLINE:
            ret.append('4')
        if mod & TTkTermColor.STRIKETROUGH:
            ret.append('9')
        if mod & TTkTermColor.BLINKING:
            ret.append('5')

        if ret:
            return f'\033[{";".join(str(x) for x in ret)}m'
        else:
            return '\033[0m'

    def _256toRgb(val):
        pass

    ansiParser = re.compile(r'^\033\[([\d;]*)m$')
    @staticmethod
    def ansi2rgb(ansi:str):
        fg = None
        bg = None
        mod = 0
        clean = False
        if m := TTkTermColor.ansiParser.match(ansi):
            values = m.group(1).split(';')

            if not all(values): # Return None if not all the values are set
                return (None, None, 0, True)

            while values:
                s = int(values.pop(0))
                if 30 <= s <= 37: # Ansi 16 colors - fg
                    fg = ansiMap16.get(s-30)
                elif 40 <= s <= 47: # Ansi 16 colors - bg
                    bg = ansiMap16.get(s-40)
                elif s == 38:
                    t =  int(values.pop(0))
                    if t == 5:# 256 fg
                        fg = ansiMap256.get(int(values.pop(0)))
                    if t == 2:# 24 bit fg
                        fg = (int(values.pop(0)),int(values.pop(0)),int(values.pop(0)))
                elif s == 48:
                    t =  int(values.pop(0))
                    if t == 5:# 256 bg
                        bg = ansiMap256.get(int(values.pop(0)))
                    if t == 2:# 24 bit bg
                        bg = (int(values.pop(0)),int(values.pop(0)),int(values.pop(0)))
                elif s==0: # Reset Color/Format
                    fg = None
                    bg = None
                    mod = 0
                    clean = True
                elif s==1: mod += TTkTermColor.BOLD
                elif s==3: mod += TTkTermColor.ITALIC
                elif s==4: mod += TTkTermColor.UNDERLINE
                elif s==9: mod += TTkTermColor.STRIKETROUGH
                elif s==5: mod += TTkTermColor.BLINKING
        return fg,bg,mod,clean


    @staticmethod
    def esc_color(val: str, fg: bool):
        # Return the escape sequence for bg or fg
        # of the color represented in hex: "#AABBCC"
        if len(val) != 7:
            raise ValueError()
        r = int(val[1:3],base=16)
        g = int(val[3:5],base=16)
        b = int(val[5:7],base=16)
        return f'\033[{38 if fg else 48};2;{r};{g};{b}m'

    @staticmethod
    def fg(val) -> str:
        return TTkTermColor.esc_color(val, True)

    @staticmethod
    def bg(val) -> str:
        return TTkTermColor.esc_color(val, False)
