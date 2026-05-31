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
**Layout Item** [:ref:`Tutorial <Layout-Tutorial_Intro>`]
'''

from __future__ import annotations

__all__ = ['TTkLayoutItem', 'TTkWidgetItem']

from typing import TYPE_CHECKING, Any, Optional, Tuple

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK

if TYPE_CHECKING:
    from TermTk.TTkWidgets.widget import TTkWidget


class TTkLayoutItem():
    ''' :py:class:`~TTkLayoutItem` is the base class of layout Items inherited by :py:class:`~TTkLayout`, :py:class:`~TTkWidgetItem`, and all the derived layout managers.

    :param int row:     (used only in the :py:class:`TTkGridLayout`), the row of the grid,   optional, defaults to 0
    :param int col:     (used only in the :py:class:`TTkGridLayout`), the col of the grid,   optional, defaults to 0
    :param int rowspan: (used only in the :py:class:`TTkGridLayout`), the rows used by this, optional, defaults to 1
    :param int colspan: (used only in the :py:class:`TTkGridLayout`), the cols used by this, optional, defaults to 1
    '''

    LAYER0    =  0x00000000
    LAYER1    =  0x40000000
    LAYER2    =  0x80000000
    LAYER3    =  0xC0000000
    LAYERMASK = ~(LAYER0 | LAYER1 | LAYER2 | LAYER3)

    __slots__ = (
        '_x', '_y', '_z', '_w', '_h',
        '_layer',
        '_xOffset', '_yOffset',
        '_maxw', '_maxh', '_minw', '_minh',
        '_row','_col',
        '_rowspan', '_colspan',
        '_sMax', '_sMaxVal',
        '_sMin', '_sMinVal',
        '_parent')

    _x: int
    _y: int
    _z: int
    _w: int
    _h: int
    _layer: int
    _xOffset: int
    _yOffset: int
    _maxw: int
    _maxh: int
    _minw: int
    _minh: int
    _row: int
    _col: int
    _rowspan: int
    _colspan: int
    _sMax: bool
    _sMaxVal: int
    _sMin: bool
    _sMinVal: int
    _parent: Optional[TTkLayoutItem]

    def __init__(self, *,
                 x:int=0,
                 y:int=0,
                 z:int=0,
                 pos:Optional[Tuple[int,int]]=None,
                 width:int=0,
                 height:int=0,
                 size:Optional[Tuple[int,int]]=None,
                 row:int=0,
                 col:int=0,
                 rowspan:int=1,
                 colspan:int=1,
                 maxWidth:int=0x10000,
                 maxHeight:int=0x10000,
                 maxSize:Optional[Tuple[int,int]]=None,
                 minWidth:int=0,
                 minHeight:int=0,
                 minSize:Optional[Tuple[int,int]]=None,
                 **kwargs: Any) -> None:
        if kwargs:
            TTkLog.warn(f"Unhandled init params {self.__class__.__name__} -> {kwargs}")

        self._x, self._y = pos  if pos is not None  else (x,y)
        self._w, self._h = size if size is not None else (width,height)
        self._z = z
        self._layer = TTkLayoutItem.LAYER0
        self._xOffset = 0
        self._yOffset = 0
        self._row = row
        self._col = col
        self._rowspan = rowspan
        self._colspan = colspan
        self._sMax,    self._sMin    = False, False
        self._sMaxVal, self._sMinVal = 0, 0
        self._maxw, self._maxh = maxSize if maxSize is not None else (maxWidth,maxHeight)
        self._minw, self._minh = minSize if minSize is not None else (minWidth,minHeight)
        self._parent = None

    def minimumSize(self) -> Tuple[int,int]:
        '''Return the minimum size as ``(width, height)``.'''
        return self.minimumWidth(), self.minimumHeight()
    def minDimension(self, o: int) -> int:
        '''Return minimum size along an orientation.

        :param o: orientation constant
        :type o: int
        :return: minimum size for the requested orientation
        :rtype: int
        '''
        return self._minh if o == TTkK.HORIZONTAL else self._minw
    def minimumHeight(self) -> int:
        '''Return the minimum allowed height.'''
        return self._minh
    def minimumWidth(self)  -> int:
        '''Return the minimum allowed width.'''
        return self._minw

    def maximumSize(self) -> Tuple[int,int]:
        '''Return the maximum size as ``(width, height)``.'''
        return self.maximumWidth(), self.maximumHeight()
    def maxDimension(self, o: int) -> int:
        '''Return maximum size along an orientation.

        :param o: orientation constant
        :type o: int
        :return: maximum size for the requested orientation
        :rtype: int
        '''
        return self._maxh if o == TTkK.HORIZONTAL else self._maxw
    def maximumHeight(self) -> int:
        '''Return the maximum allowed height.'''
        return self._maxh
    def maximumWidth(self)  -> int:
        '''Return the maximum allowed width.'''
        return self._maxw

    @staticmethod
    def _calcSpanValue(value: int, pos: int, curpos: int, span: int) -> int:
        '''Split ``value`` across ``span`` cells preserving the original total.

        The first occupied cell gets the remainder so that the sum of all
        returned chunks equals ``value``.
        '''
        if pos==curpos:
            return value - (value//span) * (span-1)
        else:
            return value//span

    def minimumHeightSpan(self, pos: int) -> int:
        '''Return the minimum height contribution for a grid row.

        :param pos: row index being queried
        :type pos: int
        :return: minimum height for this row slice
        :rtype: int
        '''
        return TTkLayoutItem._calcSpanValue(self.minimumHeight(),pos,self._row,self._rowspan)
    def minimumWidthSpan(self, pos: int)  -> int:
        '''Return the minimum width contribution for a grid column.

        :param pos: column index being queried
        :type pos: int
        :return: minimum width for this column slice
        :rtype: int
        '''
        return TTkLayoutItem._calcSpanValue(self.minimumWidth(), pos,self._col,self._colspan)
    def maximumHeightSpan(self, pos: int) -> int:
        '''Return the maximum height contribution for a grid row.

        :param pos: row index being queried
        :type pos: int
        :return: maximum height for this row slice
        :rtype: int
        '''
        return TTkLayoutItem._calcSpanValue(self.maximumHeight(),pos,self._row,self._rowspan)
    def maximumWidthSpan(self, pos: int)  -> int:
        '''Return the maximum width contribution for a grid column.

        :param pos: column index being queried
        :type pos: int
        :return: maximum width for this column slice
        :rtype: int
        '''
        return TTkLayoutItem._calcSpanValue(self.maximumWidth(), pos,self._col,self._colspan)

    def offset(self) -> Tuple[int, int]:
        '''Return the item offset as ``(xOffset, yOffset)``.'''
        return self._xOffset, self._yOffset
    def pos(self) -> Tuple[int, int]:
        '''Return the item position as ``(x, y)``.'''
        return self._x, self._y
    def size(self) -> Tuple[int, int]:
        '''Return the item size as ``(width, height)``.'''
        return self._w, self._h
    def geometry(self) -> Tuple[int, int, int, int]:
        '''Return the item geometry as ``(x, y, width, height)``.'''
        return self._x, self._y, self._w, self._h

    def setOffset(self, x: int, y: int) -> None:
        '''Set the item offset.

        :param x: horizontal offset
        :type x: int
        :param y: vertical offset
        :type y: int
        '''
        self._xOffset = x
        self._yOffset = y

    def setGeometry(self, x: int, y: int, w: int, h: int) -> None:
        '''Set item geometry.

        :param x: horizontal position
        :type x: int
        :param y: vertical position
        :type y: int
        :param w: width
        :type w: int
        :param h: height
        :type h: int
        '''
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def parent(self) -> Optional[TTkLayoutItem]:
        '''Return the parent layout item/container.'''
        return self._parent

    def setParent(self, parent: Optional[TTkLayoutItem]) -> None:
        '''Set the parent layout item/container.

        :param parent: parent object in the layout hierarchy
        :type parent: object
        '''
        self._parent = parent

    def layer(self) -> int:
        '''Return the current layer flag.'''
        return self._layer

    def setLayer(self, layer: int) -> None:
        '''Set the layer and update the packed z-order layer bits.

        :param layer: one of the ``TTkLayoutItem.LAYER*`` constants
        :type layer: int
        '''
        self._layer = layer
        self._z = (self._z & TTkLayoutItem.LAYERMASK) | layer

    def layoutItemType(self) -> TTkK.LayoutItemTypes:
        '''Return the layout item type.

        .. deprecated:: 0.50.0
            Prefer using ``isinstance(item, TTkLayout)`` or
            ``isinstance(item, TTkWidgetItem)`` for type checks.
        '''
        raise NotImplementedError()


class TTkWidgetItem(TTkLayoutItem):
    '''Layout item wrapper for a single :py:class:`TTkWidget` instance.'''
    __slots__ = ('_widget',)
    _widget: TTkWidget
    def __init__(self, *,
                 widget: TTkWidget,
                 **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._widget = widget

    def widget(self) -> TTkWidget:
        '''Return the wrapped widget.'''
        return self._widget

    def isVisible(self) -> bool:
        '''Return ``True`` when the wrapped widget is visible.'''
        return self._widget.isVisible()

    def isEmpty(self) -> bool:
        '''Return ``True`` when no widget is associated with this item.'''
        return self._widget is None

    def minimumSize(self)   -> Tuple[int,int]:
        '''Return the wrapped widget minimum size.'''
        return self._widget.minimumSize()
    def minDimension(self, o: int) -> int:
        '''Return wrapped widget minimum size along an orientation.'''
        return self._widget.minDimension(o)
    def minimumHeight(self) -> int:
        '''Return wrapped widget minimum height.'''
        return self._widget.minimumHeight()
    def minimumWidth(self)  -> int:
        '''Return wrapped widget minimum width.'''
        return self._widget.minimumWidth()
    def maximumSize(self)   -> Tuple[int,int]:
        '''Return the wrapped widget maximum size.'''
        return self._widget.maximumSize()
    def maxDimension(self, o: int) -> int:
        '''Return wrapped widget maximum size along an orientation.'''
        return self._widget.maxDimension(o)
    def maximumHeight(self) -> int:
        '''Return wrapped widget maximum height.'''
        return self._widget.maximumHeight()
    def maximumWidth(self)  -> int:
        '''Return wrapped widget maximum width.'''
        return self._widget.maximumWidth()

    def pos(self) -> Tuple[int, int]:
        '''Return the wrapped widget position as ``(x, y)``.'''
        return self._widget.pos()
    def size(self) -> Tuple[int, int]:
        '''Return the wrapped widget size as ``(width, height)``.'''
        return self._widget.size()
    def geometry(self) -> Tuple[int, int, int, int]:
        '''Return the wrapped widget geometry as ``(x, y, width, height)``.'''
        return self._widget.geometry()

    def setGeometry(self, x: int, y: int, w: int, h: int) -> None:
        '''Forward geometry updates to the wrapped widget.

        :param x: horizontal position
        :type x: int
        :param y: vertical position
        :type y: int
        :param w: width
        :type w: int
        :param h: height
        :type h: int
        '''
        self._widget.setGeometry(x, y, w, h)

    def layoutItemType(self) -> TTkK.LayoutItemTypes:
        '''Return :py:attr:`TTkK.LayoutItemTypes.WidgetItem`.'''
        return TTkK.LayoutItemTypes.WidgetItem