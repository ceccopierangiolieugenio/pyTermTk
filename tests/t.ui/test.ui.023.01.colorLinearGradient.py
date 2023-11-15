#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Luchr  <https://github.com/luchr>
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

import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk
from math import sin, cos

import TermTk

root = TermTk.TTk()

win_layout = TermTk.TTkGridLayout()
win = TermTk.TTkWindow(
    parent=root, pos=(1, 1), size=(70, 30), title='Rotating linear gradient',
    layout=win_layout)

len_direction, phi_direction, delay_direction = 40, 0.0, 0.1
dirtimer = TermTk.TTkTimer()

lingradBg = TermTk.TTkLinearGradient(
    base_pos=(20, 10),
    direction=(int(len_direction), 0),
    target_color=TermTk.TTkColor.bg('#ff0000'))

lingradFg = TermTk.TTkLinearGradient(
    base_pos=(20, 10),
    direction=(int(len_direction), 0),
    target_color=TermTk.TTkColor.fg('#00ff00'))


button_color = TermTk.TTkColor.bg('#0000ff', modifier=lingradBg)
border_color = TermTk.TTkColor.fg('#ff00ff', modifier=lingradFg)
button = TermTk.TTkButton(border=True, text="", color=button_color, borderColor=border_color)
win_layout.addWidget(button, 0, 0)

def dirtimer_cb():
    global phi_direction
    phi_direction += 0.05
    new_dir = (
        int(len_direction*cos(phi_direction)),
        int(len_direction*sin(phi_direction)))
    lingradBg.setParam(direction=new_dir)
    new_dir = (
        int(-len_direction*cos(phi_direction)),
        int(len_direction*sin(phi_direction)))
    lingradFg.setParam(direction=new_dir)
    button.update()  # button has no chance to know that the
                     # color modifier changed!
    dirtimer.start(delay_direction)

dirtimer.timeout.connect(dirtimer_cb)
dirtimer.start(delay_direction)

root.mainloop()