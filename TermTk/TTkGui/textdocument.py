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

__all__ = ['TTkTextDocument']

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
                  0         i1      12
         Base:    |---------aaaaaaaa---------|
         Mod:     |---------bbbbb   ---------|
                  0         slice
        '''
        __slots__ = ('_slice', '_i1', '_i2', '_snap')
        def __init__(self, txt, i1, i2, snap):
            # The text slice required to change the current snap to the next one
            self._slice = txt
            # Starting position of the slice to be removed
            self._i1 = i1
            # Ending position of the slice to be removed
            self._i2 = i2
            # This is the link to the next _snapshot structure
            self._snap = snap

    class _snapshot():
        _lastId = 0
        __slots__ = (
                '_cursor', '_id',
                '_nextDiff', '_prevDiff')
        def __init__(self, cursor, nextDiff, prevDiff):
            self._cursor = cursor
            self._nextDiff = nextDiff
            self._prevDiff = prevDiff
            self._id = TTkTextDocument._snapshot._lastId = self._lastId+1
            # TTkLog.debug(f"{self._id=}")

        def getNextSnap(self, lines):
            return self._getSnap(lines, self._nextDiff)
        def getPrevSnap(self, lines):
            return self._getSnap(lines, self._prevDiff)

        def _getSnap(self, lines, d):
            lines[d._i1:d._i2] = d._slice
            return d._snap


    __slots__ = (
        '_dataLines', '_modified',
        '_snap', '_snapChanged',
        '_lastSnap', '_lastCursor',
        # Signals
        'contentsChange', 'contentsChanged',
        'cursorPositionChanged',
        'undoAvailable', 'redoAvailable', 'undoCommandAdded',
        'modificationChanged'
        )
    def __init__(self, *args, **kwargs):
        from TermTk.TTkGui.textcursor import TTkTextCursor
        self.cursorPositionChanged = pyTTkSignal(TTkTextCursor)
        self.contentsChange = pyTTkSignal(int,int,int) # int line, int linesRemoved, int linesAdded
        self.contentsChanged = pyTTkSignal()
        self.undoAvailable = pyTTkSignal(bool)
        self.redoAvailable = pyTTkSignal(bool)
        self.undoCommandAdded = pyTTkSignal()
        self.modificationChanged = pyTTkSignal(bool)
        text =  kwargs.get('text'," ")
        self._dataLines = [TTkString(t) for t in text.split('\n')]
        self._modified = False
        # Cumulative changes since the lasrt snapshot
        self._snapChanged = None
        self.contentsChange.connect(self._saveSnapChanged)
        self._lastSnap = self._dataLines.copy()
        self._lastCursor = TTkTextCursor(document=self)
        self._snap = TTkTextDocument._snapshot(self._lastCursor, None, None)

    # I need this moethod to cover the math of merging
    # multiples retuen values to be used in the contentsChange
    # method
    #
    #         ┬    ┬         ┬    ┬
    # x2     -│----│-----l2 ┬┼----┼┐
    # x1 l1  ┬┼----┼┐       ││    ││
    #        ││    ││ a1 r2 ││    ││ a2
    #        ││   /┼┘-------││-.  ││
    #    r1  ││  /.│--------└┼-.. ││
    #        ││ /. │         │  \.││-z1
    # y1     └┼'. /┴         ┴-. -┼┘-z2
    # y2     _│. /              \ │
    #         │ /                -┴
    #         ┴'
    #
    # x1 = l1
    # x2 = l2
    # y1 = l1+r1
    # y2 = l2+r2 + (r1-a1)
    # z1 = l1+a1 + (a2-r2)
    # z2 = l2+a2

    @staticmethod
    def _mergeChangesSlices(ch1,ch2):
        l1,r1,a1 = ch1
        l2,r2,a2 = ch2
        x1 = l1
        x2 = l2
        y1 = l1+r1
        y2 = l2+r2 + (r1-a1)
        z1 = l1+a1 + (a2-r2)
        z2 = l2+a2
        a = min(x1,x2)
        b = max(y1,y2) - a
        c = max(z1,z2) - a
        return a,b,c

    @pyTTkSlot(int,int,int)
    def _saveSnapChanged(self,a,b,c):
        if self._snapChanged:
            self._snapChanged = TTkTextDocument._mergeChangesSlices(self._snapChanged,(a,b,c))
        else:
            self._snapChanged = (a,b,c)

    def redo(self): pass

    def setModified(self, m=True):
        if m and self._snap:
            self._snap._nextDiff = None
        if self._modified == m: return
        self._modified = m
        self.modificationChanged.emit(m)

    def undo(self): pass

    def changed(self):
        return self._modified

    def setChanged(self, c):
        self._modified = c
        if c and self._snap:
            self._snap._nextDiff = None

    def lineCount(self):
        return len(self._dataLines)

    def characterCount(self):
        return sum([len[x] for x in self._dataLines])+self.lineCount()

    def setText(self, text):
        remLines = len(self._dataLines)
        self._dataLines = [TTkString(t) for t in text.split('\n')]
        self._modified = False
        self._lastSnap = self._dataLines.copy()
        self._snap = TTkTextDocument._snapshot(self._lastCursor, None, None)
        self.contentsChanged.emit()
        self.contentsChange.emit(0,remLines,len(self._dataLines))
        self._snapChanged = None

    def appendText(self, text):
        if type(text) == str:
            text = TTkString() + text
        oldLines = len(self._dataLines)
        self._dataLines += text.split('\n')
        self._modified = False
        self._lastSnap = self._dataLines.copy()
        self._snap = TTkTextDocument._snapshot(self._lastCursor, None, None)
        self.contentsChanged.emit()
        self.contentsChange.emit(oldLines,0,len(self._dataLines)-oldLines)
        self._snapChanged = None

    def isUndoAvailable(self):
        return self._snap and self._snap._prevDiff

    def isRedoAvailable(self):
        return self._snap and self._snap._nextDiff

    def hasSnapshots(self):
        return self._snap is not None

    def snapshootId(self):
        return self._snap._id

    def saveSnapshot(self, cursor):
        docA = self._lastSnap
        docB = self._dataLines

        # get the
        #   sa = starting line
        #   sb = removed lines
        #   sc = added lines
        # of the cumulative changes applied since the last snapshot
        sa,sb,sc = self._snapChanged if self._snapChanged else (0,0,0)
        self._snapChanged = None

        sliceA = docA[sa:sa+sb]
        sliceB = docB[sa:sa+sc]

        if sliceA or sliceB:
            # current snapshot
            # is becoming the previous one
            snapA  = self._snap
            diffBA = TTkTextDocument._snapDiff(sliceA, sa, sa+sc, snapA)
            snapB  = TTkTextDocument._snapshot(cursor, None, diffBA)
            diffAB = TTkTextDocument._snapDiff(sliceB, sa, sa+sb, snapB)
            snapA._nextDiff = diffAB
            self._snap = snapB
        else:
            self._snap._cursor = cursor

        self._modified = False
        self._lastSnap = self._dataLines.copy()
        self._lastCursor = cursor
        self.undoAvailable.emit(self.isUndoAvailable())
        self.redoAvailable.emit(self.isRedoAvailable())

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

    # def toHtml(self, encoding): pass
    # def toMarkdown(self, features): pass
    def toAnsi(self):
        return "\n".join([l.toAnsi() for l in self._dataLines])

    def toPlainText(self):
        return "\n".join([str(l) for l in self._dataLines])

    def toRawText(self):
        return TTkString("\n").join(self._dataLines)


