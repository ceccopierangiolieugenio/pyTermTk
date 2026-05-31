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

'''
**Layout** [:ref:`Tutorial <Layout-Tutorial_Intro>`]
'''

from __future__ import annotations

__all__ = ['TTkLayoutItem', 'TTkLayout', 'TTkWidgetItem']

from typing import TYPE_CHECKING, Generator, List

from TermTk.TTkCore.constant import TTkK

from .layoutitem import TTkLayoutItem, TTkWidgetItem

if TYPE_CHECKING:
    from TermTk.TTkWidgets.widget import TTkWidget

class TTkLayout(TTkLayoutItem):
    '''
    | The :py:class:`TTkLayout` class is the base class of geometry managers. <br/>
    | It allows free placement of the widgets in the layout area. <br/>
    | Used mainly to have free range moving :py:class:`TTkWindow` because the widgets are not automatically rearranged after a layout event

    ::

        ╔════════════════════════════╗
        ║   pos(4,2)                 ║
        ║   ┌───────┐   pos(16,4)    ║
        ║   │Widget1│   ┌─────────┐  ║
        ║   │       │   │ Widget2 │  ║
        ║   │       │   └─────────┘  ║
        ║   │       │                ║
        ║   └───────┘                ║
        ║                            ║
        ╚════════════════════════════╝
    '''
    __slots__ = ('_items', '_zSortedItems')
    _items:List[TTkLayoutItem]
    _zSortedItems:List[TTkLayoutItem]
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._items = []
        self._zSortedItems = []

    def children(self):
        '''Return the list of direct child layout items.'''
        return self._items

    def count(self):
        '''Return the number of direct child layout items.'''
        return len(self._items)

    def itemAt(self, index):
        '''Return the item at ``index`` or ``None`` when out of range.

        :param index: child index
        :type index: int
        :return: the layout item at ``index`` if available
        :rtype: :py:class:`TTkLayoutItem` or None
        '''
        if index < len(self._items):
            return self._items[index]
        return None

    def setParent(self, parent):
        '''Set the parent layout item and propagate parent widget ownership.

        :param parent: parent layout item or widget-like owner
        :type parent: object
        '''
        if parent is None:
            self._parent = parent
        elif isinstance(parent, TTkLayoutItem):
            self._parent = parent
        else:
            self._parent = parent.widgetItem()
        for item in self._items:
            item.setParent(self)
            if isinstance(item, TTkWidgetItem):
                item.widget().setParent(self.parentWidget())

    def parentWidget(self):
        '''Return the widget owning this layout branch.

        :return: nearest parent widget in the hierarchy
        :rtype: :py:class:`TTkWidget` or None
        '''
        parent = self._parent
        if parent is None: return None
        if isinstance(parent, TTkWidgetItem):
            return parent.widget()
        else:
            return parent.parentWidget()

    def iterWidgets(
            self,
            onlyVisible: bool = True,
            recurse: bool = True,
            reverse: bool = False) -> Generator[TTkWidget, None, None]:
        '''
        Iterate over all widgets in the layout.

        :param onlyVisible: if True, only yield visible widgets
        :type onlyVisible: bool
        :param recurse: if True, recursively iterate through nested layouts
        :type recurse: bool
        :param reverse: if True, iterate in reverse order
        :type reverse: bool

        :return: generator yielding widgets
        :rtype: Generator[:py:class:`TTkWidget`, None, None]
        '''
        items = reversed(self._items) if reverse else self._items
        for child in items:
            if isinstance(child, TTkWidgetItem):
                if onlyVisible and not child.widget().isVisible(): continue
                yield child.widget()
            if recurse and isinstance(child, TTkLayout):
                yield from child.iterWidgets(onlyVisible, recurse)

    def _zSortItems(self):
        '''Sort child items by z-order and cache the sorted list.'''
        self._zSortedItems = sorted(self._items, key=lambda item: item._z)

    @property
    def zSortedItems(self):
        '''Return child items sorted by z-order.'''
        return self._zSortedItems

    def replaceItem(self, item, index):
        '''Replace the item at ``index`` with ``item``.

        :param item: replacement item
        :type item: :py:class:`TTkLayoutItem`
        :param index: target index to replace
        :type index: int
        :raises ValueError: if ``index`` is outside the valid range
        '''
        if index < 0 or index >= len(self._items):
            raise ValueError(f"The {index=} is not inside the items list")
        self.removeItem(item=self._items[index])
        self.insertItem(item=item,index=index)

    def addItem(self, item):
        '''Append a layout item.

        :param item: item to append
        :type item: :py:class:`TTkLayoutItem`
        '''
        self.insertItems(len(self._items),[item])

    def addItems(self, items):
        '''Append multiple layout items.

        :param items: items to append
        :type items: list[:py:class:`TTkLayoutItem`]
        '''
        self.insertItems(len(self._items),items)

    def insertItem(self, index, item):
        '''Insert a single item at ``index``.

        :param index: insertion index
        :type index: int
        :param item: item to insert
        :type item: :py:class:`TTkLayoutItem`
        '''
        return self.insertItems(index,[item])

    def insertItems(self, index, items):
        '''Insert multiple items at ``index`` and re-parent them.

        Widgets passed directly are converted to their associated
        :py:class:`TTkWidgetItem` wrapper before insertion.

        :param index: insertion index
        :type index: int
        :param items: items or widgets to insert
        :type items: list
        '''
        for i,item in enumerate(items):
            if not isinstance(widget:=item, TTkLayoutItem):
                parent_widget = widget.parentWidget()
                if parent_widget and parent_widget.layout():
                    parent_widget.layout().removeWidget(widget)
                item = widget.widgetItem()
                items[i]=item
        self._items[index:index] = items
        self._zSortItems()
        #self.update()
        parent_widget = self.parentWidget()
        for item in items:
            item.setParent(self)
            if isinstance(item, TTkWidgetItem):
                item.widget().setParent(parent_widget)
        if parent_widget and parent_widget.isVisible():
            parent_widget.update(repaint=True, updateLayout=True)
        self.update()

    def addWidget(self, widget):
        ''' Add a widget to this Layout

        :param widget: the widget to be added
        :type widget: :py:class:`TTkWidgets`
        '''
        self.insertItems(len(self._items),[widget])

    def addWidgets(self, widgets):
        ''' Add a list of widgets to this Layout

        :param widgets: the widget to be added
        :type widgets: list of :py:class:`TTkWidgets`
        '''
        self.insertItems(len(self._items),widgets)

    def insertWidget(self, index, widget):
        '''Insert a widget at ``index``.

        :param index: insertion index
        :type index: int
        :param widget: widget to insert
        :type widget: :py:class:`TTkWidgets`
        '''
        self.insertItems(index, [widget])

    def insertWidgets(self, index, widgets):
        '''Insert widgets at ``index``.

        :param index: insertion index
        :type index: int
        :param widgets: widgets to insert
        :type widgets: list of :py:class:`TTkWidgets`
        '''
        self.insertItems(index, widgets)

    def removeItem(self, item):
        '''Remove a single layout item.

        :param item: item to remove
        :type item: :py:class:`TTkLayoutItem`
        '''
        self.removeItems([item])

    def clear(self) -> None:
        '''Remove and detach all items from this layout.'''
        for item in self._items:
            if isinstance(item, TTkWidgetItem):
                item.widget().setParent(None)
            item.setParent(None)
        self._items = []
        self._zSortItems()

    def removeItems(self, items):
        '''Remove a list of layout items if present.

        :param items: items to remove
        :type items: list[:py:class:`TTkLayoutItem`]
        '''
        for item in items.copy():
            if item in self._items:
                self._items.remove(item)
                if isinstance(item, TTkWidgetItem):
                    item.widget().setParent(None)
                item.setParent(None)
        self._zSortItems()

    def removeWidget(self, widget):
        ''' Remove a widget from this Layout

        :param widget: the widget to be removed
        :type widget: :py:class:`TTkWidgets`
        '''
        self.removeWidgets([widget])

    def removeWidgets(self, widgets):
        ''' Remove a list of widget from this Layout

        :param widgets: the widget to be removed
        :type widgets: list of :py:class:`TTkWidgets`
        '''
        for item in reversed(self._items):
            if isinstance(item, TTkWidgetItem):
               if item.widget() in widgets:
                    self.removeItem(item)
            elif isinstance(item, TTkLayout):
                item.removeWidgets(widgets)

    def _findBranchWidget(self, widget):
        '''Find the direct branch item containing ``widget``.

        :param widget: widget to search in the layout tree
        :type widget: :py:class:`TTkWidget`
        :return: direct child branch that contains the widget
        :rtype: :py:class:`TTkLayoutItem` or None
        '''
        for item in self._items:
            if isinstance(item, TTkLayout):
                if item._findBranchWidget(widget) is not None:
                    return item
            else:
                if item.widget() == widget:
                    return item
        return None

    def raiseWidget(self, widget):
        '''Raise a widget (and its branch) to the top z-order.

        :param widget: widget to raise
        :type widget: :py:class:`TTkWidget`
        '''
        item = self._findBranchWidget(widget)
        item._z = item._z if (maxz:=max(TTkLayoutItem.LAYERMASK & i._z for i in self._items))==(TTkLayoutItem.LAYERMASK & item._z)!=0 else item._layer|maxz+1
        if isinstance(item, TTkLayout):
            item.raiseWidget(widget)
        self._zSortItems()

    def lowerWidget(self, widget):
        '''Lower a widget (and its branch) to the bottom z-order.

        :param widget: widget to lower
        :type widget: :py:class:`TTkWidget`
        '''
        item = self._findBranchWidget(widget)
        for i in self._items: i._z+=1
        item._z = item._layer
        if isinstance(item, TTkLayout):
            item.lowerWidget(widget)
        self._zSortItems()

    def setGeometry(self, x, y, w, h):
        '''Set layout geometry and propagate a layout update when changed.

        :param x: horizontal position
        :type x: int
        :param y: vertical position
        :type y: int
        :param w: width
        :type w: int
        :param h: height
        :type h: int
        '''
        ax, ay, aw, ah = self.geometry()
        if ax==x and ay==y and aw==w and ah==h: return
        TTkLayoutItem.setGeometry(self, x, y, w, h)
        self.update(repaint=True, updateLayout=True)

    def fullWidgetAreaGeometry(self):
        '''Return the bounding geometry that encloses all child items.

        :return: ``(x, y, width, height)`` bounding box
        :rtype: tuple[int, int, int, int]
        '''
        if not self._items: return 0,0,0,0
        minx,miny,maxx,maxy = 0x10000,0x10000,-0x10000,-0x10000
        for item in self._items:
            x,y,w,h = item.geometry()
            minx = min(minx,x)
            miny = min(miny,y)
            maxx = max(maxx,x+w)
            maxy = max(maxy,y+h)
        return minx, miny, maxx-minx, maxy-miny

    def update(self, *args, **kwargs) -> None:
        '''Propagate update requests to child widgets and nested layouts.'''
        for i in self._items:
            if isinstance(i, TTkWidgetItem) and (_wid:=i._widget):
                _wid.update(*args, **kwargs)
            elif isinstance(i, TTkLayout):
                i.update(*args, **kwargs)

    def layoutItemType(self) -> TTkK.LayoutItemTypes:
        '''Return :py:attr:`TTkK.LayoutItemTypes.LayoutItem`.'''
        return TTkK.LayoutItemTypes.LayoutItem
