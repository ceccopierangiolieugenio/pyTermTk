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

from ttkode.app.ttkode import TTKode, TTKodeWidget

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
    _ttkode:TTKode
    _openFileCb:Callable[[Any, int, int], Any]
    def __init__(self, ttkode:TTKode) -> None:
        self._ttkode = ttkode
        self._openFileCb = ttkode._openFile

    def ttkode(self) -> TTKode:
        return self._ttkode

    def iterWidgets(self, widType=TTKodeWidget):
        for kt, index in self._ttkode._kodeTab.iterItems():
            if issubclass(type(wid:=kt.widget(index)), widType):
                yield wid

    @ttk.pyTTkSlot(TTKodeWidget)
    def closeTab(self, widget:TTKodeWidget) -> None:
        for kt, index in self._ttkode._kodeTab.iterItems():
            if kt.widget(index)==widget:
                kt.removeTab(index)

    def setOpenFile(self, cb):
        self._openFileCb = cb

    def openFile(self, fileName:str, line:int=0, pos:int=0):
        return self._openFileCb(fileName, line, pos)

ttkodeProxy:TTKodeProxy = TTKodeProxy(ttkode=TTKode())