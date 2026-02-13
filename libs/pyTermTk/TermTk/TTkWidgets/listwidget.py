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

from __future__ import annotations

__all__ = ['TTkAbstractListItem', 'TTkListWidget', 'TTkAbstractListItemType']

from dataclasses import dataclass
from typing import Optional, List, Any, Tuple

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkGui.drag import TTkDrag, TTkDnDEvent

from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView
from TermTk.TTkAbstract.abstract_list_item import _TTkAbstractListItem
from TermTk.TTkWidgets.listwidget_item import TTkListItem, TTkAbstractListItemType, TTkAbstractListItem

class TTkListWidget(TTkAbstractScrollView):
    '''TTkListWidget:

    A widget that displays a scrollable list of selectable items with optional search functionality.

    This widget supports single/multiple selection modes, drag-and-drop reordering,
    keyboard navigation, and incremental search. Items can be strings or custom
    :py:class:`TTkAbstractListItem` widgets.

    ::

        ╔════════════════════════════════╗
        ║Search: te_                    ▲║ ← Search bar (optional)
        ║S-0) --Zero-3- officia         ▓║
        ║S-1) ad ipsum                  ┊║
        ║S-2) irure nisi                ┊║ ← Scrollable items
        ║S-3) minim --Zero-3-           ┊║
        ║S-4) ea sunt                   ┊║
        ║S-5) qui mollit                ┊║
        ║S-6) magna sunt                ┊║
        ║S-7) sunt officia              ▼║
        ╚════════════════════════════════╝

    Demo: `list.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/list.py>`_
    (`online <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/sandbox.html?filePath=demo/showcase/list.py>`__)

    .. code-block:: python

        import TermTk as ttk

        root = ttk.TTk(layout=ttk.TTkGridLayout(), mouseTrack=True)

        # Simple string list
        l1 = ttk.TTkList(parent=root, items=[123, 456, 789])
        id1 = l1.indexOf(456)
        l1.setCurrentRow(id1)

        # List with many items (scrollable)
        ttk.TTkList(parent=root, items=[f"Item 0x{i:03X}" for i in range(100)])

        # Multi-selection list with drag-drop
        ttkList = ttk.TTkList(
            parent=root,
            selectionMode=ttk.TTkK.SelectionMode.MultiSelection,
            dragDropMode=ttk.TTkK.DragDropMode.AllowDragDrop
        )
        ttkList.addItems([f"Item 0x{i:04X}" for i in range(50)])

        root.layout().addWidget(ttk.TTkLogViewer(),1,0,1,3)

        # Handle selection
        @ttk.pyTTkSlot(str)
        def on_item_clicked(text):
            ttk.TTkLog.debug(f"Clicked: {text}")

        ttkList.textClicked.connect(on_item_clicked)

        root.mainloop()

    **Features:**

    - Single or multiple selection modes
    - Keyboard navigation (arrows, page up/down, home/end)
    - Incremental search by typing
    - Drag-and-drop reordering (optional)
    - Custom item widgets via :py:class:`TTkAbstractListItem`
    - Signals for item selection and search events
    '''

    classStyle = {
        'default': {
            'color':       TTkColor.RST,
            'highlighted': TTkColor.bg("#004433"),
            'hovered':     TTkColor.bg('#0088FF'),
            'selected':    TTkColor.bg('#0055FF'),
            'clicked':     TTkColor.fg('#FFFF00'),
            'disabled':    TTkColor.fg('#888888'),
            'searchColor': TTkColor.fg("#FFFF00")+TTkColor.UNDERLINE,
        }
    }

    @property
    def itemClicked(self) -> pyTTkSignal:
        '''
        This signal is emitted whenever an item is clicked.

        :param item: the item selected
        :type item: :py:class:`TTkAbstractListItem`
        '''
        return self._itemClicked

    @property
    def textClicked(self) -> pyTTkSignal:
        '''
        This signal is emitted whenever an item is clicked.

        :param text: the text of the item selected
        :type text: str
        '''
        return self._textClicked

    @property
    def searchModified(self) -> pyTTkSignal:
        '''
        This signal is emitted whenever the search text is modified.

        :param text: the search text
        :type text: str
        '''
        return self._searchModified

    @dataclass(frozen=True)
    class _DropListData:
        widget: TTkListWidget
        items: List[TTkAbstractListItem]

    __slots__ = ('_selectedItems', '_selectionMode',
                 '_hovered', '_highlighted', '_items', '_filteredItems',
                 '_dragPos', '_dndMode',
                 '_searchText', '_showSearch',
                 # Signals
                 '_itemClicked', '_textClicked', '_searchModified')

    _showSearch:bool
    _dragPos:Optional[Tuple[int,int]]
    _items:List[TTkAbstractListItem]
    _selectedItems:List[TTkAbstractListItem]
    _filteredItems:List[TTkAbstractListItem]
    _highlighted:Optional[TTkAbstractListItem]
    _hovered:Optional[TTkAbstractListItem]

    def __init__(self, *,
                 items:List[TTkAbstractListItemType]=[],
                 selectionMode:TTkK.SelectionMode=TTkK.SelectionMode.SingleSelection,
                 dragDropMode:TTkK.DragDropMode=TTkK.DragDropMode.NoDragDrop,
                 showSearch:bool=True,
                 **kwargs) -> None:
        '''
        :param items: Initial list of items (Any or :py:class:`TTkAbstractListItem` objects), defaults to []
        :type items: list, optional
        :param selectionMode: Selection behavior (:py:class:`TTkK.SelectionMode.SingleSelection` or :py:class:`TTkK.SelectionMode.MultiSelection`), defaults to :py:class:`TTkK.SelectionMode.SingleSelection`
        :type selectionMode: :py:class:`TTkK.SelectionMode`, optional
        :param dragDropMode: Drag and drop behavior (NoDragDrop, InternalMove, DragOnly, DropOnly, DragDrop), defaults to NoDragDrop
        :type dragDropMode: :py:class:`TTkK.DragDropMode`, optional
        :param showSearch: Whether to show the search hint at the top, defaults to True
        :type showSearch: bool, optional
        '''
        # Signals
        self._itemClicked = pyTTkSignal(TTkAbstractListItem)
        self._textClicked = pyTTkSignal(str)
        self._searchModified = pyTTkSignal(str)

        # Default Class Specific Values
        self._selectionMode = selectionMode
        self._selectedItems = []
        self._items = []
        self._filteredItems = self._items
        self._highlighted = None
        self._hovered = None
        self._dragPos = None
        self._dndMode = dragDropMode
        self._searchText:str = ''
        self._showSearch:bool = showSearch
        # Init Super
        super().__init__(**kwargs)
        self.addItemsAt(items=items, pos=0)
        self.setFocusPolicy(TTkK.ClickFocus | TTkK.TabFocus)
        self.searchModified.connect(self._searchModifiedHandler)

    @pyTTkSlot(str)
    def _searchModifiedHandler(self) -> None:
        if self._searchText:
            text = self._searchText.lower()
            self._filteredItems = [i for i in self._items if text in i._lowerText]
        else:
            self._filteredItems = self._items
        self.viewChanged.emit()
        self.update()

    @pyTTkSlot()
    def _itemChangedHandler(self):
        self.viewChanged.emit()

    def viewFullAreaSize(self) -> Tuple[int,int]:
        ''' Return the full area size including padding

        :return: the (width, height) of the full area
        :rtype: tuple[int,int]
        '''
        width = 0
        height = len(self._filteredItems) + ( 1 if self._showSearch and self._searchText else 0 )
        if self._filteredItems:
            width = max(_i.toTTkString().termWidth() for _i in self._filteredItems)
        return width, height

    def search(self) -> str:
        '''
        Returns the current search text.

        :return: The active search filter string
        :rtype: str
        '''
        return self._searchText

    def setSearch(self, search:str) -> None:
        '''
        Sets the search text to filter items.

        :param search: The search string to filter by
        :type search: str
        '''
        self._searchText = search
        self.searchModified.emit(search)

    def searchVisibility(self) -> bool:
        '''
        Returns whether the search hint is visible.

        :return: True if search hint is shown
        :rtype: bool
        '''
        return self._showSearch

    def setSearchVisibility(self, visibility:bool) -> None:
        '''
        Sets the visibility of the search hint at the top of the list.

        :param visibility: True to show search hint, False to hide
        :type visibility: bool
        '''
        self._showSearch = visibility

    def dragDropMode(self) -> TTkK.DragDropMode:
        '''
        Returns the current drag-drop mode.

        :return: The drag-drop behavior setting
        :rtype: :py:class:`TTkK.DragDropMode`
        '''
        return self._dndMode

    def setDragDropMode(self, dndMode:TTkK.DragDropMode) -> None:
        '''
        Sets the drag-drop mode for this list.

        :param dndMode: The new drag-drop behavior
        :type dndMode: :py:class:`TTkK.DragDropMode`
        '''
        self._dndMode = dndMode

    def selectionMode(self) -> TTkK.SelectionMode:
        '''
        Returns the current selection mode.

        :return: The selection behavior setting
        :rtype: :py:class:`TTkK.SelectionMode`
        '''
        return self._selectionMode

    def setSelectionMode(self, mode:TTkK.SelectionMode) -> None:
        '''
        Sets the selection mode for this list.

        :param mode: The new selection behavior (SingleSelection or MultiSelection)
        :type mode: :py:class:`TTkK.SelectionMode`
        '''
        self._selectionMode = mode

    def selectedItems(self) -> List[TTkAbstractListItem]:
        '''
        Returns the list of currently selected items.

        :return: List of selected item widgets
        :rtype: list[:py:class:`TTkAbstractListItem`]
        '''
        return self._selectedItems

    def selectedLabels(self) -> List[str]:
        '''
        Returns the text of all selected items.

        :return: List of selected item texts
        :rtype: list[str]
        '''
        return [i.text() for i in self._selectedItems]

    def items(self) -> List[TTkAbstractListItem]:
        '''
        Returns all items in the list.

        :return: Complete list of items
        :rtype: list[:py:class:`TTkAbstractListItem`]
        '''
        return self._items

    def filteredItems(self) -> List[TTkAbstractListItem]:
        '''
        Returns items matching the current search filter.

        :return: Filtered list of visible items
        :rtype: list[:py:class:`TTkAbstractListItem`]
        '''
        return self._filteredItems

    def addItem(self, item:TTkAbstractListItemType, data:Any=None) -> None:
        '''
        Appends a single item to the end of the list.

        :param item: The item to add (string or :py:class:`TTkAbstractListItem`)
        :type item: str or :py:class:`TTkAbstractListItem`
        :param data: Optional user data to associate with the item
        :type data: Any, optional
        '''
        self.addItemAt(item, len(self._items), data)

    def addItems(self, items:List[TTkAbstractListItemType]) -> None:
        '''
        Appends multiple items to the end of the list.

        :param items: List of items to add (strings or :py:class:`TTkAbstractListItem` objects)
        :type items: list
        '''
        self.addItemsAt(items=items, pos=len(self._items))

    def addItemAt(self, item:TTkAbstractListItemType, pos:int, data:Any=None) -> None:
        '''
        Inserts a single item at the specified position.

        :param item: The item to insert (string or :py:class:`TTkAbstractListItem`)
        :type item: str or :py:class:`TTkAbstractListItem`
        :param pos: The index position to insert at
        :type pos: int
        :param data: Optional user data to associate with the item
        :type data: Any, optional
        '''
        if isinstance(item, str) or isinstance(item, TTkString):
            item = TTkListItem(text=item, data=data)
        self.addItemsAt([item],pos)

    def addItemsAt(self, items:List[TTkAbstractListItemType], pos:int) -> None:
        '''
        Inserts multiple items at the specified position.

        :param items: List of items to insert (strings or :py:class:`TTkAbstractListItem` objects)
        :type items: list
        :param pos: The index position to insert at
        :type pos: int
        '''
        list_items = [
            _i if isinstance(_i, _TTkAbstractListItem)
            else TTkListItem(
                    text=TTkString(_i if isinstance(_i,TTkString) else str(_i)),
                    data=_i)
            for _i in items
        ]
        for item in list_items:
            if not isinstance(item,_TTkAbstractListItem):
                TTkLog.error(f"{item=} is not an TTkAbstractListItem")
                return
        for item in list_items:
            item.dataChanged.connect(self._itemChangedHandler)
        self._items[pos:pos] = list_items
        self._searchModifiedHandler()

    def indexOf(self, item:TTkAbstractListItemType) -> int:
        '''
        Returns the index of the given item.

        :param item: The item to find
        :type item: :py:class:`TTkAbstractListItem` or the data or the text to be searched
        :return: The index of the item, or -1 if not found
        :rtype: int
        '''
        if isinstance(item, _TTkAbstractListItem):
            return self._items.index(item)
        for i, it in enumerate(self._items):
            if it.data() == item or it.text() == item:
                return i
        return -1

    def itemAt(self, pos:int) -> TTkAbstractListItem:
        '''
        Returns the item at the specified index.

        :param pos: The index position
        :type pos: int
        :return: The item at that position
        :rtype: :py:class:`TTkAbstractListItem`
        '''
        return self._items[pos]

    def moveItem(self, fr:int, to:int) -> None:
        '''
        Moves an item from one position to another.

        :param fr: The source index
        :type fr: int
        :param to: The destination index
        :type to: int
        '''
        fr = max(min(fr,len(self._items)-1),0)
        to = max(min(to,len(self._items)-1),0)
        # Swap
        self._items[to] , self._items[fr] = self._items[fr] , self._items[to]
        self._searchModifiedHandler()

    def removeItem(self, item:TTkAbstractListItem) -> None:
        '''
        Removes a single item from the list.

        :param item: The item to remove
        :type item: :py:class:`TTkAbstractListItem`
        '''
        self.removeItems([item])

    def removeItems(self, items:List[TTkAbstractListItem]) -> None:
        '''
        Removes multiple items from the list.

        :param items: List of items to remove
        :type items: list[:py:class:`TTkAbstractListItem`]
        '''
        self.layout().removeWidgets(items)
        for item in items.copy():
            item.dataChanged.disconnect(self._itemChangedHandler)
            self._items.remove(item)
            if item in self._selectedItems:
                self._selectedItems.remove(item)
            if item is self._highlighted:
                self._highlighted = None
        self._searchModifiedHandler()

    def removeAt(self, pos:int) -> None:
        '''
        Removes the item at the specified index.

        :param pos: The index of the item to remove
        :type pos: int
        '''
        self.removeItem(self._items[pos])

    def setCurrentRow(self, row:int) -> None:
        '''
        Selects the item at the specified row.

        :param row: The row index to select
        :type row: int
        '''
        if row<len(self._items):
            item = self._items[row]
            self.setCurrentItem(item)

    def setCurrentItem(self, item:TTkAbstractListItem) -> None:
        '''
        Selects the specified item and emits the itemClicked signal.

        :param item: The item to select
        :type item: :py:class:`TTkAbstractListItem`
        '''
        if self._selectionMode is TTkK.SelectionMode.MultiSelection:
            if item not in self._selectedItems:
                self._selectedItems.append(item)
        else:
            self._selectedItems = [item]
        self._itemClicked.emit(item)
        self._textClicked.emit(item.text())

    def _itemTriggered(self, item:TTkAbstractListItem) -> None:
        if item in self._selectedItems:
            index = self._selectedItems.index(item)
            self._selectedItems.pop(index)
            self.update()
        else:
            self.setCurrentItem(item)

    def _moveToHighlighted(self) -> None:
        '''
        Internal method to scroll the view to show the highlighted item.
        '''
        index = self._items.index(self._highlighted)
        h = self.height()
        offx,offy = self.getViewOffsets()
        if index >= h+offy-1:
            self.viewMoveTo(offx, index-h+1)
        elif index <= offy:
            self.viewMoveTo(offx, index)

    def _to_list_coordinates(self, pos:Tuple[int,int]) -> Tuple[int,int]:
        x,y = pos
        ox,oy = self.getViewOffsets()
        if self._showSearch and self._searchText:
            y-=1
        return (x+ox, y+oy)

    def leaveEvent(self, evt):
        self._hovered = None
        self.update()
        return True

    def mouseMoveEvent(self, evt:TTkMouseEvent) -> bool:
        x,y = self._to_list_coordinates(pos=(evt.x,evt.y))
        self._hovered = None
        if 0<=y<len(self._filteredItems):
            self._hovered = self._filteredItems[y]
        self.update()
        return True

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        x,y = self._to_list_coordinates(pos=(evt.x,evt.y))
        if 0<=y<len(self._filteredItems):
            self._highlighted = self._filteredItems[y]
        self.update()
        return True

    def mouseReleaseEvent(self, evt:TTkMouseEvent):
        if self._highlighted:
            self._itemTriggered(self._highlighted)
            self.update()
        return True

    def mouseDragEvent(self, evt:TTkMouseEvent) -> bool:
        if not(self._dndMode & TTkK.DragDropMode.AllowDrag):
            return False
        items = []
        if self._selectionMode is TTkK.SelectionMode.MultiSelection:
            items = self._selectedItems.copy()
        if self._highlighted and self._highlighted not in items:
            items.append(self._highlighted)
        if not items:
            return True
        drag = TTkDrag()
        data =TTkListWidget._DropListData(widget=self,items=items)
        h = min(3,ih:=len(items)) + 2 + (1 if ih>3 else 0)
        w = min(20,iw:=max([it.text().termWidth() for it in items[:3]])) + 2
        pm = TTkCanvas(width=w,height=h)
        for y,it in enumerate(items[:3],1):
            txt = it.text()
            if txt.termWidth() < 20:
                pm.drawText(pos=(1,y), text=it.text())
            else:
                pm.drawText(pos=(1,y), text=it.text(), width=17)
                pm.drawText(pos=(18,y), text='...')
        if ih>3:
            pm.drawText(pos=(1,4), text='...')
        pm.drawBox(pos=(0,0),size=(w,h))
        drag.setPixmap(pm)
        drag.setData(data)
        drag.exec()
        return True

    def dragEnterEvent(self, evt:TTkDnDEvent) -> bool:
        if not(self._dndMode & TTkK.DragDropMode.AllowDrop):
            return False
        if issubclass(type(evt.data()),TTkListWidget._DropListData):
            return self.dragMoveEvent(evt)
        return False

    def dragMoveEvent(self, evt:TTkDnDEvent) -> bool:
        if not(self._dndMode & TTkK.DragDropMode.AllowDrop):
            return False
        x,y = self._to_list_coordinates(pos=(evt.x,evt.y))
        y=max(0,min(y,len(self._items)))
        self._dragPos = (x,y)
        self.update()
        return True

    def dragLeaveEvent(self, evt:TTkDnDEvent) -> bool:
        self._dragPos = None
        self.update()
        return True

    def dropEvent(self, evt:TTkDnDEvent) -> bool:
        if not(self._dndMode & TTkK.DragDropMode.AllowDrop):
            return False
        self._dragPos = None
        data = evt.data()
        if not isinstance(data ,TTkListWidget._DropListData):
            return False

        x,y = self._to_list_coordinates(pos=(evt.x,evt.y))

        wid   = data.widget
        items = data.items
        if not (wid and items):
            return False

        wid.removeItems(items)
        wid._searchModifiedHandler()

        if y <= 0:
            y = 0
        elif y > len(self._filteredItems):
            y = len(self._items)
        elif y == len(self._filteredItems):
            filteredItemAt = self._filteredItems[-1]
            y = self._items.index(filteredItemAt)+1
        else:
            filteredItemAt = self._filteredItems[y]
            y = self._items.index(filteredItemAt)

        self.addItemsAt(items,y)
        self._searchModifiedHandler()
        return True

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        # if not self._highlighted: return False
        if ( not self._searchText and evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            self._itemTriggered(self._highlighted)

        elif evt.type == TTkK.Character:
            # Add this char to the search text
            self._searchText += evt.key
            self.update()
            self.searchModified.emit(self._searchText)

        elif ( evt.type == TTkK.SpecialKey and
               evt.key == TTkK.Key_Tab ):
            return False

        elif ( evt.type == TTkK.SpecialKey and
               evt.key in (TTkK.Key_Delete,TTkK.Key_Backspace) and
               self._searchText ):
            # Handle the backspace to remove the last char from the search text
            self._searchText = self._searchText[:-1]
            self.update()
            self.searchModified.emit(self._searchText)

        elif ( evt.type == TTkK.SpecialKey and
               self._filteredItems):
            # Handle the arrow/movement keys
            index = 0
            if self._highlighted:
                if self._highlighted not in self._filteredItems:
                    self._highlighted = self._filteredItems[0]
                index = self._filteredItems.index(self._highlighted)
            offx,offy = self.getViewOffsets()
            h = self.height()
            if evt.key == TTkK.Key_Up:
                index = max(0, index-1)
            elif evt.key == TTkK.Key_Down:
                index = min(len(self._filteredItems)-1, index+1)
            elif evt.key == TTkK.Key_PageUp:
                index = max(0, index-h)
            elif evt.key == TTkK.Key_PageDown:
                index = min(len(self._filteredItems)-1, index+h)
            elif evt.key == TTkK.Key_Right:
                self.viewMoveTo(offx+1, offy)
            elif evt.key == TTkK.Key_Left:
                self.viewMoveTo(offx-1, offy)
            elif evt.key == TTkK.Key_Home:
                self.viewMoveTo(0, offy)
            elif evt.key == TTkK.Key_End:
                self.viewMoveTo(0x10000, offy)
            elif evt.key in (TTkK.Key_Delete,TTkK.Key_Backspace):
                if self._searchText:
                    self._searchText = self._searchText[:-1]
                    self.update()
                    self.searchModified.emit(self._searchText)
            self._highlighted = self._filteredItems[index]
            self._moveToHighlighted()
            self.update()
        else:
            return False
        return True

    def focusInEvent(self):
        if not self._items: return
        if not self._highlighted and self._filteredItems:
            self._highlighted = self._filteredItems[0]

    def focusOutEvent(self):
        self._dragPos = None

    def paintEvent(self, canvas: TTkCanvas) -> None:
        w,h = self.size()
        ox,oy = self.getViewOffsets()
        search_offset = 0

        style = self.currentStyle()
        color_base = style['color']
        color_search = style['searchColor']
        color_hovered = style['hovered']
        color_selected = style['selected']
        color_highlighted = style['highlighted']

        if self._showSearch and self._searchText:
            search_offset = 1
            if len(self._searchText) > w:
                text = TTkString("≼",TTkColor.BG_BLUE+TTkColor.FG_CYAN)+TTkString(self._searchText[-w+1:], color_search)
            else:
                text = TTkString(self._searchText, color_search)
            canvas.drawTTkString(pos=(0,0),text=text, color=color_search, width=w)

        for i,item in enumerate(self._filteredItems[oy:oy+h-search_offset], search_offset):
            if item in self._selectedItems:
                item_color = color_selected
            elif item is self._highlighted:
                item_color = color_highlighted
            elif item is self._hovered:
                item_color = color_hovered
            else:
                item_color = color_base
            canvas.drawTTkString(text=item.toTTkString(), pos=(-ox,i), width=w+ox, color=item_color)

        # Draw the drop visual feedback
        if self._dragPos:
            x,y = self._dragPos
            y+=search_offset
            offx,offy = self.getViewOffsets()
            p1 = (0,y-offy-1)
            p2 = (0,y-offy)
            canvas.drawText(pos=p1,text="╙─╼", color=TTkColor.fg("#FFFF00")+TTkColor.bg("#008855"))
            canvas.drawText(pos=p2,text="╓─╼", color=TTkColor.fg("#FFFF00")+TTkColor.bg("#008855"))

