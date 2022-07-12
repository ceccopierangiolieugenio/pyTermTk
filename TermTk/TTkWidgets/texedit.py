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
            '_textWrap', '_lineWrapMode', '_lastWrapUsed',
            '_replace',
            '_readOnly', '_multiCursor',
            # Forwarded Methods
            'wrapWidth',    'setWrapWidth',
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
        self._multiCursor = True
        self._hsize = 0
        self._lastWrapUsed  = 0
        self._textDocument = TTkTextDocument()
        self._textCursor = TTkTextCursor(document=self._textDocument)
        self._lineWrapMode = TTkK.NoWrap
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
        self.wordWrapMode    = self._textWrap.wordWrapMode
        self.setWordWrapMode = self._textWrap.setWordWrapMode

    def isReadOnly(self) -> bool :
        return self._readOnly

    def setReadOnly(self, ro):
        self._readOnly = ro

    def clear(self):
        self.setText(TTkString())

    def lineWrapMode(self):
        return self._lineWrapMode

    def setLineWrapMode(self, mode):
        self._lineWrapMode = mode
        if mode == TTkK.NoWrap:
            self._textWrap.disable()
        else:
            self._textWrap.enable()
            if mode == TTkK.WidgetWidth:
                self._textWrap.setWrapWidth(self.width())
        self._textWrap.rewrap()

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
        if self.lineWrapMode() == TTkK.NoWrap:
            return self._hsize, self._textWrap.size()
        elif self.lineWrapMode() == TTkK.WidgetWidth:
            return self.width(), self._textWrap.size()
        elif self.lineWrapMode() == TTkK.FixedWidth:
            return self.wrapWidth(), self._textWrap.size()

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def _pushCursor(self):
        if self._readOnly or not self.hasFocus():
            return
        ox, oy = self.getViewOffsets()

        x,y = self._textWrap.dataToScreenPosition(
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

    def _setCursorPos(self, x, y, moveAnchor=True, addCursor=False):
        x,y = self._textWrap.normalizeScreenPosition(x,y)
        line, pos = self._textWrap.screenToDataPosition(x,y)
        if addCursor:
            self._textCursor.addCursor(line, pos)
        else:
            self._textCursor.cleanCursors()
            self._textCursor.setPosition(line, pos,
                            moveMode=TTkTextCursor.MoveAnchor if moveAnchor else TTkTextCursor.KeepAnchor )
        self._scrolToInclude(x,y)
        return x, y

    def _scrolToInclude(self, x, y):
        # Scroll the area (if required) to include the position x,y
        _,_,w,h = self.geometry()
        offx, offy = self.getViewOffsets()
        offx = max(min(offx, x),x-w)
        offy = max(min(offy, y),y-h+1)
        self.viewMoveTo(offx, offy)

    def mousePressEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mousePressEvent(evt)
        ox, oy = self.getViewOffsets()
        self._setCursorPos(evt.x + ox, evt.y + oy, addCursor=evt.mod&TTkK.ControlModifier==TTkK.ControlModifier)
        self.update()
        return True

    def mouseDragEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseDragEvent(evt)
        ox, oy = self.getViewOffsets()
        x,y = self._setCursorPos(evt.x + ox, evt.y + oy, moveAnchor=False)
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
            cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos)
            dt, _ = self._textWrap._lines[cy]
            # Don't Handle the special tab key, for now

            moveMode = TTkTextCursor.MoveAnchor
            if evt.mod==TTkK.ShiftModifier:
                moveMode = TTkTextCursor.KeepAnchor

            ctrl = evt.mod==TTkK.ControlModifier

            if evt.key == TTkK.Key_Tab:
                return False
            if ctrl:
                p = self._textCursor.position()
                cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos)
                if evt.key == TTkK.Key_Up:     self._setCursorPos(cx, cy-1, addCursor=True)
                if evt.key == TTkK.Key_Down:   self._setCursorPos(cx, cy+1, addCursor=True)
            elif evt.key == TTkK.Key_Up:         self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Up,   textWrap=self._textWrap)
            elif evt.key == TTkK.Key_Down:     self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Down, textWrap=self._textWrap)
            elif evt.key == TTkK.Key_Left:     self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Left)
            elif evt.key == TTkK.Key_Right:    self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Right)
            elif evt.key == TTkK.Key_End:      self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.EndOfLine)
            elif evt.key == TTkK.Key_Home:     self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.StartOfLine)
            elif evt.key == TTkK.Key_PageUp:   self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Up,   textWrap=self._textWrap, n=h) #self._setCursorPos(cx , cy - h)
            elif evt.key == TTkK.Key_PageDown: self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Down, textWrap=self._textWrap, n=h) #self._setCursorPos(cx , cy + h)
            elif evt.key == TTkK.Key_Insert:
                self._replace = not self._replace
                self._setCursorPos(cx , cy)
            elif evt.key == TTkK.Key_Delete:
                if not self._textCursor.hasSelection():
                    self._textCursor.movePosition(TTkTextCursor.Right, TTkTextCursor.KeepAnchor)
                self._textCursor.removeSelectedText()
            elif evt.key == TTkK.Key_Backspace:
                if not self._textCursor.hasSelection():
                    self._textCursor.movePosition(TTkTextCursor.Left, TTkTextCursor.KeepAnchor)
                self._textCursor.removeSelectedText()
            elif evt.key == TTkK.Key_Enter:
                self._textCursor.insertText('\n')
                self._textCursor.movePosition(TTkTextCursor.Right)
            p = self._textCursor.position()
            cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos)
            self._scrolToInclude(cx,cy)
            self.update()
            return True
        else: # Input char
            self._textCursor.insertText(evt.key)
            self._textCursor.movePosition(TTkTextCursor.Right)
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

        if self._lineWrapMode == TTkK.FixedWidth:
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
