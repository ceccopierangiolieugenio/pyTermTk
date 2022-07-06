#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.string import TTkString
from TermTk.TTkGui.textcursor import TTkTextCursor
from TermTk.TTkGui.textdocument import TTkTextDocument

class TTkTextWrap():
    __slots__ = (
        '_lines', '_textDocument', '_tabSpaces',
        '_lineWrapMode', '_wordWrapMode', '_wrapWidth',
        # Signals
        'wrapChanged'
        )
    def __init__(self, *args, **kwargs):
        # signals
        self.wrapChanged = pyTTkSignal()

        self._lines = [(0,(0,0))]
        self._tabSpaces = 4
        self._wrapWidth     = 80
        self._lineWrapMode = TTkK.NoWrap
        self._wordWrapMode = TTkK.WrapAnywhere
        self.setDocument(kwargs.get('document',TTkTextDocument()))

    def setDocument(self, document):
        self._textDocument = document
        self.rewrap()

    def wrapWidth(self):
        return self._wrapWidth

    def setWrapWidth(self, width):
        self._wrapWidth = width
        self.rewrap()

    def lineWrapMode(self):
        return self._lineWrapMode

    def setLineWrapMode(self, mode):
        self._lineWrapMode = mode
        self.rewrap()

    def wordWrapMode(self):
        return self._wordWrapMode

    def setWordWrapMode(self, mode):
        self._wordWrapMode = mode
        self.rewrap()

    def rewrap(self):
        self._lines = []
        if self._lineWrapMode == TTkK.NoWrap:
            def _process(i,l):
                self._lines.append((i,(0,len(l))))
        else:
            if   self._lineWrapMode == TTkK.WidgetWidth:
                w = self.width()
                if not w: return
            elif self._lineWrapMode == TTkK.FixedWidth:
                w = self._wrapWidth

            def _process(i,l):
                fr = 0
                to = 0
                if not len(l): # if the line is empty append it
                    self._lines.append((i,(0,0)))
                    return
                while len(l):
                    fl = l.tab2spaces(self._tabSpaces)
                    if len(fl) <= w:
                        self._lines.append((i,(fr,fr+len(l))))
                        l=[]
                    else:
                        to = max(1,l.tabCharPos(w,self._tabSpaces))
                        if self._wordWrapMode == TTkK.WordWrap: # Find the index of the first white space
                            s = str(l)
                            newTo = to
                            while newTo and ( s[newTo] != ' ' and s[newTo] != '\t' ): newTo-=1
                            if newTo: to = newTo

                        self._lines.append((i,(fr,fr+to)))
                        l = l.substring(to)
                        fr += to
        for i,l in enumerate(self._textDocument._dataLines):
            _process(i,l)
        self.wrapChanged.emit()


