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

import re

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.widget import *


'''
     Line Edit: |_________-___________|
     Text  "abcdefbhijklmnopqrstuvwxyz12345"
            <------------> Cursor Position
            <-->           Offset
'''
class TTkLineEdit(TTkWidget):
    __slots__ = (
        '_text', '_cursorPos', '_offset', '_replace', '_inputType', '_selectionFrom', '_selectionTo',
        # Signals
        'returnPressed', 'textChanged', 'textEdited'     )
    def __init__(self, *args, **kwargs):
        # Signals
        self.returnPressed = pyTTkSignal()
        self.textChanged =  pyTTkSignal(str)
        self.textEdited =  pyTTkSignal(str)
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkLineEdit' )
        self._inputType = kwargs.get('inputType' , TTkK.Input_Text )
        self._text = kwargs.get('text' , '' )
        if self._inputType & TTkK.Input_Number and\
           not self._text.lstrip('-').isdigit(): self._text = ""
        self._offset = 0
        self._cursorPos = 0
        self._selectionFrom = 0
        self._selectionTo   = 0
        self._replace=False
        self.setMaximumHeight(1)
        self.setMinimumSize(1,1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    @pyTTkSlot(str)
    def setText(self, text, cursorPos=-1):
        if text != self._text:
            self.textChanged.emit(text)
            self._text = text
            self._cursorPos = cursorPos if cursorPos >= 0 else len(text)
            self.update()

    def text(self):
        return self._text

    def _pushCursor(self):
        w = self.width()

        self._selectionTo   = self._selectionFrom

        # Align the text and the offset and the cursor to the current view
        self._offset = max(0, min(self._offset, len(self._text)-w))
        # Scroll to the right if reached the edge
        if self._cursorPos - self._offset > w:
            self._offset = self._cursorPos-w
        if self._cursorPos - self._offset < 0:
            self._offset = self._cursorPos

        TTkHelper.moveCursor(self,self._cursorPos-self._offset,0)
        if self._replace:
            TTkHelper.showCursor(TTkK.Cursor_Blinking_Block)
        else:
            TTkHelper.showCursor(TTkK.Cursor_Blinking_Bar)
        self.update()

    def paintEvent(self):
        if self.hasFocus():
            color = TTkCfg.theme.lineEditTextColorFocus
            selectColor = TTkCfg.theme.lineEditTextColorSelected
        else:
            color = TTkCfg.theme.lineEditTextColor
            selectColor = TTkCfg.theme.lineEditTextColorSelected
        w = self.width()
        text = TTkString() + color
        if self._inputType & TTkK.Input_Password:
            text += ("*"*(len(self._text)))
        else:
            text += self._text
        if self._selectionFrom < self._selectionTo:
            text = text.setColor(color=selectColor, posFrom=self._selectionFrom, posTo=self._selectionTo)
        text = text.substring(self._offset)
        self._canvas.drawText(pos=(0,0), text=text, color=color, width=w)

    def mousePressEvent(self, evt):
        txtPos = evt.x+self._offset
        if txtPos > len(self._text):
            txtPos = len(self._text)
        self._cursorPos     = txtPos
        self._selectionFrom = txtPos
        self._selectionTo   = txtPos
        self._pushCursor()
        return True

    def mouseDragEvent(self, evt) -> bool:
        txtPos = evt.x+self._offset
        self._selectionFrom = max(0,              min(txtPos,self._cursorPos))
        self._selectionTo   = min(len(self._text),max(txtPos,self._cursorPos))
        if self._selectionFrom < self._selectionTo:
            TTkHelper.hideCursor()
        self.update()
        return True

    def mouseDoubleClickEvent(self, evt) -> bool:
        before = self._text[:self._cursorPos]
        after =  self._text[self._cursorPos:]

        self._selectionFrom = len(before)
        self._selectionTo = len(before)

        selectRE = '[a-zA-Z0-9:,./]*'

        if m := re.search(selectRE+'$',before):
            self._selectionFrom -= len(m.group(0))
        if m := re.search('^'+selectRE,after):
            self._selectionTo += len(m.group(0))

        # TTkLog.debug("x"*self._selectionFrom)
        # TTkLog.debug("x"*self._selectionTo)
        # TTkLog.debug(self._text)

        if self._selectionFrom < self._selectionTo:
            TTkHelper.hideCursor()

        self.update()
        return True

    def mouseTapEvent(self, evt) -> bool:
        self._selectionFrom = 0
        self._selectionTo = len(self._text)
        if self._selectionFrom < self._selectionTo:
            TTkHelper.hideCursor()
        self.update()
        return True

    def keyEvent(self, evt):
        w = self.width()
        baseText = self._text
        if evt.type == TTkK.SpecialKey:
            # Don't Handle the special tab key
            if evt.key == TTkK.Key_Tab:
                return False
            if evt.key == TTkK.Key_Up: pass
            elif evt.key == TTkK.Key_Down: pass
            elif evt.key == TTkK.Key_Left:
                if self._selectionFrom < self._selectionTo:
                    self._cursorPos = self._selectionTo
                if self._cursorPos > 0:
                    self._cursorPos -= 1
            elif evt.key == TTkK.Key_Right:
                if self._selectionFrom < self._selectionTo:
                    self._cursorPos = self._selectionTo-1
                if self._cursorPos < len(self._text):
                    self._cursorPos += 1
            elif evt.key == TTkK.Key_End:
                self._cursorPos = len(self._text)
            elif evt.key == TTkK.Key_Home:
                self._cursorPos = 0
            elif evt.key == TTkK.Key_Insert:
                self._replace = not self._replace
            elif evt.key == TTkK.Key_Delete:
                if self._selectionFrom < self._selectionTo:
                    self._text = self._text[:self._selectionFrom] + self._text[self._selectionTo:]
                    self._cursorPos = self._selectionFrom
                else:
                    self._text = self._text[:self._cursorPos] + self._text[self._cursorPos+1:]
            elif evt.key == TTkK.Key_Backspace:
                if self._selectionFrom < self._selectionTo:
                    self._text = self._text[:self._selectionFrom] + self._text[self._selectionTo:]
                    self._cursorPos = self._selectionFrom
                elif self._cursorPos > 0:
                   self._text = self._text[:self._cursorPos-1] + self._text[self._cursorPos:]
                   self._cursorPos -= 1

            self._pushCursor()

            if evt.key == TTkK.Key_Enter:
                self.returnPressed.emit()
        else:
            text = self._text

            if self._selectionFrom < self._selectionTo:
                pre  = text[:self._selectionFrom]
                post = text[self._selectionTo:]
                self._cursorPos = self._selectionFrom
            else:
                pre = text[:self._cursorPos]
                if self._replace:
                    post = text[self._cursorPos+1:]
                else:
                    post = text[self._cursorPos:]

            text = pre + evt.key + post
            if self._inputType & TTkK.Input_Number and \
               not text.lstrip('-').isdigit():
                return
            self.setText(text, self._cursorPos+1)

            self._pushCursor()
        # Emit event only if the text changed
        if baseText != self._text:
            self.textEdited.emit(self._text)
        return True

    def focusInEvent(self):
        self._pushCursor()

    def focusOutEvent(self):
        self._selectionFrom = 0
        self._selectionTo   = 0
        TTkHelper.hideCursor()
        self.update()
