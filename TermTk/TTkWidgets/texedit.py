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
            '_lines', '_dataLines', '_hsize',
            '_cursorPos', '_cursorParams', '_selectionFrom', '_selectionTo',
            '_tabSpaces',
            '_lineWrapMode', '_wordWrapMode', '_wrapWidth', '_lastWrapUsed',
            '_replace',
            '_readOnly'
        )
    '''
        in order to support the line wrap, I need to divide the full data text in;
        _dataLines = the entire text divided in lines, easy to add/remove/append lines
        _lines     = an array of tuples for each displayed line with a pointer to a
                     specific line and its slice to be shown at this coordinate;
                     [ (line, (posFrom, posTo)), ... ]
                     This is required to support the wrap feature
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTextEditView' )
        self._readOnly = True
        self._hsize = 0
        self._lines = [(0,(0,0))]
        self._dataLines = ['']
        self._tabSpaces = 4
        self._wrapWidth     = 80
        self._lastWrapUsed  = 0
        self._lineWrapMode = TTkK.NoWrap
        self._wordWrapMode = TTkK.WrapAnywhere
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

    def wrapWidth(self):
        return self._wrapWidth

    def setWrapWidth(self, width):
        self._wrapWidth = width
        self._rewrap()

    def lineWrapMode(self):
        return self._lineWrapMode

    def setLineWrapMode(self, mode):
        self._lineWrapMode = mode
        self._rewrap()

    def wordWrapMode(self):
        return self._wordWrapMode

    def setWordWrapMode(self, mode):
        self._wordWrapMode = mode
        self._rewrap()

    @pyTTkSlot(str)
    def setText(self, text):
        self.viewMoveTo(0, 0)
        self._dataLines = []
        self.append(text)

    @pyTTkSlot(str)
    def append(self, text):
        if type(text) == str:
            text = TTkString() + text
        self._dataLines += text.split('\n')
        self._updateSize()
        self._rewrap()

    def _rewrap(self):
        self._lines = []
        if self._lineWrapMode == TTkK.NoWrap:
            def _process(i,l):
                self._lines.append((i,(0,len(l))))
        else:
            if   self._lineWrapMode == TTkK.WidgetWidth:
                w = self.width()
                if not w: return
            elif self._lineWrapMode == TTkK.FixedWidth:
                w = self._wrapWidth

            def _process(i,l):
                fr = 0
                to = 0
                if not len(l): # if the line is empty append it
                    self._lines.append((i,(0,0)))
                    return
                while len(l):
                    fl = l.tab2spaces(self._tabSpaces)
                    if len(fl) <= w:
                        self._lines.append((i,(fr,fr+len(l))))
                        l=[]
                    else:
                        to = max(1,l.tabCharPos(w,self._tabSpaces))
                        if self._wordWrapMode == TTkK.WordWrap: # Find the index of the first white space
                            s = str(l)
                            newTo = to
                            while newTo and ( s[newTo] != ' ' and s[newTo] != '\t' ): newTo-=1
                            if newTo: to = newTo

                        self._lines.append((i,(fr,fr+to)))
                        l = l.substring(to)
                        fr += to
        self.viewChanged.emit()
        self.update()

        for i,l in enumerate(self._dataLines):
            _process(i,l)

    def resizeEvent(self, w, h):
        if w != self._lastWrapUsed and w>self._tabSpaces:
            self._lastWrapUsed = w
            self._rewrap()
        return super().resizeEvent(w,h)

    def _updateSize(self):
        self._hsize = max( [ len(l) for l in self._dataLines ] )

    def viewFullAreaSize(self) -> (int, int):
        if self._lineWrapMode == TTkK.NoWrap:
            return self._hsize, len(self._lines)
        elif self._lineWrapMode == TTkK.WidgetWidth:
            return self.width(), len(self._lines)
        elif self._lineWrapMode == TTkK.FixedWidth:
            return self._wrapWidth, len(self._lines)

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

    def _setCursorPos(self, x, y, alignRightTab = False):
        x,y = self._cursorAlign(x,y, alignRightTab)
        self._cursorPos     = (x,y)
        self._selectionFrom = (x,y)
        self._selectionTo   = (x,y)
        self._scrolToInclude(x,y)

    def _moveHCursor(self, x,y, hoff):
        l, dx = self._linePosFromCursor(x,y)
        dt, _ = self._lines[y]
        # Due to the internal usage I assume hoff 1 or -1
        dx += hoff
        if hoff > 0 and dx>len(l) and dt<len(self._dataLines):
            dx  = 0
            dt += 1
        elif dx<0:
            if dt == 0: # Beginning of the file
                dx = 0
            else:
                dt -= 1
                dx = len(self._dataLines[dt])
        cx, cy = self._cursorFromDataPos(dt,dx)
        self._setCursorPos(cx, cy, hoff>0)

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
        if not self._selection(): return
        _,sx1 = self._linePosFromCursor(self._selectionFrom[0],self._selectionFrom[1])
        sy1 = self._lines[self._selectionFrom[1]][0]
        _,sx2 = self._linePosFromCursor(self._selectionTo[0]  ,self._selectionTo[1])
        sy2 = self._lines[self._selectionTo[1]][0]
        self._cursorPos   = self._selectionFrom
        self._selectionTo = self._selectionFrom
        self._dataLines[sy1] = self._dataLines[sy1].substring(to=sx1) + \
                           self._dataLines[sy2].substring(fr=sx2)
        self._dataLines = self._dataLines[:sy1+1] + self._dataLines[sy2+1:]
        self._rewrap()

    def _cursorAlign(self, x, y, alignRightTab = False):
        '''
        Return the widget position of the closest editable char
        in:
        x,y = widget relative position
        alignRightTab = if true, align the position to the right of the tab space
        return:
        x,y = widget relative position aligned to the close editable char
        '''
        y = max(0,min(y,len(self._lines)))
        dt, (fr, to) = self._lines[y]
        x = max(0,x)
        s = self._dataLines[dt].substring(fr,to)
        x = s.tabCharPos(x, self._tabSpaces, alignRightTab)
        # The replace cursor need to be aligned to the char
        # The Insert cursor must be placed between chars
        if self._replace and x==len(s):
            x -= 1
        x = len(s.substring(0,x).tab2spaces(self._tabSpaces))
        return x, y

    def _linePosFromCursor(self,x,y):
        '''
        return the line and the x position from the x,y cursor position relative to the widget
        I assume the x,y position already normalized using the _cursorAlign function
        '''
        dt, (fr, to) = self._lines[y]
        return self._dataLines[dt], fr+self._dataLines[dt].substring(fr,to).tabCharPos(x,self._tabSpaces)

    def _cursorFromLinePos(self,liney,p):
        '''
        return the x,y cursor position relative to the widget from the
        liney value relative to the self._lines and the
        p = position value relative to the string related to self._lines[liney][0]
        I know, big chink of crap
        '''
        # Find the bginning of the string in the "self._lines" (position from == 0)
        while self._lines[liney][1][0]: liney -=1
        dt = self._lines[liney][0]
        while liney < len(self._lines):
            dt1, (fr, to) = self._lines[liney]
            if dt1 != dt:
                break
            if fr<=p<to:
                s = self._dataLines[dt].substring(fr,p).tab2spaces(self._tabSpaces)
                return len(s), liney
            liney += 1
        liney-=1
        dt, (fr, to) = self._lines[liney]
        s = self._dataLines[dt].substring(fr,to)
        return len(s.tab2spaces(self._tabSpaces)), liney

    def _cursorFromDataPos(self,y,p):
        for i,l in enumerate(self._lines):
            if l[0] == y:
                return self._cursorFromLinePos(i,p)
        return 0,0

    def mousePressEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mousePressEvent(evt)
        ox, oy = self.getViewOffsets()
        x,y = self._cursorAlign(evt.x + ox, evt.y + oy)
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
        x,y = self._cursorAlign(evt.x + ox, evt.y + oy)
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
        x,y = self._cursorAlign(evt.x + ox, evt.y + oy)
        self._cursorPos     = (x,y)

        l,p = self._linePosFromCursor(x,y)
        before = l.substring(to=p)
        after =  l.substring(fr=p)

        xFrom = len(before)
        xTo   = len(before)

        selectRE = '[a-zA-Z0-9:,./]*'

        if m := before.search(selectRE+'$'):
            xFrom -= len(m.group(0))
        if m := after.search('^'+selectRE):
            xTo += len(m.group(0))

        self._selectionFrom = self._cursorFromLinePos(y,xFrom)
        self._selectionTo   = self._cursorFromLinePos(y,xTo)
        self._cursorPos     = self._selectionFrom

        self.update()
        return True

    def mouseTapEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseTapEvent(evt)
        ox, oy = self.getViewOffsets()
        x,y = self._cursorAlign(evt.x + ox, evt.y + oy)
        self._cursorPos     = (x,y)

        l,_ = self._linePosFromCursor(x,y)

        self._selectionFrom = self._cursorFromLinePos(y,0)
        self._selectionTo   = self._cursorFromLinePos(y,len(l))
        self._cursorPos     = self._selectionFrom
        self.update()
        return True

    def mouseReleaseEvent(self, evt) -> bool:
        if self._readOnly:
            return super().mouseReleaseEvent(evt)
        ox, oy = self.getViewOffsets()
        self._cursorPos     = self._selectionFrom
        self.update()
        return True

    def keyEvent(self, evt):
        if self._readOnly:
            return super().keyEvent(evt)
        if evt.type == TTkK.SpecialKey:
            _,_,w,h = self.geometry()

            cx, cy = self._cursorPos
            dt, (fr, to) = self._lines[cy]
            # Don't Handle the special tab key, for now
            if evt.key == TTkK.Key_Tab:
                return False
            if evt.key == TTkK.Key_Up:         self._setCursorPos(cx , cy-1)
            elif evt.key == TTkK.Key_Down:     self._setCursorPos(cx , cy+1)
            elif evt.key == TTkK.Key_Left:     self._moveHCursor( cx , cy , -1 )
            elif evt.key == TTkK.Key_Right:    self._moveHCursor( cx , cy , +1 )
            elif evt.key == TTkK.Key_End:      self._setCursorPos(w  , cy )
            elif evt.key == TTkK.Key_Home:     self._setCursorPos(0  , cy )
            elif evt.key == TTkK.Key_PageUp:   self._setCursorPos(cx , cy - h)
            elif evt.key == TTkK.Key_PageDown: self._setCursorPos(cx , cy + h)
            elif evt.key == TTkK.Key_Insert:
                self._replace = not self._replace
                self._setCursorPos(cx , cy)
            elif evt.key == TTkK.Key_Delete:
                if self._selection():
                    self._eraseSelection()
                else:
                    l,dx = self._linePosFromCursor(cx,cy)
                    if dx < len(l): # Erase next caracter on the same line
                        self._dataLines[dt] = l.substring(to=dx) + l.substring(fr=dx+1)
                    elif (dt+1)<len(self._dataLines): # End of the line, remove "\n" and merge with the next line
                        self._dataLines[dt] += self._dataLines[dt+1]
                        self._dataLines = self._dataLines[:dt+1] + self._dataLines[dt+2:]
                        self._setCursorPos(cx, cy)
                    self._rewrap()
            elif evt.key == TTkK.Key_Backspace:
                if self._selection():
                    self._eraseSelection()
                else:
                    l,dx = self._linePosFromCursor(cx,cy)
                    if dx > 0: # Erase the previous character
                        dx -= 1
                        self._dataLines[dt] = l.substring(to=dx) + l.substring(fr=dx+1)
                    elif dt>0: # Beginning of the line, remove "\n" and merge with the previous line
                        dt -=1
                        dx = len(self._dataLines[dt])
                        self._dataLines[dt] += l
                        self._dataLines = self._dataLines[:dt+1] + self._dataLines[dt+2:]
                    self._rewrap()
                    cx, cy = self._cursorFromDataPos(dt,dx)
                    self._setCursorPos(cx, cy)
            elif evt.key == TTkK.Key_Enter:
                self._eraseSelection()
                l,dx = self._linePosFromCursor(cx,cy)
                self._dataLines[dt] = l.substring(to=dx)
                self._dataLines = self._dataLines[:dt+1] + [l.substring(fr=dx)] + self._dataLines[dt+1:]
                self._rewrap()
                self._setCursorPos(0,cy+1)
            self.update()
            return True
        else: # Input char
            self._eraseSelection()
            cx,cy = self._cursorPos
            dt, _ = self._lines[cy]
            l, dx = self._linePosFromCursor(cx,cy)
            if self._replace:
                self._dataLines[dt] = l.substring(to=dx) + evt.key + l.substring(fr=dx+1)
            else:
                self._dataLines[dt] = l.substring(to=dx) + evt.key + l.substring(fr=dx)
            self._rewrap()
            cx, cy = self._cursorFromDataPos(dt,dx+1)
            self._setCursorPos(cx, cy)
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
            selectColor = TTkCfg.theme.lineEditTextColorSelected
        else:
            selectColor = TTkCfg.theme.lineEditTextColorSelected

        h = self.height()
        for y, l in enumerate(self._lines[oy:oy+h]):
            t = self._dataLines[l[0]].substring(l[1][0],l[1][1]).tab2spaces(self._tabSpaces)
            if self._selectionFrom[1] <= y+oy <= self._selectionTo[1]:
                pf = 0      if y+oy > self._selectionFrom[1] else self._selectionFrom[0]
                pt = len(t) if y+oy < self._selectionTo[1]   else self._selectionTo[0]
                t = t.setColor(color=selectColor, posFrom=pf, posTo=pt )
            self._canvas.drawText(pos=(-ox,y), text=t)
        if self._lineWrapMode == TTkK.FixedWidth:
            self._canvas.drawVLine(pos=(self._wrapWidth,0), size=h, color=TTkCfg.theme.treeLineColor)
        self._pushCursor()

class TTkTextEdit(TTkAbstractScrollArea):
    __slots__ = (
            '_textEditView',
            # Forwarded Methods
            'setText', 'append', 'isReadOnly', 'setReadOnly'
            'wrapWidth', 'setWrapWidth',
            'lineWrapMode', 'setLineWrapMode',
            'wordWrapMode', 'setWordWrapMode',
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTextEdit' )
        self._textEditView = _TTkTextEditView()
        self.setViewport(self._textEditView)
        self.setText = self._textEditView.setText
        self.append  = self._textEditView.append
        self.isReadOnly  = self._textEditView.isReadOnly
        self.setReadOnly = self._textEditView.setReadOnly
        # Forward Wrap Methods
        self.wrapWidth       = self._textEditView.wrapWidth
        self.setWrapWidth    = self._textEditView.setWrapWidth
        self.lineWrapMode    = self._textEditView.lineWrapMode
        self.setLineWrapMode = self._textEditView.setLineWrapMode
        self.wordWrapMode    = self._textEditView.wordWrapMode
        self.setWordWrapMode = self._textEditView.setWordWrapMode

