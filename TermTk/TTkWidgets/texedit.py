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

from math import log10, ceil

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkGui.clipboard import TTkClipboard
from TermTk.TTkGui.textwrap import TTkTextWrap
from TermTk.TTkGui.textcursor import TTkTextCursor
from TermTk.TTkGui.textdocument import TTkTextDocument
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView, TTkAbstractScrollViewGridLayout

class _TTkTextEditViewLineNumber(TTkAbstractScrollView):
    __slots__ = ('_textWrap')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumWidth(20)
        self._textWrap = None

    def _wrapChanged(self):
        dt = max(1,self._textWrap._lines[-1][0])
        width = 1+ceil(log10(dt))
        self.setMaximumWidth(width)
        self.update()

    def setTextWrap(self, tw):
        self._textWrap = tw
        tw.wrapChanged.connect(self._wrapChanged)
        self._wrapChanged()

    def viewFullAreaSize(self) -> (int, int):
        if self._textWrap:
            return 5, self._textWrap.size()
        else:
            return self.size()

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def paintEvent(self):
        if not self._textWrap: return
        _, oy = self.getViewOffsets()
        w, h = self.size()
        if self._textWrap:
            for i, (dt, (fr, _)) in enumerate(self._textWrap._lines[oy:oy+h]):
                if fr:
                    txt = "<"
                    color = TTkCfg.theme.textEditLineNumberWrapcharColor
                else:
                    txt = f"{dt}"
                    color = TTkCfg.theme.textEditLineNumberColor
                self._canvas.drawText(pos=(0,i), text=txt, width=w, color=color)
                self._canvas.drawChar(pos=(w-1,i), char='▌', color=TTkCfg.theme.textEditLineNumberSeparatorColor)
        else:
            color = TTkCfg.theme.textEditLineNumberColor
            for y in range(h):
                self._canvas.drawText(pos=(0,y), text=f"{y+oy}", width=w, color=color)
                self._canvas.drawChar(pos=(w-1,y), char='▌', color=TTkCfg.theme.textEditLineNumberSeparatorColor)

