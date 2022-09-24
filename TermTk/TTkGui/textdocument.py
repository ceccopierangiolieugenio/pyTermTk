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
    '''
        Undo,Redo Logic

        Old:
            _snapshotId: = last saved/undo/redo state
                                   3 = doc4
            _snapshots:
                [doc1, doc2, doc3, doc4, doc5, doc6, . . .]

        New:
            SnapshotId:
                              2
            Snapshots:                  _lastSnap     _dataLines (unstaged)
                ╒═══╕ ╒═══╕ ╒═══╕ ╒═══╕ ╒═══╕         ╒═══╕
                │ 0 │ │ 1 │ │ 2 │ │ 3 │ │ 4 │         │ 5 │
                └───┘ └───┘ └───┘ └───┘ └───┘         └───┘
            Cursors:
                 c0,   c1,   c2,   c3,   c4 = _lastCursor
            Diffs:
                [   d01,  d12,  d23,  d34   ] = Forward  Diffs
                [   d10,  d21,  d32,  d43   ] = Backward Diffs
            Slices: = common txt slices between snapshots
                [   s01,  s12,  s23,  s34   ]

            Data Structure
                        ╔═══════════════╗                         ╔═══════════════╗
                        ║   Snapshot B  ║          ┌─────────────>║   Snapshot C  ║
                        ╟───────────────╢          │              ╟───────────────╢
                        ║ _nextDiff     ║──────┐   │              ║ _nextDiff     ║───> Next snapshot
                    ┌───║ _prevDiff     ║      │   │          ┌───║ _prevDiff     ║  or Null if at the end
                    │   ╚═══════════════╝      │   │          │   ╚═══════════════╝
                    V              A           V   │          V
                ╔═══════════════╗  │  ╔═══════════════╗   ╔═══════════════╗
                ║   Diff B->A   ║  │  ║   Diff B->C   ║   ║   Diff C->B   ║
                ╟───────────────╢  │  ╟───────────────╢   ╟───────────────╢
                ║ slice = txtBA ║  │  ║ slice = txtBC ║   ║ slice = txtBA ║
                ║ snap          ║  │  ║ snap          ║   ║ snap          ║
                ╚═══════════════╝  │  ╚═══════════════╝   ╚═══════════════╝
                                   │                             │
                                   └─────────────────────────────┘
    '''
    class _snapDiff():
        '''
        Doc:
                  0<--i1-->f1      t1<--i2-->l1
         Base:    |---------aaaaaaaa---------|
         Mod:     |---------bbbbb   ---------|
                  0        f2   t2           l2 = l1 - (t1-f1) + (t2-f2)
        '''
        __slots__ = ('_slice', '_i1', '_i2', '_snap')
        def __init__(self, txt, i1, i2, snap):
            # The text slice required to change the current snap to the next one
            self._slice = txt
            # i1 are the num. of common lines from the starting between the 2 snaps
            self._i1 = i1
            # i1 are the num. of common lines from the ending between the 2 snaps
            self._i2 = i2
            # This is the link to the next _snapshot structure
            self._snap = snap

    class _snapshot():
        __slots__ = (
                '_cursor',
                '_nextDiff', '_prevDiff')
        def __init__(self, cursor, nextDiff, prevDiff):
            self._cursor = cursor
            self._nextDiff = nextDiff
            self._prevDiff = prevDiff

        def getNextSnap(self, lines):
            return self._getSnap(lines, self._nextDiff)
        def getPrevSnap(self, lines):
            return self._getSnap(lines, self._prevDiff)

        def _getSnap(self, lines, d):
            i1 = d._i1
            i2 = d._i2
            if d._i2 == 0:
                lines[d._i1:] = d._slice
            else:
                lines[d._i1:-d._i2] = d._slice
            return d._snap


    __slots__ = (
        '_dataLines', '_changed',
        '_snap',
        '_lastSnap', '_lastCursor',
        # Signals
        'contentsChange', 'contentsChanged',
        'cursorPositionChanged',
        'undoAvailable', 'redoAvailable'
        )
    def __init__(self, *args, **kwargs):
        from TermTk.TTkGui.textcursor import TTkTextCursor
        self.cursorPositionChanged = pyTTkSignal(TTkTextCursor)
        self.contentsChange = pyTTkSignal(int,int,int) # int line, int linesRemoved, int linesAdded
        self.contentsChanged = pyTTkSignal()
        self.undoAvailable = pyTTkSignal(bool)
        self.redoAvailable = pyTTkSignal(bool)
        text =  kwargs.get('text'," ")
        self._dataLines = [TTkString(t) for t in text.split('\n')]
        self._changed = False
        self._lastSnap = self._dataLines.copy()
        self._lastCursor = TTkTextCursor(document=self)
        self._snap = TTkTextDocument._snapshot(self._lastCursor, None, None)

    def changed(self):
        return self._changed

    def lineCount(self):
        return len(self._dataLines)

    def characterCount(self):
        return sum([len[x] for x in self._dataLines])+self.lineCount()

    def setText(self, text):
        self._dataLines = [TTkString(t) for t in text.split('\n')]
        self._changed = False
        self._lastSnap = self._dataLines.copy()
        self._snap = TTkTextDocument._snapshot(self._lastCursor, None, None)
        self.contentsChanged.emit()
        self.contentsChange.emit(0,0,len(self._dataLines))

    def appendText(self, text):
        if type(text) == str:
            text = TTkString() + text
        oldLines = len(self._dataLines)
        self._dataLines += text.split('\n')
        self._changed = False
        self._lastSnap = self._dataLines.copy()
        self._snap = TTkTextDocument._snapshot(self._lastCursor, None, None)
        self.contentsChanged.emit()
        self.contentsChange.emit(oldLines,0,len(self._dataLines)-oldLines)

    def isUndoAvailable(self):
        return self._snap and self._snap._prevDiff

    def isRedoAvailable(self):
        return self._snap and self._snap._nextDiff

    def hasSnapshots(self):
        return self._snap is not None

    def saveSnapshot(self, cursor):
        docA = self._lastSnap
        docB = self._dataLines

        i1 = min(len(docA),len(docB))
        for i,(a,b) in enumerate(zip(docA,docB)):
            if a!=b:
                i1 = i
                break

        i2 = min(len(docA),len(docB))-i1
        for i,(a,b) in enumerate(zip(reversed(docA[i1:]),reversed(docB[i1:]))):
            if a!=b:
                i2 = i
                break

        if i2 == 0:
            sliceA = docA[i1:]
            sliceB = docB[i1:]
        else:
            sliceA = docA[i1:-i2]
            sliceB = docB[i1:-i2]

        if sliceA or sliceB:
            # current snapshot
            # is becoming the previous one
            snapA  = self._snap
            diffBA = TTkTextDocument._snapDiff(sliceA, i1, i2, snapA)
            snapB  = TTkTextDocument._snapshot(cursor, None, diffBA)
            diffAB = TTkTextDocument._snapDiff(sliceB, i1, i2, snapB)
            snapA._nextDiff = diffAB
            self._snap = snapB
        else:
            self._snap._cursor = cursor

        self._changed = False
        self._lastSnap = self._dataLines.copy()
        self._lastCursor = cursor
        self.undoAvailable.emit(self.isUndoAvailable())
        self.redoAvailable.emit(self.isRedoAvailable())
        # ddd(self)

    def _restoreSnapshotDiff(self, next=True):
        if ( not self._snap or
            (    next and not self._snap._nextDiff) or
            (not next and not self._snap._prevDiff) ):
            return None

        if next:
            self._snap = self._snap.getNextSnap(self._dataLines)
        else:
            self._snap = self._snap.getPrevSnap(self._dataLines)

        self._lastSnap = self._dataLines.copy()
        self._lastCursor = self._snap._cursor.copy()

        self.contentsChanged.emit()
        self.undoAvailable.emit(self.isUndoAvailable())
        self.redoAvailable.emit(self.isRedoAvailable())
        return self._snap._cursor

    def restoreSnapshotPrev(self):
        return self._restoreSnapshotDiff(False)

    def restoreSnapshotNext(self):
        return self._restoreSnapshotDiff(True)


