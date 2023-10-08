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

__all__ = ['TTkAbstractListItem', 'TTkListWidget']

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.string import TTkString
from TermTk.TTkGui.drag import TTkDrag
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class TTkAbstractListItem(TTkWidget):
    '''TTkAbstractListItem'''

    classStyle = TTkWidget.classStyle | {
                'default':     {'color': TTkColor.RST},
                'highlighted': {'color': TTkColor.fg('#00FF00')+TTkColor.bg('#0055FF')+TTkColor.UNDERLINE},
                'hover':       {'color': TTkColor.fg('#00FF00')+TTkColor.bg('#0088FF')},
                'selected':    {'color': TTkColor.fg('#00FF00')+TTkColor.bg('#0055FF')},
                'clicked':     {'color': TTkColor.fg('#FFFF00')},
                'disabled':    {'color': TTkColor.fg('#888888')},
            }

    __slots__ = ('_text', '_selected', '_highlighted', '_data',
                 'listItemClicked')
    def __init__(self, *, text='', data=None, **kwargs):
        self.listItemClicked = pyTTkSignal(TTkAbstractListItem)

        self._selected = False
        self._highlighted = False

        self._text = TTkString(text)
        self._data  = data

        super().__init__(**kwargs)

        self.setFocusPolicy(TTkK.ParentFocus)

    def text(self):
        return self._text

    def setText(self, text):
        self._text = TTkString(text)
        self.update()

    def data(self):
        '''data'''
        return self._data

    def setData(self, data):
        '''setData'''
        if self._data == data: return
        self._data = data
        self.update()

    def mousePressEvent(self, evt) -> bool:
        self.listItemClicked.emit(self)
        return True

    def _setSelected(self, selected):
        if self._selected == selected: return
        self._selected = selected
        self._highlighted = not selected
        self.update()

    def _setHighlighted(self, highlighted):
        if self._highlighted == highlighted: return
        self._highlighted = highlighted
        self.update()

    def paintEvent(self, canvas):
        style = self.currentStyle()
        if style == self.classStyle['hover']:
            pass
        elif self._highlighted:
            style = self.style()['highlighted']
        elif self._selected:
            style = self.style()['selected']

        w = self.width()

        canvas.drawTTkString(pos=(0,0), width=w, color=style['color'] ,text=self._text)

