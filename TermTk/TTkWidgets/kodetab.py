# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkKodeTab']

from TermTk.TTkCore.constant import  TTkK
from TermTk.TTkCore.helper import  TTkHelper
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.color import TTkColor, TTkColorGradient
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.tabwidget import TTkTabWidget
from TermTk.TTkWidgets.splitter import TTkSplitter
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkLayouts.gridlayout import TTkGridLayout

class _KolorFrame(TTkFrame):
    __slots__ = ('_fillColor')
    def __init__(self, *args, **kwargs):
        TTkFrame.__init__(self, *args, **kwargs)
        self._fillColor = kwargs.get('fillColor', TTkColor.RST)

    def setFillColor(self, color):
        self._fillColor = color

    def paintEvent(self, canvas):
        w,h = self.size()
        for y in range(h):
            canvas.drawText(pos=(0,y),text='',width=w,color=self._fillColor)
        return super().paintEvent()

class _TTkKodeTab(TTkTabWidget):
    __slots__ = (
        '_frameOverlay','_baseWidget')
    def __init__(self, baseWidget, *args, **kwargs):
        self._baseWidget = baseWidget
        TTkTabWidget.__init__(self, *args, **kwargs)
        self._frameOverlay = None
        self.tabBarClicked.connect(    lambda i:self._baseWidget.tabBarClicked.emit(    self, i, self.widget(i), self.tabData(i)))
        self.currentChanged.connect(   lambda i:self._baseWidget.currentChanged.emit(   self, i, self.widget(i), self.tabData(i)))
        self.tabCloseRequested.connect(lambda i:self._baseWidget.tabCloseRequested.emit(self, i))
        self.tabCloseRequested.connect(         self._kodeTabClosed)

    def _hasMenu(self):
        return True if (self._topLeftLayout or self._topRightLayout) else False

    def _importMenu(self, kt):
        kt._tabBarTopLayout.removeItem(ll := kt._topLeftLayout)
        kt._tabBarTopLayout.removeItem(rl := kt._topRightLayout)
        kt._topLeftLayout  = None
        kt._topRightLayout = None
        self._topLeftLayout  = ll
        self._topRightLayout = rl
        if ll:
            self._tabBarTopLayout.addItem(ll, 1 if self.border() else 0,0)
        if rl:
            self._tabBarTopLayout.addItem(rl,1 if self.border() else 0,2)
        self._tabBarTopLayout.update()
        kt._tabBarTopLayout.update()

    def dragEnterEvent(self, evt) -> bool:
        TTkLog.debug(f"Drag Enter")
        return True

    def dragLeaveEvent(self, evt) -> bool:
        TTkLog.debug(f"Drag Leave")
        self._frameOverlay = None
        self.update()
        return True

    def dragMoveEvent(self, evt) -> bool:
        x,y = evt.x, evt.y
        w,h = self.size()
        k = 3 if self.border() else 2
        if y<k:
            return super().dragMoveEvent(evt)
        h-=k
        y-=k
        if x<w//4:
            self._frameOverlay = (0,k,w//4,h)
        elif x>w*3//4:
            self._frameOverlay = (w-w//4,k,w//4,h)
        elif y<h//4:
            self._frameOverlay = (0,k,w,h//4)
        elif y>h*3//4:
            self._frameOverlay = (0,k+h-h//4,w,h//4)
        else:
            self._frameOverlay = None
        self.update()
        return True

    def dropEvent(self, evt) -> bool:
        self._frameOverlay = None
        x,y = evt.x, evt.y
        ret = True
        data = evt.data()
        tb = data.tabButton()
        tw = data.tabWidget()
        if y<3:
            ret = super().dropEvent(evt)
        else:
            w,h = self.size()
            h-=3
            y-=3
            index  = tw._tabBar._tabButtons.index(tb)
            widget = tw._tabWidgets[index]

            def _processDrop(index, orientation, offset):
                fwold = self._baseWidget._getFirstWidget()
                tw.removeTab(index)
                splitter = self.parentWidget()
                index = splitter.indexOf(self)
                if splitter.orientation() != orientation:
                    splitter.replaceWidget(index, splitter := TTkSplitter(orientation=orientation))
                    splitter.addWidget(self)
                    index=offset
                splitter.insertWidget(index+offset, kt:=_TTkKodeTab(baseWidget=self._baseWidget, border=self.border(), closable=self.tabsClosable()))
                kt.addTab(widget,tb.text())
                if fwold!=(fwnew := self._baseWidget._getFirstWidget()) and fwold._hasMenu():
                    fwnew._importMenu(fwold)
            if x<w//4:
                _processDrop(index, TTkK.HORIZONTAL, 0)
            elif x>w*3//4:
                _processDrop(index, TTkK.HORIZONTAL, 1)
            elif y<h//4:
                _processDrop(index, TTkK.VERTICAL, 0)
            elif y>h*3//4:
                _processDrop(index, TTkK.VERTICAL, 1)
            else:
                ret = super().dropEvent(evt)

        # Remove the widget and/or all the cascade empty splitters
        self._kodeTabClosed(tw)
        self.update()
        return ret

    @pyTTkSlot()
    def _kodeTabClosed(self, widget=None):
        # Remove the widget and/or all the cascade empty splitters
        fwold = self._baseWidget._getFirstWidget()
        widget = widget if type(widget) is _TTkKodeTab else self
        if not widget._tabWidgets:
            if splitter := widget.parentWidget():
                while splitter.count() == 1 and splitter != self._baseWidget:
                    widget = splitter
                    splitter = widget.parentWidget()
                splitter.removeWidget(widget)
                if splitter == self._baseWidget and splitter.count() == 0:
                    splitter.addWidget(self)
        if fwold!=(fwnew := self._baseWidget._getFirstWidget()) and fwold._hasMenu():
            fwnew._importMenu(fwold)

    # Stupid hack to paint on top of the child widgets
    def paintChildCanvas(self):
        super().paintChildCanvas()

        if self._frameOverlay:
            x,y,w,h = self._frameOverlay
            canvas = self.getCanvas()
            canvas.drawBox(pos=(x,y), size=(w,h), color=TTkColor.fg("#FFFF00", modifier=TTkColorGradient(increment=-3))+TTkColor.bg("#0000FF"))

class TTkKodeTab(TTkSplitter):
    __slots__ = (
        '_lastKodeTabWidget',
        # Signals
        'currentChanged','tabBarClicked','tabCloseRequested' )

    def __init__(self, **kwargs):
        self.currentChanged    = pyTTkSignal(TTkTabWidget,int,TTkWidget,object)
        self.tabBarClicked     = pyTTkSignal(TTkTabWidget,int,TTkWidget,object)
        self.tabCloseRequested = pyTTkSignal(TTkTabWidget,int)
        super().__init__(**kwargs|{'layout':TTkGridLayout()})
        if 'parent' in kwargs: kwargs.pop('parent')
        # self.layout().addWidget(splitter := TTkSplitter())
        self._lastKodeTabWidget = _TTkKodeTab(baseWidget=self, **kwargs)
        self.addWidget(self._lastKodeTabWidget)

    def _getFirstWidget(self):
        kt = self
        item = None
        while type(item:=kt.widget(0)) != _TTkKodeTab: kt = item
        return item if type(item)==_TTkKodeTab else None

    @pyTTkSlot(TTkWidget)
    def setCurrentWidget(self, *args, **kwargs):
        return self._lastKodeTabWidget.setCurrentWidget(*args, **kwargs)

    def addTab(self, *args, **kwargs):
        if not TTkHelper.isParent(self._lastKodeTabWidget, self):
            for w in self.layout().iterWidgets():
                if type(w) is _TTkKodeTab:
                    self._lastKodeTabWidget = w
                    return self._lastKodeTabWidget.addTab(*args, **kwargs)
            raise Exception("No TTkKodeTab found to be used")
        return self._lastKodeTabWidget.addTab(*args, **kwargs)

    # def addMenu(self, text, position=TTkK.LEFT, data=None):
    def addMenu(self, text:TTkString, data:object=None, checkable:bool=False, checked:bool=False, position=TTkK.LEFT):
        '''addMenu'''
        # return self._lastKodeTabWidget.addMenu(text=text, data=data, checkable=checkable, checked=checked, position=position)
        return self._lastKodeTabWidget.addMenu(text=text, data=data, position=position)
