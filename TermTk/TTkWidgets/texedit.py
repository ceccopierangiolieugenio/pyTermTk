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

__all__ = ['TTkTextEditView', 'TTkTextEdit']

from math import log10, floor

from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkGui.clipboard import TTkClipboard
from TermTk.TTkGui.textwrap1 import TTkTextWrap
from TermTk.TTkGui.textcursor import TTkTextCursor
from TermTk.TTkGui.textdocument import TTkTextDocument
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView, TTkAbstractScrollViewGridLayout

class _TTkTextEditViewLineNumber(TTkAbstractScrollView):
    classStyle = {
                'default':     {
                    'color': TTkColor.fg("#88aaaa")+TTkColor.bg("#333333"),
                    'wrapColor': TTkColor.fg("#888888")+TTkColor.bg("#333333"),
                    'separatorColor': TTkColor.fg("#444444")},
                'disabled':    {
                    'color': TTkColor.fg('#888888'),
                    'wrapColor': TTkColor.fg('#888888'),
                    'separatorColor': TTkColor.fg("#888888")},
            }

    __slots__ = ('_textWrap','_startingNumber')
    def __init__(self, startingNumber=0, **kwargs):
        self._startingNumber = startingNumber
        self._textWrap = None
        super().__init__(**kwargs)
        self.setMaximumWidth(2)

    def _wrapChanged(self):
        dt = max(1,self._textWrap._lines[-1][0])
        off  = self._startingNumber
        width = 1+max(len(str(int(dt+off))),len(str(int(off))))
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

    def paintEvent(self, canvas):
        if not self._textWrap: return
        _, oy = self.getViewOffsets()
        w, h = self.size()
        off  = self._startingNumber

        style = self.currentStyle()
        color = style['color']
        wrapColor = style['wrapColor']
        separatorColor = style['separatorColor']

        if self._textWrap:
            for i, (dt, (fr, _)) in enumerate(self._textWrap._lines[oy:oy+h]):
                if fr:
                    canvas.drawText(pos=(0,i), text='<', width=w, color=wrapColor)
                else:
                    canvas.drawText(pos=(0,i), text=f"{dt+off}", width=w, color=color)
                canvas.drawChar(pos=(w-1,i), char='▌', color=separatorColor)
        else:
            for y in range(h):
                canvas.drawText(pos=(0,y), text=f"{y+oy+off}", width=w, color=color)
                canvas.drawChar(pos=(w-1,y), char='▌', color=separatorColor)

