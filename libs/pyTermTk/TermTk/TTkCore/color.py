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

__all__ = ['TTkColor',
           'TTkColorModifier',
           'TTkColorGradient', 'TTkLinearGradient', 'TTkAlternateColor']

from TermTk.TTkCore.TTkTerm.colors import TTkTermColor
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
    __slots__ = ('_fg','_bg', '_colorMod', '_buffer', '_clean')
    _fg: tuple[int]
    _bg: tuple[int]
    def __init__(self,
                 fg:tuple[int]=None,
                 bg:tuple[int]=None,
                 colorMod=None,
                 clean=False) -> None:
        self._fg  = fg
        self._bg  = bg
        self._clean = clean or not (fg or bg)
        self._colorMod = colorMod
        self._buffer = None

    def foreground(self):
        if self._fg:
            return _TTkColor(fg=self._fg)
        else:
            return TTkColor.RST

    def background(self):
        if self._bg:
            return _TTkColor(bg=self._bg)
        else:
            return TTkColor.RST

    def hasForeground(self) -> bool:
        return True if self._fg else False

    def hasBackground(self) -> bool:
        return True if self._bg else False

    def bold(self) -> bool:
        return  False

    def italic(self) -> bool:
        return  False

    def underline(self) -> bool:
        return  False

    def strikethrough(self) -> bool:
        return  False

    def blinking(self) -> bool:
        return  False

    def colorType(self):
        return (
            ( TTkK.ColorType.ColorModifier if self._colorMod  else TTkK.NONE ) |
            ( TTkK.ColorType.Foreground    if self._fg        else TTkK.NONE ) |
            ( TTkK.ColorType.Background    if self._bg        else TTkK.NONE ) )

    @staticmethod
    def rgb2hsl(rgb):
        r = rgb[0]/255
        g = rgb[1]/255
        b = rgb[2]/255
        cmax = max(r,g,b)
        cmin = min(r,g,b)

        lum = (cmax+cmin)/2
        if cmax == cmin:
            return 0,0,lum

        delta = cmax-cmin
        if   cmax == r:
            hue = ((g-b)/delta)%6
        elif cmax == g:
            hue = (b-r)/delta+2
        else:
            hue = (r-g)/delta+4

        sat = delta / (1 - abs(delta-1))
        hue = int(hue*60) + ( 360 if hue < 0 else 0 )
        sat = int(sat*100)
        lum = int(lum*100)

        return hue,sat,lum

    @staticmethod
    def hsl2rgb(hsl):
        hue = hsl[0]
        sat = hsl[1] / 100
        lum = hsl[2] / 100

        c = (1-abs(2*lum-1))*sat
        x = c*(1-abs((hue/60)%2-1))
        m = lum-c/2

        if     0 <= hue < 60:
          r,g,b = c,x,0
        elif  60 <= hue < 120:
          r,g,b = x,c,0
        elif 120 <= hue < 180:
          r,g,b = 0,c,x
        elif 180 <= hue < 240:
          r,g,b = 0,x,c
        elif 240 <= hue < 300:
          r,g,b = x,0,c
        elif 300 <= hue < 360:
          r,g,b = c,0,x

        r = int((r + m) * 255)
        g = int((g + m) * 255)
        b = int((b + m) * 255)

        return r,g,b

    def getHex(self, ctype):
        if ctype == TTkK.ColorType.Foreground:
            r,g,b = self.fgToRGB()
        else:
            r,g,b = self.bgToRGB()
        return f"#{r<<16|g<<8|b:06x}"

    def fgToRGB(self):
        return self._fg if self._fg else (0,0,0)

    def bgToRGB(self):
        return self._bg if self._bg else (0,0,0)

    def invertFgBg(self):
        ret = self.copy()
        ret._fg = self._bg
        ret._bg = self._fg
        return ret

    def __str__(self):
        if not self._buffer:
            self._buffer = TTkTermColor.rgb2ansi(
                                fg=self._fg, bg=self._bg,
                                clean=self._clean)
        return self._buffer

    def __eq__(self, other):
        if not other: return False
        return (
            self._fg   == other._fg and
            self._bg   == other._bg )

    # self | other
    def __or__(self, other):
        c = self.copy()
        c._clean = False
        return other + c

    # self + other
    def __add__(self, other):
        # TTkLog.debug("__add__")
        if other._clean:
            return other
        clean = self._clean
        fg:  str = other._fg or self._fg
        bg:  str = other._bg or self._bg
        colorMod = other._colorMod or self._colorMod
        return _TTkColor(
                    fg=fg, bg=bg,
                    colorMod=colorMod,
                    clean=clean)

    def __sub__(self, other) -> str:
        '''
        I am abusing this operator in order to save time in the diff resolv between two adjacent colors
        '''
        if ( None == self._bg   != other._bg or
             None == self._fg   != other._fg ):
            return TTkTermColor.rgb2ansi(
                                fg=self._fg, bg=self._bg,
                                clean=True)
        return str(self)

    def modParam(self, *args, **kwargs) -> None:
        if not self._colorMod: return self
        ret = self.copy()
        ret._colorMod.setParam(*args, **kwargs)
        return ret

    def mod(self, x , y):
        if not self._colorMod: return self
        return self._colorMod.exec(x,y,self)

    def copy(self, modifier=True):
        ret = _TTkColor()
        ret._fg   = self._fg
        ret._bg   = self._bg
        ret._clean = self._clean
        if modifier and self._colorMod:
            ret._colorMod = self._colorMod.copy()
        return ret

