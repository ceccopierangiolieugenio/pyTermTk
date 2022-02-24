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

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkWidgets.widget import *
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.scrollbar import TTkScrollBar
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView


'''
    Design:

'''
class _TTkTextEditView(TTkAbstractScrollView):
    __slots__ = (
            '_lines', '_hsize',
            '_cursorPos', '_cursorParams', '_selectionFrom', '_selectionTo',
            '_replace',
            '_readOnly'
        )
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTextEditView' )
        self._readOnly = True
        self._hsize = 0
        self._lines = ['']
        self._replace = False
        self._cursorPos = (0,0)
        self._selectionFrom = (0,0)
        self._selectionTo = (0,0)
        self._cursorParams = None
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)


    def isReadOnly(self) -> bool :
        return self._readOnly

    def setReadOnly(self, ro):
        self._readOnly = ro

    @pyTTkSlot(str)
    def setText(self, text):
        if type(text) == str:
            text = TTkString() + text
        self._lines = text.split('\n')
        self.viewMoveTo(0, 0)
        self._updateSize()
        self.viewChanged.emit()
        self.update()

    def _updateSize(self):
        self._hsize = max( [ len(l) for l in self._lines ] )

    def viewFullAreaSize(self) -> (int, int):
        return self._hsize, len(self._lines)

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def _pushCursor(self):
        if self._readOnly or not self.hasFocus():
            return
        ox, oy = self.getViewOffsets()

        x = self._cursorPos[0]-ox
        y = self._cursorPos[1]-oy

        if x >= self.width() or y>=self.height() or \
           self._selectionFrom != self._selectionTo or \
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

    def mousePressEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mousePressEvent(evt)
        ox, oy = self.getViewOffsets()
        y = max(0,min(evt.y + oy,len(self._lines)))
        x = max(0,min(evt.x + ox,len(self._lines[y])))
        self._cursorPos     = (x,y)
        self._selectionFrom = (x,y)
        self._selectionTo   = (x,y)
        # TTkLog.debug(f"{self._cursorPos=}")
        self.update()
        return True

    def mouseDragEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseDragEvent(evt)
        ox, oy = self.getViewOffsets()
        y = max(0,min(evt.y + oy,len(self._lines)))
        x = max(0,min(evt.x + ox,len(self._lines[y])))

        self._selectionFrom = ( min(x,self._cursorPos[0]), min(y,self._cursorPos[1]) )
        self._selectionTo   = ( max(x,self._cursorPos[0]), max(y,self._cursorPos[1]) )

        self.update()
        return True

    def mouseDoubleClickEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseDoubleClickEvent(evt)
        ox, oy = self.getViewOffsets()
        y = max(0,min(evt.y + oy,len(self._lines)))
        x = max(0,min(evt.x + ox,len(self._lines[y])))
        self._cursorPos     = (x,y)

        before = self._lines[y].substring(to=x)
        after =  self._lines[y].substring(fr=x)

        xFrom = len(before)
        xTo   = len(before)

        selectRE = '[a-zA-Z0-9:,./]*'

        if m := before.search(selectRE+'$'):
            xFrom -= len(m.group(0))
        if m := after.search('^'+selectRE):
            xTo += len(m.group(0))

        self._selectionFrom = ( xFrom, y )
        self._selectionTo   = ( xTo,   y )

        self.update()
        return True

    def mouseTapEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseTapEvent(evt)
        ox, oy = self.getViewOffsets()
        y = max(0,min(evt.y + oy,len(self._lines)))
        x = max(0,min(evt.x + ox,len(self._lines[y])))
        self._cursorPos     = (x,y)

        self._selectionFrom = ( 0 , y )
        self._selectionTo   = ( len(self._lines[y]) ,   y )

        self.update()
        return True

    def keyEvent(self, evt):
        if self._readOnly:
            return super().keyEvent(evt)
        return True

    def focusInEvent(self):
        self._pushCursor()
        self.update()

    def focusOutEvent(self):
        TTkHelper.hideCursor()

    def paintEvent(self):
        ox, oy = self.getViewOffsets()
        if self.hasFocus():
            color = TTkCfg.theme.lineEditTextColorFocus
            selectColor = TTkCfg.theme.lineEditTextColorSelected
        else:
            color = TTkCfg.theme.lineEditTextColor
            selectColor = TTkCfg.theme.lineEditTextColorSelected

        h = self.height()
        for y, t in enumerate(self._lines[oy:oy+h]):
            if self._selectionFrom[1] <= y+oy <= self._selectionTo[1]:
                pf = 0      if y+oy > self._selectionFrom[1] else self._selectionFrom[0]
                pt = len(t) if y+oy < self._selectionTo[1]   else self._selectionTo[0]
                t = t.setColor(color=selectColor, posFrom=pf, posTo=pt )
            self._canvas.drawText(pos=(-ox,y), text=t)
        self._pushCursor()

class TTkTextEdit(TTkAbstractScrollArea):
    __slots__ = (
            '_textEditView',
            # Forwarded Methods
            'setText', 'isReadOnly', 'setReadOnly'
        )
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTextEdit' )
        self._textEditView = _TTkTextEditView()
        self.setViewport(self._textEditView)
        self.setText = self._textEditView.setText
        self.isReadOnly  = self._textEditView.isReadOnly
        self.setReadOnly = self._textEditView.setReadOnly

