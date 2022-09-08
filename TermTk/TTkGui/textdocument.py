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

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.string import TTkString

class TTkTextDocument():
    class _snapDiff():
        '''
        Doc:
                  0       f1      t1      l1
         Base:    |--------aaaaaaaa-------|
         Mod:     |--------bbbbb   -------|
                  0       f2   t2         l2 = l1 - (t1-f1) + (t2-f2)
        '''
        __slots__ = ('_slice1','_slice2', '_f1', '_t1', '_f2', '_t2', '_cursor1', '_cursor2')
        def __init__(self, doc1, doc2, cursor1, cursor2, f1, f2, t1, t2):
            self._slice1 = doc1
            self._slice2 = doc2
            self._cursor1 = cursor1
            self._cursor2 = cursor2
            self._f1 = f1
            self._f2 = f2
            self._t1 = t1
            self._t2 = t2

    class _snapshot():
        __slots__ = ('_lines', '_cursor')
        def __init__(self, lines, cursor):
            self._lines  = lines
            self._cursor = cursor

    __slots__ = (
        '_dataLines', '_diffs', '_snapshots', '_snapshotId', '_changed',
        # Signals
        'contentsChange', 'contentsChanged',
        'cursorPositionChanged'
        )
    def __init__(self, *args, **kwargs):
        from TermTk.TTkGui.textcursor import TTkTextCursor
        self.cursorPositionChanged = pyTTkSignal(TTkTextCursor)
        self.contentsChange = pyTTkSignal(int,int,int) # int line, int linesRemoved, int linesAdded
        self.contentsChanged = pyTTkSignal()
        text =  kwargs.get('text'," ")
        self._dataLines = [TTkString(t) for t in text.split('\n')]
        self._changed = False
        self._diffs = []
        self._snapshots = []
        self._snapshotId = -1

    def changed(self):
        return self._changed

    def lineCount(self):
        return len(self._dataLines)

    def characterCount(self):
        return sum([len[x] for x in self._dataLines])+self.lineCount()

    def setText(self, text):
        self._dataLines = [TTkString(t) for t in text.split('\n')]
        self._changed = True
        self.contentsChanged.emit()
        self.contentsChange.emit(0,0,len(self._dataLines))

    def appendText(self, text):
        if type(text) == str:
            text = TTkString() + text
        oldLines = len(self._dataLines)
        self._dataLines += text.split('\n')
        self._changed = True
        self.contentsChanged.emit()
        self.contentsChange.emit(oldLines,0,len(self._dataLines)-oldLines)

    def hasSnapshots(self):
        return len(self._snapshots)>0

    def saveSnapshot(self, cursor):
        # TTkLog.debug(f"snaps: {len(self._snapshots)} id:{self._snapshotId}")
        # TTkLog.debug(f"Cur: {self._dataLines[0]}")
        if not self._changed:
            return
        self._changed = False
        self._snapshots = self._snapshots[:max(0,self._snapshotId+1)]
        self._snapshotId = len(self._snapshots)
        self._snapshots.append(
                TTkTextDocument._snapshot(self._dataLines.copy(), cursor))
        # for i,s in enumerate(self._snapshots):
        #     TTkLog.debug(f"{i=} {s._lines[0]}")

    def restoreSnapshot(self, inc=0):
        # TTkLog.debug(f"R: snaps: {len(self._snapshots)} id:{self._snapshotId}")
        self._snapshotId = min((max(-1,self._snapshotId+inc)),len(self._snapshots))
        if self._snapshots and 0 <= self._snapshotId < len(self._snapshots):
            snap = self._snapshots[self._snapshotId]
            self._dataLines = snap._lines.copy()
            self.contentsChanged.emit()
            return snap._cursor
        return None

    def restoreSnapshotPrev(self):
        return self.restoreSnapshot(-1)

    def restoreSnapshotNext(self):
        return self.restoreSnapshot(+1)