class _TTkColor_mod(_TTkColor):
    __slots__ = ('_mod')
    _mod: int
    def __init__(self, *,
                 mod:int=0,
                 **kwargs
                 ) -> None:
        self._mod = mod
        super().__init__(**kwargs)
        self._clean = self._clean and not mod

    def bold(self) -> bool:
        return  self._mod & TTkTermColor.BOLD

    def italic(self) -> bool:
        return  self._mod & TTkTermColor.ITALIC

    def underline(self) -> bool:
        return  self._mod & TTkTermColor.UNDERLINE

    def strikethrough(self) -> bool:
        return  self._mod & TTkTermColor.STRIKETROUGH

    def blinking(self) -> bool:
        return  self._mod & TTkTermColor.BLINKING

    def colorType(self):
        return (
            super().colorType() |
            ( TTkK.ColorType.Modifier if self._mod else TTkK.NONE ))

    def __str__(self):
        if not self._buffer:
            self._buffer = TTkTermColor.rgb2ansi(
                                fg=self._fg, bg=self._bg, mod=self._mod,
                                clean=self._clean)
        return self._buffer

    def __eq__(self, other):
        return (
                _TTkColor.__eq__(self,other) and
                ( self._mod == (other._mod if isinstance(other,_TTkColor_mod) else 0))
            )

    # self | other
    def __or__(self, other):
        c = self.copy()
        c._clean = False
        return other + c

    # self + other
    def __add__(self, other):
        # TTkLog.debug("__add__")
        if other._clean:
            return other
        otherMod = other._mod if isinstance(other,_TTkColor_mod) else 0
        clean = self._clean
        fg:  str = other._fg or self._fg
        bg:  str = other._bg or self._bg
        mod: str = self._mod + otherMod
        colorMod = other._colorMod or self._colorMod
        return _TTkColor_mod(
                    fg=fg, bg=bg, mod=mod,
                    colorMod=colorMod,
                    clean=clean)

    # self + other
    def __radd__(self, other):
        # TTkLog.debug("__add__")
        if self._clean:
            return self
        clean = other._clean
        fg:  str = self._fg or other._fg
        bg:  str = self._bg or other._bg
        mod: str = self._mod
        colorMod = self._colorMod or other._colorMod
        return _TTkColor_mod(
                    fg=fg, bg=bg, mod=mod,
                    colorMod=colorMod,
                    clean=clean)

    def __sub__(self, other) -> str:
        otherMod = other._mod if isinstance(other,_TTkColor_mod) else 0
        if ( None == self._bg   != other._bg or
             None == self._fg   != other._fg or
                     self._mod  != otherMod ):
            return TTkTermColor.rgb2ansi(
                                fg=self._fg, bg=self._bg, mod=self._mod,
                                clean=True)
        return str(self)

    def __rsub__(self, other) -> str:
        return TTkTermColor.rgb2ansi(fg=other._fg, bg=other._bg, clean=True)

    def copy(self, modifier=True):
        ret = _TTkColor_mod()
        ret._fg   = self._fg
        ret._bg   = self._bg
        ret._mod  = self._mod
        ret._clean = self._clean
        if modifier and self._colorMod:
            ret._colorMod = self._colorMod.copy()
        return ret


