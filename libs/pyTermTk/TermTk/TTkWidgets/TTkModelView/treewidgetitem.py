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

__all__ = ['TTkTreeWidgetItem']

from dataclasses import dataclass
from typing import List, Tuple, Iterator, Generator, Optional, Callable, Any

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets import TTkWidget
from TermTk.TTkAbstract.abstractitemmodel import TTkAbstractItemModel

@dataclass
class _TTkTreePageItem():
    y:int
    level:int
    item:TTkTreeWidgetItem

@dataclass
class _TTkTreeBuffer():
    level:int
    total_size:int
    buffered_size:int
    buffer:List[Tuple[int,int,TTkTreeWidgetItem]]
    buffer_link:List[Tuple[int,int]]


    def __init__(self):
        self.level = 0
        self.total_size = 0
        self.buffer = []
        self.buffer_link = []
        self._gen:Optional[Iterator] = None

    def get_link(self, index:int) -> int:
        if index<0:
            return 0
        if index >= len(self.buffer_link):
            return len(self.buffer)
        return self.buffer_link[index][0]

    def clearBuffer(self):
        self.buffer = []
        self.buffer_link = []

    def clearBufferFromIndex(self, index:int) -> None:
        if index<0:
            self.clearBuffer()
        elif index >= len(self.buffer_link):
            pass
        else:
            link = self.buffer_link[index][0]
            self.buffer[link:] = []
            self.buffer_link[index+1:] = []
            link = self.buffer_link[index] = (link,0)

    def get_page(self, item:TTkTreeWidgetItem, level:int, index:int, size:int) -> List[Tuple[int,int,TTkTreeWidgetItem]]:
        # Add the item to the buffer
        if self.level != level:
            self.clearBuffer()
        if not self.buffer:
            self.buffer = [(level, _y, item) for _y in range(item._height)]
            self.buffer_link = [(item._height, 0)]
        final_index = index+size
        buffered_size = len(self.buffer)
        if item._expanded:
            while buffered_size < final_index:
                last_index = len(self.buffer_link)-1
                if len(item._children) <= last_index:
                    break
                #                   | last_index
                #                   |    ch_last_index = ch_h
                #                   |    |       => left to fetch = (ch_h, final_index - buffered_size)
                # Children  * <---> * <--|xxxx|      > * <  >
                #          /
                # item    *<-------------|xxxx|             buffer
                #                        |    final_index
                #                        buffered_size
                #
                ch_buffer_index, ch_h = self.buffer_link[last_index]
                child = item._children[last_index]
                ch_s = child.size()
                if ch_h != ch_s:
                    ch_index = ch_h
                    ch_size = final_index - ch_buffer_index - ch_h
                    child_page = child._get_page(level+1, ch_index, ch_size)

                    self.buffer.extend(child_page)
                    ch_h += len(child_page)
                    self.buffer_link[last_index] = (ch_buffer_index, ch_h)
                    buffered_size = len(self.buffer)
                if ch_h == ch_s:
                    self.buffer_link.append((buffered_size, 0))
        return self.buffer[index:final_index]

