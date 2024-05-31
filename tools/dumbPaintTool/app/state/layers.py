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

__all__ = ['Layers']

import TermTk as ttk
from ..canvaslayer import CanvasLayer


class Layers():
    __slots__ = ('_layers','_selected', '_modified',
                 # Signals
                 'layerSelected','layerAdded','layerDeleted','layersOrderChanged','changed')
    def __init__(self) -> None:
        self._modified = True
        self.changed       = ttk.pyTTkSignal()
        self.layerSelected = ttk.pyTTkSignal(CanvasLayer)
        self.layerAdded    = ttk.pyTTkSignal(CanvasLayer)
        self.layerDeleted  = ttk.pyTTkSignal(CanvasLayer)
        self.layersOrderChanged = ttk.pyTTkSignal(list[CanvasLayer])

        self._selected = None
        self._layers:list[CanvasLayer] = []

    def clone(self) -> None:
        la = Layers()
        la._modified = False
        la._selected = self._selected
        la._layers   = self._layers.copy()
        return la

    def restore(self, la) -> None:
        self._modified = False
        self._selected = la._selected
        self._layers   = la._layers.copy()
        self.layersOrderChanged.emit(self._layers)
        self.layerSelected.emit(self._selected)
        self.changed.emit()

    def __eq__(self, value: object) -> bool:
        return self._layers == value._layers

    def __len__(self):
        return len(self._layers)

    def layers(self) -> list[CanvasLayer]:
        return self._layers

    def selected(self) -> CanvasLayer:
        return self._selected

    def isEmpty(self):
        return len(self._layers) == 0

    @ttk.pyTTkSlot()
    def clear(self) -> None:
        if not self._layers: return
        self._layers = []
        self._selected = None
        self.layerSelected.emit(None)
        self.layersOrderChanged.emit(self._layers)

    @ttk.pyTTkSlot()
    def addLayer(self,name:ttk.TTkString=None) -> CanvasLayer:
        from ..glbls import glbls
        name = ttk.TTkString(name if name else f"Layer #{len(self._layers)}")
        ld=CanvasLayer(name=name)
        ld.resize(*glbls.documentSize)
        ld.changed.connect(self.changed.emit)
        self._layers.insert(0,ld)
        self._selected = ld
        self._modified = True
        self.layerAdded.emit(ld)
        self.layersOrderChanged.emit(self._layers)
        self.layerSelected.emit(self._selected)
        return ld

    @ttk.pyTTkSlot()
    def delLayer(self) -> None:
        if not self._selected: return
        la = self._layers
        dl = la.pop(la.index(self._selected))
        self._selected = la[0] if la else None
        self._modified = True
        self.layerDeleted.emit(dl)
        self.layersOrderChanged.emit(self._layers)
        return dl

    def selectLayer(self, layer) -> None:
       if layer in self._layers:
           self._selected = layer
           self.layerSelected.emit(layer)

    @ttk.pyTTkSlot()
    def moveUp(self):
        return self._moveLayer(-1)

    @ttk.pyTTkSlot()
    def moveDown(self):
        return self._moveLayer(+1)

    def _moveLayer(self,direction):
        if not self._selected: return
        index = self._layers.index(self._selected)
        if index+direction < 0: return
        la = self._layers.pop(index)
        self._layers.insert(index+direction,la)
        self._modified = True
        self.layersOrderChanged.emit(self._layers)

    def moveLayer(self, fr:int, to:int) -> None:
        if not self._layers: return
        if fr == to: return
        fr = max(0,fr)
        to = max(0,to) - (1 if to>fr else 0)
        # ttk.TTkLog.debug(f"{fr=} {to=}")
        la = self._layers.pop(fr)
        self._modified = True
        self._layers.insert(to,la)
        self.layersOrderChanged.emit(self._layers)