class TTkTextEditView(TTkAbstractScrollView):
    __slots__ = (
            '_textDocument', '_hsize',
            '_textCursor', '_textColor', '_cursorParams',
            '_textWrap', '_lineWrapMode', '_lastWrapUsed',
            '_replace',
            '_readOnly', '_multiCursor',
            '_clipboard',
            '_preview', '_previewWidth',
            # # Forwarded Methods
            # 'wrapWidth',    'setWrapWidth',
            # 'wordWrapMode', 'setWordWrapMode',
            # Signals
            'currentColorChanged',
            'undoAvailable', 'redoAvailable'
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
        self.currentColorChanged = pyTTkSignal(TTkColor)
        self.undoAvailable = pyTTkSignal(bool)
        self.redoAvailable = pyTTkSignal(bool)
        self._readOnly = kwargs.get('readOnly', True)
        self._multiCursor = True
        self._hsize = 0
        self._lastWrapUsed  = 0
        self._lineWrapMode = TTkK.NoWrap
        self._replace = False
        self._cursorParams = None
        self._textDocument = None
        self._textCursor = None
        self._textWrap = None
        self._clipboard = TTkClipboard()
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)
        self.setDocument(kwargs.get('document', TTkTextDocument()))
        self._updateSize()

    @pyTTkSlot(bool)
    def _undoAvailable(self, available):
        self.undoAvailable.emit(available)

    @pyTTkSlot(bool)
    def _redoAvailable(self, available):
        self.redoAvailable.emit(available)

    def isUndoAvailable(self):
        if self._textDocument:
            return self._textDocument.isUndoAvailable()
        return False

    def isRedoAvailable(self):
        if self._textDocument:
            return self._textDocument.isRedoAvailable()
        return False

    def document(self):
        return self._textDocument

    def setDocument(self, document):
        if self._textDocument:
            self._textDocument.contentsChanged.disconnect(self._rewrap)
            self._textDocument.cursorPositionChanged.disconnect(self._cursorPositionChanged)
            self._textDocument.undoAvailable.disconnect(self._undoAvailable)
            self._textDocument.redoAvailable.disconnect(self._redoAvailable)
            self._textWrap.wrapChanged.disconnect(self.update)
        if not document:
            document = TTkTextDocument()
        self._textDocument = document
        self._textCursor = TTkTextCursor(document=self._textDocument)
        self._textWrap = TTkTextWrap(document=self._textDocument)
        self._textDocument.contentsChanged.connect(self._rewrap)
        self._textDocument.cursorPositionChanged.connect(self._cursorPositionChanged)
        self._textDocument.undoAvailable.connect(self._undoAvailable)
        self._textDocument.redoAvailable.connect(self._redoAvailable)
        # Trigger an update when the rewrap happen
        self._textWrap.wrapChanged.connect(self.update)

    # forward textWrap Methods
    def wrapWidth(self, *args, **kwargs):       return self._textWrap.wrapWidth(*args, **kwargs)
    def setWrapWidth(self, *args, **kwargs):    return self._textWrap.setWrapWidth(*args, **kwargs)
    def wordWrapMode(self, *args, **kwargs):    return self._textWrap.wordWrapMode(*args, **kwargs)
    def setWordWrapMode(self, *args, **kwargs): return self._textWrap.setWordWrapMode(*args, **kwargs)

    def textCursor(self):
        return self._textCursor

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

    @pyTTkSlot()
    def undo(self):
        if c := self._textDocument.restoreSnapshotPrev():
            self._textCursor.restore(c)

    @pyTTkSlot()
    def redo(self):
        if c := self._textDocument.restoreSnapshotNext():
            self._textCursor.restore(c)

    @pyTTkSlot()
    def clear(self):
        pass

    @pyTTkSlot()
    def copy(self):
        if not self._textCursor.hasSelection():
            txt = TTkString('\n').join(self._textCursor.getLinesUnderCursor())
        else:
            txt = self._textCursor.selectedText()
        self._clipboard.setText(txt)

    @pyTTkSlot()
    def cut(self):
        if not self._textCursor.hasSelection():
            self._textCursor.movePosition(moveMode=TTkTextCursor.MoveAnchor, operation=TTkTextCursor.StartOfLine)
            self._textCursor.movePosition(moveMode=TTkTextCursor.KeepAnchor, operation=TTkTextCursor.EndOfLine)
            self._textCursor.movePosition(moveMode=TTkTextCursor.KeepAnchor, operation=TTkTextCursor.Right)
        self.copy()
        self._textCursor.removeSelectedText()

    @pyTTkSlot()
    def paste(self):
        txt = self._clipboard.text()
        self._textCursor.insertText(txt)

    @pyTTkSlot()
    def _rewrap(self):
        self._textWrap.rewrap()
        self.viewChanged.emit()
        self.update()

    @pyTTkSlot(TTkTextCursor)
    def _cursorPositionChanged(self, cursor):
        if cursor == self._textCursor:
            self.currentColorChanged.emit(cursor.positionColor())

    def resizeEvent(self, w, h):
        if ( self.lineWrapMode() == TTkK.WidgetWidth and
             w != self._lastWrapUsed and
             w > self._textWrap._tabSpaces ):
            self._textWrap.setWrapWidth(w)
            self._lastWrapUsed = w
            self._rewrap()
        return super().resizeEvent(w,h)

    def _updateSize(self):
        self._hsize = max( len(l) for l in self._textDocument._dataLines ) + 1

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
            self._textCursor.clearCursors()
            self._textCursor.setPosition(line, pos,
                            moveMode=TTkTextCursor.MoveAnchor if moveAnchor else TTkTextCursor.KeepAnchor )
        self._scrolToInclude(x,y)
        return x, y

    def _scrolToInclude(self, x, y):
        # Scroll the area (if required) to include the position x,y
        _,_,w,h = self.geometry()
        offx, offy = self.getViewOffsets()
        offx = max(min(offx, x),x-w+1)
        offy = max(min(offy, y),y-h+1)
        self.viewMoveTo(offx, offy)

    def mousePressEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mousePressEvent(evt)
        ox, oy = self.getViewOffsets()
        self._setCursorPos(evt.x + ox, evt.y + oy, addCursor=evt.mod&TTkK.ControlModifier==TTkK.ControlModifier)
        self._textCursor.clearColor()
        self.update()
        return True

    def mouseReleaseEvent(self, evt) -> bool:
        if self._textCursor.hasSelection():
            self.copy()
        return True

    def mouseDragEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseDragEvent(evt)
        ox, oy = self.getViewOffsets()
        x,y = self._setCursorPos(evt.x + ox, evt.y + oy, moveAnchor=False)
        self._textCursor.clearColor()
        self._scrolToInclude(x,y)
        self.update()
        return True

    def mouseDoubleClickEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseDoubleClickEvent(evt)
        self._textCursor.select(TTkTextCursor.WordUnderCursor)
        if self._textCursor.hasSelection():
            self.copy()
        self._textCursor.clearColor()
        self.update()
        return True

    def mouseTapEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseTapEvent(evt)
        self._textCursor.select(TTkTextCursor.LineUnderCursor)
        if self._textCursor.hasSelection():
            self.copy()
        self._textCursor.clearColor()
        self.update()
        return True

    def keyEvent(self, evt):
        if self._readOnly:
            return super().keyEvent(evt)

        # Keep a snapshot in case of those actions
        if (( evt.type == TTkK.Character and (
              ( evt.key == ' ' ) or
              ( evt.key == '\n') or
              ( evt.key == '\t') or
              ( self._textCursor.hasSelection() ) )  )  or
            ( evt.type == TTkK.SpecialKey and (
              ( evt.key == TTkK.Key_Enter     ) or
              ( evt.key == TTkK.Key_Delete    ) or
              ( evt.key == TTkK.Key_Backspace ) or
              ( self._textDocument.changed()  and evt.key == TTkK.Key_Z ) or
              ( evt.mod==TTkK.ControlModifier and
                (   evt.key == TTkK.Key_V or
                    evt.key == TTkK.Key_X or
                  ( evt.key == TTkK.Key_Z and self._textDocument.changed() ) )
              ) ) ) ):
            # TTkLog.debug(f"Saving {self._textCursor.selectedText()} {self._textCursor._properties[0].anchor.pos}")
            self._textDocument.saveSnapshot(self._textCursor.copy())

        if evt.type == TTkK.SpecialKey:
            _,_,w,h = self.geometry()

            # TODO: Remove this HACK As soon as possible
            # Due to the lack of 'INS' key on many laptops
            # I emulate this key using
            #    CTRL + HOME
            if evt.key == TTkK.Key_Home and evt.mod==TTkK.ControlModifier:
                evt.key = TTkK.Key_Insert
                evt.mod = TTkK.NoModifier

            moveMode = TTkTextCursor.MoveAnchor
            if evt.mod==TTkK.ShiftModifier:
                moveMode = TTkTextCursor.KeepAnchor

            ctrl = evt.mod==TTkK.ControlModifier

            if evt.key == TTkK.Key_Tab:
                # Don't Handle the special tab key, for now
                return False
            if ctrl:
                p = self._textCursor.position()
                cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos)
                if evt.key == TTkK.Key_Up:
                    self._setCursorPos(cx, cy-1, addCursor=True)
                    self._textCursor.clearColor()
                elif evt.key == TTkK.Key_Down:
                    self._setCursorPos(cx, cy+1, addCursor=True)
                    self._textCursor.clearColor()
                elif evt.key == TTkK.Key_C:
                    self.copy()
                elif evt.key == TTkK.Key_V:
                    self.paste()
                elif evt.key == TTkK.Key_X:
                    self.cut()
                elif evt.key == TTkK.Key_Z:
                    self.undo()
                elif evt.key == TTkK.Key_Y:
                    self.redo()
            elif evt.key == TTkK.Key_Up:
                self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Up,   textWrap=self._textWrap)
                self._textCursor.clearColor()
            elif evt.key == TTkK.Key_Down:
                self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Down, textWrap=self._textWrap)
                self._textCursor.clearColor()
            elif evt.key == TTkK.Key_Left:
                self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Left)
                self._textCursor.clearColor()
            elif evt.key == TTkK.Key_Right:
                self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Right)
                self._textCursor.clearColor()
            elif evt.key == TTkK.Key_End:
                self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.EndOfLine)
                self._textCursor.clearColor()
            elif evt.key == TTkK.Key_Home:
                self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.StartOfLine)
                self._textCursor.clearColor()
            elif evt.key == TTkK.Key_PageUp:
                self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Up,   textWrap=self._textWrap, n=h) #self._setCursorPos(cx , cy - h)
                self._textCursor.clearColor()
            elif evt.key == TTkK.Key_PageDown:
                self._textCursor.movePosition(moveMode=moveMode, operation=TTkTextCursor.Down, textWrap=self._textWrap, n=h) #self._setCursorPos(cx , cy + h)
                self._textCursor.clearColor()
            elif evt.key == TTkK.Key_Escape:
                self._textCursor.clearCursors()
                self._textCursor.clearSelection()
                self._textCursor.clearColor()
            elif evt.key == TTkK.Key_Insert:
                self._replace = not self._replace
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
            # Scroll to align to the cursor
            p = self._textCursor.position()
            cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos)
            self._updateSize()
            self._scrolToInclude(cx,cy)
            self.update()
            return True
        else: # Input char
            if self._replace:
                self._textCursor.replaceText(evt.key)
            else:
                self._textCursor.insertText(evt.key)
            self._textCursor.movePosition(TTkTextCursor.Right)
            # Scroll to align to the cursor
            p = self._textCursor.position()
            cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos)
            self._updateSize()
            self._scrolToInclude(cx,cy)
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
        if not subLines: return
        outLines = self._textCursor.getHighlightedLines(subLines[0][0], subLines[-1][0], selectColor)

        for y, l in enumerate(subLines):
            t = outLines[l[0]-subLines[0][0]]
            self._canvas.drawTTkString(pos=(-ox,y), text=t.substring(l[1][0],l[1][1]).tab2spaces(self._textWrap._tabSpaces))

        if self._lineWrapMode == TTkK.FixedWidth:
            self._canvas.drawVLine(pos=(self._textWrap._wrapWidth,0), size=h, color=TTkCfg.theme.treeLineColor)
        self._pushCursor()

