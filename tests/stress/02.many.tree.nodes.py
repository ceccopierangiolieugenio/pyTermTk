#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

class _OnOff(ttk.TTkButton):
    classStyle = ttk.TTkButton.classStyle | {
                'checked':     {'color': ttk.TTkColor.fg("#00FF00")+ttk.TTkColor.bg("#444400"),
                                'borderColor': ttk.TTkColor.fg("#FFFFFF"),
                                'text': 'On',
                                'grid':0},
                'unchecked':   {'color': ttk.TTkColor.fg("#FF0000")+ttk.TTkColor.bg("#440000"),
                                'borderColor': ttk.TTkColor.RST,
                                'text': 'Off',
                                'grid':3},
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def text(self):
        if self._checked:
            return self.style()['checked']['text']
        else:
            return self.style()['unchecked']['text']

    def paintEvent(self, canvas):
        if self._checked:
            style = self.style()['checked']
        else:
            style = self.style()['unchecked']

        borderColor = style['borderColor']
        textColor   = style['color']
        text = style['text']

        w,h = self.size()

        # Draw the border and bgcolor
        canvas.drawChar(pos=(0  ,0), color=borderColor ,char='[')
        canvas.drawChar(pos=(w-1,0), color=borderColor ,char=']')
        canvas.drawText(pos=(1,0) ,text=text, color=textColor, width=w-2)



ttk.TTkLog.use_default_file_logging()

root = ttk.TTk(layout=ttk.TTkGridLayout())

root.layout().addWidget(btn:=ttk.TTkButton(text="Add Buttons",border=True,maxHeight=3),0,0)
root.layout().addWidget(tw:=ttk.TTkTree(),1,0,1,2)
root.layout().addWidget(ttk.TTkLogViewer(maxHeight=10),2,0,1,2)

tw.setHeaderLabels(          ["Name"  , "Console" , "Fatal" , "Error" , "Mil"  , "Warning" , "Info" , "Entry" , "Exit"])
tw._treeView._columnsPos =   [ _a:=50 , _b:=_a+10 , _b+6    ,  _b+12  ,  _b+18 , _b+24     , _b+30  , _b+36   , _b+42]
types = ("Fatal", "Error", "Mil", "Warning", "Info", "Entry", "Exit")

def _addMany():
    ttk.TTkLog.info("Start Stress!!!")
    items = []
    for i in range(300):
        _item_elements = [f"n: {i=}", 'console']
        for _t in types:
            _btn_t = _OnOff(checkable=True, checked=(i%0x07==0))
            _item_elements.append(_btn_t)
            # _item_elements.append(_t)
        _item = ttk.TTkTreeWidgetItem(_item_elements)
        items.append(_item)
    tw.addTopLevelItems(items)
    ttk.TTkLog.info("End Stress!!!")

btn.clicked.connect(_addMany)

root.mainloop()
