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
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkTemplates.color import TColor
from TermTk.TTkTemplates.text  import TText
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView



'''
             w1   w3   w2   w5
    Buffer |----|----|----|----|
             |      \ /       \
             |       x         \
             |      / \         \
    File   |----|----|----|----|----|----|
             w1   w2   w3   w4   w5   w6
'''
class _FileBuffer():
    class _Page:
        __slots__ = ('_page', '_size', '_buffer')
        def __init__(self, page, size):
            self._page = page
            self._size = size
            self._buffer = [""]*self._size
            #TTkLog.debug(f"{self._buffer}")
        @property
        def buffer(self):
            return self._buffer
        @property
        def page(self):
            return self._page

    __slots__ = ('_filename', '_indexes', '_fd', '_lastline', '_pages', '_buffer', '_window', '_numW', '_width')
    def __init__(self, filename, window, numWindows):
        self._window = window
        self._numW = numWindows
        self._filename = filename
        self._indexes = []
        self._width=0
        self.createIndex()
        self._buffer = [None]*self._numW
        self._pages = [None]*(1+self.getLen()//window)
        self._fd = open(self._filename,'r')

    def __del__(self):
        self._fd.close()

    def getLen(self):
        return len(self._indexes)

    def getWidth(self, indexes=None):
       return self._width

    def getLineDirect(self, line):
        if line >= self.getLen():
            return ""
        self._fd.seek(self._indexes[line])
        return self._fd.readline()

    def getLine(self, line):
        if line >= self.getLen():
            return ""
        page = line//self._window
        offset = line%self._window
        if self._pages[page] == None:
            # Dispose of the pages to the bottom
            dispose = self._buffer.pop(0)
            if dispose is not None:
                self._pages[dispose.page] = None
            self._pages[page] = self._Page(page, self._window)
            self._buffer.append(self._pages[page])
            self._fd.seek(self._indexes[line])
            buffer = self._pages[page].buffer
            for i in range(self._window):
                buffer[i] = self._fd.readline()
                self._width = max(self._width,len(buffer[i]))
        else:
            # Push the page to the top of the buffer
            i = self._buffer.index(self._pages[page])
            p = self._buffer.pop(i)
            self._buffer.append(p)
        return self._pages[page].buffer[offset]


    def createIndex(self):
        self._indexes = []
        lines = 0
        offset = 0
        with open(self._filename,'r') as infile:
            for line in infile:
                lines += 1
                self._indexes.append(offset)
                offset += len(line)

    def searchRe(self, regex):
        indexes = []
        id = 0
        rr = re.compile(regex)
        with open(self._filename,'r') as infile:
            for line in infile:
                ma = rr.match(line)
                if ma:
                    indexes.append(id)
                id += 1
        return indexes

    def search(self, txt):
        indexes = []
        id = 0
        with open(self._filename,'r') as infile:
            for line in infile:
                if txt in line:
                    indexes.append(id)
                id += 1
        return indexes

class _FileViewer(TTkAbstractScrollView):
    __slots__ = ('_fileBuffer', '_indexes', '_indexesMark', '_indexexSearched', '_selected')
    def __init__(self, *args, **kwargs):
        self._indexes = None
        self._indexesMark = []
        self._indexesSearched = []
        self._selected = None
        TTkAbstractScrollView.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_FileViewer' )
        self._fileBuffer = kwargs.get('filebuffer')
        self.viewChanged.connect(self._viewChangedHandler)

    @pyTTkSlot()
    def _viewChangedHandler(self):
        self.update()

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
        return False

    def paintEvent(self):
        ox,oy = self.getViewOffsets()
        if self._indexes is None:
            for i in range(min(self.height(),self._fileBuffer.getLen()-oy)):
                if (i+oy) in self._indexesSearched:
                    color = TTkColor.fg("#ff0000")
                else:
                    color = TTkColor.fg("#0000ff")
                self.getCanvas().drawText(pos=(0,i), text="●", color=color)
                self.getCanvas().drawText(pos=(2,i), text=self._fileBuffer.getLine(i+oy).replace('\t','    ').replace('\n','')[ox:] )
        else:
            for i in range(min(self.height(),len(self._indexes))):
                if self._indexes[i+oy] in self._indexesSearched:
                    color = TTkColor.fg("#ff0000")
                else:
                    color = TTkColor.fg("#0000ff")
                self.getCanvas().drawText(pos=(0,i), text="●", color=color)
                self.getCanvas().drawText(
                                    pos=(2,i),
                                    text=self._fileBuffer.getLineDirect(self._indexes[i+oy]).replace('\t','    ').replace('\n','')[ox:] )



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
        fileBuffer = _FileBuffer(file, 0x1000, 0x10)
        topViewer = FileViewer(parent=topFrame, filebuffer=fileBuffer)
        # Define the Search Viewer
        bottomViewer = FileViewer(parent=bottomFrame, filebuffer=fileBuffer)
        bottomViewport = bottomViewer.viewport()
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