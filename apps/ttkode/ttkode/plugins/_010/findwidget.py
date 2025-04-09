# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['FindWidget']

import TermTk as ttk

import ttkode

class FindWidget(ttk.TTkContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setLayout(layout:=ttk.TTkGridLayout())
        searchLayout = ttk.TTkGridLayout()
        searchLayout.addWidget(expandReplace:=ttk.TTkButton(text=">", maxWidth=3, checkable=True), 0, 0)
        searchLayout.addWidget(ttk.TTkLineEdit(), 0, 1)
        searchLayout.addWidget(replace:=ttk.TTkLineEdit(), 1, 0, 1, 2)
        layout.addItem(searchLayout, 0, 0)
        layout.addWidget(ttk.TTkButton(text="Find", border=False), 1,0)
        layout.addWidget(ttk.TTkButton(text="Find", border=False), 2,0)
        layout.addWidget(ttk.TTkButton(text="Find", border=True), 3,0)
        expandReplace.toggled.connect(replace.setVisible)
        replace.setVisible(False)