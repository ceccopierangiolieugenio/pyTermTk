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

def demoGraph(root= None):
    frame = ttk.TTkFrame(parent=root, border=False, layout=ttk.TTkGridLayout())
    graphWidget1 = ttk.TTkGraph(color=ttk.TTkColor.fg('#00dddd', modifier=ttk.TTkColorGradient(increment=-25)))
    graphWidget2 = ttk.TTkGraph(direction=ttk.TTkK.LEFT, color=ttk.TTkColor.fg('#ff8800', modifier=ttk.TTkColorGradient(increment= 40)))
    graphWidget3 = ttk.TTkGraph(color=ttk.TTkColor.fg('#dd00dd', modifier=ttk.TTkColorGradient(increment=-20)))
    graphWidget4 = ttk.TTkGraph(color=ttk.TTkColor.fg('#00dd44', modifier=ttk.TTkColorGradient(increment=-30)))
    frame.layout().addWidget(graphWidget1, 0,0)
    frame.layout().addWidget(graphWidget2, 0,1)
    frame.layout().addWidget(graphWidget3, 1,0)
    frame.layout().addWidget(graphWidget4, 1,1)
    class timerEvent():
        def __init__(self, w, type):
            self.timer = ttk.TTkTimer()
            self.val = 10
            self.switch = False
            self.w = w
            self.type = type
            self.timer.timeout.connect(self.timerEvent)
            self.timer.start(1)
        @ttk.pyTTkSlot()
        def timerEvent(self):
            self.switch = not self.switch
            if self.type == 1: # Simple sin
                    val = math.sin(self.val*math.pi/40)*4*10
            if self.type == 2: # Double sin
                offset = 15
                if self.switch: val = math.sin(self.val*math.pi/40)*4*10
                else:           val = math.sin((self.val+offset)*math.pi/40)*4*7
            if self.type == 3: # random
                val = random.uniform(-40,+40)
            if self.type == 4: # mix rand and sin
                if self.switch: val = math.sin(self.val*math.pi/40)*4*10
                else:           val = random.uniform(-40,+40)
            self.val+=1
            self.w.addValue(val)
            self.timer.start(0.1)
    timerEvent(graphWidget1, 1)
    timerEvent(graphWidget2, 2)
    timerEvent(graphWidget3, 3)
    timerEvent(graphWidget4, 4)
    return frame

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
        rootGraph = ttk.TTkWindow(parent=root,pos=(1,1), size=(100,40), title="Test Graph", border=True, layout=ttk.TTkGridLayout())
    demoGraph(rootGraph)
    root.mainloop()

if __name__ == "__main__":
    main()