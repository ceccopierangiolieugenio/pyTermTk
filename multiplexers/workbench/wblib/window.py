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
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkLayouts import TTkGridLayout, TTkLayout
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.resizableframe import TTkResizableFrame

from .colors import *
from .scrollbar import *

__all__ = ['WBWindow']


class _MinimizedButton(TTkButton):
    __slots__ = ('_windowWidget')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._windowWidget = kwargs.get('windowWidget')
        def _cb():
            self._windowWidget.show()
            self.close()
        self.clicked.connect(_cb)

class WBWindow(TTkResizableFrame):
    '''TTkWindow'''
    __slots__ = (
            '_title', '_mouseDelta', '_draggable',
            '_btnClose', '_btnMax', '_btnMin', '_btnReduce',
            '_flags', '_winTopLayout',
            '_sbRight', '_sbBottom',
            '_maxBk', '_redBk',
            '_wbbg')
    def __init__(self, wbbg=fgWHITE+bgBLUE, *args, **kwargs):
        self._winTopLayout = TTkGridLayout()
        self._wbbg = wbbg
        super().__init__(*args, **kwargs)
        self._flags = TTkK.NONE
        self.setPadding(1,1,1,1)
        self._mouseDelta = (0,0)
        self.setFocusPolicy(TTkK.ClickFocus)
        self._draggable = False
        self._sbRight  = WBScrollBar(orientation=TTkK.VERTICAL)
        self._sbBottom = WBScrollBar(orientation=TTkK.HORIZONTAL)
        self._sbRight.setPageStep(60)
        self._sbRight.setRange(0, 100)
        self._sbBottom.setPageStep(60)
        self._sbBottom.setRange(0, 100)
        self.rootLayout().addWidgets([self._sbRight,self._sbBottom])
        w,h = self.size()
        self._sbRight.setGeometry(  w-1, 1,   1,   h-2)
        self._sbBottom.setGeometry( 0  , h-1, w-1, 1  )

    def resizeEvent(self, w, h):
        self._maxBk = None
        self._redBk = None
        self._winTopLayout.setGeometry(1,1,w-2,1)
        self._sbRight.setGeometry(  w-1, 1,   1,   h-2)
        self._sbBottom.setGeometry( 0  , h-1, w-1, 1  )
        super().resizeEvent(w,h)

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

    def paintEvent(self, canvas=TTkCanvas):
        if self.hasFocus():
            color = TTkCfg.theme.windowBorderColorFocus
            titleChar = '☰'
        else:
            color = TTkCfg.theme.windowBorderColor
            # titleChar = '☷'
            titleChar = '⚏'

        w,h = self.size()


        canvas.fill(color=bgBLUE)
        canvas.fill(char='▎',pos=(0,1), size=(1,h-2), color=self._wbbg)
        # draw the title ┃ │
        canvas.drawText(
            text=f"│▣│ {self._title} {titleChar*w}",
            # text=f"│⚀│ {self._title} {titleChar*w}",
            color=bgWHITE+fgBLUE)

        canvas.drawText(
            text="│◪│◩│",
            pos=(w-5,0),
            color=bgWHITE+fgBLUE)

        canvas.drawChar(pos=(w-1,h-1),char='⇱',color=fgBLUE+bgWHITE)