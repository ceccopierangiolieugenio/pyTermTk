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
from datetime import time,date,datetime

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk

root = ttk.TTk()
winLog = ttk.TTkWindow(parent=root, pos=(20,1), size=(80,30), layout=ttk.TTkGridLayout())
ttk.TTkLogViewer(parent=winLog)

win = ttk.TTkWindow(parent=root, pos=(0,0), size=(57,14))
win2 = ttk.TTkWindow(parent=root, pos=(60,0), size=(22,12), layout=ttk.TTkGridLayout())

testTime1=time(hour=3,minute=30)
timeWidget1 = ttk.TTkTime(parent=win, pos=(1,0), time=testTime1)
timeWidget2 = ttk.TTkTime(parent=win, pos=(1,2))

timeLabel1 = ttk.TTkLabel(parent=win, pos=(1,4), text=str(testTime1))
timeLabel2 = ttk.TTkLabel(parent=win, pos=(1,6), text=str(timeWidget2.time()))
timeWidget1.timeChanged.connect(lambda _t:timeLabel1.setText(str(_t)))
timeWidget2.timeChanged.connect(lambda _t:timeLabel2.setText(str(_t)))

testDate = date(year=1980, month=12, day=25)
dateWidget1 = ttk.TTkDateForm(parent=win, pos=(12,0), date=testDate)
dateWidget2 = ttk.TTkDateForm(parent=win, pos=(34,0))
dateWidget3 = ttk.TTkDateForm(parent=win2, date=testDate.replace(year=2000))
dateLabel = ttk.TTkLabel(parent=win, pos=(1,8), text=str(testDate))
dateWidget1.dateChanged.connect(lambda _d: dateLabel.setText(str(_d)))
dateWidget1.dateChanged.connect(dateWidget2.setDate)
dateWidget2.dateChanged.connect(dateWidget1.setDate)
dateWidget3.dateChanged.connect(dateWidget2.setDate)

root.mainloop()