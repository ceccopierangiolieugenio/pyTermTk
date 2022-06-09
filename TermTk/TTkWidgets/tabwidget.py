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
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.string import TTkString
from TermTk.TTkGui.drag import TTkDrag
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.spacer import TTkSpacer
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.menubar import TTkMenuButton
from TermTk.TTkLayouts.boxlayout import TTkHBoxLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout

class _TTkTabWidgetDragData():
    __slots__ = ('_tabButton', '_tabWidget')
    def __init__(self, b, tw):
        self._tabButton = b
        self._tabWidget = tw
    def tabButton(self): return self._tabButton
    def tabWidget(self): return self._tabWidget

class _TTkTabBarDragData():
    __slots__ = ('_tabButton','_tabBar')
    def __init__(self, b, tb):
        self._tabButton = b
        self._tabBar = tb
    def tabButton(self): return self._tabButton
    def tabBar(self): return self._tabBar

class TTkTabButton(TTkButton):
    __slots__ = ('_sideEnd', '_tabStatus', '_closable', 'closeClicked', '_closeButton')
    def __init__(self, *args, **kwargs):
        self._sideEnd = TTkK.NONE
        self._tabStatus = TTkK.Unchecked
        self._closable = kwargs.get('closable', False)
        self.closeClicked = pyTTkSignal()
        TTkButton.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTabButton' )
        size = len(self.text) + 2
        if self._closable:
            size += 3
            self._closeButton = TTkButton(parent=self, border=False, text="x", pos=(size-4,1 if self._border else 0), size=(3,1))
            self._closeButton.setFocusPolicy(TTkK.ParentFocus)
            self._closeButton.clicked.connect(self.closeClicked.emit)
        if self._border:
            self.resize(size, 3)
            self.setMinimumSize(size, 3)
            self.setMaximumSize(size, 3)
        else:
            self.resize(size, 2)
            self.setMinimumSize(size, 2)
            self.setMaximumSize(size, 2)
        self.setFocusPolicy(TTkK.ParentFocus)

    def sideEnd(self):
        return self._sideEnd

    def setSideEnd(self, sideEnd):
        self._sideEnd = sideEnd
        self.update()

    def tabStatus(self):
        return self._tabStatus

    def setTabStatus(self, status):
        self._tabStatus = status
        self.update()

    # This is a hack to force the action aftet the keypress
    # And not key release as normally happen to the button
    def mousePressEvent(self, evt):
        if  self._closable and evt.key == TTkK.MidButton:
            self.closeClicked.emit()
            return True
        return super().mouseReleaseEvent(evt)
    def mouseReleaseEvent(self, evt):
        return False
    def mouseDragEvent(self, evt) -> bool:
        drag = TTkDrag()
        if tb := self.parentWidget():
            if issubclass(type(tb),TTkTabBar):
                if tw:= tb.parentWidget():
                    # Init the drag only if used in a tabBar/tabWidget
                    if issubclass(type(tw), TTkTabWidget):
                        data = _TTkTabWidgetDragData(self,tw)
                    else:
                        data = _TTkTabBarDragData(self,tb)
                    drag.setPixmap(self)
                    drag.setData(data)
                    drag.exec()
                    return True
        return super().mouseDragEvent(evt)

    def paintEvent(self):
        self._canvas.drawTabButton(
            pos=(0,0), size=self.size(),
            small=(not self._border),
            sideEnd=self._sideEnd, status=self._tabStatus,
            color=self._borderColor )
        self._canvas.drawText(pos=(1,1 if self._border else 0), text=self.text, color=self.color())

class _TTkTabMenuButton(TTkMenuButton):
    def __init__(self, *args, **kwargs):
        TTkMenuButton.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTabMenuButton')

    def paintEvent(self):
        if self._pressed:
            borderColor = self._borderColor
            textColor   = TTkCfg.theme.menuButtonColorClicked
            scColor     = TTkCfg.theme.menuButtonShortcutColor
        else:
            borderColor = self._borderColor
            textColor   = self._color
            scColor     =  TTkCfg.theme.menuButtonShortcutColor
        text = TTkString('[',borderColor) + TTkString(self.text,textColor) + TTkString(']',borderColor)
        self._canvas.drawText(pos=(0,0),text=text)

