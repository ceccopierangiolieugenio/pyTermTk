# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTKodeViewerProxy', 'ttkodeProxy']

from typing import Optional, Callable, Any

import TermTk as ttk

from ttkode.app.ttkode import TTKode

class TTKodeViewerProxy():
    __slots__ = ('_fileName')
    def __init__(self, fileName) -> None:
        self._fileName = fileName

    def fileName(self):
        return self._fileName

class TTKodeProxy():
    __slots__ = ('_openFileCb',
                 '_ttkode',
                 # Signals
                 )
    _ttkode:Optional[TTKode]
    _openFileCb:Optional[Callable[[Any, int, int], Any]]
    def __init__(self) -> None:
        self._openFileCb = None
        self._ttkode = None

    def setTTKode(self, ttkode:TTKode) -> None:
        self._ttkode = ttkode
        self._openFileCb = ttkode._openFile

    def ttkode(self) -> TTKode:
        if not self._ttkode:
            raise Exception("TTkode uninitialized")
        return self._ttkode

    def setOpenFile(self, cb):
        self._openFileCb = cb

    def openFile(self, fileName:str, line:int=0, pos:int=0):
        if self._ttkode and self._openFileCb:
            return self._openFileCb(fileName, line, pos)

ttkodeProxy:TTKodeProxy = TTKodeProxy()