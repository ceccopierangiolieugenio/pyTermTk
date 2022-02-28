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

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.list_ import TTkList
from TermTk.TTkWidgets.lineedit import TTkLineEdit
from TermTk.TTkWidgets.resizableframe import TTkResizableFrame


class TTkComboBox(TTkWidget):
    __slots__ = (
        "_list",
        "_id",
        "_lineEdit",
        "_listw",
        "_editable",
        "_insertPolicy",
        "_textAlign"
        # signals
        "currentIndexChanged",
        "currentTextChanged",
        "editTextChanged",
    )

    def __init__(self, *args, **kwargs):
        # Define Signals
        self.currentIndexChanged = pyTTkSignal(int)
        self.currentTextChanged = pyTTkSignal(str)
        self.editTextChanged = pyTTkSignal(str)
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get("name", "TTkCheckbox")
        # self.cehcked = pyTTkSignal()
        self._lineEdit = TTkLineEdit(parent=self)
        self._list = kwargs.get("list", [])
        self._insertPolicy = kwargs.get("insertPolicy", TTkK.InsertAtBottom)
        self._lineEdit.returnPressed.connect(self._lineEditChanged)
        self._textAlign = kwargs.get("textAlign", TTkK.CENTER_ALIGN)
        self._id = -1
        self._popupFrame = None
        self.setEditable(kwargs.get("editable", False))
        self.setMinimumSize(5, 1)
        self.setMaximumHeight(1)

    def _lineEditChanged(self):
        text = self._lineEdit.text()
        self._id = -1
        if text in self._list:
            self._id = self._list.index(text)
        elif self._insertPolicy == TTkK.NoInsert:
            pass
        elif self._insertPolicy == TTkK.InsertAtTop:
            self._id = 0
            self._list.insert(0, text)
        # elif self._insertPolicy ==  TTkK.InsertAtCurrent:
        #     pass
        elif self._insertPolicy == TTkK.InsertAtBottom:
            self._id = len(self._list)
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

    def addItem(self, item):
        self._list.append(item)
        self.update()

    def addItems(self, items):
        for item in items:
            self.addItem(item)

    def clear(self):
        self._lineEdit.setText("")
        self._list = []
        self._id = -1
        self.update()

    def lineEdit(self):
        return self._lineEdit if self._editable else None

    def resizeEvent(self, w: int, h: int):
        w, h = self.size()
        self._lineEdit.setGeometry(1, 0, w - 4, h)

    def paintEvent(self):
        if self.hasFocus():
            borderColor = TTkCfg.theme.comboboxBorderColorFocus
            color = TTkCfg.theme.comboboxContentColorFocus
        else:
            borderColor = TTkCfg.theme.comboboxBorderColor
            color = TTkCfg.theme.comboboxContentColor
        if self._id == -1:
            text = "- select -"
        else:
            text = self._list[self._id]
        w = self.width()

        self._canvas.drawText(
            pos=(1, 0), text=text, width=w - 2, alignment=self._textAlign, color=color
        )
        self._canvas.drawText(pos=(0, 0), text="[", color=borderColor)
        if self._editable:
            self._canvas.drawText(pos=(w - 3, 0), text="[^]", color=borderColor)
        else:
            self._canvas.drawText(pos=(w - 2, 0), text="^]", color=borderColor)

    def currentText(self):
        if self._editable:
            return self._lineEdit.text()
        elif self._id >= 0:
            return self._list[self._id]
        return ""

    def currentIndex(self):
        return self._id

    @pyTTkSlot(int)
    def setCurrentIndex(self, index):
        if index > len(self._list) - 1:
            return
        self._id = index
        if self._editable:
            self._lineEdit.setText(self._list[self._id])
        else:
            self.currentTextChanged.emit(self._list[self._id])
        self.currentIndexChanged.emit(self._id)
        self.update()

    @pyTTkSlot(str)
    def setCurrentText(self, text):
        if self._editable:
            self.setEditText(text)
        else:
            if id := self._list.index(text):
                self.setCurrentIndex(id)

    @pyTTkSlot(str)
    def setEditText(self, text):
        if self._editable:
            self._lineEdit.setText(text)

    def insertPolicy(self):
        return self._insertPolicy

    def setInsertPolicy(self, ip):
        self._insertPolicy = ip

    def isEditable(self):
        return self._editable

    def setEditable(self, editable):
        self._editable = editable
        if editable:
            self._lineEdit.show()
            self.setFocusPolicy(TTkK.ClickFocus)
        else:
            self._lineEdit.hide()
            self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    @pyTTkSlot(str)
    def _callback(self, label):
        self._lineEdit.setText(label)
        self.setCurrentIndex(self._list.index(label))
        TTkHelper.removeOverlayAndChild(self._popupFrame)
        self._popupFrame = None
        self.setFocus()
        self.update()

    def _pressEvent(self):
        frameHeight = len(self._list) + 2
        frameWidth = self.width()
        if frameHeight > 20:
            frameHeight = 20
        if frameWidth < 20:
            frameWidth = 20

        self._popupFrame = TTkResizableFrame(
            layout=TTkGridLayout(), size=(frameWidth, frameHeight)
        )
        TTkHelper.overlay(self, self._popupFrame, 0, 0)
        listw = TTkList(parent=self._popupFrame)
        TTkLog.debug(f"{self._list}")
        for item in self._list:
            listw.addItem(item)
        if self._id != -1:
            listw.setCurrentRow(self._id)
        listw.textClicked.connect(self._callback)
        listw.viewport().setFocus()
        self.update()
        return True

    def mousePressEvent(self, evt):
        self._pressEvent()
        return True

    def keyEvent(self, evt):
        if (evt.type == TTkK.Character and evt.key == " ") or (
            evt.type == TTkK.SpecialKey and evt.key in [TTkK.Key_Enter, TTkK.Key_Down]
        ):
            self._pressEvent()
            return True
        return False

    def focusInEvent(self):
        if self._editable:
            self._lineEdit.setFocus()