class TTkTreeWidgetItem(TTkAbstractItemModel):
    '''
    The :py:class:`TTkTreeWidgetItem` class provides an item for use with the :py:class:'TTkTree' convenience class.

    Tree widget items are used to hold rows of information for tree widgets.
    Rows usually contain several columns of data, each of which can contain a :py:class:`TTkString` label and an icon or a :py:class:`TTkWidget`.

    Items are usually constructed with a parent that is :py:class:`TTkTreeWidgetItem` (for items on lower levels of the tree). For example,
    the following code constructs a top-level item to represent cities of the world, and adds a entry
    for Oslo as a child item:

    .. code-block:: python

        cities = TTkWidgetItem(["Cities"])
        osloItem = TTkWidgetItem(["Oslo"], parent=cities)

    or

    .. code-block:: python

        cities = TTkWidgetItem(["Cities"])
        osloItem = TTkWidgetItem(["Oslo"]
        cities.addChild(osloItem)

    '''

    __slots__ = ('_parent', '_data', '_widgets', '_height', '_alignment', '_children', '_expanded', '_selected', '_hidden',
                 '_childIndicatorPolicy', '_icon', '_defaultIcon',
                 '_sortColumn', '_sortOrder', '_hasWidgets', '_parentWidget',
                 '_list_bk', '_list_h_bk',
                 '_buffer',
        # Signals
        # 'refreshData'
        'heightChanged', '_invalidateListBuffer', '_sizeChanged',

        # Slot that accept itself
        '_sizeChangedHandler'
        )

    _children:List[TTkTreeWidgetItem]
    _buffer:_TTkTreeBuffer
    _sizeChangedHandler: Callable[[TTkTreeWidgetItem,int,int], None]

    def __init__(self, *args,
                 parent:TTkTreeWidgetItem=None,
                 expanded:bool=False,
                 selected:bool=False,
                 hidden:bool=False,
                 icon:TTkString=None,
                 childIndicatorPolicy:TTkK.ChildIndicatorPolicy =TTkK.ChildIndicatorPolicy.DontShowIndicatorWhenChildless,
                 **kwargs) -> None:
        # Signals
        # self.refreshData = pyTTkSignal(TTkTreeWidgetItem)
        self.heightChanged = pyTTkSignal(int)
        self._invalidateListBuffer = pyTTkSignal(TTkTreeWidgetItem)
        self._sizeChanged = pyTTkSignal(TTkTreeWidgetItem,int)
        self._hasWidgets = False
        self._children = []
        self._list_bk = []
        self._list_h_bk = []
        self._buffer = _TTkTreeBuffer()
        self._parentWidget = None
        self._height = 1
        data = args[0] if len(args)>0 and type(args[0])==list else [TTkString()]
        # self._data = [i if issubclass(type(i), TTkString) else TTkString(i) if isinstance(i,str) else TTkString() for i in data]
        self._parent = None
        self._childIndicatorPolicy = childIndicatorPolicy
        self._defaultIcon = True
        self._expanded = expanded
        self._selected = selected
        self._hidden = hidden
        self._sortColumn = -1
        self._sortOrder = TTkK.AscendingOrder

        # I need this hack because I cannot define the class itself in the slot
        @pyTTkSlot(TTkTreeWidgetItem, int)
        def _sch(item:TTkTreeWidgetItem, diffSize:int) -> None:
            if item == self or self._expanded:
                if item==self:
                    self._buffer.clearBuffer()
                else:
                    self._buffer.clearBufferFromIndex(self._children.index(item))
                self._buffer.total_size += diffSize
                self._sizeChanged.emit(self, diffSize)
        self._sizeChangedHandler = _sch

        super().__init__(**kwargs)
        self._data, self._widgets = self._processDataInput(data)
        self._alignment = [TTkK.LEFT_ALIGN]*len(self._data)

        self._icon = ['']*len(self._data)
        self._setDefaultIcon()
        if icon:
            self._icon[0] = icon
            self._defaultIcon = False
        if parent:
            parent.addChild(self)

    def _processDataInputWidget(self, widget, index):
        self._hasWidgets = True
        widget.hide()
        widget.sizeChanged.connect(self._widgetSizeChanged)
        self._height = max(self._height,widget.height())
        if self._parentWidget:
            widget.setTreeItemParent(self._parentWidget)
        if hasattr(widget, 'text'):
            ret = widget.text()
            if hasattr(widget,'textChanged'):
                def _updateField(index):
                    def __updateFieldRet(text):
                        self._data[index] = text
                    return __updateFieldRet
                widget.textChanged.connect(_updateField(index))
        else:
            ret = TTkString()
        return ret

    def _processDataInput(self, dataInput):
        retData, retWidgets = [],[]
        for index, di in enumerate(dataInput):
            if issubclass(type(di), TTkString):
                retData.append(di)
                retWidgets.append(None)
            elif isinstance(di,str):
                retData.append(TTkString(di))
                retWidgets.append(None)
            elif issubclass(type(di), TTkWidget):
                retData.append(self._processDataInputWidget(di, index))
                retWidgets.append(di)
            else:
                retData.append(TTkString())
                retWidgets.append(None)
            self._height = max(self._height,len(retData[-1].split('\n')))
            self._buffer.total_size = self._height
        return retData, retWidgets

    def _setDefaultIcon(self):
        if not self._defaultIcon: return
        self._icon[0] = TTkCfg.theme.tree[0]
        if self._childIndicatorPolicy == TTkK.DontShowIndicatorWhenChildless and self._children or \
           self._childIndicatorPolicy == TTkK.ShowIndicator:
            if self._expanded:
                self._icon[0] = TTkCfg.theme.tree[2]
            else:
                self._icon[0] = TTkCfg.theme.tree[1]

    @pyTTkSlot(int, int)
    def _widgetSizeChanged(self, _, h):
        if h != self._height:
            h = max(max([len(s.split("\n")) for s in self._data]), max(w.height() for w in self._widgets if w))
        if h != self._height:
            diffSize = h - self._height
            self._height = h
            self.heightChanged.emit(h)
            self._sizeChangedHandler(self,diffSize)
            if self._parentWidget:
                self._parentWidget._refreshCache()

    def height(self):
        return self._height

    def _clearTreeItemParent(self):
        widgets = []
        if self._hasWidgets:
            widgets += [w for w in self._widgets if w and w.parentWidget()]
            # for widget in widgets:
            #     if pw := widget.parentWidget():
            #         pw.rootLayout().removeWidgets([w for w in self._widgets if w])
            if self._parentWidget:
                self._parentWidget.rootLayout().removeWidgets(widgets)
        self._parentWidget = None
        for c in self._children:
            widgets += c._clearTreeItemParent()
        return widgets

    def _setTreeItemParent(self, parent):
        self._parentWidget = parent
        widgets = []
        if self._hasWidgets:
            widgets += [w for w in self._widgets if w]
            # parent.layout().addWidgets(widgets)
        for c in self._children:
            widgets += c._setTreeItemParent(parent)
        return widgets

    def _item_at(self, pos:int) -> Optional[Tuple[int,int,TTkTreeWidgetItem]]:
        if pos < 0:
            return None
        if page := self._get_page(self._buffer.level, pos, 1):
            return page[0]
        else:
            return None

    def _get_page(self, level:int, index:int, size:int) -> List[Tuple[int,int,TTkTreeWidgetItem]]:
        return self._buffer.get_page(self,level,index,size)

    def _iterate(self, level:int=0, skip:int=0) ->  Generator[Tuple[TTkTreeWidgetItem, int], None, int]:
        for _c in self._children:
            if skip>0:
                skip -= 1
            else:
                yield _c, level
            if _c._expanded:
                skip = yield from _c._iterate(level+1, skip)
        return skip

    def _iterate_h(self, level:int=0, skip:int=0) -> Generator[Tuple[TTkTreeWidgetItem, int, int], None, int]:
        for _c in self._children:
            for _y in range(_c._height):
                if skip>0:
                    skip -= 1
                else:
                    yield _c, level, _y
            if _c._expanded:
                skip = yield from _c._iterate_h(level+1, skip)
        return skip

    def _listify(self, level:int):
        self._list_h_bk = [(self,level,_y) for _y in range(self._height)]
        if self._expanded:
            for _c in self._children:
                self._list_h_bk.extend(_c.listify(level+1))

    def listify(self,level:int=0) -> List[TTkTreeWidgetItem, int, int]:
        if not self._list_h_bk:
            self._listify(level=level)
        return self._list_h_bk

    def setTreeItemParent(self, parent):
        if parent:
            widgets = self._setTreeItemParent(parent)
            parent.layout().addWidgets(widgets)
        else:
            # pw = self._parentWidget
            widgets = self._clearTreeItemParent()
            # pw.rootLayout().removeWidgets(widgets)

    def hasWidgets(self):
        return self._hasWidgets

    def isHidden(self):
        return self._hidden

    def setHidden(self, hide):
        if hide == self._hidden: return
        self._hidden = hide
        self.emitDataChanged()

    def childIndicatorPolicy(self):
        return self._childIndicatorPolicy

    def setChildIndicatorPolicy(self, policy):
        self._childIndicatorPolicy = policy
        self._setDefaultIcon()

    def _addChild(self, child:TTkTreeWidgetItem):
        self._children.append(child)
        child._parent = self
        child._sortOrder = self._sortOrder
        child._sortColumn = self._sortColumn
        self._setDefaultIcon()
        self._sort(children=False)
        if self._parentWidget:
            child.setTreeItemParent(self._parentWidget)
        child.dataChanged.connect(self.emitDataChanged)
        child._sizeChanged.connect(self._sizeChangedHandler)
        child._invalidateListBuffer.connect(self._invalidateListBufferHandler)

    def addChild(self, child:TTkTreeWidgetItem):
        self._addChild(child)
        self._list_h_bk = []
        self._invalidateListBuffer.emit(self)
        if self._expanded:
            self._sizeChangedHandler(self, child.size())
        self.emitDataChanged()

    def addChildren(self, children:List[TTkTreeWidgetItem]):
        for child in children:
            self._addChild(child)
        self._list_h_bk = []
        self._invalidateListBuffer.emit(self)
        if self._expanded:
            sizes = sum(_c.size() for _c in children)
            self._sizeChangedHandler(self, sizes)
        self.emitDataChanged()

    def removeChild(self, child:TTkTreeWidgetItem):
        if child in self._children:
            self.takeChild(self._children.index(child))

    def takeChild(self, index):
        if not (self._children and 0<= index < len(self._children)):
            return None
        child = self._children.pop(index)
        child.dataChanged.disconnect(self.emitDataChanged)
        child._sizeChanged.disconnect(self._sizeChangedHandler)
        child._invalidateListBuffer.disconnect(self._invalidateListBufferHandler)
        child.setTreeItemParent(None)
        self._sizeChangedHandler(self, -child.size())
        self._list_h_bk = []
        self._invalidateListBuffer.emit(self)
        self.emitDataChanged()
        return child

    def takeChildren(self):
        children = self._children
        for child in children:
            child.dataChanged.disconnect(self.emitDataChanged)
            child._sizeChanged.disconnect(self._sizeChangedHandler)
            child._invalidateListBuffer.disconnect(self._invalidateListBufferHandler)
            child.setTreeItemParent(None)
        self._sizeChangedHandler(self, self._height-self._buffer.total_size)
        self._children = []
        self._list_h_bk = []
        self._invalidateListBuffer.emit(self)
        self.emitDataChanged()
        return children

    def child(self, index:int) -> TTkTreeWidgetItem:
        if 0 <= index < len(self._children):
            return self._children[index]
        return None

    def children(self) -> List[TTkTreeWidgetItem]:
        return [x for x in self._children if not x.isHidden()]

    def indexOfChild(self, child:TTkTreeWidgetItem) -> Optional[int]:
        if child in self._children:
            return self._children.index(child)
        return None

    def icon(self, col):
        if col >= len(self._icon):
            return ''
        return self._icon[col]

    def setIcon(self, col, icon):
        if col==0:
            self._defaultIcon = False
        self._icon[col] = icon
        self.dataChanged.emit()

    def textAlignment(self, col):
        if col >= len(self._alignment):
            return TTkK.LEFT_ALIGN
        return self._alignment[col]

    def setTextAlignment(self, col, alignment):
        self._alignment[col] = alignment
        self.dataChanged.emit()

    def data(self, col, role=None):
        if col >= len(self._data):
            return ''
        return self._data[col]

    def widget(self, col, role=None):
        if col >= len(self._data):
            return None
        return self._widgets[col]

    def expandAll(self) -> None:
        for child in self._children:
            child.setExpanded(True)
            child.expandAll()

    def collapseAll(self) -> None:
        for child in self._children:
            child.setExpanded(False)
            child.collapseAll()

    def sortData(self, col):
        return self.data(col)

    def _sort(self, children):
        if self._sortColumn == -1: return
        self._children = sorted(
                self._children,
                key = lambda x : x.sortData(self._sortColumn),
                reverse = self._sortOrder == TTkK.DescendingOrder)
        # Broadcast the sorting to the children
        if children:
            for c in self._children:
                c.dataChanged.disconnect(self.emitDataChanged)
                c._sizeChanged.disconnect(self._sizeChangedHandler)
                c._invalidateListBuffer.disconnect(self._invalidateListBufferHandler)
                c.sortChildren(self._sortColumn, self._sortOrder)
                c._invalidateListBuffer.connect(self._invalidateListBufferHandler)
                c._sizeChanged.connect(self._sizeChangedHandler)
                c.dataChanged.connect(self.emitDataChanged)

    def sortChildren(self, col, order):
        self._sortColumn = col
        self._sortOrder = order
        if not self._children: return
        self._sort(children=True)
        self._list_h_bk = []
        self._invalidateListBuffer.emit(self)
        self.dataChanged.emit()

    @pyTTkSlot()
    def emitDataChanged(self):
        self.dataChanged.emit()

    @pyTTkSlot()
    def _invalidateListBufferHandler(self):
        self._list_h_bk = []
        if self._expanded:
            self._invalidateListBuffer.emit(self)

    # def setDisabled(disabled):
    #    pass

    def setExpanded(self, expand:bool):
        # hide all the widgets if this item is not expanded
        if not expand:
            def _recurseHide(item):
                for c in item._children:
                    if c._hasWidgets:
                        for widget in [w for w in c._widgets if w]:
                            widget.hide()
                    if c._expanded:
                        _recurseHide(c)
            _recurseHide(self)
        if self._expanded != expand and self._children:
            self._list_h_bk = []
            if expand:
                self._sizeChangedHandler(self, sum(_c.size() for _c in self._children))
            else:
                self._sizeChangedHandler(self, self._height-self._buffer.total_size)
            self._invalidateListBuffer.emit(self)
        self._expanded = expand
        self._setDefaultIcon()
        self.dataChanged.emit()

    def setSelected(self, select):
        self._selected = select

    # def isDisabled():
    #     pass

    def isExpanded(self):
        return self._expanded

    def isSelected(self):
        return self._selected

    def size(self):
        if not self._children:
            return self._height
        if not self._buffer.total_size:
            if self._expanded:
                ret = self._height
                for _c in self._children:
                    ret += _c.size()
                self._buffer.total_size = ret
            else:
                self._buffer.total_size = self._height
        return self._buffer.total_size
