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
from TermTk.TTkCore.signal import pyTTkSlot

from dataclasses import dataclass

class TTkTreeWidget(TTkAbstractScrollView):
    __slots__ = ( '_items', '_header', '_columnsPos', '_cache',
                  '_selectedId', '_selected', '_separatorSelected', '_mouseDelta',
                  '_headerColor', '_selectedColor')
    @dataclass(frozen=True)
    class _Cache:
        item: TTkTreeWidgetItem
        level: int
        data: list

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTreeView' )
        self._selected = None
        self._selectedId = None
        self._separatorSelected = None
        self._items = []
        self._header = kwargs.get('header',[])
        self._columnsPos = []
        self._cache = []
        self._headerColor   = kwargs.get('headerColor',TTkCfg.theme.treeHeaderColor)
        self._selectedColor = kwargs.get('selectedColor',TTkCfg.theme.treeSelectedColor)
        self.setMinimumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus)

    # Overridden function
    def viewFullAreaSize(self) -> (int, int):
        w = self._columnsPos[-1] if self._columnsPos else 0
        h = 1+sum([c.size() for c in self._items])
        # TTkLog.debug(f"{w=} {h=}")
        return w,h

    # Overridden function
    def viewDisplayedSize(self) -> (int, int):
        # TTkLog.debug(f"{self.size()=}")
        return self.size()

    def addTopLevelItem(self, item):
        item.dataChanged.connect(self._refreshCache)
        self._items.append(item)
        self._refreshCache()
        self.viewChanged.emit()
        self.update()

    def setHeaderLabels(self, labels):
        self._header = labels
        # Set 20 as default column size
        self._columnsPos = [20+x*20 for x in range(len(labels))]
        self.viewChanged.emit()
        self.update()

    def mouseDoubleClickEvent(self, evt):
        _,y = evt.x, evt.y
        _, oy = self.getViewOffsets()
        y -= 1-oy
        if 0 <= y < len(self._cache):
            item  = self._cache[y].item
            item.setExpanded(not item.isExpanded())
            if self._selected:
                self._selected.setSelected(False)
            self._selectedId = y
            self._selected = item
            self._selected.setSelected(True)

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
                    self._separatorSelected = i
                    self.update()
            return True
        # Handle Tree/Table Events
        y += oy-1
        if 0 <= y < len(self._cache):
            item  = self._cache[y].item
            level = self._cache[y].level
            if level*2 <= x < level*2+3:
                item.setExpanded(not item.isExpanded())
            else:
                if self._selected:
                    self._selected.setSelected(False)
                self._selectedId = y
                self._selected = item
                self._selected.setSelected(True)
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
            self._columnsPos[ss] = pos
            # Align the previous Separators if pushed
            for i in range(ss):
                self._columnsPos[i] = min(self._columnsPos[i], pos-(ss-i)*4)
            # Align the next Separators if pushed
            for i in range(ss, len(self._columnsPos)):
                self._columnsPos[i] = max(self._columnsPos[i], pos+(i-ss)*4)
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
            tt = TTkCfg.theme.tree
            _data = []
            for _il in range(len(self._header)):
                _data.append(_child.data(_il))
            if not _child.children():
                _data[0] = f"{'  '*_level} {tt[0]} {_data[0]}"
            elif _child.isExpanded():
                _data[0] = f"{'  '*_level} {tt[2]} {_data[0]}"
            else:
                _data[0] = f"{'  '*_level} {tt[1]} {_data[0]}"
            self._cache.append(TTkTreeWidget._Cache(
                                item  = _child,
                                level = _level,
                                data  = _data))
            if _child.isExpanded():
                for _c in _child.children():
                   _addToCache(_c, _level+1)
        for c in self._items:
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
        # Draw header separators
        for sx in self._columnsPos:
            self._canvas.drawChar(pos=(sx-x,0), char=tt[5], color=self._headerColor)
            for sy in range(1,h):
                self._canvas.drawChar(pos=(sx-x,sy), char=tt[4])

        # Draw cache
        for i, c in enumerate(self._cache):
            if i-y<0 : continue
            item  = c.item
            level = c.level
            color = self._selectedColor if item.isSelected() else TTkColor.RST
            for il in range(len(self._header)):
                lx = 0 if il==0 else self._columnsPos[il-1]+1
                lx1 = self._columnsPos[il]
                self._canvas.drawText(pos=(lx-x,i-y+1), text=c.data[il], width=lx1-lx, color=color)
