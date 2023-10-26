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

__all__ = ['TTkTabButton', 'TTkTabBar', 'TTkTabWidget']

from TermTk.TTkCore.constant import  TTkK
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.string import TTkString
from TermTk.TTkGui.drag import TTkDrag
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.spacer import TTkSpacer
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.menubar import TTkMenuBarButton
from TermTk.TTkLayouts.boxlayout import TTkHBoxLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout

_tabStyle  = {
            'default':     {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000044"),
                            'borderColor': TTkColor.RST,
                            'tabOffsetColor': TTkColor.RST},
            'disabled':    {'color': TTkColor.fg('#888888'),
                            'borderColor':TTkColor.fg('#888888'),
                            'tabOffsetColor': TTkColor.RST},
            'focus':       {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000044")+TTkColor.BOLD,
                            'borderColor': TTkColor.fg("#ffff00") + TTkColor.BOLD,
                            'tabOffsetColor': TTkColor.RST},
        }

_tabStyleNormal = {
            'default':     {'borderColor': TTkColor.RST},
        }

_tabStyleFocussed = {
            'default':     {'borderColor': TTkColor.fg("#ffff00") + TTkColor.BOLD},
        }

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

class _TTkTabColorButton(TTkContainer):
    classStyle = _tabStyle | {
                'hover':       {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000050")+TTkColor.BOLD,
                                'borderColor': TTkColor.fg("#AAFFFF")+TTkColor.BOLD},
            }

    __slots__ = (
        '_text', '_border',
        # Signals
        'clicked'
        )
    def __init__(self, *, text="", border=True, **kwargs):
        self.clicked = pyTTkSignal()

        self._text = TTkString(text.replace('\n',''))
        self._border = border

        super().__init__(forwardStyle=True, **kwargs)

    def text(self) -> TTkString:
        return self._text

    def mouseReleaseEvent(self, evt):
        self.clicked.emit()
        return True

    def keyEvent(self, evt):
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            self._keyPressed = True
            self._pressed = True
            self.update()
            self.clicked.emit()
            return True
        return False

class TTkTabButton(_TTkTabColorButton):
    '''TTkTabButton'''
    __slots__ = ('_data','_sideEnd', '_tabStatus', '_closable', 'closeClicked', '_closeButtonPressed','_data')
    def __init__(self, *, data=None, closable=False, **kwargs):
        self._sideEnd = TTkK.NONE
        self._tabStatus = TTkK.Unchecked
        self._data = data
        self._closable = closable
        self.closeClicked = pyTTkSignal()
        super().__init__(**kwargs)
        self._closeButtonPressed = False
        size = self.text().termWidth() + 2
        if self._closable:
            size += 3
        if self._border:
            self.resize(size, 3)
            self.setMinimumSize(size, 3)
            self.setMaximumSize(size, 3)
        else:
            self.resize(size, 2)
            self.setMinimumSize(size, 2)
            self.setMaximumSize(size, 2)
        self.setFocusPolicy(TTkK.ParentFocus)

    def data(self):
        return self._data

    def setData(self, data):
        self._data=data

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
        x,y = evt.x,evt.y
        w,h = self.size()
        self._closeButtonPressed = False
        if  self._closable and evt.key == TTkK.MidButton:
            self.closeClicked.emit()
            return True
        if self._closable and y == (1 if self._border else 0) and w-4<=x<w-1:
            self._closeButtonPressed = True
            return True
        return super().mouseReleaseEvent(evt)
    def mouseReleaseEvent(self, evt):
        x,y = evt.x,evt.y
        w,h = self.size()
        if self._closable and y == (1 if self._border else 0) and w-4<=x<w-1 and self._closeButtonPressed:
            self._closeButtonPressed = False
            self.closeClicked.emit()
            return True
        self._closeButtonPressed = False
        return False
    def mouseDragEvent(self, evt) -> bool:
        drag = TTkDrag()
        self._closeButtonPressed = False
        if tb := self.parentWidget():
            if issubclass(type(tb),TTkTabBar):
                if tw:= tb.parentWidget():
                    # Init the drag only if used in a tabBar/tabWidget
                    if issubclass(type(tw), TTkTabWidget):
                        data = _TTkTabWidgetDragData(self,tw)
                    else:
                        data = _TTkTabBarDragData(self,tb)
                    pm = TTkCanvas(width=self.width(),height=3)
                    pm.drawBox(pos=(0,0),size=(self.width(),3))
                    pm.drawText(pos=(1,1), text=self.text(), color=self.currentStyle()['color'])
                    drag.setPixmap(pm)
                    # drag.setPixmap(self)
                    drag.setData(data)
                    drag.exec()
                    return True
        return super().mouseDragEvent(evt)

    def paintEvent(self, canvas):
        style = self.currentStyle()

        borderColor = style['borderColor']
        textColor   = style['color']

        w,h = self.size()

        canvas.drawTabButton(
            pos=(0,0), size=self.size(),
            small=(not self._border),
            sideEnd=self._sideEnd, status=self._tabStatus,
            color=borderColor )
        canvas.drawText(pos=(1,1 if self._border else 0), text=self.text(), color=textColor)
        if self._closable:
            canvas.drawText(pos=(w-4,1 if self._border else 0), text="[X]", color=textColor)

