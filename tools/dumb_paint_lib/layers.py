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

__all__ = ['Layers','LayerData']

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

class LayerData():
    __slots__ = ('_name','_data',
                 #signals
                 'nameChanged','visibilityToggled')
    def __init__(self,name:ttk.TTkString=ttk.TTkString('New'),data=None) -> None:
        self._name:ttk.TTkString = ttk.TTkString(name) if type(name)==str else name
        self.visibilityToggled = ttk.pyTTkSignal(bool)
        self._data = data
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

    __slots__ = ('_layerData','_first', '_isSelected', '_layerVisible',
                 '_ledit',
               # signals
               'clicked', 'visibilityToggled',
               )
    def __init__(self, layer:LayerData, **kwargs):
        self.clicked = ttk.pyTTkSignal(_layerButton)
        self._layerData:LayerData = layer
        self._isSelected = False
        self._first = True
        self._layerVisible = True
        self.visibilityToggled = layer.visibilityToggled

        super().__init__(**kwargs|{'layout':ttk.TTkGridLayout()})
        self.setPadding(1,1,7,2)
        self._ledit = ttk.TTkLineEdit(parent=self, text=layer.name(),visible=False)
        self._ledit.focusChanged.connect(self._ledit.setVisible)
        self._ledit.textEdited.connect(self._textEdited)
        # self.setFocusPolicy(ttk.TTkK.ClickFocus)

    @ttk.pyTTkSlot(str)
    def _textEdited(self, text):
        self._layerData.setName(text)

    def mousePressEvent(self, evt) -> bool:
        if evt.x <= 3:
            self._layerVisible = not self._layerVisible
            self.visibilityToggled.emit(self._layerVisible)
        self.setFocus()
        self.update()
        return True

    def mouseReleaseEvent(self, evt) -> bool:
        self.clicked.emit(self)
        return True

    def mouseDoubleClickEvent(self, evt) -> bool:
        self._ledit.setVisible(True)
        self._ledit.setFocus()
        return True

    def mouseDragEvent(self, evt) -> bool:
        drag = ttk.TTkDrag()
        drag.setData(self)
        name = self._layerData.name()
        pm = ttk.TTkCanvas(width=len(name)+4,height=3)
        pm.drawBox(pos=(0,0),size=pm.size())
        pm.drawText(pos=(2,1), text=name)
        drag.setHotSpot(5, 1)
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
        btnVisible = '▣' if self._layerVisible else '□'
        w,h = self.size()
        canvas.drawText(    pos=(0,0),text=f"     ┏{'━'*(w-7)}┓",color=borderColor)
        canvas.drawText(    pos=(0,2),text=f"     ┗{'━'*(w-7)}┛",color=borderColor)
        if self._first:
            canvas.drawText(pos=(0,1),text=f" {btnVisible} - ┃{' '*(w-7)}┃",color=borderColor)
        else:
            canvas.drawText(pos=(0,1),text=f" {btnVisible} - ╽{' '*(w-7)}╽",color=borderColor)
        canvas.drawTTkString(pos=(7,1),text=self._layerData.name(), width=w-9, color=textColor)

