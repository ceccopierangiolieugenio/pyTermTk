#!/usr/bin/env python3

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

import sys, os

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk


class TryModal(ttk.TTkWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        overlay_btn = ttk.TTkButton(parent=self, pos=(0,0), size=(15,3), border=True, text='Overlay')
        modal_btn   = ttk.TTkButton(parent=self, pos=(0,3), size=(15,3), border=True, text='Modal')
        toolbox_btn = ttk.TTkButton(parent=self, pos=(0,6), size=(15,3), border=True, text='Toolbox')

        def _overlay():
            win = TryModal(size=(30,13), title="Overlay")
            ttk.TTkHelper.overlay(
                caller=overlay_btn,
                widget=win,
                x=0,y=0)
        overlay_btn.clicked.connect(_overlay)

        def _modal():
            win = TryModal(size=(30,13), title="Modal")
            ttk.TTkHelper.overlay(
                caller=modal_btn,
                widget=win,
                modal=True,
                x=0,y=0)
        modal_btn.clicked.connect(_modal)

        def _toolbox():
            win = TryModal(size=(30,13), title="Toolbox")
            ttk.TTkHelper.overlay(
                caller=toolbox_btn,
                widget=win,
                toolWindow=True,
                x=0,y=0)
        toolbox_btn.clicked.connect(_toolbox)

root = ttk.TTk()

TryModal(parent=root, pos=(5,2), size=(30,13), title="Root")

root.mainloop()

