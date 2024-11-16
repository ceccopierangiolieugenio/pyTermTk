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

__all__ = ['TTkLogViewer']

import os
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSlot
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class _TTkLogViewer(TTkAbstractScrollView):
    __slots__ = ('_messages', '_cwd', '_follow')
    def __init__(self, *,
                 follow:bool=False,
                 **kwargs) -> None:
        self._cwd = os.getcwd()
        self._messages = [TTkString()]
        self._follow = follow
        super().__init__(**kwargs)
        TTkLog.installMessageHandler(self.loggingCallback)
        self.viewChanged.connect(self._viewChangedHandler)

    @pyTTkSlot()
    def _viewChangedHandler(self):
        self.update()

    def viewFullAreaSize(self) -> tuple[int,int]:
        w = max( m.termWidth() for m in self._messages)
        h = len(self._messages)
        return w , h

    def loggingCallback(self, mode, context, message):
        logType = "NONE"
        if mode == TTkLog.InfoMsg:       logType = TTkString("INFO "   ,TTkColor.fg("#00ff00"))
        elif mode == TTkLog.DebugMsg:    logType = TTkString("DEBUG"   ,TTkColor.fg("#00ffff"))
        elif mode == TTkLog.ErrorMsg:    logType = TTkString("ERROR"   ,TTkColor.fg("#ff0000"))
        elif mode == TTkLog.FatalMsg:    logType = TTkString("FATAL"   ,TTkColor.fg("#ff0000"))
        elif mode == TTkLog.WarningMsg:  logType = TTkString("WARNING ",TTkColor.fg("#ff0000"))
        elif mode == TTkLog.CriticalMsg: logType = TTkString("CRITICAL",TTkColor.fg("#ff0000"))
        self._messages.append(logType+TTkString(f": {context.file}:{context.line} {message}".replace(self._cwd,"_")))
        offx, offy = self.getViewOffsets()
        _,h = self.size()
        if self._follow or offy == len(self._messages)-h-1:
            offy = len(self._messages)-h
        self.viewMoveTo(offx, offy)
        self.viewChanged.emit()
        self.update()

    def paintEvent(self, canvas):
        ox,oy = self.getViewOffsets()
        _,h = self.size()
        for y, message in enumerate(self._messages[oy:oy+h]):
            canvas.drawTTkString(pos=(-ox,y),text=message)

class TTkLogViewer(TTkAbstractScrollArea):
    __slots__ = ('_logView')
    def __init__(self, *,
                 # TTkWidget init
                 parent:TTkWidget=None,
                 visible:bool=True,
                 # TTkLogViewer init
                 follow:bool=False,
                 **kwargs) -> None:
        self._logView = _TTkLogViewer(follow=follow)
        super().__init__(parent=parent, visible=visible, **kwargs)
        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._logView)
