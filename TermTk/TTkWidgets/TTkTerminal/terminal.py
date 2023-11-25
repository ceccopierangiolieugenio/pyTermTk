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

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkWidgets.TTkTerminal.terminalview import TTkTerminalView

class TTkTerminal(TTkAbstractScrollArea):
    '''TTkTerminal

    This is a terminal emulator fot TermTk

    .. warning::
        This is an Alpha feature, it is not optimized and the API definition may change in the future

    '''
    __slots__ = ('_terminalView',
                 # Exported methods
                 'termWrite', 'termSize',
                 # Exported Signals
                 'titleChanged', 'bell', 'terminalClosed', 'textSelected',
                 'termData', 'termResized')
    def __init__(self, *args, **kwargs):
        TTkAbstractScrollArea.__init__(self, *args, **kwargs)
        if 'parent' in kwargs: kwargs.pop('parent')
        self._terminalView = TTkTerminalView(*args, **kwargs)
        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._terminalView)

        # Export Methods
        self.termSize  = self._terminalView.termSize
        self.termWrite = self._terminalView.termWrite

        # Export Signals
        self.bell         = self._terminalView.bell
        self.termData     = self._terminalView.termData
        self.termResized  = self._terminalView.termResized
        self.titleChanged = self._terminalView.titleChanged
        self.textSelected = self._terminalView.textSelected

        self.terminalClosed = pyTTkSignal(TTkTerminal)
        self._terminalView.terminalClosed.connect(lambda : self.terminalClosed.emit(self))

    def close(self):
        self._terminalView.close()
        return super().close()

