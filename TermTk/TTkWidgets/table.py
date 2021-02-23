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
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.layout import *
from TermTk.TTkWidgets.spacer import TTkSpacer
from TermTk.TTkWidgets.scrollbar import TTkScrollBar

'''


'''
class TTkTable(TTkWidget):
    __slots__ = ('_hlayout','_vscroller','_columns','_tableData', '_moveTo')
    def __init__(self, *args, **kwargs):
        self._vscroller = None # This is required to avoid crash int he vScroller Tuning
        self._moveTo = 0
        self._tableData = []
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTable' )
        self._columns = kwargs.get('columns' , 'TTkTable' )
        self._hlayout = TTkHBoxLayout()
        self.setLayout(self._hlayout)
        TTkSpacer(parent=self)
        self._vscroller = TTkScrollBar(parent=self)
        self._vscroller.valueChanged.connect(self.scrollTo)

    def setColumnSize(self, columns):
        self._columns = columns

    def appendItem(self, item):
        self._tableData.append(item)
        self._tuneTheScroller()

    def resizeEvent(self, w, h):
        if self._moveTo > len(self._tableData)-h:
            self._moveTo = len(self._tableData)-h
        self._tuneTheScroller()

    def _tuneTheScroller(self):
        if self._vscroller is None: return
        scrollTo = len(self._tableData) - self.height()
        self._vscroller.setRange(0, scrollTo)
        self._vscroller.pagestep = self.height()

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
        y = 0
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
        TTkLog.debug(f"ss:{slicesize}, w:{w}")

        maxItems = len(self._tableData)
        itemFrom = self._moveTo
        itemTo   = itemFrom + h
        if itemFrom > maxItems: itemFrom = maxItems
        if itemTo > maxItems: itemTo = maxItems
        for i in range(itemFrom, itemTo):
            item=  self._tableData[i]
            line = ""
            for i in range(0,len(item)):
                txt = item[i]
                width = self._columns[i]
                if width < 0:
                    width = slicesize
                if width > 0:
                    lentxt = len(txt)
                    if lentxt > width:
                        line += txt[0:width]
                    else:
                        line += txt + " "*(width-lentxt)
                    line += "  "
            lentxt = len(line)
            if lentxt > w-2:
                line = line[0:w-2]
            else:
                line = line + " "*(w-2-lentxt)
            self._canvas.drawText(pos=(0,y), text=line)
            y+=1





