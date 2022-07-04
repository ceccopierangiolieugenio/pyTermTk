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

    __slots__ = ('_document', '_properties', '_docData')
    def __init__(self, *args, **kwargs):
        self._properties = [TTkTextCursor._prop(
                                TTkTextCursor._CP(),
                                TTkTextCursor._CP())]
        self._document = kwargs.get('document',TTkTextDocument())
        self._docData = self._document._dataLines

    def anchor(self):
        return self._properties[0].anchor

    def position(self):
        return self._properties[0].position

    def setPosition(self, line, pos, moveMode=MoveMode.MoveAnchor ):
        self._properties[0].position.set(line,pos)
        if moveMode==TTkTextCursor.MoveAnchor:
            self._properties[0].anchor.set(line,pos)

    #def movePosition(self, operation, moveMode=MoveMode.MoveAnchor, n=1 ):
    #    pass

    def document(self):
        return self._document

    def insertText(self, text):
        pass

    def removeSelectedText(self):
        pass

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
            self._properties[0].anchor.pos   = len(self._docData[line])
        elif selection == TTkTextCursor.SelectionType.WordUnderCursor:
            line = self._properties[0].position.line
            pos  = self._properties[0].position.pos
            # Split the current line from the current cursor position
            # search the leftmost(on the right slice)/rightmost(on the left slice) word
            # in order to match the full word under the cursor
            splitBefore = self._docData[line].substring(to=pos)
            splitAfter =  self._docData[line].substring(fr=pos)
            xFrom = pos
            xTo   = pos
            selectRE = '[a-zA-Z0-9:,./]*'
            if m := splitBefore.search(selectRE+'$'):
                xFrom -= len(m.group(0))
            if m := splitAfter.search('^'+selectRE):
                xTo += len(m.group(0))
            self._properties[0].position.pos = xTo
            self._properties[0].anchor.pos   = xFrom
