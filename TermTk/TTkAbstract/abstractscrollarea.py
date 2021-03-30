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

from TermTk.TTkCore.constant import TTkConstant, TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.scrollbar import TTkScrollBar
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class TTkAbstractScrollArea(TTkWidget):
    __slots__ = (
        '_viewport',
        '_verticalScrollBar',   '_verticalScrollBarPolicy',
        '_horizontalScrollBar', '_horizontalScrollBarPolicy',)

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkAbstractScrollArea')
        self.setLayout(TTkGridLayout())
        self._verticalScrollBar = TTkScrollBar(orientation=TTkK.VERTICAL)
        self._horizontalScrollBar = TTkScrollBar(orientation=TTkK.HORIZONTAL)
        self._verticalScrollBarPolicy = TTkK.ScrollBarAsNeeded
        self._horizontalScrollBarPolicy = TTkK.ScrollBarAsNeeded

    @pyTTkSlot()
    def _viewportChanged(self):
        if not self.isVisible(): return
        fw, fh = self._viewport.viewFullAreaSize()
        dw, dh = self._viewport.viewDisplayedSize()
        ox, oy = self._viewport.getViewOffsets()
        if 0 in [fw,fh,dw,dh]:
            return
        hpage = dw
        vpage = dh
        hrange = fw - dw
        vrange = fh - dh
        # TTkLog.debug(f"f:{fw,fh}, d:{dw,dh}, o:{ox,oy}")
        self._verticalScrollBar.setPageStep(vpage)
        self._verticalScrollBar.setRange(0, vrange)
        self._verticalScrollBar.setValue(oy)
        self._horizontalScrollBar.setPageStep(hpage)
        self._horizontalScrollBar.setRange(0, hrange)
        self._horizontalScrollBar.setValue(ox)

        if self._verticalScrollBarPolicy == TTkK.ScrollBarAsNeeded:
            if vrange<=0:
                self._verticalScrollBar.hide()
            elif dh>self._verticalScrollBar.minimumHeight()+1:
                # we need enough space to display the bar to avoid endless loop
                self._verticalScrollBar.show()
        elif self._verticalScrollBarPolicy == TTkK.ScrollBarAlwaysOn:
            self._verticalScrollBar.show()
        else:
            self._verticalScrollBar.show()

        if self._horizontalScrollBarPolicy == TTkK.ScrollBarAsNeeded:
            if hrange<=0:
                self._horizontalScrollBar.hide()
            elif dw>self._horizontalScrollBar.minimumWidth()+1:
                # we need enough space to display the bar to avoid endless loop
                self._horizontalScrollBar.show()
        elif self._horizontalScrollBarPolicy == TTkK.ScrollBarAlwaysOn:
            self._horizontalScrollBar.show()
        else:
            self._horizontalScrollBar.show()

    @pyTTkSlot(int)
    def _vscrollMoved(self, val):
        ox, _ = self._viewport.getViewOffsets()
        self._viewport.viewMoveTo(ox, val)

    @pyTTkSlot(int)
    def _hscrollMoved(self, val):
        _, oy = self._viewport.getViewOffsets()
        self._viewport.viewMoveTo(val, oy)

    def setViewport(self, viewport):
        if not isinstance(viewport, TTkAbstractScrollView):
            raise TypeError("TTkAbstractScrollView is required in TTkAbstractScrollArea.setVewport(viewport)")
        self._viewport = viewport
        self._viewport.viewChanged.connect(self._viewportChanged)
        self._verticalScrollBar.sliderMoved.connect(self._vscrollMoved)
        self._horizontalScrollBar.sliderMoved.connect(self._hscrollMoved)
        self.layout().addWidget(viewport,0,0)
        self.layout().addWidget(self._verticalScrollBar,0,1)
        self.layout().addWidget(self._horizontalScrollBar,1,0)

    def setVerticalScrollBarPolicy(self, policy):
        self._verticalScrollBarPolicy = policy

    def setHorizontalScrollBarPolicy(self, policy):
        self._horizontalScrollBarPolicy = policy

    def viewport(self):
        return self._viewport
