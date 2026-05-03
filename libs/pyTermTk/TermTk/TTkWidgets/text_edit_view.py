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

__all__ = ['TTkTextEditView']

from dataclasses import dataclass
from typing import List,Optional

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString, TTkStringType
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

from TermTk.TTkGui.clipboard import TTkClipboard
from TermTk.TTkGui.textcursor import TTkTextCursor
from TermTk.TTkGui.textdocument import TTkTextDocument
from TermTk.TTkGui.TTkTextWrap.text_wrap import TTkTextWrap

from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

@dataclass
class _TextEditLineMap():
    line: int = 0
    line_pos: int = 0
    '''The Document logical Line'''
    pos_y: int = 0
    '''The screen y position'''

class TTkTextEditView(TTkAbstractScrollView):
    '''
    :py:class:`TTkTextEditView`

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

    Demo: :ttk:sbIntLink:`demo/showcase,textedit.py`

    :ref:`ttkdesigner Tutorial <TextEdit_ttkDesigner-Tutorial_Intro>`
    '''


    class ExtraSelection():
        '''
        The :py:class:`ExtraSelection` structure provides a way of specifying a character format for a given selection in a document.

        :param format: A format that is used to specify the type of selection, defaults to :py:class:`TTkK.NONE`.
        :type format: :py:class:`TTkK.SelectionFormat`
        :param color: The color used to specify the foreground/background color/mod for the selection.
        :type color: :py:class:`TTkColor`
        :param cursor: A cursor that contains a selection in a :py:class:`TTkTextDocument`.
        :type cursor: :py:class:`TTkTextCursor`
        '''

        __slots__ = ('_format', '_color', '_cursor')
        def __init__(self,
                     cursor:TTkTextCursor,
                     format:TTkK.SelectionFormat=TTkK.SelectionFormat.NONE,
                     color:TTkColor=TTkColor.RST) -> None:
            self._color = color
            self._format = format
            self._cursor = cursor

        def color(self) -> TTkColor:
             '''
               This property holds the color that is used for the selection.

             :rtype: :py:class:`TTkColor`
             '''
             return self._color

        def setColor(self, color:TTkColor) -> None:
            '''
            Set the color.

            :param color: A color that is used for the selection.
            :type color: :py:class:`TTkColor`
            '''
            self._color = color

        def format(self) -> TTkK.SelectionFormat:
             '''
               This property holds the format that is used to specify the type of selection.

             :rtype: :py:class:`TTkK.SelectionFormat`
             '''
             return self._format

        def setFormat(self, format:TTkK.SelectionFormat) -> None:
            '''
            Set the format.

            :param format: A format that is used to specify the type of selection.
            :type format: :py:class:`TTkK.SelectionFormat`
            '''
            self._format = format

        def cursor(self) -> TTkTextCursor:
             '''
               This property holds the cursor that contains a selection in a :py:class:`TTkTextDocument`.

             :rtype: :py:class:`TTkTextCursor`
             '''
             return self._cursor

        def setCursor(self, cursor:TTkTextCursor) -> None:
            '''
            Set the cursor.

            :param cursor: A cursor that contains a selection in a :py:class:`QTextDocument`.
            :type cursor: :py:class:`TTkTextCursor`
            '''
            self._cursor = cursor

    @property
    def currentColorChanged(self) -> pyTTkSignal:
        '''
        This signal is emitted if the current character color has changed,
        for example caused by a change of the cursor position.

        :param color: the new color
        :type color: :py:class:`TTkColor`
        '''
        return self._currentColorChanged

    @property
    def cursorPositionChanged(self) -> pyTTkSignal:
        '''
        This signal is emitted whenever the position of the cursor changed.

        :param cursor: the cursor changed.
        :type cursor: :py:class:`TTkTextCursor`
        '''
        return self._cursorPositionChanged_sig

    @property
    def undoAvailable(self) -> pyTTkSignal:
        '''
        This signal is emitted whenever undo operations become available (available is true)
        or unavailable (available is false).

        :param available: the availability of undo
        :type available: bool
        '''
        return self._undoAvailable_sig

    @property
    def redoAvailable(self) -> pyTTkSignal:
        '''
        This signal is emitted whenever redo operations become available (available is true)
        or unavailable (available is false).

        :param available: the availability of redo
        :type available: bool
        '''
        return self._redoAvailable_sig

    @property
    def textChanged(self) -> pyTTkSignal:
        '''
        This signal is emitted whenever the document's content changes;
        for example, when text is inserted or deleted, or when formatting is applied.
        '''
        return self._textChanged

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
            '_textCursor',
            '_extraSelections',
            '_textWrap', '_lineWrapMode', '_lastWrapUsed',
            '_replace',
            '_readOnly', '_multiCursor',
            '_clipboard',
            '_lineMap',
            # '_preview', '_previewWidth',
            '_multiLine',
            # # Forwarded Methods
            # 'wrapWidth',    'setWrapWidth',
            # 'wordWrapMode', 'setWordWrapMode',
            # Signals
            '_currentColorChanged', '_cursorPositionChanged_sig',
            '_undoAvailable_sig', '_redoAvailable_sig',
            '_textChanged'
        )

    _textWrap:TTkTextWrap
    _textDocument:TTkTextDocument
    _textCursor:TTkTextCursor
    _lineMap: _TextEditLineMap

    #    in order to support the line wrap, I need to divide the full data text in;
    #    _textDocument = the entire text divided in lines, easy to add/remove/append lines
    #    _textWrap._lines     = an array of tuples for each displayed line with a pointer to a
    #                 specific line and its slice to be shown at this coordinate;
    #                 [ (line, (posFrom, posTo)), ... ]
    #                 This is required to support the wrap feature

    def __init__(self, *,
                 readOnly:bool=False,
                 multiLine:bool=True,
                 document:Optional[TTkTextDocument]=None,
                 **kwargs) -> None:
        '''
        :param readOnly: In a read-only text edit the user can only navigate through the text and select text; modifying the text is not possible, defaults to **False**
        :type readOnly: bool, optional

        :param multiLine: In a multiline text edit the user can split the text in multiple lines, defaults to **True**
        :type multiLine: bool, optional

        :param document: If required an external Document can be used in this text editor, this option is useful if multiple editors share the same document as in the `demo <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/sandbox.html?filePath=demo/showcase/textedit.py>`__, defaults to a new Document
        :type document: :py:class:`TTkTextDocument`, optional
        '''

        self._currentColorChanged = pyTTkSignal(TTkColor)
        self._cursorPositionChanged_sig = pyTTkSignal(TTkTextCursor)
        self._undoAvailable_sig = pyTTkSignal(bool)
        self._redoAvailable_sig = pyTTkSignal(bool)
        self._textChanged = pyTTkSignal()

        self._readOnly:bool = readOnly
        self._multiLine:bool = multiLine
        self._multiCursor:bool = True
        self._extraSelections:List[TTkTextEditView.ExtraSelection] = []
        self._hsize:int = 0
        self._lastWrapUsed  = 0
        self._lineWrapMode = TTkK.LineWrapMode.NoWrap
        self._replace = False
        self._clipboard = TTkClipboard()
        self._setDocument(document)

        super().__init__(**kwargs)

        self.setFocusPolicy(TTkK.ClickFocus | TTkK.TabFocus)
        self.disableWidgetCursor(self._readOnly)
        self._updateSize()
        self.viewMovedTo.connect(self._view_moved_event)
        self.viewChanged.connect(self._pushCursor)
        # self.viewChanged.connect(self._check_document_wrap_position)

    def multiLine(self) -> bool:
        '''
        This property define if the text edit area will use a single line, like in the line-edit or it allows multilines like a normal text edit area.

        :rtype: bool
        '''
        return self._multiLine

    @pyTTkSlot(bool)
    def _undoAvailable(self, available) -> None:
        self.undoAvailable.emit(available)

    @pyTTkSlot(bool)
    def _redoAvailable(self, available) -> None:
        self.redoAvailable.emit(available)

    # def toHtml(self, encoding): pass
    #    if self._textDocument:
    #        return self._textDocument.toHtml()
    #    return ""

    # def toMarkdown(self, features): pass
    #    if self._textDocument:
    #        return self._textDocument.toMarkdown()
    #    return ""

    def toAnsi(self) -> str:
        '''
        Returns the text of the text edit as ANSI text string.

        This string will include the ANSI escape codes for color and text formatting.

        :rtype: str
        '''
        if self._textDocument:
            return self._textDocument.toAnsi()
        return ""

    def toPlainText(self) ->str:
        '''
        Returns the text of the text edit as plain text string.

        :rtype: str
        '''
        if self._textDocument:
            return self._textDocument.toPlainText()
        return ""

    def toRawText(self) -> TTkString:
        '''
        Return :py:class:`TTkString` representing the document

        :rtype: :py:class:`TTkString`
        '''
        if self._textDocument:
            return self._textDocument.toRawText()
        return TTkString()

    def isUndoAvailable(self) -> bool:
        '''
        This property holds whether undo is available.

        :return: the undo available status
        :rtype: bool
        '''
        if self._textDocument:
            return self._textDocument.isUndoAvailable()
        return False

    def isRedoAvailable(self) -> bool:
        '''
        This property holds whether redo is available.

        :return: the redo available status
        :rtype: bool
        '''
        if self._textDocument:
            return self._textDocument.isRedoAvailable()
        return False

    def document(self) -> TTkTextDocument:
        '''
        This property holds the underlying document of the text editor.

        :rtype: :py:class:`TTkTextDocument`
        '''
        return self._textDocument

    def _setDocument(self, document:Optional[TTkTextDocument]) -> None:
        self._lineMap = _TextEditLineMap()
        if not document:
            document = TTkTextDocument()
        self._textDocument = document
        self._textCursor = TTkTextCursor(document=self._textDocument)
        self._textWrap = TTkTextWrap(document=self._textDocument)
        self._textWrap.wrapChanged.connect(self._wrapChanged)
        self._textDocument.contentsChanged.connect(self._documentChanged)
        self._textDocument.cursorPositionChanged.connect(self._cursorPositionChanged)
        self._textDocument.undoAvailable.connect(self._undoAvailable)
        self._textDocument.redoAvailable.connect(self._redoAvailable)
        self._textDocument.formatChanged.connect(self.update)

    def setDocument(self, document:TTkTextDocument) -> None:
        '''
        Set the underlying document of the text editor.

        :param document: the text document
        :type document: :py:class:`TTkTextDocument`
        '''
        self._textDocument.contentsChanged.disconnect(self._documentChanged)
        self._textDocument.cursorPositionChanged.disconnect(self._cursorPositionChanged)
        self._textDocument.undoAvailable.disconnect(self._undoAvailable)
        self._textDocument.redoAvailable.disconnect(self._redoAvailable)
        self._textDocument.formatChanged.disconnect(self.update)
        self._textWrap.wrapChanged.disconnect(self._wrapChanged)
        self._setDocument(document)

    @pyTTkSlot()
    def _wrapChanged(self):
        line = self._lineMap.line
        line_pos = self._lineMap.line_pos
        pos_y = self._lineMap.pos_y
        screen_position = self._textWrap.dataToScreenPosition(line, line_pos)
        if screen_position.extra is not None:
            screen_y = screen_position.extra.y
        else:
            screen_y = screen_position.main.y
        if screen_y != pos_y:
            ox, oy = self.getViewOffsets()
            self.viewMoveTo(ox, screen_y)
        else:
            self.update()

    # forward textWrap Methods
    def wrapWidth(self, *args, **kwargs) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextWrap.wrapWidth`
        '''
        return self._textWrap.wrapWidth(*args, **kwargs)

    def setWrapWidth(self, *args, **kwargs) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextWrap.setWrapWidth`
        '''
        return self._textWrap.setWrapWidth(*args, **kwargs)

    def wordWrapMode(self, *args, **kwargs) -> TTkK.WrapMode:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextWrap.wordWrapMode`
        '''
        return self._textWrap.wordWrapMode(*args, **kwargs)

    def setWordWrapMode(self, *args, **kwargs) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextWrap.setWordWrapMode`
        '''
        return self._textWrap.setWordWrapMode(*args, **kwargs)

    def extraSelections(self) -> List[ExtraSelection]:
        '''
        Returns previously set extra selections.

        :rtype: List[:py:class:`ExtraSelection`]
        '''
        return self._extraSelections

    def setExtraSelections(self, extraSelections:List[ExtraSelection]) -> None:
        '''
        This function allows temporarily marking certain regions in the document with a given color,
        specified as selections. This can be useful for example in a programming editor to mark a
        whole line of text with a given background color to indicate the existence of a breakpoint.

        :param extraSelections: the list of extra selections.
        :type extraSelections: List[:py:class:`ExtraSelection`]
        '''
        self._extraSelections = extraSelections
        self.update()

    def textCursor(self) -> TTkTextCursor:
        '''
        This property holds the underlying text cursor.

        :rtype: :py:class:`TTkTextCursor`
        '''
        return self._textCursor

    def isReadOnly(self) -> bool:
        '''
        This property holds whether the text edit is read-only

        In a read-only text edit the user can only navigate through the text and select text; modifying the text is not possible.

        This property's default is false.

        :rtype: bool
        '''
        return self._readOnly

    def setReadOnly(self, ro:bool) -> None:
        '''
        This property holds whether the text edit is read-only

        In a read-only text edit the user can only navigate through the text and select text; modifying the text is not possible.

        :param ro: the readonly status
        :type ro: bool
        '''
        self._readOnly = ro
        self.disableWidgetCursor(ro)

    def clear(self) -> None:
        '''
        Deletes all the text in the text edit.

        .. note::

            The undo/redo history is also cleared.
        '''
        self.viewMoveTo(0, 0)
        self._setCursorPos(0,0)
        self._textDocument.clear()
        self._updateSize()

    def lineWrapMode(self) -> TTkK.LineWrapMode:
        '''
        This property holds the line wrap mode

        The default mode is :py:class:`TTkK.LineWrapMode.NoWrap`.

        :rtype: :py:class:`TTkK.LineWrapMode`
        '''
        return self._lineWrapMode

    def setLineWrapMode(self, mode:TTkK.LineWrapMode, wrapEngine:TTkK.WrapEngine=TTkK.WrapEngine.FullWrap) -> None:
        '''
        Set the wrapping method

        :param mode: the line wrap mode
        :type mode: :py:class:`TTkK.LineWrapMode`
        :param wrapEngine: the wrap engine used when wrapping is enabled
        :type wrapEngine: :py:class:`TTkK.WrapEngine`
        '''
        if self._lineWrapMode == mode and self._textWrap.engine() == wrapEngine:
            return
        self._lineWrapMode = mode
        if mode == TTkK.LineWrapMode.NoWrap:
            self._textWrap.setEngine(engine=TTkK.WrapEngine.NoWrap)
        elif mode == TTkK.LineWrapMode.WidgetWidth:
            self._textWrap.setEngine(engine=wrapEngine, width=self.width())
        else:
            self._textWrap.setEngine(engine=wrapEngine)

    @pyTTkSlot(TTkStringType)
    def setText(self, text:TTkStringType) -> None:
        '''
        Sets the text edit's text.
        The text can be plain text or :py:class:`TTkString` and the text edit will
        try to guess the right format.

        :param text: the text
        :type text: str or :py:class:`TTkString`
        '''
        self.viewMoveTo(0, 0)
        self._textDocument.setText(text)
        self._updateSize()

    @pyTTkSlot(TTkStringType)
    def append(self, text:TTkStringType) -> None:
        '''
        Appends a new paragraph with text to the end of the text edit.
        The text can be plain text or :py:class:`TTkString`.

        :param text: the text
        :type text: str or :py:class:`TTkString`
        '''
        self._textDocument.appendText(text)
        self._updateSize()

    @pyTTkSlot()
    def undo(self) -> None:
        '''
        Undoes the last operation.

        If there is no operation to undo,
        i.e. there is no undo step in the undo/redo history, nothing happens.
        '''
        if c := self._textDocument.restoreSnapshotPrev():
            self._textCursor.restore(c)

    @pyTTkSlot()
    def redo(self) -> None:
        '''
        Redoes the last operation.

        If there is no operation to redo,
        i.e. there is no redo step in the undo/redo history, nothing happens.
        '''
        if c := self._textDocument.restoreSnapshotNext():
            self._textCursor.restore(c)

    @pyTTkSlot(TTkStringType)
    def find(self, exp:TTkStringType) -> bool:
        '''
        Search for text in the document and place the cursor at the beginning of the first match.

        :param exp: the expression to find
        :type exp: str or :py:class:`TTkString`

        :return: ``True`` if the operation is successful, ``False`` otherwise
        :rtype: bool
        '''
        if not (cursor := self._textDocument.find(exp)):
            return False
        self._textCursor = cursor
        self._textDocument.cursorPositionChanged.emit(self._textCursor)
        return True

    @pyTTkSlot()
    def copy(self) -> None:
        '''
        Copies any selected text to the clipboard.
        '''
        if not self._textCursor.hasSelection():
            txt = TTkString('\n').join(self._textCursor.getLinesUnderCursor())
        else:
            txt = self._textCursor.selectedText()
        self._clipboard.setText(txt)

    @pyTTkSlot()
    def cut(self) -> None:
        '''
        Copies the selected text to the clipboard and deletes it from the text edit.

        If there is no selected text nothing happens.
        '''
        if not self._textCursor.hasSelection():
            self._textCursor.movePosition(moveMode=TTkTextCursor.MoveAnchor, operation=TTkTextCursor.StartOfLine)
            self._textCursor.movePosition(moveMode=TTkTextCursor.KeepAnchor, operation=TTkTextCursor.EndOfLine)
            self._textCursor.movePosition(moveMode=TTkTextCursor.KeepAnchor, operation=TTkTextCursor.Right)
        self.copy()
        self._textCursor.removeSelectedText()

    @pyTTkSlot()
    def paste(self) -> None:
        '''
        Pastes the text from the clipboard into the text edit at the current cursor position.

        If there is no text in the clipboard nothing happens.
        '''
        txt = self._clipboard.text()
        self.pasteEvent(txt)

    @pyTTkSlot()
    def _documentChanged(self) -> None:
        self.textChanged.emit()

    def _rewrap(self) -> None:
        self._textWrap.rewrap()
        self.viewChanged.emit()
        self.update()

    @pyTTkSlot(TTkColor)
    def setColor(self, color:TTkColor) -> None:
        '''
        Change the color used by the cursor to input new text or change the color of the selection

        :param color: the color to be used
        :type color: :py:class:`TTkColor`
        '''
        self.textCursor().setColor(color)

    @pyTTkSlot(TTkTextCursor)
    def _cursorPositionChanged(self, cursor:TTkTextCursor) -> None:
        if cursor == self._textCursor:
            self.currentColorChanged.emit(cursor.positionColor())
            self.cursorPositionChanged.emit(cursor)
            self._pushCursor()

    def resizeEvent(self, w:int, h:int) -> None:
        if ( self.lineWrapMode() == TTkK.WidgetWidth and
             w != self._lastWrapUsed and
             w > self._textWrap._wrapState.tabSpaces ):
            self._textWrap.setWrapWidth(w)
            self._lastWrapUsed = w
            self._rewrap()
        return super().resizeEvent(w,h)

    def _updateSize(self) -> None:
        self._hsize = max( len(l) for l in self._textDocument._dataLines ) + 1

    def viewFullAreaSize(self) -> tuple[int,int]:
        if self.lineWrapMode() == TTkK.NoWrap:
            return self._hsize, self._textWrap.size()
        elif self.lineWrapMode() == TTkK.WidgetWidth:
            return self.width(), self._textWrap.size()
        elif self.lineWrapMode() == TTkK.FixedWidth:
            return self.width(), self._textWrap.size()
        return self.width(), self._textWrap.size()

    # @pyTTkSlot()
    # def _check_document_wrap_position(self):
    #     ox, oy = self.getViewOffsets()
    #     w, h = self.size()
    #     y = self._textWrap.screenRows(oy,h).y
    #     if y == oy:
    #         return
    #     self.viewMoveTo(ox, y)

    @pyTTkSlot(int,int)
    def _view_moved_event(self, x:int, y:int):
        h = self.height()
        screen_rows = self._textWrap.screenRows(y,h)
        self._lineMap.line = 0 if not screen_rows.rows else screen_rows.rows[0].line
        self._lineMap.line_pos = 0 if not screen_rows.rows else screen_rows.rows[0].start
        self._lineMap.pos_y = y

    @pyTTkSlot()
    def _pushCursor(self, moving_left:bool=False) -> None:
        ox, oy = self.getViewOffsets()

        screen_position = self._textWrap.dataToScreenPosition(
                self._textCursor.position().line,
                self._textCursor.position().pos)

        if moving_left and screen_position.extra is not None:
            x,y = screen_position.extra.to_xy()
        else:
            x,y = screen_position.main.to_xy()

        y -= oy
        x -= ox

        if self._replace:
            self.setWidgetCursor(pos=(x,y), type=TTkK.Cursor_Blinking_Block)
        else:
            self.setWidgetCursor(pos=(x,y), type=TTkK.Cursor_Blinking_Bar)

        self.update()

    def _setCursorPos(self, x, y, moveAnchor=True, addCursor=False) -> tuple[int,int]:
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

    @pyTTkSlot()
    def ensureCursorVisible(self):
        cp = self._textCursor.position()
        self._scrolToInclude(cp.pos,cp.line)

    def _scrolToInclude(self, x, y) -> None:
        # Scroll the area (if required) to include the position x,y
        _,_,w,h = self.geometry()
        offx, offy = self.getViewOffsets()
        offx = max(min(offx, x),x-w+1)
        offy = max(min(offy, y),y-h+1)
        self.viewMoveTo(offx, offy)

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        if self._readOnly:
            return super().mousePressEvent(evt)
        ox, oy = self.getViewOffsets()
        self._setCursorPos(evt.x + ox, evt.y + oy, addCursor=evt.mod&TTkK.ControlModifier==TTkK.ControlModifier)
        self._textCursor.clearColor()
        self._pushCursor()
        self.update()
        return True

    def mouseReleaseEvent(self, evt:TTkMouseEvent) -> bool:
        if self._textCursor.hasSelection():
            self.copy()
        return True

    def mouseDragEvent(self, evt:TTkMouseEvent) -> bool:
        if self._readOnly:
            return super().mouseDragEvent(evt)
        ox, oy = self.getViewOffsets()
        x,y = self._setCursorPos(evt.x + ox, evt.y + oy, moveAnchor=False)
        self._textCursor.clearColor()
        self._scrolToInclude(x,y)
        self._pushCursor()
        self.update()
        return True

    def mouseDoubleClickEvent(self, evt:TTkMouseEvent) -> bool:
        if self._readOnly:
            return super().mouseDoubleClickEvent(evt)
        self._textCursor.select(TTkTextCursor.WordUnderCursor)
        if self._textCursor.hasSelection():
            self.copy()
        self._textCursor.clearColor()
        self._pushCursor()
        self.update()
        return True

    def mouseTapEvent(self, evt:TTkMouseEvent) -> bool:
        if self._readOnly:
            return super().mouseTapEvent(evt)
        self._textCursor.select(TTkTextCursor.LineUnderCursor)
        if self._textCursor.hasSelection():
            self.copy()
        self._textCursor.clearColor()
        self._pushCursor()
        self.update()
        return True

    def pasteEvent(self, txt:TTkStringType) -> bool:
        txt = TTkString(txt)
        if not self._multiLine:
            txt = TTkString().join(txt.split('\n'))
        if self._replace:
            self._textCursor.replaceText(txt, moveCursor=True)
        else:
            self._textCursor.insertText(txt, moveCursor=True)
        # Scroll to align to the cursor
        p = self._textCursor.position()
        cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos).to_xy()
        self._updateSize()
        self._scrolToInclude(cx,cy)
        self._pushCursor()
        self.update()
        return True

    def keyEvent(self, evt: TTkKeyEvent) -> bool:
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
            self._textDocument.saveSnapshot(self._textCursor.copy())

        if evt.key == TTkK.Key_Tab and evt.mod==TTkK.NoModifier:
            evt = TTkKeyEvent(TTkK.Character, '\t', '\t', TTkK.NoModifier)

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

            if ctrl:
                p = self._textCursor.position()
                cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos).to_xy()
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
                elif evt.key == TTkK.Key_A:
                    self._textCursor.select(TTkTextCursor.SelectionType.Document)
                else:
                    # No action performed
                    return super().keyEvent(evt)
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
            else:
                # No action performed
                return super().keyEvent(evt)
            # Scroll to align to the cursor
            p = self._textCursor.position()
            cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos).to_xy()
            self._updateSize()
            self._scrolToInclude(cx,cy)
            self._pushCursor(evt.key == TTkK.Key_Left)
            self.update()
            return True
        else: # Input char
            if self._replace:
                self._textCursor.replaceText(str(evt.key), moveCursor=True)
            else:
                self._textCursor.insertText(str(evt.key), moveCursor=True)
            # Scroll to align to the cursor
            p = self._textCursor.position()
            cx, cy = self._textWrap.dataToScreenPosition(p.line, p.pos).to_xy()
            self._updateSize()
            self._scrolToInclude(cx,cy)
            self._pushCursor()
            self.update()
            return True

        return super().keyEvent(evt)

    def paintEvent(self, canvas: TTkCanvas) -> None:
        ox, oy = self.getViewOffsets()
        w,h = self.size()

        style = self.currentStyle()
        color         = style['color']
        selectColor = style['selectedColor']
        lineColor = style['lineColor']
        backgroundColors = [self._textDocument._backgroundColor]*h

        subLines = self._textWrap.screenRows(oy,+h).rows
        if not subLines: return
        fr = subLines[0].line
        to = subLines[-1].line
        outLines = self._textDocument._dataLines[fr:to+1]
        outLines = self._textCursor._getHighlightedLines(fr, to, outLines, selectColor)

        for extraSelection in self._extraSelections:
            esCursor = extraSelection._cursor
            esColor  = extraSelection._color
            esFormat = extraSelection._format
            if esFormat == TTkK.SelectionFormat.FullWidthSelection:
                backgroundColors = esCursor._getCoveredLines(fr, to, backgroundColors, esColor)
            outLines = esCursor._getHighlightedLines(fr, to, outLines, esColor)

        outLines = self._textCursor._getBlinkingCursors(fr, to, outLines, selectColor)

        for y, row in enumerate(subLines):
            t  = outLines[row.line-subLines[0].line]
            bg = backgroundColors[row.line-subLines[0].line]
            text:TTkString = t.substring(row.start,row.stop).tab2spaces(self._textWrap._wrapState.tabSpaces)
            if bg != TTkColor.RST:
                canvas.fill(color=bg,pos=(0,y), size=(w,1))
                text = text.completeColor(bg)
            canvas.drawTTkString(pos=(-ox,y), text=text)

        if self._lineWrapMode == TTkK.FixedWidth:
            canvas.drawVLine(pos=(self._textWrap.wrapWidth(),0), size=h, color=lineColor)