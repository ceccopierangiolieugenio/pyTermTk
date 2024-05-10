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

__all__ = ['Layers', 'LayerData']

import TermTk as ttk

class LayerData():
    __slots__ = ('_name','_data',
                 #signals
                 'nameChanged','visibilityToggled')
    def __init__(self,name:ttk.TTkString=ttk.TTkString('New'),data=None) -> None:
        self._name:ttk.TTkString = ttk.TTkString(name) if isinstance(name,str) else name
        self.visibilityToggled = ttk.pyTTkSignal(bool)
        self._data = data if data else {}
        self.nameChanged = ttk.pyTTkSignal(str)

    def name(self):
        return self._name
    def setName(self,name):
        self.nameChanged.emit(name)
        self._name = name

    def data(self):
        return self._data
    def setData(self,data):
        self._data = data

class Layers():
    __slots__ = ('_layers','_selected',
                 # Signals
                 'layerSelected','layerAdded','layerDeleted','layersOrderChanged')
    def __init__(self) -> None:
        self.layerSelected = ttk.pyTTkSignal(LayerData)
        self.layerAdded    = ttk.pyTTkSignal(LayerData)
        self.layerDeleted  = ttk.pyTTkSignal(LayerData)
        self.layersOrderChanged = ttk.pyTTkSignal(list[LayerData])

        self._selected = None
        self._layers:list[LayerData] = []

    def layers(self) -> list[LayerData]:
        return self._layers

    def layersData(self) -> list:
        return [ld.data() for ld in self._layers]

    def selected(self) -> LayerData:
        return self._selected.data()

    def isEmpty(self):
        return len(self._layers) == 0

    @ttk.pyTTkSlot()
    def clear(self) -> None:
        if not self._layers: return
        self._layers = []
        self._selected = None
        self.layerSelected.emit(None)
        self.layersOrderChanged.emit(self.layersData())

    @ttk.pyTTkSlot(int, int)
    def move(self, fr:int, to:int) -> None:
        obj = self._layers.pop(fr)
        if to>fr:
            to-=1
        self._layers.insert(to,obj)
        self.layersOrderChanged.emit(self.layersData())

    @ttk.pyTTkSlot()
    def addLayer(self,name:str=None, data=None) -> LayerData:
        name = name if name else f"Layer #{len(self._layers)}"
        ld=LayerData(name=name,data=data)
        self._layers.insert(0,ld)
        self._selected = ld
        self.layerAdded.emit(ld.data())
        self.layersOrderChanged.emit(self.layersData())
        if len(self._layers) == 1:
            self.layerSelected.emit(ld.data())
        return ld

    @ttk.pyTTkSlot()
    def delLayer(self) -> None:
        if not self._selected: return
        la = self._layers
        dl = la.pop(la.index(self._selected))
        self._selected = la[0] if la else None
        self.layerDeleted(dl.data())
        self.layersOrderChanged.emit(self.layersData())
        return dl

    def selectLayerByData(self, data) -> None:
       for lay in self._layers:
            if lay.data() == data:
                self._selected = lay
                self.layerSelected.emit(data)
                return

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
        self.layersOrderChanged.emit(self.layersData())