class _TTkTabScrollerButton(TTkButton):
    __slots__ = ('_side', '_sideEnd')
    def __init__(self, *args, **kwargs):
        self._side = kwargs.get('side',TTkK.LEFT)
        self._sideEnd = self._side
        TTkButton.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTabScrollerButton' )
        if self._border:
            self.resize(2, 3)
            self.setMinimumSize(2, 3)
            self.setMaximumSize(2, 3)
        else:
            self.resize(2, 2)
            self.setMinimumSize(2, 2)
            self.setMaximumSize(2, 2)
        self.setFocusPolicy(TTkK.ParentFocus)

    def side(self):
        return self._side

    def setSide(self, side):
        self._side = side
        self.update()

    def sideEnd(self):
        return self._sideEnd

    def setSideEnd(self, sideEnd):
        self._sideEnd = sideEnd
        self.update()

    # This is a hack to force the action aftet the keypress
    # And not key release as normally happen to the button
    def mousePressEvent(self, evt):
        return super().mouseReleaseEvent(evt)
    def mouseReleaseEvent(self, evt):
        return False
    def mouseTapEvent(self, evt) -> bool:
        self.clicked.emit()
        return True

    def paintEvent(self):
        tt = TTkCfg.theme.tab
        if self._border:
            lse = tt[11] if self._sideEnd &  TTkK.LEFT  else tt[13]
            rse = tt[15] if self._sideEnd &  TTkK.RIGHT else tt[13]
            if self._side == TTkK.LEFT:
                self._canvas.drawText(pos=(0,0), color=self._borderColor, text=tt[7] +tt[1])
                self._canvas.drawText(pos=(0,1), color=self._borderColor, text=tt[9] +tt[31])
                self._canvas.drawText(pos=(0,2), color=self._borderColor, text=lse   +tt[12])
                self._canvas.drawChar(pos=(1,1), char=tt[31], color=TTkCfg.theme.tabOffsetColor)
            else:
                self._canvas.drawText(pos=(0,0), color=self._borderColor, text=tt[1] +tt[8])
                self._canvas.drawText(pos=(0,1), color=self._borderColor, text=tt[32]+tt[9])
                self._canvas.drawText(pos=(0,2), color=self._borderColor, text=tt[12]+rse)
                self._canvas.drawChar(pos=(0,1), char=tt[32], color=TTkCfg.theme.tabOffsetColor)
        else:
            if self._side == TTkK.LEFT:
                self._canvas.drawText(pos=(0,0), color=self._borderColor, text=tt[9] +tt[31])
                self._canvas.drawText(pos=(0,1), color=self._borderColor, text=tt[23]+tt[1])
                self._canvas.drawChar(pos=(1,0), char=tt[31], color=TTkCfg.theme.tabOffsetColor)
            else:
                self._canvas.drawText(pos=(0,0), color=self._borderColor, text=tt[32]+tt[9])
                self._canvas.drawText(pos=(0,1), color=self._borderColor, text=tt[1] +tt[24])
                self._canvas.drawChar(pos=(0,0), char=tt[32], color=TTkCfg.theme.tabOffsetColor)
'''
_curentIndex =              2
_tabButtons  =    [0],[1],  [2],   [3],   [4],
                ╭─┌──┌──────╔══════╗──────┬──────┐─╮
_labels=        │◀│La│Label1║Label2║Label3│Label4│▶│
                ╞═══════════╩══════╩═══════════════╡
                 leftscroller                     rightScroller
'''

