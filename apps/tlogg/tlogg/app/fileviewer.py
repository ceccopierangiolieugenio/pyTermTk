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

__all__ = ['FileViewer','FileViewerSearch','FileViewerArea']

import TermTk as ttk

from tlogg import TloggHelper, tloggProxy

from . import TloggCfg

class FileViewer(ttk.TTkAbstractScrollView):
    __slots__ = (
        '_fileBuffer', '_indexesMark', '_indexesSearched',
        '_selected', '_indexing', '_searchRe',
        '_selection', '_pressed'
        # Signals
        'selected', 'marked')
    def __init__(self, *args, **kwargs):
        self._indexesMark = []
        self._indexesSearched = []
        self._indexing = None
        self._selected = -1
        self._selection = None
        self._pressed = False
        self._searchRe = ""
        # Signals
        self.selected = ttk.pyTTkSignal(int)
        self.marked = ttk.pyTTkSignal(list)
        self._fileBuffer = kwargs.get('filebuffer')
        super().__init__(*args, **kwargs)
        self.viewChanged.connect(self._viewChangedHandler)
        self.setFocusPolicy(ttk.TTkK.ClickFocus)

    @ttk.pyTTkSlot()
    def _viewChangedHandler(self):
        self.update()

    def _copy(self):
        clipboard = ttk.TTkClipboard()
        lines = ttk.TTkString().join([
            self.getLine(i) for i in range(min(self._selection),max(self._selection)+1) ])
        clipboard.setText(lines)

    @ttk.pyTTkSlot(float)
    def fileIndexing(self, percentage):
        self._indexing = percentage
        self.viewChanged.emit()

    @ttk.pyTTkSlot()
    def fileIndexed(self):
        self._indexing = None
        self.viewChanged.emit()

    def markIndexes(self, indexes):
        self._indexesMark = indexes
        self.viewChanged.emit()

    def searchedIndexes(self, indexes):
        self._indexesSearched = indexes
        self.viewChanged.emit()

    def searchRe(self, searchRe):
        self._searchRe = searchRe
        self.update()

    def viewFullAreaSize(self) -> (int, int):
        w = 10+self._fileBuffer.getWidth()
        h = self._fileBuffer.getLen()
        return ( w , h )

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def keyEvent(self, evt):
        # Enable CTRL+C = Copy
        if ( evt.type == ttk.TTkK.SpecialKey and
             evt.mod  == ttk.TTkK.ControlModifier and
             evt.key  == ttk.TTkK.Key_C ):
                self._copy()

    def mousePressEvent(self, evt):
        x,y = evt.x, evt.y
        ox,oy = self.getViewOffsets()
        index = oy+y
        self._selection = [index,index]
        self._pressed = True
        if 0 <= index < self._fileBuffer.getLen():
            if x<3:
                if index in self._indexesMark:
                    self._indexesMark.pop(self._indexesMark.index(index))
                else:
                    self._indexesMark.append(index)
                self.marked.emit(self._indexesMark)
            else:
                self._selected = index
                self.selected.emit(self._selected)
                tloggProxy.lineSelected.emit(self.getLine(self._selected))
            self.update()
            return True
        return super().mousePressEvent(evt)

    def mouseDragEvent(self, evt) -> bool:
        if self._pressed and self._selection:
            w,h = self.size()
            x,y = evt.x, evt.y
            lines=self._fileBuffer.getLen()
            ox,oy = self.getViewOffsets()
            index = oy+y
            self._selection[1] = min(max(0,index),lines-1)
            if y < 0:
                self.viewMoveTo(ox, max(0,min(oy+min(y,3),lines-h)))
            elif y >= h:
                self.viewMoveTo(ox, max(0,min(oy+min(y-h,3),lines-h)))
            else:
                self.update()
        return super().mouseDragEvent(evt)

    def mouseReleaseEvent(self, evt) -> bool:
        self._pressed = False
        if self._selection and self._selection[0] != self._selection[1]:
            self._copy()
        self.update()
        return super().mouseReleaseEvent(evt)

    @ttk.pyTTkSlot(int)
    def selectAndMove(self, line):
        self._selected = line
        self._selection = [line,line]
        ox,_ = self.getViewOffsets()
        self.viewMoveTo(ox, max(0,line-self.height()//2))
        self.update()

    def getLen(self):
        return self._fileBuffer.getLen()

    def getLine(self, num) -> str:
        return self._fileBuffer.getLine(num)

    def getLineNum(self, num) -> int:
        return num

    def paintEvent(self, canvas):
        ox,oy = self.getViewOffsets()
        bufferLen = self.getLen()
        for i in range(min(self.height(),bufferLen-oy)):
            line = ttk.TTkString(self.getLine(i+oy).replace('\n','')).tab2spaces()
            lineNum = self.getLineNum(i+oy)
            if lineNum in self._indexesMark:
                symbolcolor = ttk.TTkColor.fg("#00ffff")
                numberColor = ttk.TTkColor.bg("#444444")
                symbol='❥'
            elif lineNum in self._indexesSearched:
                symbolcolor = ttk.TTkColor.fg("#ff0000")
                numberColor = ttk.TTkColor.bg("#444444")
                symbol='●'
            else:
                symbolcolor = ttk.TTkColor.fg("#0000ff")
                numberColor = ttk.TTkColor.bg("#444444")
                symbol='○'

            if i+oy == self._selected:
                selectedColor = ttk.TTkColor.bg("#008844")
                searchedColor = ttk.TTkColor.fg("#FFFF00")+ttk.TTkColor.bg("#004400")
                line = line.setColor(selectedColor)
            elif self._selection and min(self._selection) <= i+oy <= max(self._selection):
                selectedColor = ttk.TTkColor.bg("#008888")
                searchedColor = ttk.TTkColor.fg("#FFFF00")+ttk.TTkColor.bg("#004400")
                line = line.setColor(selectedColor)
            else:
                selectedColor = ttk.TTkColor.RST
                searchedColor = ttk.TTkColor.fg("#000000")+ttk.TTkColor.bg("#AAAAAA")
                # Check in the filters a matching color
                for color in TloggCfg.colors:
                    #TTkLog.debug(f"{color['pattern']} - {line}")
                    if m := line.findall(regexp=color['pattern'], ignoreCase=color['ignorecase']):
                        selectedColor = ttk.TTkColor.fg(color['fg'])+ttk.TTkColor.bg(color['bg'])
                        searchedColor = ttk.TTkColor.fg(color['bg'])+ttk.TTkColor.bg(color['fg'])
                        line = line.setColor(selectedColor)
                        break
            if self._searchRe:
                if m := line.findall(regexp=self._searchRe, ignoreCase=True):
                    for match in m:
                        line = line.setColor(searchedColor, match=match)

            # Add Line Number
            lenLineNumber = len(str(self.getLineNum(bufferLen-1)))
            lineNumber = ttk.TTkString() + numberColor + str(lineNum).rjust(lenLineNumber) + ttk.TTkColor.RST + ' '
            # Compose print line
            printLine = ttk.TTkString() + symbolcolor + symbol + ttk.TTkColor.RST + ' ' + lineNumber + line.substring(ox)
            # stupid scramble
            # printLine._text = ''.join([chr(121-(ord(l)-65)) if (65<=ord(l)<=121) else l for l in printLine._text])
            canvas.drawText(pos=(0,i), text=printLine, color=selectedColor, width=self.width(), )

        # Draw the loading banner
        if self._indexing is not None:
            canvas.drawText(pos=(0,0), text=f" [ Indexed: {int(100*self._indexing)}% ] ")

class FileViewerSearch(FileViewer):
    __slots__ = ('_indexes')
    def __init__(self, *args, **kwargs):
        self._indexes = []
        FileViewer.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'FileViewerSearch' )

    def markIndexes(self, indexes):
        self._indexesMark = indexes
        self._indexes = [i for i in sorted(set(self._indexesSearched+self._indexesMark))]
        ox,oy = self.getViewOffsets()
        self.viewMoveTo(ox,oy)
        self.update()

    def searchedIndexes(self, indexes):
        # Get the current lineSelected to be used to scroll
        # the search viewer to the similar to previous position
        lineSelected = -1
        if self._selected > -1:
            lineSelected = self._indexes[self._selected]

        self._indexesSearched = indexes
        self._indexes = [i for i in sorted(set(self._indexesSearched+self._indexesMark))]
        ox,_ = self.getViewOffsets()

        lineToMove = 0
        if lineSelected > -1:
            for i, lineNum in enumerate(self._indexes):
                if lineNum >= lineSelected:
                   if lineNum == lineSelected:
                       self._selected = i
                   else:
                       self._selected = -1
                   # Try to keep the  selected area at the center of the widget
                   lineToMove = i if i <= self.height()/2 else int(i-self.height()/2)
                   break

        self.viewMoveTo(ox, lineToMove)
        self.update()

    def viewFullAreaSize(self) -> (int, int):
        if self._indexes is None:
            w = 2+self._fileBuffer.getWidth()
            h = self._fileBuffer.getLen()
        else:
            w = 2+self._fileBuffer.getWidth(self._indexes)
            h = len(self._indexes)
        return w , h

    def mousePressEvent(self, evt):
        x,y = evt.x, evt.y
        ox,oy = self.getViewOffsets()
        index = oy+y
        self._selection = [index,index]
        self._pressed = True
        if 0 <= index < len(self._indexes):
            if x<3:
                index = self._indexes[oy+y]
                if index in self._indexesMark:
                    self._indexesMark.pop(self._indexesMark.index(index))
                else:
                    self._indexesMark.append(index)
                self.markIndexes(self._indexesMark)
                self.marked.emit(self._indexesMark)
            else:
                self._selected = index
                self.selected.emit(self._indexes[self._selected])
                tloggProxy.lineSelected.emit(self.getLine(self._selected))
            self.update()
            return True
        return False

    def getLen(self):
        return len(self._indexes)

    def getLine(self, num) -> str:
        return self._fileBuffer.getLine(self._indexes[num])

    def getLineNum(self, num) -> int:
        return self._indexes[num]

class FileViewerArea(ttk.TTkAbstractScrollArea):
    __slots__ = ('_fileView')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = kwargs.get('name' , 'FileViewer' )
        if 'parent' in kwargs: kwargs.pop('parent')
        self._fileView = kwargs.get('fileView')
        self.setFocusPolicy(ttk.TTkK.ClickFocus)
        self.setViewport(self._fileView)
