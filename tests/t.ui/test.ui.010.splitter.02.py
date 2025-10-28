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

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()

winSplitter1 = ttk.TTkWindow(parent=root,pos = (1,1), size=(100,40), title="Test Splitter1", border=True, layout=ttk.TTkGridLayout())
vsplitter1_1 = ttk.TTkSplitter(parent=winSplitter1, orientation=ttk.TTkK.VERTICAL)
ttk.TTkTestWidgetSizes(parent=vsplitter1_1 ,border=True, title="Frame1.1")
ttk.TTkTestWidgetSizes(parent=vsplitter1_1 ,border=True, title="Frame1.2")
ttk.TTkTestWidgetSizes(parent=vsplitter1_1 ,border=True, title="Frame1.3")


winSplitter2 = ttk.TTkWindow(parent=root,pos = (10,5), size=(100,40), title="Test Splitter2", border=True, layout=ttk.TTkGridLayout())
vsplitter2_1 = ttk.TTkSplitter(parent=winSplitter2, orientation=ttk.TTkK.HORIZONTAL)
ttk.TTkTestWidgetSizes(parent=vsplitter2_1 ,border=True, title="Frame1.1")
ttk.TTkTestWidgetSizes(parent=vsplitter2_1 ,border=True, title="Frame1.2")
ttk.TTkTestWidgetSizes(parent=vsplitter2_1 ,border=True, title="Frame1.3")

winSplitter3 = ttk.TTkWindow(parent=root,pos = (15,10), size=(100,40), title="Test Splitter3", border=True, layout=ttk.TTkGridLayout())
vsplitter3_1 = ttk.TTkSplitter(parent=winSplitter3, orientation=ttk.TTkK.HORIZONTAL)
ttk.TTkTestWidgetSizes(parent=vsplitter3_1 ,border=True, title="Frame1.1")
ttk.TTkTestWidgetSizes(parent=vsplitter3_1 ,border=True, title="Frame1.2")
ttk.TTkTestWidgetSizes(parent=vsplitter3_1 ,border=True, title="Frame1.3")
ttk.TTkTestWidgetSizes(parent=vsplitter3_1 ,border=True, title="Frame1.4")
ttk.TTkTestWidgetSizes(parent=vsplitter3_1 ,border=True, title="Frame1.5")
vsplitter3_1.setSizes([25,None,15,None,30])



root.mainloop()