class LayerScrollWidget(ttk.TTkAbstractScrollView):
    __slots__ = ('_layers','_selected', '_dropTo',
                 # Signals
                 'layerSelected','layerAdded','layerDeleted','layersOrderChanged')
    def __init__(self, **kwargs):
        self.layerSelected = ttk.pyTTkSignal(LayerData)
        self.layerAdded    = ttk.pyTTkSignal(LayerData)
        self.layerDeleted  = ttk.pyTTkSignal(LayerData)
        self.layersOrderChanged = ttk.pyTTkSignal(list[LayerData])

        self._selected = None
        self._dropTo = None
        self._layers:list[_layerButton] = []
        super().__init__(**kwargs)
        self.viewChanged.connect(self._placeTheButtons)
        self.viewChanged.connect(self._viewChangedHandler)

    @ttk.pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def viewFullAreaSize(self) -> tuple:
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w,h

    def viewDisplayedSize(self) -> tuple:
        return self.size()

    def maximumWidth(self):   return 0x10000
    def maximumHeight(self):  return 0x10000
    def minimumWidth(self):   return 0
    def minimumHeight(self):  return 0

    @ttk.pyTTkSlot(_layerButton)
    def _clickedLayer(self, layerButton:_layerButton):
        if sel:=self._selected:
            sel._isSelected = False
            sel.update()
        self._selected = layerButton
        layerButton._isSelected = True
        self.layerSelected.emit(layerButton._layerData)
        self.update()

    def clear(self):
        for layBtn in self._layers:
            self.layout().removeWidget(layBtn)
            layBtn.clicked.clear()
            layBtn.visibilityToggled.clear()
            layBtn._layerData.nameChanged.clear()
        self._layers.clear()
        self.update()

    @ttk.pyTTkSlot()
    def moveUp(self):
        return self._moveButton(-1)

    @ttk.pyTTkSlot()
    def moveDown(self):
        return self._moveButton(+1)

    def _moveButton(self,direction):
        if not self._selected: return
        index = self._layers.index(self._selected)
        if index+direction < 0: return
        l = self._layers.pop(index)
        self._layers.insert(index+direction,l)
        self._placeTheButtons()
        self.layersOrderChanged.emit([_l._layerData for _l in self._layers])

    @ttk.pyTTkSlot()
    def addLayer(self,name=None, data=None):
        name = name if name else f"Layer #{len(self._layers)}"
        _l=LayerData(name=name,data=data)
        newLayerBtn:_layerButton  = _layerButton(parent=self,layer=_l)
        self._layers.insert(0,newLayerBtn)
        if sel:=self._selected: sel._isSelected = False
        self._selected = newLayerBtn
        newLayerBtn._isSelected = True
        newLayerBtn.clicked.connect(self._clickedLayer)
        self.viewChanged.emit()
        self._placeTheButtons()
        self.layerAdded.emit(newLayerBtn._layerData)
        return _l

    def _placeTheButtons(self):
        w,h = self.size()
        for i,l in enumerate(self._layers):
            l._first = i==0
            l.setGeometry(0,i*2,w,3)
            l.lowerWidget()
        self.update()

    @ttk.pyTTkSlot()
    def delLayer(self):
        self._layers.remove()

    def dragEnterEvent(self, evt) -> bool:
        if type(evt.data())!=_layerButton: return False
        x,y = self.getViewOffsets()
        self._dropTo = max(0,min(len(self._layers),(evt.y-1+y)//2))
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
        self._dropTo = max(0,min(len(self._layers),(evt.y-1+y)//2))
        self.update()
        ttk.TTkLog.debug(f"{evt.x},{evt.y-y} - {len(self._layers)} - {self._dropTo}")
        return True
    def dropEvent(self, evt) -> bool:
        if type(evt.data())!=_layerButton: return False
        x,y = self.getViewOffsets()
        self._dropTo = None
        data = evt.data()
        # dropPos = len(self._layers)-(evt.y-1)//2
        dropPos = max(0,min(len(self._layers),(evt.y-1+y)//2))
        ttk.TTkLog.debug(f"{evt.x},{evt.y-y} - {len(self._layers)} - {self._dropTo} {dropPos}")
        if dropPos > self._layers.index(data):
            dropPos -= 1
        self._layers.remove(data)
        self._layers.insert(dropPos,data)
        self._placeTheButtons()
        self.layersOrderChanged.emit([_l._layerData for _l in self._layers])
        return True

    # Stupid hack to paint on top of the child widgets
    def paintChildCanvas(self):
        super().paintChildCanvas()
        offx, offy = self.getViewOffsets()
        if self._dropTo == None: return
        canvas = self.getCanvas()
        w,h = canvas.size()
        color = ttk.TTkColor.YELLOW
        canvas.drawText(pos=(0,(self._dropTo)*2-offy),text=f"╞{'═'*(w-2)}╍",color=color)



class Layers(ttk.TTkGridLayout):
    __slots__ = ('_scrollWidget',
                 # Forward Methods
                 'addLayer','clear',
                 # Forward Signals
                 'layerSelected','layerAdded','layerDeleted','layersOrderChanged')
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

        btnAdd.clicked.connect( _lsw.addLayer)
        btnDel.clicked.connect( _lsw.delLayer)
        btnUp.clicked.connect(  _lsw.moveUp)
        btnDown.clicked.connect(_lsw.moveDown)

        # forward signals
        self.layerSelected = _lsw.layerSelected
        self.layerSelected = _lsw.layerSelected
        self.layerAdded    = _lsw.layerAdded
        self.layerDeleted  = _lsw.layerDeleted
        self.layersOrderChanged = _lsw.layersOrderChanged

        # forward methods
        self.addLayer = _lsw.addLayer
        self.clear    = _lsw.clear
