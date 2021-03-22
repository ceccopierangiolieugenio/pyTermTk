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

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import *

class TTkRadioButton(TTkWidget):
    _radioLists = {}
    __slots__ = ('_checked')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkRadioButton' )
        # Define Signals
        # self.cehcked = pyTTkSignal()
        self._checked = kwargs.get('checked', False )
        self.setMinimumSize(3, 1)
        self.setMaximumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)
        if self._name not in TTkRadioButton._radioLists:
            TTkRadioButton._radioLists[self._name] = [self]
        else:
            TTkRadioButton._radioLists[self._name].append(self)

    def paintEvent(self):
        if self.hasFocus():
            borderColor = TTkCfg.theme.radioButtonBorderColorFocus
            color       = TTkCfg.theme.radioButtonContentColorFocus
        else:
            borderColor = TTkCfg.theme.radioButtonBorderColor
            color       = TTkCfg.theme.radioButtonContentColor
        if self._checked:
            self._canvas.drawText(pos=(0,0), color=borderColor ,text="( )")
            self._canvas.drawText(pos=(1,0), color=color ,text="X")
        else:
            self._canvas.drawText(pos=(0,0), color=borderColor ,text="( )")
            self._canvas.drawText(pos=(1,0), color=color ,text=" ")

    def _pressEvent(self):
        # Uncheck the radio already checked;
        for radio in TTkRadioButton._radioLists[self._name]:
            if self != radio != None:
                if radio._checked:
                    radio._checked = False
                    radio.update()
        self._checked = True
        self.update()

    def mousePressEvent(self, evt):
        self._pressEvent()
        return True

    def keyEvent(self, evt):
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            self._pressEvent()
            return True
        return False
