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

__all__ = ['TTkTreeWidget']

from typing import List

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkGui.drag import TTkDrag, TTkDnDEvent

from TermTk.TTkWidgets.TTkModelView.treewidgetitem import TTkTreeWidgetItem
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView
from TermTk.TTkAbstract.abstractitemmodel import TTkAbstractItemModel
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot

from dataclasses import dataclass

class TTkTreeWidget(TTkAbstractScrollView):
    '''
    The :py:class:`TTkTreeWidget` class is a convenience class that provides a standard tree
    widget with a classic item-based interface.

    This class is based on TTk's Model/View architecture and uses a default model to hold items,
    each of which is a :py:class:`TTkTreeWidgetItem`.

    In its simplest form, a tree widget can be constructed in the following way:

    .. code-block:: python

        import TermTk as ttk

        root = ttk.TTk()

        tree = ttk.TTkTree(parent=root,size=(80,24))
        tree.setHeaderLabels(["Column 1", "Column 2", "Column 3"])

        top = ttk.TTkTreeWidgetItem(["String A", "String B", "String C"])

        tree.addTopLevelItem(top)

        for i in range(5):
            child = ttk.TTkTreeWidgetItem(["Child A" + str(i), "Child B" + str(i), "Child C" + str(i)])
            top.addChild(child)

        root.mainloop()

    Before items can be added to the tree widget,
    the number of columns must be set with :meth:`setHeaderLabels`.
    This allows each item to have one label.

    The tree can have a header that contains a section for each column in the widget.
    It is easiest to set up the labels for each section by supplying a list of strings with :meth:`setHeaderLabels`.

    The items in the tree can be sorted by column according to a predefined sort order.
    If sorting is enabled, the user can sort the items by clicking on a column header.
    Sorting can be enabled or disabled by calling setSortingEnabled().
    The isSortingEnabled() function indicates whether sorting is enabled.
    '''

    itemActivated:pyTTkSignal
    '''
    This signal is emitted when the user activates an item by double-clicking
    or pressing a special key (e.g., Enter).

    :param item: the item that was clicked.
    :type item: :py:class:`TTkTreeWidgetItem`
    :param col: the item's column that was clicked.
    :type col: int
    '''
    itemChanged:pyTTkSignal
    '''
    This signal is emitted when the contents of the column in the specified item changes.

    :param item: the item reported by this signal
    :type item: :py:class:`TTkTreeWidgetItem`
    :param col: the item's column
    :type col: int
    '''
    itemClicked:pyTTkSignal
    '''
    This signal is emitted when the user clicks inside the widget.

    If no item was clicked, no signal will be emitted.

    :param item: the item that was clicked.
    :type item: :py:class:`TTkTreeWidgetItem`
    :param col: the item's column that was clicked.
    :type col: int
    '''
    itemDoubleClicked:pyTTkSignal
    '''
    This signal is emitted when the user double clicks inside the widget.

    If no item was double clicked, no signal will be emitted.

    :param item: the item that was clicked.
    :type item: :py:class:`TTkTreeWidgetItem`
    :param col: the item's column that was clicked.
    :type col: int
    '''
    itemExpanded:pyTTkSignal
    '''
    This signal is emitted when the specified item is expanded so that all of its children are displayed.

    :param item: the item reported by this signal
    :type item: :py:class:`TTkTreeWidgetItem`
    '''
    itemCollapsed:pyTTkSignal
    '''
    This signal is emitted when the specified item is collapsed so that none of its children are displayed.

    :param item: the item reported by this signal
    :type item: :py:class:`TTkTreeWidgetItem`
    '''

    classStyle = {
                'default':     {
                    'color': TTkColor.RST,
                    'lineColor': TTkColor.fg("#444444"),
                    'headerColor': TTkColor.fg("#ffffff")+TTkColor.bg("#444444")+TTkColor.BOLD,
                    'selectedColor': TTkColor.fg("#ffff88")+TTkColor.bg("#000066")+TTkColor.BOLD,
                    'separatorColor': TTkColor.fg("#444444")},
                'disabled':    {
                    'color': TTkColor.fg("#888888"),
                    'lineColor': TTkColor.fg("#888888"),
                    'headerColor': TTkColor.fg("#888888"),
                    'selectedColor': TTkColor.fg("#888888"),
                    'separatorColor': TTkColor.fg("#888888")},
            }

    __slots__ = ( '_rootItem', '_cache',
                  '_header', '_columnsPos',
                  '_selectedId', '_selected', '_separatorSelected',
                  '_sortColumn', '_sortOrder', '_sortingEnabled',
                  '_dndMode',
                  # Signals
                  'itemChanged', 'itemClicked', 'itemDoubleClicked', 'itemExpanded', 'itemCollapsed', 'itemActivated'
                  )
    @dataclass(frozen=True)
    class _Cache:
        item: TTkTreeWidgetItem
        level: int
        data: list
        widgets: list
        firstLine: bool

    @dataclass(frozen=True)
    class _DropTreeData:
        widget: TTkAbstractScrollView
        items: List[TTkAbstractItemModel]

    def __init__(self, *,
                 header=None,
                 sortingEnabled=True,
                 dragDropMode:TTkK.DragDropMode=TTkK.DragDropMode.NoDragDrop,
                 **kwargs) -> None:
        '''
        :param header: define the header labels of each column, defaults to []
        :type header: list[TTkString], optional
        :param sortingEnabled: enable the column sorting, defaults to False
        :type sortingEnabled: bool, optional
        :param dragDropMode: This property holds the drag and drop event the view will act upon, defaults to :py:class:`TTkK.DragDropMode.NoDragDrop`.
        :type dragDropMode: :py:class:`TTkK.DragDropMode`, optional
        '''
        # Signals
        self.itemActivated     = pyTTkSignal(TTkTreeWidgetItem, int)
        self.itemChanged       = pyTTkSignal(TTkTreeWidgetItem, int)
        self.itemClicked       = pyTTkSignal(TTkTreeWidgetItem, int)
        self.itemDoubleClicked = pyTTkSignal(TTkTreeWidgetItem, int)
        self.itemExpanded      = pyTTkSignal(TTkTreeWidgetItem)
        self.itemCollapsed     = pyTTkSignal(TTkTreeWidgetItem)

        self._dndMode = dragDropMode
        self._selected = None
        self._selectedId = None
        self._separatorSelected = None
        self._header = header if header else []
        self._columnsPos = []
        self._cache = []
        self._sortingEnabled=sortingEnabled
        self._sortColumn = -1
        self._sortOrder = TTkK.AscendingOrder
        self._rootItem = TTkTreeWidgetItem(expanded=True)
        super().__init__(**kwargs)
        self.setMinimumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus)
        self.clear()
        self.setPadding(1,0,0,0)
        self.viewChanged.connect(self._viewChangedHandler)

    @pyTTkSlot()
    def _viewChangedHandler(self) -> None:
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    # Overridden function
    def viewFullAreaSize(self) -> tuple[int, int]:
        w = self._columnsPos[-1]+1 if self._columnsPos else 0
        h = self._rootItem.size()
        # TTkLog.debug(f"{w=} {h=}")
        return w,h

    def clear(self) -> None:
        '''clear'''
        # Remove all the widgets
        for ri in self._rootItem.children():
            ri.setTreeItemParent(None)
        if self._rootItem:
            self._rootItem.dataChanged.disconnect(self._refreshCache)
        self._rootItem = TTkTreeWidgetItem(expanded=True)
        self._rootItem.dataChanged.connect(self._refreshCache)
        self.sortItems(self._sortColumn, self._sortOrder)
        self._refreshCache()
        self.viewChanged.emit()
        self.update()

    def addTopLevelItem(self, item:TTkTreeWidgetItem) -> None:
        '''addTopLevelItem'''
        self._rootItem.addChild(item)
        item.setTreeItemParent(self)
        self._refreshCache()
        self.viewChanged.emit()
        self.update()

    def addTopLevelItems(self, items:TTkTreeWidgetItem) -> None:
        '''addTopLevelItems'''
        self._rootItem.addChildren(items)
        self._rootItem.setTreeItemParent(self)
        #for item in items:
        #    item.setTreeItemParent(self)
        self._refreshCache()
        self.viewChanged.emit()
        self.update()

    def takeTopLevelItem(self, index) -> None:
        '''takeTopLevelItem'''
        self._rootItem.takeChild(index)
        self._refreshCache()
        self.viewChanged.emit()
        self.update()

    def topLevelItem(self, index) -> TTkTreeWidgetItem:
        '''topLevelItem'''
        return self._rootItem.child(index)

    def indexOfTopLevelItem(self, item:TTkTreeWidgetItem) -> int:
        '''indexOfTopLevelItem'''
        return self._rootItem.indexOfChild(item)

    def selectedItems(self) -> list[TTkTreeWidgetItem]:
        '''selectedItems'''
        if self._selected:
            return [self._selected]
        return None

    def setHeaderLabels(self, labels:TTkString) -> None:
        '''setHeaderLabels'''
        self._header = labels
        # Set 20 as default column size
        self._columnsPos = [20+x*20 for x in range(len(labels))]
        self.viewChanged.emit()
        self.update()

    def dragDropMode(self):
        '''dragDropMode'''
        return self._dndMode

    def setDragDropMode(self, dndMode):
        '''setDragDropMode'''
        self._dndMode = dndMode

    def isSortingEnabled(self) -> bool:
        'isSortingEnabled'
        return self._sortingEnabled

    def setSortingEnabled(self, enabled) -> None:
        'setSortingEnabled'
        if enabled != self._sortingEnabled:
            self._sortingEnabled = enabled
            self.update()

    def sortColumn(self):
        '''Returns the column used to sort the contents of the widget.'''
        return self._sortColumn

    def sortItems(self, col:int, order:TTkK.SortOrder) -> None:
        '''Sorts the items in the widget in the specified order by the values in the given column.'''
        if not self._sortingEnabled: return
        self._sortColumn = col
        self._sortOrder = order
        self._rootItem.sortChildren(col, order)

    def columnWidth(self, column:int) -> int:
        '''columnWidth'''
        if column==0:
            return self._columnsPos[column]
        else:
            return self._columnsPos[column]-self._columnsPos[column-1]-1

    def setColumnWidth(self, column:int, width: int) -> None:
        '''setColumnWidth'''
        i = column
        newSize = ((1+self._columnsPos[i-1]) if i>0 else 0) + width
        oldSize = self._columnsPos[i]
        for ii in range(i,len(self._columnsPos)):
            self._columnsPos[ii] += newSize-oldSize+1
        self._alignWidgets()
        self.viewChanged.emit()
        self.update()

    def resizeColumnToContents(self, column:int) -> None:
        '''resizeColumnToContents'''
        contentSize = max(row.data[column].termWidth() for row in self._cache)
        self.setColumnWidth(column, contentSize)

    @pyTTkSlot()
    def expandAll(self) -> None:
        '''expandAll'''
        if not self._rootItem:
            return
        self._rootItem.dataChanged.disconnect(self._refreshCache)
        self._rootItem.expandAll()
        self._rootItem.dataChanged.connect(self._refreshCache)
        self._refreshCache()

    @pyTTkSlot()
    def collapseAll(self) -> None:
        '''collapseAll'''
        if not self._rootItem:
            return
        self._rootItem.dataChanged.disconnect(self._refreshCache)
        self._rootItem.collapseAll()
        self._rootItem.dataChanged.connect(self._refreshCache)
        self._refreshCache()

    def mouseDoubleClickEvent(self, evt:TTkMouseEvent) -> bool:
        x,y = evt.x, evt.y
        ox, oy = self.getViewOffsets()
        x += ox

        # Handle Header Events
        # Doubleclick resize to the content size
        if y == 0:
            for i, c in enumerate(self._columnsPos):
                if x == c:
                    self.resizeColumnToContents(i)
                    break
            return True

        y += oy-1
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

    def focusOutEvent(self) -> None:
        self._separatorSelected = None

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        x,y = evt.x, evt.y
        ox, oy = self.getViewOffsets()
        x += ox
        self._separatorSelected = None

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
            # check if the expand button is pressed with +-1 tollerance
            if level*2 <= x < level*2+3 and \
               ( item.childIndicatorPolicy() == TTkK.DontShowIndicatorWhenChildless and item.children() or
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

    def mouseDragEvent(self, evt:TTkMouseEvent) -> bool:
        #    columnPos       (Selected = 2)
        #        0       1        2          3   4
        #    ----|-------|--------|----------|---|
        #    Mouse (Drag) Pos
        #                            ^
        #    I consider at least 4 char (3+1) as spacing
        #    Min Selected Pos = (Selected+1) * 4
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
            self._alignWidgets()
            self.viewChanged.emit()
            self.update()
            return True
        elif ( self._dndMode & TTkK.DragDropMode.AllowDrag and
               evt.key == TTkMouseEvent.LeftButton and self._selected ):
            drag = TTkDrag()
            data = TTkTreeWidget._DropTreeData(widget=self,items=[self._selected])
            text = self._selected.data(0)
            if text.termWidth() > 30:
                text = '['+text.substring(to=27)+'...]'
            else:
                text = '['+text+']'
            pm = TTkCanvas(text.termWidth()+2,1)
            pm.drawTTkString(pos=(0,0),text=text)
            drag.setPixmap(pm)
            drag.setData(data)
            drag.exec()
            return True
        return False

    def _alignWidgets(self) -> None:
        for y,c in enumerate(self._cache):
            if not c.firstLine:
                continue
            for i,w in enumerate(c.widgets):
                if w:
                    _pos   = self._columnsPos[i-1]+1 if i else 3 + c.level*2
                    _width = self._columnsPos[i] - _pos
                    _height = w.height()
                    w.setGeometry(_pos,y,_width,_height)
                    w.show()

    @pyTTkSlot()
    def _refreshCache(self) -> None:
        # I save a representation of the displayed tree in a cache array
        # to avoid eccessve recursion over the items and
        # identify quickly the nth displayed line to improve the interaction
        #
        # _cache is an array of TTkTreeWidget._Cache:
        # [ item, level, data=[txtCol1, txtCol2, txtCol3, ... ]]
        self._cache = []
        def _addToCache(_child, _level:int) -> None:
            _data = []
            _widgets = []
            _h =_child.height()
            for _il in range(len(self._header)):
                _lines = _child.data(_il).split('\n')
                if _il==0:
                    _data0 = []
                    for _id in range(_h):
                        # Trying to define an icon to obtain this results on multiline field
                        #  ▶ Label
                        #  ┊ NewLine 1
                        #  │ NewLine 2
                        #  ╽
                        if _id == 0:
                            _icon = " "+_child.icon(_il)+" "
                        elif _id == _h-1:
                            _icon = TTkString(" ╽ ", TTkColor.fg("#666666"))
                        elif _id == 1:
                            _icon = TTkString(" ┊ ", TTkColor.fg("#666666"))
                        else:
                            _icon = TTkString(" │ ", TTkColor.fg("#666666"))
                        _text = _lines[_id] if _id<len(_lines) else ""
                        _data0.append('  '*_level+_icon+_text)
                    _data.append(_data0)
                    _widgets.append(_child.widget(_il))
                else:
                    _data.append([TTkString(s) for s in _lines]+[TTkString()]*(_h-len(_lines)))
                    _widgets.append(_child.widget(_il))

            for _id in range(_h):
                self._cache.append(TTkTreeWidget._Cache(
                                        item  = _child,
                                        level = _level,
                                        data  = [ dt[_id] for dt in _data],
                                        widgets = _widgets,
                                        firstLine=_id==0))
            if _child.isExpanded():
                for _c in _child.children():
                   _addToCache(_c, _level+1)
        for c in self._rootItem.children():
            _addToCache(c,0)
        self._alignWidgets()
        self.update()
        self.viewChanged.emit()

    def paintEvent(self, canvas) -> None:
        style = self.currentStyle()

        color= style['color']
        lineColor= style['lineColor']
        headerColor= style['headerColor']
        selectedColor= style['selectedColor']
        separatorColor= style['separatorColor']

        x,y = self.getViewOffsets()
        w,h = self.size()
        tt = TTkCfg.theme.tree

        # Draw header first:
        for i,l in enumerate(self._header):
            hx  = 0 if i==0 else self._columnsPos[i-1]+1
            hx1 = self._columnsPos[i]
            canvas.drawText(pos=(hx-x,0), text=l, width=hx1-hx, color=headerColor)
            if self._sortingEnabled and i == self._sortColumn:
                s = tt[6] if self._sortOrder == TTkK.AscendingOrder else tt[7]
                canvas.drawText(pos=(hx1-x-1,0), text=s, color=headerColor)
        # Draw header separators
        for sx in self._columnsPos:
            canvas.drawChar(pos=(sx-x,0), char=tt[5], color=headerColor)
            for sy in range(1,h):
                canvas.drawChar(pos=(sx-x,sy), char=tt[4], color=lineColor)

        # Draw cache
        for i, c in enumerate(self._cache):
            if i-y<0: continue
            item  = c.item
            for il in range(len(self._header)):
                lx = 0 if il==0 else self._columnsPos[il-1]+1
                lx1 = self._columnsPos[il]

                text = c.data[il]
                if item.isSelected():
                    canvas.drawText(pos=(lx-x,i-y+1), text=text.completeColor(selectedColor), width=lx1-lx, alignment=item.textAlignment(il), color=selectedColor)
                else:
                    canvas.drawText(pos=(lx-x,i-y+1), text=text, width=lx1-lx, alignment=item.textAlignment(il))
