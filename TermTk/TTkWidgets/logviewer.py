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
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkWidgets.widget import *
from TermTk.TTkTemplates.color import TColor
from TermTk.TTkTemplates.text  import TText

class TTkLogViewer(TTkWidget):
    __slots__ = ('_color', '_text', '_messages', '_cwd')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkLabel' )
        self._messages = []
        self._cwd = os.getcwd()
        TTkLog.installMessageHandler(self.loggingCallback)


    def loggingCallback(self, mode, context, message):
        logType = "NONE"
        if mode == TTkLog.InfoMsg:       logType = "INFO"
        elif mode == TTkLog.DebugMsg:  logType = "DEBUG"
        elif mode == TTkLog.WarningMsg:  logType = "WARNING"
        elif mode == TTkLog.CriticalMsg: logType = "CRITICAL"
        elif mode == TTkLog.FatalMsg:    logType = "FATAL"
        elif mode == TTkLog.ErrorMsg:    logType = "ERROR"
        self._messages.append(f"{logType}: {context.file}:{context.line} {message}".replace(self._cwd,"_"))
        self.update()

    def paintEvent(self):
        y = 0
        _,h = self.size()
        offset = len(self._messages)-h
        if offset<0: offset = 0
        for message in self._messages[offset:]:
            self._canvas.drawText(pos=(0,y),text=message)
            y+=1



