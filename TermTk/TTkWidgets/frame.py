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

__all__ = ['TTkFrame']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.container import TTkContainer

class TTkFrame(TTkContainer):
    '''

    ::

        ┌──────│Title│──────┐
        │                   │
        │                   │
        │                   │
        │                   │
        │                   │
        └───────────────────┘

    Demo1: `layout_nested.py  <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/layout_nested.py>`_

    Demo2: `splitter.py  <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/splitter.py>`_

    '''
    classStyle = {
                'default':     {'color': TTkColor.fg("#dddddd")+TTkColor.bg("#222222"),
                                'fillColor': TTkColor.RST,
                                'borderColor': TTkColor.RST},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'fillColor': TTkColor.RST,
                                'borderColor':TTkColor.fg('#888888')}
            }

    __slots__ = (
        '_border','_title', '_titleAlign',
        '_menubarTop', '_menubarTopPosition', '_menubarBottom', '_menubarBottomPosition')
    def __init__(self, *,
                 title:TTkString='',
                 border:bool=True,
                 titleAlign:TTkK.Alignment=TTkK.CENTER_ALIGN,
                 **kwargs) -> None:
        '''
        :param title: the title displayed at the top border of the frame, defaults to ""
        :type title: TTkString, optional
        :param titleAlign: the position of the title, defaults to :py:class:`TTkK.Alignment.CENTER_ALIGN`
        :type titleAlign: :py:class:`TTkK.Alignment`, optional
        :param border: Enable/Disable the border, defaults to **True**
        :type border: bool, optional
        '''

        self._titleAlign = titleAlign
        self._title = TTkString(title)
        self._border = border
        self._menubarBottomPosition = 0
        self._menubarTop = None
        self._menubarBottom = None
        super().__init__(**kwargs)
        # This is a little hack used in TTKWindow to define the placement of the TOP menubar inside TTKFrame
        self._menubarTopPosition = 0
        self.setBorder(self._border)

    def newMenubarTop(self):
        '''newMenubarTop

        .. warning::
            Method Deprecated,

            use :py:class:`~TermTk.TTkWidgets.frame.setMenuBar` instead

            i.e.

            .. code:: python

                menuBar = TTkMenuBarLayout()
                frame.setMenuBar(menuBar)
                menuBar.addMenu("File")

        '''
        if not self._menubarTop:
            from TermTk.TTkWidgets.menubar import TTkMenuBarLayout
            self._menubarTop = TTkMenuBarLayout()
            self.rootLayout().addItem(self._menubarTop)
            self._menubarTop.setGeometry(1,self._menubarTopPosition,self.width()-2,1)
            if not self._border and self._padt == 0:
                self.setPadding(self._menubarTopPosition,0,0,0)
        return self._menubarTop

    def menuBar(self, position=TTkK.TOP):
        if position == TTkK.TOP:
            return self._menubarTop
        else:
            return self._menubarBottom

    def setMenuBar(self, menuBar, position=TTkK.TOP):
        if not menuBar: # a null menuBar remove the current one
            if position == TTkK.TOP and self._menubarTop:
                self.rootLayout().removeItem(self._menubarTop)
                self._menubarTop = None
                if not self._border:
                    pt,pb,pl,pr = self.getPadding()
                    self.setPadding(0,pb,pl,pr)
            if position == TTkK.BOTTOM and self._menubarBottom:
                self.rootLayout().removeItem(self._menubarBottom)
                self._menubarBottom = None
                if not self._border:
                    pt,pb,pl,pr = self.getPadding()
                    self.setPadding(pt,0,pl,pr)
            return
        # menuBar is not null and it must be added to the rootLayout
        self.rootLayout().addItem(menuBar)
        if position == TTkK.TOP:
            self._menubarTop = menuBar
            menuBar.setGeometry(1,self._menubarTopPosition,self.width()-2,1)
        else:
            self._menubarBottom = menuBar
            menuBar.setGeometry(1,self.height()-1-self._menubarBottomPosition,self.width()-2,1)
        if not self._border:
            pt,pb,pl,pr = self.getPadding()
            pt = 1 if position==TTkK.TOP    else pt
            pb = 1 if position==TTkK.BOTTOM else pb
            self.setPadding(pt,pb,pl,pr)

    def resizeEvent(self, w, h):
        if self._menubarTop:
            self._menubarTop.setGeometry(1,self._menubarTopPosition,w-2,1)
        if self._menubarBottom:
            self._menubarBottom.setGeometry(1,h-1-self._menubarBottomPosition,w-2,1)
        super().resizeEvent(w,h)

    def title(self):
        '''title'''
        return self._title

    def setTitle(self, title):
        '''setTitle'''
        if self._title.sameAs(title): return
        self._title = TTkString(title)
        self.update()

    def titleAlign(self):
        return self._titleAlign

    def setTitleAlign(self, align):
        if align == self._titleAlign: return
        self._titleAlign = align
        self.update()

    def setBorder(self, border):
        '''setBorder'''
        self._border = border
        if border: self.setPadding(1,1,1,1)
        else:      self.setPadding(0,0,0,0)
        self.update()

    def border(self):
        '''border'''
        return self._border

    def paintEvent(self, canvas):
        style = self.currentStyle()
        color = style['color']
        fillColor = style['fillColor']
        borderColor = style['borderColor']

        if fillColor != TTkColor.RST:
            canvas.fill(color=fillColor)
        if self._border:
            canvas.drawBox(pos=(0,0),size=(self._width,self._height), color=borderColor)
            if len(self._title) != 0:
                canvas.drawBoxTitle(
                                pos=(0,0),
                                size=(self._width,self._height),
                                text=self._title,
                                align=self._titleAlign,
                                color=borderColor,
                                colorText=color)
        else:
            if self._menubarTop:
                canvas.drawMenuBarBg(pos=(0,0),size=self.width(),color=borderColor)
            if self._menubarBottom:
                canvas.drawMenuBarBg(pos=(0,self.height()-1),size=self.width(),color=borderColor)
