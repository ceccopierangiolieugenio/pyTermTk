#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
import time, math

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

class Parallax(ttk.TTk):
    COLOR1 = ttk.TTkColor.fg("#FFFFFF")+ttk.TTkColor.bg("#AFAEBC")
    COLOR2 = ttk.TTkColor.fg("#FFFFFF")+ttk.TTkColor.bg("#858494")
    COLOR3 = ttk.TTkColor.fg("#FFFFFF")+ttk.TTkColor.bg("#63687B")
    COLOR4 = ttk.TTkColor.fg("#9694A1")+ttk.TTkColor.bg("#B3B2C0")
    COLOR5 = ttk.TTkColor.fg("#333238")+ttk.TTkColor.bg("#B3B2C0")
    COLOR6 = ttk.TTkColor.fg("#333238")+ttk.TTkColor.bg("#333238")

    def __init__(self, *args, **kwargs):
        self._baseTime = time.time()
        super().__init__(*args, **kwargs)
        ttk.TTkHelper._rootWidget.paintExecuted.connect(self._refreshAnimation)
        self._refreshAnimation()

    @ttk.pyTTkSlot()
    def _refreshAnimation(self):
        self.update()

    # 1) 11 11 11 11-11 11 11 11-11 11 ..
    # 2) 22 11 11 11-22 11 11 11-22 11 ..
    # 3) 33 33 11 11-33 33 11 11-33 33 ..
    # 4) 44 44 44 11-44 44 44 11-44 44 ..
    # 5) 44 44 44 44-44 44 44 44-44 44 ..

    def paintEvent(self, canvas: ttk.TTkCanvas):
        w,h = self.size()
        diff = int(300*(time.time() - self._baseTime))

        secH  = h//5
        # draw the 1st section
        canvas.fill(pos=(0,0), size=(w,secH*4), color=Parallax.COLOR1)
        # draw the 2nd section
        for x in range(0,w+8,16):
            x += (diff%(32*4))//8
            canvas.fill(pos=(w-x,  secH), size=(3,secH*3), color=Parallax.COLOR2)
            canvas.fill(pos=(w-x-2,secH+2), size=(6,secH*3), color=Parallax.COLOR2)
            canvas.fill(pos=(w-x,  secH+3), size=(10,secH*3), color=Parallax.COLOR2)
        canvas.fill(    pos=(0,3*secH+3), size=(w,secH*3), color=Parallax.COLOR2)
        # draw the 3nd section
        for x in range(0,w+16,32):
            x += (diff%(32*6))//6
            canvas.fill(pos=(w-x,2*secH), size=(12,secH*3), color=Parallax.COLOR3)
            canvas.fill(pos=(w-x+12,5*secH//2), size=(4,secH*3), color=Parallax.COLOR3)
        # draw the 4nd section
        for x in range(0,w+20,50):
            x += (diff%(50*4))//4
            canvas.fill(    pos=(w-x+15,2*secH-3), color=Parallax.COLOR6, size=(1,secH*3) )
            canvas.fill(    pos=(w-x+10,3*secH-4), color=Parallax.COLOR6, size=(10,secH*3) )
            canvas.drawText(pos=(w-x,   3*secH+0), color=Parallax.COLOR5, text='▀'*43)
            canvas.drawText(pos=(w-x,   3*secH+1), color=Parallax.COLOR4, text=f'┌{"─╥"*20}─┐')
            canvas.drawText(pos=(w-x,   3*secH+2), color=Parallax.COLOR4, text=f'└{"─╨"*20}─┘')
            canvas.drawText(pos=(w-x,   3*secH+3), color=Parallax.COLOR5, text=f'  {"███ "*10} ')
            canvas.drawText(pos=(w-x,   3*secH+4), color=Parallax.COLOR5, text=f'  {"███ "*10} ')
            canvas.fill(    pos=(w-x,   3*secH+5), color=Parallax.COLOR4, size=(43,secH) )
        # draw the 5nd section
        canvas.fill(pos=(0,4*secH+2), size=(w,secH), color=Parallax.COLOR4)


root = Parallax(title="TTKanabalt")
root.mainloop()

