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

from TermTk.TTkCore.constant import TTkConstant, TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.spacer import TTkSpacer
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkWidgets.menubar import TTkMenuButton
from TermTk.TTkLayouts.boxlayout import TTkHBoxLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout


class _TTkTabMenuButton(TTkMenuButton):
    __slots__ = ('_sideBorder', '_tabPosition')

    def __init__(self, *args, **kwargs):
        self._sideBorder = TTkK.NONE
        self._tabPosition = kwargs.get('tabPosition', TTkK.LEFT)
        TTkMenuButton.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTabMenuButton')
        txtlen = len(self.text)
        self.setMinimumSize(txtlen+1,0x2)
        self.setMaximumSize(txtlen+1,0x1000)

    def setSideBorder(self, border):
        self._sideBorder |= border

    def unsetSideBorder(self, border):
        self._sideBorder &= ~border

    def paintEvent(self):
        if self._pressed:
            borderColor = self._borderColor
            textColor   = TTkCfg.theme.menuButtonColorClicked
            scColor     = TTkCfg.theme.menuButtonShortcutColor
        else:
            borderColor = self._borderColor
            textColor   = self._color
            scColor     =  TTkCfg.theme.menuButtonShortcutColor
        if self._tabPosition == TTkK.LEFT:
            text = f" {self.text}"
        else:
            text = f"{self.text} "
        self._canvas.drawTabMenuButton(
                        pos=(0,0),text=text,
                        slim=(self._height==2),
                        size=self.size(),
                        color=textColor,
                        borderColor=borderColor,
                        sideBorder = self._sideBorder)

