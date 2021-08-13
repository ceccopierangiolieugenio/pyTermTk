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

import os
import re
import sys
import argparse

sys.path.append(os.path.join(sys.path[0],'..'))

from TermTk import *

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.ttk import TTk
from TermTk.TTkCore.filebuffer import TTkFileBuffer
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkTemplates.color import TColor
from TermTk.TTkTemplates.text  import TText
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView


class _FileViewer(TTkAbstractScrollView):
    __slots__ = (
        '_fileBuffer', '_indexesMark', '_indexesSearched', '_selected', '_indexing',
        # Signals
        'selected', 'marked')
    def __init__(self, *args, **kwargs):
        self._indexesMark = []
        self._indexesSearched = []
        self._indexing = None
        self._selected = -1
        # Signals
        self.selected = pyTTkSignal(int)
        self.marked = pyTTkSignal(list)
        TTkAbstractScrollView.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_FileViewer' )
        self._fileBuffer = kwargs.get('filebuffer')
        self.viewChanged.connect(self._viewChangedHandler)

    @pyTTkSlot()
    def _viewChangedHandler(self):
        self.update()

    @pyTTkSlot(float)
    def fileIndexing(self, percentage):
        self._indexing = percentage
        self.viewChanged.emit()

    @pyTTkSlot()
    def fileIndexed(self):
        self._indexing = None
        self.viewChanged.emit()

    def markIndexes(self, indexes):
        self._indexesMark = indexes
        self.viewChanged.emit()

    def searchedIndexes(self, indexes):
        self._indexesSearched = indexes
        self.viewChanged.emit()

    def viewFullAreaSize(self) -> (int, int):
        w = 2+self._fileBuffer.getWidth()
        h = self._fileBuffer.getLen()
        return w , h

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def mousePressEvent(self, evt):
        x,y = evt.x, evt.y
        ox,oy = self.getViewOffsets()
        index = oy+y
        if oy+y<self._fileBuffer.getLen():
            if x<3:
                if index in self._indexesMark:
                    self._indexesMark.pop(self._indexesMark.index(index))
                else:
                    self._indexesMark.append(index)
                self.marked.emit(self._indexesMark)
            else:
                self._selected = index
                self.selected.emit(self._selected)
            self.update()
            return True
        return False

    @pyTTkSlot(int)
    def selectAndMove(self, line):
        self._selected = line
        ox,_ = self.getViewOffsets()
        self.viewMoveTo(ox, max(0,line-self.height()//2))
        self.update()

    def paintEvent(self):
        ox,oy = self.getViewOffsets()
        for i in range(min(self.height(),self._fileBuffer.getLen()-oy)):
            if (i+oy) in self._indexesMark:
                color = TTkColor.fg("#00ffff")
                symbol='❥'
            elif (i+oy) in self._indexesSearched:
                color = TTkColor.fg("#ff0000")
                symbol='●'
            else:
                color = TTkColor.fg("#0000ff")
                symbol='○'
            if i+oy == self._selected:
                selectedColor = TTkColor.bg("#008844")
            else:
                selectedColor = TTkColor.RST
            self.getCanvas().drawText(pos=(0,i), text=symbol, color=color)
            self.getCanvas().drawText(pos=(2,i), text=self._fileBuffer.getLine(i+oy).replace('\t','    ').replace('\n','')[ox:], color=selectedColor )
        if self._indexing is not None:
            self.getCanvas().drawText(pos=(0,0), text=f" [ Indexed: {int(100*self._indexing)}% ] ")

class _FileViewerSearch(_FileViewer):
    __slots__ = ('_indexes')
    def __init__(self, *args, **kwargs):
        self._indexes = []
        _FileViewer.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_FileViewerSearch' )

    def markIndexes(self, indexes):
        self._indexesMark = indexes
        self._indexes = [i for i in set(sorted(self._indexesSearched+self._indexesMark))]
        ox,oy = self.getViewOffsets()
        self.viewMoveTo(ox,oy)
        self.update()

    def searchedIndexes(self, indexes):
        self._indexesSearched = indexes
        self._indexes = [i for i in set(sorted(self._indexesSearched+self._indexesMark))]
        ox,_ = self.getViewOffsets()
        self.viewMoveTo(ox, 0)
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
        if index<len(self._indexes):
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
            self.update()
            return True
        return False

    def paintEvent(self):
        ox,oy = self.getViewOffsets()
        if self._indexes:
            allIndexes = self._indexes
            for i in range(min(self.height(),len(allIndexes)-oy)):
                if allIndexes[i+oy] in self._indexesMark:
                    color = TTkColor.fg("#00ffff")
                    numberColor = TTkColor.bg("#444444")
                    symbol='❥'
                elif allIndexes[i+oy] in self._indexesSearched:
                    color = TTkColor.fg("#ff0000")
                    numberColor = TTkColor.bg("#444444")
                    symbol='●'
                else:
                    color = TTkColor.fg("#0000ff")
                    numberColor = TTkColor.bg("#444444")
                    symbol='○'
                if i+oy == self._selected:
                    selectedColor = TTkColor.bg("#008844")
                else:
                    selectedColor = TTkColor.RST
                lenLineNumber = len(str(allIndexes[-1]))
                self.getCanvas().drawText(pos=(0,i), text=symbol, color=color)
                # Draw Linenumber
                self.getCanvas().drawText(
                                    pos=(3+lenLineNumber,i),
                                    text=self._fileBuffer.getLineDirect(allIndexes[i+oy]).replace('\t','    ').replace('\n','')[ox:], color=selectedColor )
                # Draw Line
                self.getCanvas().drawText(pos=(2,i), text=str(allIndexes[i+oy])+" "*lenLineNumber, width=lenLineNumber, color=numberColor)
        if self._indexing is not None:
            self.getCanvas().drawText(pos=(0,0), text=f" [ Indexed: {int(100*self._indexing)}% ] ")

class FileViewer(TTkAbstractScrollArea):
    __slots__ = ('_fileView')
    def __init__(self, *args, **kwargs):
        TTkAbstractScrollArea.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'FileViewer' )
        if 'parent' in kwargs: kwargs.pop('parent')
        self._fileView = kwargs.get('fileView')
        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._fileView)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    parser.add_argument('filename', type=str, nargs='+',
                    help='the filename')
    args = parser.parse_args()

    TTkLog.use_default_file_logging()

    root = TTk(layout=TTkGridLayout())
    splitter = TTkSplitter(parent=root, orientation=TTkK.VERTICAL)
    tab = TTkTabWidget(parent=splitter, border=False)
    splitter.addWidget(TTkLogViewer(),3)

    for file in args.filename:
        tabSplitter = TTkSplitter(orientation=TTkK.VERTICAL)
        tab.addTab(tabSplitter, file)
        topFrame    = TTkFrame(parent=tabSplitter, border=False, layout=TTkVBoxLayout())
        bottomFrame = TTkFrame(parent=tabSplitter, border=False, layout=TTkVBoxLayout())


        # Define the bottom layout widgets
        bottomLayoutSearch = TTkHBoxLayout()
        bls_label_1 = TTkLabel(text="Text:", maxWidth=6)
        bls_textbox = TTkLineEdit()
        bls_label_2 = TTkLabel(text="re:", maxWidth=3)
        bls_cb_re   = TTkCheckbox(maxWidth=3)
        bls_search  = TTkButton(text="Search", maxWidth=10)

        bottomLayoutSearch.addWidget(bls_label_2)
        bottomLayoutSearch.addWidget(bls_cb_re)
        bottomLayoutSearch.addWidget(bls_label_1)
        bottomLayoutSearch.addWidget(bls_textbox)
        bottomLayoutSearch.addWidget(bls_search)

        bottomFrame.layout().addItem(bottomLayoutSearch)

        # Define the main file Viewer
        fileBuffer = TTkFileBuffer(file, 0x1000, 0x10)
        topViewport = _FileViewer(filebuffer=fileBuffer)
        topViewer = FileViewer(parent=topFrame, fileView=topViewport)
        fileBuffer.indexUpdated.connect(topViewport.fileIndexing)
        fileBuffer.indexed.connect(topViewport.fileIndexed)
        # Define the Search Viewer
        bottomViewport = _FileViewerSearch(filebuffer=fileBuffer)
        bottomViewer = FileViewer(parent=bottomFrame, fileView=bottomViewport)
        bottomViewport.selected.connect(topViewport.selectAndMove)
        bottomViewport.marked.connect(topViewport.markIndexes)
        topViewport.marked.connect(bottomViewport.markIndexes)

        class _search:
            def __init__(self,tb,fb,cb,tvp,bvp):
                self.tb=tb
                self.fb=fb
                self.cb=cb
                self.tvp=tvp
                self.bvp=bvp
            def search(self):
                searchtext = self.tb.text()
                if self.cb.checkState() == TTkK.Checked:
                    indexes = self.fb.searchRe(searchtext)
                else:
                    indexes = self.fb.search(searchtext)
                self.bvp.searchedIndexes(indexes)
                self.tvp.searchedIndexes(indexes)
        _s = _search(bls_textbox,fileBuffer,bls_cb_re,topViewport,bottomViewport)
        bls_search.clicked.connect(_s.search)
        bls_textbox.returnPressed.connect(_s.search)


    root.mainloop()

if __name__ == "__main__":
    main()