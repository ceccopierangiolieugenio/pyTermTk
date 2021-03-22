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
from TermTk.TTkLayouts.gridlayout import TTkGridLayout


'''
_curentIndex =              2
_labelPos =      [0],[1],  [2],   [3],   [4],
                ╭─┌──┌──────╔══════╗──────┬──────┐─╮
_labels=        │◀│La│Label1║Label2║Label3│Label4│▶│
                ╞═══════════╩══════╩═══════════════╡
                 leftscroller                     rightScroller
'''
class TTkTabWidget(TTkFrame):
    __slots__ = (
        '_viewport',
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
        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTabWidget')
        self.setLayout(TTkGridLayout())
        self._viewport = TTkWidget(layout=TTkGridLayout())
        self.layout().addWidget(self._viewport,0,0)
        #self.layout().addWidget(TTkSpacer(),0,1)
        #self.layout().addWidget(TTkSpacer(),1,0)
        if self.border():
            self.setPadding(3,1,1,1)
        else:
            self.setPadding(2,0,0,0)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)


    def addTab(self, widget, label):
        widget.hide()
        self._tabWidgets.append(widget)
        self._labels.append(label)
        self._viewport.addWidget(widget)
        self._updateTabs()

    def insertTab(self, index, widget, label):
        widget.hide()
        self._tabWidgets.insert(index, widget)
        self._labels.insert(index, label)
        self._viewport.addWidget(widget)
        self._updateTabs()

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

        for i, widget in enumerate(self._tabWidgets):
            if self._currentIndex == i:
                widget.show()
            else:
                widget.hide()
        self.update()

    def resizeEvent(self, w, h):
        self._updateTabs()

    def mousePressEvent(self, evt):
        x,y = evt.x, evt.y
        w = self.width()
        offset = self._offset
        if self.border():
            if y>2: return False
        else:
            if y>1: return False
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
        if self.border():
            self._canvas.drawBox(pos=(0,2),size=(self._width,self._height-2), color=tabBorderColor, grid=9)
        self._canvas.drawTab(
                pos=(0,0), size=self.size(), slim=not self.border(),
                labels=self._labels, labelsPos=self._labelsPos,
                selected=self._currentIndex, offset=self._offset,
                leftScroller=self._leftScroller, rightScroller=self._rightScroller,
                color=tabColor, borderColor=tabBorderColor, selectColor=tabSelectColor, offsetColor=tabOffsetColor)