class _TTkTabMenuButton(TTkMenuBarButton):
    def paintEvent(self, canvas):
        style = self.currentStyle()
        borderColor = style['borderColor']
        textColor   = style['color']
        text = TTkString('[',borderColor) + TTkString(self.text(),textColor) + TTkString(']',borderColor)
        canvas.drawText(pos=(0,0),text=text)

class _TTkTabScrollerButton(_TTkTabColorButton):
    classStyle = _tabStyle
    __slots__ = ('_side', '_sideEnd')
    def __init__(self, *args, **kwargs):
        self._side = kwargs.get('side',TTkK.LEFT)
        self._sideEnd = self._side
        super().__init__(*args, **kwargs)
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

    def paintEvent(self, canvas):
        style = self.currentStyle()
        borderColor = style['borderColor']
        offsetColor = style['tabOffsetColor']
        # textColor   = style['color']

        tt = TTkCfg.theme.tab
        if self._border:
            lse = tt[11] if self._sideEnd &  TTkK.LEFT  else tt[13]
            rse = tt[15] if self._sideEnd &  TTkK.RIGHT else tt[13]
            if self._side == TTkK.LEFT:
                canvas.drawText(pos=(0,0), color=borderColor, text=tt[7] +tt[1])
                canvas.drawText(pos=(0,1), color=borderColor, text=tt[9] +tt[31])
                canvas.drawText(pos=(0,2), color=borderColor, text=lse   +tt[12])
                canvas.drawChar(pos=(1,1), char=tt[31], color=offsetColor)
            else:
                canvas.drawText(pos=(0,0), color=borderColor, text=tt[1] +tt[8])
                canvas.drawText(pos=(0,1), color=borderColor, text=tt[32]+tt[9])
                canvas.drawText(pos=(0,2), color=borderColor, text=tt[12]+rse)
                canvas.drawChar(pos=(0,1), char=tt[32], color=offsetColor)
        else:
            if self._side == TTkK.LEFT:
                canvas.drawText(pos=(0,0), color=borderColor, text=tt[9] +tt[31])
                canvas.drawText(pos=(0,1), color=borderColor, text=tt[23]+tt[1])
                canvas.drawChar(pos=(1,0), char=tt[31], color=offsetColor)
            else:
                canvas.drawText(pos=(0,0), color=borderColor, text=tt[32]+tt[9])
                canvas.drawText(pos=(0,1), color=borderColor, text=tt[1] +tt[24])
                canvas.drawChar(pos=(0,0), char=tt[32], color=offsetColor)
'''
_curentIndex =              2
_tabButtons  =    [0],[1],  [2],   [3],   [4],
                ╭─┌──┌──────╔══════╗──────┬──────┐─╮
_labels=        │◀│La│Label1║Label2║Label3│Label4│▶│
                ╞═══════════╩══════╩═══════════════╡
                 leftscroller                     rightScroller
'''

