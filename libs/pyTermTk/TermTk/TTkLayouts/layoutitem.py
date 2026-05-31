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

from typing import TYPE_CHECKING, Optional, Tuple

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.constant import TTkK

if TYPE_CHECKING:
    from TermTk.TTkWidgets.widget import TTkWidget


class TTkLayoutItem():
    ''' :py:class:`~TTkLayoutItem` is the base class of layout Items inherited by :py:class:`~TTkLayout`, :py:class:`~TTkWidgetItem`, and all the derived layout managers.

    :param int row:     (used only in the :py:class:`TTkGridLayout`), the row of the grid,   optional, defaults to None
    :param int col:     (used only in the :py:class:`TTkGridLayout`), the col of the grid,   optional, defaults to None
    :param int rowspan: (used only in the :py:class:`TTkGridLayout`), the rows used by this, optional, defaults to 1
    :param int colspan: (used only in the :py:class:`TTkGridLayout`), the cols used by this, optional, defaults to 1
    :param layoutItemType: The Type of this class, optional, defaults to TTkK.NONE
    :type  layoutItemType: :py:class:`TTkConstant.LayoutItemTypes`
    :param alignment: The alignment of this item in the layout (not yet used)
    :type  alignment: :py:class:`TTkConstant.Alignment`
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
        '_parent',
        '_layoutItemType')

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
                 **kwargs) -> None:
        if kwargs:
            TTkLog.warn(f"Unhandled init params {self.__class__.__name__} -> {kwargs}")

        self._x, self._y = pos  if pos  else (x,y)
        self._w, self._h = size if size else (width,height)
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
        self._maxw, self._maxh = maxSize if maxSize else (maxWidth,maxHeight)
        self._minw, self._minh = minSize if minSize else (minWidth,minHeight)
        self._parent = None

    def minimumSize(self):
        return self.minimumWidth(), self.minimumHeight()
    def minDimension(self,o)-> int: return self._minh if o == TTkK.HORIZONTAL else self._minw
    def minimumHeight(self) -> int: return self._minh
    def minimumWidth(self)  -> int: return self._minw

    def maximumSize(self):
        return self.maximumWidth(), self.maximumHeight()
    def maxDimension(self,o)-> int: return self._maxh if o == TTkK.HORIZONTAL else self._maxw
    def maximumHeight(self) -> int: return self._maxh
    def maximumWidth(self)  -> int: return self._maxw

    @staticmethod
    def _calcSpanValue(value, pos, curpos, span):
        if pos==curpos:
            return value - (value//span) * (span-1)
        else:
            return value//span

    def minimumHeightSpan(self,pos) -> int:
        return TTkLayoutItem._calcSpanValue(self.minimumHeight(),pos,self._row,self._rowspan)
    def minimumWidthSpan(self,pos)  -> int:
        return TTkLayoutItem._calcSpanValue(self.minimumWidth(), pos,self._col,self._colspan)
    def maximumHeightSpan(self,pos) -> int:
        return TTkLayoutItem._calcSpanValue(self.maximumHeight(),pos,self._row,self._rowspan)
    def maximumWidthSpan(self,pos)  -> int:
        return TTkLayoutItem._calcSpanValue(self.maximumWidth(), pos,self._col,self._colspan)

    def offset(self):   return self._xOffset, self._yOffset
    def pos(self):      return self._x, self._y
    def size(self):     return self._w, self._h
    def geometry(self): return self._x, self._y, self._w, self._h

    def setOffset(self, x, y):
        '''setOffset'''
        self._xOffset = x
        self._yOffset = y

    def setGeometry(self, x, y, w, h):
        '''setGeometry'''
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def parent(self):
        '''parent'''
        return self._parent

    def setParent(self, parent):
        '''setParent'''
        self._parent = parent

    def layer(self):
        '''layer'''
        return self._layer

    def setLayer(self, layer):
        '''setLayer'''
        self._layer = layer
        self._z = (self._z & TTkLayoutItem.LAYERMASK) | layer

    def layoutItemType(self) -> TTkK.LayoutItemTypes:
        raise NotImplementedError()


class TTkWidgetItem(TTkLayoutItem):
    __slots__ = ('_widget',)
    _widget:TTkWidget
    def __init__(self, *,
                 widget,
                 **kwargs) -> None:
        TTkLayoutItem.__init__(self, **kwargs)
        self._widget = widget

    def widget(self) -> TTkWidget:
        return self._widget

    def isVisible(self): return self._widget.isVisible()

    def isEmpty(self): return self._widget is None

    def minimumSize(self)   -> Tuple[int,int]: return self._widget.minimumSize()
    def minDimension(self,o)-> int: return self._widget.minDimension(o)
    def minimumHeight(self) -> int: return self._widget.minimumHeight()
    def minimumWidth(self)  -> int: return self._widget.minimumWidth()
    def maximumSize(self)   -> Tuple[int,int]: return self._widget.maximumSize()
    def maxDimension(self,o)-> int: return self._widget.maxDimension(o)
    def maximumHeight(self) -> int: return self._widget.maximumHeight()
    def maximumWidth(self)  -> int: return self._widget.maximumWidth()

    def pos(self):      return self._widget.pos()
    def size(self):     return self._widget.size()
    def geometry(self): return self._widget.geometry()

    def setGeometry(self, x, y, w, h):
        self._widget.setGeometry(x, y, w, h)

    def layoutItemType(self) -> TTkK.LayoutItemTypes:
        return TTkK.LayoutItemTypes.WidgetItem