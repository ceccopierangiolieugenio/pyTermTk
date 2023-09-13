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

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkLayouts import TTkGridLayout, TTkLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.resizableframe import TTkResizableFrame
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollViewLayout, TTkAbstractScrollViewInterface


from .colors import *
from .scrollbar import *

__all__ = ['WBScrollWin']


class _MinimizedButton(TTkButton):
    __slots__ = ('_windowWidget')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._windowWidget = kwargs.get('windowWidget')
        def _cb():
            self._windowWidget.show()
            self.close()
        self.clicked.connect(_cb)

class WBScrollWin(TTkResizableFrame):
    '''WBScrollWin'''

    _styleScrollBar = {
                'default':     {'color': bgWHITE+fgBLUE},
                'disabled':    {'color': bgWHITE+fgBLUE},
                'focus':       {'color': bgWHITE+fgBLUE},
            }

    _styleBgWhite = {
                'default':     {'color': fgWHITE+bgBLUE},
                'disabled':    {'color': fgWHITE+bgBLUE},
                'focus':       {'color': fgWHITE+bgBLUE},
            }

    _styleBgNone = {
                'default':     {'color': fgWHITE},
                'disabled':    {'color': fgWHITE},
                'focus':       {'color': fgWHITE},
            }

    classStyle = {
                'default':     {'titleChar': '⚏',
                                'borderColor': bgWHITE+fgBLUE},
                'disabled':    {'titleChar': '⚏',
                                'borderColor':bgWHITE+fgBLUE},
                'focus':       {'titleChar': '☰',
                                'borderColor': bgWHITE+fgBLUE}
            }

    __slots__ = (
            # Copied from Scroll Area
            '_viewport',
            '_verticalScrollBar',
            '_horizontalScrollBar',

            # Copied from Window
            '_mouseDelta', '_draggable',
            '_btnClose', '_btnMax', '_btnMin', '_btnReduce',
            '_flags', '_winTopLayout',
            '_sbRight', '_sbBottom')

    def __init__(self, whiteBg=True, *args, **kwargs):
        self._winTopLayout = TTkGridLayout()
        self._viewport = TTkAbstractScrollViewLayout()

        super().__init__(*args, **kwargs|{'layout':TTkGridLayout()})

        self._verticalScrollBar   = WBScrollBar(orientation=TTkK.VERTICAL)
        self._horizontalScrollBar = WBScrollBar(orientation=TTkK.HORIZONTAL)

        self.rootLayout().addWidgets([self._verticalScrollBar, self._horizontalScrollBar])

        self.layout().addItem(self._viewport)

        if whiteBg:
            self.mergeStyle(self._styleBgWhite)
        else:
            self.mergeStyle(self._styleBgNone)

        self._flags = TTkK.NONE
        self.setPadding(1,1,1,1)
        self._mouseDelta = (0,0)
        self.setFocusPolicy(TTkK.ClickFocus)
        self._draggable = False

        self._resizeEvent()

    def setViewport(self, viewport):
        if not isinstance(viewport, TTkAbstractScrollViewInterface):
            raise TypeError("TTkAbstractScrollViewInterface is required in TTkAbstractScrollArea.setVewport(viewport)")
        if self._viewport:
            self._viewport.viewChanged.disconnect(self._viewportChanged)
            if isinstance(self._viewport, TTkWidget):
                self.layout().removeWidget(self._viewport)
            else:
                self.layout().removeItem(self._viewport)
        self._viewport = viewport
        self._viewport.viewChanged.connect(self._viewportChanged)
        self._verticalScrollBar.sliderMoved.connect(self._vscrollMoved)
        self._horizontalScrollBar.sliderMoved.connect(self._hscrollMoved)
        if isinstance(viewport, TTkWidget):
            self.layout().addWidget(viewport)
        else:
            self.layout().addItem(viewport)
        self._resizeEvent()

    def viewport(self):
        return self._viewport

    def _resizeEvent(self):
        w,h = self.size()
        self._verticalScrollBar.setGeometry(   w-1,   1,   1, h-2)
        self._horizontalScrollBar.setGeometry( 0  , h-1, w-1, 1  )
        # if self._viewport:
        #     self._viewport.setGeometry(0,0,w-2,h-2)
        self._winTopLayout.setGeometry(1,1,w-2,1)

    def resizeEvent(self, w, h):
        super().resizeEvent(w,h)
        self._resizeEvent()

    @pyTTkSlot()
    def _viewportChanged(self):
        if not self.isVisible(): return
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

        self._resizeEvent()

    @pyTTkSlot(int)
    def _vscrollMoved(self, val):
        ox, _ = self._viewport.getViewOffsets()
        self._viewport.viewMoveTo(ox, val)

    @pyTTkSlot(int)
    def _hscrollMoved(self, val):
        _, oy = self._viewport.getViewOffsets()
        self._viewport.viewMoveTo(val, oy)

    def update(self, repaint=True, updateLayout=False, updateParent=False):
        if self._viewport:
            self._viewport.update(repaint, updateLayout, updateParent)
        return super().update(repaint, updateLayout, updateParent)

    def mousePressEvent(self, evt):
        self._mouseDelta = (evt.x, evt.y)
        self._draggable = False
        w,_ = self.size()
        x,y = evt.x, evt.y
        # If the mouse position is inside the header box enable the dragging feature
        if y==0 and 1<=x<w-1:
            if x<4:
                self.close()
                return True
            if x>w-4:
                self.lowerWidget()
                return True
            self._draggable = True
            return True
        return TTkResizableFrame.mousePressEvent(self, evt)

    def mouseDragEvent(self, evt):
        if self._draggable:
            x,y = self.pos()
            dx = evt.x-self._mouseDelta[0]
            dy = evt.y-self._mouseDelta[1]
            self.move(x+dx, y+dy)
            return True
        return TTkResizableFrame.mouseDragEvent(self, evt)

    def focusInEvent(self):
        if self._menubarTop:
            self._menubarTop.setBorderColor(TTkColor.fg("#ffff55"))
        self.update()

    def focusOutEvent(self):
        self._draggable = False
        if self._menubarTop:
            self._menubarTop.setBorderColor(TTkColor.RST)
        self.update()

    # # Stupid hack to paint on top of the child widgets
    # def paintChildCanvas(self):
    #     super().paintChildCanvas()
    #     style = self.currentStyle()
    #     borderColor = style['borderColor']
    #     w,h = self.size()
    #     canvas = self.getCanvas()
    #     canvas.drawChar(pos=(w-1,h-1),char='⇱',color=borderColor)

    def paintEvent(self, canvas=TTkCanvas):
        style = self.currentStyle()
        color = style['color']
        borderColor = style['borderColor']
        titleChar = style['titleChar']

        w,h = self.size()

        canvas.fill(color=bgBLUE)
        canvas.fill(char='▎',pos=(0,1), size=(1,h-2), color=color)
        # draw the title ┃ │
        canvas.drawText(
            text=f"│▣│ {self._title} {titleChar*w}",
            # text=f"│⚀│ {self._title} {titleChar*w}",
            color=borderColor)

        canvas.drawText(
            text="│◪│◩│",
            pos=(w-5,0),
            color=borderColor)

        canvas.drawChar(pos=(w-1,h-1),char='⇱',color=borderColor)