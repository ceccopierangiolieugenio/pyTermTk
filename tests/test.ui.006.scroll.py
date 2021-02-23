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

import sys, os

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()

win1 = ttk.TTkWindow(parent=root,pos = (1,1), size=(30,40), title="Test Window 1", border=True)
win1.setLayout(ttk.TTkVBoxLayout())
top = ttk.TTkFrame(parent=win1, layout=ttk.TTkHBoxLayout())
ttk.TTkScrollBar(parent=win1, orientation=ttk.TTk.HORIZONTAL, value=0,  color=ttk.TTkColor.bg('#990044')+ttk.TTkColor.fg('#ffff00'))
ttk.TTkScrollBar(parent=win1, orientation=ttk.TTk.HORIZONTAL, value=10, color=ttk.TTkColor.bg('#770044')+ttk.TTkColor.fg('#ccff00'))
ttk.TTkScrollBar(parent=win1, orientation=ttk.TTk.HORIZONTAL, value=50, color=ttk.TTkColor.bg('#660044')+ttk.TTkColor.fg('#88ff00'))
ttk.TTkScrollBar(parent=win1, orientation=ttk.TTk.HORIZONTAL, value=80, color=ttk.TTkColor.bg('#550044')+ttk.TTkColor.fg('#55ff00'))
ttk.TTkScrollBar(parent=win1, orientation=ttk.TTk.HORIZONTAL, value=99, color=ttk.TTkColor.bg('#330044')+ttk.TTkColor.fg('#33ff00'))


ttk.TTkScrollBar(parent=top, orientation=ttk.TTk.VERTICAL, value=0)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTk.VERTICAL, value=10)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTk.VERTICAL, value=40)
ttk.TTkSpacer(parent=top)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTk.VERTICAL, value=40, pagestep=3)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTk.VERTICAL, value=50, pagestep=5)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTk.VERTICAL, value=60, pagestep=20)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTk.VERTICAL, value=70, pagestep=30)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTk.VERTICAL, value=80, pagestep=60)
ttk.TTkSpacer(parent=top)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTk.VERTICAL, value=80)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTk.VERTICAL, value=90)
ttk.TTkScrollBar(parent=top, orientation=ttk.TTk.VERTICAL, value=99)


root.mainloop()