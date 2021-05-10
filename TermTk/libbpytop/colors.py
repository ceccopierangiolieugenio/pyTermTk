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

from TermTk.libbpytop.term import Term
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.log import TTkLog


# Ansi Escape Codes:
# https://conemu.github.io/en/AnsiEscapeCodes.html

class Color:
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
                    if TTkCfg.color_depth is TTkK.DEP_24:
                        color = f'\033[{dint};2;{c};{c};{c}m'
                    else:
                        color = f'{Color.truecolor_to_256(rgb=(c, c, c), depth=depth)}'
                elif len(hexa) == 7:
                    if TTkCfg.color_depth is TTkK.DEP_24:
                        color = f'\033[{dint};2;{int(hexa[1:3], base=16)};{int(hexa[3:5], base=16)};{int(hexa[5:7], base=16)}m'
                    else:
                        color = f'{Color.truecolor_to_256(rgb=(int(hexa[1:3], base=16), int(hexa[3:5], base=16), int(hexa[5:7], base=16)), depth=depth)}'
            except ValueError as e:
                TTkLog.error(f'{e}')

        else:
            if TTkCfg.color_depth is TTkK.DEP_24:
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