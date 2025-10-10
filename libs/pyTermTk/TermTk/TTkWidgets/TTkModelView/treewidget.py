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

from typing import List,Tuple,Optional

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.log import TTkLog
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

class _RootWidgetItem(TTkTreeWidgetItem):
    __slots__ = ('_widgets_buffer','_widgets_buffer_check')

    _widgets_buffer:List[int]
    _widgets_buffer_check:int

    def __init__(self):
        self._widgets_buffer = []
        self._widgets_buffer_check=0
        super().__init__(expanded=True)

    def _getColumnContentSize(self, column:int, offset:int) -> int:
        if offset+0x200 > (_sz:=self.size()):
            offset = _sz-0x200
        if offset < 0x200:
            offset = 0x200
        limited_page = self._get_page_root(offset-0x200,0x400)
        if column==0:
            size = max(max(_l+_i.icon(column).termWidth()+_t.termWidth() for _t in _i.data(column).split('\n')) for _l,_y,_i in limited_page if not _y)
        else:
            size = max(max((_i.icon(column)+_t).termWidth() for _t in _i.data(column).split('\n')) for _l,_y,_i in limited_page if not _y)
        return size-1

    def _get_page_root(self, index:int, size:int) -> List[Tuple[int,int,TTkTreeWidgetItem]]:
        if self._children:
            if self._widgets_buffer_check >= len(self._children._buffer):
                self._widgets_buffer = []
                self._widgets_buffer_check=0
            page = self._children.get_page(0, index, size)
            if any(_wbi[1] != self._children._buffer[_wbi[0]] for _wbi in self._widgets_buffer):
                self._widgets_buffer = []
                self._widgets_buffer_check=0
            if self._widgets_buffer_check < len(self._children._buffer):
                for i,(_l,_y,_i) in enumerate(self._children._buffer[self._widgets_buffer_check:]):
                    if not _y and _i.hasWidgets():
                        self._widgets_buffer.append((_l,i,_i))
                self._widgets_buffer_check = len(self._children._buffer)
            return page
        return []

    def _item_at(self, pos:int) -> Optional[Tuple[int,int,TTkTreeWidgetItem]]:
        if pos < 0 or not self._children:
            return None
        if page := self._children.get_page(0, pos, 1):
            return page[0]
        else:
            return None

    def size(self):
        if self._children:
            return self._children.size()
        return 0

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

    @property
    def itemActivated(self) -> pyTTkSignal:
        '''
        This signal is emitted when the user activates an item by double-clicking
        or pressing a special key (e.g., Enter).

        :param item: the item that was clicked.
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column that was clicked.
        :type col: int
        '''
        return self._itemActivated
    @property
    def itemChanged(self) -> pyTTkSignal:
        '''
        This signal is emitted when the contents of the column in the specified item changes.

        :param item: the item reported by this signal
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column
        :type col: int
        '''
        return self._itemChanged
    @property
    def itemClicked(self) -> pyTTkSignal:
        '''
        This signal is emitted when the user clicks inside the widget.

        If no item was clicked, no signal will be emitted.

        :param item: the item that was clicked.
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column that was clicked.
        :type col: int
        '''
        return self._itemClicked
    @property
    def itemDoubleClicked(self) -> pyTTkSignal:
        '''
        This signal is emitted when the user double clicks inside the widget.

        If no item was double clicked, no signal will be emitted.

        :param item: the item that was clicked.
        :type item: :py:class:`TTkTreeWidgetItem`
        :param col: the item's column that was clicked.
        :type col: int
        '''
        return self._itemDoubleClicked
    @property
    def itemExpanded(self) -> pyTTkSignal:
        '''
        This signal is emitted when the specified item is expanded so that all of its children are displayed.

        :param item: the item reported by this signal
        :type item: :py:class:`TTkTreeWidgetItem`
        '''
        return self._itemExpanded
    @property
    def itemCollapsed(self) -> pyTTkSignal:
        '''
        This signal is emitted when the specified item is collapsed so that none of its children are displayed.

        :param item: the item reported by this signal
        :type item: :py:class:`TTkTreeWidgetItem`
        '''
        return self._itemCollapsed

    classStyle = {
                'default':     {
                    'color': TTkColor.RST,
                    'lineColor': TTkColor.fg("#444444"),
                    'lineHeightColor': TTkColor.fg("#666666"),
                    'headerColor': TTkColor.fg("#ffffff")+TTkColor.bg("#444444")+TTkColor.BOLD,
                    'selectedColor': TTkColor.fg("#ffff88")+TTkColor.bg("#000066")+TTkColor.BOLD,
                    'separatorColor': TTkColor.fg("#444444")},
                'disabled':    {
                    'color': TTkColor.fg("#888888"),
                    'lineColor': TTkColor.fg("#888888"),
                    'lineHeightColor': TTkColor.fg("#666666"),
                    'headerColor': TTkColor.fg("#888888"),
                    'selectedColor': TTkColor.fg("#888888"),
                    'separatorColor': TTkColor.fg("#888888")},
            }

    __slots__ = ( '_rootItem', '_cache',
                  '_header', '_columnsPos',
                  '_selectionMode',
                  '_selectedId', '_selected', '_separatorSelected',
                  '_sortColumn', '_sortOrder', '_sortingEnabled',
                  '_dndMode',
                  # Signals
                  '_itemChanged', '_itemClicked', '_itemDoubleClicked', '_itemExpanded', '_itemCollapsed', '_itemActivated'
                  )

    _selected:List[TTkTreeWidgetItem]
    _rootItem:_RootWidgetItem

    @dataclass(frozen=True)
    class _DropTreeData:
        widget: TTkAbstractScrollView
        items: List[TTkAbstractItemModel]

    def __init__(self, *,
                 header:List[TTkString]=[],
                 sortingEnabled:bool=True,
                 selectionMode:TTkK.SelectionMode=TTkK.SelectionMode.SingleSelection,
                 dragDropMode:TTkK.DragDropMode=TTkK.DragDropMode.NoDragDrop,
                 **kwargs) -> None:
        '''
        :param header: define the header labels of each column, defaults to []
        :type header: List[:py:class:`TTkString`], optional
        :param sortingEnabled: enable the column sorting, defaults to False
        :type sortingEnabled: bool, optional
        :param selectionMode: This property controls whether the user can select one or many items, defaults to :py:class:`TTkK.SelectionMode.SingleSelection`.
        :type selectionMode: :py:class:`TTkK.SelectionMode`, optional
        :param dragDropMode: This property holds the drag and drop event the view will act upon, defaults to :py:class:`TTkK.DragDropMode.NoDragDrop`.
        :type dragDropMode: :py:class:`TTkK.DragDropMode`, optional
        '''
        # Signals
        self._itemActivated     = pyTTkSignal(TTkTreeWidgetItem, int)
        self._itemChanged       = pyTTkSignal(TTkTreeWidgetItem, int)
        self._itemClicked       = pyTTkSignal(TTkTreeWidgetItem, int)
        self._itemDoubleClicked = pyTTkSignal(TTkTreeWidgetItem, int)
        self._itemExpanded      = pyTTkSignal(TTkTreeWidgetItem)
        self._itemCollapsed     = pyTTkSignal(TTkTreeWidgetItem)

        self._cache = []

        self._selectionMode = selectionMode
        self._dndMode = dragDropMode
        self._selected = []
        self._selectedId = None
        self._separatorSelected = None
        self._header = header if header else []
        self._columnsPos = []
        self._sortingEnabled=sortingEnabled
        self._sortColumn = -1
        self._sortOrder = TTkK.AscendingOrder
        self._rootItem = _RootWidgetItem()
        super().__init__(**kwargs)
        self.setMinimumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus)
        self.clear()
        self.setPadding(1,0,0,0)
        self.viewChanged.connect(self._viewChangedHandler)
        self._alignWidgets()
        self.sizeChanged.connect(self._alignWidgets)
        self._rootItem.dataChanged.connect(self._refreshCache)

    @pyTTkSlot()
    def _viewChangedHandler(self) -> None:
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    # Overridden function
    def viewFullAreaSize(self) -> tuple[int, int]:
        w = self._columnsPos[-1]+1 if self._columnsPos else 0
        h = self._rootItem.size()+1
        # TTkLog.debug(f"{w=} {h=}")
        return w,h

    def invisibleRootItem(self) -> TTkTreeWidgetItem:
        '''
        Returns the tree widget's invisible root item.

        The invisible root item provides access to the tree widget's top-level items through the :py:class:`TTkTreeWidgetItem` API,
        making it possible to write functions that can treat top-level items and their children in a uniform way;
        for example, recursive functions.

        :return: the root Item
        :rtype: :py:class:`TTkTreeWidgetItem`
        '''
        return self._rootItem

    def clear(self) -> None:
        '''
        Clears the tree widget by removing all of its items and selections.
        '''
        # Remove all the widgets
        if self._rootItem:
            self._rootItem.dataChanged.disconnect(self._refreshCache)
        self._rootItem = _RootWidgetItem()
        self._rootItem.dataChanged.connect(self._refreshCache)
        self.sortItems(self._sortColumn, self._sortOrder)
        self.viewChanged.emit()
        self.update()

    def addTopLevelItem(self, item:TTkTreeWidgetItem) -> None:
        '''
        Appends the item as a top-level item in the widget.

        :param item: the item to be added.
        :type item: :py:class:`TTkTreeWidgetItem`
        '''
        self._rootItem.addChild(item)
        self.viewChanged.emit()
        self.update()

    def addTopLevelItems(self, items:List[TTkTreeWidgetItem]) -> None:
        '''
        Appends the list of items as a top-level items in the widget.

        :param item: the item to be added.
        :type item: List[:py:class:`TTkTreeWidgetItem`]
        '''
        self._rootItem.addChildren(items)
        self.viewChanged.emit()
        self.update()

    def takeTopLevelItem(self, index:int) -> Optional[TTkTreeWidgetItem]:
        '''
        Removes the top-level item at the given index in the tree and returns it, otherwise returns None;

        :param index: the index of the item
        :type index: int

        :rtype: Optional[:py:class:`TTkTreeWidgetItem`]
        '''
        ret = self._rootItem.takeChild(index)
        self.viewChanged.emit()
        self.update()
        return ret

    def topLevelItem(self, index) -> Optional[TTkTreeWidgetItem]:
        '''
        Returns the top level item at the given index, or None if the item does not exist.

        :param index: the index of the item
        :type index: int

        :rtype: Optional[:py:class:`TTkTreeWidgetItem`]
        '''
        return self._rootItem.child(index)

    def indexOfTopLevelItem(self, item:TTkTreeWidgetItem) -> int:
        '''
        Returns the index of the given top-level item, or -1 if the item cannot be found.

        :rtype: int
        '''
        return self._rootItem.indexOfChild(item)

    def selectionMode(self) -> TTkK.SelectionMode:
        '''
        selectionMode

        :rtype: :py:class:`TTkK.SelectionMode`
        '''
        return self._selectionMode

    def setSelectionMode(self, mode:TTkK.SelectionMode) -> None:
        '''
        Sets the current selection model to the given selectionModel.

        :param mode: the selection mode used in this tree
        :type mode: :py:class:`TTkK.SelectionMode`
        '''
        self._selectionMode = mode

    def selectedItems(self) -> List[TTkTreeWidgetItem]:
        '''
        Returns a list of all selected non-hidden items.

        :rtype: List[:py:class:`TTkTreeWidgetItem`]
        '''
        if self._selected:
            return self._selected
        return None

    def setHeaderLabels(self, labels:List[TTkString]) -> None:
        '''
        Adds a column in the header for each item in the labels list, and sets the label for each column.

        :param labels: the list of labels
        :type labels: List[:py:class:`TTkString`]
        '''
        self._header = labels
        # Set 20 as default column size
        self._columnsPos = [20+x*20 for x in range(len(labels))]
        self.viewChanged.emit()
        self.update()

    def dragDropMode(self) -> TTkK.DragDropMode:
        '''dragDropMode'''
        return self._dndMode

    def setDragDropMode(self, dndMode:TTkK.DragDropMode):
        '''setDragDropMode'''
        self._dndMode = dndMode

    def isSortingEnabled(self) -> bool:
        '''
        This property holds whether sorting is enabled

        If this property is true, sorting is enabled for the tree;
        if the property is false, sorting is not enabled.
        The default value is false.

        :rtype: bool
        '''
        return self._sortingEnabled

    def setSortingEnabled(self, enabled:bool) -> None:
        '''
        This property holds whether sorting is enabled

        If this property is true, sorting is enabled for the tree;
        if the property is false, sorting is not enabled.
        The default value is false.

        :param enabled: the sorting status
        :type enabled: bool
        '''
        if enabled != self._sortingEnabled:
            self._sortingEnabled = enabled
            self.update()

    def sortColumn(self) -> int:
        '''
        Returns the column used to sort the contents of the widget.
        -1 in case no column sort is used

        :rtype: int
        '''
        return self._sortColumn

    def sortItems(self, col:int, order:TTkK.SortOrder) -> None:
        '''
        Sorts the items in the widget in the specified order by the values in the given column.

        :param col: the column used as reference for the sorting
        :type col: int
        :param order: the sorting order
        :type order: :py:class:`TTkK.SortOrder`
        '''
        if not self._sortingEnabled: return
        self._sortColumn = col
        self._sortOrder = order
        self._rootItem.dataChanged.disconnect(self._refreshCache)
        self._rootItem.sortChildren(col, order)
        self._rootItem.dataChanged.connect(self._refreshCache)
        self._refreshCache()

    def columnWidth(self, column:int) -> int:
        '''
        This property hold the width of the column requested

        :param column: the column position
        :type column: int

        :rtype: int
        '''
        if column==0:
            return self._columnsPos[column]
        else:
            return self._columnsPos[column]-self._columnsPos[column-1]-1

    def setColumnWidth(self, column:int, width: int) -> None:
        '''
        Set the width of the column requested

        :param column: the column position
        :type column: int

        :rtype: int
        '''
        i = column
        newSize = ((1+self._columnsPos[i-1]) if i>0 else 0) + width
        oldSize = self._columnsPos[i]
        for ii in range(i,len(self._columnsPos)):
            self._columnsPos[ii] += newSize-oldSize+1
        self._alignWidgets()
        self.viewChanged.emit()
        self.update()

    def resizeColumnToContents(self, column:int) -> None:
        '''
        rwsize the width of the column requestedto its content

        :param column: the column position
        :type column: int
        '''
        _,oy = self.getViewOffsets()
        contentSize = self._rootItem._getColumnContentSize(column, oy)
        self.setColumnWidth(column, contentSize)

    @pyTTkSlot()
    def expandAll(self) -> None:
        '''Expands all expandable items.'''
        if not self._rootItem:
            return
        self._rootItem.dataChanged.disconnect(self._refreshCache)
        self._rootItem.expandAll()
        self._rootItem.dataChanged.connect(self._refreshCache)
        self._refreshCache()

    @pyTTkSlot()
    def collapseAll(self) -> None:
        '''Collapse all collapsable items.'''
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
        if  _item_at := self._rootItem._item_at(y):
            _,_,_i = _item_at
            item  = _i
            if item.childIndicatorPolicy() == TTkK.DontShowIndicatorWhenChildless and item.children() or \
               item.childIndicatorPolicy() == TTkK.ShowIndicator:
                item.setExpanded(not item.isExpanded())
                if item.isExpanded():
                    self.itemExpanded.emit(item)
                else:
                    self.itemCollapsed.emit(item)
            for _s in self._selected:
                _s.setSelected(False)
            self._selectedId = y
            self._selected = [item]
            item.setSelected(True)
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
        if  _item_at := self._rootItem._item_at(y):
            _l, _yi, _i = _item_at
            item  = _i
            level = _l
            # check if the expand button is pressed with +-1 tollerance
            if ( _yi==0 and level*2 <= x < level*2+3 and \
                 ( item.childIndicatorPolicy() == TTkK.DontShowIndicatorWhenChildless and item.children() or
                   item.childIndicatorPolicy() == TTkK.ShowIndicator )):
                item.setExpanded(not item.isExpanded())
                if item.isExpanded():
                    self.itemExpanded.emit(item)
                else:
                    self.itemCollapsed.emit(item)
            else:
                if self._selectionMode in (TTkK.SelectionMode.SingleSelection,TTkK.SelectionMode.MultiSelection):
                    _multiSelect = self._selectionMode == TTkK.SelectionMode.MultiSelection
                    if not ( bool(evt.mod & TTkK.ControlModifier) and _multiSelect ):
                        for _s in self._selected:
                            _s.setSelected(False)
                        self._selected.clear()
                    self._selectedId = y
                    # Unselect Items if already selected in multiselect mode
                    if item in self._selected and _multiSelect:
                        self._selected.remove(item)
                        item.setSelected(False)
                    else:
                        self._selected.append(item)
                        item.setSelected(True)
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
            data = TTkTreeWidget._DropTreeData(widget=self,items=self._selected)
            text = [(_n.substring(to=27)+'...') if (_n:=_s.data(0)).termWidth()>30 else _n for _s in self._selected[:4]]
            dh = len(text) + 2
            dw = max(_t.termWidth() for _t in text[:3])+2
            pm = TTkCanvas(width=dw,height=dh)
            for _y,_t in enumerate(text[:3],1):
                pm.drawTTkString(pos=(1,_y),text=_t)
            if len(self._selected) > 3:
                pm.drawText(pos=(1,4),text='...')
            pm.drawBox(pos=(0,0),size=(dw,dh))
            drag.setPixmap(pm)
            drag.setData(data)
            drag.exec()
            return True
        return False

    @pyTTkSlot()
    def _alignWidgets(self) -> None:
        self.layout().clear()

        ox, oy = self.getViewOffsets()
        w,h = self.size()
        self._rootItem._get_page_root(0,oy+h)

        if not self._rootItem._widgets_buffer:
            self.update()
            return

        wids = []
        for _l,_y,_i in self._rootItem._widgets_buffer:
            for _il in range(len(self._header)):
                if _wid:=_i.widget(_il):
                    _pos   = self._columnsPos[_il-1]+1 if _il else 3 + _l*2
                    _width = self._columnsPos[_il] - _pos
                    _height = _wid.height()
                    _wid.setGeometry(_pos,_y,_width,_height)
                    _wid.show()
                    wids.append(_wid)
        if wids:
            self.layout().addWidgets(wids)

    @pyTTkSlot()
    def _refreshCache(self) -> None:
        self._alignWidgets()
        self.update()
        self.viewChanged.emit()
        return

    def paintEvent(self, canvas) -> None:
        style = self.currentStyle()

        color= style['color']
        lineColor= style['lineColor']
        lineHeightColor= style['lineHeightColor']
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

        col_slices = list(zip([0]+[_p+1 for _p in self._columnsPos], self._columnsPos))
        for _y, (_l, _yi, _i) in enumerate(self._rootItem._get_page_root(y,h)):
            for il in range(len(self._header)):
                _lx,_lx1 = col_slices[il]
                _width = _lx1-_lx
                _ih = _i.height()
                _data = _i.data(il).split('\n') + [TTkString()]*_ih
                if il==0: # First Column
                    if _yi == 0:
                        _icon = f"{'  '*_l}"+_i.icon(il)
                    elif _yi == _ih-1:
                        _icon = TTkString(f"{'  '*_l} ╽ ", lineHeightColor)
                    elif _yi == 1:
                        _icon = TTkString(f"{'  '*_l} ┊ ", lineHeightColor)
                    else:
                        _icon = TTkString(f"{'  '*_l} │ ", lineHeightColor)
                    _text=_icon+_data[_yi]
                else: # Other columns
                    _text=_data[_yi]
                if _i.isSelected():
                    _text = (_text + ' '*_width).completeColor(selectedColor)
                canvas.drawTTkString(text=_text,pos=(_lx-x,_y+1),width=_width)
