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

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollView
from TermTk.TTkCore.signal import pyTTkSlot

class TTkTreeWidget(TTkAbstractScrollView):
    __slots__ = ( '_items', '_header', '_columnsPos', '_cache', '_selected')

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTreeView' )
        self._selected = -1
        self._items = []
        self._header = kwargs.get('header',[])
        self._columnsPos = []
        self._cache = []
        self.setMinimumHeight(1)

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
            item  = self._cache[y][0]
            item.setExpanded(not item.isExpanded())
            self._selected = y
            self.update()
        return True

    def mousePressEvent(self, evt):
        x,y = evt.x, evt.y
        ox, oy = self.getViewOffsets()
        y += oy-1
        x += ox
        if 0 <= y < len(self._cache):
            item  = self._cache[y][0]
            level = self._cache[y][1]
            if level*2 <= x < level*2+3:
                item.setExpanded(not item.isExpanded())
            else:
                self._selected = y
            self.update()
        return True

    @pyTTkSlot()
    def _refreshCache(self):
        ''' I save a representation fo the displayed tree in a cache array
            to avoid eccessve recursion over the items and
            identify quickly the nth displayed line to improve the interaction

            _cache is an array of:
            [ item, level, txtCol1, txtCol2, txtCol3, ... ]
        '''
        self._cache = []
        def _addToCache(_child, _level):
            _entry = [_child, _level]
            for _il in range(len(self._header)):
                _entry.append(_child.data(_il))
            self._cache.append(_entry)
            if _child.isExpanded():
                for _c in _child.children():
                   _addToCache(_c, _level+1)
        for c in self._items:
            _addToCache(c,0)
        self.update()

    def paintEvent(self):
        x,y = self.getViewOffsets()
        w,h = self.size()

        # Draw header first:
        for i,l in enumerate(self._header):
            hx = 0 if i==0 else self._columnsPos[i-1]+1
            self._canvas.drawText(pos=(hx-x,0), text=l)
        # Draw header separators
        for sx in self._columnsPos:
            self._canvas.drawText(pos=(sx-x,0), text='|')

        # Draw cache
        for i, l in enumerate(self._cache):
            if i-y<0 : continue
            item  = l[0]
            level = l[1]
            l1    = l[2]
            if not item.children():
                l1 = '  '*level + " • " + l1
            elif item.isExpanded():
                l1 = '  '*level + " ▼ " + l1
            else:
                l1 = '  '*level + " ▶ " + l1

            self._canvas.drawText(pos=(-x,i-y+1), text=l1)
            for il in range(1,len(self._header)):
                lx = self._columnsPos[il-1]+1
                self._canvas.drawText(pos=(lx-x,i-y+1), text=l[2+il])





