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

__all__ = ['LayersControl']

import TermTk as ttk

from .glbls import glbls
from .canvaslayer import CanvasLayer

class _layerButton(ttk.TTkContainer):
    classStyle = {
                'default':     {'color': ttk.TTkColor.fg("#dddd88")+ttk.TTkColor.bg("#000044"),
                                'borderColor': ttk.TTkColor.fg('#CCDDDD'),
                                'grid':1},
                'disabled':    {'color': ttk.TTkColor.fg('#888888'),
                                'borderColor':ttk.TTkColor.fg('#888888'),
                                'grid':0},
                'hover':       {'color': ttk.TTkColor.fg("#dddd88")+ttk.TTkColor.bg("#000050")+ttk.TTkColor.BOLD,
                                'borderColor': ttk.TTkColor.fg("#FFFFCC")+ttk.TTkColor.BOLD,
                                'grid':1},
                'selected':     {'color': ttk.TTkColor.fg("#dddd88")+ttk.TTkColor.bg("#004488"),
                                'borderColor': ttk.TTkColor.fg("#FFFF00"),
                                'grid':0},
                'unchecked':   {'color': ttk.TTkColor.fg("#dddd88")+ttk.TTkColor.bg("#000044"),
                                'borderColor': ttk.TTkColor.RST,
                                'grid':3},
                'clicked':     {'color': ttk.TTkColor.fg("#FFFFDD")+ttk.TTkColor.BOLD,
                                'borderColor': ttk.TTkColor.fg("#DDDDDD")+ttk.TTkColor.BOLD,
                                'grid':0},
                'focus':       {'color': ttk.TTkColor.fg("#dddd88")+ttk.TTkColor.bg("#000044")+ttk.TTkColor.BOLD,
                                'borderColor': ttk.TTkColor.fg("#ffff00") + ttk.TTkColor.BOLD,
                                'grid':1},
            }

    __slots__ = ('_canvasLayer','_first', '_isSelected',
                 '_ledit'
               )
    def __init__(self, layer:CanvasLayer, **kwargs):
        self._canvasLayer:CanvasLayer = layer
        self._isSelected = False
        self._first = True

        super().__init__(**kwargs|{'layout':ttk.TTkGridLayout()})
        self.setPadding(1,1,7,2)
        self._ledit = ttk.TTkLineEdit(parent=self, text=layer.name(),visible=False)
        self._ledit.focusChanged.connect(self._ledit.setVisible)
        self._ledit.textEdited.connect(self._textEdited)
        # self.setFocusPolicy(ttk.TTkK.ClickFocus)

    def data(self):
        return self._canvasLayer

    def setData(self, data):
        self._canvasLayer = data
        self.update()

    def setSelected(self, selected:bool=True) -> None:
        if self._isSelected == selected: return
        self._isSelected = selected
        self.update()

    @ttk.pyTTkSlot(str)
    def _textEdited(self, text):
        self._canvasLayer.setName(text)

    def mousePressEvent(self, evt) -> bool:
        if evt.x <= 3:
            self._canvasLayer.setVisible(not self._canvasLayer.visible())
        self.setFocus()
        self.update()
        return True

    def mouseReleaseEvent(self, evt) -> bool:
        glbls.layers.selectLayer(self._canvasLayer)
        return True

    def mouseDoubleClickEvent(self, evt) -> bool:
        self._ledit.setVisible(True)
        self._ledit.setFocus()
        return True

    def mouseDragEvent(self, evt) -> bool:
        drag = ttk.TTkDrag()
        drag.setData(self)
        name = self._canvasLayer.name()
        pm = ttk.TTkCanvas(width=len(name)+4,height=3)
        pm.drawBox(pos=(0,0),size=pm.size())
        pm.drawText(pos=(2,1), text=name)
        drag.setHotSpot(pos=(5, 1))
        drag.setPixmap(pm)
        drag.exec()
        return True

    def paintEvent(self, canvas: ttk.TTkCanvas):
        if self._isSelected:
            style = self.style()['selected']
        else:
            style = self.currentStyle()
        borderColor = style['borderColor']
        textColor   = style['color']
        btnVisible = '▣' if self._canvasLayer.visible() else '□'
        w,h = self.size()
        canvas.drawText(    pos=(0,0),text=f"     ┏{'━'*(w-7)}┓",color=borderColor)
        canvas.drawText(    pos=(0,2),text=f"     ┗{'━'*(w-7)}┛",color=borderColor)
        if self._first:
            canvas.drawText(pos=(0,1),text=f" {btnVisible} - ┃{' '*(w-7)}┃",color=borderColor)
        else:
            canvas.drawText(pos=(0,1),text=f" {btnVisible} - ╽{' '*(w-7)}╽",color=borderColor)
        canvas.drawTTkString(pos=(7,1),text=self._canvasLayer.name(), width=w-9, color=textColor)

