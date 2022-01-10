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
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkWidgets.treewidgetitem import TTkTreeWidgetItem
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollView
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot

from dataclasses import dataclass

class TTkTreeWidget(TTkAbstractScrollView):
    __slots__ = ( '_rootItem', '_header', '_columnsPos', '_cache',
                  '_selectedId', '_selected', '_separatorSelected', '_mouseDelta',
                  '_headerColor', '_selectedColor', '_lineColor',
                  '_sortColumn', '_sortOrder',
                  # Signals
                  'itemChanged', 'itemClicked', 'itemDoubleClicked', 'itemExpanded', 'itemCollapsed', 'itemActivated'
                  )
    @dataclass(frozen=True)
    class _Cache:
        item: TTkTreeWidgetItem
        level: int
        data: list

    def __init__(self, *args, **kwargs):
        # Signals
        self.itemActivated     = pyTTkSignal(TTkTreeWidgetItem, int)
        self.itemChanged       = pyTTkSignal(TTkTreeWidgetItem, int)
        self.itemClicked       = pyTTkSignal(TTkTreeWidgetItem, int)
        self.itemDoubleClicked = pyTTkSignal(TTkTreeWidgetItem, int)
        self.itemExpanded      = pyTTkSignal(TTkTreeWidgetItem)
        self.itemCollapsed     = pyTTkSignal(TTkTreeWidgetItem)

        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTreeView' )
        self._selected = None
        self._selectedId = None
        self._separatorSelected = None
        self._header = kwargs.get('header',[])
        self._columnsPos = []
        self._cache = []
        self._sortColumn = -1
        self._sortOrder = TTkK.AscendingOrder
        self._headerColor   = kwargs.get('headerColor',   TTkCfg.theme.treeHeaderColor)
        self._selectedColor = kwargs.get('selectedColor', TTkCfg.theme.treeSelectedColor)
        self._lineColor     = kwargs.get('lineColor',     TTkCfg.theme.treeLineColor)
        self.setMinimumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus)
        self._rootItem = None
        self.clear()


    # Overridden function
    def viewFullAreaSize(self) -> (int, int):
        w = self._columnsPos[-1]+1 if self._columnsPos else 0
        h = self._rootItem.size()
        # TTkLog.debug(f"{w=} {h=}")
        return w,h

    # Overridden function
    def viewDisplayedSize(self) -> (int, int):
        # TTkLog.debug(f"{self.size()=}")
        return self.size()

    def clear(self):
        if self._rootItem:
            self._rootItem.dataChanged.disconnect(self._refreshCache)
        self._rootItem = TTkTreeWidgetItem(expanded=True)
        self._rootItem.dataChanged.connect(self._refreshCache)
        self.sortItems(self._sortColumn, self._sortOrder)
        self._refreshCache()
        self.viewChanged.emit()
        self.update()

    def addTopLevelItem(self, item):
        self._rootItem.addChild(item)
        self._refreshCache()
        self.viewChanged.emit()
        self.update()

    def setHeaderLabels(self, labels):
        self._header = labels
        # Set 20 as default column size
        self._columnsPos = [20+x*20 for x in range(len(labels))]
        self.viewChanged.emit()
        self.update()

    def sortColumn(self):
        '''Returns the column used to sort the contents of the widget.'''
        return self._sortColumn

    def sortItems(self, col, order):
        '''Sorts the items in the widget in the specified order by the values in the given column.'''
        self._sortColumn = col
        self._sortOrder = order
        self._rootItem.sortChildren(col, order)

    def mouseDoubleClickEvent(self, evt):
        x,y = evt.x, evt.y
        ox, oy = self.getViewOffsets()
        y += oy-1
        x += ox
        if 0 <= y < len(self._cache):
            item  = self._cache[y].item
            if item.childIndicatorPolicy() == TTkK.DontShowIndicatorWhenChildless and item.children() or \
               item.childIndicatorPolicy() == TTkK.ShowIndicator:
                item.setExpanded(not item.isExpanded())
                if item.isExpanded():
                    self.itemExpanded.emit(item)
                else:
                    self.itemCollapsed.emit(item)
            if self._selected:
                self._selected.setSelected(False)
            self._selectedId = y
            self._selected = item
            self._selected.setSelected(True)
            col = -1
            for i, c in enumerate(self._columnsPos):
                if x < c:
                    col = i
                    break
            self.itemDoubleClicked.emit(item, col)
            self.itemActivated.emit(item, col)

            self.update()
        return True

    def focusOutEvent(self):
        self._separatorSelected = None

    def mousePressEvent(self, evt):
        x,y = evt.x, evt.y
        ox, oy = self.getViewOffsets()

        x += ox

        self._separatorSelected = None
        self._mouseDelta = (evt.x, evt.y)

        # Handle Header Events
        if y == 0:
            for i, c in enumerate(self._columnsPos):
                if x == c:
                    # I-th separator selected
                    self._separatorSelected = i
                    self.update()
                    break
                elif x < c:
                    # I-th header selected
                    order = not self._sortOrder if self._sortColumn == i else TTkK.AscendingOrder
                    self.sortItems(i, order)
                    break
            return True
        # Handle Tree/Table Events
        y += oy-1
        if 0 <= y < len(self._cache):
            item  = self._cache[y].item
            level = self._cache[y].level
            if level*2 <= x < level*2+3 and \
               ( item.childIndicatorPolicy() == TTkK.DontShowIndicatorWhenChildless and item.children() or \
                 item.childIndicatorPolicy() == TTkK.ShowIndicator ):
                item.setExpanded(not item.isExpanded())
                if item.isExpanded():
                    self.itemExpanded.emit(item)
                else:
                    self.itemCollapsed.emit(item)
            else:
                if self._selected:
                    self._selected.setSelected(False)
                self._selectedId = y
                self._selected = item
                self._selected.setSelected(True)
            col = -1
            for i, c in enumerate(self._columnsPos):
                if x < c:
                    col = i
                    break
            self.itemClicked.emit(item, col)
            self.update()
        return True

    def mouseDragEvent(self, evt):
        '''
        ::

            columnPos       (Selected = 2)
                0       1        2          3   4
            ----|-------|--------|----------|---|
            Mouse (Drag) Pos
                                    ^
            I consider at least 4 char (3+1) as spacing
            Min Selected Pos = (Selected+1) * 4

        '''
        if self._separatorSelected is not None:
            x,y = evt.x, evt.y
            ox, oy = self.getViewOffsets()
            y += oy
            x += ox
            ss = self._separatorSelected
            pos = max((ss+1)*4, x)
            diff = pos - self._columnsPos[ss]
            # Align the previous Separators if pushed
            for i in range(ss):
                self._columnsPos[i] = min(self._columnsPos[i], pos-(ss-i)*4)
            # Align all the other Separators relative to the selection
            for i in range(ss, len(self._columnsPos)):
                self._columnsPos[i] += diff
            self.update()
            self.viewChanged.emit()
            return True
        return False

    @pyTTkSlot()
    def _refreshCache(self):
        ''' I save a representation fo the displayed tree in a cache array
            to avoid eccessve recursion over the items and
            identify quickly the nth displayed line to improve the interaction

            _cache is an array of TTkTreeWidget._Cache:
            [ item, level, data=[txtCol1, txtCol2, txtCol3, ... ]]
        '''
        self._cache = []
        def _addToCache(_child, _level):
            _data = []
            for _il in range(len(self._header)):
                _icon = _child.icon(_il)
                if _icon:
                    _icon = ' '+_icon+' '
                if _il==0:
                    _data.append('  '*_level+_icon+_child.data(_il))
                else:
                    _data.append(_icon+_child.data(_il))

            self._cache.append(TTkTreeWidget._Cache(
                                item  = _child,
                                level = _level,
                                data  = _data))
            if _child.isExpanded():
                for _c in _child.children():
                   _addToCache(_c, _level+1)
        for c in self._rootItem.children():
            _addToCache(c,0)
        self.update()
        self.viewChanged.emit()

    def paintEvent(self):
        x,y = self.getViewOffsets()
        w,h = self.size()
        tt = TTkCfg.theme.tree

        # Draw header first:
        for i,l in enumerate(self._header):
            hx  = 0 if i==0 else self._columnsPos[i-1]+1
            hx1 = self._columnsPos[i]
            self._canvas.drawText(pos=(hx-x,0), text=l, width=hx1-hx, color=self._headerColor)
            if i == self._sortColumn:
                s = tt[6] if self._sortOrder == TTkK.AscendingOrder else tt[7]
                self._canvas.drawText(pos=(hx1-x-1,0), text=s, color=self._headerColor)
        # Draw header separators
        for sx in self._columnsPos:
            self._canvas.drawChar(pos=(sx-x,0), char=tt[5], color=self._headerColor)
            for sy in range(1,h):
                self._canvas.drawChar(pos=(sx-x,sy), char=tt[4], color=self._lineColor)

        # Draw cache
        for i, c in enumerate(self._cache):
            if i-y<0 : continue
            item  = c.item
            level = c.level
            for il in range(len(self._header)):
                lx = 0 if il==0 else self._columnsPos[il-1]+1
                lx1 = self._columnsPos[il]
                if item.isSelected():
                    self._canvas.drawText(pos=(lx-x,i-y+1), text=c.data[il], width=lx1-lx, alignment=item.textAlignment(il), color=self._selectedColor, forceColor=True)
                else:
                    self._canvas.drawText(pos=(lx-x,i-y+1), text=c.data[il], width=lx1-lx, alignment=item.textAlignment(il))
