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

from typing import Callable, Iterator, Tuple

from TermTk.TTkCore.constant import  TTkK
from TermTk.TTkCore.helper import  TTkHelper
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.color import TTkColor, TTkColorGradient
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.tabwidget import TTkTabWidget, TTkBarType, _TTkNewTabWidgetDragData, _TTkTabWidgetDragData
from TermTk.TTkWidgets.splitter import TTkSplitter
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkGui.drag import TTkDnDEvent

_splitter_NERD_1_style = {
        'default':{
            'glyphs' : {
                TTkK.VERTICAL   : ('▃','▃','▃'),
                TTkK.HORIZONTAL : ('┇','║','┇') },
            'color': TTkColor.fgbg("#dddddd","#222222"),
            'borderColor': TTkColor.fg("#8888aa") },
        'focus':{
            'color': TTkColor.fgbg("#ffddff","#222222"),
            'borderColor': TTkColor.fg("#8888aa")},
        'hover':{
            'borderColor': TTkColor.fg("#aaaa88")}
    }
class _TTkKodeTab(TTkTabWidget):
    __slots__ = (
        '_frameOverlay','_baseWidget',
        #Signals
        'kodeTabCloseRequested')
    def __init__(self, *,
                 baseWidget=None,
                 **kwargs) -> None:
        self.kodeTabCloseRequested = pyTTkSignal(_TTkKodeTab,int)
        self._baseWidget:TTkKodeTab = baseWidget
        self._frameOverlay = None
        super().__init__(**kwargs)
        self.tabBarClicked.connect(    lambda i:self._baseWidget.tabBarClicked.emit(    self, i, self.widget(i), self.tabData(i)))
        self.currentChanged.connect(   lambda i:self._baseWidget.currentChanged.emit(   self, i, self.widget(i), self.tabData(i)))
        self.tabCloseRequested.connect(self._handleTabCloseRequested)

    def _handleTabCloseRequested(self, index):
        self.kodeTabCloseRequested.emit(self,index)

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

    def iterItems(self):
        for i in range(self.count()):
            yield self, i

    def dragEnterEvent(self, evt:TTkDnDEvent) -> bool:
        TTkLog.debug(f"Drag Enter")
        return True

    def dragLeaveEvent(self, evt:TTkDnDEvent) -> bool:
        TTkLog.debug(f"Drag Leave")
        self._frameOverlay = None
        self.update()
        return True

    def dragMoveEvent(self, evt:TTkDnDEvent) -> bool:
        x,y = evt.x, evt.y
        w,h = self.size()
        k,_,_,_ = self.getPadding()
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
            self._frameOverlay = (0,k,w,h)
        self.update()
        return True

    def dropEvent(self, evt:TTkDnDEvent) -> bool:
        self._frameOverlay = None
        x,y = evt.x, evt.y
        data = evt.data()
        if issubclass(type(data),_TTkNewTabWidgetDragData):
            tw = None
        elif issubclass(type(data),_TTkTabWidgetDragData):
            tw = data.tabWidget()
        else:
            return False

        def _processDrop(widget, label, orientation, offset):
            fwold = self._baseWidget._getFirstWidget()
            splitter = self.parentWidget()
            index = splitter.indexOf(self)
            if splitter.orientation() != orientation:
                splitter.replaceWidget(index, splitter := TTkSplitter(orientation=orientation, style=self.parentWidget().classStyle))
                splitter.mergeStyle(_splitter_NERD_1_style)
                splitter.addWidget(self)
                index=offset
            splitter.insertWidget(index+offset, kt:=_TTkKodeTab(baseWidget=self._baseWidget, border=self.border(), barType=self._barType, closable=self.tabsClosable()))
            kt._dropEventProxy = self._dropEventProxy
            kt.kodeTabCloseRequested.connect(self._baseWidget._handleKodeTabCloseRequested)
            ret = kt.addTab(widget,label)
            self._baseWidget.tabAdded.emit(kt, ret)
            if fwold!=(fwnew := self._baseWidget._getFirstWidget()) and fwold._hasMenu():
                fwnew._importMenu(fwold)

        ret = True
        if y<3:
            ret = super().dropEvent(evt)
        elif issubclass(type(data),_TTkNewTabWidgetDragData):
            tw = None
            widget = data.widget()
            tabData = data.data()
            label = data.label()
            closable = data.closable()
            w,h = self.size()
            h-=3
            y-=3
            if x<w//4:
                _processDrop(widget, label, TTkK.HORIZONTAL, 0)
            elif x>w*3//4:
                _processDrop(widget, label, TTkK.HORIZONTAL, 1)
            elif y<h//4:
                _processDrop(widget, label, TTkK.VERTICAL, 0)
            elif y>h*3//4:
                _processDrop(widget, label, TTkK.VERTICAL, 1)
            else:
                ret = super().dropEvent(evt)
        elif issubclass(type(data),_TTkTabWidgetDragData):
            tb = data.tabButton()
            tw = data.tabWidget()
            w,h = self.size()
            h-=3
            y-=3
            index  = tw._tabBar._tabButtons.index(tb)
            widget = tw._tabWidgets[index]
            label  = tb.text()

            if x<w//4:
                tw.removeTab(index)
                _processDrop(widget, label, TTkK.HORIZONTAL, 0)
            elif x>w*3//4:
                tw.removeTab(index)
                _processDrop(widget, label, TTkK.HORIZONTAL, 1)
            elif y<h//4:
                tw.removeTab(index)
                _processDrop(widget, label, TTkK.VERTICAL, 0)
            elif y>h*3//4:
                tw.removeTab(index)
                _processDrop(widget, label, TTkK.VERTICAL, 1)
            else:
                ret = super().dropEvent(evt)

        # Remove the widget and/or all the cascade empty splitters
        if tw:
            self._kodeTabClosed(tw)
        self.update()
        return ret

    @pyTTkSlot()
    def _kodeTabClosed(self, widget=None):
        # Remove the widget and/or all the cascade empty splitters
        fwold = self._baseWidget._getFirstWidget()
        widget = widget if issubclass(type(widget), _TTkKodeTab) else self
        if not widget._tabWidgets:
            if splitter := widget.parentWidget():
                while splitter.count() == 1 and splitter != self._baseWidget:
                    widget = splitter
                    splitter = widget.parentWidget()
                splitter.removeWidget(widget)
                widget.kodeTabCloseRequested.clear()
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
        '_lastKodeTabWidget', '_barType',
        # Signals
        'currentChanged','tabBarClicked','kodeTabCloseRequested', 'tabAdded' )

    def __init__(self,
                 barType:TTkBarType=TTkBarType.NONE,
                 **kwargs) -> None:
        self.currentChanged    = pyTTkSignal(TTkTabWidget,int,TTkWidget,object)
        self.tabBarClicked     = pyTTkSignal(TTkTabWidget,int,TTkWidget,object)
        self.kodeTabCloseRequested = pyTTkSignal(TTkTabWidget,int)
        self.tabAdded = pyTTkSignal(TTkTabWidget, int)
        self._barType = barType

        super().__init__(**kwargs|{'layout':TTkGridLayout()})

        self.mergeStyle(_splitter_NERD_1_style)
        kwargs.pop('parent',None)
        kwargs.pop('visible',None)
        # self.layout().addWidget(splitter := TTkSplitter())
        self._lastKodeTabWidget = kt = _TTkKodeTab(baseWidget=self, barType=self._barType, **kwargs)
        self._lastKodeTabWidget._dropEventProxy = self._dropEventProxy
        self.addWidget(self._lastKodeTabWidget)
        kt.kodeTabCloseRequested.connect(self._handleKodeTabCloseRequested)

    @pyTTkSlot(_TTkKodeTab,int)
    def _handleKodeTabCloseRequested(self, kt:_TTkKodeTab, index:int) -> None:
        TTkLog.debug(f"{kt} -> {index}")
        self.kodeTabCloseRequested.emit(kt, index)
        # kt.removeTab(index)

    def _getFirstWidget(self):
        kt = self
        item = None
        while type(item:=kt.widget(0)) != _TTkKodeTab: kt = item
        return item if type(item)==_TTkKodeTab else None

    def iterItems(self) -> Iterator[Tuple[_TTkKodeTab, int]]:
        def _iterSplitter(split:TTkSplitter):
            for i in range(split.count()):
                _wid = split.widget(i)
                if issubclass(type(_wid), TTkSplitter):
                    yield from _iterSplitter(_wid)
                elif issubclass(type(_wid), _TTkKodeTab):
                    yield from _wid.iterItems()
        yield from _iterSplitter(self)

    def setDropEventProxy(self, proxy:Callable) -> None:
        for widget in self.layout().iterWidgets(onlyVisible=False):
            if issubclass(type(widget),_TTkKodeTab):
                widget.setDropEventProxy(proxy)
        return super().setDropEventProxy(proxy)

    @pyTTkSlot(TTkWidget)
    def setCurrentWidget(self, *args, **kwargs) -> None:
        return self._lastKodeTabWidget.setCurrentWidget(*args, **kwargs)

    def addTab(self, *args, **kwargs) -> int:
        if not TTkHelper.isParent(self._lastKodeTabWidget, self):
            for w in self.layout().iterWidgets():
                if isinstance(w,_TTkKodeTab):
                    self._lastKodeTabWidget = w
                    ret = self._lastKodeTabWidget.addTab(*args, **kwargs)
                    self.tabAdded.emit(self._lastKodeTabWidget, ret)
                    return ret
            raise Exception("No TTkKodeTab found to be used")
        ret = self._lastKodeTabWidget.addTab(*args, **kwargs)
        self.tabAdded.emit(self._lastKodeTabWidget, ret)
        return ret

    # def addMenu(self, text, position=TTkK.LEFT, data=None):
    def addMenu(self, text:TTkString, data:object=None, checkable:bool=False, checked:bool=False, position=TTkK.LEFT):
        '''addMenu'''
        # return self._lastKodeTabWidget.addMenu(text=text, data=data, checkable=checkable, checked=checked, position=position)
        return self._lastKodeTabWidget.addMenu(text=text, data=data, position=position)
