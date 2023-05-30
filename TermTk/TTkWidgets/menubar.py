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

from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.listwidget import TTkListWidget, TTkAbstractListItem
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.boxlayout import TTkHBoxLayout
from TermTk.TTkWidgets.menu import TTkMenu, TTkMenuButton, _TTkMenuSpacer

class TTkMenuBarButton(TTkAbstractListItem):
    '''TTkMenuButton'''
    __slots__ = ('_border', '_borderColor', '_shortcut', '_menu', 'menuButtonClicked', '_menuOffset')
    def __init__(self, *args, **kwargs):
        TTkAbstractListItem.__init__(self, *args, **kwargs)
        # signals
        self.menuButtonClicked = pyTTkSignal(TTkMenuButton)
        self._color = kwargs.get('color', TTkCfg.theme.menuButtonColor )
        self._border = kwargs.get('border', TTkCfg.theme.menuButtonColor )
        self._borderColor = kwargs.get('borderColor', TTkCfg.theme.menuButtonBorderColor )
        self._menuOffset = kwargs.get('menuOffset', (-1,0) )
        self._shortcut = []
        self._menu = []
        while self.text().find('&') != -1:
            index = self.text().find('&')
            shortcut = self.text().charAt(index+1)
            TTkHelper.addShortcut(self, shortcut)
            self._shortcut.append(index)
            self.setText(self.text().substring(to=index)+self.text().substring(fr=index+1))
        txtlen = self.text().termWidth()
        self.resize(txtlen,1)
        self.setMinimumSize(txtlen+2,1)
        self.setMaximumSize(txtlen+2,1)
        self.listItemClicked.connect(self.menuButtonEvent)

    def addMenu(self, text, data:object=None, checkable:bool=False, checked:bool=False):
        '''addMenu'''
        button = TTkMenuButton(text=text, data=data, checkable=checkable, checked=checked)
        self._menu.append(button)
        return button

    def addSpacer(self):
        '''addSpacer'''
        self._menu.append(_TTkMenuSpacer())

    def setColor(self, color):
        self._color = color
        self.update()

    def setBorderColor(self, color):
        self._borderColor = color
        self.update()

    def shortcutEvent(self):
        self.menuButtonEvent()

    @pyTTkSlot(TTkAbstractListItem)
    def menuButtonEvent(self, listItem=None):
        if not self._menu:
            self.menuButtonClicked.emit(self)
            return

        width = 3+max((len(smb._text) + (2 if smb._submenu else 0)) for smb in self._menu if type(smb) is TTkMenuButton)
        height = len(self._menu)+2
        subMenu = TTkMenu(pos=(8,6), size=(width,height), title=self.text(), titleAlign=TTkK.LEFT_ALIGN)
        for smb  in self._menu:
            subMenu.addMenuItem(smb)
        TTkHelper.overlay(self, subMenu, -1, 0)
        self.update()

    def paintEvent(self, canvas):
        if self._pressed:
            borderColor = self._borderColor
            textColor   = TTkCfg.theme.menuButtonColorClicked
            scColor     = TTkCfg.theme.menuButtonShortcutColor
        else:
            borderColor = self._borderColor
            textColor   = self._color
            scColor     =  TTkCfg.theme.menuButtonShortcutColor
        canvas.drawMenuBarButton(
                        pos=(0,0),text=self.text(),
                        width=self.width(),
                        shortcuts=self._shortcut,
                        border=self._border,
                        submenu=len(self._menu)>0,
                        color=textColor,
                        borderColor=borderColor,
                        shortcutColor=scColor )

    def focusInEvent(self):
        self.highlighted=True

    def focusOutEvent(self):
        self.highlighted=False

class TTkMenuBarLayout(TTkHBoxLayout):
    '''TTkMenuBarLayout'''
    __slots__ = ('_borderColor', '_itemsLeft', '_itemsCenter', '_itemsRight', '_buttons')
    def __init__(self, *args, **kwargs):
        self._buttons = []
        TTkHBoxLayout.__init__(self, *args, **kwargs)
        self._borderColor = kwargs.get('borderColor', TTkCfg.theme.frameBorderColor )
        self._itemsLeft   = TTkHBoxLayout()
        self._itemsCenter = TTkHBoxLayout()
        self._itemsRight  = TTkHBoxLayout()
        self.addItem(self._itemsLeft)
        self.addItem(TTkLayout())
        self.addItem(self._itemsCenter)
        self.addItem(TTkLayout())
        self.addItem(self._itemsRight)

    def setBorderColor(self, color):
        self._borderColor = color
        for b in self._buttons:
            b.setBorderColor(color)
        self.update()

    def addMenu(self, text, alignment=TTkK.LEFT_ALIGN):
        '''addMenu'''
        button = TTkMenuBarButton(text=text, borderColor=self._borderColor, border=True)
        if  alignment == TTkK.LEFT_ALIGN:
            self._itemsLeft.addWidget(button)
        elif alignment == TTkK.CENTER_ALIGN:
            self._itemsCenter.addWidget(button)
        elif alignment == TTkK.RIGHT_ALIGN:
            self._itemsRight.addWidget(button)
        self._buttons.append(button)
        self.update()
        return button
