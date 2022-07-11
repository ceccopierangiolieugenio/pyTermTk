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

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.string import TTkString
from TermTk.TTkGui.textdocument import TTkTextDocument

class TTkTextCursor():
    class MoveMode():
        MoveAnchor = 0x00
        '''Moves the anchor to the same position as the cursor itself.'''
        KeepAnchor = 0x01
        '''Keeps the anchor where it is.'''
    MoveAnchor = MoveMode.MoveAnchor
    KeepAnchor = MoveMode.KeepAnchor

    class SelectionType():
        Document         = 0x03
        '''Selects the entire document.'''
        BlockUnderCursor = 0x02
        '''Selects the block of text under the cursor.'''
        LineUnderCursor  = 0x01
        '''Selects the line of text under the cursor.'''
        WordUnderCursor  = 0x00
        '''Selects the word under the cursor. If the cursor is not positioned within a string of selectable characters, no text is selected.'''
    Document         = SelectionType.Document
    BlockUnderCursor = SelectionType.BlockUnderCursor
    LineUnderCursor  = SelectionType.LineUnderCursor
    WordUnderCursor  = SelectionType.WordUnderCursor

    class MoveOperation():
        NoMove            = 0
        '''Keep the cursor where it is'''
        Start             = 1
        '''Move to the start of the document.'''
        StartOfLine       = 3
        '''Move to the start of the current line.'''
        StartOfBlock      = 4
        '''Move to the start of the current block.'''
        StartOfWord       = 5
        '''Move to the start of the current word.'''
        PreviousBlock     = 6
        '''Move to the start of the previous block.'''
        PreviousCharacter = 7
        '''Move to the previous character.'''
        PreviousWord      = 8
        '''Move to the beginning of the previous word.'''
        Up                = 2
        '''Move up one line.'''
        Left              = 9
        '''Move left one character.'''
        WordLeft          = 10
        '''Move left one word.'''
        End               = 11
        '''Move to the end of the document.'''
        EndOfLine         = 13
        '''Move to the end of the current line.'''
        EndOfWord         = 14
        '''Move to the end of the current word.'''
        EndOfBlock        = 15
        '''Move to the end of the current block.'''
        NextBlock         = 16
        '''Move to the beginning of the next block.'''
        NextCharacter     = 17
        '''Move to the next character.'''
        NextWord          = 18
        '''Move to the next word.'''
        Down              = 12
        '''Move down one line.'''
        Right             = 19
        '''Move right one character.'''
        WordRight         = 20
        '''Move right one word.'''
        NextCell          = 21
        '''Move to the beginning of the next table cell inside the current table. If the current cell is the last cell in the row, the cursor will move to the first cell in the next row.'''
        PreviousCell      = 22
        '''Move to the beginning of the previous table cell inside the current table. If the current cell is the first cell in the row, the cursor will move to the last cell in the previous row.'''
        NextRow           = 23
        '''Move to the first new cell of the next row in the current table.'''
        PreviousRow       = 24
        '''Move to the last cell of the previous row in the current table.'''
    NoMove            = MoveOperation.NoMove
    Start             = MoveOperation.Start
    StartOfLine       = MoveOperation.StartOfLine
    StartOfBlock      = MoveOperation.StartOfBlock
    StartOfWord       = MoveOperation.StartOfWord
    PreviousBlock     = MoveOperation.PreviousBlock
    PreviousCharacter = MoveOperation.PreviousCharacter
    PreviousWord      = MoveOperation.PreviousWord
    Up                = MoveOperation.Up
    Left              = MoveOperation.Left
    WordLeft          = MoveOperation.WordLeft
    End               = MoveOperation.End
    EndOfLine         = MoveOperation.EndOfLine
    EndOfWord         = MoveOperation.EndOfWord
    EndOfBlock        = MoveOperation.EndOfBlock
    NextBlock         = MoveOperation.NextBlock
    NextCharacter     = MoveOperation.NextCharacter
    NextWord          = MoveOperation.NextWord
    Down              = MoveOperation.Down
    Right             = MoveOperation.Right
    WordRight         = MoveOperation.WordRight
    NextCell          = MoveOperation.NextCell
    PreviousCell      = MoveOperation.PreviousCell
    NextRow           = MoveOperation.NextRow
    PreviousRow       = MoveOperation.PreviousRow

    class _prop():
        __slots__ = ('anchor', 'position')
        def __init__(self, anchor, position):
            self.anchor = anchor
            self.position = position

        def selectionStart(self):
            if self.position.line == self.anchor.line:
                if self.position.pos < self.anchor.pos:
                    return self.position
                else:
                    return self.anchor
            elif self.position.line < self.anchor.line:
                return self.position
            else:
                return self.anchor

        def selectionEnd(self):
            if self.position.line == self.anchor.line:
                if self.position.pos < self.anchor.pos:
                    return self.anchor
                else:
                    return self.position
            elif self.position.line < self.anchor.line:
                return self.anchor
            else:
                return self.position

    class _CP():
        # The Cursor Position is based on the
        # document data structure, where the
        # the entire document is divided in lines
        # instead of considering it a massive string
        __slots__ = ('line','pos')
        def __init__(self, l=0, p=0):
            self.set(l,p)
        def set(self, l, p):
            self.pos  = p
            self.line = l

    __slots__ = ('_document', '_properties')
    def __init__(self, *args, **kwargs):
        self._properties = [TTkTextCursor._prop(
                                TTkTextCursor._CP(),
                                TTkTextCursor._CP())]
        self._document = kwargs.get('document',TTkTextDocument())

    def anchor(self):
        return self._properties[0].anchor

    def position(self):
        return self._properties[0].position

    def addCursor(self, line, pos):
        self._properties.insert(0,
                        TTkTextCursor._prop(
                                TTkTextCursor._CP(line, pos),
                                TTkTextCursor._CP(line, pos)))

    def cleanCursors(self):
        self._properties = self._properties[:1]

    def setPosition(self, line, pos, moveMode=MoveMode.MoveAnchor, cID=0):
        # TTkLog.debug(f"{line=}, {pos=}, {moveMode=}")
        self._properties[cID].position.set(line,pos)
        if moveMode==TTkTextCursor.MoveAnchor:
            self._properties[cID].anchor.set(line,pos)

    def movePosition(self, operation, moveMode=MoveMode.MoveAnchor, n=1, textWrap=None):
        def moveRight(cID,p,_):
            if p.pos < len(self._document._dataLines[p.line]):
                self.setPosition(p.line, p.pos+1, moveMode, cID=cID)
            elif p.line < len(self._document._dataLines)-1:
                self.setPosition(p.line+1, 0, moveMode, cID=cID)
        def moveLeft(cID,p,_):
            if p.pos > 0:
                self.setPosition(p.line, p.pos-1, moveMode, cID=cID)
            elif p.line > 0:
                self.setPosition(p.line-1, len(self._document._dataLines[p.line-1]) , moveMode, cID=cID)
        def moveUpDown(offset):
            def _moveUpDown(cID,p,n):
                cx, cy    = textWrap.dataToScreenPosition(p.line, p.pos)
                x,  y     = textWrap.normalizeScreenPosition(cx,cy+offset*n)
                line, pos = textWrap.screenToDataPosition(x,y)
                self.setPosition(line, pos, moveMode, cID=cID)
            return _moveUpDown
        def moveEnd(cID,p,_):
            l = self._document._dataLines[p.line]
            self.setPosition(p.line, len(l), moveMode, cID=cID)
        def moveHome(cID,p,_):
            self.setPosition(p.line, 0, moveMode, cID=cID)

        operations = {
                TTkTextCursor.Right : moveRight,
                TTkTextCursor.Left  : moveLeft,
                TTkTextCursor.Up    : moveUpDown(-1),
                TTkTextCursor.Down  : moveUpDown(+1),
                TTkTextCursor.EndOfLine  : moveEnd,
                TTkTextCursor.StartOfLine: moveHome
            }

        for cID, prop in enumerate(self._properties):
            p = prop.position
            operations.get(operation,lambda _:_)(cID,p,n)
            #if operation == TTkTextCursor.Right:
            #    if p.pos < len(self._document._dataLines[p.line]):
            #        self.setPosition(p.line, p.pos+1, moveMode, cID=cID)
            #    elif p.line < len(self._document._dataLines)-1:
            #        self.setPosition(p.line+1, 0, moveMode, cID=cID)
            #elif operation == TTkTextCursor.Left:
            #    if p.pos > 0:
            #        self.setPosition(p.line, p.pos-1, moveMode, cID=cID)
            #    elif p.line > 0:
            #        self.setPosition(p.line-1, len(self._document._dataLines[p.line-1]) , moveMode, cID=cID)

    def document(self):
        return self._document

    def insertText(self, text):
        l,b,c = 0,1,1
        if self.hasSelection():
            l,b,c = self._removeSelectedText()
        l = self.position().line
        p = self.position().pos
        # [TTkString(t) for t in text.split('\n')]
        newLines = (self._document._dataLines[l].substring(to=p) + text + self._document._dataLines[l].substring(fr=p)).split('\n')
        self._document._dataLines[l] = newLines[0]
        for nl in reversed(newLines[1:]):
            self._document._dataLines.insert(l+1, nl)
            c+=1
        self._document.contentsChanged.emit()
        self._document.contentsChange.emit(l,b,c)

    def selectionStart(self):
        return self._properties[0].selectionStart()

    def selectionEnd(self):
        return self._properties[0].selectionEnd()

    def select(self, selection):
        if   selection == TTkTextCursor.SelectionType.Document:
            pass
        elif selection == TTkTextCursor.SelectionType.LineUnderCursor:
            line = self._properties[0].position.line
            self._properties[0].position.pos = 0
            self._properties[0].anchor.pos   = len(self._document._dataLines[line])
        elif selection == TTkTextCursor.SelectionType.WordUnderCursor:
            line = self._properties[0].position.line
            pos  = self._properties[0].position.pos
            # Split the current line from the current cursor position
            # search the leftmost(on the right slice)/rightmost(on the left slice) word
            # in order to match the full word under the cursor
            splitBefore = self._document._dataLines[line].substring(to=pos)
            splitAfter =  self._document._dataLines[line].substring(fr=pos)
            xFrom = pos
            xTo   = pos
            selectRE = '[a-zA-Z0-9:,./]*'
            if m := splitBefore.search(selectRE+'$'):
                xFrom -= len(m.group(0))
            if m := splitAfter.search('^'+selectRE):
                xTo += len(m.group(0))
            self._properties[0].position.pos = xTo
            self._properties[0].anchor.pos   = xFrom

    def hasSelection(self):
        return ( self._properties[0].anchor.pos  != self._properties[0].position.pos or
                 self._properties[0].anchor.line != self._properties[0].position.line )

    def clearSelection(self):
        self._properties[0].anchor.pos  = self._properties[0].position.pos
        self._properties[0].anchor.line = self._properties[0].position.line

    def _removeSelectedText(self):
        selSt = self.selectionStart()
        selEn = self.selectionEnd()
        self._document._dataLines[selSt.line] = self._document._dataLines[selSt.line].substring(to=selSt.pos) + \
                           self._document._dataLines[selEn.line].substring(fr=selEn.pos)
        self._document._dataLines = self._document._dataLines[:selSt.line+1] + self._document._dataLines[selEn.line+1:]
        self.setPosition(selSt.line, selSt.pos)
        return selSt.line, selEn.line-selSt.line, 1

    def removeSelectedText(self):
        if not self.hasSelection(): return
        a,b,c = self._removeSelectedText()
        self._document.contentsChanged.emit()
        self._document.contentsChange.emit(a,b,c)

    def getHighlightedLines(self, fr, to, color):
        # Create a list of cursors (filtering out the ones which
        # position/selection is outside the screen boundaries)
        sel = []
        for p in self._properties:
            selSt = p.selectionStart()
            selEn = p.selectionEnd()
            if selEn.line >= fr and selSt.line<=to:
                sel.append((selSt,selEn,p))

        # Retrieve the sublist of lines to be required (displayed)
        ret = self._document._dataLines[fr:to+1]
        # Apply the selection color for each of them
        for s in sel:
            selSt, selEn, _ = s
            for i in range(max(selSt.line,fr),min(selEn.line+1,to+1)):
                l = ret[i-fr]
                pf = 0      if i > selSt.line else selSt.pos
                pt = len(l) if i < selEn.line else selEn.pos
                ret[i-fr] = l.setColor(color=color, posFrom=pf, posTo=pt)
        # Add Blinking cursor
        if len(sel)>1:
            for s in sel:
                _, _, prop = s
                p = prop.position
                ret[p.line-fr] = (ret[p.line-fr]+" ").setColor(color=color+TTkColor.BLINKING, posFrom=p.pos, posTo=p.pos+1)

        return ret
