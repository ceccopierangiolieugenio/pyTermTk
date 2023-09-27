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

__all__ = ['TTkTerminal']

import os, pty, threading
import struct, fcntl, termios

from dataclasses import dataclass

import re
from select import select
from TermTk.TTkCore.canvas import TTkCanvas


from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkWidgets.TTkTerminal.terminalview import TTkTerminalView

from .terminalview_CSI_DEC import _TTkTerminal_CSI_DEC

class TTkTerminal(TTkAbstractScrollArea):
    __slots__ = ('_terminalView',
                 # Exported methods
                 'runShell',
                 # Exported Signals
                 'titleChanged', 'bell', 'terminalClosed')
    def __init__(self, *args, **kwargs):
        TTkAbstractScrollArea.__init__(self, *args, **kwargs)
        if 'parent' in kwargs: kwargs.pop('parent')
        self._terminalView = TTkTerminalView(*args, **kwargs)
        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._terminalView)

        # Export Methods
        self.runShell = self._terminalView.runShell

        # Export Signals
        self.titleChanged = self._terminalView.titleChanged
        self.bell = self._terminalView.bell
        self.terminalClosed = pyTTkSignal(TTkTerminal)
        self._terminalView.closed.connect(lambda : self.terminalClosed.emit(self))

    def close(self):
        self._terminalView.close()
        return super().close()

