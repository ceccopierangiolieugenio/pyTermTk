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

class TTkCheckbox(TTkWidget):
    __slots__ = ('_checked', 'clicked', 'stateChanged')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkCheckbox' )
        # Define Signals
        self.stateChanged = pyTTkSignal(int)
        self.clicked = pyTTkSignal(bool)
        self._checked = kwargs.get('checked', False )
        self.setMinimumSize(3, 1)
        self.setMaximumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def checkState(self):
        if self._checked:
            return TTkK.Checked
        else:
            return TTkK.Unchecked

    def setCheckState(self, state):
        self._checked = state == TTkK.Checked
        self.update()

    def paintEvent(self):
        if self.hasFocus():
            borderColor = TTkCfg.theme.checkboxBorderColorFocus
            color       = TTkCfg.theme.checkboxContentColorFocus
        else:
            borderColor = TTkCfg.theme.checkboxBorderColor
            color       = TTkCfg.theme.checkboxContentColor
        if self._checked:
            self._canvas.drawText(pos=(0,0), color=borderColor ,text="[ ]")
            self._canvas.drawText(pos=(1,0), color=color ,text="X")
        else:
            self._canvas.drawText(pos=(0,0), color=borderColor ,text="[ ]")
            self._canvas.drawText(pos=(1,0), color=color ,text=" ")

    def _pressEvent(self):
        self._checked = not self._checked
        self.clicked.emit(self._checked)
        self.stateChanged.emit(self.checkState())
        self.update()
        return True

    def mousePressEvent(self, evt):
        self._pressEvent()
        return True

    def keyEvent(self, evt):
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            self._pressEvent()
            return True
        return False