'''
_curentIndex =              2
_labelPos =      [0],[1],  [2],   [3],   [4],
                ╭─┌──┌──────╔══════╗──────┬──────┐─╮
_labels=        │◀│La│Label1║Label2║Label3│Label4│▶│
                ╞═══════════╩══════╩═══════════════╡
                 leftscroller                     rightScroller
'''
class _TTkTabs(TTkWidget):
    __slots__ = (
        '_tabColor', '_tabBorderColor', '_tabSelectColor', '_tabOffsetColor',
        '_tabColorFocus', '_tabBorderColorFocus', '_tabSelectColorFocus', '_tabOffsetColorFocus',
        '_labels', '_labelsPos',
        '_offset', '_currentIndex','_lastIndex',
        '_leftScroller', '_rightScroller',
        '_tabMovable', '_tabClosable',
        '_sideBorder',
        #Signals
        'currentChanged')

    def __init__(self, *args, **kwargs):
        self._labels = []
        self._labelsPos = []
        self._currentIndex = -1
        self._lastIndex = -1
        self._offset = -1
        self._tabMovable = False
        self._tabClosable = False
        self._leftScroller = False
        self._rightScroller = False
        self._sideBorder = TTkK.LEFT | TTkK.RIGHT
        self._tabColor       = TTkCfg.theme.tabColor
        self._tabBorderColor = TTkCfg.theme.tabBorderColor
        self._tabSelectColor = TTkCfg.theme.tabSelectColor
        self._tabOffsetColor = TTkCfg.theme.tabOffsetColor
        self._tabColorFocus       = TTkCfg.theme.tabColorFocus
        self._tabBorderColorFocus = TTkCfg.theme.tabBorderColorFocus
        self._tabSelectColorFocus = TTkCfg.theme.tabSelectColorFocus
        self._tabOffsetColorFocus = TTkCfg.theme.tabOffsetColorFocus
        # Signals
        self.currentChanged = pyTTkSignal(int)
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTabs')
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def addTab(self, label):
        self._labels.append(label)
        self._updateTabs()

    def insertTab(self, index, label):
        self._labels.insert(index, label)
        self._updateTabs()

    def setSideBorder(self, border):
        self._sideBorder |= border

    def unsetSideBorder(self, border):
        self._sideBorder &= ~border


    def setBorderColor(self, color):
        self._tabBorderColor      = color
        self._tabBorderColorFocus = color

    def _updateTabs(self):
        xpos = 0+2
        w = self.width()-4
        self._labelsPos = []
        self._leftScroller = False
        self._rightScroller = False
        minLabelLen = 0
        for label in self._labels:
            labelLen = len(label)
            if xpos+labelLen > w:
                xpos = w-labelLen
                self._leftScroller = True
                self._rightScroller = True
            self._labelsPos.append(xpos)
            xpos += labelLen+1
            if minLabelLen < labelLen:
                minLabelLen = labelLen
        self.setMinimumWidth(minLabelLen+2+4)

        if self._currentIndex == -1:
            self._currentIndex = len(self._labels) -1

        if self._lastIndex != self._currentIndex:
            self._lastIndex = self._currentIndex
            self.currentChanged.emit(self._currentIndex)

        self.update()

    def resizeEvent(self, w, h):
        self._updateTabs()

    def mousePressEvent(self, evt):
        x = evt.x
        w = self.width()
        offset = self._offset
        # Check from the selected to the left and from selected+1 to the right
        if self._leftScroller and x<2 and offset>0:
            self._offset -= 1
            self._updateTabs()
            return True
        if self._rightScroller and x>w-3 and offset<len(self._labels)-1:
            self._offset += 1
            self._updateTabs()
            return True
        for i in list(reversed(range(offset+1                  )) ) + \
                 list(         range(offset+1, len(self._labels)) ) :
            posx = self._labelsPos[i]
            tablen = len(self._labels[i])+2
            if posx <= x < (posx+tablen):
                self._currentIndex = i
                self._offset = i
                self._updateTabs()
                return True
        return False

    def mouseDragEvent(self, evt):
        return False

    def wheelEvent(self, evt):
        _,y = evt.x, evt.y
        if y>2: return False
        if evt.evt == TTkK.WHEEL_Down:
            if self._currentIndex < len(self._labels)-1:
                self._currentIndex += 1
        else:
            if self._currentIndex > 0:
                self._currentIndex -= 1
        self._offset = self._currentIndex
        self._updateTabs()
        return True

    def keyEvent(self, evt):
        if evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Right:
            self._offset = min(self._offset+1,len(self._labels)-1)
            self._updateTabs()
            return True
        if evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Left:
            self._offset = max(self._offset-1,0)
            self._updateTabs()
            return True
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            self._currentIndex = self._offset
            self._updateTabs()
            return True
        return False

    def paintEvent(self):
        if self.hasFocus():
            tabColor       = self._tabColorFocus
            tabBorderColor = self._tabBorderColorFocus
            tabSelectColor = self._tabSelectColorFocus
            tabOffsetColor = self._tabOffsetColorFocus
        else:
            tabColor       = self._tabColor
            tabBorderColor = self._tabBorderColor
            tabSelectColor = self._tabSelectColor
            tabOffsetColor = self._tabOffsetColor
        self._canvas.drawTab(
                pos=(0,0), size=self.size(), slim=(self._height==2),
                labels=self._labels, labelsPos=self._labelsPos,
                selected=self._currentIndex, offset=self._offset,
                leftScroller=self._leftScroller, rightScroller=self._rightScroller,
                color=tabColor, borderColor=tabBorderColor, selectColor=tabSelectColor,
                offsetColor=tabOffsetColor, sideBorder = self._sideBorder)

'''
           ┌────────────────────────────┐
           │ Root Layout                │
           │┌────────┬────────┬────────┐│
           ││ Left M │ TABS   │ RightM ││
           │└────────┴────────┴────────┘│
           │┌──────────────────────────┐│
           ││ Layout                   ││
           ││                          ││
           │└──────────────────────────┘│
           └────────────────────────────┘
'''

