#!/usr/bin/env python3

# Copyright 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
# Copyright 2020 Aristocratos (https://github.com/aristocratos/bpytop)
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os, sys, io, threading, signal, re, subprocess, logging, logging.handlers, argparse
import queue
from select import select
from time import time, sleep, strftime, localtime
from typing import List, Set, Dict, Tuple, Optional, Union, Any, Callable, ContextManager, Iterable, Type, NamedTuple

try: import fcntl, termios, tty, pwd
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)

from . import Term
import TermTk as ttk


# Ansi Escape Codes:
# https://conemu.github.io/en/AnsiEscapeCodes.html

class Color:
    '''Holds representations for a 24-bit color value
    __init__(color, depth="fg", default=False)
    -- color accepts 6 digit hexadecimal: string "#RRGGBB", 2 digit hexadecimal: string "#FF" or decimal RGB "255 255 255" as a string.
    -- depth accepts "fg" or "bg"
    __call__(*args) joins str arguments to a string and apply color
    __str__ returns escape sequence to set color
    __iter__ returns iteration over red, green and blue in integer values of 0-255.
    * Values:  .hexa: str  |  .dec: Tuple[int, int, int]  |  .red: int  |  .green: int  |  .blue: int  |  .depth: str  |  .escape: str
    '''
    hexa: str; dec: Tuple[int, int, int]; red: int; green: int; blue: int; depth: str; escape: str; default: bool

    def __init__(self, color: str, depth: str = "fg", default: bool = False):
        self.depth = depth
        self.default = default
        try:
            if not color:
                self.dec = (-1, -1, -1)
                self.hexa = ""
                self.red = self.green = self.blue = -1
                self.escape = "\033[49m" if depth == "bg" and default else ""
                return

            elif color.startswith("#"):
                self.hexa = color
                if len(self.hexa) == 3:
                    self.hexa += self.hexa[1:3] + self.hexa[1:3]
                    c = int(self.hexa[1:3], base=16)
                    self.dec = (c, c, c)
                elif len(self.hexa) == 7:
                    self.dec = (int(self.hexa[1:3], base=16), int(self.hexa[3:5], base=16), int(self.hexa[5:7], base=16))
                else:
                    raise ValueError(f'Incorrectly formatted hexadecimal rgb string: {self.hexa}')

            else:
                c_t = tuple(map(int, color.split(" ")))
                if len(c_t) == 3:
                    self.dec = c_t #type: ignore
                else:
                    raise ValueError(f'RGB dec should be "0-255 0-255 0-255"')

            ct = self.dec[0] + self.dec[1] + self.dec[2]
            if ct > 255*3 or ct < 0:
                raise ValueError(f'RGB values out of range: {color}')
        except Exception as e:
            ttk.TTkLog.error(str(e))
            self.escape = ""
            return

        if self.dec and not self.hexa: self.hexa = f'{hex(self.dec[0]).lstrip("0x").zfill(2)}{hex(self.dec[1]).lstrip("0x").zfill(2)}{hex(self.dec[2]).lstrip("0x").zfill(2)}'

        if self.dec and self.hexa:
            self.red, self.green, self.blue = self.dec
            self.escape = f'\033[{38 if self.depth == "fg" else 48};2;{";".join(str(c) for c in self.dec)}m'

        if ttk.TTkCfg.color_depth is not ttk.TTkCfg.DEP_24:
            self.escape = f'{self.truecolor_to_256(rgb=self.dec, depth=self.depth)}'

    def __str__(self) -> str:
        return self.escape

    def __repr__(self) -> str:
        return repr(self.escape)

    def __iter__(self) -> Iterable:
        for c in self.dec: yield c

    def __call__(self, *args: str) -> str:
        if len(args) < 1: return ""
        return f'{self.escape}{"".join(args)}{getattr(Term, self.depth)}'

    @staticmethod
    def truecolor_to_256(rgb: Tuple[int, int, int], depth: str="fg") -> str:
        out: str = ""
        pre: str = f'\033[{"38" if depth == "fg" else "48"};5;'

        greyscale: Tuple[int, int, int] = ( rgb[0] // 11, rgb[1] // 11, rgb[2] // 11 )
        if greyscale[0] == greyscale[1] == greyscale[2]:
            out = f'{pre}{232 + greyscale[0]}m'
        else:
            out = f'{pre}{round(rgb[0] / 51) * 36 + round(rgb[1] / 51) * 6 + round(rgb[2] / 51) + 16}m'

        return out

    @staticmethod
    def escape_color(hexa: str = "", r: int = 0, g: int = 0, b: int = 0, depth: str = "fg") -> str:
        """Returns escape sequence to set color
        * accepts either 6 digit hexadecimal hexa="#RRGGBB", 2 digit hexadecimal: hexa="#FF"
        * or decimal RGB: r=0-255, g=0-255, b=0-255
        * depth="fg" or "bg"
        """
        dint: int = 38 if depth == "fg" else 48
        color: str = ""
        if hexa:
            try:
                if len(hexa) == 3:
                    c = int(hexa[1:], base=16)
                    if ttk.TTkCfg.color_depth is ttk.TTkCfg.DEP_24:
                        color = f'\033[{dint};2;{c};{c};{c}m'
                    else:
                        color = f'{Color.truecolor_to_256(rgb=(c, c, c), depth=depth)}'
                elif len(hexa) == 7:
                    if ttk.TTkCfg.color_depth is ttk.TTkCfg.DEP_24:
                        color = f'\033[{dint};2;{int(hexa[1:3], base=16)};{int(hexa[3:5], base=16)};{int(hexa[5:7], base=16)}m'
                    else:
                        color = f'{Color.truecolor_to_256(rgb=(int(hexa[1:3], base=16), int(hexa[3:5], base=16), int(hexa[5:7], base=16)), depth=depth)}'
            except ValueError as e:
                ttk.TTkLog.error(f'{e}')

        else:
            if ttk.TTkCfg.color_depth is ttk.TTkCfg.DEP_24:
                color = f'\033[{dint};2;{r};{g};{b}m'
            else:
                color = f'{Color.truecolor_to_256(rgb=(r, g, b), depth=depth)}'
        return color

    @classmethod
    def fg(cls, *args) -> str:
        if len(args) > 2: return cls.escape_color(r=args[0], g=args[1], b=args[2], depth="fg")
        else: return cls.escape_color(hexa=args[0], depth="fg")

    @classmethod
    def bg(cls, *args) -> str:
        if len(args) > 2: return cls.escape_color(r=args[0], g=args[1], b=args[2], depth="bg")
        else: return cls.escape_color(hexa=args[0], depth="bg")

#class Colors:
#    '''Standard colors for menus and dialogs'''
#    default = Color("#cc")
#    white = Color("#ff")
#    red = Color("#bf3636")
#    green = Color("#68bf36")
#    blue = Color("#0fd7ff")
#    yellow = Color("#db8b00")
#    black_bg = Color("#00", depth="bg")
#    null = Color("")