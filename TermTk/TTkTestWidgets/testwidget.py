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
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import *
from TermTk.TTkWidgets.button import *
from TermTk.TTkWidgets.label import *
from TermTk.TTkWidgets.frame import *

class _TestContent(TTkWidget):
    def paintEvent(self):
        # TTkLog.debug(f"Test Paint - {self._name}")
        y=0;  self._canvas.drawText(pos=(-5,y),color=TTkColor.fg("#ff0000"),text="     Lorem ipsum dolor sit amet,")
        y+=1; self._canvas.drawText(pos=(0,y),color=TTkColor.fg("#ff8800"),text="consectetur adipiscing elit,")
        y+=1; self._canvas.drawText(pos=(0,y),color=TTkColor.fg("#ffff00"),text="sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        y+=1; self._canvas.drawText(pos=(0,y),color=TTkColor.fg("#00ff00"),text="Ut enim ad minim veniam,")
        y+=1; self._canvas.drawText(pos=(0,y),color=TTkColor.fg("#00ffff"),text="quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        y+=1; self._canvas.drawText(pos=(0,y),color=TTkColor.fg("#0088ff"),text="Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
        y+=1; self._canvas.drawText(pos=(0,y),color=TTkColor.fg("#0000ff"),text="Excepteur sint occaecat cupidatat non proident,")
        y+=1; self._canvas.drawText(pos=(0,y),color=TTkColor.fg("#ff00ff"),text="sunt in culpa qui officia deserunt mollit anim id est laborum.")
        y+=1; self._canvas.drawGrid(
                pos=(0,y),size=(self._width,self._height-y),
                hlines=(2,5,7), vlines=(4,7,15,30),
                color=TTkColor.fg("#aaffaa"))



class TTkTestWidget(TTkFrame):
    ID = 1
    __slots__ = ('_name', '_l')
    def __init__(self, *args, **kwargs):
        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTestWidget' )
        #self.setLayout(TTkHBoxLayout())
        self._name = f"TestWidget-{TTkTestWidget.ID}"
        t,_,l,_ = self.getPadding()
        TTkButton(parent=self, x=l, y=t, width=15, height=3, border=True, text=' Test Button')
        self._l = [
                TTkLabel(parent=self,pos=(l, t+3), size=(50,1), color=TTkColor.bg('#440099')+TTkColor.fg('#00ffff'), text="pippo"),
                TTkLabel(parent=self,pos=(l, t+4), size=(50,1), color=TTkColor.bg('#440077')+TTkColor.fg('#00ccff')),
                TTkLabel(parent=self,pos=(l, t+5), size=(50,1), color=TTkColor.bg('#440066')+TTkColor.fg('#0088ff')),
                TTkLabel(parent=self,pos=(l, t+6), size=(50,1), color=TTkColor.bg('#440055')+TTkColor.fg('#0055ff')),
                TTkLabel(parent=self,pos=(l, t+7), size=(50,1), color=TTkColor.bg('#440033')+TTkColor.fg('#0033ff')),
            ]
        _TestContent(parent=self, x=l, y=t+8, width=50, height=50, name=f"content-{self._name}")
        TTkTestWidget.ID+=1

    def paintEvent(self):
        TTkFrame.paintEvent(self)
        self._l[0].text=f"Test Widget [{self._name}]"
        self._l[1].text=f"x,y ({self._x},{self._y})"
        self._l[2].text=f"w,h ({self._width},{self._height})"
        self._l[3].text=f"max w,h ({self._maxw},{self._maxh})"
        self._l[4].text=f"min w,h ({self._minw},{self._minh})"


    def mousePressEvent(self, evt):
        TTkLog.debug(f"{self._name} Test Mouse {evt}")

    def mouseDragEvent(self, evt):
        TTkLog.debug(f"{self._name} Test Mouse {evt}")