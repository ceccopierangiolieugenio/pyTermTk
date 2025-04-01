# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['glbls']

from dataclasses import dataclass

import TermTk as ttk

from .state.brush  import Brush
from .state.layers import Layers
# from .canvaslayer import CanvasLayer

class Snapshot():
    __slots__ = ('_layer','_canvasLayers')
    def __init__(self) -> None:
        self._layer = glbls.layers.clone()
        self._canvasLayers = [cl.saveSnapshot() for cl in glbls.layers.layers()]

    def restore(self) -> None:
        if self._layer:
            glbls.layers.restore(self._layer)
        for cl,snapId in zip(glbls.layers.layers(),self._canvasLayers):
            cl.restoreSnapshot(snapId)

    def __eq__(self, value: object) -> bool:
        return (
            self._layer == value._layer and
            self._canvasLayers == value._canvasLayers )

class Glbls:
    def __init__(self) -> None:
        self.brush:Brush   = Brush()
        self.layers:Layers = Layers()
        self.documentSize  = (80,25)
        self.fileNameChanged = ttk.pyTTkSignal(str)

        self._filename = "untitled.DPT.json"

        self._snaphots     = []
        self._snapId:int   = 0

    def setFilename(self, fileName):
        self._filename = fileName
        self.fileNameChanged.emit(fileName)

    def fileName(self):
        return self._filename

    def clearSnapshot(self):
        self._snaphots     = []
        self._snapId:int   = 0

    def saveSnapshot(self):
        # TODO: Dispose properly of the unused clones
        snapshot = Snapshot()
        # if not snapshot.valid():
        #     return
        if 0 <= self._snapId < len(self._snaphots):
            if self._snaphots[self._snapId] == snapshot:
                return
        self._snaphots = self._snaphots[:self._snapId+1] + [snapshot]
        self._snapId = len(self._snaphots)-1

    @ttk.pyTTkSlot()
    def undo(self):
        # ttk.TTkLog.debug(f"{self._snapId=} - {len(self._snaphots)=}")
        if self._snapId:
            self._snapId -= 1
            self._snaphots[self._snapId].restore()

    @ttk.pyTTkSlot()
    def redo(self):
        if 0 <= self._snapId < len(self._snaphots)-1:
            self._snapId += 1
            self._snaphots[self._snapId].restore()

glbls = Glbls()
