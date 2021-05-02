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

'''
### Box Layout - [Tutorial](https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/002-layout.md)
'''

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkLayouts.gridlayout import TTkGridLayout

class TTkHBoxLayout(TTkGridLayout):
    ''' The TTkHBoxLayout class lines up widgets horizontally

    ::

        TTkHBoxLayout
         ╔═════════╤═════════╤═════════╗
         ║ Widget1 │ Widget2 │ Widget3 ║
         ║         │         │         ║
         ║         │         │         ║
         ║         │         │         ║
         ║         │         │         ║
         ║         │         │         ║
         ╚═════════╧═════════╧═════════╝
    '''
    pass

class TTkVBoxLayout(TTkGridLayout):
    ''' The TTkVBoxLayout class lines up widgets vertically

    ::

        TTkVBoxLayout
         ╔═════════════════════════════╗
         ║         Widget 1            ║
         ╟─────────────────────────────╢
         ║         Widget 2            ║
         ╟─────────────────────────────╢
         ║         Widget 3            ║
         ╟─────────────────────────────╢
         ║         Widget 4            ║
         ╚═════════════════════════════╝
    '''
    def addItem(self, item):
        TTkGridLayout.addItem(self, item, self.count(), 0)
    def addWidget(self, widget):
        TTkGridLayout.addWidget(self, widget, self.count(), 0)