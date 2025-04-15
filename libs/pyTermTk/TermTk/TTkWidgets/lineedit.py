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

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

from TermTk.TTkGui.clipboard import TTkClipboard
from TermTk.TTkWidgets.widget import TTkWidget

'''
     Line Edit: |_________-___________|
     Text  "abcdefbhijklmnopqrstuvwxyz12345"
            <------------> Cursor Position
            <-->           Offset
'''
class TTkLineEdit(TTkWidget):
    '''TTkLineEdit'''

    class EchoMode(int):
        '''EchoMode'''
        Normal             = 0x00
        '''Display characters as they are entered. This is the default.'''
        NoEcho             = 0x01
        '''Do not display anything. This may be appropriate for passwords where even the length of the password should be kept secret.'''
        Password           = 0x02
        '''Display asterisks instead of the characters actually entered.'''
        PasswordEchoOnEdit = 0x03
        '''Display characters as they are entered while editing otherwise display asterisks.'''

    classStyle = {
                'default':     {'color':         TTkColor.fgbg("#dddddd","#222222"),
                                'bgcolor':       TTkColor.fgbg("#666666","#222222")+TTkColor.UNDERLINE,
                                'selectedColor': TTkColor.fgbg("#ffffff","#008844")},
                'disabled':    {'color':         TTkColor.fg(  "#888888"),
                                'bgcolor':       TTkColor.fg(  "#444444")+TTkColor.UNDERLINE,
                                'selectedColor': TTkColor.fgbg("#888888","#444444")},
                'focus':       {'color':         TTkColor.fgbg("#dddddd","#000044"),
                                'bgcolor':       TTkColor.fgbg("#666666","#000044")+TTkColor.UNDERLINE}
            }

    __slots__ = (
        '_text', '_cursorPos', '_offset', '_replace', '_inputType', '_echoMode',
        '_selectionFrom', '_selectionTo',
        '_clipboard',
        '_hint',
        # Signals
        'returnPressed', 'textChanged', 'textEdited'     )
    def __init__(self, *,
                 text:TTkString='',
                 hint:TTkString='',
                 inputType:int=TTkK.Input_Text,
                 echoMode:EchoMode=EchoMode.Normal,
                 **kwargs) -> None:
        # Signals
        self.returnPressed = pyTTkSignal()
        self.textChanged =  pyTTkSignal(str)
        self.textEdited =  pyTTkSignal(str)
        self._offset = 0
        self._cursorPos = 0
        self._selectionFrom = 0
        self._selectionTo   = 0
        self._replace=False
        self._text = TTkString(text)
        self._hint = TTkString(hint)
        self._inputType = inputType
        self._echoMode = echoMode
        self._clipboard = TTkClipboard()
        super().__init__(**kwargs)
        self.setInputType(inputType)
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
        if cursorPos != self._cursorPos:
            self._cursorPos = max(0,min(cursorPos, len(text)))
            self._pushCursor()

    def text(self):
        '''text'''
        return self._text

    def inputType(self):
        '''inputType'''
        return self._inputType

    def setInputType(self, inputType):
        '''inputType'''
        if bool(inputType & TTkK.Input_Text) and bool(inputType & TTkK.Input_Number):
            return
        # Kept here for retrocompatibility
        if inputType & TTkK.Input_Password:
            TTkLog.warn("TTkK.Input_Password is deprecated, use the EchoMode instead")
            self._echoMode = TTkLineEdit.EchoMode.Password
            inputType &= ~TTkK.Input_Password
        if inputType & ~(TTkK.Input_Text|TTkK.Input_Number):
            return
        self._inputType = inputType & (TTkK.Input_Text|TTkK.Input_Number) if inputType else TTkK.Input_Text
        if ( self._inputType == TTkK.Input_Number and
             not self._isFloat(self._text)):
            self._text = TTkString('0')
        self.update()

    def echoMode(self) -> EchoMode:
        return self._echoMode

    def setEchoMode(self, echoMode:EchoMode):
        self._echoMode = echoMode
        self.update()

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

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        txtPos = self._text.tabCharPos(evt.x+self._offset)
        self._cursorPos     = txtPos
        self._selectionFrom = txtPos
        self._selectionTo   = txtPos
        self._pushCursor()
        return True

    def mouseDragEvent(self, evt:TTkMouseEvent) -> bool:
        txtPos = self._text.tabCharPos(evt.x+self._offset)
        self._selectionFrom = max(0,              min(txtPos,self._cursorPos))
        self._selectionTo   = min(len(self._text),max(txtPos,self._cursorPos))
        if self._selectionFrom < self._selectionTo:
            TTkHelper.hideCursor()
        self.update()
        self.copy()
        return True

    def mouseDoubleClickEvent(self, evt:TTkMouseEvent) -> bool:
        before = self._text.substring(to=self._cursorPos)
        after =  self._text.substring(fr=self._cursorPos)

        self._selectionFrom = len(before)
        self._selectionTo = len(before)

        selectRE = r'[^ \t\r\n()[\]\.\,\+\-\*\/]*'

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
        self.copy()
        return True

    def mouseTapEvent(self, evt:TTkMouseEvent) -> bool:
        self._selectionFrom = 0
        self._selectionTo = len(self._text)
        if self._selectionFrom < self._selectionTo:
            TTkHelper.hideCursor()
        self.update()
        self.copy()
        return True

    @staticmethod
    def _isFloat(num):
        try:
            float(str(num))
            return True
        except:
            return False

    @pyTTkSlot()
    def copy(self):
        if self._selectionFrom >= self._selectionTo: return
        txt = self._text.substring(fr=self._selectionFrom,to=self._selectionTo)
        self._clipboard.setText(txt)

    @pyTTkSlot()
    def cut(self):
        self.copy()
        self._text = self._text.substring(to=self._selectionFrom) + self._text.substring(fr=self._selectionTo)
        self._cursorPos = self._selectionFrom
        self.update()

    @pyTTkSlot()
    def paste(self):
        txt = self._clipboard.text()
        self.pasteEvent(txt)

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

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        baseText = self._text
        if evt.type == TTkK.SpecialKey:
            # Don't Handle the special focus switch key
            if evt.key in (
                TTkK.Key_Tab, TTkK.Key_Up, TTkK.Key_Down):
                return False

            # CTRL Pressed
            if evt.mod==TTkK.ControlModifier:
                if   evt.key == TTkK.Key_C:
                    self.copy()
                elif evt.key == TTkK.Key_V:
                    self.paste()
                elif evt.key == TTkK.Key_X:
                    self.cut()
                else:
                    return super().keyEvent(evt)
                return True

            text = self._text
            cursorPos = self._cursorPos

            if evt.key == TTkK.Key_Left:
                if self._selectionFrom < self._selectionTo:
                    cursorPos = self._selectionTo
                cursorPos = self._text.prevPos(self._cursorPos)
            elif evt.key == TTkK.Key_Right:
                if self._selectionFrom < self._selectionTo:
                    cursorPos = self._selectionTo-1
                cursorPos = self._text.nextPos(self._cursorPos)
            elif evt.key == TTkK.Key_End:
                cursorPos = len(self._text)
            elif evt.key == TTkK.Key_Home:
                cursorPos = 0
            elif evt.key == TTkK.Key_Insert:
                self._replace = not self._replace
            elif evt.key == TTkK.Key_Delete:
                if self._selectionFrom < self._selectionTo:
                    text = self._text.substring(to=self._selectionFrom) + self._text.substring(fr=self._selectionTo)
                    cursorPos = self._selectionFrom
                else:
                    text = self._text.substring(to=self._cursorPos) + self._text.substring(fr=self._text.nextPos(self._cursorPos))
            elif evt.key == TTkK.Key_Backspace:
                if self._selectionFrom < self._selectionTo:
                    text = self._text.substring(to=self._selectionFrom) + self._text.substring(fr=self._selectionTo)
                    cursorPos = self._selectionFrom
                elif self._cursorPos > 0:
                   prev = self._text.prevPos(self._cursorPos)
                   text = self._text.substring(to=prev) + self._text.substring(fr=self._cursorPos)
                   cursorPos = prev

            if ( self._inputType & TTkK.Input_Number and
                 not self._isFloat(self._text) ):
                self.setText('0', 1)
            else:
                self.setText(text, cursorPos)

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
                 ( evt.key in (' ') or not self._isFloat(text) )):
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

    def paintEvent(self, canvas):
        style = self.currentStyle()

        color       = style['color']
        bgcolor     = style['bgcolor']
        selectColor = style['selectedColor']

        w = self.width()
        text = TTkString('', color)
        if self._echoMode != TTkLineEdit.EchoMode.NoEcho:
            if ( self._echoMode == TTkLineEdit.EchoMode.Password or
                 ( self._echoMode == TTkLineEdit.EchoMode.PasswordEchoOnEdit and
                   not self.hasFocus() )):
                text += ("*"*(len(self._text)))
            else:
                text += self._text
        if self._selectionFrom < self._selectionTo:
            text = text.setColor(color=selectColor, posFrom=self._selectionFrom, posTo=self._selectionTo)
        text = text.substring(self._offset)
        canvas.fill(color=bgcolor)
        if self._text:
            canvas.drawTTkString(pos=(0,0), text=text, color=color)
        else:
            canvas.drawTTkString(pos=(0,0), text=self._hint, color=bgcolor)


