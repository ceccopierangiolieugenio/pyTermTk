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
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.helper import TTkHelper

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
    __slots__ = ('_fg','_bg','_mod', '_colorMod')
    _fg: str; _bg: str; _mod: str
    def __init__(self, fg:str="", bg:str="", mod:str="", colorMod=None):
        self._fg  = fg
        self._bg  = bg
        self._mod = mod
        self._colorMod = colorMod

    def colorType(self):
        return \
            ( TTkK.Foreground if self._fg  != "" else TTkK.NONE ) | \
            ( TTkK.Background if self._bg  != "" else TTkK.NONE ) | \
            ( TTkK.Modifier   if self._mod != "" else TTkK.NONE )

    def getHex(self, ctype):
        if ctype == TTkK.Foreground:
            r,g,b = self.fgToRGB()
        else:
            r,g,b = self.bgToRGB()
        return "#{:06x}".format(r<<16|g<<8|b)

    def fgToRGB(self):
        if self._fg == "": return 0xff,0xff,0xff
        cc = self._fg.split(';')
        r = int(cc[2])
        g = int(cc[3])
        b = int(cc[4][:-1])
        return r,g,b

    def bgToRGB(self):
        if self._bg == "": return 0,0,0
        cc = self._bg.split(';')
        r = int(cc[2])
        g = int(cc[3])
        b = int(cc[4][:-1])
        return r,g,b

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
            fg:  str = other._fg or self._fg
            bg:  str = other._bg or self._bg
            mod: str = self._mod + other._mod
            colorMod = other._colorMod or self._colorMod
            return TTkColor(fg,bg,mod,colorMod)

    def __radd__(self, other):
        # TTkLog.debug("__radd__")
        if isinstance(other, str):
            return other+str(self)
        else:
            fg:  str = other._fg or self._fg
            bg:  str = other._bg or self._bg
            mod: self._mod + other._mod
            colorMod = other._colorMod or self._colorMod
            return TTkColor(fg,bg,mod,colorMod)

    def __sub__(self, other):
        # TTkLog.debug("__sub__")
        # if other is None: return str(self)
        if "" == self._bg  != other._bg  or \
           "" == self._fg  != other._fg  or \
           "" == self._mod != other._mod :
            return '\033[0m'+self
        return str(self)

    def modParam(self, *args, **kwargs):
        if self._colorMod is None: return self
        ret = self.copy()
        ret._colorMod.setParam(*args, **kwargs)
        return ret

    def mod(self, x , y):
        if self._colorMod is None: return self
        return self._colorMod.exec(x,y,self)

    def copy(self, modifier=True):
        ret = _TTkColor()
        ret._fg  = self._fg
        ret._bg  = self._bg
        ret._mod = self._mod
        if modifier:
            ret._colorMod = self._colorMod.copy()
        return ret

class _TTkColorModifier():
    def __init__(self, *args, **kwargs): pass
    def setParam(self, *args, **kwargs): pass
    def copy(self): return self

class TTkColorGradient(_TTkColorModifier):
    __slots__ = ('_increment', '_val', '_buffer')
    _increment: int; _val: int
    def __init__(self, *args, **kwargs):
        _TTkColorModifier.__init__(self, *args, **kwargs)
        self._increment = kwargs.get("increment",0)
        self._val = 0
        self._buffer = {}
    def setParam(self, *args, **kwargs):
        self._val = kwargs.get("val",0)
    def exec(self, x, y, color):
        def _applyGradient(c):
            if c == "": return c
            multiplier = abs(self._val + y)
            cc = c.split(';')
            #TTkLog.debug("Eugenio "+c.replace('\033','<ESC>'))
            r = int(cc[2])     + self._increment * multiplier
            g = int(cc[3])     + self._increment * multiplier
            b = int(cc[4][:-1])+ self._increment * multiplier
            r = max(min(255,r),0)
            g = max(min(255,g),0)
            b = max(min(255,b),0)
            return f"{cc[0]};{cc[1]};{r};{g};{b}m"

        bname = str(color)
        # I made a buffer to keep all the gradient values to speed up the paint process
        if bname not in self._buffer:
            self._buffer[bname] = [None]*(256*2)
        id = self._val + y - 256
        if self._buffer[bname][id] is not None:
            return self._buffer[bname][id]
        copy = color.copy(modifier=False)
        copy._fg = _applyGradient(color._fg)
        copy._bg = _applyGradient(color._bg)
        self._buffer[bname][id] = copy
        return self._buffer[bname][id]

    def copy(self):
        return self
        #ret = TTkColorGradient()
        #ret._increment = self._increment
        #ret._val = self._val
        #return ret



class TTkColor(_TTkColor):
    RST = _TTkColor(fg='\033[0m')

    # Modifiers:
    BOLD         = _TTkColor(mod='\033[1m')
    ITALIC       = _TTkColor(mod='\033[3m')
    UNDERLINE    = _TTkColor(mod='\033[4m')
    STRIKETROUGH = _TTkColor(mod='\033[9m')

    @staticmethod
    def fg(*args, **kwargs):
        mod = kwargs.get('modifier', None )
        if len(args) > 0:
            color = args[0]
        else:
            color = kwargs.get('color', "" )
        return TTkColor(fg=TTkHelper.Color.fg(color), colorMod=mod)

    @staticmethod
    def bg(*args, **kwargs):
        mod = kwargs.get('modifier', None )
        if len(args) > 0:
            color = args[0]
        else:
            color = kwargs.get('color', "" )
        return TTkColor(bg=TTkHelper.Color.bg(color), colorMod=mod)

