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

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkWidgets.widget import *
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.scrollbar import TTkScrollBar
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class _TTkTextEditView(TTkAbstractScrollView):
    __slots__ = (
            '_lines', '_hsize',
            '_cursorPos', '_cursorParams', '_selectionFrom', '_selectionTo',
            '_tabSpaces',
            '_replace',
            '_readOnly'
        )
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTextEditView' )
        self._readOnly = True
        self._hsize = 0
        self._lines = ['']
        self._tabSpaces = 4
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
        self.viewMoveTo(0, 0)
        self._lines = []
        self.append(text)

    @pyTTkSlot(str)
    def append(self, text):
        if type(text) == str:
            text = TTkString() + text
        self._lines += text.split('\n')
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

        if x > self.width() or y>=self.height() or \
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

    def _setCursorPos(self, x, y):
        y = max(0,min(y,len(self._lines)-1))
        # The replace cursor need to be aligned to the char
        # The Insert cursor must be placed between chars
        if self._replace:
            x = max(0,min(x,len(self._lines[y])-1))
        else:
            x = max(0,min(x,len(self._lines[y])))
        self._cursorPos     = (x,y)
        self._selectionFrom = (x,y)
        self._selectionTo   = (x,y)
        self._scrolToInclude(x,y)

    def _scrolToInclude(self, x, y):
        # Scroll the area (if required) to include the position x,y
        _,_,w,h = self.geometry()
        offx, offy = self.getViewOffsets()
        offx = max(min(offx, x),x-w)
        offy = max(min(offy, y),y-h+1)
        self.viewMoveTo(offx, offy)

    def _selection(self) -> bool:
        return self._selectionFrom != self._selectionTo

    def _eraseSelection(self):
       if self._selection(): # delete selection
        sx1,sy1 = self._selectionFrom
        sx2,sy2 = self._selectionTo
        self._cursorPos   = self._selectionFrom
        self._selectionTo = self._selectionFrom
        self._lines[sy1] = self._lines[sy1].substring(to=sx1) + \
                           self._lines[sy2].substring(fr=sx2)
        self._lines = self._lines[:sy1+1] + self._lines[sy2+1:]

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
        cx = self._cursorPos[0]
        cy = self._cursorPos[1]

        if y < cy:    # Mouse Dragged above the cursor
            self._selectionFrom = (  x,  y )
            self._selectionTo   = ( cx, cy )
        elif y > cy:  # Mouse Dragged below the cursor
            self._selectionFrom = ( cx, cy )
            self._selectionTo   = (  x,  y )
        else: # Mouse on the same line of the cursor
            self._selectionFrom = ( min(cx,x), y )
            self._selectionTo   = ( max(cx,x), y )

        self._scrolToInclude(x,y)

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

    def mouseReleaseEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseReleaseEvent(evt)
        ox, oy = self.getViewOffsets()
        y = max(0,min(evt.y + oy,len(self._lines)))
        x = max(0,min(evt.x + ox,len(self._lines[y])))
        self._cursorPos     = (x,y)
        self.update()
        return True

    def keyEvent(self, evt):
        if self._readOnly:
            return super().keyEvent(evt)
        if evt.type == TTkK.SpecialKey:
            _,_,w,h = self.geometry()

            cx = self._cursorPos[0]
            cy = self._cursorPos[1]
            # Don't Handle the special tab key, for now
            if evt.key == TTkK.Key_Tab:
                return False
            if evt.key == TTkK.Key_Up:         self._setCursorPos(cx  , cy-1)
            elif evt.key == TTkK.Key_Down:     self._setCursorPos(cx  , cy+1)
            elif evt.key == TTkK.Key_Left:     self._setCursorPos(cx-1, cy  )
            elif evt.key == TTkK.Key_Right:    self._setCursorPos(cx+1, cy  )
            elif evt.key == TTkK.Key_End:      self._setCursorPos(len(self._lines[cy]) , cy )
            elif evt.key == TTkK.Key_Home:     self._setCursorPos(0   , cy )
            elif evt.key == TTkK.Key_PageUp:   self._setCursorPos(cx   , cy - h)
            elif evt.key == TTkK.Key_PageDown: self._setCursorPos(cx   , cy + h)
            elif evt.key == TTkK.Key_Insert:
                self._replace = not self._replace
                self._setCursorPos(cx , cy)
            elif evt.key == TTkK.Key_Delete:
                if self._selection():
                    self._eraseSelection()
                else:
                    l = self._lines[cy]
                    if cx < len(l): # Erase next caracter on the same line
                        self._lines[cy] = l.substring(to=cx) + l.substring(fr=cx+1)
                    elif (cy+1)<len(self._lines): # End of the line, remove "\n" and merge with the next line
                        self._lines[cy] += self._lines[cy+1]
                        self._lines = self._lines[:cy+1] + self._lines[cy+2:]
                        self._setCursorPos(cx, cy)
            elif evt.key == TTkK.Key_Backspace:
                if self._selection():
                    self._eraseSelection()
                else:
                    l = self._lines[cy]
                    if cx > 0: # Erase the previous character
                        cx-=1
                        self._lines[cy] = l.substring(to=cx) + l.substring(fr=cx+1)
                        self._setCursorPos(cx, cy)
                    elif cy>0: # Beginning of the line, remove "\n" and merge with the previous line
                        cx = len(self._lines[cy-1])
                        self._lines[cy-1] += l
                        self._lines = self._lines[:cy] + self._lines[cy+1:]
                        self._setCursorPos(cx, cy-1)
            elif evt.key == TTkK.Key_Enter:
                self._eraseSelection()
                l = self._lines[cy]
                self._lines[cy] = l.substring(to=cx)
                self._lines = self._lines[:cy+1] + [l.substring(fr=cx)] + self._lines[cy+1:]
                self._setCursorPos(0,cy+1)
            self.update()
            return True
        else: # Input char
            self._eraseSelection()
            cpx,cpy = self._cursorPos
            l = self._lines[cpy]
            self._lines[cpy] = l.substring(to=cpx) + evt.key + l.substring(fr=cpx)
            self._setCursorPos(cpx+1,cpy)
            self.update()
            return True

        return super().keyEvent(evt)

    def focusInEvent(self):
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
            t = t.tab2spaces(self._tabSpaces)
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
            'setText', 'append', 'isReadOnly', 'setReadOnly'
        )
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTextEdit' )
        self._textEditView = _TTkTextEditView()
        self.setViewport(self._textEditView)
        self.setText = self._textEditView.setText
        self.append  = self._textEditView.append
        self.isReadOnly  = self._textEditView.isReadOnly
        self.setReadOnly = self._textEditView.setReadOnly