class _TTkColor_mod_link(_TTkColor_mod):
    __slots__ = ('_link')
    _link: str
    def __init__(self, *,
                 link:str='',
                 **kwargs
                 ) -> None:
        self._link = link
        super().__init__(**kwargs)
        self._clean = self._clean and not link

    def colorType(self):
        return (
            super().colorType() |
            ( TTkK.Link if self._link else TTkK.NONE ))

    def __str__(self):
        if not self._buffer:
            self._buffer = TTkTermColor.rgb2ansi_link(
                                fg=self._fg, bg=self._bg, mod=self._mod,
                                link=self._link, clean=self._clean)
        return self._buffer

    def __eq__(self, other):
        return (
                _TTkColor_mod.__eq__(self,other) and
                ( self._link == (other._link if isinstance(other,_TTkColor_mod_link) else 0))
            )

    # self | other
    def __or__(self, other):
        c = self.copy()
        c._clean = False
        return other + c

    # self + other
    def __add__(self, other):
        # TTkLog.debug("__add__")
        if other._clean:
            return other
        otherMod  = other._mod  if isinstance(other,_TTkColor_mod) else 0
        otherLink = other._link if isinstance(other,_TTkColor_mod_link) else ''
        clean = self._clean
        fg:  str = other._fg or self._fg
        bg:  str = other._bg or self._bg
        mod: str = self._mod + otherMod
        link:str = self._link or otherLink
        colorMod = other._colorMod or self._colorMod
        return _TTkColor_mod_link(
                    fg=fg, bg=bg, mod=mod,
                    colorMod=colorMod, link=link,
                    clean=clean)

    def __radd__(self, other):
        # TTkLog.debug("__add__")
        if self._clean:
            return self
        otherMod  = other._mod  if isinstance(other,_TTkColor_mod) else 0
        clean = self._clean
        fg:  str = self._fg or other._fg
        bg:  str = self._bg or other._bg
        mod: str = self._mod + otherMod
        link:str = self._link
        colorMod = self._colorMod or other._colorMod
        return _TTkColor_mod_link(
                    fg=fg, bg=bg, mod=mod,
                    colorMod=colorMod, link=link,
                    clean=clean)

    def __sub__(self, other):
        # TTkLog.debug("__sub__")
        # if other is None: return str(self)
        otherMod  = other._mod  if isinstance(other,_TTkColor_mod) else 0
        otherLink = other._link if isinstance(other,_TTkColor_mod_link) else ''
        if ( None == self._bg   != other._bg or
             None == self._fg   != other._fg or
                     self._link != otherLink or
                     self._mod  != otherMod ):
            return TTkTermColor.rgb2ansi_link(
                                fg=self._fg, bg=self._bg, mod=self._mod,
                                link=self._link, clean=True)
        return ''

    def __rsub__(self, other) -> str:
        if type(other) == _TTkColor:
            return TTkTermColor.rgb2ansi_link(fg=other._fg, bg=other._bg, clean=True, cleanLink=True)
        else:
            return TTkTermColor.rgb2ansi_link(fg=other._fg, bg=other._bg, mod=other._mod, clean=True, cleanLink=True)

    def copy(self, modifier=True):
        ret = _TTkColor_mod_link()
        ret._fg   = self._fg
        ret._bg   = self._bg
        ret._mod  = self._mod
        ret._link = self._link
        ret._clean = self._clean
        if modifier and self._colorMod:
            ret._colorMod = self._colorMod.copy()
        return ret


class TTkColorModifier():
    def __init__(self, *args, **kwargs) -> None: pass
    def setParam(self, *args, **kwargs) -> None: pass
    def copy(self): return self

