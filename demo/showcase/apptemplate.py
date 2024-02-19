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

import sys, os, argparse
from random import randint

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk


class AppTestWidget(ttk.TTkContainer):
    def __init__(self, at, wids, **kwargs):
        super().__init__(**kwargs)
        self._at = at
        self._wids = wids

        self.layout().addWidget(ttk.TTkLabel(pos=(1,0),text="v------< Border"))
        self.layout().addWidget(ttk.TTkLabel(pos=(1,1),text="   v---< Fixed"))
        self.layout().addWidget(ttk.TTkLabel(pos=(1,2),text="   <---< Main"))
        self.layout().addWidget(cbbm:=ttk.TTkCheckbox(pos=(0,2),size=(3,1), checked=True))
        cbbm.clicked.connect(lambda b: at.setBorder(b))

        for y,wn in enumerate(wids,3):
            wid = wids[wn]['wid']
            style = wid.style()
            # Choose a random color for the background
            h,s,l = randint(0,359),100,randint(60,80)
            r,g,b = ttk.TTkColor.hsl2rgb(((h+5)%360,s,l))
            style['default']['color'] = ttk.TTkColor.fg('#000000')+ttk.TTkColor.bg(f"#{r:02X}{g:02X}{b:02X}", modifier=ttk.TTkColorGradient(increment=+2))
            wid.setStyle(style)
            self.layout().addWidget(cbw:=ttk.TTkCheckbox(pos=(7,y),size=(10,1),checked=True,text=wn))
            self.layout().addWidget(cbb:=ttk.TTkCheckbox(pos=(0,y),size=(3,1), checked=True))
            self.layout().addWidget(cbf:=ttk.TTkCheckbox(pos=(3,y),size=(3,1), checked=False))
            cbw.clicked.connect(wid.setVisible)
            cbb.clicked.connect(lambda b,loc=wids[wn]['loc']: at.setBorder(b,loc))
            cbf.clicked.connect(lambda b,loc=wids[wn]['loc']: at.setFixed(b,loc))

def demoAppTemplate(root=None):
    at = ttk.TTkAppTemplate(parent=root)

    twl = ttk.TTkTestWidgetSizes(border=False, name="Left",   minSize=( 15,  5), maxSize=( 50, 25))
    twr = ttk.TTkTestWidgetSizes(border=False, name="Right",  minSize=( 15,  5), maxSize=( 50, 25))
    twh = ttk.TTkTestWidgetSizes(border=False, name="Header", minSize=( 15,  3), maxSize=(160,  7))
    twt = ttk.TTkTestWidgetSizes(border=False, name="Top",    minSize=( 15,  3), maxSize=(100,  7))
    twb = ttk.TTkTestWidgetSizes(border=False, name="Bottom", minSize=( 15,  3), maxSize=(100,  7))
    twf = ttk.TTkTestWidgetSizes(border=False, name="Footer", minSize=( 15,  3), maxSize=(160,  7))

    twm = AppTestWidget(
            at = at,
            wids={
                "Header" : {'wid': twh, 'loc':at.HEADER},
                "Footer" : {'wid': twf, 'loc':at.FOOTER},
                "Top"    : {'wid': twt, 'loc':at.TOP},
                "Bottom" : {'wid': twb, 'loc':at.BOTTOM},
                "Right"  : {'wid': twr, 'loc':at.RIGHT},
                "Left"   : {'wid': twl, 'loc':at.LEFT}},
            minSize=( 15,  5), maxSize=( 50, 10))

    at.setWidget(twm, at.MAIN)
    at.setWidget(twl, at.LEFT)
    at.setWidget(twr, at.RIGHT)
    at.setWidget(twh, at.HEADER)
    at.setWidget(twt, at.TOP)
    at.setWidget(twb, at.BOTTOM)
    at.setWidget(twf, at.FOOTER)

    return at



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    root = ttk.TTk()
    if args.f:
        rootAppTemplate = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootAppTemplate = ttk.TTkWindow(parent=root,pos = (0,0), size=(100,40), title="Test AppTemplate", border=True, layout=ttk.TTkGridLayout())
    demoAppTemplate(rootAppTemplate)
    root.mainloop()

if __name__ == "__main__":
    main()