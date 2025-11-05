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

__all__ = ['TTkMenuBarButton', 'TTkMenuBarLayout']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.color import TTkColor
# from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.shortcut import TTkShortcut
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.boxlayout import TTkHBoxLayout
from TermTk.TTkWidgets.menu import TTkMenuButton

class TTkMenuBarButton(TTkMenuButton):
    classStyle = TTkMenuButton.classStyle | {
                'default': TTkMenuButton.classStyle['default'] |
                           {'borderColor':TTkColor.RST, 'shortcutColor': TTkColor.fg("#dddddd") + TTkColor.UNDERLINE,
                            'glyphs':('├','─','┤','┄','┄','▶')},
                'clicked': TTkMenuButton.classStyle['clicked'] |
                           {'color': TTkColor.fg("#ffff88")},
            }

    __slots__=('_shortcut')
    def __init__(self, *,
                 text:TTkString=...,
                 data:object=None,
                 checkable:bool=False,
                 checked:bool=False,
                 **kwargs) -> None:
        self._shortcut = []
        super().__init__(text=text, data=data, checkable=checkable, checked=checked, **kwargs)
        self.setCheckable(self.isCheckable())

    def setCheckable(self, ch):
        txtlen = self.text().termWidth()
        if ch:
            self.resize(txtlen+4,1)
            self.setMinimumSize(txtlen+4,1)
            self.setMaximumSize(txtlen+4,1)
        else:
            self.resize(txtlen+2,1)
            self.setMinimumSize(txtlen+2,1)
            self.setMaximumSize(txtlen+2,1)
        return super().setCheckable(ch)

    def paintEvent(self, canvas):
        style = self.currentStyle()
        borderColor = style['borderColor']
        glyphs      = style['glyphs']
        textColor   = style['color']
        scColor     = style['shortcutColor']
        if self._checkable:
            text = ('▣ ' if self._checked else '□ ') + self.text()
        else:
            text = self.text()

        canvas.drawText(pos=(0,0), color=borderColor ,text=glyphs[2])
        canvas.drawText(pos=(1+text.termWidth(),0), color=borderColor ,text=glyphs[0])
        canvas.drawText(pos=(1,0), color=textColor ,text=text)

        for sc in self._shortcut:
            canvas.drawChar(pos=(0,sc+1), char=text.charAt(sc), color=scColor)

class TTkMenuBarLayout(TTkHBoxLayout):
    '''TTkMenuBarLayout'''
    __slots__ = ('_itemsLeft', '_itemsCenter', '_itemsRight', '_buttons')
    def __init__(self, **kwargs) -> None:
        self._buttons = []
        super().__init__(**kwargs)
        self._itemsLeft   = TTkHBoxLayout()
        self._itemsCenter = TTkHBoxLayout()
        self._itemsRight  = TTkHBoxLayout()
        self.addItem(self._itemsLeft)
        self.addItem(TTkLayout())
        self.addItem(self._itemsCenter)
        self.addItem(TTkLayout())
        self.addItem(self._itemsRight)

    def addMenu(self,text:TTkString, data:object=None, checkable:bool=False, checked:bool=False, alignment=TTkK.LEFT_ALIGN):
        '''addMenu'''
        text = text if issubclass(type(text),TTkString) else TTkString(text)
        text, shortcuts = text.extractShortcuts()
        button = TTkMenuBarButton(text=text, data=data, checkable=checkable, checked=checked)
        for ch in shortcuts:
            shortcut = TTkShortcut(key=TTkK.CTRL | ord(ch.upper()))
            shortcut.activated.connect(button.shortcutEvent)
        self._mbItems(alignment).addWidget(button)
        self._buttons.append(button)
        self.update()
        return button

    def _menus(self, alignment=TTkK.LEFT_ALIGN):
        return [w.widget() for w in self._mbItems(alignment).children()]

    def _mbItems(self, alignment=TTkK.LEFT_ALIGN):
        return {
            TTkK.LEFT_ALIGN:   self._itemsLeft   ,
            TTkK.CENTER_ALIGN: self._itemsCenter ,
            TTkK.RIGHT_ALIGN:  self._itemsRight
        }.get(alignment, self._itemsLeft)

    def clear(self):
        self._buttons = []
        self._itemsLeft.removeItems(self._itemsLeft.children())
        self._itemsCenter.removeItems(self._itemsCenter.children())
        self._itemsRight.removeItems(self._itemsRight.children())