class TTkListWidget(TTkAbstractScrollView):
    '''TTkListWidget'''
    __slots__ = ('itemClicked', 'textClicked',
                 '_selectedItems', '_selectionMode',
                 '_highlighted', '_items',
                 '_dragPos')
    def __init__(self, *args, **kwargs):
        # Default Class Specific Values
        self._selectionMode = kwargs.get("selectionMode", TTkK.SingleSelection)
        self._selectedItems = []
        self._items = []
        self._highlighted = None
        self._dragPos = None
        # Signals
        self.itemClicked = pyTTkSignal(TTkWidget)
        self.textClicked = pyTTkSignal(str)
        # Init Super
        TTkAbstractScrollView.__init__(self, *args, **kwargs)
        self.viewChanged.connect(self._viewChangedHandler)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    @pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    @pyTTkSlot(TTkAbstractListItem)
    def _labelSelectedHandler(self, label:TTkAbstractListItem):
        if self._selectionMode == TTkK.SingleSelection:
            for item in self._selectedItems:
                item._setSelected(False)
                item._setHighlighted(False)
            self._selectedItems = [label]
            label._setSelected(True)
        elif self._selectionMode == TTkK.MultiSelection:
            for item in self._selectedItems:
                item._setHighlighted(False)
            label._setSelected(not label._selected)
            if label._selected:
                self._selectedItems.append(label)
            else:
                self._selectedItems.remove(label)
        if self._highlighted:
            self._highlighted._setHighlighted(False)
        label._setHighlighted(True)
        self._highlighted = label
        self.itemClicked.emit(label)
        self.textClicked.emit(label.text())

    def setSelectionMode(self, mode):
        '''setSelectionMode'''
        self._selectionMode = mode

    def selectedItems(self):
        '''selectedItems'''
        return self._selectedItems

    def selectedLabels(self):
        '''selectedLabels'''
        return [i.text() for i in self._selectedItems]

    def items(self):
        '''items'''
        return self._items

    def resizeEvent(self, w, h):
        maxw = 0
        for item in self.layout().children():
            maxw = max(maxw,item.minimumWidth())
        maxw = max(self.width(),maxw)
        for item in self.layout().children():
            x,y,_,h = item.geometry()
            item.setGeometry(x,y,maxw,h)
        TTkAbstractScrollView.resizeEvent(self, w, h)

    def viewFullAreaSize(self) -> (int, int):
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w, h

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def addItem(self, item, data=None):
        '''addItem'''
        self.addItemAt(item, len(self._items), data)

    def _placeItems(self):
        minw = self.width()
        for item in self._items:
            minw = max(minw,item.minimumWidth())
        for y,item in enumerate(self._items):
            item.setGeometry(0,y,minw,1)
        self.viewChanged.emit()
        self.update()

    def addItemAt(self, item, pos, data=None):
        '''addItemAt'''
        if isinstance(item, str) or isinstance(item, TTkString):
            #label = TTkAbstractListItem(text=item, width=max(len(item),self.width()))
            label = TTkAbstractListItem(text=item, data=data)
            return self.addItemAt(label,pos)
        item.listItemClicked.connect(self._labelSelectedHandler)
        self._items.insert(pos,item)
        self.layout().addWidget(item)
        self._placeItems()

    def indexOf(self, item):
        '''indexOf'''
        for i, it in enumerate(self._items):
            if it == item:
                return i
        return -1

    def itemAt(self, pos):
        '''itemAt'''
        return self._items[pos]

    def moveItem(self, fr, to):
        '''moveItem'''
        fr = max(min(fr,len(self._items)-1),0)
        to = max(min(to,len(self._items)-1),0)
        # Swap
        self._items[to] , self._items[fr] = self._items[fr] , self._items[to]
        self._placeItems()

    def removeItem(self, item):
        '''removeItem'''
        self.removeItems([item])

    def removeItems(self, items):
        '''removeItems'''
        self.layout().removeWidgets(items)
        for item in items.copy():
            item.listItemClicked.disconnect(self._labelSelectedHandler)
            item._setSelected(False)
            item._setHighlighted(False)
            self._items.remove(item)
            if item in self._selectedItems:
                self._selectedItems.remove(item)
            if item == self._highlighted:
                self._highlighted = None
        self._placeItems()

    def removeAt(self, pos):
        '''removeAt'''
        self.removeItem(self._items[pos])

    def setCurrentRow(self, row):
        '''setCurrentRow'''
        if row<len(self._items):
            item = self._items[row]
            self.setCurrentItem(item)

    def setCurrentItem(self, item):
        '''setCurrentItem'''
        item.listItemClicked.emit(item)

    def _moveToHighlighted(self):
        index = self._items.index(self._highlighted)
        h = self.height()
        offx,offy = self.getViewOffsets()
        if index >= h+offy-1:
            TTkLog.debug(f"{index} {h} {offy}")
            self.viewMoveTo(offx, index-h+1)
        elif index <= offy:
            self.viewMoveTo(offx, index)

    def mouseDragEvent(self, evt) -> bool:
        TTkLog.debug("Start DnD")
        if not (items:=self._selectedItems.copy()):
            return True
        drag = TTkDrag()
        data = (self,items)
        h = min(3,ih:=len(items)) + 2 + (1 if ih>3 else 0)
        w = min(20,iw:=max([it.text().termWidth() for it in items[:3]])) + 2
        pm = TTkCanvas(width=w,height=h)
        for y,it in enumerate(items[:3],1):
            txt = it.text()
            pm.drawText(pos=(1,y), text=it.text())
            if txt.termWidth() >= 20:
                pm.drawText(pos=(18,y), text='...')
        if ih>3:
            pm.drawText(pos=(1,4), text='...')
        pm.drawBox(pos=(0,0),size=(w,h))
        drag.setPixmap(pm)
        drag.setData(data)
        drag.exec()
        return True

    def dragEnterEvent(self, evt):
        return self.dragMoveEvent(evt)

    def dragMoveEvent(self, evt):
        offx,offy = self.getViewOffsets()
        y=min(evt.y+offy,len(self._items))
        self._dragPos = (offx+evt.x, y)
        self.update()
        return True

    def dragLeaveEvent(self, evt):
        self._dragPos = None
        self.update()
        return True

    def dropEvent(self, evt) -> bool:
        TTkLog.debug(f"Drop pos={evt.pos()}")
        self._dragPos = None
        offx,offy = self.getViewOffsets()
        wid,items = evt.data()
        # check the correct wid type
        if wid and items:
            wid.removeItems(items)
            for it in reversed(items):
                it.setCurrentStyle(it.style()['default'])
                self.addItemAt(it,offy+evt.y)
            return True
        return False

    def keyEvent(self, evt):
        if not self._highlighted: return False
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            if self._highlighted:
                # TTkLog.debug(self._highlighted)
                self._highlighted.listItemClicked.emit(self._highlighted)
            return True
        elif evt.type == TTkK.SpecialKey:
            if evt.key == TTkK.Key_Tab:
                return False
            index = self._items.index(self._highlighted)
            offx,offy = self.getViewOffsets()
            h = self.height()
            if evt.key == TTkK.Key_Up:
                index = max(0, index-1)
            elif evt.key == TTkK.Key_Down:
                index = min(len(self._items)-1, index+1)
            elif evt.key == TTkK.Key_PageUp:
                index = max(0, index-h)
            elif evt.key == TTkK.Key_PageDown:
                index = min(len(self._items)-1, index+h)
            elif evt.key == TTkK.Key_Right:
                self.viewMoveTo(offx+1, offy)
            elif evt.key == TTkK.Key_Left:
                self.viewMoveTo(offx-1, offy)
            elif evt.key == TTkK.Key_Home:
                self.viewMoveTo(0, offy)
            elif evt.key == TTkK.Key_End:
                self.viewMoveTo(0x10000, offy)

            self._highlighted._setHighlighted(False)
            self._highlighted = self._items[index]
            self._highlighted._setHighlighted(True)
            self._moveToHighlighted()
            return True
        return False

    def focusInEvent(self):
        if not self._items: return
        if not self._highlighted:
            self._highlighted = self._items[0]
        self._highlighted._setHighlighted(True)
        self._moveToHighlighted()

    def focusOutEvent(self):
        if self._highlighted:
            self._highlighted._setHighlighted(False)
        self._dragPos = None

    # Stupid hack to paint on top of the child widgets
    def paintChildCanvas(self):
        super().paintChildCanvas()
        if self._dragPos:
            canvas = self.getCanvas()
            x,y = self._dragPos
            offx,offy = self.getViewOffsets()
            p1 = (0,y-offy-1)
            p2 = (0,y-offy)
            canvas.drawText(pos=p1,text="╙─╼", color=TTkColor.fg("#FFFF00")+TTkColor.bg("#008855"))
            canvas.drawText(pos=p2,text="╓─╼", color=TTkColor.fg("#FFFF00")+TTkColor.bg("#008855"))


