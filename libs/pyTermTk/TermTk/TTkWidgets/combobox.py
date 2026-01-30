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

__all__ = ['TTkComboBox']

from typing import Dict,Any,List,Optional

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.list_ import TTkList
from TermTk.TTkWidgets.lineedit import TTkLineEdit
from TermTk.TTkWidgets.resizableframe import TTkResizableFrame


class _TTkComboBoxPopup(TTkResizableFrame):
    ''' _TTkComboBoxPopup:

    Internal popup widget for :py:class:`TTkComboBox` that displays a selectable list of items.

    ::

           ┌╼ Customized search component
           │
        ┌╼ dolore ╾────────────────────┐
        │sed aute tempor in et deseru ▲│
        │cupidatat sit magna in cillum▓│
        │nostrud -- Zero --incididunt ▓│
        │dolore                       ▓│
        │dolore esse ullamco          ┊│
        │est sunt issum dolore velit e┊│
        │irure nulla sed --Zeno--  aut▼│
        └──────────────────────────────┘

    This widget extends :py:class:`TTkResizableFrame` and wraps a :py:class:`TTkList` widget,
    providing a custom overlay display for combo box selections. Unlike the standard list widget,
    this popup provides enhanced visual feedback for incremental search by overlaying the search
    text at the top of the frame.

    The key customization over the legacy list widget behavior:
    - Disables the default list search display (showSearch=False)
    - Implements a custom paintEvent that renders the search text as an overlay
    - Uses styled search text with custom colors (yellow by default)
    - Displays truncation indicator (≼) when search text exceeds available width
    - Positions search overlay at the top border of the frame (row 0)

    This approach allows better visual integration with the combo box frame borders
    while maintaining the full search functionality of TTkList.
    '''

    classStyle:Dict[str,Dict[str,Any]] = TTkResizableFrame.classStyle
    classStyle['default'] |= {'searchColor': TTkColor.fg("#FFFF00")}

    __slots__ = ('_list',
                 #exportedMethods
                 'setCurrentRow',
                 #exportedSignals
                 'textClicked')
    def __init__(self, *, items:list[str], **kwargs) -> None:
        '''
        :param items: the list of items to display in the popup
        :type items: list[str]
        '''
        super().__init__(**kwargs|{'layout':TTkGridLayout()})
        # Create internal list with search disabled - we'll render search text manually
        self._list:TTkList = TTkList(parent=self, showSearch=False)
        self._list.addItems(list(items))
        # Trigger repaint when search changes to update our custom search overlay
        self._list.searchModified.connect(self.update)

        # Export key list methods and signals for external use
        self.textClicked   = self._list.textClicked
        self.setCurrentRow = self._list.setCurrentRow

    # def setFocus(self) -> None:
    #     self._list.viewport().setFocus()

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        '''Forward all key events to the list viewport for navigation and search'''
        if (viewport := self._list.viewport()) and isinstance(viewport, TTkWidget):
            return viewport.keyEvent(evt)
        return False

    def paintEvent(self, canvas:TTkCanvas) -> None:
        '''Custom paint event that overlays search text on top of the frame.

        This overrides the default behavior to provide a styled search text display
        at the top of the popup frame, replacing the standard list widget search display.
        The search text is rendered as an overlay with:
        - Custom search color (yellow by default)
        - Truncation indicator (≼) when text is too long
        - Decorative borders (╼ ╾) around the search text
        '''
        super().paintEvent(canvas)
        # Only render search overlay if there's active search text
        if str_text := self._list.search():
            w = self.width()-6
            color = self.currentStyle()['searchColor']
            # Truncate and show indicator if search text is too long
            if len(str_text) > w:
                text = TTkString("≼",TTkColor.BG_BLUE+TTkColor.FG_CYAN)+TTkString(str_text[-w+1:],color)
            else:
                text = TTkString(str_text,color)
            # Draw search text overlay at the top of the frame
            canvas.drawText(pos=(1,0), text=f"╼ {text} ╾")
            canvas.drawTTkString(pos=(3,0), text=text)

