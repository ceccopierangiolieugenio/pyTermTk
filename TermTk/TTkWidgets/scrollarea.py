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

__all__ = ['TTkScrollArea']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSlot
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class _TTkAreaWidget(TTkAbstractScrollView):
    __slots__ = ()
    def __init__(self, *args, **kwargs) -> None:
        TTkAbstractScrollView.__init__(self, *args, **kwargs)
        self.viewChanged.connect(self._viewChangedHandler)

    @pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def maximumWidth(self):   return 0x10000
    def maximumHeight(self):  return 0x10000
    def minimumWidth(self):   return 0
    def minimumHeight(self):  return 0

class TTkScrollArea(TTkAbstractScrollArea):
    '''TTkScrollArea'''
    __slots__ = ('_areaView')
    def __init__(self, *,
                 # TTkWidget init
                 parent:TTkWidget=None,
                 visible:bool=True,
                 # TTkAbstractScrollArea init
                 verticalScrollBarPolicy:TTkK.ScrollBarPolicy=TTkK.ScrollBarPolicy.ScrollBarAsNeeded,
                 horizontalScrollBarPolicy:TTkK.ScrollBarPolicy=TTkK.ScrollBarPolicy.ScrollBarAsNeeded,
                 **kwargs) -> None:
        self._areaView = _TTkAreaWidget(**kwargs)
        TTkAbstractScrollArea.__init__(self, parent=parent, visible=visible, verticalScrollBarPolicy=verticalScrollBarPolicy, horizontalScrollBarPolicy=horizontalScrollBarPolicy, **kwargs)
        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._areaView)