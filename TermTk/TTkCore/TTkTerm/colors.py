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

class TTkTermColor():
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
        # 256 colors
        #     if r//11 == g//11 == b//11:
        #         # Shade of grey
        #         return f"\033[{38 if fg else 48};5;{232+r//11}m"
        #     else:
        #         # truecolor
        #         return f"\033[{38 if fg else 48};5;{round(r/51)*36 + round(g/51)*6 + round(b/51) + 16}m"

    @staticmethod
    def fg(val) -> str:
        return TTkTermColor.esc_color(val, True)

    @staticmethod
    def bg(val) -> str:
        return TTkTermColor.esc_color(val, False)