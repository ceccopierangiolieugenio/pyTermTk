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

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget, TTkScrollBar, TTkLayout

'''


'''
class TTkScrollArea(TTkWidget):
    __slots__ = ('_border', '_hszroll', '_vscroll', '_widgetScroller')
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkScrollArea' )
    #    self._border = kwargs.get('border', True )
    #    if self._border:
    #        self.setPadding(1,2,1,2)
    #    else:
    #        self.setPadding(0,1,0,1)
    #    self._hscroll = TTkScrollBar(parent=self)
    #    self._vscroll = TTkScrollBar(parent=self)

    #def setWidget(self, widget):

    #def setLayout(self, layout):
    #    self._layout = layout
    #    self._layout.setParent(self)
    #    self._layout.setGeometry(
    #                    self._padl, self._padt,
    #                    self._width   - self._padl - self._padr,
    #                    self._height  - self._padt - self._padb)
    #    self.update(repaint=True, updateLayout=True)

    #def paintEvent(self):
    #    if self._border:
    #        self._canvas.drawBox(pos=(0,0),size=(self._width,self._height))