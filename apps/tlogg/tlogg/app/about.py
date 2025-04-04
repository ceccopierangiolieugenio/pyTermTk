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

__all__ = ['About']

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
from TermTk import TTkAbout, TTkWindow
from .cfg import TloggCfg

class About(TTkAbout):
    tlogg = [
        " __    ___                               ",
        "/\ \__/\_ \                              ",
        "\ \ ,_\//\ \     ___      __      __     ",
        " \ \ \/ \ \ \   / __`\  /'_ `\  /'_ `\   ",
        "  \ \ \_ \_\ \_/\ \L\ \/\ \L\ \/\ \L\ \  ",
        "   \ \__\/\____\ \____/\ \____ \ \____ \ ",
        "    \/__/\/____/\/___/  \/___L\ \/___L\ \\",
        "                          /\____/ /\____/",
        "                          \_/__/  \_/__/ "]

    __slots__=('_image')
    def __init__(self, *args, **kwargs):
        TTkAbout.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'About' )
        self.setTitle('[PierCecco Cecco] Eugenio Parodi proudly presents...')
        self.resize(56,16)



    def paintEvent(self, canvas):
        c = [0xFF,0xFF,0xFF]
        for y, line in enumerate(About.tlogg):
            canvas.drawText(pos=(13,3+y),text=line, color=TTkColor.fg(f'#{c[0]:02X}{c[1]:02X}{c[2]:02X}'))
            c[2]-=0x18
            c[0]-=0x08
        canvas.drawText(pos=(26,4),text=f"  Version: {TloggCfg.version}", color=TTkColor.fg('#AAAAFF'))
        canvas.drawText(pos=(14,11),text=f"Powered By, pyTermTk")
        canvas.drawText(pos=(2,13),text=f"https://github.com/ceccopierangiolieugenio/tlogg", color=TTkColor.fg('#44FFFF'))
        canvas.drawText(pos=(2,14),text=f"https://github.com/ceccopierangiolieugenio/pyTermTk", color=TTkColor.fg('#44FFFF'))

        TTkWindow.paintEvent(self, canvas)
