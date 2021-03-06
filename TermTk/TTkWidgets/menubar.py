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
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.boxlayout import TTkHBoxLayout

class _TTkMenuSpacer(TTkWidget):
    __slots__ = ('clicked')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkMenuSpacer' )
        # Define Signals
        self.clicked = pyTTkSignal()
        self.resize(1,1)
        #self.setMinimumHeight(1)

    def paintEvent(self):
        TTkLog.debug("pippo")
        self._canvas.drawText(pos=(0,0), text="-"*self.width())

class _TTkMenuButton(TTkButton):
    __slot__ = ('_color', '_borderColor', '_shortcut', '_menu', 'menuButtonClicked')
    def __init__(self, *args, **kwargs):
        TTkButton.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkMenuButton' )
        # signals
        self.menuButtonClicked = pyTTkSignal(TTkButton)
        self._color = kwargs.get('color', TTkCfg.theme.menuButtonColor )
        self._borderColor = kwargs.get('borderColor', TTkCfg.theme.menuButtonBorderColor )
        self._shortcut = []
        self._menu = []
        while self._text.find('&') != -1:
            index = self._text.find('&')
            shortcut = self._text[index+1]
            TTkHelper.addShortcut(self, shortcut)
            self._shortcut.append(index)
            self._text = self._text[:index]+self._text[index+1:]
        txtlen = len(self._text)
        self.resize(txtlen,1)
        self.setMinimumSize(txtlen+2,1)
        self.setMaximumSize(txtlen+2,1)
        self.clicked.connect(self.menuButtonEvent)

    def addMenu(self, text):
        button = _TTkMenuButton(text=text, borderColor=self._borderColor, border=False)
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
        TTkLog.debug(f"Bind Clicked {button._text}")
        self.menuButtonClicked.emit(button)
        self.setFocus()
        self.update()

    @pyTTkSlot()
    def menuButtonEvent(self):
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
            frame = TTkResizableFrame(layout=TTkHBoxLayout(), size=(frameWidth,frameHeight), title=self._text, titleAlign=TTkK.LEFT_ALIGN)
            pos = (-1, 0)
        listw = TTkList(parent=frame)
        # listw.textClicked.connect(self._menuCallback)
        # listw.textClicked.connect(self._menuCallback)
        TTkLog.debug(f"{self._menu}")
        for item in self._menu:
            listw.addItem(item)
        TTkHelper.overlay(self, frame, pos[0], pos[1])
        self.update()

    def paintEvent(self):
        if self._pressed:
            borderColor = self._borderColor
            textColor   = TTkCfg.theme.menuButtonColorClicked
            scColor     =  TTkCfg.theme.menuButtonShortcutColor
        else:
            borderColor = self._borderColor
            textColor   = self._color
            scColor     =  TTkCfg.theme.menuButtonShortcutColor
        self._canvas.drawMenuBarButton(
                        pos=(0,0),text=self._text,
                        width=self.width(),
                        shortcuts=self._shortcut,
                        border=self._border,
                        submenu=len(self._menu)>0,
                        color=textColor,
                        borderColor=borderColor,
                        shortcutColor=scColor )

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
        button = _TTkMenuButton(text=text, borderColor=self._borderColor, border=True)
        if  alignment == TTkK.LEFT_ALIGN:
            self._itemsLeft.addWidget(button)
        elif alignment == TTkK.CENTER_ALIGN:
            self._itemsCenter.addWidget(button)
        elif alignment == TTkK.RIGHT_ALIGN:
            self._itemsRight.addWidget(button)
        self._buttons.append(button)
        return button
