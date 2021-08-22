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
import threading
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot

'''
             w1   w3   w2   w5
    Buffer |----|----|----|----|            cache buffer
             |      \ /       \
             |       x         \
             |      / \         \
    Pages  | 0  | 2  | 1  |None| 3  |None|  index to buffer
    File   |----|----|----|----|----|----|  view as list of windows
             w1   w2   w3   w4   w5   w6
'''
class TTkFileBuffer():
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

    __slots__ = (
        '_indexes', '_indexesMutex',
        '_filename', '_fd',
        '_pages', '_buffer',
        '_window', '_numW',
        '_width',
        #Signals
        'indexUpdated', 'indexed')
    def __init__(self, filename, window, numWindows):
        # Signals
        self.indexUpdated = pyTTkSignal(float)
        self.indexed = pyTTkSignal()

        self._window = window
        self._numW = numWindows
        self._filename = filename
        self._indexes = [0]
        self._indexesMutex = threading.Lock()
        self._width=0
        self._buffer = [None]*self._numW
        self._pages = [None]
        self._fd = open(self._filename,'r')
        threading.Thread(target=self.createIndex).start()

    def __del__(self):
        self._fd.close()

    def getLen(self):
        return len(self._indexes)

    def getWidth(self, indexes=None):
       return self._width

    def getLineDirect(self, line):
        if line >= self.getLen():
            return ""
        self._indexesMutex.acquire()
        self._fd.seek(self._indexes[line])
        self._indexesMutex.release()
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
            self._indexesMutex.acquire()
            self._fd.seek(self._indexes[line-offset])
            self._indexesMutex.release()
            buffer = self._pages[page].buffer
            for i in range(self._window):
                buffer[i] = self._fd.readline()
                #self._width = max(self._width,len(buffer[i]))
        else:
            # Push the page to the top of the buffer
            i = self._buffer.index(self._pages[page])
            p = self._buffer.pop(i)
            self._buffer.append(p)
        return self._pages[page].buffer[offset]

    def getSlice(self, line, length):
        ret = []
        for i in range(line, line+length):
            ret.append(self.getLine(i))
        return ret

    def createIndex(self):
        # TTkLog.debug(f"Start Indexing {self._filename}")
        indexes = []
        lines = 0
        offset = 0
        width = 0
        fileSize = os.stat(self._filename).st_size
        chunkSize = 0x1000000 # ~16M
        with open(self._filename,'r') as infile:
            while (chunk:=infile.read(chunkSize)):
                start = 0
                while (index:=chunk.find('\n',start))!=-1:
                    indexes.append(index+offset+1)
                    start = index+1
                self._indexesMutex.acquire()
                self._indexes += indexes
                self._pages += [None]*(1+(self.getLen()//self._window)-(len(self._pages)))
                self._indexesMutex.release()
                indexes = []
                offset+=len(chunk)
                self.indexUpdated.emit(offset/fileSize)
                # TTkLog.debug(f"{self._filename} {offset/fileSize} ...")
        self._width = max([ (self._indexes[i+1]-self._indexes[i]) for i in range(len(self._indexes)-1) ])
        self.indexUpdated.emit(1.0)
        self.indexed.emit()
        # TTkLog.debug(f"{self._filename} {offset/fileSize} END")

    def searchRe(self, regex, ignoreCase=False):
        indexes = []
        id = 0
        rr = re.compile(regex, re.IGNORECASE if ignoreCase else 0)
        with open(self._filename,'r') as infile:
            for line in infile:
                ma = rr.search(line)
                if ma:
                    indexes.append(id)
                id += 1
        return indexes

    def search(self, txt):
        indexes = []
        with open(self._filename,'r') as infile:
            for line in infile:
                if txt in line:
                    indexes.append(id)
        return indexes
