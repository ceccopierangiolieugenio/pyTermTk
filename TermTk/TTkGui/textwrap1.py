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

__all__ = ['TTkTextWrap']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.string import TTkString
from TermTk.TTkGui.textcursor import TTkTextCursor
from TermTk.TTkGui.textdocument import TTkTextDocument

class TTkTextWrap():
    __slots__ = (
        '_lines', '_textDocument', '_tabSpaces',
        '_wordWrapMode', '_wrapWidth',
        '_enable',
        # Signals
        'wrapChanged'
        )
    def __init__(self, *args, **kwargs):
        # signals
        self.wrapChanged = pyTTkSignal()

        self._enable = False
        self._lines = [(0,(0,0))]
        self._tabSpaces = 4
        self._wrapWidth     = 80
        self._wordWrapMode = TTkK.WrapAnywhere
        self.setDocument(kwargs.get('document',TTkTextDocument()))

    def setDocument(self, document):
        self._textDocument = document
        self.rewrap()

    def disable(self):
        self._enable = False

    def enable(self):
        self._enable = True

    def size(self):
        return len(self._lines)

    def wrapWidth(self):
        return self._wrapWidth

    def setWrapWidth(self, width):
        self._wrapWidth = width
        self.rewrap()

    def wordWrapMode(self):
        return self._wordWrapMode

    def setWordWrapMode(self, mode):
        self._wordWrapMode = mode
        self.rewrap()

    def rewrap(self):
        self._lines = []
        if not self._enable:
            def _process(i,l):
                self._lines.append((i,(0,len(l)+1)))
        else:
            if not (w := self._wrapWidth):
                return

            def _process(i,l:TTkString):
                fr = 0
                to = 0
                if not len(l): # if the line is empty append it
                    self._lines.append((i,(0,0)))
                    return
                while len(l):
                    fl = l.tab2spaces(self._tabSpaces)
                    if fl.termWidth() <= w:
                        self._lines.append((i,(fr,fr+len(l)+1)))
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

    def dataToScreenPosition(self, line, pos):
        for i, (dt, (fr, to)) in enumerate(self._lines):
            if dt == line and fr <= pos <= to:
                l = self._textDocument._dataLines[dt].substring(fr,pos).tab2spaces(self._tabSpaces)
                return l.termWidth(), i
        return 0,0

    def screenToDataPosition(self, x, y):
        dt, (fr, to) = self._lines[y]
        pos = fr+self._textDocument._dataLines[dt].substring(fr,to).tabCharPos(x,self._tabSpaces)
        return dt, pos

    def normalizeScreenPosition(self, x, y):
        '''
        Return the widget position of the closest editable char
        in:
        x,y = widget relative position
        alignRightTab = if true, align the position to the right of the tab space
        return:
        x,y = widget relative position aligned to the close editable char
        '''
        y = max(0,min(y,self.size()-1))
        dt, (fr, to) = self._lines[y]
        x = max(0,x)
        s = self._textDocument._dataLines[dt].substring(fr,to)
        x = s.tabCharPos(x, self._tabSpaces)
        x = s.substring(0,x).tab2spaces(self._tabSpaces).termWidth()
        return x, y
