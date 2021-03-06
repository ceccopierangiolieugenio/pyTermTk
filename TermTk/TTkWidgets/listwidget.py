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

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.label import TTkLabel
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class _TTkListWidgetText(TTkLabel):
    __slots__ = ('selected', '_selected')
    def __init__(self, *args, **kwargs):
        TTkLabel.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkListWidgetText' )
        # Define Signals
        self.selected = pyTTkSignal(_TTkListWidgetText)
        self._selected = False

    def mouseReleaseEvent(self, evt):
        self.selected.emit(self)
        return True

class TTkListWidget(TTkAbstractScrollView):
    __slots__ = ('itemClicked', 'textClicked', '_color', '_selectedColor', '_selectedItems', '_selectionMode')
    def __init__(self, *args, **kwargs):
        # Default Class Specific Values
        self._selectionMode = kwargs.get("selectionMode", TTkK.SingleSelection)
        self._selectedItems = []
        self._color = TTkCfg.theme.listColor
        self._selectedColor = TTkCfg.theme.listColorSelected
        # Signals
        self.itemClicked = pyTTkSignal(TTkWidget)
        self.textClicked = pyTTkSignal(str)
        # Init Super
        TTkAbstractScrollView.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkListWidget' )
        self.viewChanged.connect(self._viewChangedHandler)

    @pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().groupMoveTo(-x,-y)

    @pyTTkSlot(_TTkListWidgetText)
    def _labelSelectedHandler(self, label):
        if self._selectionMode == TTkK.SingleSelection:
            for i in self._selectedItems:
                i._selected = False
                i.color = TTkCfg.theme.listColor
            label._selected = True
        elif self._selectionMode == TTkK.MultiSelection:
            label._selected = not label._selected
        if label._selected:
            self._selectedItems.append(label)
        else:
            self._selectedItems.remove(label)
        if label._selected:
            label.color = TTkCfg.theme.listColorSelected
        else:
            label.color = TTkCfg.theme.listColor

        self.textClicked.emit(label.text)

    def setSelectionMode(self, mode):
        self._selectionMode = mode

    def selectedLabels(self):
        return [i.text for i in self._selectedItems]

    def resizeEvent(self, w, h):
        maxw = 0
        for item in self.layout().children():
            maxw = max(maxw,item.minimumWidth())
        maxw = max(self.width(),maxw)
        for item in self.layout().children():
            x,y,_,h = item.geometry()
            item.setGeometry(x,y,maxw,h)
        self.viewChanged.emit()

    def viewFullAreaSize(self) -> (int, int):
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w , h

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def addItem(self, item):
        if isinstance(item, str):
            label = _TTkListWidgetText(text=item, width=max(len(item),self.width()))
            label.selected.connect(self._labelSelectedHandler)
            return self.addItem(label)
        _,y,_,h = self.layout().fullWidgetAreaGeometry()
        self.addWidget(item)
        item.move(0,y+h)
        _,_,fw,_ = self.layout().fullWidgetAreaGeometry()
        w = self.width()
        for item in self.layout().children():
            x,y,_,h = item.geometry()
            item.setGeometry(x,y,max(w-1,fw),h)
        self.viewChanged.emit()