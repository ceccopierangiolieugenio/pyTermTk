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
        self._layer = None
        self._canvasLayers = []
        if glbls.layers._modified:
            self._layer = glbls.layers.clone()
            glbls.layers._modified = False
        for cl in glbls.layers.layers():
            if cl._modified:
                cl._modified = False
                self._canvasLayers.append((cl,cl.clone()))

    def valid(self) -> None:
        if self._layer or self._canvasLayers:
            return True
        return False

    def restore(self) -> None:
        if self._layer:
            glbls.layers.restore(self._layer)
        for cl,clone in self._canvasLayers:
            cl.restore(clone)

    def __eq__(self, value: object) -> bool:
        if self._layer != value._layer:
            return False
        for (a,_),(b,_) in zip(self._canvasLayers,value._canvasLayers):
            if a!=b:
                return False
        return True



@dataclass()
class Glbls:
    brush:Brush   = Brush()
    layers:Layers = Layers()
    documentSize  = (80,25)

    _snaphots     = []
    _snapId:int   = 0

    def clearSnapshot(self):
        self._snaphots     = []
        self._snapId:int   = 0

    def saveSnapshot(self):
        # TODO: Dispose properly of the unused clones
        snapshot = Snapshot()
        if not snapshot.valid():
            return
        self._snaphots = self._snaphots[:self._snapId+1] + [snapshot]
        self._snapId = len(self._snaphots)-1

    @ttk.pyTTkSlot()
    def undo(self):
        if self._snapId:
            self._snapId -= 1
            self._snaphots[self._snapId].restore()

    @ttk.pyTTkSlot()
    def redo(self):
        if 0 <= self._snapId < len(self._snaphots)-1:
            self._snapId += 1
            self._snaphots[self._snapId].restore()

glbls = Glbls()