class TTkTabBar(TTkContainer):
    '''TTkTabBar'''
    classStyle = _tabStyle
    __slots__ = (
        '_tabButtons', '_tabMovable', '_small',
        '_highlighted', '_currentIndex','_lastIndex',
        '_leftScroller', '_rightScroller',
        '_tabClosable',
        '_sideEnd',
        #Signals
        'currentChanged', 'tabBarClicked', 'tabCloseRequested')

    def __init__(self, **kwargs):
        self._tabButtons = []
        self._currentIndex = -1
        self._lastIndex = -1
        self._highlighted = -1
        self._tabMovable = False
        self._tabClosable = kwargs.get('closable',False)
        self._sideEnd = TTkK.LEFT | TTkK.RIGHT
        self._small = kwargs.get('small',True)
        self._leftScroller =  _TTkTabScrollerButton(border=not self._small,side=TTkK.LEFT)
        self._rightScroller = _TTkTabScrollerButton(border=not self._small,side=TTkK.RIGHT)
        self._leftScroller.clicked.connect( self._moveToTheLeft)
        self._rightScroller.clicked.connect(self._andMoveToTheRight)

        super().__init__(forwardStyle=False, **kwargs)

        # Add and connect the scrollers
        self.layout().addWidget(self._leftScroller)
        self.layout().addWidget(self._rightScroller)

        # Signals
        self.currentChanged    = pyTTkSignal(int)
        self.tabBarClicked     = pyTTkSignal(int)
        self.tabCloseRequested = pyTTkSignal(int)

        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def mergeStyle(self, style):
        super().mergeStyle(style)
        for t in self._tabButtons:
            t.mergeStyle(style)
        self._leftScroller.mergeStyle(style)
        self._rightScroller.mergeStyle(style)

    def sideEnd(self):
        return self._sideEnd

    def setSideEnd(self, sideEnd):
        self._sideEnd = sideEnd
        self._rightScroller.setSideEnd(sideEnd&TTkK.RIGHT)
        self._leftScroller.setSideEnd(sideEnd&TTkK.LEFT)
        self._updateTabs()

    def addTab(self, label, data=None, closable=None):
        '''addTab'''
        return self.insertTab(len(self._tabButtons), label=label, data=data, closable=closable)

    def insertTab(self, index, label, data=None, closable=None):
        '''insertTab'''
        if index <= self._currentIndex:
            self._currentIndex += 1
        button = TTkTabButton(parent=self, text=label, border=not self._small, closable=self._tabClosable if closable is None else closable, data=data)
        self._tabButtons.insert(index,button)
        button.clicked.connect(lambda :self.setCurrentIndex(self._tabButtons.index(button)))
        button.clicked.connect(lambda :self.tabBarClicked.emit(self._tabButtons.index(button)))
        button.closeClicked.connect(lambda :self.tabCloseRequested.emit(self._tabButtons.index(button)))
        self._updateTabs()
        return index

    @pyTTkSlot(int)
    def removeTab(self, index):
        '''removeTab'''
        button = self._tabButtons[index]
        button.clicked.clear()
        button.closeClicked.clear()
        self.layout().removeWidget(button)
        self._tabButtons.pop(index)
        if self._currentIndex == index:
            self._lastIndex = -2
        if self._currentIndex >= index:
            self._currentIndex -= 1
        self._highlighted = self._currentIndex
        self._updateTabs()

    def currentData(self):
        return self.tabData(self._currentIndex)

    def tabData(self, index):
        '''tabData'''
        if 0 <= index < len(self._tabButtons):
            return self._tabButtons[index].data()
        return None

    def setTabData(self, index, data):
        '''setTabData'''
        self._tabButtons[index].setData(data)

    def tabsClosable(self):
        '''tabsClosable'''
        return self._tabClosable

    def setTabsClosable(self, closable):
        '''setTabsClosable'''
        self._tabClosable = closable

    def currentIndex(self):
        '''currentIndex'''
        return self._currentIndex

    @pyTTkSlot(int)
    def setCurrentIndex(self, index):
        '''setCurrentIndex'''
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
                b.setTabStatus(TTkK.PartiallyChecked)
                b.raiseWidget()
            elif i == self._currentIndex:
                b.setTabStatus(TTkK.Checked)
            else:
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

    def paintEvent(self, canvas):
        style = self.currentStyle()
        borderColor = style['borderColor']
        w = self.width()
        tt = TTkCfg.theme.tab
        if self._small:
            lse = tt[23] if self._sideEnd &  TTkK.LEFT  else tt[19]
            rse = tt[24] if self._sideEnd &  TTkK.RIGHT else tt[19]
            canvas.drawText(pos=(0,1),text=lse + tt[19]*(w-2) + rse, color=borderColor)
        else:
            lse = tt[11] if self._sideEnd &  TTkK.LEFT  else tt[12]
            rse = tt[15] if self._sideEnd &  TTkK.RIGHT else tt[12]
            canvas.drawText(pos=(0,2),text=lse + tt[12]*(w-2) + rse, color=borderColor)


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
    '''TTkTabWidget'''
    classStyle = _tabStyle
    __slots__ = (
        '_tabBarTopLayout', '_tabBar', '_topLeftLayout', '_topRightLayout',
        '_tabWidgets', '_spacer',
        # Forward Signals
        'currentChanged', 'tabBarClicked',
        # forward methods
        'tabsClosable', 'setTabsClosable',
        'tabData', 'setTabData', 'currentData',
        'currentIndex', 'setCurrentIndex', 'tabCloseRequested')

    def __init__(self, **kwargs):
        self._tabWidgets = []
        self._tabBarTopLayout = TTkGridLayout()

        super().__init__(forwardStyle=False, **kwargs)

        self._tabBar = TTkTabBar(small = not self.border(), closable=kwargs.get('closable', False))
        self._topLeftLayout   = None
        self._topRightLayout  = None
        self._tabBarTopLayout.addWidget(self._tabBar,0,1,3 if self.border() else 2,1)

        self._tabBar.currentChanged.connect(self._tabChanged)
        self.setFocusPolicy(self._tabBar.focusPolicy())
        self._tabBar.setFocusPolicy(TTkK.ParentFocus)

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
        self.tabData     = self._tabBar.tabData
        self.setTabData  = self._tabBar.setTabData
        self.currentData = self._tabBar.currentData
        self.tabsClosable    = self._tabBar.tabsClosable
        self.setTabsClosable = self._tabBar.setTabsClosable
        # forwarded Signals
        self.currentChanged    = self._tabBar.currentChanged
        self.tabBarClicked     = self._tabBar.tabBarClicked
        self.tabCloseRequested = pyTTkSignal(int)

        self.focusChanged.connect(self._focusChanged)

    def _focusChanged(self, focus):
        if focus:
            self._tabBar.mergeStyle(_tabStyleFocussed)
        else:
            self._tabBar.mergeStyle(_tabStyleNormal)

    def count(self) -> int:
        return len(self._tabWidgets)

    def widget(self, index):
        '''widget'''
        if 0 <= index < len(self._tabWidgets):
            return self._tabWidgets[index]
        return None

    def currentWidget(self):
        '''currentWidget'''
        for w in self._tabWidgets:
            if w.isVisible():
                return w
        return self._spacer

    @pyTTkSlot(TTkWidget)
    def setCurrentWidget(self, widget):
        '''setCurrentWidget'''
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
        data   = tw.tabData(index)
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
            self.insertTab(newIndex, widget, tb.text(), data, tb._closable)
            self.setCurrentIndex(newIndex)
            #self._tabChanged(newIndex)
        elif tw != self:
            tw.removeTab(index)
            newIndex = len(self._tabWidgets)
            self.addTab(widget, tb.text(), data)
            self.setCurrentIndex(newIndex)
            self._tabChanged(newIndex)

        TTkLog.debug(f"Drop -> pos={evt.pos()}")
        return True

    def addMenu(self, text, position=TTkK.LEFT, data=None) -> TTkMenuBarButton:
        '''addMenu'''
        button = _TTkTabMenuButton(text=text, data=data)
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
        self._tabBarTopLayout.update()
        return button

    def addTab(self, widget, label, data=None, closable=None):
        '''addTab'''
        widget.hide()
        self._tabWidgets.append(widget)
        self.layout().addWidget(widget)
        self._tabBar.addTab(label, data, closable)

    def insertTab(self, index, widget, label, data=None, closable=None):
        '''insertTab'''
        widget.hide()
        self._tabWidgets.insert(index, widget)
        self.layout().addWidget(widget)
        self._tabBar.insertTab(index, label, data, closable)

    @pyTTkSlot(int)
    def removeTab(self, index):
        '''removeTab'''
        self.tabCloseRequested.emit(index)
        self.layout().removeWidget(self._tabWidgets[index])
        self._tabWidgets.pop(index)
        self._tabBar.removeTab(index)

    def resizeEvent(self, w, h):
        self._tabBarTopLayout.setGeometry(0,0,w,self._padt)

    def paintEvent(self, canvas):
        style = self.currentStyle()
        borderColor = style['borderColor']
        tt = TTkCfg.theme.tab
        if self.border():
            canvas.drawBox(pos=(0,2),size=(self.width(),self.height()-2), color=borderColor, grid=9)
        else:
            canvas.drawText(pos=(0,1),text=tt[36] + tt[19]*(self.width()-2) + tt[35], color=borderColor)