class TTkTabWidget(TTkFrame):
    __slots__ = (
        '_tabBarTopLayout', '_tabBar', '_topLeftLayout', '_topRightLayout',
        '_tabColor', '_tabBorderColor', '_tabSelectColor', '_tabOffsetColor',
        '_tabColorFocus', '_tabBorderColorFocus', '_tabSelectColorFocus', '_tabOffsetColorFocus',
        '_tabWidgets', '_labels', '_labelsPos',
        '_offset', '_currentIndex',
        '_leftScroller', '_rightScroller',
        '_tabMovable', '_tabClosable')

    def __init__(self, *args, **kwargs):
        self._tabWidgets = []
        self._labels = []
        self._labelsPos = []
        self._currentIndex = 0
        self._offset = 0
        self._tabMovable = False
        self._tabClosable = False
        self._leftScroller = False
        self._rightScroller = False
        self._tabColor       = TTkCfg.theme.tabColor
        self._tabBorderColor = TTkCfg.theme.tabBorderColor
        self._tabSelectColor = TTkCfg.theme.tabSelectColor
        self._tabOffsetColor = TTkCfg.theme.tabOffsetColor
        self._tabColorFocus       = TTkCfg.theme.tabColorFocus
        self._tabBorderColorFocus = TTkCfg.theme.tabBorderColorFocus
        self._tabSelectColorFocus = TTkCfg.theme.tabSelectColorFocus
        self._tabOffsetColorFocus = TTkCfg.theme.tabOffsetColorFocus
        self._tabBar = _TTkTabs()
        self._tabBar.currentChanged.connect(self._tabChanged)
        self._tabBar.focusChanged.connect(self._focusChanged)
        self._tabBarTopLayout = TTkGridLayout()
        self._topLeftLayout   = None
        self._topRightLayout  = None
        self._tabBarTopLayout.addWidget(self._tabBar,0,1)
        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTabWidget')
        self.setLayout(TTkGridLayout())
        if self.border():
            self.setPadding(3,1,1,1)
        else:
            self.setPadding(2,0,0,0)
        self.rootLayout().addItem(self._tabBarTopLayout)
        self._tabBarTopLayout.setGeometry(0,0,self._width,self._padt)

    @pyTTkSlot(int)
    def _tabChanged(self, index):
        for i, widget in enumerate(self._tabWidgets):
            if index == i:
                widget.show()
            else:
                widget.hide()

    @pyTTkSlot(bool)
    def _focusChanged(self, focus):
        if focus:
            tabBorderColor = self._tabBorderColorFocus
        else:
            tabBorderColor = self._tabBorderColor

        for widget in self._tabBarTopLayout.iterWidgets():
            widget.setBorderColor(tabBorderColor)
            widget.update()

    def addMenu(self, text, position=TTkK.LEFT):
        button = _TTkTabMenuButton(text=text, borderColor=self._tabBorderColor, menuOffset=(-1,1) if self.border() else (-1,0) , tabPosition=position)
        button.focusChanged.connect(self._focusChanged)
        if position==TTkK.LEFT:
            if not self._topLeftLayout:
                self._topLeftLayout = TTkHBoxLayout()
                self._tabBarTopLayout.addItem(self._topLeftLayout,0,0)
                button.setSideBorder(TTkK.LEFT)
            layout = self._topLeftLayout
        else:
            if not self._topRightLayout:
                self._topRightLayout = TTkHBoxLayout()
                self._tabBarTopLayout.addItem(self._topRightLayout,0,2)
            layout = self._topRightLayout
            button.setSideBorder(TTkK.RIGHT)
            for b in self._topRightLayout.iterWidgets(onlyVisible=False):
                b.unsetSideBorder(TTkK.RIGHT)
        self._tabBar.unsetSideBorder(position)
        layout.addWidget(button)
        return button

    def addTab(self, widget, label):
        widget.hide()
        self._tabWidgets.append(widget)
        self.layout().addWidget(widget)
        self._tabBar.addTab(label)

    def insertTab(self, index, widget, label):
        widget.hide()
        self._tabWidgets.insert(index, widget)
        self.layout().addWidget(widget)
        self._tabBar.insertTab(index, label)

    def resizeEvent(self, w, h):
        self._tabBarTopLayout.setGeometry(0,0,w,self._padt)

    def paintEvent(self):
        if any(w.hasFocus() for w in self._tabBarTopLayout.iterWidgets()):
            tabBorderColor = self._tabBorderColorFocus
        else:
            tabBorderColor = self._tabBorderColor
        if self.border():
            self._canvas.drawBox(pos=(0,2),size=(self._width,self._height-2), color=tabBorderColor, grid=9)