class TTkColorGradient(TTkColorModifier):
    '''TTkColorGradient'''

    __slots__ = ('_fgincrement', '_bgincrement', '_val', '_step', '_buffer', '_orientation')
    _increment: int; _val: int
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if "increment" in kwargs:
            self._fgincrement = kwargs.get("increment")
            self._bgincrement = kwargs.get("increment")
        else:
            self._fgincrement = kwargs.get("fgincrement",0)
            self._bgincrement = kwargs.get("bgincrement",0)
        self._orientation = kwargs.get("orientation", TTkK.VERTICAL)
        self._val = 0
        self._step = 1
        self._buffer = {}

    def setParam(self, *args, **kwargs) -> None:
        self._val = kwargs.get("val",0)
        self._step = kwargs.get("step",1)

    def exec(self, x, y, color):
        vx = x if self._orientation == TTkK.HORIZONTAL else y
        step = self._step
        def _applyGradient(c,incr):
            if not c: return c
            multiplier = abs(self._val + vx)
            r = int(c[0])+ incr * multiplier // step
            g = int(c[1])+ incr * multiplier // step
            b = int(c[2])+ incr * multiplier // step
            r = max(min(255,r),0)
            g = max(min(255,g),0)
            b = max(min(255,b),0)
            return (r,g,b)

        bname = str(color)
        # I made a buffer to keep all the gradient values to speed up the paint process
        if bname not in self._buffer:
            self._buffer[bname] = [None]*(256*2)
        id = self._val + vx - 256
        if self._buffer[bname][id] is not None:
            return self._buffer[bname][id]
        copy = color.copy(modifier=False)
        copy._fg = _applyGradient(color._fg, self._fgincrement)
        copy._bg = _applyGradient(color._bg, self._bgincrement)
        self._buffer[bname][id] = copy
        return self._buffer[bname][id]

    def copy(self):
        return self

class TTkLinearGradient(TTkColorModifier):
    '''TTkLinearGradient'''

    __slots__ = (
        '_direction', '_direction_squaredlength',
        '_base_pos', '_target_color')

    default_target_color = _TTkColor(fg=(0,255,0), bg=(255,0,0))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._base_pos = (0, 0)
        self._direction = (30, 30)
        self._target_color = self.default_target_color
        self.setParam(*args, **kwargs)

    def setParam(self, *args, **kwargs) -> None:
        self._base_pos = tuple(kwargs.get('base_pos', self._base_pos))
        direct = tuple(kwargs.get('direction', self._direction))
        self._direction = direct
        self._direction_squaredlength = direct[0]*direct[0] + direct[1]*direct[1]
        self._target_color = kwargs.get('target_color', self._target_color)

    def exec(self, x, y, base_color):
        diffx, diffy = x - self._base_pos[0], y - self._base_pos[1]
        prod = diffx * self._direction[0] + diffy * self._direction[1]
        beta = prod/self._direction_squaredlength
        if beta <= 0:
            return base_color
        target_color = self._target_color
        if beta >= 1:
            return target_color
        alpha = 1.0 - beta
        copy = base_color.copy(modifier=False)
        if copy._fg is not None  and  target_color._fg is not None:
            copy._fg = (
                int(alpha*base_color._fg[0] + beta*target_color._fg[0]),
                int(alpha*base_color._fg[1] + beta*target_color._fg[1]),
                int(alpha*base_color._fg[2] + beta*target_color._fg[2]))
        if copy._bg is not None  and  target_color._bg is not None:
            copy._bg = (
                int(alpha*base_color._bg[0] + beta*target_color._bg[0]),
                int(alpha*base_color._bg[1] + beta*target_color._bg[1]),
                int(alpha*base_color._bg[2] + beta*target_color._bg[2]))
        return copy

