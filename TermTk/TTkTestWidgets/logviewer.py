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

import os
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkTemplates.color import TColor
from TermTk.TTkTemplates.text  import TText
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class _TTkLogViewer(TTkAbstractScrollView):
    __slots__ = ('_color', '_text', '_messages', '_cwd')
    def __init__(self, *args, **kwargs):
        TTkAbstractScrollView.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkLogViewer' )
        self._messages = [""]
        self._cwd = os.getcwd()
        TTkLog.installMessageHandler(self.loggingCallback)
        self.viewChanged.connect(self._viewChangedHandler)

    @pyTTkSlot()
    def _viewChangedHandler(self):
        self.update()

    def viewFullAreaSize(self) -> (int, int):
        w = max([ len(m) for m in self._messages])
        h = len(self._messages)
        return w , h

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def loggingCallback(self, mode, context, message):
        logType = "NONE"
        if mode == TTkLog.InfoMsg:       logType = "INFO "
        elif mode == TTkLog.DebugMsg:    logType = "DEBUG"
        elif mode == TTkLog.ErrorMsg:    logType = "ERROR"
        elif mode == TTkLog.FatalMsg:    logType = "FATAL"
        elif mode == TTkLog.WarningMsg:  logType = "WARNING "
        elif mode == TTkLog.CriticalMsg: logType = "CRITICAL"
        self._messages.append(f"{logType}: {context.file}:{context.line} {message}".replace(self._cwd,"_"))
        offx, offy = self.getViewOffsets()
        _,h = self.size()
        if offy == len(self._messages)-h-1:
            offy = len(self._messages)-h
        self.viewMoveTo(offx, offy)
        self.viewChanged.emit()
        self.update()

    def paintEvent(self):
        ox,oy = self.getViewOffsets()
        _,h = self.size()
        offset = max(0,ox)
        for y, message in enumerate(self._messages[oy:]):
            self._canvas.drawText(pos=(0,y),text=message[ox:])
            c = TTkColor.RST
            if   message.startswith("INFO ") : c = TTkColor.fg("#00ff00")
            elif message.startswith("DEBUG") : c = TTkColor.fg("#00ffff")
            elif message.startswith("ERROR") : c = TTkColor.fg("#ff0000")
            elif message.startswith("FATAL") : c = TTkColor.fg("#ff0000")
            self._canvas.drawText(pos=(-ox,y),text=message[:5], color=c)

class TTkLogViewer(TTkAbstractScrollArea):
    __slots__ = ('_logView')
    def __init__(self, *args, **kwargs):
        TTkAbstractScrollArea.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkLogViewer' )
        if 'parent' in kwargs: kwargs.pop('parent')
        self._logView = _TTkLogViewer(*args, **kwargs)
        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._logView)