class TTkTabBar(TTkWidget):
    __slots__ = (
        '_tabButtons', '_tabData', '_small',
        '_highlighted', '_currentIndex','_lastIndex',
        '_leftScroller', '_rightScroller',
        '_borderColor', '_tabClosable',
        '_sideEnd',
        #Signals
        'currentChanged', 'tabBarClicked', 'tabCloseRequested')

    def __init__(self, *args, **kwargs):
        self._tabButtons = []
        self._tabData = []
        self._currentIndex = -1
        self._lastIndex = -1
        self._highlighted = -1
        self._tabMovable = False
        self._tabClosable = kwargs.get('closable',False)
        self._sideEnd = TTkK.LEFT | TTkK.RIGHT
        self._borderColor = TTkCfg.theme.tabBorderColor
        self._small = kwargs.get('small',True)
        self._leftScroller =  _TTkTabScrollerButton(border=not self._small,side=TTkK.LEFT)
        self._rightScroller = _TTkTabScrollerButton(border=not self._small,side=TTkK.RIGHT)
        self._leftScroller.clicked.connect( self._moveToTheLeft)
        self._rightScroller.clicked.connect(self._andMoveToTheRight)

        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTabs')
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)
        self.focusChanged.connect(self._focusChanged)


        # Add and connect the scrollers
        self.layout().addWidget(self._leftScroller)
        self.layout().addWidget(self._rightScroller)

        # Signals
        self.currentChanged    = pyTTkSignal(int)
        self.tabBarClicked     = pyTTkSignal(int)
        self.tabCloseRequested = pyTTkSignal(int)

        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def sideEnd(self):
        return self._sideEnd

    def setSideEnd(self, sideEnd):
        self._sideEnd = sideEnd
        self._rightScroller.setSideEnd(sideEnd&TTkK.RIGHT)
        self._leftScroller.setSideEnd(sideEnd&TTkK.LEFT)
        self._updateTabs()

    def addTab(self, label, data=None):
        self.insertTab(len(self._tabButtons), label, data)

    def insertTab(self, index, label, data=None):
        if index <= self._currentIndex:
            self._currentIndex += 1
        button = TTkTabButton(parent=self, text=label, border=not self._small, closable=self._tabClosable)
        button._borderColor = self._borderColor
        self._tabButtons.insert(index,button)
        self._tabData.insert(index,data)
        button.clicked.connect(lambda :self.setCurrentIndex(self._tabButtons.index(button)))
        button.closeClicked.connect(lambda :self.tabCloseRequested.emit(self._tabButtons.index(button)))
        self._updateTabs()

    @pyTTkSlot(int)
    def removeTab(self, index):
        button = self._tabButtons[index]
        self.layout().removeWidget(button)
        self._tabButtons.pop(index)
        self._tabData.pop(index)
        if self._currentIndex == index:
            self._lastIndex = -2
        if self._currentIndex >= index:
            self._currentIndex -= 1
        self._highlighted = self._currentIndex
        self._updateTabs()

    def data(self, index):
        return self._tabData[index]

    def setData(self, index, data):
        self._tabData[index] = data

    def borderColor(self):
        return self._borderColor

    def setBorderColor(self, color):
        self._borderColor = color
        for b in self._tabButtons:
            b.setBorderColor(color)
        self._leftScroller.setBorderColor(color)
        self._rightScroller.setBorderColor(color)
        self.update()

    def tabsClosable(self):
        return self._tabClosable

    def setTabsClosable(self, closable):
        self._tabClosable = closable

    def currentIndex(self):
        return self._currentIndex

    @pyTTkSlot(int)
    def setCurrentIndex(self, index):
        TTkLog.debug(index)
        if 0 <= index < len(self._tabButtons):
            self._currentIndex = index
            self._highlighted = index
            self._updateTabs()

    def resizeEvent(self, w, h):
        self._updateTabs()

    def _updateTabs(self):
        w = self.width()
        # Find the tabs used size max size
        maxLen = 0
        sizes = [t.width()-1 for t in self._tabButtons]
        for s in sizes: maxLen += s
        if maxLen <= w:
            self._leftScroller.hide()
            self._rightScroller.hide()
            shrink = 1
            offx = 0
        else:
            self._leftScroller.show()
            self._rightScroller.show()
            self._rightScroller.move(w-2,0)
            w-=4
            shrink = w/maxLen
            offx = 2

        posx=0
        for t in self._tabButtons:
            tmpx = offx+min(int(posx*shrink),w-t.width())
            sideEnd = TTkK.NONE
            if tmpx==0:
                sideEnd |= self.sideEnd() & TTkK.LEFT
            if tmpx+t.width()==self.width():
                sideEnd |= self.sideEnd() & TTkK.RIGHT
            t.move(tmpx,0)
            t.setSideEnd(sideEnd)
            posx += t.width()-1

        # ZReorder the widgets:
        for i in range(0,max(0,self._currentIndex)):
            self._tabButtons[i].raiseWidget()
        for i in reversed(range(max(0,self._currentIndex),len(self._tabButtons))):
            self._tabButtons[i].raiseWidget()

        if self._currentIndex == -1:
            self._currentIndex = len(self._tabButtons)-1

        if self._lastIndex != self._currentIndex:
            self._lastIndex = self._currentIndex
            self.currentChanged.emit(self._currentIndex)

        # set the buttons text color based on the selection/offset
        for i,b in enumerate(self._tabButtons):
            if i == self._highlighted != self._currentIndex:
                b.setColor(TTkCfg.theme.tabOffsetColor)
                b.setTabStatus(TTkK.PartiallyChecked)
                b.raiseWidget()
            elif i == self._currentIndex:
                b.setColor(TTkCfg.theme.tabSelectColor)
                b.setTabStatus(TTkK.Checked)
            else:
                b.setColor(TTkCfg.theme.tabColor)
                b.setTabStatus(TTkK.Unchecked)

        self.update()

    def _moveToTheLeft(self):
        self._currentIndex = max(self._currentIndex-1,0)
        self._highlighted = self._currentIndex
        self._updateTabs()

    def _andMoveToTheRight(self):
        self._currentIndex = min(self._currentIndex+1,len(self._tabButtons)-1)
        self._highlighted = self._currentIndex
        self._updateTabs()

    def wheelEvent(self, evt):
        if evt.evt == TTkK.WHEEL_Up:
            self._moveToTheLeft()
        else:
            self._andMoveToTheRight()
        return True

    def keyEvent(self, evt):
        if evt.type == TTkK.SpecialKey:
            if evt.key == TTkK.Key_Right:
                self._highlighted = min(self._highlighted+1,len(self._tabButtons)-1)
                self._updateTabs()
                return True
            elif evt.key == TTkK.Key_Left:
                self._highlighted = max(self._highlighted-1,0)
                self._updateTabs()
                return True
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            self._currentIndex = self._highlighted
            self._updateTabs()
            return True
        return False

    @pyTTkSlot(bool)
    def _focusChanged(self, focus):
        if focus:
            borderColor = TTkCfg.theme.tabBorderColorFocus
        else:
            borderColor = TTkCfg.theme.tabBorderColor
        self.setBorderColor(borderColor)


    def paintEvent(self):
        w = self.width()
        tt = TTkCfg.theme.tab
        if self._small:
            lse = tt[23] if self._sideEnd &  TTkK.LEFT  else tt[19]
            rse = tt[24] if self._sideEnd &  TTkK.RIGHT else tt[19]
            self._canvas.drawText(pos=(0,1),text=lse + tt[19]*(w-2) + rse, color=self._borderColor)
        else:
            lse = tt[11] if self._sideEnd &  TTkK.LEFT  else tt[12]
            rse = tt[15] if self._sideEnd &  TTkK.RIGHT else tt[12]
            self._canvas.drawText(pos=(0,2),text=lse + tt[12]*(w-2) + rse, color=self._borderColor)


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
                          ╭─┌──┌──────╔══════╗──────┬──────┐─╮
                ┌[M1]┬[M2]┤◀│La│Label1║Label2║Label3│Label4│▶│
                ╞════╧════╧═══════════╩══════╩═══════════════╡
                 leftscroller                     rightScroller
