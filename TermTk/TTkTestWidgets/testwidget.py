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

__all__ = ['TTkTestWidget']

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.widget import *
from TermTk.TTkWidgets.button import *
from TermTk.TTkWidgets.label import *
from TermTk.TTkWidgets.frame import *

class _TestContent(TTkWidget):
    t01 = TTkString(color=TTkColor.fg("#ff0000") ,text="     L😎rem ipsum dolor sit amet, ⌚ ❤ 💙 🙋'")
    t02 = TTkString(color=TTkColor.fg("#ff8800") ,text="consectetur adipiscing elit,")
    t03 = TTkString(color=TTkColor.fg("#ffff00") ,text="sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
    t04 = TTkString(color=TTkColor.fg("#00ff00") ,text="Ut enim ad minim veniam,")
    t05 = TTkString(color=TTkColor.fg("#00ffff") ,text="quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
    t06 = TTkString(color=TTkColor.fg("#0088ff") ,text="Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
    t07 = TTkString(color=TTkColor.fg("#0000ff") ,text="Excepteur sint occaecat cupidatat non proident,")
    t08 = TTkString(color=TTkColor.fg("#ff00ff") ,text="sunt in culpa qui officia deserunt mollit anim id est laborum.")
    def paintEvent(self, canvas):
        # TTkLog.debug(f"Test Paint - {self._name}")
        y=0;  canvas.drawText(pos=(-5,y), text=self.t01)
        y+=1; canvas.drawText(pos=( 0,y), text=self.t02)
        y+=1; canvas.drawText(pos=( 0,y), text=self.t03)
        y+=1; canvas.drawText(pos=( 0,y), text=self.t04)
        y+=1; canvas.drawText(pos=( 0,y), text=self.t05)
        y+=1; canvas.drawText(pos=( 0,y), text=self.t06)
        y+=1; canvas.drawText(pos=( 0,y), text=self.t07)
        y+=1; canvas.drawText(pos=( 0,y), text=self.t08)
        y+=1; canvas.drawGrid(
                pos=(0,y),size=(self._width,self._height-y),
                hlines=(2,5,7), vlines=(4,7,15,30),
                color=TTkColor.fg("#aaffaa"))



class TTkTestWidget(TTkFrame):
    ID = 1
    __slots__ = ('_l')
    def __init__(self, *args, **kwargs):
        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , f"TestWidget-{TTkTestWidget.ID}" )
        TTkButton(parent=self, width=15, height=3, border=True, text=' Test Button')
        label = TTkLabel(parent=self,pos=(20, 1), size=(50,1))
        label.setText(TTkString("test \033[42;1;30mANSI\033[44;1;33m TTkString",TTkColor.bg('#440099')+TTkColor.UNDERLINE))
        self._l = [
                TTkColor.bg('#440099')+TTkColor.fg('#00ffff'),
                TTkColor.bg('#440077')+TTkColor.fg('#00ccff'),
                TTkColor.bg('#440066')+TTkColor.fg('#0088ff'),
                TTkColor.bg('#440055')+TTkColor.fg('#0055ff'),
                TTkColor.bg('#440033')+TTkColor.fg('#0033ff'),
            ]
        _TestContent(parent=self, pos=(0,8), width=50, height=50, name=f"content-{self._name}")
        TTkTestWidget.ID+=1

    def paintEvent(self, canvas):
        x = 1 if self.border() else 0
        y = 1 if self.border() else 0
        w = 50
        canvas.drawText(pos=(x,y+3), width=w, color=self._l[0], text=f"Test Widget [{self._name}]")
        canvas.drawText(pos=(x,y+4), width=w, color=self._l[1], text=f"x,y ({self._x},{self._y})")
        canvas.drawText(pos=(x,y+5), width=w, color=self._l[2], text=f"w,h ({self._width},{self._height})")
        canvas.drawText(pos=(x,y+6), width=w, color=self._l[3], text=f"max w,h ({self._maxw},{self._maxh})")
        canvas.drawText(pos=(x,y+7), width=w, color=self._l[4], text=f"min w,h ({self._minw},{self._minh})")
        TTkFrame.paintEvent(self, canvas)

    def mousePressEvent(self, evt):
        TTkLog.debug(f"{self._name} Test Mouse {evt}")

    def mouseDragEvent(self, evt):
        TTkLog.debug(f"{self._name} Test Mouse {evt}")