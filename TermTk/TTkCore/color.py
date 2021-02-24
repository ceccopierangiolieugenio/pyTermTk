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

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.helper import *

# Ansi Escape Codes:
# https://conemu.github.io/en/AnsiEscapeCodes.html

# From http://pueblo.sourceforge.net/doc/manual/ansi_color_codes.html
# Code:         Client:   Meaning:
# [0m           --        reset; clears all colors and styles (to white on black)
# [1m           --        bold on (see below)
# [3m           --        italics on
# [4m           --        underline on
# [7m           2.50      inverse on; reverses foreground & background colors
# [9m           2.50      strikethrough on
# [22m          2.50      bold off (see below)
# [23m          2.50      italics off
# [24m          2.50      underline off
# [27m          2.50      inverse off
# [29m          2.50      strikethrough off
# [30m          --        set foreground color to black
# [31m          --        set foreground color to red
# [32m          --        set foreground color to green
# [33m          --        set foreground color to yellow
# [34m          --        set foreground color to blue
# [35m          --        set foreground color to magenta (purple)
# [36m          --        set foreground color to cyan
# [37m          --        set foreground color to white
# [39m          2.53      set foreground color to default (white)
# [40m          --        set background color to black
# [41m          --        set background color to red
# [42m          --        set background color to green
# [43m          --        set background color to yellow
# [44m          --        set background color to blue
# [45m          --        set background color to magenta (purple)
# [46m          --        set background color to cyan
# [47m          --        set background color to white
# [49m          2.53      set background color to default (black)

class _TTkColor:
    __slots__ = ('_fg','_bg','_mod')
    _fg: str; _bg: str; _mod: str
    def __init__(self, fg:str="", bg:str="", mod:str=""):
        self._fg  = fg
        self._bg  = bg
        self._mod = mod

    def __str__(self):
        return self._fg+self._bg+self._mod

    def __eq__(self, other):
        if other is None: return False
        return \
            self._fg == other._fg and \
            self._bg == other._bg and \
            self._mod== other._mod

    def __add__(self, other):
        # TTkLog.debug("__add__")
        if isinstance(other, str):
            return str(self)+other
        else:
            fg:  str = self._fg  if other._fg == ""  else other._fg
            bg:  str = self._bg  if other._bg == ""  else other._bg
            mod: str = self._mod if other._mod == "" else other._mod
            return TTkColor(fg,bg,mod)

    def __radd__(self, other):
        # TTkLog.debug("__radd__")
        if isinstance(other, str):
            return other+str(self)
        else:
            fg:  str = self._fg  if other._fg == ""  else other._fg
            bg:  str = self._bg  if other._bg == ""  else other._bg
            mod: str = self._mod if other._mod == "" else other._mod
            return TTkColor(fg,bg,mod)

    def __sub__(self, other):
        # TTkLog.debug("__sub__")
        if other is None: return str(self)
        if "" == self._bg  != other._bg  or \
           "" == self._mod != other._mod :
            return '\033[0m'+self
        return str(self)

class TTkColor(_TTkColor):
    RST = _TTkColor('\033[0m')

    @staticmethod
    def fg(*args, **kwargs):
        return _TTkColor(fg=TTkHelper.Color.fg(*args, **kwargs))
    @staticmethod
    def bg(*args, **kwargs):
        return _TTkColor(bg=TTkHelper.Color.bg(*args, **kwargs))