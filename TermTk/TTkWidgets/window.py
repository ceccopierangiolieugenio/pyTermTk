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

__all__ = ['TTkWindow']

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkLayouts import TTkGridLayout, TTkLayout
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.resizableframe import TTkResizableFrame

class _MinimizedButton(TTkButton):
    __slots__ = ('_windowWidget')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._windowWidget = kwargs.get('windowWidget')
        def _cb():
            self._windowWidget.show()
            self.close()
        self.clicked.connect(_cb)

class TTkWindow(TTkResizableFrame):
    '''TTkWindow'''

    _windowStyleNormal = {
            'default':     {'borderColor': TTkColor.RST},
        }

    _windowStyleFocussed = {
            'default':     {'borderColor': TTkColor.fg("#ffff55")},
        }

    classStyle = {
                'default':     {'color': TTkColor.RST,
                                'borderColor': TTkColor.RST},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'borderColor':TTkColor.fg('#888888')},
                'focus':       {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000044")+TTkColor.BOLD,
                                'borderColor': TTkColor.fg("#ffff55")}
            }

    __slots__ = (
            '_mouseDelta', '_draggable',
            '_btnClose', '_btnMax', '_btnMin', '_btnReduce',
            '_flags', '_winTopLayout',
            '_maxBk', '_redBk' )
    def __init__(self, *args, **kwargs):
        self._winTopLayout = TTkGridLayout()
        super().__init__(*args, **kwargs)
        self._flags = TTkK.NONE
        self.setPadding(3,1,1,1)
        self._mouseDelta = (0,0)
        self.setFocusPolicy(TTkK.ClickFocus)
        self._draggable = False
        self._menubarTopPosition = 2

        # Add the top Layout to keep the windows action buttons
        # self._winTopLayout = TTkGridLayout()
        self.rootLayout().addItem(self._winTopLayout)
        # Close Button
        self._btnClose = TTkButton(border=False, text="x", size=(3,1), maxWidth=3, minWidth=3, visible=False)
        self._btnClose.clicked.connect(self.close)
        # Max Button
        self._maxBk = None
        self._btnMax = TTkButton(border=False, text="^", size=(3,1), maxWidth=3, minWidth=3, visible=False)
        self._btnMax.clicked.connect(self._maximize)
        # Min Button
        self._btnMin = TTkButton(border=False, text="_", size=(3,1), maxWidth=3, minWidth=3, visible=False)
        self._btnMin.clicked.connect(self._minimize)
        # Button Reduce_border
        self._redBk = None
        self._btnReduce = TTkButton(border=False, text=".", size=(3,1), maxWidth=3, minWidth=3, visible=False)
        self._btnReduce.clicked.connect(self._reduce)

        self._winTopLayout.addItem(TTkLayout(),0,0)
        self._winTopLayout.addWidget(self._btnClose, 0,4)
        self._winTopLayout.addWidget(self._btnMax,   0,3)
        self._winTopLayout.addWidget(self._btnMin,   0,2)
        self._winTopLayout.addWidget(self._btnReduce,0,1)
        self._winTopLayout.setGeometry(1,1,self.width()-2,1)
        self._winTopLayout.update()

        self.setWindowFlag(kwargs.get('flags', TTkK.WindowFlag.WindowCloseButtonHint))
        self.focusChanged.connect(self._focusChanged)

    def _maximize(self):
        if not (pw := self.parentWidget()): return
        if self._maxBk:
            self.setGeometry(*self._maxBk)
            self._maxBk = None
        else:
            bk = self.geometry()
            maxw,maxh = pw.layout().size()
            self.setGeometry(0,0,maxw,maxh)
            self._maxBk = bk

    def _reduce(self):
        if self._redBk:
            self.resize(*self._redBk)
            self._redBk = None
        else:
            bk = self.size()
            self.resize(self.width(),4)
            self._redBk = bk

    def _minimize(self):
        if not (pw := self.parentWidget()): return
        stack = []
        for li in pw.rootLayout().children():
            if li.layoutItemType() == TTkK.WidgetItem and issubclass(type(w:=li.widget()),_MinimizedButton):
                stack.append(w.y())
        stack = sorted(stack)
        lx,ly = pw.layout().pos()
        pos = ly
        for v in stack:
            if (pos+2) < v or (v+2) < pos:
                break
            pos += 3
        mb = _MinimizedButton(windowWidget=self,text=self._title,border=True,pos=(lx,pos),size=(15,3))
        pw.rootLayout().addWidget(mb)
        self.hide()

    def windowFlag(self):
        '''windowFlag'''
        return self._flags

    def setWindowFlag(self, flag):
        '''setWindowFlag'''
        if self._flags == flag: return
        self._flags = flag
        self._btnClose.setVisible( bool(flag & TTkK.WindowFlag.WindowCloseButtonHint))
        self._btnMax.setVisible(   bool(flag & TTkK.WindowFlag.WindowMaximizeButtonHint))
        self._btnMin.setVisible(   bool(flag & TTkK.WindowFlag.WindowMinimizeButtonHint))
        self._btnReduce.setVisible(bool(flag & TTkK.WindowFlag.WindowReduceButtonHint))
        self._winTopLayout.update()

    def resizeEvent(self, w, h):
        self._maxBk = None
        self._redBk = None
        self._winTopLayout.setGeometry(1,1,w-2,1)
        super().resizeEvent(w,h)

    def mousePressEvent(self, evt):
        self._mouseDelta = (evt.x, evt.y)
        self._draggable = False
        w,_ = self.size()
        x,y = evt.x, evt.y
        # If the mouse position is inside the header box enable the dragging feature
        if x >= 1 and y>=1 and x<w-1 and y<3:
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

    def _focusChanged(self, focus):
        if focus:
            styleToMerge = TTkWindow._windowStyleFocussed
        else:
            styleToMerge = TTkWindow._windowStyleNormal

        def _applyStyle(_mb):
            if not _mb: return
            for m in _mb._menus(TTkK.LEFT_ALIGN):   m.mergeStyle(styleToMerge)
            for m in _mb._menus(TTkK.RIGHT_ALIGN):  m.mergeStyle(styleToMerge)
            for m in _mb._menus(TTkK.CENTER_ALIGN): m.mergeStyle(styleToMerge)

        _applyStyle(self.menuBar(TTkK.TOP))
        _applyStyle(self.menuBar(TTkK.BOTTOM))


    def focusOutEvent(self):
        self._draggable = False

    def paintEvent(self, canvas):
        style = self.currentStyle()
        color = style['color']
        borderColor = style['borderColor']

        canvas.drawText(pos=(2,1),text=self._title, color=color)
        canvas.drawGrid(
                    color=borderColor,
                    pos=(0,0), size=self.size(),
                    hlines=[2], grid=2)