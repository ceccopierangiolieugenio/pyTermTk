# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk import TTkAbout, TTkWindow
from .cfg import TTkDesignerCfg

class About(TTkAbout):
    # designerTxt = [
    #     "   ____          _                 ",
    #     "╭─|    \ ___ ___|_|___ ___ ___ ___ ",
    #     "│ |  |  | -_|_ -| | . |   | -_|  _|",
    #     "TTk____/|___|___|_|_  |_|_|___|_|  ",
    #     "╰─────────────────|___|──────────┄ "]
    designerTxt = [
                                                                        TTkString("   ____          _                 ",TTkColor.fg("#FFFFFF")),
        TTkString("╭─", TTkColor.fg("#4400FF"))+                        TTkString(  "|    \ ___ ___|_|___ ___ ___ ___ ",TTkColor.fg("#F8FFE8")),
        TTkString("│ ", TTkColor.fg("#5500FF"))+                        TTkString(  "|  |  | -_|_ -| | . |   | -_|  _|",TTkColor.fg("#EFFFCF")),
        TTkString("TTk",TTkColor.fg("#00FF66")+TTkColor.bg("#7700FF"))+ TTkString(   "____/|___|___|_|_  |_|_|___|_|  ",TTkColor.fg("#E8FFB8")),
        TTkString("╰─────────────────",TTkColor.fg("#9900FF"))+         TTkString(                  "|___|",            TTkColor.fg("#DFFF9F"))+TTkString("──────────┄ ",TTkColor.fg("#BB00FF"))]

    __slots__=('_image')
    def __init__(self, *args, **kwargs):
        TTkAbout.__init__(self, *args, **kwargs)

        self.setTitle('[PierCecco Cecco] Eugenio Parodi proudly presents...')
        self.resize(56,15)

    def paintEvent(self, canvas):
        c = [0xFF,0xFF,0xFF]
        for y, line in enumerate(About.designerTxt):
            canvas.drawText(pos=(13,3+y),text=line)
        canvas.drawText(pos=(20, 9),text=f"  Version: {TTkDesignerCfg.version}", color=TTkColor.fg('#AAAAFF'))
        canvas.drawText(pos=(14,11),text=f"Powered By, pyTermTk")
        canvas.drawText(pos=( 2,13),text=f"https://github.com/ceccopierangiolieugenio/pyTermTk", color=TTkColor.fg('#44FFFF'))

        TTkWindow.paintEvent(self, canvas)