class TTkComboBox(TTkContainer):
    ''' TTkComboBox:

    editable = False
    ::

         [ - select -  ^]

    editable = True
    ::

         [ Text       [^]

    '''

    classStyle = {
                'default':     {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#222222"),
                                'borderColor':TTkColor.RST},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'borderColor':TTkColor.fg('#888888')},
                'focus':       {'color': TTkColor.fg("#ffff88")+TTkColor.bg("#222222"),
                                'borderColor': TTkColor.fg("#ffff00") + TTkColor.BOLD},
            }

    __slots__ = ('_list', '_id', '_lineEdit', '_insertPolicy', '_textAlign', '_popupFrame',
        #signals
        'currentIndexChanged', 'currentTextChanged', 'editTextChanged')

    currentIndexChanged:pyTTkSignal
    '''
    This signal is emitted when the index in the combobox changes either through user interaction or programmatically.

    :param index: the new current index
    :type index: int
    '''
    currentTextChanged:pyTTkSignal
    '''
    This signal is emitted when the text of the current item changes. The text is passed as parameter.

    :param text: the new current text
    :type text: str
    '''
    editTextChanged:pyTTkSignal
    '''
    This signal is emitted when the text in the combobox's line edit widget is changed. This signal is only emitted when the combobox is editable.

    :param text: the new text in the line edit
    :type text: str
    '''

    _list:List[str]
    _lineEdit:Optional[TTkLineEdit]
    _popupFrame:Optional[_TTkComboBoxPopup]

    def __init__(self, *,
                 list:Optional[List[str]] = None,
                 index:int = -1,
                 insertPolicy:TTkK.InsertPolicy = TTkK.InsertAtBottom,
                 textAlign:TTkK.Alignment = TTkK.CENTER_ALIGN,
                 editable:bool = False,
                 **kwargs) -> None:
        '''
        :param list: the list of the items selectable by this combobox, defaults to []
        :type list: list[str], optional

        :param index: the initial selected index, defaults to -1 (no selection)
        :type index: int, optional

        :param insertPolicy: the policy used to determine where user-inserted items should appear in the combobox, defaults to :py:class:`TTkK.InsertPolicy.InsertAtBottom`
        :type insertPolicy: :py:class:`TTkK.InsertPolicy`, optional

        :param textAlign: the text alignment for the displayed text, defaults to :py:class:`TTkK.Alignment.CENTER_ALIGN`
        :type textAlign: :py:class:`TTkK.Alignment`, optional

        :param editable: whether the combo box can be edited by the user, defaults to False
        :type editable: bool, optional
        '''

        # Define Sub-Widgets
        self._lineEdit = None    # TTkLineEdit created only when required, if editable
        self._popupFrame = None  # TTkList created only when required, on _pressEvent()

        # Define Signals
        self.currentIndexChanged = pyTTkSignal(int)
        self.currentTextChanged  = pyTTkSignal(str)
        self.editTextChanged     = pyTTkSignal(str)

        super().__init__(**kwargs)
        self._list =  list if list else []
        self._insertPolicy = insertPolicy
        self._textAlign = textAlign
        self._id = index
        self.setEditable(editable)
        self.setMinimumSize(5, 1)
        self.setMaximumHeight(1)

    def _lineEditChanged(self) -> None:
        '''Internal callback triggered when line edit text changes.

        Handles text updates in editable mode by:
        - Checking if the text matches an existing item
        - Inserting new items based on the insert policy
        - Emitting appropriate signals for index and text changes
        '''
        if self._lineEdit is None:
            return
        text = self._lineEdit.text().toAscii()
        self._id = -1
        if text in self._list:
            self._id = self._list.index(text)
        elif self._insertPolicy ==  TTkK.NoInsert:
            pass
        elif self._insertPolicy ==  TTkK.InsertAtTop:
            self._id=0
            self._list.insert(0,text)
        # elif self._insertPolicy ==  TTkK.InsertAtCurrent:
        #     pass
        elif self._insertPolicy ==  TTkK.InsertAtBottom:
            self._id=len(self._list)
            self._list.append(text)
        # elif self._insertPolicy ==  TTkK.InsertAfterCurrent:
        #     pass
        # elif self._insertPolicy ==  TTkK.InsertBeforeCurrent:
        #     pass
        # elif self._insertPolicy ==  TTkK.InsertAlphabetically:
        #     pass
        else:
            pass
        self.currentIndexChanged.emit(self._id)
        self.currentTextChanged.emit(text)
        self.editTextChanged.emit(text)

    def textAlign(self) -> TTkK.Alignment:
        '''This property holds the displayed text alignment

        :return: the current text alignment
        :rtype: :py:class:`TTkK.Alignment`
        '''
        return self._textAlign

    def setTextAlign(self, align:TTkK.Alignment) -> None:
        '''This property holds the displayed text alignment

        :param align:
        :type align: :py:class:`TTkK.Alignment`
        '''
        if self._textAlign != align:
            self._textAlign = align
            self.update()

    def addItem(self, text:str):
        '''
        Adds an item to the combobox with the given text.

        The item is appended to the list of existing items.

        :param text: the text of the item to add
        :type text: str
        '''
        self._list.append(text)
        self.update()

    def addItems(self, items:list[str]) -> None:
        '''
        Adds a list of items to the combobox with the given text.

        The items are appended to the list of existing items.

        :param items:
        :type items: list[str]
        '''
        for item in items:
            self.addItem(item)

    pyTTkSlot()
    def clear(self) -> None:
        '''Remove all the items.'''
        if self._lineEdit is not None:
            self._lineEdit.setText("")
        self._list = []
        self._id = -1
        self.update()

    def lineEdit(self) -> Optional[TTkLineEdit]:
        '''
        Returns the :py:class:`TTkLineEdit` widget used if the editable flag is enabled

        :return: the line edit if available, None otherwise
        :rtype: :py:class:`TTkLineEdit` | None
        '''
        return self._lineEdit

    def resizeEvent(self, width: int, height: int) -> None:
        if self._lineEdit is not None:
            self._lineEdit.setGeometry(1,0,width-4,height)

    def paintEvent(self, canvas: TTkCanvas) -> None:
        style = self.currentStyle()

        color   = style['color']
        borderColor = style['borderColor']

        if self._id == -1 or self._id >= len(self._list):
            text = "- select -"
        else:
            text = self._list[self._id]
        w = self.width()

        canvas.drawTTkString(pos=(1,0), text=TTkString(text), width=w-3, alignment=self._textAlign, color=color)
        canvas.drawText(pos=(0,0), text="[",    color=borderColor)
        if self._lineEdit is not None:
            canvas.drawText(pos=(w-3,0), text="[▽]", color=borderColor)
        else:
            canvas.drawText(pos=(w-2,0), text="▽]", color=borderColor)

    def currentText(self) -> str:
        '''
        Returns the selected text

        :return: the current text
        :rtype: str
        '''
        if self._lineEdit is not None:
            return self._lineEdit.text().toAscii()
        elif self._id >= 0:
            return self._list[self._id]
        return ""

    def currentIndex(self) -> int:
        '''
        Return the current selected index.

        :return: the current index, -1 if no selection
        :rtype: int
        '''
        return self._id

    @pyTTkSlot(int)
    def setCurrentIndex(self, index:int) -> None:
        '''
        Set the selected index

        :param index:
        :type index: int
        '''
        if index < 0: return
        if index >= len(self._list): return
        if self._id == index: return
        self._id = index
        if self._id >= 0:
            if self._lineEdit is not None:
                self._lineEdit.setText(self._list[self._id])
            self.currentTextChanged.emit(self._list[self._id])
        self.currentIndexChanged.emit(self._id)
        self.update()

    @pyTTkSlot(str)
    def setCurrentText(self, text:str) -> None:
        '''
        Set the selected Text

        :param text:
        :type text: str
        '''
        if self._lineEdit is not None:
            self.setEditText(text)
        else:
            if text in self._list:
                id = self._list.index(text)
                self.setCurrentIndex(id)
            elif len(self._list) > 0:
                # Text not found, select first item
                self.setCurrentIndex(0)

    @pyTTkSlot(str)
    def setEditText(self, text) -> None:
        '''
        Set the text in the :py:class:`TTkLineEdit` widget

        :param text: the text to set (str or TTkString)
        :type text: str, :py:class:`TTkString`
        '''
        if self._lineEdit is not None:
            self._lineEdit.setText(text)

    def insertPolicy(self) -> TTkK.InsertPolicy:
        '''
        Retrieve the insert policy used when a new item is added if the combobox editable flag is true.

        :return: the current insert policy
        :rtype: :py:class:`TTkK.InsertPolicy`
        '''
        return self._insertPolicy

    def setInsertPolicy(self, policy:TTkK.InsertPolicy) -> None:
        '''
        Define the insert policy used when a new item is inserted when the widget is editable.

        :param policy:
        :type policy: :py:class:`TTkK.InsertPolicy`
        '''
        self._insertPolicy = policy

    def isEditable(self) -> bool:
        '''
        This tells if an editable :py:class:`TTkLineEdit` exists within this widget or not.

        :return: True if editable, False otherwise
        :rtype: bool
        '''
        return bool(self._lineEdit is not None)

    def setEditable(self, editable:bool) -> None:
        '''
        Create or destroy the editable :py:class:`TTkLineEdit` inside this widget.

        :param editable:
        :type editable: bool
        '''
        if editable:
            if self._lineEdit is None:
                self._lineEdit = TTkLineEdit(parent=self, hint=' - select - ')
                self._lineEdit.returnPressed.connect(self._lineEditChanged)
                # Initialize line edit with current selected text
                if self._id >= 0 and self._id < len(self._list):
                    self._lineEdit.setText(self._list[self._id])
            self.setFocusPolicy(TTkK.ClickFocus)
        else:
            if self._lineEdit is not None:
                self._lineEdit.returnPressed.disconnect(self._lineEditChanged)
                self.layout().removeWidget(self._lineEdit)
                self._lineEdit.close()
                self._lineEdit = None
            self.setFocusPolicy(TTkK.ClickFocus | TTkK.TabFocus)

    @pyTTkSlot(str)
    def _callback(self, label:str) -> None:
        '''Internal callback when an item is selected from the popup list.

        Updates the combobox selection, closes the popup, and restores focus.

        :param label: the selected item text
        :type label: str
        '''
        if self._lineEdit is not None:
            self._lineEdit.setText(label)
        self.setCurrentIndex(self._list.index(label))
        TTkHelper.removeOverlayAndChild(self._popupFrame)
        self._popupFrame = None
        self.setFocus()
        self.update()

    def _pressEvent(self) -> bool:
        '''Internal method to display the popup list overlay.

        Creates and shows the popup frame with the list of items,
        positioning it as an overlay on top of the combobox.

        :return: True to indicate event was handled
        :rtype: bool
        '''
        frameHeight = len(self._list) + 2
        frameWidth = self.width()
        if frameHeight > 20: frameHeight = 20
        if frameWidth  < 20: frameWidth = 20

        self._popupFrame = _TTkComboBoxPopup(items=self._list, size=(frameWidth,frameHeight))
        TTkHelper.overlay(self, self._popupFrame, 0, 0)
        if self._id != -1:
            self._popupFrame.setCurrentRow(self._id)
        self._popupFrame.textClicked.connect(self._callback)
        self.update()
        return True

    def wheelEvent(self, evt:TTkMouseEvent) -> bool:
        if evt.evt == TTkK.WHEEL_Up:
            self.setCurrentIndex(self._id-1)
        else:
            self.setCurrentIndex(self._id+1)
        return True

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        self._pressEvent()
        return True

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        if ((evt.type == TTkK.SpecialKey and evt.key==TTkK.Key_Down) or
                self._lineEdit is None and (evt.type == TTkK.Character and evt.key==" " or
                                            evt.type == TTkK.SpecialKey and evt.key==TTkK.Key_Enter)):
            self._pressEvent()
            return True
        return super().keyEvent(evt=evt)

    def focusInEvent(self) -> None:
        if self._lineEdit is not None:
            self._lineEdit.setFocus()
