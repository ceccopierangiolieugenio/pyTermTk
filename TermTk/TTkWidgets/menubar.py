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
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.listwidget import TTkListWidget, TTkAbstractListItem
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.boxlayout import TTkHBoxLayout


class _TTkMenuListWidget(TTkListWidget):
    __slots__ = ('_previous')
    def __init__(self, *args, **kwargs):
        TTkListWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkMenuListWidget' )
        self._previous = kwargs.get('previous',TTkHelper.getFocus())

    def keyEvent(self, evt):
        if evt.type == TTkK.SpecialKey:
            if evt.key == TTkK.Key_Left:
                TTkHelper.removeSingleOverlay(self)
                if self._previous:
                    self._previous.setFocus()
                return True
            elif evt.key == TTkK.Key_Right:
                if self._highlighted and \
                   isinstance(self._highlighted,TTkMenuButton) and \
                   self._highlighted._menu:
                    self._highlighted.menuButtonEvent()
                return True
        return TTkListWidget.keyEvent(self, evt)


class _TTkMenuSpacer(TTkAbstractListItem):
    def __init__(self, *args, **kwargs):
        TTkAbstractListItem.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkMenuSpacer' )
        self.resize(1,1)

    def paintEvent(self):
        self._canvas.drawText(pos=(0,0), text="-"*self.width())

class TTkMenuButton(TTkAbstractListItem):
    __slots__ = ('_border', '_borderColor', '_shortcut', '_menu', 'menuButtonClicked', '_menuOffset')
    def __init__(self, *args, **kwargs):
        TTkAbstractListItem.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkMenuButton' )
        # signals
        self.menuButtonClicked = pyTTkSignal(TTkButton)
        self._color = kwargs.get('color', TTkCfg.theme.menuButtonColor )
        self._border = kwargs.get('border', TTkCfg.theme.menuButtonColor )
        self._borderColor = kwargs.get('borderColor', TTkCfg.theme.menuButtonBorderColor )
        self._menuOffset = kwargs.get('menuOffset', (-1,0) )
        self._shortcut = []
        self._menu = []
        while self.text.find('&') != -1:
            index = self.text.find('&')
            shortcut = self.text[index+1]
            TTkHelper.addShortcut(self, shortcut)
            self._shortcut.append(index)
            self.text = self.text[:index]+self.text[index+1:]
        txtlen = len(self.text)
        self.resize(txtlen,1)
        self.setMinimumSize(txtlen+2,1)
        self.setMaximumSize(txtlen+2,1)
        self.listItemClicked.connect(self.menuButtonEvent)

    def addMenu(self, text):
        button = TTkMenuButton(text=text, borderColor=self._borderColor, border=False)
        button.menuButtonClicked.connect(self._menuCallback)
        self._menu.append(button)
        return button

    def addSpacer(self):
        self._menu.append(_TTkMenuSpacer())

    def setColor(self, color):
        self._color = color
        self.update()

    def setBorderColor(self, color):
        self._borderColor = color
        self.update()

    def shortcutEvent(self):
        self.menuButtonEvent()

    @pyTTkSlot(TTkButton)
    def _menuCallback(self, button):
        #self._id = self._list.index(label)
        TTkLog.debug(f"Bind Clicked {button.text}")
        self.menuButtonClicked.emit(button)
        TTkHelper.removeOverlay()
        self.update()

    @pyTTkSlot(TTkAbstractListItem)
    def menuButtonEvent(self, listItem=None):
        if not self._menu:
            self.menuButtonClicked.emit(self)
            return
        # Import here to avoid circular import
        from TermTk.TTkWidgets.list   import TTkList
        from TermTk.TTkWidgets.resizableframe import TTkResizableFrame

        # Stupid way to find out if I am a submenu
        isSubmenu = not self._border
        frameHeight = len(self._menu) + 2
        frameWidth = self.width()
        if frameHeight > 15: frameHeight = 15
        if frameWidth  < 15: frameWidth = 15
        if isSubmenu:
            frame = TTkResizableFrame(layout=TTkHBoxLayout(), size=(frameWidth,frameHeight))
            pos = (self.width(), -1)
        else:
            frame = TTkResizableFrame(layout=TTkHBoxLayout(), size=(frameWidth,frameHeight), title=self.text, titleAlign=TTkK.LEFT_ALIGN)
            pos = self._menuOffset
        menuListWidget = _TTkMenuListWidget()
        listw = TTkList(parent=frame, listWidget = menuListWidget)
        # listw.textClicked.connect(self._menuCallback)
        # listw.textClicked.connect(self._menuCallback)
        # TTkLog.debug(f"{self._menu}")
        for item in self._menu:
            listw.addItem(item)
        TTkHelper.overlay(self, frame, pos[0], pos[1])
        listw.viewport().setFocus()
        self.update()

    def paintEvent(self):
        if self._pressed:
            borderColor = self._borderColor
            textColor   = TTkCfg.theme.menuButtonColorClicked
            scColor     = TTkCfg.theme.menuButtonShortcutColor
        else:
            borderColor = self._borderColor
            textColor   = self._color
            scColor     =  TTkCfg.theme.menuButtonShortcutColor
        self._canvas.drawMenuBarButton(
                        pos=(0,0),text=self.text,
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

class TTkMenuLayout(TTkHBoxLayout):
    __slots__ = ('_itemsLeft', '_itemsCenter', '_itemsRight', '_buttons')
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
        button = TTkMenuButton(text=text, borderColor=self._borderColor, border=True)
        if  alignment == TTkK.LEFT_ALIGN:
            self._itemsLeft.addWidget(button)
        elif alignment == TTkK.CENTER_ALIGN:
            self._itemsCenter.addWidget(button)
        elif alignment == TTkK.RIGHT_ALIGN:
            self._itemsRight.addWidget(button)
        self._buttons.append(button)
        return button
