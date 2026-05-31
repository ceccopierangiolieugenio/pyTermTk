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
        TTkLayoutItem.__init__(self, **kwargs)
        self._items = []
        self._zSortedItems = []

    def children(self):
        return self._items

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if index < len(self._items):
            return self._items[index]
        return None

    def setParent(self, parent):
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
        self._zSortedItems = sorted(self._items, key=lambda item: item._z)

    @property
    def zSortedItems(self): return self._zSortedItems

    def replaceItem(self, item, index):
        if index < 0 or index >= len(self._items):
            raise ValueError(f"The {index=} is not inside the items list")
        self.removeItem(item=self._items[index])
        self.insertItem(item=item,index=index)

    def addItem(self, item):
        self.insertItems(len(self._items),[item])

    def addItems(self, items):
        self.insertItems(len(self._items),items)

    def insertItem(self, index, item):
        return self.insertItems(index,[item])

    def insertItems(self, index, items):
        for i,item in enumerate(items):
            if not isinstance(widget:=item, TTkLayoutItem):
                if widget.parentWidget() and widget.parentWidget().layout():
                    widget.parentWidget().layout().removeWidget(self)
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
        '''insertWidget'''
        self.insertItems(index, [widget])

    def insertWidgets(self, index, widgets):
        '''insertWidgets'''
        self.insertItems(index, widgets)

    def removeItem(self, item):
        '''removeItem'''
        self.removeItems([item])

    def clear(self) -> None:
        '''clear'''
        for item in self._items:
            if isinstance(item, TTkWidgetItem):
                item.widget().setParent(None)
            item.setParent(None)
        self._items = []
        self._zSortItems()

    def removeItems(self, items):
        '''removeItems'''
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
        for item in self._items:
            if isinstance(item, TTkLayout):
                if item._findBranchWidget(widget) is not None:
                    return item
            else:
                if item.widget() == widget:
                    return item
        return None

    def raiseWidget(self, widget):
        '''raiseWidget'''
        item = self._findBranchWidget(widget)
        item._z = item._z if (maxz:=max(TTkLayoutItem.LAYERMASK & i._z for i in self._items))==(TTkLayoutItem.LAYERMASK & item._z)!=0 else item._layer|maxz+1
        if isinstance(item, TTkLayout):
            item.raiseWidget(widget)
        self._zSortItems()

    def lowerWidget(self, widget):
        '''lowerWidget'''
        item = self._findBranchWidget(widget)
        for i in self._items: i._z+=1
        item._z = item._layer
        if isinstance(item, TTkLayout):
            item.lowerWidget(widget)
        self._zSortItems()

    def setGeometry(self, x, y, w, h):
        '''setGeometry'''
        ax, ay, aw, ah = self.geometry()
        if ax==x and ay==y and aw==w and ah==h: return
        TTkLayoutItem.setGeometry(self, x, y, w, h)
        self.update(repaint=True, updateLayout=True)

    def fullWidgetAreaGeometry(self):
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
        for i in self._items:
            if isinstance(i, TTkWidgetItem) and (_wid:=i._widget):
                _wid.update(*args, **kwargs)
            elif isinstance(i, TTkLayout):
                i.update(*args, **kwargs)

    def layoutItemType(self) -> TTkK.LayoutItemTypes:
        return TTkK.LayoutItemTypes.LayoutItem