class TTkTextEdit(TTkAbstractScrollArea):
    __slots__ = (
            '_textEditView',
            '_lineNumberView', '_lineNumber',
            # Forwarded Methods
            'clear', 'setText', 'append', 'isReadOnly', 'setReadOnly', 'document',
            'wrapWidth', 'setWrapWidth',
            'lineWrapMode', 'setLineWrapMode',
            'wordWrapMode', 'setWordWrapMode',
            'textCursor', 'setFocus',
            'undo', 'redo', 'isUndoAvailable', 'isRedoAvailable',
            # Signals
            'focusChanged', 'currentColorChanged',
            'undoAvilable', 'redoAvailable'
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTextEdit' )
        if 'parent' in kwargs: kwargs.pop('parent')
        self._textEditView = kwargs.get('textEditView', TTkTextEditView(*args, **kwargs))
        # self.setFocusPolicy(self._textEditView.focusPolicy())
        # self._textEditView.setFocusPolicy(TTkK.ParentFocus)
        self._lineNumber = kwargs.get('lineNumber', False)

        textEditLayout = TTkAbstractScrollViewGridLayout()
        textEditLayout.addWidget(self._textEditView,0,1)
        self._lineNumberView = _TTkTextEditViewLineNumber(visible=self._lineNumber)
        self._lineNumberView.setTextWrap(self._textEditView._textWrap)
        textEditLayout.addWidget(self._lineNumberView,0,0)
        self.setViewport(textEditLayout)

        self.clear   = self._textEditView.clear
        self.setText = self._textEditView.setText
        self.append  = self._textEditView.append
        self.document = self._textEditView.document
        self.isReadOnly  = self._textEditView.isReadOnly
        self.setReadOnly = self._textEditView.setReadOnly
        self.textCursor = self._textEditView.textCursor
        self.setFocus = self._textEditView.setFocus
        self.undo = self._textEditView.undo
        self.redo = self._textEditView.redo
        self.isUndoAvailable = self._textEditView.isUndoAvailable
        self.isRedoAvailable = self._textEditView.isRedoAvailable
        # Forward Wrap Methods
        self.wrapWidth       = self._textEditView.wrapWidth
        self.setWrapWidth    = self._textEditView.setWrapWidth
        self.lineWrapMode    = self._textEditView.lineWrapMode
        self.setLineWrapMode = self._textEditView.setLineWrapMode
        self.wordWrapMode    = self._textEditView.wordWrapMode
        self.setWordWrapMode = self._textEditView.setWordWrapMode
        # Forward Signals
        self.focusChanged = self._textEditView.focusChanged
        self.currentColorChanged = self._textEditView.currentColorChanged
        self.undoAvailable = self._textEditView.undoAvailable
        self.redoAvailable = self._textEditView.redoAvailable

    def setLineNumber(self, ln):
        self._lineNumberView.setVisible(ln)

    def setDocument(self, document):
        self._textEditView.setDocument(document)
        self._lineNumberView.setTextWrap(self._textEditView._textWrap)
