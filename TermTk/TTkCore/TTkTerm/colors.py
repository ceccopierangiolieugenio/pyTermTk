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

__all__ = ['TTkTermColor']

# Ansi Escape Codes:
# https://conemu.github.io/en/AnsiEscapeCodes.html

import re

from .colors_ansi_map import ansiMap256, ansiMap16

class TTkTermColor():
    BOLD         = 0x01  # <ESC>[1m
    FAINT        = 0x02  # <ESC>[2m
    ITALIC       = 0x04  # <ESC>[3m
    UNDERLINE    = 0x08  # <ESC>[4m
    BLINKING     = 0x10  # <ESC>[5m
    REVERSED     = 0x20  # <ESC>[7m
    HIDDEN       = 0x40  # <ESC>[8m
    STRIKETROUGH = 0x80  # <ESC>[9m

    SGR_SET = {        # CSI Pm m  Character Attributes (SGR).
                           # Ps = 0  ⇒  Normal (default), VT100.
        1: BOLD ,          # Ps = 1  ⇒  Bold, VT100.
        2: FAINT ,         # Ps = 2  ⇒  Faint, decreased intensity, ECMA-48 2nd.
        3: ITALIC ,        # Ps = 3  ⇒  Italicized, ECMA-48 2nd.
        4: UNDERLINE ,     # Ps = 4  ⇒  Underlined, VT100.
        5: BLINKING ,      # Ps = 5  ⇒  Blink, VT100. - This appears as Bold in X11R6 xterm.
        7: REVERSED ,      # Ps = 7  ⇒  Inverse, VT100.
        8: HIDDEN ,        # Ps = 8  ⇒  Invisible, i.e., hidden, ECMA-48 2nd, VT300.
        9: STRIKETROUGH }  # Ps = 9  ⇒  Crossed-out characters, ECMA-48 3rd.

    SGR_RST = {       # CSI Pm m  Character Attributes (SGR).
                            # Ps = 2 1  ⇒  Doubly-underlined, ECMA-48 3rd.
        22: ~(BOLD|FAINT),  # Ps = 2 2  ⇒  Normal (neither bold nor faint), ECMA-48 3rd.
        23: ~ITALIC,        # Ps = 2 3  ⇒  Not italicized, ECMA-48 3rd.
        24: ~UNDERLINE,     # Ps = 2 4  ⇒  Not underlined, ECMA-48 3rd.
        25: ~BLINKING,      # Ps = 2 5  ⇒  Steady (not blinking), ECMA-48 3rd.
        27: ~REVERSED,      # Ps = 2 7  ⇒  Positive (not inverse), ECMA-48 3rd.
        28: ~HIDDEN,        # Ps = 2 8  ⇒  Visible, i.e., not hidden, ECMA-48 3rd, VT300.
        29: ~STRIKETROUGH } # Ps = 2 9  ⇒  Not crossed-out, ECMA-48 3rd.

    @staticmethod
    def rgb2ansi(fg: tuple=None, bg:tuple=None, mod:int=0, clean:bool=False):
        ret = []
        ret_append = ret.append

        if clean:
            ret_append('0')

        if fg:
            ret_append(f'38;2;{fg[0]};{fg[1]};{fg[2]}')
        if bg:
            ret_append(f'48;2;{bg[0]};{bg[1]};{bg[2]}')

        if mod:
            if mod & TTkTermColor.BOLD:
                ret_append('1')
            if mod & TTkTermColor.FAINT:
                ret_append('2')
            if mod & TTkTermColor.ITALIC:
                ret_append('3')
            if mod & TTkTermColor.UNDERLINE:
                ret_append('4')
            if mod & TTkTermColor.BLINKING:
                ret_append('5')
            if mod & TTkTermColor.REVERSED:
                ret_append('7')
            if mod & TTkTermColor.HIDDEN:
                ret_append('8')
            if mod & TTkTermColor.STRIKETROUGH:
                ret_append('9')
        if ret:
            return f'\033[{";".join(ret)}m'
        else:
            return '\033[0m'

    @staticmethod
    def rgb2ansi_link(fg: tuple=None, bg:tuple=None, mod:int=0, link:str='', clean:bool=False, cleanLink:bool=False):
        linkAnsi = ""
        if cleanLink:
            linkAnsi = "\033]8;;\033\\"
        if link:
            linkAnsi = f"\033]8;id=1;{link}\033\\"
        return TTkTermColor.rgb2ansi(fg=fg,bg=bg,mod=mod,clean=clean)+linkAnsi

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

                if ( # Ansi 16 colors
                     30  <= s <= 37 or   # fg [ 30 -  37]
                     90  <= s <= 97 ):   # fg [ 90 -  97] Bright
                    fg = ansiMap16.get(s)
                elif ( # Ansi 16 colors
                     40  <= s <= 47 or   # bg [ 40 -  47]
                     100 <= s <= 107 ) : # bg [100 - 107] Bright
                    bg = ansiMap16.get(s)
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
                elif _sgr:=TTkTermColor.SGR_SET.get(s,None):
                    mod |= _sgr
                elif _sgr:=TTkTermColor.SGR_RST.get(s,None):
                    mod &= _sgr
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