class TTkColor(_TTkColor):
    ''' TermTk Color helper

    .. role:: strike
        :class: strike

    .. role:: underline
        :class: underline

    The TTkColor constructor creates the color based on HEX values.

    Example:

    .. code:: python

        # Foreground only colors:
        color_fg_red   = TTkColor.fg('#FF0000')
        color_fg_green = TTkColor.fg('#00FF00')
        color_fg_blue  = TTkColor.fg('#0000FF')

        # Background only colors:
        color_bg_red   = TTkColor.bg('#FF0000')
        color_bg_green = TTkColor.bg('#00FF00')
        color_bg_blue  = TTkColor.bg('#0000FF')

        # Combine
        color_1 = color_fg_red + color_bg_blue
        color_2 = color_fg_red + TTkColor.bg('#FFFF00')
        color_3 = color_2 + TTkColor.UNDERLINE + TTkColor.BOLD

        # Use presets
        color_4 = TTkColor.RED
        color_5 = TTkColor.BG_YELLOW + color_4
        color_6 = color_5 + TTkColor.UNDERLINE + TTkColor.BOLD

    '''
    RST = _TTkColor()
    '''Reset to the default terminal color and modifiers'''

    BLACK   = _TTkColor(fg=(  0,  0,  0))
    '''(fg) #000000 - Black'''
    WHITE   = _TTkColor(fg=(255,255,255))
    '''(fg) #FFFFFF - White'''
    RED     = _TTkColor(fg=(255,  0,  0))
    '''(fg) #FF0000 - Red'''
    GREEN   = _TTkColor(fg=(  0,255,  0))
    '''(fg) #00FF00 - Green'''
    BLUE    = _TTkColor(fg=(  0,  0,255))
    '''(fg) #0000FF - Blue'''
    CYAN    = _TTkColor(fg=(  0,255,255))
    '''(fg) #00FFFF - Cyan'''
    MAGENTA = _TTkColor(fg=(255,  0,255))
    '''(fg) #FF00FF - Magenta'''
    YELLOW  = _TTkColor(fg=(255,255,  0))
    '''(fg) #FFFF00 - Yellow'''

    FG_BLACK   = BLACK
    '''(fg) #000000 - Black'''
    FG_WHITE   = WHITE
    '''(fg) #FFFFFF - White'''
    FG_RED     = RED
    '''(fg) #FF0000 - Red'''
    FG_GREEN   = GREEN
    '''(fg) #00FF00 - Green'''
    FG_BLUE    = BLUE
    '''(fg) #0000FF - Blue'''
    FG_CYAN    = CYAN
    '''(fg) #00FFFF - Cyan'''
    FG_MAGENTA = MAGENTA
    '''(fg) #FF00FF - Magenta'''
    FG_YELLOW  = YELLOW
    '''(fg) #FFFF00 - Yellow'''

    BG_BLACK   = BLACK.invertFgBg()
    '''(bg) #000000 - Black'''
    BG_WHITE   = WHITE.invertFgBg()
    '''(bg) #FFFFFF - White'''
    BG_RED     = RED.invertFgBg()
    '''(bg) #FF0000 - Red'''
    BG_GREEN   = GREEN.invertFgBg()
    '''(bg) #00FF00 - Green'''
    BG_BLUE    = BLUE.invertFgBg()
    '''(bg) #0000FF - Blue'''
    BG_CYAN    = CYAN.invertFgBg()
    '''(bg) #00FFFF - Cyan'''
    BG_MAGENTA = MAGENTA.invertFgBg()
    '''(bg) #FF00FF - Magenta'''
    BG_YELLOW  = YELLOW.invertFgBg()
    '''(bg) #FFFF00 - Yellow'''

    # Modifiers:
    BOLD         = _TTkColor_mod(mod=TTkTermColor.BOLD)
    '''**Bold** modifier'''
    ITALIC       = _TTkColor_mod(mod=TTkTermColor.ITALIC)
    '''*Italic* modifier'''
    UNDERLINE    = _TTkColor_mod(mod=TTkTermColor.UNDERLINE)
    ''':underline:`Underline` modifier'''
    STRIKETROUGH = _TTkColor_mod(mod=TTkTermColor.STRIKETROUGH)
    ''':strike:`Striketrough` modifier'''

    BLINKING     = _TTkColor_mod(mod=TTkTermColor.BLINKING)
    '''"Blinking" modifier'''

    @staticmethod
    def hexToRGB(val):
        r = int(val[1:3],base=16)
        g = int(val[3:5],base=16)
        b = int(val[5:7],base=16)
        return (r,g,b)

    @staticmethod
    def ansi(ansi):
        fg,bg,mod,clean = TTkTermColor.ansi2rgb(ansi)
        if mod:
            return _TTkColor_mod(fg=fg, bg=bg, mod=mod, clean=clean)
        else:
            return _TTkColor(fg=fg, bg=bg, clean=clean)

    @staticmethod
    def fg(*args, **kwargs) -> None:
        ''' Helper to generate a Foreground color

        Example:

        .. code:: python

            color_1 = TTkColor.fg('#FF0000')
            color_2 = TTkColor.fg(color='#00FF00')
            color_3 = TTkColor.fg('#0000FF', modifier=TTkColorGradient(increment=6))

        :param str color: the color representation in (str)HEX
        :type color: str
        :param str modifier: (experimental) the color modifier to be used to improve the **kinkiness**
        :type modifier: TTkColorModifier, optional

        :return: :py:class:`TTkColor`
        '''
        mod = kwargs.get('modifier', None )
        link = kwargs.get('link', '' )
        if len(args) > 0:
            color = args[0]
        else:
            color = kwargs.get('color', "" )
        if link:
            return _TTkColor_mod_link(fg=TTkColor.hexToRGB(color), colorMod=mod, link=link)
        else:
            return _TTkColor(fg=TTkColor.hexToRGB(color), colorMod=mod)

    @staticmethod
    def bg(*args, **kwargs) -> None:
        ''' Helper to generate a Background color

        Example:

        .. code:: python

            color_1 = TTkColor.bg('#FF0000')
            color_2 = TTkColor.bg(color='#00FF00')
            color_3 = TTkColor.bg('#0000FF', modifier=TTkColorGradient(increment=6))

        :param str color: the color representation in (str)HEX
        :type color: str
        :param str modifier: (experimental) the color modifier to be used to improve the **kinkiness**
        :type modifier: TTkColorModifier, optional

        :return: :py:class:`TTkColor`
        '''
        mod = kwargs.get('modifier', None )
        link = kwargs.get('link', '' )
        if len(args) > 0:
            color = args[0]
        else:
            color = kwargs.get('color', "" )
        if link:
            return _TTkColor_mod_link(bg=TTkColor.hexToRGB(color), colorMod=mod, link=link)
        else:
            return _TTkColor(bg=TTkColor.hexToRGB(color), colorMod=mod)

    @staticmethod
    def fgbg(fg:str='', bg:str='', link:str='', modifier:TTkColorModifier=None):
        ''' Helper to generate a Background color

        Example:

        .. code:: python

            color_1 = TTkColor.fgbg('#FF0000','#0000FF')
            color_2 = TTkColor.fgbg(fg='#00FF00',bg='#0000FF')
            color_3 = TTkColor.fgbg('#0000FF','#0000FF', modifier=TTkColorGradient(increment=6))

        :param str fg: the foreground color representation in (str)HEX
        :type fg: str
        :param str bg: the background color representation in (str)HEX
        :type bg: str
        :param str modifier: (experimental) the color modifier to be used to improve the **kinkiness**
        :type modifier: TTkColorModifier, optional

        :return: :py:class:`TTkColor`
        '''
        if link:
            return _TTkColor_mod_link(fg=TTkColor.hexToRGB(fg), bg=TTkColor.hexToRGB(bg), colorMod=modifier, link=link)
        else:
            return _TTkColor(fg=TTkColor.hexToRGB(fg), bg=TTkColor.hexToRGB(bg), colorMod=modifier)

class TTkAlternateColor(TTkColorModifier):
    '''TTkAlternateColor'''

    __slots__ = ('_alternateColor')
    def __init__(self, alternateColor:TTkColor=TTkColor.RST, **kwargs) -> None:
        super().__init__(**kwargs)
        self.setParam(alternateColor)

    def setParam(self, alternateColor:TTkColor):
        self._alternateColor = alternateColor

    def exec(self, x:int, y:int, base_color:TTkColor) -> TTkColor:
        if y%2: return self._alternateColor
        else:   return base_color.copy(modifier=False)
