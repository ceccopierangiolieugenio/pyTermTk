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
        '_fileBuffer', '_indexes', '_indexesMark', '_indexexSearched', '_selected', '_indexing',
        # Signals
        'selected')
    def __init__(self, *args, **kwargs):
        self._indexes = None
        self._indexesMark = []
        self._indexesSearched = []
        self._indexing = None
        self._selected = -1
        # Signals
        self.selected = pyTTkSignal(int)
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

    def showIndexes(self, indexes):
        self._indexes = indexes
        self.viewChanged.emit()

    def markIndexes(self, indexes):
        self._indexesMark = indexes
        self.viewChanged.emit()

    def searchedIndexes(self, indexes):
        self._indexesSearched = indexes
        self.viewChanged.emit()

    def viewFullAreaSize(self) -> (int, int):
        if self._indexes is None:
            w = 2+self._fileBuffer.getWidth()
            h = self._fileBuffer.getLen()
        else:
            w = 2+self._fileBuffer.getWidth(self._indexes)
            h = len(self._indexes)
        return w , h

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def mousePressEvent(self, evt):
        x,y = evt.x, evt.y
        ox,oy = self.getViewOffsets()
        if self._indexes is None:
            if oy+y<self._fileBuffer.getLen():
                self._selected = oy+y
                self.update()
                self.selected.emit(self._selected)
                return True
        else:
            if oy+y<len(self._indexes):
                self._selected = oy+y
                self.update()
                self.selected.emit(self._indexes[self._selected])
                return True
        return False

    @pyTTkSlot(int)
    def selectAndMove(self, line):
        self._selected = line
        ox,_ = self.getViewOffsets()
        self.viewMoveTo(ox, line)

    def paintEvent(self):
        ox,oy = self.getViewOffsets()
        if self._indexes is None:
            for i in range(min(self.height(),self._fileBuffer.getLen()-oy)):
                if (i+oy) in self._indexesSearched:
                    color = TTkColor.fg("#ff0000")
                else:
                    color = TTkColor.fg("#0000ff")
                if i+oy == self._selected:
                    selectedColor = TTkColor.bg("#008844")
                else:
                    selectedColor = TTkColor.RST
                self.getCanvas().drawText(pos=(0,i), text="●", color=color)
                self.getCanvas().drawText(pos=(2,i), text=self._fileBuffer.getLine(i+oy).replace('\t','    ').replace('\n','')[ox:], color=selectedColor )
        else:
            for i in range(min(self.height(),len(self._indexes))):
                if self._indexes[i+oy] in self._indexesSearched:
                    color = TTkColor.fg("#ff0000")
                    numberColor = TTkColor.bg("#444444")
                else:
                    color = TTkColor.fg("#0000ff")
                    numberColor = TTkColor.bg("#444444")
                if i+oy == self._selected:
                    selectedColor = TTkColor.bg("#008844")
                else:
                    selectedColor = TTkColor.RST
                lenLineNumber = len(str(self._indexes[-1]))
                self.getCanvas().drawText(pos=(0,i), text="●", color=color)
                # Draw Linenumber
                self.getCanvas().drawText(
                                    pos=(3+lenLineNumber,i),
                                    text=self._fileBuffer.getLineDirect(self._indexes[i+oy]).replace('\t','    ').replace('\n','')[ox:], color=selectedColor )
                # Draw Line
                self.getCanvas().drawText(pos=(2,i), text=str(self._indexes[i+oy])+" "*lenLineNumber, width=lenLineNumber, color=numberColor)
        if self._indexing is not None:
            self.getCanvas().drawText(pos=(0,0), text=f" [ Indexed: {int(100*self._indexing)}% ] ")


class FileViewer(TTkAbstractScrollArea):
    __slots__ = ('_fileView')
    def __init__(self, *args, **kwargs):
        TTkAbstractScrollArea.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'FileViewer' )
        if 'parent' in kwargs: kwargs.pop('parent')
        self._fileView = _FileViewer(filebuffer=kwargs.get('filebuffer'))
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
    TTkLogViewer(parent=splitter)

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
        topViewer = FileViewer(parent=topFrame, filebuffer=fileBuffer)
        fileBuffer.indexUpdated.connect(topViewer.viewport().fileIndexing)
        fileBuffer.indexed.connect(topViewer.viewport().fileIndexed)
        # Define the Search Viewer
        bottomViewer = FileViewer(parent=bottomFrame, filebuffer=fileBuffer)
        bottomViewport = bottomViewer.viewport()
        bottomViewport.selected.connect(topViewer.viewport().selectAndMove)
        # indexes = fileBuffer.search(r'.*1234.*')
        bottomViewport.showIndexes([])

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
                self.bvp.showIndexes(indexes)
                self.bvp.searchedIndexes(indexes)
                self.tvp.searchedIndexes(indexes)
        _s = _search(bls_textbox,fileBuffer,bls_cb_re,topViewer.viewport(),bottomViewport)
        bls_search.clicked.connect(_s.search)
        bls_textbox.returnPressed.connect(_s.search)


    root.mainloop()

if __name__ == "__main__":
    main()