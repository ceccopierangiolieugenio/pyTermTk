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

__all__ = ['TTkAbstractScrollArea']

from dataclasses import dataclass
from typing import List,Any,Type,Optional

from TermTk.TTkCore.constant import TTkK
# from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.scrollbar import TTkScrollBar
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollViewInterface

@dataclass
class _ForwardData():
    forwardClass: Type
    instance: str
    signals: List[str]
    methods: List[str]

class TTkAbstractScrollArea(TTkContainer):
    '''
    The :py:class:`TTkAbstractScrollArea` provides a scrolling area with on-demand scroll bars.

    This abstract class manages vertical and horizontal scroll bars that appear automatically
    based on the viewport size and content.
    '''
    __slots__ = (
        '_processing', # this flag is required to avoid unnecessary loop on edge cases
        '_viewport',
        '_verticalScrollBar',   '_verticalScrollBarPolicy',
        '_horizontalScrollBar', '_horizontalScrollBarPolicy',)

    _processing:bool
    _viewport:Optional[TTkAbstractScrollViewInterface]
    _verticalScrollBar:TTkScrollBar
    _horizontalScrollBar:TTkScrollBar
    _verticalScrollBarPolicy:TTkK.ScrollBarPolicy
    _horizontalScrollBarPolicy:TTkK.ScrollBarPolicy

    def __init__(self, *,
                 verticalScrollBarPolicy:TTkK.ScrollBarPolicy=TTkK.ScrollBarPolicy.ScrollBarAsNeeded,
                 horizontalScrollBarPolicy:TTkK.ScrollBarPolicy=TTkK.ScrollBarPolicy.ScrollBarAsNeeded,
                 **kwargs) -> None:
        self._processing = False
        self._viewport = None
        # self.setLayout(TTkGridLayout())
        self._verticalScrollBar = TTkScrollBar(orientation=TTkK.VERTICAL, visible=False)
        self._horizontalScrollBar = TTkScrollBar(orientation=TTkK.HORIZONTAL, visible=False)
        self._verticalScrollBarPolicy   = verticalScrollBarPolicy
        self._horizontalScrollBarPolicy = horizontalScrollBarPolicy
        super().__init__(**kwargs)
        self.layout().addWidget(self._verticalScrollBar)
        self.layout().addWidget(self._horizontalScrollBar)

    def _resizeEvent(self) -> None:
        ''' Internal method to handle resize events and reposition scroll bars '''
        if self._processing:
            return
        self._processing = True
        w,h = self.size()
        vert = 1 if self._verticalScrollBar.isVisible() else 0
        hori = 1 if self._horizontalScrollBar.isVisible() else 0
        if vert:
            self._verticalScrollBar.setGeometry(w-1,0,1,h-hori)
        if hori:
            self._horizontalScrollBar.setGeometry(0,h-1,w-vert,1)
        if isinstance(self._viewport, (TTkWidget, TTkLayout)):
            self._viewport.setGeometry(0,0,w-vert,h-hori)
        self._processing = False

    def resizeEvent(self, w: int, h: int) -> None:
        ''' Handle resize events

        :param w: the new width
        :type w: int
        :param h: the new height
        :type h: int
        '''
        self._resizeEvent()

    @pyTTkSlot()
    def _viewportChanged(self) -> None:
        ''' Internal slot to handle viewport changes and update scroll bar ranges and visibility '''
        if self._processing or not self._viewport or not self.isVisible(): return
        w,h = self.size()
        fw, fh = self._viewport.viewFullAreaSize()
        dw, dh = self._viewport.viewDisplayedSize()
        ox, oy = self._viewport.getViewOffsets()
        if 0 in [fw,fh,dw,dh]:
            return
        hpage = dw
        vpage = dh
        hrange = fw - dw
        vrange = fh - dh
        # TTkLog.debug(f"f:{fw,fh=}, d:{dw,dh=}, o:{ox,oy=}")
        self._verticalScrollBar.setPageStep(vpage)
        self._verticalScrollBar.setRange(0, vrange)
        self._verticalScrollBar.setValue(oy)
        self._horizontalScrollBar.setPageStep(hpage)
        self._horizontalScrollBar.setRange(0, hrange)
        self._horizontalScrollBar.setValue(ox)

        if self._verticalScrollBarPolicy == TTkK.ScrollBarAsNeeded:
            if w<=self._verticalScrollBar.minimumWidth() or vrange<=0:
                self._verticalScrollBar.hide()
            elif dh>=self._verticalScrollBar.minimumHeight():
                self._verticalScrollBar.show()
        elif self._verticalScrollBarPolicy == TTkK.ScrollBarAlwaysOn:
            self._verticalScrollBar.show()
        else:
            self._verticalScrollBar.hide()

        if self._horizontalScrollBarPolicy == TTkK.ScrollBarAsNeeded:
            if h<=self._horizontalScrollBar.minimumHeight() or hrange<=0:
                self._horizontalScrollBar.hide()
            elif dw>=self._horizontalScrollBar.minimumWidth():
                self._horizontalScrollBar.show()
        elif self._horizontalScrollBarPolicy == TTkK.ScrollBarAlwaysOn:
            self._horizontalScrollBar.show()
        else:
            self._horizontalScrollBar.hide()
        self._resizeEvent()

    @pyTTkSlot(int)
    def _vscrollMoved(self, val: int) -> None:
        ''' Internal slot to handle vertical scroll bar movement

        :param val: the new vertical scroll position
        :type val: int
        '''
        if not self._viewport:
            return
        ox, _ = self._viewport.getViewOffsets()
        self._viewport.viewMoveTo(ox, val)

    @pyTTkSlot(int)
    def _hscrollMoved(self, val: int) -> None:
        ''' Internal slot to handle horizontal scroll bar movement

        :param val: the new horizontal scroll position
        :type val: int
        '''
        if not self._viewport:
            return
        _, oy = self._viewport.getViewOffsets()
        self._viewport.viewMoveTo(val, oy)

    def setViewport(self, viewport: TTkAbstractScrollViewInterface) -> None:
        ''' Set the viewport widget

        :param viewport: the viewport widget implementing TTkAbstractScrollViewInterface
        :type viewport: :py:class:`TTkAbstractScrollViewInterface`

        :raises TypeError: if viewport does not implement TTkAbstractScrollViewInterface
        '''
        if not isinstance(viewport, TTkAbstractScrollViewInterface):
            raise TypeError("TTkAbstractScrollViewInterface is required in TTkAbstractScrollArea.setVewport(viewport)")
        if self._viewport:
            self._viewport.viewChanged.disconnect(self._viewportChanged)
            # TODO: Remove this check once
            #  unified  "addWidget" and "addItem" in the TTKGridLayout
            if isinstance(viewport, TTkWidget):
                self.layout().removeWidget(self._viewport)
            else:
                self.layout().removeItem(self._viewport)
        self._viewport = viewport
        self._viewport.viewChanged.connect(self._viewportChanged)
        self._verticalScrollBar.sliderMoved.connect(self._vscrollMoved)
        self._horizontalScrollBar.sliderMoved.connect(self._hscrollMoved)
        # TODO: Remove this check once
        #  unified  "addWidget" and "addItem" in the TTKGridLayout
        if isinstance(viewport, TTkWidget):
            self.layout().addWidget(viewport)
        else:
            self.layout().addItem(viewport)
        self._resizeEvent()

    def setVerticalScrollBarPolicy(self, policy: TTkK.ScrollBarPolicy) -> None:
        ''' Set the vertical scroll bar policy

        :param policy: the scroll bar policy (ScrollBarAsNeeded, ScrollBarAlwaysOn, ScrollBarAlwaysOff)
        :type policy: :py:class:`TTkK.ScrollBarPolicy`
        '''
        if policy != self._verticalScrollBarPolicy:
            self._verticalScrollBarPolicy = policy
            self._viewportChanged()

    def setHorizontalScrollBarPolicy(self, policy: TTkK.ScrollBarPolicy) -> None:
        ''' Set the horizontal scroll bar policy

        :param policy: the scroll bar policy (ScrollBarAsNeeded, ScrollBarAlwaysOn, ScrollBarAlwaysOff)
        :type policy: :py:class:`TTkK.ScrollBarPolicy`
        '''
        if policy != self._horizontalScrollBarPolicy:
            self._horizontalScrollBarPolicy = policy
            self._viewportChanged()

    def viewport(self) -> Optional[TTkAbstractScrollViewInterface]:
        ''' Return the current viewport

        :return: the viewport widget or None
        :rtype: :py:class:`TTkAbstractScrollViewInterface`, optional
        '''
        return self._viewport

    def update(self, repaint: bool = True, updateLayout: bool = False, updateParent: bool = False) -> None:
        ''' Update the scroll area and viewport

        :param repaint: trigger a repaint, defaults to True
        :type repaint: bool, optional
        :param updateLayout: trigger a layout update, defaults to False
        :type updateLayout: bool, optional
        :param updateParent: trigger a parent update, defaults to False
        :type updateParent: bool, optional
        '''
        if isinstance(self._viewport, (TTkWidget, TTkLayout)):
            self._viewport.update(repaint, updateLayout, updateParent=False)
        return super().update(repaint, updateLayout, updateParent)