'''

class TTkTabWidget(TTkFrame):
    __slots__ = (
        '_tabBarTopLayout', '_tabBar', '_topLeftLayout', '_topRightLayout',
        '_tabWidgets', '_spacer',
        # Forward Signals
        'currentChanged', 'tabBarClicked',
        # forward methods
        'tabsClosable', 'setTabsClosable',
        'data', 'setData',
        'currentIndex', 'setCurrentIndex', 'tabCloseRequested')

    def __init__(self, *args, **kwargs):
        self._tabWidgets = []
        self._tabBarTopLayout = TTkGridLayout()
        self._borderColor = TTkCfg.theme.tabBorderColor

        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTabWidget')

        self._tabBar = TTkTabBar(small = not self.border(), closable=kwargs.get('closable', False))
        self._topLeftLayout   = None
        self._topRightLayout  = None
        self._tabBarTopLayout.addWidget(self._tabBar,0,1,3 if self.border() else 2,1)

        self._tabBar.currentChanged.connect(self._tabChanged)
        self.setFocusPolicy(self._tabBar.focusPolicy())
        self._tabBar.setFocusPolicy(TTkK.ParentFocus)
        self.focusChanged.connect(self._focusChanged)

        self._spacer = TTkSpacer(parent=self)

        self.setLayout(TTkGridLayout())
        if self.border():
            self.setPadding(3,1,1,1)
        else:
            self.setPadding(2,0,0,0)

        self.rootLayout().addItem(self._tabBarTopLayout)
        self._tabBarTopLayout.setGeometry(0,0,self._width,self._padt)
        self._tabBar.tabCloseRequested.connect(self.removeTab)
        # forwarded methods
        self.currentIndex    = self._tabBar.currentIndex
        self.setCurrentIndex = self._tabBar.setCurrentIndex
        self.data    = self._tabBar.data
        self.setData = self._tabBar.setData
        self.tabsClosable    = self._tabBar.tabsClosable
        self.setTabsClosable = self._tabBar.setTabsClosable
        # forwarded Signals
        self.currentChanged    = self._tabBar.currentChanged
        self.tabBarClicked     = self._tabBar.tabBarClicked
        self.tabCloseRequested = self._tabBar.tabCloseRequested

    def widget(self, index):
        return self._tabWidgets[index]

    def currentWidget(self):
        for w in self._tabWidgets:
            if w.isVisible():
                return w
        return self._spacer

    @pyTTkSlot(TTkWidget)
    def setCurrentWidget(self, widget):
        for i, w in enumerate(self._tabWidgets):
            if widget == w:
                self.setCurrentIndex(i)
                break

    @pyTTkSlot(int)
    def _tabChanged(self, index):
        self._spacer.show()
        for i, widget in enumerate(self._tabWidgets):
            if index == i:
                widget.show()
                self._spacer.hide()
            else:
                widget.hide()

    @pyTTkSlot(bool)
    def _focusChanged(self, focus):
        if focus:
            borderColor = TTkCfg.theme.tabBorderColorFocus
        else:
            borderColor = TTkCfg.theme.tabBorderColor
        self.setBorderColor(borderColor)
        self._tabBar.setBorderColor(borderColor)

    def keyEvent(self, evt) -> bool:
        return self._tabBar.keyEvent(evt)

    def dropEvent(self, evt) -> bool:
        data = evt.data()
        x, y = evt.x, evt.y
        if not issubclass(type  (data),_TTkTabWidgetDragData):
            return False
        tb = data.tabButton()
        tw = data.tabWidget()
        index  = tw._tabBar._tabButtons.index(tb)
        widget = tw.widget(index)
        data   = tw.data(index)
        if TTkHelper.isParent(self, tw):
            return False
        if y < 3:
            tbx = self._tabBar.x()
            newIndex = 0
            for b in self._tabBar._tabButtons:
                if tbx+b.x()+b.width()/2 < x:
                    newIndex += 1
            if tw == self:
                if index <= newIndex:
                    newIndex -= 1
            tw.removeTab(index)
            self.insertTab(newIndex, widget, tb.text, data)
            self.setCurrentIndex(newIndex)
            #self._tabChanged(newIndex)
        elif tw != self:
            tw.removeTab(index)
            newIndex = len(self._tabWidgets)
            self.addTab(widget, tb.text, data)
            self.setCurrentIndex(newIndex)
            self._tabChanged(newIndex)

        TTkLog.debug(f"Drop -> pos={evt.pos()}")
        return True

    def addMenu(self, text, position=TTkK.LEFT):
        button = _TTkTabMenuButton(text=text, borderColor=TTkCfg.theme.tabBorderColor)
        self._tabBar.setSideEnd(self._tabBar.sideEnd() & ~position)
        if position==TTkK.LEFT:
            if not self._topLeftLayout:
                self._topLeftLayout = TTkHBoxLayout()
                self._tabBarTopLayout.addItem(self._topLeftLayout,1 if self.border() else 0,0)
            layout = self._topLeftLayout
        else:
            if not self._topRightLayout:
                self._topRightLayout = TTkHBoxLayout()
                self._tabBarTopLayout.addItem(self._topRightLayout,1 if self.border() else 0,2)
            layout = self._topRightLayout
        layout.addWidget(button)
        return button

    def addTab(self, widget, label, data=None):
        widget.hide()
        self._tabWidgets.append(widget)
        self.layout().addWidget(widget)
        self._tabBar.addTab(label, data)

    def insertTab(self, index, widget, label, data=None):
        widget.hide()
        self._tabWidgets.insert(index, widget)
        self.layout().addWidget(widget)
        self._tabBar.insertTab(index, label, data)

    @pyTTkSlot(int)
    def removeTab(self, index):
        self.layout().removeWidget(self._tabWidgets[index])
        self._tabWidgets.pop(index)
        self._tabBar.removeTab(index)

    def resizeEvent(self, w, h):
        self._tabBarTopLayout.setGeometry(0,0,w,self._padt)

    def paintEvent(self):
        tt = TTkCfg.theme.tab
        if self.border():
            self._canvas.drawBox(pos=(0,2),size=(self.width(),self.height()-2), color=self._borderColor, grid=9)
        else:
            self._canvas.drawText(pos=(0,1),text=tt[36] + tt[19]*(self.width()-2) + tt[35], color=self._borderColor)
