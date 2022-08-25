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

import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

class graphTimerEvent():
    def __init__(self, w, delay):
        self.timer = ttk.TTkTimer()
        self.val = 10
        self.delay = delay
        self.w = w
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1)
    @ttk.pyTTkSlot()
    def timerEvent(self):
        plot = [
            math.sin((self.val+10)*math.pi/30)*
            math.sin((self.val+15)*math.pi/40)*4*7,
            math.sin( self.val    *math.pi/40)*4*10 ,
            math.sin((self.val+20)*math.pi/30)*4*5,
            ]
        self.val+=1
        self.w.addValue(plot)
        self.timer.start(self.delay)

def demoScrollArea(root= None):
    scrollArea = ttk.TTkScrollArea(parent=root)
    ttk.TTkTestWidget(pos=(0,0)   , size=(50,25), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(10,25) , size=(40,20), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(20,50) , size=(60,10), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(50,0)  , size=(40,10), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(100,0) , size=(40,10), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(150,0) , size=(40,10), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidgetSizes(pos=(50,31) , size=(60,10), parent=scrollArea.viewport(), border=True)
    ttk.TTkTestWidget(pos=(110,15) , size=(60,40), parent=scrollArea.viewport(), border=True)
    graph = ttk.TTkGraph(  pos=(50,11) , size=(60,20), parent=scrollArea.viewport(), color=ttk.TTkColor.fg('#ff8800', modifier=ttk.TTkColorGradient(increment= 40)))
    graphTimerEvent(graph, 0.1)
    return scrollArea

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if args.f:
        rootGraph = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        rootGraph = ttk.TTkWindow(parent=root,pos=(1,1), size=(100,40), title="Test Scroll Area", border=True, layout=ttk.TTkGridLayout())
    demoScrollArea(rootGraph)
    root.mainloop()

if __name__ == "__main__":
    main()