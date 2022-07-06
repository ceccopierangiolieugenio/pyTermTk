#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkGui.textwrap import TTkTextWrap
from TermTk.TTkGui.textcursor import TTkTextCursor
from TermTk.TTkGui.textdocument import TTkTextDocument
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class _TTkTextEditView(TTkAbstractScrollView):
    __slots__ = (
            '_textDocument', '_hsize',
            '_textCursor', '_textColor', '_cursorParams',
            '_textWrap', '_tabSpaces',
            '_lineWrapMode', '_wordWrapMode', '_wrapWidth', '_lastWrapUsed',
            '_replace',
            '_readOnly',
            # Forwarded Methods
            'wrapWidth',    'setWrapWidth',
            'lineWrapMode', 'setLineWrapMode',
            'wordWrapMode', 'setWordWrapMode',
            # Signals
            'currentCharFormatChanged'
        )
    '''
        in order to support the line wrap, I need to divide the full data text in;
        _textDocument = the entire text divided in lines, easy to add/remove/append lines
        _textWrap._lines     = an array of tuples for each displayed line with a pointer to a
                     specific line and its slice to be shown at this coordinate;
                     [ (line, (posFrom, posTo)), ... ]
                     This is required to support the wrap feature
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTextEditView' )
        self._readOnly = True
        self._hsize = 0
        self._lastWrapUsed  = 0
        self._textDocument = TTkTextDocument()
        self._textCursor = TTkTextCursor(document=self._textDocument)
        self._textWrap = TTkTextWrap(document=self._textDocument)
        self._textDocument.contentsChanged.connect(self._rewrap)
        self._replace = False
        self._cursorParams = None
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)
        # Trigger an update when the rewrap happen
        self._textWrap.wrapChanged.connect(self.update)
        # forward textWrap Methods
        self.wrapWidth       = self._textWrap.wrapWidth
        self.setWrapWidth    = self._textWrap.setWrapWidth
        self.lineWrapMode    = self._textWrap.lineWrapMode
        self.setLineWrapMode = self._textWrap.setLineWrapMode
        self.wordWrapMode    = self._textWrap.wordWrapMode
        self.setWordWrapMode = self._textWrap.setWordWrapMode

    def isReadOnly(self) -> bool :
        return self._readOnly

    def setReadOnly(self, ro):
        self._readOnly = ro

    def clear(self):
        self.setText(TTkString())

    @pyTTkSlot(str)
    def setText(self, text):
        self.viewMoveTo(0, 0)
        self._textDocument.setText(text)
        self._updateSize()

    @pyTTkSlot(str)
    def append(self, text):
        self._textDocument.appendText(text)
        self._updateSize()

    def _rewrap(self):
        self._textWrap.rewrap()
        self.viewChanged.emit()
        self.update()

    def resizeEvent(self, w, h):
        if w != self._lastWrapUsed and w>self._textWrap._tabSpaces:
            self._lastWrapUsed = w
            self._rewrap()
        return super().resizeEvent(w,h)

    def _updateSize(self):
        self._hsize = max( len(l) for l in self._textDocument._dataLines )

    def viewFullAreaSize(self) -> (int, int):
        if self._textWrap._lineWrapMode == TTkK.NoWrap:
            return self._hsize, len(self._textWrap._lines)
        elif self._textWrap._lineWrapMode == TTkK.WidgetWidth:
            return self.width(), len(self._textWrap._lines)
        elif self._textWrap._lineWrapMode == TTkK.FixedWidth:
            return self._textWrap._wrapWidth, len(self._textWrap._lines)

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def _pushCursor(self):
        if self._readOnly or not self.hasFocus():
            return
        ox, oy = self.getViewOffsets()

        x,y = self._cursorFromDataPos(
            self._textCursor.position().line,
            self._textCursor.position().pos)
        y -= oy
        x -= ox

        if x > self.width() or y>=self.height() or \
           x<0 or y<0:
            TTkHelper.hideCursor()
            return

        # Avoid the show/move cursor to be called again if in the same position
        if self._cursorParams and \
           self._cursorParams['pos'] == (x,y) and \
           self._cursorParams['replace'] == self._replace:
            return

        self._cursorParams = {'pos': (x,y), 'replace': self._replace}
        TTkHelper.moveCursor(self,x,y)
        if self._replace:
            TTkHelper.showCursor(TTkK.Cursor_Blinking_Block)
        else:
            TTkHelper.showCursor(TTkK.Cursor_Blinking_Bar)
        self.update()

    def _setCursorPos(self, x, y, alignRightTab=False):
        self._setCursorPosNEW(x,y,alignRightTab)

    def _setCursorPosNEW(self, x, y, alignRightTab=False, moveAnchor=True):
        x,y = self._cursorAlign(x,y, alignRightTab)
        _, pos = self._linePosFromCursor(x,y)
        self._textCursor.setPosition(self._textWrap._lines[y][0], pos,
                            moveMode=TTkTextCursor.MoveAnchor if moveAnchor else TTkTextCursor.KeepAnchor)
        self._scrolToInclude(x,y)

    def _scrolToInclude(self, x, y):
        # Scroll the area (if required) to include the position x,y
        _,_,w,h = self.geometry()
        offx, offy = self.getViewOffsets()
        offx = max(min(offx, x),x-w)
        offy = max(min(offy, y),y-h+1)
        self.viewMoveTo(offx, offy)

    def _selection(self) -> bool:
        return self._textCursor.hasSelection()

    def _eraseSelection(self):
        if not self._textCursor.hasSelection(): return
        self._textCursor.removeSelectedText()

    def _cursorAlign(self, x, y, alignRightTab = False):
        '''
        Return the widget position of the closest editable char
        in:
        x,y = widget relative position
        alignRightTab = if true, align the position to the right of the tab space
        return:
        x,y = widget relative position aligned to the close editable char
        '''
        y = max(0,min(y,len(self._textWrap._lines)-1))
        dt, (fr, to) = self._textWrap._lines[y]
        x = max(0,x)
        s = self._textDocument._dataLines[dt].substring(fr,to)
        x = s.tabCharPos(x, self._textWrap._tabSpaces, alignRightTab)
        # The replace cursor need to be aligned to the char
        # The Insert cursor must be placed between chars
        if self._replace and x==len(s):
            x -= 1
        x = len(s.substring(0,x).tab2spaces(self._textWrap._tabSpaces))
        return x, y

    def _linePosFromCursor(self,x,y):
        '''
        return the line and the x position from the x,y cursor position relative to the widget
        I assume the x,y position already normalized using the _cursorAlign function
        '''
        dt, (fr, to) = self._textWrap._lines[y]
        return self._textDocument._dataLines[dt], fr+self._textDocument._dataLines[dt].substring(fr,to).tabCharPos(x,self._textWrap._tabSpaces)

    def _widgetPositionFromTextCursor(self, line, pos):
        for i,l in enumerate(self._textWrap._lines):
            if l[0] == line and l[1][0] <= pos < l[1][1]:
                return pos-l[1][0], i
        return 0,0

    def _cursorFromLinePos(self,liney,p):
        '''
        return the x,y cursor position relative to the widget from the
        liney value relative to the self._textWrap._lines and the
        p = position value relative to the string related to self._textWrap._lines[liney][0]
        I know, big chink of crap
        '''
        # Find the bginning of the string in the "self._textWrap._lines" (position from == 0)
        while self._textWrap._lines[liney][1][0]: liney -=1
        dt = self._textWrap._lines[liney][0]
        while liney < len(self._textWrap._lines):
            dt1, (fr, to) = self._textWrap._lines[liney]
            if dt1 != dt:
                break
            if fr<=p<to:
                s = self._textDocument._dataLines[dt].substring(fr,p).tab2spaces(self._textWrap._tabSpaces)
                return len(s), liney
            liney += 1
        liney-=1
        dt, (fr, to) = self._textWrap._lines[liney]
        s = self._textDocument._dataLines[dt].substring(fr,to)
        return len(s.tab2spaces(self._textWrap._tabSpaces)), liney

    def _cursorFromDataPos(self,y,p):
        for i,l in enumerate(self._textWrap._lines):
            if l[0] == y:
                return self._cursorFromLinePos(i,p)
        return 0,0

    def mousePressEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mousePressEvent(evt)
        ox, oy = self.getViewOffsets()
        x,y = self._cursorAlign(evt.x + ox, evt.y + oy)
        self._setCursorPos(x,y)
        self.update()
        return True

    def mouseDragEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseDragEvent(evt)
        ox, oy = self.getViewOffsets()
        x,y = self._cursorAlign(evt.x + ox, evt.y + oy)
        self._setCursorPosNEW(x,y,moveAnchor=False)
        self._scrolToInclude(x,y)
        self.update()
        return True

    def mouseDoubleClickEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseDoubleClickEvent(evt)
        self._textCursor.select(TTkTextCursor.WordUnderCursor)
        self.update()
        return True

    def mouseTapEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseTapEvent(evt)
        self._textCursor.select(TTkTextCursor.LineUnderCursor)
        self.update()
        return True

    def keyEvent(self, evt):
        if self._readOnly:
            return super().keyEvent(evt)
        if evt.type == TTkK.SpecialKey:
            _,_,w,h = self.geometry()

            p = self._textCursor.position()
            cx, cy = self._cursorFromDataPos(p.line, p.pos)
            dt, (fr, to) = self._textWrap._lines[cy]
            # Don't Handle the special tab key, for now
            if evt.key == TTkK.Key_Tab:
                return False
            if evt.key == TTkK.Key_Up:         self._setCursorPos(cx , cy-1)
            elif evt.key == TTkK.Key_Down:     self._setCursorPos(cx , cy+1)
            elif evt.key == TTkK.Key_Left:     self._textCursor.movePosition(TTkTextCursor.Left)
            elif evt.key == TTkK.Key_Right:    self._textCursor.movePosition(TTkTextCursor.Right)
            elif evt.key == TTkK.Key_End:      self._setCursorPos(w  , cy )
            elif evt.key == TTkK.Key_Home:     self._setCursorPos(0  , cy )
            elif evt.key == TTkK.Key_PageUp:   self._setCursorPos(cx , cy - h)
            elif evt.key == TTkK.Key_PageDown: self._setCursorPos(cx , cy + h)
            elif evt.key == TTkK.Key_Insert:
                self._replace = not self._replace
                self._setCursorPos(cx , cy)
            elif evt.key == TTkK.Key_Delete:
                if not self._selection():
                    self._textCursor.movePosition(TTkTextCursor.Right, TTkTextCursor.KeepAnchor)
                self._eraseSelection()
            elif evt.key == TTkK.Key_Backspace:
                if not self._selection():
                    self._textCursor.movePosition(TTkTextCursor.Left, TTkTextCursor.KeepAnchor)
                self._eraseSelection()
            elif evt.key == TTkK.Key_Enter:
                self._eraseSelection()
                l,dx = self._linePosFromCursor(cx,cy)
                self._textDocument._dataLines[dt] = l.substring(to=dx)
                self._textDocument._dataLines = self._textDocument._dataLines[:dt+1] + [l.substring(fr=dx)] + self._textDocument._dataLines[dt+1:]
                self._rewrap()
                self._setCursorPos(0,cy+1)
            self.update()
            return True
        else: # Input char
            self._textCursor.insertText(evt.key)
            self.update()
            return True

        return super().keyEvent(evt)

    def focusInEvent(self):
        self.update()

    def focusOutEvent(self):
        TTkHelper.hideCursor()

    def paintEvent(self):
        ox, oy = self.getViewOffsets()
        if self.hasFocus():
            selectColor = TTkCfg.theme.lineEditTextColorSelected
        else:
            selectColor = TTkCfg.theme.lineEditTextColorSelected

        h = self.height()
        subLines = self._textWrap._lines[oy:oy+h]
        outLines = self._textCursor.getHighlightedLines(subLines[0][0], subLines[-1][0], selectColor)

        for y, l in enumerate(subLines):
            t = outLines[l[0]-subLines[0][0]]
            self._canvas.drawText(pos=(-ox,y), text=t.substring(l[1][0],l[1][1]).tab2spaces(self._textWrap._tabSpaces))

        if self._textWrap._lineWrapMode == TTkK.FixedWidth:
            self._canvas.drawVLine(pos=(self._textWrap._wrapWidth,0), size=h, color=TTkCfg.theme.treeLineColor)
        self._pushCursor()

class TTkTextEdit(TTkAbstractScrollArea):
    __slots__ = (
            '_textEditView',
            # Forwarded Methods
            'clear', 'setText', 'append', 'isReadOnly', 'setReadOnly'
            'wrapWidth', 'setWrapWidth',
            'lineWrapMode', 'setLineWrapMode',
            'wordWrapMode', 'setWordWrapMode',
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTextEdit' )
        self._textEditView = _TTkTextEditView()
        # self.setFocusPolicy(self._textEditView.focusPolicy())
        # self._textEditView.setFocusPolicy(TTkK.ParentFocus)
        self.setViewport(self._textEditView)
        self.clear   = self._textEditView.clear
        self.setText = self._textEditView.setText
        self.append  = self._textEditView.append
        self.isReadOnly  = self._textEditView.isReadOnly
        self.setReadOnly = self._textEditView.setReadOnly
        # Forward Wrap Methods
        self.wrapWidth       = self._textEditView.wrapWidth
        self.setWrapWidth    = self._textEditView.setWrapWidth
        self.lineWrapMode    = self._textEditView.lineWrapMode
        self.setLineWrapMode = self._textEditView.setLineWrapMode
        self.wordWrapMode    = self._textEditView.wordWrapMode
        self.setWordWrapMode = self._textEditView.setWordWrapMode
        # Forward Signals
        self.focusChanged = self._textEditView.focusChanged
