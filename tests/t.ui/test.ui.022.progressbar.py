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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    layout = ttk.TTkGridLayout(columnMinHeight=1)
    if args.f:
        rootW = root
        root.setLayout(layout)
    else:
        rootW = ttk.TTkWindow(
            parent=root,pos=(1,1), size=(55,15), border=True, layout=layout,
            title="Test Progressbar (resize me)")

    class TextLAF(ttk.TTkLookAndFeelFPBar):
        def text(self, value, max, min):
            return 'low' if value < 0.5 else 'high'

    class ColorLAF(ttk.TTkLookAndFeelFPBar):
        def color(self, value,max,min):
            red, green = round(value*255), round((1-value)*255)
            fg = f"#{red:02x}{green:02x}00"
            return ( ttk.TTkColor.fg(fg) +
                     ttk.TTkColor.bg("#004444", modifier=ttk.TTkColorGradient(orientation=ttk.TTkK.HORIZONTAL, fgincrement=100, bgincrement=100)) )

    claf = ColorLAF(textWidth=5)

    rootW.layout().addWidget(pb1 := ttk.TTkFancyProgressBar(), row=0, col=0)
    rootW.layout().addWidget(pb2 := ttk.TTkFancyProgressBar(lookAndFeel=ColorLAF(showText=False)), row=2, col=0)
    rootW.layout().addWidget(pb3 := ttk.TTkFancyProgressBar(lookAndFeel=TextLAF(textWidth=6)),     row=3, col=0)

    rootW.layout().addWidget(pb4 := ttk.TTkFancyProgressBar(lookAndFeel=claf),            row=4, col=0)
    rootW.layout().addWidget(pb5 := ttk.TTkFancyProgressBar(lookAndFeel=claf, value=0.5), row=5, col=0)

    rootW.layout().addWidget(cbt := ttk.TTkCheckbox(text=" - Rem/Add Text", checked=True), row=6, col=0)

    cbt.stateChanged.connect(lambda x: claf.setShowText(x==ttk.TTkK.Checked))

    timer = ttk.TTkTimer()

    def _timerEvent():
        for pb in (pb1, pb2, pb3, pb4, pb5):
            last_value = pb.value()
            pb.setValue(0 if last_value == 1 else last_value + 0.01)

        timer.start(0.1)

    timer.timeout.connect(_timerEvent)
    timer.start(1)

    root.mainloop()

if __name__ == "__main__":
    main()