class LayerScrollWidget(ttk.TTkAbstractScrollView):
    __slots__ = ('_layers','_layerButtons', '_dropTo')
    def __init__(self, **kwargs):
        self._layers = glbls.layers
        self._dropTo = None
        self._layerButtons:list[_layerButton] = []
        super().__init__(**kwargs)
        self.viewChanged.connect(self._placeTheButtons)
        self.viewChanged.connect(self._viewChangedHandler)

        glbls.layers.layerAdded.connect(self._layerAdded)
        glbls.layers.layerDeleted.connect(self._layerDeleted)
        glbls.layers.layerSelected.connect(self._layerSelected)
        glbls.layers.layersOrderChanged.connect(self._layersOrderChanged)

    @ttk.pyTTkSlot(CanvasLayer)
    def _layerAdded(self, data:CanvasLayer) -> None:
        self._updateLayerButtons()

    @ttk.pyTTkSlot(CanvasLayer)
    def _layerDeleted(self, data:CanvasLayer) -> None:
        self._updateLayerButtons()

    @ttk.pyTTkSlot(CanvasLayer)
    def _layerSelected(self, data:CanvasLayer) -> None:
        for btn in self._layerButtons:
            btn.setSelected(id(btn.data()) == id(data))

    @ttk.pyTTkSlot(list[CanvasLayer])
    def _layersOrderChanged(self, layers:list[CanvasLayer]) -> None:
        self._updateLayerButtons()

    def _updateLayerButtons(self):
        layers = glbls.layers.layers()
        selected = glbls.layers.selected()
        # remove unused buttons
        for btn in self._layerButtons[len(layers):]:
            self.layout().removeWidget(btn)
            btn._canvasLayer.nameChanged.clear()

        self._layerButtons = self._layerButtons[:len(layers)]
        for i,layer in enumerate(layers):
            if i >= len(self._layerButtons):
                self._layerButtons.append(_layerButton(parent=self,layer=layer))
            btn = self._layerButtons[i]
            btn.setData(layer)

        for btn in self._layerButtons:
            btn.setSelected(btn.data() == selected)

        self._placeTheButtons()
        self.viewChanged.emit()


    @ttk.pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def viewDisplayedSize(self) -> tuple:
        return self.size()

    def maximumWidth(self):   return 0x10000
    def maximumHeight(self):  return 0x10000
    def minimumWidth(self):   return 0
    def minimumHeight(self):  return 0

    def _placeTheButtons(self):
        w,h = self.size()
        for i,l in enumerate(self._layerButtons):
            l._first = i==0
            l.setGeometry(0,i*2,w,3)
            l.lowerWidget()
        self.update()

    def dragEnterEvent(self, evt) -> bool:
        if type(evt.data())!=_layerButton: return False
        x,y = self.getViewOffsets()
        self._dropTo = max(0,min(len(self._layerButtons),(evt.y-1+y)//2))
        self.update()
        return True
    def dragLeaveEvent(self, evt) -> bool:
        if type(evt.data())!=_layerButton: return False
        self._dropTo = None
        self.update()
        return True
    def dragMoveEvent(self, evt) -> bool:
        if type(evt.data())!=_layerButton: return False
        x,y = self.getViewOffsets()
        self._dropTo = max(0,min(len(self._layerButtons),(evt.y+y)//2))
        self.update()
        # ttk.TTkLog.debug(f"{evt.x},{evt.y-y} - {len(self._layerButtons)} - {self._dropTo}")
        return True
    def dropEvent(self, evt) -> bool:
        if type(evt.data())!=_layerButton: return False
        x,y = self.getViewOffsets()
        self._dropTo = None
        data = evt.data()
        dropPos = max(0,min(len(self._layerButtons),(evt.y+y)//2))
        # ttk.TTkLog.debug(f"{evt.x},{evt.y-y} - {len(self._layerButtons)} - {self._dropTo} {dropPos}")
        glbls.layers.moveLayer(self._layerButtons.index(data), dropPos)
        glbls.saveSnapshot()
        return True

    # Stupid hack to paint on top of the child widgets
    def paintChildCanvas(self):
        super().paintChildCanvas()
        offx, offy = self.getViewOffsets()
        if self._dropTo is None: return
        canvas = self.getCanvas()
        w,h = canvas.size()
        color = ttk.TTkColor.YELLOW
        canvas.drawText(pos=(0,(self._dropTo)*2-offy),text=f"╞{'═'*(w-2)}╍",color=color)



class LayersControl(ttk.TTkGridLayout):
    __slots__ = ('_scrollWidget')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._scrollWidget = _lsw = LayerScrollWidget()
        _sa = ttk.TTkAbstractScrollArea(scrollWidget=self._scrollWidget,minWidth=16)
        _sa.setViewport(_lsw)
        self.addWidget(_sa,0,0,1,5)
        self.addWidget(btnAdd :=ttk.TTkButton(text='add')           ,1,0)
        self.addWidget(btnUp  :=ttk.TTkButton(text='▲',maxWidth=3)  ,1,1)
        self.addWidget(btnDown:=ttk.TTkButton(text='▼',maxWidth=3)  ,1,2)
        # self.addItem(ttk.TTkLayout(),1,3)
        self.addWidget(btnDel :=ttk.TTkButton(text=ttk.TTkString('del',ttk.TTkColor.RED),maxWidth=5),1,4)

        btnAdd.setToolTip( "Create a new Layer\nand add it to the image")
        btnDel.setToolTip( "Delete the selected Layer")
        btnUp.setToolTip(  "Raise the selected Layer one step")
        btnDown.setToolTip("Lower the selected Layer one step")

        btnAdd.clicked.connect( glbls.layers.addLayer)
        btnDel.clicked.connect( glbls.layers.delLayer)
        btnUp.clicked.connect(  glbls.layers.moveUp)
        btnDown.clicked.connect(glbls.layers.moveDown)
        btnAdd.clicked.connect( glbls.saveSnapshot)
        btnDel.clicked.connect( glbls.saveSnapshot)
        btnUp.clicked.connect(  glbls.saveSnapshot)
        btnDown.clicked.connect(glbls.saveSnapshot)
