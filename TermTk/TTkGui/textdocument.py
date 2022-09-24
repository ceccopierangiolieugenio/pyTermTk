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

# def ccc(c,dl):
#     pp = c._properties[0].selectionStart().pos
#     pl = c._properties[0].selectionStart().line
#     ap = c._properties[0].selectionEnd().pos
#     al = c._properties[0].selectionEnd().line
#     return f"{pp=},{pl=},{ap=},{al=} -> {dl[pl].substring(pp,ap)}"

# def ddd(td):
#     ii = td._diffId
#     TTkLog.debug(f"id={ii}")
#     for i,d in enumerate(td._diffs):
#         for s in d._slice1:
#             TTkLog.debug(f"{i} {' ' if i!=ii else '*' if     td._diffIdFw else '>'} s1 {str(s)}")
#         for s in d._slice2:
#             TTkLog.debug(f"{i} {' ' if i!=ii else '*' if not td._diffIdFw else '>'} s2 {str(s)}")

class TTkTextDocument():
    '''
        Undo,Redo Logic

        Old:
            _snapshotId: = last saved/undo/redo state
                                   3 = doc4
            _snapshots:
                [doc1, doc2, doc3, doc4, doc5, doc6, . . .]

        New 1:
            _diffs:
              [d01, d12,  d23,  d34,  d45,  d56,  . . .   ]
               d01 = diff between the first doc and the empty string

            _lastSnap:             doc4   -> the current full snapshot (required to gen the diff)

          Undo: (need to move to doc3)
            _lastSnap = _lastSnap (doc4) - d34 = doc3
            _diffId -= 1

          Redo: (need to move to doc4)
            _diffId += 1 = 4
            _lastSnap = _lastSnap (doc4) + d45 = doc5

          SaveSnapshot:
            diff = newDoc - _lastSnap ( doc4 )
            if diff == 0:
                replace doc4, d34
            else:
                add new doc5, d45
                _diffId += 1
                _lastSnap = newDoc

         New 2:
            SnapshotId:
                              2
            Snapshots:                  _lastSnap     _dataLines (unstaged)
                ╒═══╕ ╒═══╕ ╒═══╕ ╒═══╕ ╒═══╕         ╒═══╕
                │ 0 │ │ 1 │ │ 2 │ │ 3 │ │ 4 │         │ 5 │
                └───┘ └───┘ └───┘ └───┘ └───┘         └───┘
            Cursors:
                 c0,   c1,   c2,   c3,   c4            c5 = _lastCursor
            Diffs:
                [   d01,  d12,  d23,  d34   ]
            Slices: = common txt slices between snapshots
                [   s01,  s12,  s23,  s34   ]


    '''
    class _snapDiff():
        '''
        Doc:
                  0<--i1-->f1      t1<--i2-->l1
         Base:    |---------aaaaaaaa---------|
         Mod:     |---------bbbbb   ---------|
                  0        f2   t2           l2 = l1 - (t1-f1) + (t2-f2)
        '''
        __slots__ = ('_slice1','_slice2', '_i1', '_i2', '_cursor1', '_cursor2')
        def __init__(self, doc1, doc2, cursor1, cursor2, i1, i2):
            self._slice1 = doc1
            self._slice2 = doc2
            self._cursor1 = cursor1
            self._cursor2 = cursor2
            self._i1 = i1
            self._i2 = i2

    # class _snapshot():
    #     __slots__ = ('_lines', '_cursor')
    #     def __init__(self, lines, cursor):
    #         self._lines  = lines
    #         self._cursor = cursor

    __slots__ = (
        '_dataLines', '_changed',
        '_diffs', '_diffId', '_diffIdFw',
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
        self._diffs = []
        self._lastSnap = self._dataLines.copy()
        self._lastCursor = TTkTextCursor(document=self)
        self._diffId = -1
        self._diffIdFw = False
        # self.saveSnapshot(self._lastCursor)

    def changed(self):
        return self._changed

    def lineCount(self):
        return len(self._dataLines)

    def characterCount(self):
        return sum([len[x] for x in self._dataLines])+self.lineCount()

    def setText(self, text):
        self._dataLines = [TTkString(t) for t in text.split('\n')]
        self._changed = False
        self._diffs = []
        self._lastSnap = self._dataLines.copy()
        self.contentsChanged.emit()
        self.contentsChange.emit(0,0,len(self._dataLines))

    def appendText(self, text):
        if type(text) == str:
            text = TTkString() + text
        oldLines = len(self._dataLines)
        self._dataLines += text.split('\n')
        self._changed = False
        self._diffs = []
        self._lastSnap = self._dataLines.copy()
        self.contentsChanged.emit()
        self.contentsChange.emit(oldLines,0,len(self._dataLines)-oldLines)

    def isUndoAvailable(self):
        return (   self._diffId >  0 or
                 ( self._diffId == 0 and self._diffIdFw ) )

    def isRedoAvailable(self):
        return (   0 <= self._diffId <  len(self._diffs)-1 or
                 ( 0 <= self._diffId == len(self._diffs)-1 and not self._diffIdFw ) )

    def hasSnapshots(self):
        return len(self._diffs)>0

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

        self._diffs = self._diffs[:max(0,self._diffId+1)]
        if sliceA or sliceB or not self._diffs:
            if self._diffIdFw or not self._diffs:
                snap = TTkTextDocument._snapDiff(sliceA, sliceB, self._lastCursor, cursor, i1, i2)
                self._diffs.append(snap)
            else:
                snap = TTkTextDocument._snapDiff(sliceA, sliceB, self._diffs[-1]._cursor1, cursor, i1, i2)
                self._diffs[-1] = snap
            self._diffIdFw = True
        else:
            if self._diffIdFw:
                self._diffs[-1]._cursor2 = cursor
        self._diffId = len(self._diffs)-1

        self._changed = False
        self._lastSnap = self._dataLines.copy()
        self._lastCursor = cursor
        self.undoAvailable.emit(self.isUndoAvailable())
        self.redoAvailable.emit(self.isRedoAvailable())
        # ddd(self)

    def restoreSnapshotDiff(self, inc=0):
        # ddd(self)
        # if not (0 <= self._diffId+inc < len(self._diffs)):
        #     return None
        if ( ( inc == 1   and     self._diffIdFw ) or
             ( inc == -1  and not self._diffIdFw ) ):
            if 0<= self._diffId+inc < len(self._diffs) :
                self._diffId += inc
            else:
                return None
        d = self._diffs[self._diffId]

        if inc == -1:
            sl = d._slice1
            cu = d._cursor1
            self._diffIdFw = False
        elif inc == 1:
            sl = d._slice2
            cu = d._cursor2
            self._diffIdFw = True
        else:
            return None

        if d._i2 == 0:
            self._dataLines[d._i1:] = sl
        else:
            self._dataLines[d._i1:-d._i2] = sl

        self._lastSnap = self._dataLines.copy()
        self._lastCursor = cu.copy()

        self.contentsChanged.emit()
        self.undoAvailable.emit(self.isUndoAvailable())
        self.redoAvailable.emit(self.isRedoAvailable())
        # ddd(self)
        return cu

    def restoreSnapshotPrev(self):
        return self.restoreSnapshotDiff(-1)

    def restoreSnapshotNext(self):
        return self.restoreSnapshotDiff(+1)


