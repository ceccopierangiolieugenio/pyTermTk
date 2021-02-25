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

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkLayouts.boxlayout import TTkHBoxLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.spacer import TTkSpacer
from TermTk.TTkWidgets.scrollbar import TTkScrollBar

'''


'''
class TTkTable(TTkWidget):
    __slots__ = ('_hlayout','_vscroller', '_header', '_alignments', '_headerColor', '_columns', '_columnColors', '_selectColor', '_tableData', '_moveTo', '_selected')
    def __init__(self, *args, **kwargs):
        self._vscroller = None # This is required to avoid crash int he vScroller Tuning
        self._moveTo = 0
        self._tableData = []
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTable' )
        self._columns = kwargs.get('columns' , [] )
        self._header = [""]*len(self._columns)
        self._alignments = [TTkK.NONE]*len(self._columns)
        self._columnColors = kwargs.get('columnColors' , [TTkColor.RST]*len(self._columns) )
        self._selectColor = kwargs.get('selectColor' , TTkColor.BOLD )
        self._headerColor = kwargs.get('headerColor' , TTkColor.BOLD )
        self._hlayout = TTkHBoxLayout()
        self.setLayout(self._hlayout)
        self._selected = -1
        TTkSpacer(parent=self)
        self._vscroller = TTkScrollBar(parent=self)
        self._vscroller.valueChanged.connect(self.scrollTo)
        self.setFocusPolicy(TTkWidget.ClickFocus)

    def setAlignment(self, alignments):
        if len(alignments) != len(self._columns):
            return
        self._alignments = alignments

    def setHeader(self, header):
        if len(header) != len(self._columns):
            return
        self._header = header

    def setColumnSize(self, columns):
        self._columns = columns
        self._columnColors = [TTkColor.RST]*len(self._columns)
        self._header = [""]*len(self._columns)
        self._alignments = [TTkK.NONE]*len(self._columns)

    def setColumnColors(self, colors):
        if len(colors) != len(self._columns):
            return
        self._columnColors = colors

    def appendItem(self, item):
        if len(item) != len(self._columns):
            return
        self._tableData.append(item)
        self._tuneTheScroller()

    def resizeEvent(self, w, h):
        if self._moveTo > len(self._tableData)-h-1:
            self._moveTo = len(self._tableData)-h-1
        if self._moveTo < 0:
            self._moveTo = 0
        self._tuneTheScroller()

    def _tuneTheScroller(self):
        if self._vscroller is None: return
        scrollTo = len(self._tableData) - self.height()
        self._vscroller.setRange(0, scrollTo)
        self._vscroller.pagestep = self.height()

    def mousePressEvent(self, evt):
        x,y = evt.x, evt.y
        if x == self.width() - 1:
            return False
        if y > 0:
            self._selected = self._moveTo + y - 1
            self.update()
        return True

    def wheelEvent(self, evt):
        # delta = self.height()
        delta = 5
        if evt.evt == TTkK.WHEEL_Up:
            delta = -delta
        # self.scrollTo(self._moveTo + delta)
        self._vscroller.value = self._moveTo + delta
        return True

    @pyTTkSlot(int)
    def scrollTo(self, to):
        max = len(self._tableData) - self.height()
        if to>max: to=max
        if to<0: to=0
        self._moveTo = to
        self.update()

    def paintEvent(self):
        w,h = self.size()
        total = 0
        variableCols = 0
        slicesize = 0
        for width in self._columns:
            if width > 0:
                total += width
            else:
                variableCols += 1
        if variableCols > 0:
            slicesize = int((w-total)/variableCols)
        # TTkLog.debug(f"ss:{slicesize}, w:{w}")

        maxItems = len(self._tableData)
        itemFrom = self._moveTo -1
        if itemFrom > maxItems-h: itemFrom = maxItems-h
        if itemFrom < 0 : itemFrom = 0
        itemTo   = itemFrom + h
        if itemTo > maxItems: itemTo = maxItems
        # TTkLog.debug(f"moveto:{self._moveTo}, maxItems:{maxItems}, f:{itemFrom}, t{itemTo}, h:{h}, sel:{self._selected}")

        def _lineDraw(_y, _val, _item, _inColor=None):
            _x = 0
            for i in range(0,len(_item)):
                _txt = _item[i]
                _width = self._columns[i]
                _color = self._columnColors[i]
                _align = self._alignments[i]
                if _inColor is not None:
                    _color = _inColor
                if _width < 0:
                    _width = slicesize
                if _width > 0:
                    _line = ""
                    _lentxt = len(_txt)
                    if _lentxt > _width:
                        _line += _txt[0:_width]
                    else:
                        _pad = _width-_lentxt
                        if _align == TTkK.NONE or _align == TTkK.LEFT_ALIGN:
                            _line += _txt + " "*_pad
                        elif _align == TTkK.RIGHT_ALIGN:
                            _line += " "*_pad + _txt
                        elif _align == TTkK.CENTER_ALIGN:
                            _p1 = _pad//2
                            _p2 = _pad-_p1
                            _line += " "*_p1 + _txt+" "*_p2
                        elif _align == TTkK.JUSTIFY:
                            # TODO: Text Justification
                            _line += _txt + " "*_pad
                    self._canvas.drawText(pos=(_x,_y), text=_line, color=_color.modParam(val=-_val))
                    _line  += " "
                    _x += _width + 1

        _lineDraw(0,0,self._header,self._headerColor)

        y = 1
        for it in range(itemFrom, itemTo):
            item =  self._tableData[it]
            if self._selected > 0:
                val = self._selected - itemFrom
            else:
                val = h//2
            if val < 0 : val = 0
            if val > h : val = h
            if it == self._selected:
                _lineDraw(y,val,item,self._selectColor)
            else:
                _lineDraw(y,val,item)
            y+=1





