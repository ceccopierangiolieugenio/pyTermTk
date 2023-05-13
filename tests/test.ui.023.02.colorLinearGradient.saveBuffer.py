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

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk
from math import sin, cos

import TermTk
from TermTk import TTkCfg

class BBB(TermTk.TTkButton):

    def paintEvent(self, canvas):
        if not self.isEnabled():
            borderColor = self._borderColorDisabled
            textColor   = self._textColorDisabled
            grid = TTkCfg.theme.buttonBoxGridDisabled
        elif self._pressed:
            borderColor = self._borderColorClicked
            textColor   = self._textColorClicked
            grid = TTkCfg.theme.buttonBoxGridClicked
        else:
            if self._checkable:
                if self._checked:
                    grid = TTkCfg.theme.buttonBoxGridChecked
                    borderColor = TTkCfg.theme.buttonBorderColorChecked
                    textColor = TTkCfg.theme.buttonTextColorChecked
                else:
                    grid = TTkCfg.theme.buttonBoxGridUnchecked
                    borderColor = TTkCfg.theme.buttonBorderColorUnchecked
                    textColor = TTkCfg.theme.buttonTextColorUnchecked
                if self.hasFocus():
                    borderColor = self._borderColorFocus
            else:
                grid = TTkCfg.theme.buttonBoxGrid
                if self.hasFocus():
                    textColor   = self._textColorFocus
                    borderColor = self._borderColorFocus
                elif self.isEntered():
                    textColor   = TTkCfg.theme.buttonTextColorHover
                    borderColor = TTkCfg.theme.buttonBorderColorHover
                else:
                    textColor   = self._textColor
                    borderColor = self._borderColor

        w,h = self.size()

        # Draw the border and bgcolor
        if not self._border or (self._border and ( h==1 or ( h>1 and len(self._text)>h-2 and len(self._text[0])!=0 ))):
            canvas.fill(pos=(1,0), size=(w-2,h), color=textColor)
            if h<=1:
                canvas.drawChar(pos=(0  ,0), color=borderColor ,char='[')
                canvas.drawChar(pos=(w-1,0), color=borderColor ,char=']')
            else: # No border multiline button
                canvas.drawChar(pos=(0,  0),  char='╿', color=borderColor)
                canvas.drawChar(pos=(w-1,0),  char='╿', color=borderColor)
                canvas.drawChar(pos=(w-1,h-1),char='╽', color=borderColor)
                canvas.drawChar(pos=(0,  h-1),char='╽', color=borderColor)
                for y in range(1,h-1):
                    canvas.drawChar(pos=(0,  y),char='│', color=borderColor)
                    canvas.drawChar(pos=(w-1,y),char='│', color=borderColor)
        else:
            for y in range(1,h-1):
                canvas.drawText(pos=(1,y), text="1234567890AbcdefghiABCDEFG"*(w//10), color=textColor)
            canvas.drawButtonBox(pos=(0,0),size=(self._width,self._height),color=borderColor, grid=grid)

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
button = BBB(border=True, text="", color=button_color, borderColor=border_color)
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

button.clicked.connect(TermTk.TTkHelper.quit)

dirtimer.timeout.connect(dirtimer_cb)
dirtimer.start(delay_direction)

root.mainloop()

d = TermTk.TTkUtil.obj_inflate_2_base64(root._canvas._data)
c = TermTk.TTkUtil.obj_inflate_2_base64(root._canvas._colors)

wid = 250
dd = '    "' + '" +\n    "'.join([d[i:i+wid] for i in range(0,len(d),wid)]) + '"'
cc = '    "' + '" +\n    "'.join([c[i:i+wid] for i in range(0,len(c),wid)]) + '"'

print("cx = {")
print(f"  'data'   : ttk.TTkUtil.base64_deflate_2_obj(\n{dd} ),")
print(f"  'colors' : ttk.TTkUtil.base64_deflate_2_obj(\n{cc} )"+"}")