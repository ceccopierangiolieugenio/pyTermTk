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
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.ttk import *
from TermTk.TTkWidgets.widget import *
from TermTk.TTkWidgets.frame import *

class TTkSplitter(TTkFrame):
    __slots__ = ('_widgets', '_orientation', '_splitters', '_selected')
    def __init__(self, *args, **kwargs):
        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkSplitter' )
        self._widgets = []
        self._splitters = []
        self._orientation = kwargs.get('orientation' , TTkK.HORIZONTAL )

    def addWidget(self, widget):
        # NOTE: Check with the max/min size if the new widget can fit
        self._widgets.append(widget)
        self._splitters.append(0x10000)
        self._rearrange()

    def _rearrange(self):
        w, h = self.size()
        if self._orientation == TTkK.HORIZONTAL:
            pass
        else:
            pass

