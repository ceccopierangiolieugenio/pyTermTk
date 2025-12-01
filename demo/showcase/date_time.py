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

import sys, os, argparse
import datetime

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))
import TermTk as ttk


def demoDateTimePicker(root=None):
    frame = ttk.TTkFrame(parent=root, border=False)

    frameDateForm = ttk.TTkFrame(parent=frame, pos=(0,0), size=(24,10), title='Date Form', titleAlign=ttk.TTkK.Alignment.RIGHT_ALIGN, border=True)
    dateFormWidget = ttk.TTkDateForm(parent=frameDateForm, pos=(1,0))

    frameDateTime = ttk.TTkFrame(parent=frame, pos=(24,0), size=(26,3), title='DateTime widget', titleAlign=ttk.TTkK.Alignment.LEFT_ALIGN, border=True)
    datetimeWidget = ttk.TTkDateTime(parent=frameDateTime, pos=(1,0))

    frameDate = ttk.TTkFrame(parent=frame, pos=(24,3), size=(17,3), title='Date', titleAlign=ttk.TTkK.Alignment.LEFT_ALIGN, border=True)
    dateWidget = ttk.TTkDate(parent=frameDate, pos=(1,0))

    frameTime = ttk.TTkFrame(parent=frame, pos=(24,6), size=(12,3), title='Time', titleAlign=ttk.TTkK.Alignment.LEFT_ALIGN, border=True)
    timeWidget = ttk.TTkTime(parent=frameTime, pos=(1,0))

    ttk.pyTTkSlot(datetime.datetime)
    def _changedDatetime(dt:datetime.datetime):
        dateWidget.setDate(dt.date())
        timeWidget.setTime(dt.time())
        dateFormWidget.setDate(dt.date())

    ttk.pyTTkSlot(datetime.time)
    def _changedTime(time:datetime.time):
        dt = datetimeWidget.datetime()
        new_dt = datetime.datetime.combine(dt.date(),time)
        datetimeWidget.setDatetime(new_dt)

    ttk.pyTTkSlot(datetime.date)
    def _changedDate(date:datetime.date):
        dt = datetimeWidget.datetime()
        new_dt = datetime.datetime.combine(date,dt.time())
        datetimeWidget.setDatetime(new_dt)
        dateFormWidget.setDate(date)
        dateWidget.setDate(date)

    timeWidget.timeChanged.connect(_changedTime)
    dateWidget.dateChanged.connect(_changedDate)
    dateFormWidget.dateChanged.connect(_changedDate)
    datetimeWidget.datetimeChanged.connect(_changedDatetime)

    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    root = ttk.TTk(mouseTrack=True)
    if args.f:
        root.setLayout(ttk.TTkGridLayout())
        winColor1 = root
    else:
        winColor1 = ttk.TTkWindow(parent=root,pos = (0,0), size=(52,14), title="Test DateTime Picker", border=True, layout=ttk.TTkGridLayout())

    demoDateTimePicker(winColor1)

    root.mainloop()

if __name__ == "__main__":
    main()