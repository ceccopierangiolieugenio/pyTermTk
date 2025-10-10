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
from typing import List, Tuple, Iterator, Generator, Optional, Callable, Any, ClassVar

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString, TTkStringType
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets import TTkWidget
from TermTk.TTkAbstract.abstractitemmodel import TTkAbstractItemModel

@dataclass
class _TTkTreeChildren(TTkAbstractItemModel):
    __slots__ = (
        '_parent',
        '_level',
        '_total_size',
        '_buffer','_buffer_link',
        '_children',
        '_childrenSizeChanged')

    _parent:TTkTreeWidgetItem
    _level:int
    _total_size:int
    _buffer:List[Tuple[int,int,TTkTreeWidgetItem]]
    _buffer_link:List[Tuple[int,int]]
    _children: List[TTkTreeWidgetItem]

    def __init__(self, parent:TTkTreeWidgetItem):
        self._parent = parent
        self._childrenSizeChanged = pyTTkSignal(TTkTreeWidgetItem,int)
        self._level = 0
        self._total_size = 0
        self._buffer = []
        self._buffer_link = []
        self._children = []
        super().__init__()

    def _childrenSizeChangedHandler(self, item:Optional[TTkTreeWidgetItem], diffSize:int) -> None:
        if item:
            self.clearBufferFromIndex(self._children.index(item))
        else:
            self.clearBuffer()
        self._total_size += diffSize
        self._childrenSizeChanged.emit(self, diffSize)

    def get_link(self, index:int) -> int:
        if index<0:
            return 0
        if index >= len(self._buffer_link):
            return len(self._buffer)
        return self._buffer_link[index][0]

    def clearBuffer(self):
        self._buffer = []
        self._buffer_link = []

    def clearBufferFromIndex(self, index:int) -> None:
        if index<0:
            self.clearBuffer()
        elif index >= len(self._buffer_link):
            pass
        else:
            link = self._buffer_link[index][0]
            self._buffer[link:] = []
            self._buffer_link[index+1:] = []
            self._buffer_link[index] = (link,0)

    def get_page(self, level:int, index:int, size:int) -> List[Tuple[int,int,TTkTreeWidgetItem]]:
        # Add the item to the buffer
        if self._level != level:
            self.clearBuffer()
            self._level = level
        if not self._buffer:
            self._buffer_link = [(0, 0)]
        final_index = index+size
        buffered_size = len(self._buffer)
        while buffered_size < final_index:
            last_index = len(self._buffer_link)-1
            if len(self._children) <= last_index:
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
            ch_buffer_index, ch_h = self._buffer_link[last_index]
            child = self._children[last_index]
            ch_s = child.size()
            if ch_h != ch_s:
                ch_index = ch_h
                ch_size = final_index - ch_buffer_index - ch_h
                child_page = child._get_page(level, ch_index, ch_size)

                self._buffer.extend(child_page)
                ch_h += len(child_page)
                self._buffer_link[last_index] = (ch_buffer_index, ch_h)
                buffered_size = len(self._buffer)
            if ch_h == ch_s:
                self._buffer_link.append((buffered_size, 0))
        return self._buffer[index:final_index]

    @pyTTkSlot()
    def emitDataChanged(self):
        self.dataChanged.emit()

    def _addChild(self, parent:TTkTreeWidgetItem, child:TTkTreeWidgetItem):
        self._children.append(child)
        child._parent = self._parent
        child._sortOrder = self._parent._sortOrder
        child._sortColumn = self._parent._sortColumn
        child.dataChanged.connect(self.emitDataChanged)
        child._sizeChanged.connect(self._childrenSizeChangedHandler)

    def addChild(self, parent:TTkTreeWidgetItem, child:TTkTreeWidgetItem):
        self._addChild(parent, child)
        self._childrenSizeChangedHandler(child, child.size())
        self.sort()
        self.emitDataChanged()

    def addChildren(self, parent:TTkTreeWidgetItem, children:List[TTkTreeWidgetItem]):
        if children:
            for child in children:
                self._addChild(parent, child)
            sizes = sum(_c.size() for _c in children)
            self._childrenSizeChangedHandler(children[0], sizes)
            self.sort()
            self.emitDataChanged()

    def removeChild(self, child:TTkTreeWidgetItem) -> None:
        if child in self._children:
            self.takeChild(self._children.index(child))

    def takeChild(self, index) -> Optional[TTkTreeWidgetItem]:
        if not ( self._children and
                 0<= index < len(self._children) ):
            return None
        child = self._children.pop(index)
        child.dataChanged.disconnect(self.emitDataChanged)
        child._sizeChanged.disconnect(self._childrenSizeChangedHandler)
        self._childrenSizeChangedHandler(None, -child.size())
        self.emitDataChanged()
        return child

    def takeChildren(self) -> List[TTkTreeWidgetItem]:
        children = self._children
        for child in children:
            child.dataChanged.disconnect(self.emitDataChanged)
            child._sizeChanged.disconnect(self._childrenSizeChangedHandler)
        self._childrenSizeChangedHandler(None, -self._total_size)
        self.emitDataChanged()
        return children

    def child(self, index:int) -> Optional[TTkTreeWidgetItem]:
        if 0 <= index < len(self._children):
            return self._children[index]
        return None

    def children(self) -> List[TTkTreeWidgetItem]:
        return self._children

    def indexOfChild(self, child:TTkTreeWidgetItem) -> Optional[int]:
        if child in self._children:
            return self._children.index(child)
        return None

    def expandAll(self) -> None:
        for child in self._children:
            child.setExpanded(True)
            child.expandAll()

    def collapseAll(self) -> None:
        for child in self._children:
            child.setExpanded(False)
            child.collapseAll()

    def sort(self):
        if self._parent._sortColumn == -1: return
        self._children = sorted(
                self._children,
                key = lambda _i : _i.data(self._parent._sortColumn),
                reverse = self._parent._sortOrder == TTkK.DescendingOrder)
        for c in self._children:
            c.dataChanged.disconnect(self.emitDataChanged)
            c._sizeChanged.disconnect(self._childrenSizeChangedHandler)
            c.sortChildren(self._parent._sortColumn, self._parent._sortOrder)
            c._sizeChanged.connect(self._childrenSizeChangedHandler)
            c.dataChanged.connect(self.emitDataChanged)
        self.clearBuffer()
        self.emitDataChanged()

    def size(self):
        if not self._total_size:
            self._total_size = sum(_c.size() for _c in self._children)
        return self._total_size

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

    __slots__ = (
        '_parent', '_data', '_widgets', '_height', '_alignment',
        '_children', '_expanded', '_selected', '_hidden',
        '_childIndicatorPolicy', '_icon', '_defaultIcon',
        '_sortColumn', '_sortOrder', '_hasWidgets',
        '_buffer', '_level',
        # Signals
        # 'refreshData'
        'heightChanged', '_sizeChanged',
        )


    _icon:List[TTkString]
    _alignment:List[TTkK.Alignment]
    _sortOrder:TTkK.SortOrder
    _buffer:List[Tuple[int,int,TTkTreeWidgetItem]]
    _children:Optional[_TTkTreeChildren]
    _childIndicatorPolicy:TTkK.ChildIndicatorPolicy

    def __init__(self, *args,
                 parent:Optional[TTkTreeWidgetItem]=None,
                 expanded:bool=False,
                 selected:bool=False,
                 hidden:bool=False,
                 icon:TTkStringType='',
                 childIndicatorPolicy:TTkK.ChildIndicatorPolicy =TTkK.ChildIndicatorPolicy.DontShowIndicatorWhenChildless,
                 **kwargs) -> None:
        # Signals
        # self.refreshData = pyTTkSignal(TTkTreeWidgetItem)
        self.heightChanged = pyTTkSignal(int)
        self._sizeChanged = pyTTkSignal(TTkTreeWidgetItem,int)
        self._children = None
        self._buffer = []
        self._level = 0
        self._hasWidgets = False
        self._height = 1
        data = args[0] if len(args)>0 and type(args[0])==list else [TTkString()]
        # self._data = [i if issubclass(type(i), TTkString) else TTkString(i) if isinstance(i,str) else TTkString() for i in data]
        self._parent = parent
        self._childIndicatorPolicy = childIndicatorPolicy
        self._defaultIcon = True
        self._expanded = expanded
        self._selected = selected
        self._hidden = hidden
        self._sortColumn = -1
        self._sortOrder = TTkK.AscendingOrder

        super().__init__(**kwargs)
        self._data, self._widgets = self._processDataInput(data)
        self._alignment = [TTkK.LEFT_ALIGN]*len(self._data)

        self._icon = [TTkString()]*len(self._data)
        self._setDefaultIcon()
        if icon:
            self._icon[0] = ' '+TTkString(icon)+TTkString(' ')
            self._defaultIcon = False
        if parent:
            parent.addChild(self)

    def _sizeChangedHandler(self, item:TTkTreeWidgetItem, diffSize:int) -> None:
        if self._expanded or item==self:
            self._sizeChanged.emit(self, diffSize)

    def _processDataInputWidget(self, widget:TTkWidget, index:int) -> TTkString:
        self._hasWidgets = True
        widget.hide()
        widget.sizeChanged.connect(self._widgetSizeChanged)
        self._height = max(self._height,widget.height())
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
        return retData, retWidgets

    def _setDefaultIcon(self):
        if not self._defaultIcon: return
        self._icon[0] = TTkString(' '+TTkCfg.theme.tree[0]+' ')
        if ( self._childIndicatorPolicy == TTkK.DontShowIndicatorWhenChildless and
             self._children and self._children._children or
             self._childIndicatorPolicy == TTkK.ShowIndicator ):
            if self._expanded:
                self._icon[0] = TTkString(' '+TTkCfg.theme.tree[2]+' ')
            else:
                self._icon[0] = TTkString(' '+TTkCfg.theme.tree[1]+' ')

    @pyTTkSlot(int, int)
    def _widgetSizeChanged(self, _, h):
        if h != self._height:
            h = max(max([len(s.split("\n")) for s in self._data]), max(w.height() for w in self._widgets if w))
        if h != self._height:
            diffSize = h - self._height
            self._height = h
            self._buffer = []
            self.heightChanged.emit(h)
            self._sizeChangedHandler(self,diffSize)

    def height(self):
        return 0 if self._hidden else self._height

    def _get_page(self, level:int, index:int, size:int) -> List[Tuple[int,int,TTkTreeWidgetItem]]:
        if self._hidden:
            return []
        _h = self._height
        _to = index+size

        if self._level != level:
            self._buffer=[]
            self._level = level

        if not self._buffer:
            self._buffer = [(level, _y, self) for _y in range(_h)]

        # The page is among the children
        if self._expanded and self._children and index >= _h :
            return self._children.get_page(level+1, index-_h, size)
        elif _to <= _h: # The page is in this node
            return self._buffer[index:_to]
        elif index < _h and self._expanded and self._children: # the page include the current item and the children
            return self._buffer[index:] + self._children.get_page(level+1, 0, size+index-_h)
        return self._buffer[index:]

    def hasWidgets(self):
        return self._hasWidgets

    def isHidden(self) -> bool:
        return self._hidden

    def setHidden(self, hide:bool) -> None:
        if hide == self._hidden:
            return
        self._hidden = hide
        if hide:
            self._sizeChangedHandler(self,-self._height)
        else:
            self._sizeChangedHandler(self,self._height)
        self.emitDataChanged()

    def childIndicatorPolicy(self) -> TTkK.ChildIndicatorPolicy:
        return self._childIndicatorPolicy

    def setChildIndicatorPolicy(self, policy:TTkK.ChildIndicatorPolicy) -> None:
        self._childIndicatorPolicy = policy
        self._setDefaultIcon()


    def addChild(self, child:TTkTreeWidgetItem) -> None:
        if not self._children:
            self._children = _TTkTreeChildren(self)
            self._children._childrenSizeChanged.connect(self._sizeChangedHandler)
            self._children.dataChanged.connect(self.emitDataChanged)
        child = self._children.addChild(self, child)
        self._setDefaultIcon()

    def addChildren(self, children:List[TTkTreeWidgetItem]) -> None:
        if not self._children:
            self._children = _TTkTreeChildren(self)
            self._children._childrenSizeChanged.connect(self._sizeChangedHandler)
            self._children.dataChanged.connect(self.emitDataChanged)
        children = self._children.addChildren(self, children)
        self._setDefaultIcon()

    def removeChild(self, child:TTkTreeWidgetItem) -> None:
        if not self._children:
            return
        self._children.removeChild(child)
        if not self._children.size():
            self._children.dataChanged.disconnect(self.emitDataChanged)
            self._children._childrenSizeChanged.disconnect(self._sizeChangedHandler)
            self._children = None
        self._setDefaultIcon()

    def takeChild(self, index:int) -> Optional[TTkTreeWidgetItem]:
        if not self._children:
            return None
        child = self._children.takeChild(index)
        if not self._children.size():
            self._children.dataChanged.disconnect(self.emitDataChanged)
            self._children._childrenSizeChanged.disconnect(self._sizeChangedHandler)
            self._children = None
        self._setDefaultIcon()
        return child

    def takeChildren(self) -> List[TTkTreeWidgetItem]:
        if not self._children:
            return []
        children = self._children.takeChildren()
        self._children.dataChanged.disconnect(self.emitDataChanged)
        self._children._childrenSizeChanged.disconnect(self._sizeChangedHandler)
        self._children = None
        self._setDefaultIcon()
        return children

    def child(self, index:int) -> Optional[TTkTreeWidgetItem]:
        if not self._children:
            return None
        return self._children.child(index)

    def children(self) -> List[TTkTreeWidgetItem]:
        if not self._children:
            return []
        return self._children.children()

    def indexOfChild(self, child:TTkTreeWidgetItem) -> int:
        if not self._children:
            return -1
        try:
            return self._children.indexOfChild(child)
        except ValueError:
            return -1
        finally:
            return -1

    def icon(self, col:int) -> TTkString:
        if col >= len(self._icon):
            return TTkString()
        return self._icon[col]

    def setIcon(self, col:int, icon:TTkStringType) -> None:
        if col==0:
            self._defaultIcon = False
        if isinstance(icon,str):
            self._icon[col] = TTkString(' '+icon+' ')
        else:
            self._icon[col] = ' '+icon+TTkString(' ')
        self.dataChanged.emit()

    def textAlignment(self, col:int) -> TTkK.Alignment:
        if col >= len(self._alignment):
            return TTkK.LEFT_ALIGN
        return self._alignment[col]

    def setTextAlignment(self, col:int, alignment:TTkK.Alignment) -> None:
        self._alignment[col] = alignment
        self.dataChanged.emit()

    def data(self, col:int, role:Any=None) -> TTkString:
        if col >= len(self._data):
            return TTkString()
        return self._data[col]

    def widget(self, col:int, role:Any=None) -> Optional[TTkWidget]:
        if col >= len(self._data):
            return None
        return self._widgets[col]

    def expandAll(self) -> None:
        if self._children:
            self._children.expandAll()

    def collapseAll(self) -> None:
        if self._children:
            self._children.collapseAll()

    def sortChildren(self, col:int, order:TTkK.SortOrder) -> None:
        self._sortColumn = col
        self._sortOrder = order
        if not self._children:
            return
        self._children.sort()

    @pyTTkSlot()
    def emitDataChanged(self) -> None:
        self.dataChanged.emit()

    # def setDisabled(disabled):
    #    pass

    def setExpanded(self, expand:bool) -> None:
        if self._expanded != expand and self._children:
            if expand:
                self._sizeChangedHandler(self, self._children.size())
            else:
                self._sizeChangedHandler(self, -self._children.size())
        self._expanded = expand
        self._setDefaultIcon()
        self.dataChanged.emit()

    def setSelected(self, select:bool) -> None:
        self._selected = select

    # def isDisabled():
    #     pass

    def isExpanded(self) -> bool:
        return self._expanded

    def isSelected(self) -> bool:
        return self._selected

    def size(self) -> int:
        if self._hidden:
            return 0
        if ( self._expanded and
             self._children ):
            return self._height + self._children.size()
        return self._height