class TTkTextEditView(TTkAbstractScrollView):
    '''TTkTextEditView'''

    classStyle = {
                'default':     {'color':         TTkColor.fg("#dddddd")+TTkColor.bg("#222222"),
                                'selectedColor': TTkColor.fg("#ffffff")+TTkColor.bg("#008844"),
                                'lineColor':     TTkColor.fg("#444444"),
                                'wrapLineColor': TTkColor.fg("#888888")+TTkColor.bg("#333333")},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'selectedColor': TTkColor.bg("#888888"),
                                'lineColor':     TTkColor.fg("#888888"),
                                'wrapLineColor': TTkColor.fg('#888888')},
                'focus':       {'selectedColor': TTkColor.fg("#ffffff")+TTkColor.bg("#008888")},
            }

    __slots__ = (
            '_textDocument', '_hsize',
            '_textCursor', '_cursorParams',
            '_textWrap', '_lineWrapMode', '_lastWrapUsed',
            '_replace',
            '_readOnly', '_multiCursor',
            '_clipboard',
            # '_preview', '_previewWidth',
            '_multiLine',
            # # Forwarded Methods
            # 'wrapWidth',    'setWrapWidth',
            # 'wordWrapMode', 'setWordWrapMode',
            # Signals
            'currentColorChanged',
            'undoAvailable', 'redoAvailable',
            'textChanged'
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
        self.textChanged = pyTTkSignal()
        self._readOnly = kwargs.get('readOnly', True)
        self._multiLine = kwargs.get('multiLine', True)
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
        self.disableWidgetCursor(self._readOnly)
        self._updateSize()
        self.viewChanged.connect(self._pushCursor)

    def multiLine(self) -> bool :
        '''multiline'''
        return self._multiLine

    @pyTTkSlot(bool)
    def _undoAvailable(self, available):
        self.undoAvailable.emit(available)

    @pyTTkSlot(bool)
    def _redoAvailable(self, available):
        self.redoAvailable.emit(available)

    # def toHtml(self, encoding): pass
    #    if self._textDocument:
    #        return self._textDocument.toHtml()
    #    return ""

    # def toMarkdown(self, features): pass
    #    if self._textDocument:
    #        return self._textDocument.toMarkdown()
    #    return ""

    def toAnsi(self):
        '''toAnsi'''
        if self._textDocument:
            return self._textDocument.toAnsi()
        return ""

    def toPlainText(self):
        '''toPlainText'''
        if self._textDocument:
            return self._textDocument.toPlainText()
        return ""

    def toRawText(self):
        '''toRawText'''
        if self._textDocument:
            return self._textDocument.toRawText()
        return TTkString()

    def isUndoAvailable(self):
        '''isUndoAvailable'''
        if self._textDocument:
            return self._textDocument.isUndoAvailable()
        return False

    def isRedoAvailable(self):
        '''isRedoAvailable'''
        if self._textDocument:
            return self._textDocument.isRedoAvailable()
        return False

    def document(self):
        '''document'''
        return self._textDocument

    def setDocument(self, document):
        '''setDocument'''
        if self._textDocument:
            self._textDocument.contentsChanged.disconnect(self._documentChanged)
            self._textDocument.cursorPositionChanged.disconnect(self._cursorPositionChanged)
            self._textDocument.undoAvailable.disconnect(self._undoAvailable)
            self._textDocument.redoAvailable.disconnect(self._redoAvailable)
            self._textWrap.wrapChanged.disconnect(self.update)
        if not document:
            document = TTkTextDocument()
        self._textDocument = document
        self._textCursor = TTkTextCursor(document=self._textDocument)
        self._textWrap = TTkTextWrap(document=self._textDocument)
        self._textDocument.contentsChanged.connect(self._documentChanged)
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
        self.disableWidgetCursor(ro)

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
        self.pasteEvent(txt)

    @pyTTkSlot()
    def _documentChanged(self):
        self._rewrap()
        self.textChanged.emit()

    def _rewrap(self):
        self._textWrap.rewrap()
        self.viewChanged.emit()
        self.update()

    @pyTTkSlot(TTkColor)
    def setColor(self, color):
        self.textCursor().setColor(color)

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
        ox, oy = self.getViewOffsets()

        x,y = self._textWrap.dataToScreenPosition(
                self._textCursor.position().line,
                self._textCursor.position().pos)
        y -= oy
        x -= ox

        self._cursorParams = {'pos': (x,y), 'replace': self._replace}

        if self._replace:
            self.setWidgetCursor(pos=(x,y), type=TTkK.Cursor_Blinking_Block)
        else:
            self.setWidgetCursor(pos=(x,y), type=TTkK.Cursor_Blinking_Bar)

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
        self._pushCursor()
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
        self._pushCursor()
        self.update()
        return True

    def mouseDoubleClickEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseDoubleClickEvent(evt)
        self._textCursor.select(TTkTextCursor.WordUnderCursor)
        if self._textCursor.hasSelection():
            self.copy()
        self._textCursor.clearColor()
        self._pushCursor()
        self.update()
        return True

    def mouseTapEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseTapEvent(evt)
        self._textCursor.select(TTkTextCursor.LineUnderCursor)
        if self._textCursor.hasSelection():
            self.copy()
        self._textCursor.clearColor()
        self._pushCursor()
        self.update()
        return True

    def pasteEvent(self, txt:str):
        txt = TTkString(txt)
        if not self._multiLine:
            txt = TTkString().join(txt.split('\n'))
        if self._replace:
            self._textCursor.replaceText(txt, moveCursor=True)
        else:
            self._textCursor.insertText(txt, moveCursor=True)
        # Scroll to align to the cursor
        p = self._textCursor.position()
        cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos)
        self._updateSize()
        self._scrolToInclude(cx,cy)
        self._pushCursor()
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
                if self._multiLine:
                    self._textCursor.insertText('\n', moveCursor=True)
            # Scroll to align to the cursor
            p = self._textCursor.position()
            cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos)
            self._updateSize()
            self._scrolToInclude(cx,cy)
            self._pushCursor()
            self.update()
            return True
        else: # Input char
            if self._replace:
                self._textCursor.replaceText(evt.key, moveCursor=True)
            else:
                self._textCursor.insertText(evt.key, moveCursor=True)
            # Scroll to align to the cursor
            p = self._textCursor.position()
            cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos)
            self._updateSize()
            self._scrolToInclude(cx,cy)
            self._pushCursor()
            self.update()
            return True

        return super().keyEvent(evt)

    def paintEvent(self, canvas):
        ox, oy = self.getViewOffsets()

        style = self.currentStyle()
        color         = style['color']
        selectColor = style['selectedColor']
        lineColor = style['lineColor']

        h = self.height()
        subLines = self._textWrap._lines[oy:oy+h]
        if not subLines: return
        outLines = self._textCursor.getHighlightedLines(subLines[0][0], subLines[-1][0], selectColor)

        for y, l in enumerate(subLines):
            t = outLines[l[0]-subLines[0][0]]
            canvas.drawTTkString(pos=(-ox,y), text=t.substring(l[1][0],l[1][1]).tab2spaces(self._textWrap._tabSpaces))

        if self._lineWrapMode == TTkK.FixedWidth:
            canvas.drawVLine(pos=(self._textWrap._wrapWidth,0), size=h, color=lineColor)

