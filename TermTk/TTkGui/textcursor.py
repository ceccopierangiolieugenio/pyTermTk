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

__all__ = ['TTkTextCursor']

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
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

        def copy(self):
            return TTkTextCursor._prop(self.anchor.copy(), self.position.copy())

        def selectionStart(self):
            if self.position.toNum() > self.anchor.toNum():
                return self.anchor
            else:
                return self.position

        def selectionEnd(self):
            if self.position.toNum() >= self.anchor.toNum():
                return self.position
            else:
                return self.anchor

        def hasSelection(self):
            return not (self.position.line == self.anchor.line and self.position.pos == self.anchor.pos)

    class _CP():
        # The Cursor Position is based on the
        # document data structure, where the
        # the entire document is divided in lines
        # instead of considering it a massive string
        __slots__ = ('line','pos')
        def __init__(self, l=0, p=0):
            self.set(l,p)
        def copy(self):
            return TTkTextCursor._CP(self.line, self.pos)
        def set(self, l, p):
            self.pos  = p
            self.line = l
        def toNum(self):
            return self.pos | self.line << 16

    __slots__ = ('_document', '_properties', '_cID', '_color', '_autoChanged')
    def __init__(self, *args, **kwargs):
        self._color = None
        self._cID = 0
        self._autoChanged = False
        self._properties = [TTkTextCursor._prop(
                                TTkTextCursor._CP(),
                                TTkTextCursor._CP())]
        if 'document' in kwargs:
            self._document = kwargs.get('document')
            self._document.contentsChanged.connect(self._documentContentChanged)

    def _documentContentChanged(self):
        if self._autoChanged: return True
        self.clearCursors()
        self.clearSelection()

    def copy(self):
        ret = TTkTextCursor()
        ret._document = self._document
        ret._properties = [p.copy() for p in self._properties]
        ret._cID = self._cID
        ret._color = self._color
        ret._autoChanged = self._autoChanged
        return ret

    def restore(self, cursor):
        self._document = cursor._document
        self._properties = [p.copy() for p in cursor._properties]
        self._cID = cursor._cID
        self._color = cursor._color
        self._autoChanged = cursor._autoChanged
        self._document.cursorPositionChanged.emit(self)

    def setColor(self, color):
        self._color = color

    def clearColor(self):
        self._color = None

    def anchor(self):
        return self._properties[self._cID].anchor

    def position(self):
        return self._properties[self._cID].position

    def addCursor(self, line, pos):
        self._cID = 0
        self._properties.insert(0,
                        TTkTextCursor._prop(
                                TTkTextCursor._CP(line, pos),
                                TTkTextCursor._CP(line, pos)))
        self._checkCursors(notify=True)

    def clearCursors(self):
        p = self._properties[self._cID]
        self._cID = 0
        self._properties = [p]

    def clearSelection(self):
        for p in self._properties:
            p.anchor.line,p.anchor.pos = p.position.line,p.position.pos

    def positionColor(self, cID=-1):
        cID = self._cID if cID==-1 else cID
        p = self._properties[cID].position
        l = self._document._dataLines[p.line]
        pos = max(0,p.pos-1)
        if pos < len(l):
            color = l.colorAt(pos)
        else:
            color = TTkColor()
        return color

    def setPosition(self, line, pos, moveMode=MoveMode.MoveAnchor, cID=0):
        self._properties[cID].position.set(line,pos)
        if moveMode==TTkTextCursor.MoveAnchor:
            self._properties[cID].anchor.set(line,pos)
        self._document.cursorPositionChanged.emit(self)

    def getLinesUnderCursor(self):
        return [ self._document._dataLines[p.position.line] for p in self._properties ]

    def _checkCursors(self, notify=False):
        currCurs = self._properties[self._cID]
        currPos = currCurs.position.toNum()
        # Sort the cursors based on the starting position
        self._properties = sorted(
                self._properties,
                key=lambda x: x.selectionStart().toNum())
        # remove /merge overlapping cursors
        newProperties = self._properties[:1]
        for np in self._properties:
            op = newProperties[-1]
            if op.selectionEnd().toNum() < np.selectionStart().toNum():
                newProperties.append(np)
                continue
            if currCurs == np:
                currCurs = op
            # the two cursors are overlapping
            # I try to combine the 2 selections
            if op.selectionEnd().toNum() < np.selectionEnd().toNum():
                if op.position.toNum()>op.anchor.toNum():
                    op.position=np.selectionEnd()
                else:
                    op.anchor=np.selectionEnd()
        self._properties = newProperties
        self._cID = self._properties.index(currCurs)
        if notify or currPos != currCurs.position.toNum():
            self._document.cursorPositionChanged.emit(self)

    def movePosition(self, operation, moveMode=MoveMode.MoveAnchor, n=1, textWrap=None):
        currPos = self.position().toNum()
        def moveRight(cID,p,_):
            if p.pos < len(self._document._dataLines[p.line]):
                nextPos = self._document._dataLines[p.line].nextPos(p.pos)
                self.setPosition(p.line, nextPos, moveMode, cID=cID)
            elif p.line < len(self._document._dataLines)-1:
                self.setPosition(p.line+1, 0, moveMode, cID=cID)
        def moveLeft(cID,p,_):
            if p.pos > 0:
                prevPos = self._document._dataLines[p.line].prevPos(p.pos)
                self.setPosition(p.line, prevPos, moveMode, cID=cID)
            elif p.line > 0:
                self.setPosition(p.line-1, len(self._document._dataLines[p.line-1]) , moveMode, cID=cID)
        def moveUpDown(offset):
            def _moveUpDown(cID,p,n):
                cx, cy    = textWrap.dataToScreenPosition(p.line, p.pos)
                x,  y     = textWrap.normalizeScreenPosition(cx,cy+offset*n)
                line, pos = textWrap.screenToDataPosition(x,y)
                self.setPosition(line, pos, moveMode, cID=cID)
            return _moveUpDown
        def moveEndOfLine(cID,p,_):
            l = self._document._dataLines[p.line]
            self.setPosition(p.line, len(l), moveMode, cID=cID)
        def moveHome(cID,p,_):
            self.setPosition(p.line, 0, moveMode, cID=cID)
        def moveEnd(cID,p,_):
            l = self._document._dataLines[-1]
            self.setPosition(len(self._document._dataLines)-1, len(l), moveMode, cID=cID)

        op = {
                TTkTextCursor.Right : moveRight,
                TTkTextCursor.Left  : moveLeft,
                TTkTextCursor.Up    : moveUpDown(-1),
                TTkTextCursor.Down  : moveUpDown(+1),
                TTkTextCursor.EndOfLine  : moveEndOfLine,
                TTkTextCursor.StartOfLine: moveHome,
                TTkTextCursor.End: moveEnd,
            }.get(operation,lambda _:_)

        for _ in range(n):
          for cID, prop in enumerate(self._properties):
            p = prop.position
            op(cID,p,n)

        self._checkCursors(notify=self.position().toNum()!=currPos)

    def document(self):
        return self._document

    def replaceText(self, text, moveCursor=False):
        # if there is no selection, just select the next n chars till the end of the line
        # the newline is not replaced
        for p in self._properties:
            if not p.hasSelection():
                line = p.position.line
                pos  = p.position.pos
                lenWoZero = TTkString._getLenTextWoZero(text)
                size = len(self._document._dataLines[line])
                for _ in range(lenWoZero):
                    pos = self._document._dataLines[line].nextPos(pos)
                pos = min(size,pos)
                p.anchor.set(line,pos)
        return self.insertText(text, moveCursor)

    def insertText(self, text, moveCursor=False):
        _lineFirst = -1
        if self.hasSelection():
            _lineFirst, _lineRem, _lineAdd = self._removeSelectedText()

        lineFirst = self._properties[0].position.line
        lineRem, lineAdd = 0,0

        # Check if the number of lines is the same as the number of cursors
        # this is a corner case where each line belongs to a
        # different cursor
        textLines = text.split('\n') if len(text)>1 else [text]
        if len(textLines) != len(self._properties):
            textLines = [text]*len(self._properties)

        # Calc the added and removed lines
        for i, pr in enumerate(self._properties):
            lenNewLines=len(textLines[i].split('\n'))
            l = pr.position.line
            p = pr.position.pos
            if (  textLines[i] == '\n' and
                  l == lineFirst != _lineFirst and
                  p==len(self._document._dataLines[l]) ):
                lineFirst = l+1
                lineAdd = 1
                lineRem = 0
            elif (lineFirst + lineRem) > l:
                lineAdd += lenNewLines-1
            else:
                lineAdd += lenNewLines + l-lineFirst-lineRem
                lineRem = l - lineFirst + 1
        if _lineFirst != -1:
            lineFirst, lineRem, lineAdd = TTkTextDocument._mergeChangesSlices(
                                                (_lineFirst, _lineRem, _lineAdd),
                                                ( lineFirst,  lineRem,  lineAdd))
        for i, pr in enumerate(self._properties):
            text=textLines[i]
            l = pr.position.line
            p = pr.position.pos
            color = self._color if self._color else self.positionColor(i)

            # Use the same color under the cursor if no color is defined:
            ttktext = text
            if isinstance(ttktext, str):
                ttktext = TTkString(text, color)

            newLines = ( self._document._dataLines[l].substring(to=p) +
                         ttktext +
                         self._document._dataLines[l].substring(fr=p) ).split('\n')
            self._document._dataLines[l] = newLines[0]
            for nl in reversed(newLines[1:]):
                self._document._dataLines.insert(l+1, nl)

            # Move/Shift the cursors based on the pasted content
            #
            # 2 scenarios:
            #  1) No Newline(s) added
            #                p     p+1   p+2
            #   from:  aaaaaaXaaaaaYaaaaaYaaaa
            #
            #   to:    aaaaaaX....aaaaaYaaaaaYaaaa
            #                     diffPos = len(text)
            #
            #  2) Newlines are added
            #                p     p+1   p+2
            #   from:  aaaaaaXaaaaaYaaaaaYaaaa
            #
            #   to:    aaaaaaX...\n
            #          ......\n
            #          \n
            #          .....aaaaaYaaaaaYaaaa
            #               diffPos = len(text.split('\n')[-1]) - p
            diffLine = len(newLines)-1
            if diffLine:
                diffPos = len(text.split('\n')[-1]) - p
            else:
                diffPos = len(text)
            # Realign all the cursos (move the same if required)
            for pp in self._properties[i+(0 if moveCursor else 1):]:
                if pp.position.line == l:
                    pp.position.pos  += diffPos
                    pp.anchor.pos  += diffPos
                pp.position.line += diffLine
                pp.anchor.line += diffLine
        self._autoChanged = True
        self._document.setChanged(True)
        self._document.contentsChanged.emit()
        self._document.contentsChange.emit(lineFirst,  lineRem,  lineAdd)
        self._autoChanged = False
        self._document.cursorPositionChanged.emit(self)

    def selectionStart(self):
        return self._properties[self._cID].selectionStart()

    def selectionEnd(self):
        return self._properties[self._cID].selectionEnd()

    def select(self, selection):
        currPos = self.position().toNum()
        for p in self._properties:
            if   selection == TTkTextCursor.SelectionType.Document:
                pass
            elif selection == TTkTextCursor.SelectionType.LineUnderCursor:
                line = p.position.line
                p.position.pos = 0
                p.anchor.pos   = len(self._document._dataLines[line])
            elif selection == TTkTextCursor.SelectionType.WordUnderCursor:
                line = p.position.line
                pos  = p.position.pos
                # Split the current line from the current cursor position
                # search the leftmost(on the right slice)/rightmost(on the left slice) word
                # in order to match the full word under the cursor
                splitBefore = self._document._dataLines[line].substring(to=pos)
                splitAfter =  self._document._dataLines[line].substring(fr=pos)
                xFrom = pos
                xTo   = pos
                selectRE = r'[^ \t\r\n()[\]\.\,\+\-\*\/]*'
                if m := splitBefore.search(selectRE+'$'):
                    xFrom -= len(m.group(0))
                if m := splitAfter.search('^'+selectRE):
                    xTo += len(m.group(0))
                p.position.pos = xTo
                p.anchor.pos   = xFrom
        self._checkCursors(notify=self.position().toNum()!=currPos)

    def selectedText(self):
        def _getText(p):
            _ret = []
            selSt = p.selectionStart()
            selEn = p.selectionEnd()
            for l in range(selSt.line,selEn.line+1):
                line = self._document._dataLines[l]
                pf = 0         if l > selSt.line else selSt.pos
                pt = len(line) if l < selEn.line else selEn.pos
                _ret.append(line.substring(pf, pt))
            return _ret
        ret = []
        for p in self._properties:
            ret += _getText(p)
        return TTkString('\n').join(ret)

    def hasSelection(self):
        for p in self._properties:
            if p.hasSelection():
                return True
        return False

    def _removeSelectedText(self):
        currPos = self.position().toNum()

        lineFirst = self._properties[0].selectionStart().line
        lineAdd = 0
        lineRem = 0

        for p in self._properties:
            # Check how many lines are removed/added after this operation
            selSt = p.selectionStart()
            selEn = p.selectionEnd()

            if (lineFirst + lineRem) > selSt.line:
                _lineAdd = 0
            else:
                _lineAdd = 0 if selSt.pos == selEn.pos == 0 else 1

            lineAdd += selSt.line - lineFirst - lineRem + _lineAdd
            lineRem = selEn.line - lineFirst + _lineAdd

        def _alignPoint(point,st,en):
            point.line += st.line - en.line
            if point.line == st.line:
                point.pos += st.pos - en.pos

        for i, p in enumerate(self._properties):
            selSt = p.selectionStart()
            selEn = p.selectionEnd()
            self._document._dataLines[selSt.line] = self._document._dataLines[selSt.line].substring(to=selSt.pos) + \
                               self._document._dataLines[selEn.line].substring(fr=selEn.pos)
            self._document._dataLines = self._document._dataLines[:selSt.line+1] + self._document._dataLines[selEn.line+1:]
            for pp in self._properties[i+1:]:
                _alignPoint(pp.position, selSt, selEn)
                _alignPoint(pp.anchor,   selSt, selEn)
            self.setPosition(selSt.line, selSt.pos, cID=i)

        self._checkCursors(notify=self.position().toNum()!=currPos)

        return lineFirst, lineRem, lineAdd

    def removeSelectedText(self):
        if not self.hasSelection(): return
        a,b,c = self._removeSelectedText()
        self._autoChanged = True
        self._document.setChanged(True)
        self._document.contentsChanged.emit()
        self._document.contentsChange.emit(a,b,c)
        self._autoChanged = False

    def applyColor(self, color):
        for p in self._properties:
            selSt = p.selectionStart()
            selEn = p.selectionEnd()
            for l in range(selSt.line,selEn.line+1):
                line = self._document._dataLines[l]
                pf = 0         if l > selSt.line else selSt.pos
                pt = len(line) if l < selEn.line else selEn.pos
                self._document._dataLines[l] = line.setColor(color=color, posFrom=pf, posTo=pt)
        self._autoChanged = True
        self._document.setChanged(True)
        self._document.contentsChanged.emit()
        # self._document.contentsChange.emit(0,0,0)
        self._autoChanged = True

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
        if len(self._properties)>1:
            for s in sel:
                _, _, prop = s
                p = prop.position
                ret[p.line-fr] = ret[p.line-fr].setColor(color=color+TTkColor.BLINKING, posFrom=p.pos, posTo=p.pos+1)
                if p.pos == len(ret[p.line-fr]):
                   ret[p.line-fr] = ret[p.line-fr]+TTkString('↵',color+TTkColor.BLINKING)
                elif ret[p.line-fr].charAt(p.pos) == ' ':
                    ret[p.line-fr].setCharAt(pos=p.pos, char='∙')
                    # ret[p.line-fr].setColorAt(pos=p.pos, color=TTkCfg.theme.treeLineColor+TTkColor.BLINKING)
                #elif ret[p.line-fr].charAt(p.pos) == '\t':
                #    ret[p.line-fr].setCharAt(pos=p.pos, char='\t')

        return ret
