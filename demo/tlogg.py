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

class _FileBuffer():
    __slots__ = ('_filename', '_indexes', '_fd', '_lastline')
    def __init__(self, filename, window):
        self._filename = filename
        self._indexes = []
        self.createIndex()
        self._fd = open(self._filename,'r')
        self._lastline = {'line':0, 'txt':self._fd.readline()}

    def __del__(self):
        self._fd.close()

    def getLen(self):
        return len(self._indexes)

    def getLine(self, line):
        if line >= self.getLen():
            return ""
        if self._lastline['line'] != line :
            self._fd.seek(self._indexes[line])
            self._lastline = {'line':line, 'txt':self._fd.readline()}
        return self._lastline['txt']


    def createIndex(self):
        self._indexes = []
        lines = 0
        offset = 0
        with open(self._filename,'r') as infile:
            for line in infile:
                lines += 1
                self._indexes.append(offset)
                offset += len(line)

    def search(self, regex):
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

class _FileViewer(TTkAbstractScrollView):
    __slots__ = ('_fileBuffer', '_indexes', '_indexesMark')
    def __init__(self, *args, **kwargs):
        self._indexes = None
        self._indexesMark = []
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


    def viewFullAreaSize(self) -> (int, int):
        if self._indexes is None:
            w = 300
            h = self._fileBuffer.getLen()
        else:
            w = 300
            h = len(self._indexes)
        return w , h

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def paintEvent(self):
        ox,oy = self.getViewOffsets()
        if self._indexes is None:
            for i in range(self.height()):
                if (i+oy) in self._indexesMark:
                    color = TTkColor.fg("#ff0000")
                else:
                    color = TTkColor.fg("#0000ff")
                self.getCanvas().drawText(pos=(0,i), text="⏺", color=color)
                self.getCanvas().drawText(pos=(2,i), text=self._fileBuffer.getLine(i+oy).replace('\t','    ').replace('\n','') )
        else:
            for i in range(min(self.height(),len(self._indexes))):
                if self._indexes[i+oy] in self._indexesMark:
                    color = TTkColor.fg("#ff0000")
                else:
                    color = TTkColor.fg("#0000ff")
                self.getCanvas().drawText(pos=(0,i), text="⏺", color=color)
                self.getCanvas().drawText(
                                    pos=(2,i),
                                    text=self._fileBuffer.getLine(self._indexes[i+oy]).replace('\t','    ').replace('\n','') )



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
        bls_label   = TTkLabel(text="Text:", maxWidth=6)
        bls_textbox = TTkLineEdit()
        bls_search  = TTkButton(text="Search", maxWidth=7)

        bottomLayoutSearch.addWidget(bls_label)
        bottomLayoutSearch.addWidget(bls_textbox)
        bottomLayoutSearch.addWidget(bls_search)

        bottomFrame.layout().addItem(bottomLayoutSearch)

        # Define the main file Viewer
        fileBuffer = _FileBuffer(file, 5000)
        topViewer = FileViewer(parent=topFrame, filebuffer=fileBuffer)
        # Define the Search Viewer
        bottomViewer = FileViewer(parent=bottomFrame, filebuffer=fileBuffer)
        bottomViewport = bottomViewer.viewport()
        # indexes = fileBuffer.search(r'.*1234.*')
        bottomViewport.showIndexes([])

        class _search:
            def __init__(self,tb,fb,tvp,bvp):
                self.tb=tb
                self.fb=fb
                self.tvp=tvp
                self.bvp=bvp
            def search(self):
                searchtext = self.tb.text()
                indexes = self.fb.search(searchtext)
                self.bvp.showIndexes(indexes)
                self.bvp.markIndexes(indexes)
                self.tvp.markIndexes(indexes)
        _s = _search(bls_textbox,fileBuffer,topViewer.viewport(),bottomViewport)
        bls_search.clicked.connect(_s.search)
        bls_textbox.returnPressed.connect(_s.search)


    root.mainloop()

if __name__ == "__main__":
    main()