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

from typing import List,Optional,TYPE_CHECKING

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString, TTkStringType
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot

from TermTk.TTkGui.textcursor import TTkTextCursor
from TermTk.TTkGui.textdocument import TTkTextDocument

from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.text_edit_view import TTkTextEditView
from TermTk.TTkWidgets.text_edit_ruler import TTkTextEditRuler

from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea, _ForwardData
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollViewGridLayout

try:
    from typing import TypeAlias
except ImportError:
    # TODO: Remove this workaround for Python 3.9
    TypeAlias = type  # Fallback for Python < 3.10 without typing_extensions

class TTkTextEdit(TTkAbstractScrollArea):
    __doc__ = '''
    :py:class:`TTkTextEdit` is a container widget which place :py:class:`TTkTextEditView` in a scrolling area with on-demand scroll bars.

    ''' + (TTkTextEditView.__doc__ or '')

    ExtraSelection: TypeAlias = TTkTextEditView.ExtraSelection

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
            "followMode", "setFollowMode",
            "scrollTo",
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
                 followMode:TTkK.TextEditFollow=TTkK.TextEditFollow.NEVER,

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
        self._textEditView = textEditView if textEditView else TTkTextEditView(readOnly=readOnly, multiLine=multiLine, document=document, followMode=followMode)
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
    def wrapWidth(self) -> int:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.wrapWidth`

        Return the current wrap width in terminal cells.

        :return: wrap width.
        :rtype: int
        '''
        return self._textEditView.wrapWidth()
    def setWrapWidth(self, width:int) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setWrapWidth`

        Set wrap width and trigger a full rewrap.

        :param width: target width in terminal cells.
        :type width: int
        '''
        return self._textEditView.setWrapWidth(width=width)
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

        The default mode is :py:class:`TTkK.LineWrapMode.NoWrap`.

        :rtype: :py:class:`TTkK.LineWrapMode`
        '''
        return self._textEditView.lineWrapMode()
    def setLineWrapMode(self, mode:TTkK.LineWrapMode, wrapEngine:TTkK.WrapEngine=TTkK.WrapEngine.FullWrap) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setLineWrapMode`

        Set the wrapping method

        :param mode: the line wrap mode
        :type mode: :py:class:`TTkK.LineWrapMode`
        :param wrapEngine: the wrap engine used when wrapping is enabled
        :type wrapEngine: :py:class:`TTkK.WrapEngine`
        '''
        return self._textEditView.setLineWrapMode(mode=mode, wrapEngine=wrapEngine)
    def wordWrapMode(self) -> TTkK.WrapMode:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.wordWrapMode`

        Return the active word-wrap mode.

        :return: current wrap mode.
        :rtype: :py:class:`TTkK.WrapMode`
        '''
        return self._textEditView.wordWrapMode()
    def setWordWrapMode(self, mode:TTkK.WrapMode) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setWordWrapMode`

        Set the word-wrap mode and invalidate cached wrapping.

        :param mode: new wrap mode.
        :type mode: :py:class:`TTkK.WrapMode`
        '''
        return self._textEditView.setWordWrapMode(mode=mode)
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

        Search for text in the document and place the cursor at the beginning of the first match.

        :param exp: the expression to find
        :type exp: str or :py:class:`TTkString`

        :return: ``True`` if the operation is successful, ``False`` otherwise
        :rtype: bool
        '''
        return self._textEditView.find(exp=exp)
    @pyTTkSlot()
    def ensureCursorVisible(self):
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.ensureCursorVisible`

        '''
        return self._textEditView.ensureCursorVisible()
    def followMode(self) -> TTkK.TextEditFollow:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.followMode`

        This property holds the auto-scroll follow mode of the view.

        :rtype: :py:class:`TTkK.TextEditFollow`
        '''
        return self._textEditView.followMode()
    @pyTTkSlot(TTkK.TextEditFollow)
    def setFollowMode(self, mode:TTkK.TextEditFollow) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.setFollowMode`

        Set the auto-scroll follow mode.

        :param mode: the follow mode
        :type mode: :py:class:`TTkK.TextEditFollow`
        '''
        return self._textEditView.setFollowMode(mode=mode)
    @pyTTkSlot()
    def scrollTo(self, position:TTkK.TextEditEdge) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.scrollTo`

        Scrolls the view to the specified edge(s) of the text document.

        This method allows scrolling to the top, bottom, left, or right edge of the document.
        Multiple edges can be specified by combining them with the bitwise OR operator.

        :param position: the edge(s) to scroll to
        :type position: :py:class:`TTkK.TextEditEdge`
        '''
        return self._textEditView.scrollTo(position=position)
    def toAnsi(self) -> str:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTextEditView.toAnsi`

        Returns the text of the text edit as ANSI text string.

        This string will include the ANSI escape codes for color and text formatting.

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