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

from TermTk import TTkWidget, TTkColor, TTkString

class TTkPeppered(TTkWidget):
    # to save space I just recycle the 20x20 imageArray (~10K)
    # used in the "TtkAbout" Widget
    peppered_20= ttk.TTkAbout.peppered
    peppered_10=[
            [[0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x67,0x01], [0x25,0x93,0x1c], [0x22,0x7e,0x12], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00]],
            [[0x00,0x00,0x00], [0x00,0x00,0x00], [0x0a,0x00,0x00], [0x3e,0x29,0x08], [0x2f,0x97,0x2d], [0x2e,0x9a,0x2b], [0x6b,0x3b,0x10], [0x92,0x15,0x16], [0x4b,0x00,0x00], [0x00,0x00,0x00]],
            [[0x00,0x00,0x00], [0xcd,0x1e,0x1e], [0xff,0x82,0x82], [0xec,0x0a,0x0c], [0xfb,0x80,0x61], [0x61,0x9f,0x33], [0xea,0x4e,0x42], [0xff,0x70,0x71], [0x81,0x00,0x00], [0x00,0x00,0x00]],
            [[0x00,0x00,0x00], [0xa7,0x00,0x00], [0xdd,0x00,0x00], [0xc7,0x00,0x00], [0xff,0x12,0x0e], [0xff,0x2f,0x1d], [0xf1,0x00,0x00], [0x6b,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00]],
            [[0x00,0x00,0x00], [0x00,0x00,0x00], [0x3e,0x00,0x00], [0x65,0x00,0x00], [0xb8,0x00,0x00], [0xdc,0x00,0x00], [0x97,0x00,0x00], [0x86,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00]],
            [[0x00,0x00,0x00], [0x00,0x00,0x00], [0x3f,0x00,0x00], [0xd4,0x00,0x00], [0xc0,0x00,0x00], [0xff,0x00,0x00], [0xea,0x00,0x00], [0xd9,0x00,0x00], [0x22,0x00,0x00], [0x00,0x00,0x00]],
            [[0x00,0x00,0x00], [0x00,0x00,0x00], [0x15,0x00,0x00], [0xd7,0x00,0x00], [0xff,0x05,0x06], [0xff,0x09,0x09], [0xff,0x0a,0x0a], [0xe0,0x00,0x00], [0x1e,0x00,0x00], [0x00,0x00,0x00]],
            [[0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0xa2,0x00,0x00], [0xff,0x00,0x00], [0xff,0x69,0x69], [0xff,0x00,0x00], [0xbc,0x00,0x00], [0x14,0x00,0x00], [0x00,0x00,0x00]],
            [[0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x58,0x00,0x00], [0xb0,0x00,0x00], [0xff,0x72,0x71], [0xe0,0x05,0x05], [0x7c,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00]],
            [[0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x15,0x00,0x00], [0x55,0x00,0x00], [0x21,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00]]]

    peppered_old=[
            ['#000000', '#000000', '#000000', '#006701', '#25931c', '#227e12', '#000000', '#000000', '#000000', '#000000'],
            ['#000000', '#000000', '#0a0000', '#3e2908', '#2f972d', '#2e9a2b', '#6b3b10', '#921516', '#4b0000', '#000000'],
            ['#000000', '#cd1e1e', '#ff8282', '#ec0a0c', '#fb8061', '#619f33', '#ea4e42', '#ff7071', '#810000', '#000000'],
            ['#000000', '#a70000', '#dd0000', '#c70000', '#ff120e', '#ff2f1d', '#f10000', '#6b0000', '#000000', '#000000'],
            ['#000000', '#000000', '#3e0000', '#650000', '#b80000', '#dc0000', '#970000', '#860000', '#000000', '#000000'],
            ['#000000', '#000000', '#3f0000', '#d40000', '#c00000', '#ff0000', '#ea0000', '#d90000', '#220000', '#000000'],
            ['#000000', '#000000', '#150000', '#d70000', '#ff0506', '#ff0909', '#ff0a0a', '#e00000', '#1e0000', '#000000'],
            ['#000000', '#000000', '#000000', '#a20000', '#ff0000', '#ff6969', '#ff0000', '#bc0000', '#140000', '#000000'],
            ['#000000', '#000000', '#000000', '#580000', '#b00000', '#ff7271', '#e00505', '#7c0000', '#000000', '#000000'],
            ['#000000', '#000000', '#000000', '#000000', '#150000', '#550000', '#210000', '#000000', '#000000', '#000000']]
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self.setGeometry(0,0,40,40)

    def reduce(self, a,b,c,d):
        # quadblitter notcurses like
        l = (a,b,c,d)
        def delta(i):
            return max([v[i] for v in l]) - min([v[i] for v in l])
        deltaR = delta(0)
        deltaG = delta(1)
        deltaB = delta(2)

        def midColor(c1,c2):
            return ((c1[0]+c2[0])//2,(c1[1]+c2[1])//2,(c1[2]+c2[2])//2)

        def closer(a,b,c):
            return \
                ( (a[0]-c[0])**2 + (a[1]-c[1])**2 + (a[2]-c[2])**2 ) > \
                ( (b[0]-c[0])**2 + (b[1]-c[1])**2 + (b[2]-c[2])**2 )

        def splitReduce(i):
            s = sorted(l,key=lambda x:x[i])
            mid = (s[3][i]+s[0][i])//2
            if s[1][i] < mid:
                if s[2][i] > mid:
                    c1 = midColor(s[0],s[1])
                    c2 = midColor(s[2],s[3])
                else:
                    c1 = midColor(s[0],s[1])
                    c1 = midColor(c1,s[2])
                    c2 = s[3]
            else:
                c1 = s[0]
                c2 = midColor(s[1],s[2])
                c2 = midColor(c1,s[3])


            ch  = 0x01 if closer(c1,c2,l[0]) else 0
            ch |= 0x02 if closer(c1,c2,l[1]) else 0
            ch |= 0x04 if closer(c1,c2,l[2]) else 0
            ch |= 0x08 if closer(c1,c2,l[3]) else 0

                   # 0x00 0x01 0x02 0x03
            quad = [ ' ', '▘', '▝', '▀',
                   # 0x04 0x05 0x06 0x07
                     '▖', '▌', '▞', '▛',
                   # 0x08 0x09 0x0A 0x0B
                     '▗', '▚', '▐', '▜',
                   # 0x0C 0x0D 0x0E 0x0F
                     '▄', '▙', '▟', '█']

            return  TTkString() + \
                    (TTkColor.bg(f'#{c1[0]:02X}{c1[1]:02X}{c1[2]:02X}') + \
                     TTkColor.fg(f'#{c2[0]:02X}{c2[1]:02X}{c2[2]:02X}')) + \
                    quad[ch]

        if deltaR >= deltaG and deltaR >= deltaB:
            # Use Red as splitter
            return splitReduce(0)
        elif deltaG >= deltaB and deltaG >= deltaR:
            # Use Green as splitter
            return splitReduce(1)
        else:
            # Use Blue as splitter
            return splitReduce(2)

    def paintEvent(self, canvas):
        for y, row in enumerate(TTkPeppered.peppered_old):
            for x, col in enumerate(row):
                if col == "#000000":
                    color=TTkColor.RST
                else:
                    color=TTkColor.bg(col)
                canvas.drawText(pos=(x,y), text=' ', color=color)
        img = self.peppered_20
        for y in range(0, len(img)&(~1), 2):
            for x in range(0, min(len(img[y])&(~1),len(img[y+1])&(~1)), 2):
                canvas.drawText( \
                        pos=(x//2+11,y//2), \
                        text=self.reduce(
                                    img[y][x]   , img[y][x+1]   ,
                                    img[y+1][x] , img[y+1][x+1] ))
        img = self.peppered_10
        for y in range(0, len(img)&(~1), 2):
            for x in range(0, min(len(img[y])&(~1),len(img[y+1])&(~1)), 2):
                canvas.drawText( \
                        pos=(x//2+22,y//2), \
                        text=self.reduce(
                                    img[y][x]   , img[y][x+1]   ,
                                    img[y+1][x] , img[y+1][x+1] ))

        canvas.drawText(pos=(22,6), text='TEST Peppered')


root = ttk.TTk()

win = ttk.TTkWindow(parent=root,pos = (1,1), size=(40,15), title="About", border=True)
TTkPeppered(parent=win)

root.mainloop()