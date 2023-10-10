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

__all__ = ['TTkLineEdit']

import re

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget

'''
     Line Edit: |_________-___________|
     Text  "abcdefbhijklmnopqrstuvwxyz12345"
            <------------> Cursor Position
            <-->           Offset
'''
class TTkLineEdit(TTkWidget):
    '''TTkLineEdit'''

    classStyle = {
                'default':     {'color':         TTkColor.fg("#dddddd")+TTkColor.bg("#222222"),
                                'selectedColor': TTkColor.fg("#ffffff")+TTkColor.bg("#008844")},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'selectedColor': TTkColor.fg("#888888")+TTkColor.bg("#444444")},
                'focus':       {'color':         TTkColor.fg("#dddddd")+TTkColor.bg("#000044")},
            }

    __slots__ = (
        '_text', '_cursorPos', '_offset', '_replace', '_inputType', '_selectionFrom', '_selectionTo',
        # Signals
        'returnPressed', 'textChanged', 'textEdited'     )
    def __init__(self, *args, **kwargs):
        # Signals
        self.returnPressed = pyTTkSignal()
        self.textChanged =  pyTTkSignal(str)
        self.textEdited =  pyTTkSignal(str)
        self._offset = 0
        self._cursorPos = 0
        self._selectionFrom = 0
        self._selectionTo   = 0
        self._replace=False
        self._text = TTkString(kwargs.get('text' , '' ))
        self._inputType = kwargs.get('inputType' , TTkK.Input_Text )
        super().__init__(*args, **kwargs)
        if ( self._inputType & TTkK.Input_Number and
             not self._isFloat(self._text)):
            self._text = TTkString('0')
        self.setMaximumHeight(1)
        self.setMinimumSize(1,1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)
        self.enableWidgetCursor()

    @pyTTkSlot(str)
    def setText(self, text, cursorPos=0x1000):
        '''setText'''
        if text != self._text:
            self.textChanged.emit(text)
            self._text = TTkString(text)
            self._cursorPos = max(0,min(cursorPos, len(text)))
            self._pushCursor()

    def text(self):
        '''text'''
        return self._text

    def inputType(self):
        '''inputType'''
        return self._inputType

    def resizeEvent(self, w: int, h: int):
        self._pushCursor()
        return super().resizeEvent(w, h)

    def _pushCursor(self):
        w = self.width()

        self._selectionTo   = self._selectionFrom

        # Align the text and the offset and the cursor to the current view
        self._offset = max(0, min(self._offset, len(self._text)-w))
        # Scroll to the right if reached the edge
        cursorPos = self._text.substring(to=self._cursorPos).termWidth()
        if cursorPos - self._offset > w:
            self._offset = cursorPos-w
        if cursorPos - self._offset < 0:
            self._offset = cursorPos

        if self._replace:
            self.setWidgetCursor(pos=(cursorPos-self._offset, 0), type=TTkK.Cursor_Blinking_Block)
        else:
            self.setWidgetCursor(pos=(cursorPos-self._offset, 0), type=TTkK.Cursor_Blinking_Bar)

        self.update()

    def paintEvent(self, canvas):
        style = self.currentStyle()

        color         = style['color']
        selectColor = style['selectedColor']

        w = self.width()
        text = TTkString('', color)
        if self._inputType & TTkK.Input_Password:
            text += ("*"*(len(self._text)))
        else:
            text += self._text
        if self._selectionFrom < self._selectionTo:
            text = text.setColor(color=selectColor, posFrom=self._selectionFrom, posTo=self._selectionTo)
        text = text.substring(self._offset)
        canvas.drawText(pos=(0,0), text=text, color=color, width=w)

    def mousePressEvent(self, evt):
        txtPos = self._text.tabCharPos(evt.x+self._offset)
        self._cursorPos     = txtPos
        self._selectionFrom = txtPos
        self._selectionTo   = txtPos
        self._pushCursor()
        return True

    def mouseDragEvent(self, evt) -> bool:
        txtPos = self._text.tabCharPos(evt.x+self._offset)
        self._selectionFrom = max(0,              min(txtPos,self._cursorPos))
        self._selectionTo   = min(len(self._text),max(txtPos,self._cursorPos))
        if self._selectionFrom < self._selectionTo:
            TTkHelper.hideCursor()
        self.update()
        return True

    def mouseDoubleClickEvent(self, evt) -> bool:
        before = self._text.substring(to=self._cursorPos)
        after =  self._text.substring(fr=self._cursorPos)

        self._selectionFrom = len(before)
        self._selectionTo = len(before)

        selectRE = '[^ \t\r\n\(\)\[\]\.\,\+\-\*\/]*'

        if m := before.search(selectRE+'$'):
            self._selectionFrom -= len(m.group(0))
        if m := after.search('^'+selectRE):
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

    @staticmethod
    def _isFloat(num):
        try:
            float(str(num))
            return True
        except:
            return False


    def pasteEvent(self, txt:str):
        txt = TTkString().join(txt.split('\n'))

        text = self._text

        if self._selectionFrom < self._selectionTo:
            pre  = text.substring(to=self._selectionFrom)
            post = text.substring(fr=self._selectionTo)
            self._cursorPos = self._selectionFrom
        else:
            pre = text.substring(to=self._cursorPos)
            if self._replace:
                post = text.substring(fr=self._cursorPos+1)
            else:
                post = text.substring(fr=self._cursorPos)

        text = pre + txt + post
        if ( self._inputType & TTkK.Input_Number and
             not self._isFloat(text) ):
            return True
        self.setText(text, self._cursorPos+txt.termWidth())

        self._pushCursor()
        self.textEdited.emit(self._text)
        return True

    def keyEvent(self, evt):
        baseText = self._text
        if evt.type == TTkK.SpecialKey:
            # Don't Handle the special focus switch key
            if evt.key in (
                TTkK.Key_Tab, TTkK.Key_Up, TTkK.Key_Down):
                return False

            if evt.key == TTkK.Key_Left:
                if self._selectionFrom < self._selectionTo:
                    self._cursorPos = self._selectionTo
                self._cursorPos = self._text.prevPos(self._cursorPos)
            elif evt.key == TTkK.Key_Right:
                if self._selectionFrom < self._selectionTo:
                    self._cursorPos = self._selectionTo-1
                self._cursorPos = self._text.nextPos(self._cursorPos)
            elif evt.key == TTkK.Key_End:
                self._cursorPos = len(self._text)
            elif evt.key == TTkK.Key_Home:
                self._cursorPos = 0
            elif evt.key == TTkK.Key_Insert:
                self._replace = not self._replace
            elif evt.key == TTkK.Key_Delete:
                if self._selectionFrom < self._selectionTo:
                    self._text = self._text.substring(to=self._selectionFrom) + self._text.substring(fr=self._selectionTo)
                    self._cursorPos = self._selectionFrom
                else:
                    self._text = self._text.substring(to=self._cursorPos) + self._text.substring(fr=self._text.nextPos(self._cursorPos))
            elif evt.key == TTkK.Key_Backspace:
                if self._selectionFrom < self._selectionTo:
                    self._text = self._text.substring(to=self._selectionFrom) + self._text.substring(fr=self._selectionTo)
                    self._cursorPos = self._selectionFrom
                elif self._cursorPos > 0:
                   prev = self._text.prevPos(self._cursorPos)
                   self._text = self._text.substring(to=prev) + self._text.substring(fr=self._cursorPos)
                   self._cursorPos = prev

            if ( self._inputType & TTkK.Input_Number and
                 not self._isFloat(self._text) ):
                self.setText('0', 1)

            self._pushCursor()

            if evt.key == TTkK.Key_Enter:
                self.returnPressed.emit()
        else:
            text = self._text

            if self._selectionFrom < self._selectionTo:
                pre  = text.substring(to=self._selectionFrom)
                post = text.substring(fr=self._selectionTo)
                self._cursorPos = self._selectionFrom
            else:
                pre = text.substring(to=self._cursorPos)
                if self._replace:
                    post = text.substring(fr=self._cursorPos+1)
                else:
                    post = text.substring(fr=self._cursorPos)

            text = pre + evt.key + post
            if ( self._inputType & TTkK.Input_Number and
                 not self._isFloat(text) ):
                return True
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
