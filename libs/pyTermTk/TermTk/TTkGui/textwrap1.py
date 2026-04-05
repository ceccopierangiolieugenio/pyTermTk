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
    '''TTkTextWrap:

    Incremental text wrapping helper for :py:class:`TTkTextDocument`.
    It maps document positions to wrapped screen rows and vice versa.
    '''
    __slots__ = (
        '_lines', '_textDocument', '_tabSpaces',
        '_processedLines', '_lineStartY',
        '_checkpoints', '_checkpointStep',
        '_wordWrapMode', '_wrapWidth',
        '_enable',
        '_wrapCache',
        # Signals
        'wrapChanged'
        )
    def __init__(self, document:Optional[TTkTextDocument]=None) -> None:
        '''Create a wrap manager bound to a text document.

        :param document: optional source document; when omitted a new
                         :py:class:`TTkTextDocument` is created.
        :type document: Optional[:py:class:`TTkTextDocument`]
        '''
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
        self._wrapCache: dict = {}
        self._wordWrapMode = TTkK.WrapAnywhere
        if not document:
            document = TTkTextDocument()
        self.setDocument(document)

    def setDocument(self, document:TTkTextDocument) -> None:
        '''Attach a new document and reset wrapping caches.

        :param document: source text document.
        :type document: :py:class:`TTkTextDocument`
        '''
        self._textDocument = document
        self.rewrap()

    def disable(self) -> None:
        '''Disable wrapping and expose each data line as one screen row.'''
        self._enable = False

    def enable(self) -> None:
        '''Enable wrapping according to current width and mode.'''
        self._enable = True

    def size(self) -> int:
        '''Return the estimated wrapped row count.

        :return: wrapped size in screen rows.
        :rtype: int
        '''
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
        '''Return the number of logical data lines in the document.

        :return: document line count.
        :rtype: int
        '''
        return self._textDocument.lineCount()

    def _documentDataLine(self, line:int) -> Optional[TTkString]:
        '''Get one document line through the document thread-safe API.'''
        return self._textDocument.dataLine(line)

    def wrapWidth(self) -> int:
        '''Return the current wrap width in terminal cells.

        :return: wrap width.
        :rtype: int
        '''
        return self._wrapWidth

    def setWrapWidth(self, width:int) -> None:
        '''Set wrap width and trigger a full rewrap.

        :param width: target width in terminal cells.
        :type width: int
        '''
        self._wrapWidth = width
        self.rewrap()

    def wordWrapMode(self) -> TTkK.WrapMode:
        '''Return the active word-wrap mode.

        :return: current wrap mode.
        :rtype: :py:class:`TTkK.WrapMode`
        '''
        return self._wordWrapMode

    def setWordWrapMode(self, mode:TTkK.WrapMode) -> None:
        '''Set the word-wrap mode and invalidate cached wrapping.

        :param mode: new wrap mode.
        :type mode: :py:class:`TTkK.WrapMode`
        '''
        self._wordWrapMode = mode
        self.rewrap()

    def _invalidateAll(self) -> None:
        '''Drop all cached wrapping state and checkpoints.'''
        self._lines = []
        self._processedLines = 0
        self._lineStartY = [0]
        self._checkpoints = [(0,0)]
        self._wrapCache = {}

    def _invalidateFromDataLine(self, line:int):
        '''Invalidate cache from the given data line onward.

        :param line: first logical line to invalidate.
        :type line: int
        '''
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
        self._wrapCache = {k: v for k, v in self._wrapCache.items() if k < line}
        if self._checkpoints[-1] != (line, y):
            self._checkpoints.append((line, y))

    def invalidateFromDataLine(self, line:int, _removed:int=0, _added:int=0) -> None:
        '''Public invalidation entry point used by document change hooks.

        :param line: first changed line in the source document.
        :type line: int
        :param _removed: number of removed lines (currently unused).
        :type _removed: int
        :param _added: number of added lines (currently unused).
        :type _added: int
        '''
        self._invalidateFromDataLine(line)
        self.wrapChanged.emit()

    def _wrapLine(self, dt:int, l:TTkString) -> List[_WrapSlice]:
        '''Wrap one logical line into screen-row slices.

        :param dt: document line index.
        :type dt: int
        :param l: line content.
        :type l: :py:class:`TTkString`
        :return: list of slices as ``(line, (from, to))`` tuples.
        :rtype: List[Tuple[int, Tuple[int, int]]]
        '''
        if dt in self._wrapCache:
            return self._wrapCache[dt]
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
        self._wrapCache[dt] = out
        return out

    def _wrapLineCount(self, l:TTkString) -> int:
        '''Count wrapped rows for a single logical line.

        :param l: line content.
        :type l: :py:class:`TTkString`
        :return: number of wrapped rows.
        :rtype: int
        '''
        return len(self._wrapLine(0, l))

    def _materializeToDataLine(self, line:int) -> None:
        '''Materialize wrapping metadata up to a logical data line.

        :param line: last logical line to materialize.
        :type line: int
        '''
        line = max(0, min(line, self.documentLineCount()-1))
        while self._processedLines <= line and self._processedLines < self.documentLineCount():
            dt = self._processedLines
            if (docLine := self._documentDataLine(dt)) is None:
                break
            rows = len(self._wrapLine(dt, docLine))
            self._processedLines += 1
            self._lineStartY.append(self._lineStartY[-1] + rows)
            if self._processedLines % self._checkpointStep == 0:
                self._checkpoints.append((self._processedLines, self._lineStartY[-1]))

    def _estimateDataLineForScreenY(self, y:int) -> int:
        '''Estimate a logical line index for a target screen row.

        :param y: target screen row.
        :type y: int
        :return: estimated logical line index.
        :rtype: int
        '''
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
        '''Materialize wrapping metadata so that row ``y`` is addressable.

        :param y: target screen row.
        :type y: int
        '''
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
            if (docLine := self._documentDataLine(dt)) is None:
                break
            rows = len(self._wrapLine(dt, docLine))
            self._processedLines += 1
            self._lineStartY.append(self._lineStartY[-1] + rows)
            if self._processedLines % self._checkpointStep == 0:
                self._checkpoints.append((self._processedLines, self._lineStartY[-1]))

    def ensureScreenRows(self, y:int, h:int=1, prefetch:int=0) -> None:
        '''Ensure wrapped metadata exists for a viewport range.

        :param y: first requested screen row.
        :type y: int
        :param h: viewport height.
        :type h: int
        :param prefetch: additional rows to prefetch.
        :type prefetch: int
        '''
        if h <= 0:
            return
        self._materializeToScreenY(y + h - 1 + max(0, prefetch))

    def screenRows(self, y:int, h:int, prefetch:int=0) -> List[_WrapSlice]:
        '''Return wrapped slices visible in the requested viewport.

        :param y: first screen row.
        :type y: int
        :param h: number of rows to extract.
        :type h: int
        :param prefetch: optional prefetch budget.
        :type prefetch: int
        :return: wrapped row slices.
        :rtype: List[Tuple[int, Tuple[int, int]]]
        '''
        if h <= 0:
            return []
        y = max(0, y)
        self._materializeToScreenY(y + h - 1 + max(0, prefetch))
        if self._processedLines <= 0:
            return []

        lastRow = max(0, self._lineStartY[-1]-1)
        y = min(y, lastRow)
        line = bisect_right(self._lineStartY, y) - 1
        line = max(0, min(line, self._processedLines-1))
        lineY = self._lineStartY[line]
        out: List[_WrapSlice] = []

        while len(out) < h and line < self._processedLines:
            if (docLine := self._documentDataLine(line)) is None:
                break
            ranges = self._wrapLine(line, docLine)
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
        '''Invalidate every wrapping cache and emit ``wrapChanged``.'''
        self._invalidateAll()
        self.wrapChanged.emit()

    def dataToScreenPosition(self, line:int, pos:int) -> Tuple[int, int]:
        '''Map a document position to wrapped screen coordinates.

        :param line: logical line index.
        :type line: int
        :param pos: character position in the logical line.
        :type pos: int
        :return: ``(x, y)`` wrapped screen coordinates.
        :rtype: Tuple[int, int]
        '''
        docLines = self.documentLineCount()
        line = min(line, docLines-1)
        if line < 0 :
            return 0, 0
        self._materializeToDataLine(line)
        if line >= self._processedLines:
            return 0, max(0, self.size()-1)
        y1 = self._lineStartY[line]
        if (docLine := self._documentDataLine(line)) is None:
            return 0, y1
        ranges = self._wrapLine(line, docLine)
        for i, (dt, (fr, to)) in enumerate(ranges):
            if dt == line and fr <= pos <= to:
                if (docLineDt := self._documentDataLine(dt)) is None:
                    return 0, y1
                l = docLineDt.substring(fr,pos).tab2spaces(self._tabSpaces)
                return l.termWidth(), y1+i
        return 0, y1

    def screenToDataPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Map wrapped screen coordinates to a document position.

        :param x: horizontal screen coordinate.
        :type x: int
        :param y: vertical screen coordinate.
        :type y: int
        :return: ``(line, pos)`` document position.
        :rtype: Tuple[int, int]
        '''
        self._materializeToScreenY(y)
        if self._processedLines <= 0:
            return 0, 0
        y = max(0, min(y, self._lineStartY[-1]-1))
        dt = max(0, min(bisect_right(self._lineStartY, y)-1, self._processedLines-1))
        lineY = self._lineStartY[dt]
        if (docLine := self._documentDataLine(dt)) is None:
            return 0, 0
        ranges = self._wrapLine(dt, docLine)
        idx = max(0, min(y-lineY, len(ranges)-1))
        _, (fr, to) = ranges[idx]
        pos = fr+docLine.substring(fr,to).tabCharPos(x,self._tabSpaces)
        return dt, pos

    def normalizeScreenPosition(self, x:int, y:int) -> Tuple[int, int]:
        '''Snap a screen position to the nearest editable character cell.

        :param x: horizontal widget-relative coordinate.
        :type x: int
        :param y: vertical widget-relative coordinate.
        :type y: int
        :return: normalized ``(x, y)`` screen position.
        :rtype: Tuple[int, int]
        '''
        self._materializeToScreenY(y)
        if self._processedLines <= 0:
            return 0, 0
        y = max(0,min(y,self._lineStartY[-1]-1))
        dt = max(0, min(bisect_right(self._lineStartY, y)-1, self._processedLines-1))
        lineY = self._lineStartY[dt]
        if (docLine := self._documentDataLine(dt)) is None:
            return 0, y
        ranges = self._wrapLine(dt, docLine)
        idx = max(0, min(y-lineY, len(ranges)-1))
        _, (fr, to) = ranges[idx]
        x = max(0,x)
        s = docLine.substring(fr,to)
        x = s.tabCharPos(x, self._tabSpaces)
        x = s.substring(0,x).tab2spaces(self._tabSpaces).termWidth()
        return x, y
