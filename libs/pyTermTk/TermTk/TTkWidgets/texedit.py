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

__all__ = ['TTkTextEditView', 'TTkTextEdit', 'TTkTextEditRuler']

from typing import List,Optional,Union,Dict,Any

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString, TTkStringType
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

from TermTk.TTkGui.clipboard import TTkClipboard
from TermTk.TTkGui.textwrap1 import TTkTextWrap
from TermTk.TTkGui.textcursor import TTkTextCursor
from TermTk.TTkGui.textdocument import TTkTextDocument

from TermTk.TTkWidgets.widget import TTkWidget

from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea, _ForwardData
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView, TTkAbstractScrollViewGridLayout

class TTkTextEditRuler(TTkAbstractScrollView):
    class MarkRuler():
        class States(int):
            NONE      = 0x00
            FLAGGED   = 0x01
            UNFLAGGED = NONE

        # class MarkRulerType(int):
        #     ALLOW_EMPTY  = 0x01
        #     SINGLE_STATE = 0x02
        #     MULTI_STATE  = 0x04

        __slots__ = ('_markers','_states','_width','_lines','_defaultState')
        def __init__(self,
                markers:dict[int,TTkString]) -> None:
            self._lines:Dict[int,int] = {}
            self._markers = markers
            self._states = len(markers)
            self._defaultState = next(iter(markers))
            self._width = max(v.termWidth() for v in markers.values())

        def width(self) -> int:
            return self._width

        def nextState(self, state:int) -> int:
            return (state+1)%self._states

        def setState(self, line:int, state:int) -> None:
            if state == self._defaultState:
                if line in self._lines:
                    del self._lines[line]
            self._lines[line] = state

        def getState(self, line:int) -> int:
            return self._lines.get(line, self._defaultState)

        def getTTkStr(self, line:int) -> TTkString:
            state=self._lines.get(line, self._defaultState)
            return self._markers.get(state, TTkString())

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

    __slots__ = ('_textWrap','_startingNumber', '_markRuler', '_markRulerSizes')
    def __init__(self, startingNumber=0, **kwargs) -> None:
        self._startingNumber:int = startingNumber
        self._textWrap:Optional[TTkTextWrap] = None
        self._markRuler:List[TTkTextEditRuler.MarkRuler] = []
        self._markRulerSizes:List[int] = []
        super().__init__(**kwargs)
        self.setMaximumWidth(2)

    def _wrapChanged(self) -> None:
        if not self._textWrap:
            return
        dt = max(1,self._textWrap._lines[-1][0])
        off  = self._startingNumber
        width = 2+max(len(str(int(dt+off))),len(str(int(off))))
        width += sum(self._markRulerSizes)
        self.setMaximumWidth(width)
        self.update()

    def addMarkRuler(self, markRuler:MarkRuler) -> None:
        self._markRuler.append(markRuler)
        self._markRulerSizes.append(markRuler.width())
        self._wrapChanged()

    def setTextWrap(self, tw:TTkTextWrap) -> None:
        self._textWrap = tw
        tw.wrapChanged.connect(self._wrapChanged)
        self._wrapChanged()

    def viewFullAreaSize(self) -> tuple[int,int]:
        if self._textWrap:
            return 5, self._textWrap.size()
        else:
            return self.size()

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        if not self._markRuler:
            return True
        ox, oy = self.getViewOffsets()
        w, h = self.size()
        mx,my = evt.x+ox, evt.y+oy
        for mk in self._markRuler:
            mx -= mk.width()
            if mx < 0:
                break
        if self._textWrap and my < len(self._textWrap._lines):
            dt = self._textWrap._lines[my][0]
            mk.setState(dt, mk.nextState(mk.getState(dt)))
        else:
            mk.setState(my, mk.nextState(mk.getState(my)))

        self.update()
        return True

    def paintEvent(self, canvas: TTkCanvas) -> None:
        if not self._textWrap: return
        _, oy = self.getViewOffsets()
        w, h = self.size()
        off  = self._startingNumber
        leftOff = sum(self._markRulerSizes)
        sum(self._markRulerSizes)

        style = self.currentStyle()
        color = style['color']
        wrapColor = style['wrapColor']
        separatorColor = style['separatorColor']

        if self._textWrap:
            for i, (dt, (fr, _)) in enumerate(self._textWrap._lines[oy:oy+h]):
                if fr:
                    canvas.drawText(pos=(leftOff,i), text='<', width=w, color=wrapColor)
                else:
                    canvas.drawText(pos=(leftOff,i), text=f"{dt+off}", width=w, color=color)
                canvas.drawChar(pos=(w-1,i), char='▌', color=separatorColor)
        else:
            for y in range(h):
                canvas.drawText(pos=(leftOff,y), text=f"{y+oy+off}", width=w, color=color)
                canvas.drawChar(pos=(w-1,y), char='▌', color=separatorColor)

        ox = 0
        for mk in self._markRuler:
            if self._textWrap:
                for i, (dt, (fr, _)) in enumerate(self._textWrap._lines[oy:oy+h]):
                    if not fr:
                        canvas.drawText(pos=(ox,i), text=mk.getTTkStr(dt+off))
            else:
                for y in range(h):
                    canvas.drawText(pos=(ox,y), text=mk.getTTkStr(dt+off))
            ox += mk.width()

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
        :param cursor: A cursor that contains a selection in a :py:class:`QTextDocument`.
        :type cursor: :py:class:`TTkTextCursor`
        '''

        __slots__ = ('_format', '_color', '_cursor')
        def __init__(self,
                     format:TTkK.SelectionFormat=TTkK.NONE,
                     color:TTkColor=TTkColor.RST,
                     cursor:Optional[TTkTextCursor]=None) -> None:
            self._color = color
            self._format = format
            self._cursor = cursor if cursor else TTkTextCursor()

        def color(self) -> TTkColor:
             '''
             This propery holds the color that is used for the selection.

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
             This propery holds the format that is used to specify the type of selection.

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
             This propery holds the fcursor that contains a selection in a :py:class:`QTextDocument`.

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
        :param lineNumber: Show the line number on the left, defaults to **False**
        :type lineNumber: bool, optional

        :param readOnly: In a read-only text edit the user can only navigate through the text and select text; modifying the text is not possible, defaults to **True**
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
        self._lineWrapMode = TTkK.NoWrap
        self._replace = False
        self._clipboard = TTkClipboard()
        self._setDocument(document)

        super().__init__(**kwargs)

        self.setFocusPolicy(TTkK.ClickFocus | TTkK.TabFocus)
        self.disableWidgetCursor(self._readOnly)
        self._updateSize()
        self.viewChanged.connect(self._pushCursor)

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
        Returns the text of the text edit as ANSI test string.

        This string will insluce the ANSI escape codes for color and text formatting.

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
        if not document:
            document = TTkTextDocument()
        self._textDocument = document
        self._textCursor = TTkTextCursor(document=self._textDocument)
        self._textWrap = TTkTextWrap(document=self._textDocument)
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
        self._textWrap.wrapChanged.disconnect(self.update)
        self._setDocument(document)
        # Trigger an update when the rewrap happen
        self._textWrap.wrapChanged.connect(self.update)

    # forward textWrap Methods
    def wrapWidth(self, *args, **kwargs) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextWrap.wrapWidth`
        '''
        return self._textWrap.wrapWidth(*args, **kwargs)

    def setWrapWidth(self, *args, **kwargs) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextWrap.setWrapWidth`
        '''
        return self._textWrap.setWrapWidth(*args, **kwargs)

    def wordWrapMode(self, *args, **kwargs) -> None:
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
        self._textDocument.clear()
        self._updateSize()

    def lineWrapMode(self) -> TTkK.LineWrapMode:
        '''
        This property holds the line wrap mode

        The default mode is :py:class:`TTkK.LineWrapMode.WidgetWidth` which
        causes words to be wrapped at the right edge of the text edit.
        Wrapping occurs at whitespace, keeping whole words intact.

        :rtype: :py:class:`TTkK.LineWrapMode`
        '''
        return self._lineWrapMode

    def setLineWrapMode(self, mode:TTkK.LineWrapMode):
        '''
        Set the wrapping method

        :param mode: the line wrap mode
        :type mode: :py:class:`TTkK.LineWrapMode`
        '''
        self._lineWrapMode = mode
        if mode == TTkK.LineWrapMode.NoWrap:
            self._textWrap.disable()
        else:
            self._textWrap.enable()
            if mode == TTkK.LineWrapMode.WidgetWidth:
                self._textWrap.setWrapWidth(self.width())
        self._textWrap.rewrap()

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
        Search the match word in the document and place the cursor at the beginning of the matched word.

        :param exp: The match word
        :type exp: str or :py:class:`TTkString`

        :return: `True` if the operation is successful, `False` otherwise
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
        self._rewrap()
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
             w > self._textWrap._tabSpaces ):
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

    def _pushCursor(self) -> None:
        ox, oy = self.getViewOffsets()

        x,y = self._textWrap.dataToScreenPosition(
                self._textCursor.position().line,
                self._textCursor.position().pos)
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

    def pasteEvent(self, txt:TTkStringType) -> None:
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
            # TTkLog.debug(f"Saving {self._textCursor.selectedText()} {self._textCursor._properties[0].anchor.pos}")
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

    def paintEvent(self, canvas: TTkCanvas) -> None:
        ox, oy = self.getViewOffsets()
        w,h = self.size()

        style = self.currentStyle()
        color         = style['color']
        selectColor = style['selectedColor']
        lineColor = style['lineColor']
        backgroundColors = [self._textDocument._backgroundColor]*h

        subLines = self._textWrap._lines[oy:oy+h]
        if not subLines: return
        fr = subLines[0][0]
        to = subLines[-1][0]
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

        for y, l in enumerate(subLines):
            t  = outLines[l[0]-subLines[0][0]]
            bg = backgroundColors[l[0]-subLines[0][0]]
            text:TTkString = t.substring(l[1][0],l[1][1]).tab2spaces(self._textWrap._tabSpaces)
            if bg != TTkColor.RST:
                canvas.fill(color=bg,pos=(0,y), size=(w,1))
                text = text.completeColor(bg)
            canvas.drawTTkString(pos=(-ox,y), text=text)

        if self._lineWrapMode == TTkK.FixedWidth:
            canvas.drawVLine(pos=(self._textWrap._wrapWidth,0), size=h, color=lineColor)



class TTkTextEdit(TTkAbstractScrollArea):
    __doc__ = '''
    :py:class:`TTkTextEdit` is a container widget which place :py:class:`TTkTextEditView` in a scrolling area with on-demand scroll bars.

    ''' + (TTkTextEditView.__doc__ if TTkTextEditView.__doc__ else '')

    ExtraSelection = TTkTextEditView.ExtraSelection

    _ttk_forward:_ForwardData = _ForwardData(
        forwardClass=TTkTextEditView ,
        instance="self._textEditView",
        signals=[ # Forwarded Signals From TTkTexteditView
            'currentColorChanged', 'cursorPositionChanged',
            'undoAvailable', 'redoAvailable',
            'textChanged'],
        methods=[
            # Forwarded Methods From TTkTexteditView
            "clear", "setText", "append", "isReadOnly", "setReadOnly", "document",
            "wrapWidth", "setWrapWidth",
            "multiLine",
            "lineWrapMode", "setLineWrapMode",
            "wordWrapMode", "setWordWrapMode",
            "textCursor", "setFocus", "setColor",
            "extraSelections", "setExtraSelections",
            "cut", "copy", "paste",
            "undo", "redo", "isUndoAvailable", "isRedoAvailable",
            "find", "ensureCursorVisible",
            # Exported Methods
            "toAnsi", "toRawText", "toPlainText" # , "toHtml", "toMarkdown",
            ]
        )

    __slots__ = (
        '_textEditView',
        '_lineNumberView', '_lineNumber')

    def __init__(self, *,
                 # TTkWidget init
                 parent:Optional[TTkWidget]=None,
                 visible:bool=True,

                 # TTkTextEditView init
                 readOnly:bool=False,
                 multiLine:bool=True,
                 document:Optional[TTkTextDocument]=None,

                 # TTkText init
                 textEditView:Optional[TTkTextEditView]=None,
                 lineNumber:bool=False,
                 lineNumberStarting:int=0,
                 **kwargs) -> None:
        '''
        :param textEditView: a custom TextEdit View to be used instead of the default one.
        :type textEditView: :py:class:`TTkTextEditView`, optional
        :param lineNumber: show the line number on the left side, defaults to False
        :type lineNumber: bool, optional
        :param lineNumberStarting: set the starting number of the left line number column, defaults to 0
        :type lineNumberStarting: int, optional
        '''
        super().__init__(parent=parent, visible=visible, **kwargs)
        self._textEditView = textEditView if textEditView else TTkTextEditView(readOnly=readOnly, multiLine=multiLine, document=document)
        # self.setFocusPolicy(self._textEditView.focusPolicy())
        # self._textEditView.setFocusPolicy(TTkK.ParentFocus)
        self._lineNumber = lineNumber

        textEditLayout = TTkAbstractScrollViewGridLayout()
        textEditLayout.addWidget(self._textEditView,0,1)
        self._lineNumberView = TTkTextEditRuler(visible=self._lineNumber, startingNumber=lineNumberStarting)
        self._lineNumberView.setTextWrap(self._textEditView._textWrap)
        textEditLayout.addWidget(self._lineNumberView,0,0)
        self.setViewport(textEditLayout)
        self.focusChanged = self._textEditView.focusChanged

    def ruler(self) -> TTkTextEditRuler:
        '''ruler'''
        return self._lineNumberView

    def textEditView(self):
        '''textEditView'''
        return self._textEditView

    def getLineNumber(self):
        '''getLineNumber'''
        return self._lineNumberView.isVisible()

    @pyTTkSlot(bool)
    def setLineNumber(self, ln):
        '''setLineNumber'''
        self._lineNumberView.setVisible(ln)

    def lineNumberStarting(self):
        '''lineNumberStarting'''
        return self._lineNumberView._startingNumber

    @pyTTkSlot(int)
    def setLineNumberStarting(self, starting):
        '''setLineNumberStarting'''
        self._lineNumberView._startingNumber = starting
        self._lineNumberView._wrapChanged()

    def setDocument(self, document):
        '''setDocument'''
        self._textEditView.setDocument(document)
        self._lineNumberView.setTextWrap(self._textEditView._textWrap)

    #--FORWARD-AUTOGEN-START--#
    @property
    def currentColorChanged(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.currentColorChanged`

        This signal is emitted if the current character color has changed,
        for example caused by a change of the cursor position.
        
        :param color: the new color
        :type color: :py:class:`TTkColor`
        '''
        return self._textEditView.currentColorChanged
    @property
    def cursorPositionChanged(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.cursorPositionChanged`

        This signal is emitted whenever the position of the cursor changed.
        
        :param cursor: the cursor changed.
        :type cursor: :py:class:`TTkTextCursor`
        '''
        return self._textEditView.cursorPositionChanged
    @property
    def undoAvailable(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.undoAvailable`

        This signal is emitted whenever undo operations become available (available is true)
        or unavailable (available is false).
        
        :param available: the availability of undo
        :type available: bool
        '''
        return self._textEditView.undoAvailable
    @property
    def redoAvailable(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.redoAvailable`

        This signal is emitted whenever redo operations become available (available is true)
        or unavailable (available is false).
        
        :param available: the availability of redo
        :type available: bool
        '''
        return self._textEditView.redoAvailable
    @property
    def textChanged(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.textChanged`

        This signal is emitted whenever the document's content changes;
        for example, when text is inserted or deleted, or when formatting is applied.
        '''
        return self._textEditView.textChanged
    def clear(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.clear`

        Deletes all the text in the text edit.

        .. note::

            The undo/redo history is also cleared.
        '''
        return self._textEditView.clear()
    @pyTTkSlot(TTkStringType)
    def setText(self, text:TTkStringType) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setText`

        Sets the text edit's text.
        The text can be plain text or :py:class:`TTkString` and the text edit will
        try to guess the right format.

        :param text: the text
        :type text: str or :py:class:`TTkString`
        '''
        return self._textEditView.setText(text=text)
    @pyTTkSlot(TTkStringType)
    def append(self, text:TTkStringType) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.append`

        Appends a new paragraph with text to the end of the text edit.
        The text can be plain text or :py:class:`TTkString`.

        :param text: the text
        :type text: str or :py:class:`TTkString`
        '''
        return self._textEditView.append(text=text)
    def isReadOnly(self) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.isReadOnly`

        This property holds whether the text edit is read-only

        In a read-only text edit the user can only navigate through the text and select text; modifying the text is not possible.

        This property's default is false.

        :rtype: bool
        '''
        return self._textEditView.isReadOnly()
    def setReadOnly(self, ro:bool) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setReadOnly`

        This property holds whether the text edit is read-only

        In a read-only text edit the user can only navigate through the text and select text; modifying the text is not possible.

        :param ro: the readonly status
        :type ro: bool
        '''
        return self._textEditView.setReadOnly(ro=ro)
    def document(self) -> TTkTextDocument:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.document`

        This property holds the underlying document of the text editor.

        :rtype: :py:class:`TTkTextDocument`
        '''
        return self._textEditView.document()
    def wrapWidth(self, *args, **kwargs) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.wrapWidth`

        .. seealso:: this method is forwarded to :py:meth:`TTkTextWrap.wrapWidth`
        '''
        return self._textEditView.wrapWidth(*args, **kwargs)
    def setWrapWidth(self, *args, **kwargs) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setWrapWidth`

        .. seealso:: this method is forwarded to :py:meth:`TTkTextWrap.setWrapWidth`
        '''
        return self._textEditView.setWrapWidth(*args, **kwargs)
    def multiLine(self) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.multiLine`

        This property define if the text edit area will use a single line, like in the line-edit or it allows multilines like a normal text edit area.

        :rtype: bool
        '''
        return self._textEditView.multiLine()
    def lineWrapMode(self) -> TTkK.LineWrapMode:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.lineWrapMode`

        This property holds the line wrap mode

        The default mode is :py:class:`TTkK.LineWrapMode.WidgetWidth` which
        causes words to be wrapped at the right edge of the text edit.
        Wrapping occurs at whitespace, keeping whole words intact.

        :rtype: :py:class:`TTkK.LineWrapMode`
        '''
        return self._textEditView.lineWrapMode()
    def setLineWrapMode(self, mode:TTkK.LineWrapMode):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setLineWrapMode`

        Set the wrapping method

        :param mode: the line wrap mode
        :type mode: :py:class:`TTkK.LineWrapMode`
        '''
        return self._textEditView.setLineWrapMode(mode=mode)
    def wordWrapMode(self, *args, **kwargs) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.wordWrapMode`

        .. seealso:: this method is forwarded to :py:meth:`TTkTextWrap.wordWrapMode`
        '''
        return self._textEditView.wordWrapMode(*args, **kwargs)
    def setWordWrapMode(self, *args, **kwargs) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setWordWrapMode`

        .. seealso:: this method is forwarded to :py:meth:`TTkTextWrap.setWordWrapMode`
        '''
        return self._textEditView.setWordWrapMode(*args, **kwargs)
    def textCursor(self) -> TTkTextCursor:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.textCursor`

        This property holds the underlying text cursor.

        :rtype: :py:class:`TTkTextCursor`
        '''
        return self._textEditView.textCursor()
    @pyTTkSlot()
    def setFocus(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setFocus`

        Focus the widget
        '''
        return self._textEditView.setFocus()
    @pyTTkSlot(TTkColor)
    def setColor(self, color:TTkColor) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setColor`

        Change the color used by the cursor to input new text or change the color of the selection

        :param color: the color to be used
        :type color: :py:class:`TTkColor`
        '''
        return self._textEditView.setColor(color=color)
    def extraSelections(self) -> List[ExtraSelection]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.extraSelections`

        Returns previously set extra selections.

        :rtype: List[:py:class:`ExtraSelection`]
        '''
        return self._textEditView.extraSelections()
    def setExtraSelections(self, extraSelections:List[ExtraSelection]) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setExtraSelections`

        This function allows temporarily marking certain regions in the document with a given color,
        specified as selections. This can be useful for example in a programming editor to mark a
        whole line of text with a given background color to indicate the existence of a breakpoint.

        :param extraSelections: the list of extra selections.
        :type extraSelections: List[:py:class:`ExtraSelection`]
        '''
        return self._textEditView.setExtraSelections(extraSelections=extraSelections)
    @pyTTkSlot()
    def cut(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.cut`

        Copies the selected text to the clipboard and deletes it from the text edit.

        If there is no selected text nothing happens.
        '''
        return self._textEditView.cut()
    @pyTTkSlot()
    def copy(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.copy`

        Copies any selected text to the clipboard.
        '''
        return self._textEditView.copy()
    @pyTTkSlot()
    def paste(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.paste`

        Pastes the text from the clipboard into the text edit at the current cursor position.

        If there is no text in the clipboard nothing happens.
        '''
        return self._textEditView.paste()
    @pyTTkSlot()
    def undo(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.undo`

        Undoes the last operation.

        If there is no operation to undo,
        i.e. there is no undo step in the undo/redo history, nothing happens.
        '''
        return self._textEditView.undo()
    @pyTTkSlot()
    def redo(self) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.redo`

        Redoes the last operation.

        If there is no operation to redo,
        i.e. there is no redo step in the undo/redo history, nothing happens.
        '''
        return self._textEditView.redo()
    def isUndoAvailable(self) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.isUndoAvailable`

        This property holds whether undo is available.

        :return: the undo available status
        :rtype: bool
        '''
        return self._textEditView.isUndoAvailable()
    def isRedoAvailable(self) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.isRedoAvailable`

        This property holds whether redo is available.

        :return: the redo available status
        :rtype: bool
        '''
        return self._textEditView.isRedoAvailable()
    @pyTTkSlot(TTkStringType)
    def find(self, exp:TTkStringType) -> bool:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.find`

        Search the match word in the document and place the cursor at the beginning of the matched word.

        :param exp: The match word
        :type exp: str or :py:class:`TTkString`

        :return: `True` if the operation is successful, `False` otherwise
        :rtype: bool
        '''
        return self._textEditView.find(exp=exp)
    @pyTTkSlot()
    def ensureCursorVisible(self):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.ensureCursorVisible`

        '''
        return self._textEditView.ensureCursorVisible()
    def toAnsi(self) -> str:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.toAnsi`

        Returns the text of the text edit as ANSI test string.

        This string will insluce the ANSI escape codes for color and text formatting.

        :rtype: str
        '''
        return self._textEditView.toAnsi()
    def toRawText(self) -> TTkString:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.toRawText`

        Return :py:class:`TTkString` representing the document

        :rtype: :py:class:`TTkString`
        '''
        return self._textEditView.toRawText()
    def toPlainText(self) ->str:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.toPlainText`

        Returns the text of the text edit as plain text string.

        :rtype: str
        '''
        return self._textEditView.toPlainText()
    #--FORWARD-AUTOGEN-END--#