class TTkTextEdit(TTkAbstractScrollArea):
    '''TTkTextEdit

    ::

        ╔═══════════════════════════════════════════════════════════════════════════════════════╗
        ║ 0▌"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ╥   ║
        ║ <▌incididunt ut labore et dolore magna aliqua.                                    ║   ║
        ║ 1▌                                                                                ║   ║
        ║ 2▌Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliqu║   ║
        ║ <▌ip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate ║   ║
        ║ <▌velit esse cillum dolore eu fugiat nulla pariatur.                              ║   ║
        ║ 3▌                                                                                ║   ║
        ║ 4▌Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deseru║   ║
        ║ <▌nt mollit anim id est laborum."                                                 ╨   ║
        ╚═══════════════════════════════════════════════════════════════════════════════════════╝

    Demo: `textedit.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/textedit.py>`_
    (`Try Online <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?fileUri=https://raw.githubusercontent.com/ceccopierangiolieugenio/pyTermTk/main/demo/showcase/textedit.py>`__)

    `ttkdesigner Tutorial <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit>`_

    :param lineNumber: Show the line number on the left, defaults to **False**
    :type lineNumber: bool, optional

    :param readOnly: In a read-only text edit the user can only navigate through the text and select text; modifying the text is not possible, defaults to **True**
    :type readOnly: bool, optional

    :param multiLine: In a multiline text edit the user can split the text in multiple lines, defaults to **True**
    :type multiLine: bool, optional

    :param document: If required an external Document can be used in this text editor, this option is useful if multiple editors share the same document as in the `demo <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?fileUri=https://raw.githubusercontent.com/ceccopierangiolieugenio/pyTermTk/main/demo/showcase/textedit.py>`__, defaults to a new Document
    :type document: :class:`~TermTk.TTkGui.textdocument.TTkTextDocument`, optional

    +-----------------------------------------------------------------------------------------------+
    | `Signals <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/003-signalslots.html>`_ |
    +-----------------------------------------------------------------------------------------------+

        .. py:method:: currentColorChanged(color)
            :signal:

            This signal is emitted if the current character color has changed, for example caused by a change of the cursor position.

            :param color: the new color
            :type color: :class:`~TermTk.TTkCore.color.TTkColor`

        .. py:method:: undoAvailable(available)
            :signal:

            This signal is emitted whenever undo operations become available (available is true) or unavailable (available is false).

            :param available: the availability of undo
            :type available: bool

        .. py:method:: redoAvailable(available)
            :signal:

            This signal is emitted whenever redo operations become available (available is true) or unavailable (available is false).

            :param available: the availability of redo
            :type available: bool

        .. py:method:: textChanged()
            :signal:

            This signal is emitted whenever the document's content changes; for example, when text is inserted or deleted, or when formatting is applied.

        .. py:method:: toAnsi()


    .. py:method:: clear()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.clear`

    .. py:method:: setText(text)

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.setText`

    .. py:method:: append(text)

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.append`

    .. py:method:: isReadOnly()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.isReadOnly`

    .. py:method:: setReadOnly(ro)

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.setReadOnly`

    .. py:method:: document()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.document`

    .. py:method:: wrapWidth()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.wrapWidth`

    .. py:method:: setWrapWidth(width)

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.setWrapWidth`

    .. py:method:: multiLine()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.multiLine`

    .. py:method:: lineWrapMode()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.lineWrapMode`

    .. py:method:: setLineWrapMode(mode)

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.setLineWrapMode`

    .. py:method:: wordWrapMode()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.wordWrapMode`

    .. py:method:: setWordWrapMode(mode)

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.setWordWrapMode`

    .. py:method:: textCursor()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.textCursor`

    .. py:method:: setColor(color)

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.setColor`

    .. py:method:: cut()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.cut`

    .. py:method:: copy()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.copy`

    .. py:method:: paste()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.paste`

    .. py:method:: undo()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.undo`

    .. py:method:: redo()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.redo`

    .. py:method:: isUndoAvailable()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.isUndoAvailable`

    .. py:method:: isRedoAvailable()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.isRedoAvailable`

    .. py:method:: toAnsi()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.toAnsi`

    .. py:method:: toRawText()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.toRawText`

    .. py:method:: toPlainText()

        This method is forwarded to :class:`~TermTk.TTkWidgets.texedit.TTkTextEditView.toPlainText`

    '''
    __slots__ = (
            '_textEditView',
            '_lineNumberView', '_lineNumber',
            # Forwarded Methods
            'clear', 'setText', 'append', 'isReadOnly', 'setReadOnly', 'document',
            'wrapWidth', 'setWrapWidth',
            'multiLine',
            'lineWrapMode', 'setLineWrapMode',
            'wordWrapMode', 'setWordWrapMode',
            'textCursor', 'setFocus', 'setColor',
            'cut', 'copy', 'paste',
            'undo', 'redo', 'isUndoAvailable', 'isRedoAvailable',
            # Export Methods,
            'toAnsi', 'toRawText', 'toPlainText', # 'toHtml', 'toMarkdown',
            # Signals
            'focusChanged', 'currentColorChanged',
            'undoAvailable', 'redoAvailable',
            'textChanged'
        )
    def __init__(self, textEditView=None, lineNumber=False, lineNumberStarting=0, **kwargs):
        super().__init__(**kwargs)
        if 'parent' in kwargs: kwargs.pop('parent')
        self._textEditView = textEditView if textEditView else TTkTextEditView(**kwargs)
        # self.setFocusPolicy(self._textEditView.focusPolicy())
        # self._textEditView.setFocusPolicy(TTkK.ParentFocus)
        self._lineNumber = lineNumber

        textEditLayout = TTkAbstractScrollViewGridLayout()
        textEditLayout.addWidget(self._textEditView,0,1)
        self._lineNumberView = _TTkTextEditViewLineNumber(visible=self._lineNumber, startingNumber=lineNumberStarting)
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
        self.multiLine = self._textEditView.multiLine
        self.setColor = self._textEditView.setColor
        self.cut = self._textEditView.cut
        self.copy = self._textEditView.copy
        self.paste = self._textEditView.paste
        self.undo = self._textEditView.undo
        self.redo = self._textEditView.redo
        self.isUndoAvailable = self._textEditView.isUndoAvailable
        self.isRedoAvailable = self._textEditView.isRedoAvailable
        # Forward export methods
        self.toAnsi      = self._textEditView.toAnsi
        self.toRawText   = self._textEditView.toRawText
        self.toPlainText = self._textEditView.toPlainText
        # self.toHtml      = self._textEditView.toHtml
        # self.toMarkdown  = self._textEditView.toMarkdown
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
        self.textChanged = self._textEditView.textChanged

    def textEditView(self):
        return self._textEditView

    def getLineNumber(self):
        '''getLineNumber'''
        return self._lineNumberView.isVisible()

    @pyTTkSlot(bool)
    def setLineNumber(self, ln):
        '''setLineNumber'''
        self._lineNumberView.setVisible(ln)

    def lineNumberStarting(self):
        return self._lineNumberView._startingNumber

    @pyTTkSlot(int)
    def setLineNumberStarting(self, starting):
        self._lineNumberView._startingNumber = starting
        self._lineNumberView._wrapChanged()

    def setDocument(self, document):
        '''setDocument'''
        self._textEditView.setDocument(document)
        self._lineNumberView.setTextWrap(self._textEditView._textWrap)
