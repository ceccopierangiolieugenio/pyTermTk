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

from bisect import bisect_right
from typing import List, Optional, Tuple

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.string import TTkString
from TermTk.TTkGui.textdocument import TTkTextDocument

_WrapSlice = Tuple[int, Tuple[int, int]]
_Checkpoint = Tuple[int, int]

class TTkTextWrap():
    __slots__ = (
        '_lines', '_textDocument', '_tabSpaces',
        '_processedLines', '_lineStartY',
        '_checkpoints', '_checkpointStep',
        '_wordWrapMode', '_wrapWidth',
        '_enable',
        # Signals
        'wrapChanged'
        )
    def __init__(self, document:Optional[TTkTextDocument]=None) -> None:
        # signals
        self.wrapChanged = pyTTkSignal()

        self._enable: bool = False
        self._lines: List[_WrapSlice] = [(0,(0,0))]
        self._processedLines: int = 0
        self._lineStartY: List[int] = [0]
        self._checkpointStep: int = 256
        self._checkpoints: List[_Checkpoint] = [(0,0)] # (processedDataLine, wrappedRows)
        self._tabSpaces: int = 4
        self._wrapWidth: int = 80
        self._wordWrapMode = TTkK.WrapAnywhere
        if not document:
            document = TTkTextDocument()
        self.setDocument(document)

    def setDocument(self, document:TTkTextDocument) -> None:
        self._textDocument = document
        self.rewrap()

    def disable(self) -> None:
        self._enable = False

    def enable(self) -> None:
        self._enable = True

    def size(self) -> int:
        processedRows = self._lineStartY[-1] if self._lineStartY else 0
        rem = max(0, self.documentLineCount() - self._processedLines)
        if rem == 0:
            return processedRows
        if self._processedLines <= 0:
            # Lower bound before any sample is collected.
            return processedRows + rem
        avgRowsPerLine = processedRows / self._processedLines
        return processedRows + max(rem, int(rem * avgRowsPerLine))

    def documentLineCount(self) -> int:
        return len(self._textDocument._dataLines)

    def wrapWidth(self) -> int:
        return self._wrapWidth

    def setWrapWidth(self, width:int) -> None:
        self._wrapWidth = width
        self.rewrap()

    def wordWrapMode(self) -> TTkK.WordWrapMode:
        return self._wordWrapMode

    def setWordWrapMode(self, mode:TTkK.WordWrapMode) -> None:
        self._wordWrapMode = mode
        self.rewrap()

    def _invalidateAll(self) -> None:
        self._lines = []
        self._processedLines = 0
        self._lineStartY = [0]
        self._checkpoints = [(0,0)]

    def _invalidateFromDataLine(self, line:int):
        line = max(0, min(line, self.documentLineCount()))
        if line == 0:
            self._invalidateAll()
            return
        if line >= self._processedLines:
            return
        y = self._lineStartY[line]
        self._lines = []
        self._processedLines = line
        self._lineStartY = self._lineStartY[:line+1]
        idx = bisect_right(self._checkpoints, (line, 10**18))
        self._checkpoints = self._checkpoints[:idx]
        if self._checkpoints[-1] != (line, y):
            self._checkpoints.append((line, y))

    def invalidateFromDataLine(self, line:int, _removed:int=0, _added:int=0) -> None:
        self._invalidateFromDataLine(line)
        self.wrapChanged.emit()

    def _wrapLine(self, dt:int, l:TTkString) -> List[_WrapSlice]:
        out: List[_WrapSlice] = []
        if not self._enable:
            out.append((dt,(0,len(l)+1)))
            return out

        w = self._wrapWidth
        if w <= 0:
            out.append((dt,(0,0)))
            return out

        fr = 0
        cur = l
        if not len(cur): # if the line is empty append it
            out.append((dt,(0,0)))
            return out
        while len(cur):
            fl = cur.tab2spaces(self._tabSpaces)
            if fl.termWidth() <= w:
                out.append((dt,(fr,fr+len(cur)+1)))
                break
            to = max(1,cur.tabCharPos(w,self._tabSpaces))
            if self._wordWrapMode == TTkK.WordWrap: # Find the index of the first white space
                s = str(cur)
                newTo = to
                while newTo and ( s[newTo] != ' ' and s[newTo] != '\t' ):
                    newTo -= 1
                if newTo:
                    to = newTo
            out.append((dt,(fr,fr+to)))
            cur = cur.substring(to)
            fr += to
        return out

    def _wrapLineCount(self, l:TTkString) -> int:
        if not self._enable:
            return 1

        w = self._wrapWidth
        if w <= 0:
            return 1

        cur = l
        if not len(cur):
            return 1

        cnt = 0
        while len(cur):
            fl = cur.tab2spaces(self._tabSpaces)
            if fl.termWidth() <= w:
                cnt += 1
                break
            to = max(1,cur.tabCharPos(w,self._tabSpaces))
            if self._wordWrapMode == TTkK.WordWrap:
                s = str(cur)
                newTo = to
                while newTo and ( s[newTo] != ' ' and s[newTo] != '\t' ):
                    newTo -= 1
                if newTo:
                    to = newTo
            cnt += 1
            cur = cur.substring(to)
        return cnt

    def _materializeToDataLine(self, line:int) -> None:
        line = max(0, min(line, self.documentLineCount()-1))
        while self._processedLines <= line and self._processedLines < self.documentLineCount():
            dt = self._processedLines
            rows = self._wrapLineCount(self._textDocument._dataLines[dt])
            self._processedLines += 1
            self._lineStartY.append(self._lineStartY[-1] + rows)
            if self._processedLines % self._checkpointStep == 0:
                self._checkpoints.append((self._processedLines, self._lineStartY[-1]))

    def _estimateDataLineForScreenY(self, y:int) -> int:
        y = max(0, y)
        if self._processedLines <= 0 or not self._checkpoints:
            return min(y, self.documentLineCount()-1)

        # Use processed checkpoints as anchors then interpolate with observed avg rows/line.
        yValues = [cp[1] for cp in self._checkpoints]
        idx = bisect_right(yValues, y) - 1
        idx = max(0, idx)
        baseLine, baseY = self._checkpoints[idx]
        avgRowsPerLine = max(1.0, self._lineStartY[-1] / max(1, self._processedLines))
        deltaRows = max(0, y - baseY)
        estLine = baseLine + int(deltaRows / avgRowsPerLine)
        return max(0, min(estLine, self.documentLineCount()-1))

    def _materializeToScreenY(self, y:int) -> None:
        y = max(0, y)
        # If requested row is far away, use checkpoints to estimate a nearby data-line anchor.
        # This does not skip exact wrapping, but it provides a stable and cheap hint path used
        # by scrollbar-sized jumps and can be leveraged by future sparse materialization.
        if y > len(self._lines):
            estLine = self._estimateDataLineForScreenY(y)
            if estLine > self._processedLines:
                # Cap speculative forward materialization to avoid large synchronous spikes.
                self._materializeToDataLine(min(estLine, self._processedLines + self._checkpointStep))
        while self._lineStartY[-1] <= y and self._processedLines < self.documentLineCount():
            dt = self._processedLines
            rows = self._wrapLineCount(self._textDocument._dataLines[dt])
            self._processedLines += 1
            self._lineStartY.append(self._lineStartY[-1] + rows)
            if self._processedLines % self._checkpointStep == 0:
                self._checkpoints.append((self._processedLines, self._lineStartY[-1]))

    def ensureScreenRows(self, y:int, h:int=1, prefetch:int=0) -> None:
        if h <= 0:
            return
        self._materializeToScreenY(y + h - 1 + max(0, prefetch))

    def screenRows(self, y:int, h:int, prefetch:int=0) -> List[_WrapSlice]:
        if h <= 0:
            return []
        y = max(0, y)
        self.ensureScreenRows(y, h, prefetch=prefetch)
        if self._processedLines <= 0:
            return []

        lastRow = max(0, self._lineStartY[-1]-1)
        y = min(y, lastRow)
        line = bisect_right(self._lineStartY, y) - 1
        line = max(0, min(line, self._processedLines-1))
        lineY = self._lineStartY[line]
        out: List[_WrapSlice] = []

        while len(out) < h and line < self._processedLines:
            ranges = self._wrapLine(line, self._textDocument._dataLines[line])
            start = max(0, y-lineY)
            for i in range(start, len(ranges)):
                out.append(ranges[i])
                if len(out) >= h:
                    break
            lineY += len(ranges)
            y = lineY
            line += 1

        # Keep a small compatibility cache of the last extracted rows.
        self._lines = out
        return out

    def rewrap(self) -> None:
        self._invalidateAll()
        self.wrapChanged.emit()

    def dataToScreenPosition(self, line:int, pos:int) -> Tuple[int, int]:
        if line < 0:
            return 0, 0
        self._materializeToDataLine(line)
        if line >= self._processedLines:
            return 0, max(0, self.size()-1)
        y1 = self._lineStartY[line]
        ranges = self._wrapLine(line, self._textDocument._dataLines[line])
        for i, (dt, (fr, to)) in enumerate(ranges):
            if dt == line and fr <= pos <= to:
                l = self._textDocument._dataLines[dt].substring(fr,pos).tab2spaces(self._tabSpaces)
                return l.termWidth(), y1+i
        return 0, y1

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        self._materializeToScreenY(y)
        if self._processedLines <= 0:
            return 0, 0
        y = max(0, min(y, self._lineStartY[-1]-1))
        dt = max(0, min(bisect_right(self._lineStartY, y)-1, self._processedLines-1))
        lineY = self._lineStartY[dt]
        ranges = self._wrapLine(dt, self._textDocument._dataLines[dt])
        idx = max(0, min(y-lineY, len(ranges)-1))
        _, (fr, to) = ranges[idx]
        pos = fr+self._textDocument._dataLines[dt].substring(fr,to).tabCharPos(x,self._tabSpaces)
        return dt, pos

    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''
        Return the widget position of the closest editable char
        in:
        x,y = widget relative position
        alignRightTab = if true, align the position to the right of the tab space
        return:
        x,y = widget relative position aligned to the close editable char
        '''
        self._materializeToScreenY(y)
        if self._processedLines <= 0:
            return 0, 0
        y = max(0,min(y,self._lineStartY[-1]-1))
        dt = max(0, min(bisect_right(self._lineStartY, y)-1, self._processedLines-1))
        lineY = self._lineStartY[dt]
        ranges = self._wrapLine(dt, self._textDocument._dataLines[dt])
        idx = max(0, min(y-lineY, len(ranges)-1))
        _, (fr, to) = ranges[idx]
        x = max(0,x)
        s = self._textDocument._dataLines[dt].substring(fr,to)
        x = s.tabCharPos(x, self._tabSpaces)
        x = s.substring(0,x).tab2spaces(self._tabSpaces).termWidth()
        return x, y
