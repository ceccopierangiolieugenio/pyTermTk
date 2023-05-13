#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import argparse
import os
import sys
import time


sys.path.append(os.path.join(sys.path[0],'..'))
from TermTk import TTk, TTkLog, TTkHelper
from TermTk import TTkGridLayout, TTkFileTree, TTkWidget, TTkFrame
from TermTk import TTkWindow, TTkColor, TTkColorGradient, TTkRadioButton, TTkSpacer
from TermTk import TTkTheme, TTkK, TTkSplitter, TTkTabWidget

# TTkFileTree(parent=self, path=".")
class _KolorFrame(TTkFrame):
    __slots__ = ('_fillColor')
    def __init__(self, *args, **kwargs):
        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_KolorFrame')
        self._fillColor = kwargs.get('fillColor', TTkColor.RST)

    def setFillColor(self, color):
        self._fillColor = color

    def paintEvent(self, canvas):
        w,h = self.size()
        for y in range(h):
            canvas.drawText(pos=(0,y),text='',width=w,color=self._fillColor)
        return super().paintEvent()


class KodeTab(TTkTabWidget):
    __slots__ = ('_frameOverlay')
    def __init__(self, *args, **kwargs):
        TTkTabWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'KodeTab')
        self._frameOverlay = _KolorFrame('visible',False)
        self._frameOverlay.setBorderColor(TTkColor.fg("#00FFFF")+TTkColor.bg("#000044"))
        self._frameOverlay.setFillColor(TTkColor.bg("#000088", modifier=TTkColorGradient(increment=-3)))
        self.rootLayout().addWidget(self._frameOverlay)


    def dragEnterEvent(self, evt) -> bool:
        TTkLog.debug(f"leave")
        return True

    def dragLeaveEvent(self, evt) -> bool:
        TTkLog.debug(f"leave")
        self._frameOverlay.hide()
        return True

    def dragMoveEvent(self, evt) -> bool:
        x,y = evt.x, evt.y
        w,h = self.size()
        if y<3:
            return super().dragMoveEvent(evt)
        h-=3
        y-=3
        if x<w//4:
            self._frameOverlay.show()
            self._frameOverlay.resize(w//4,h)
            self._frameOverlay.move(0, 3)
        elif x>w*3//4:
            self._frameOverlay.show()
            self._frameOverlay.resize(w//4,h)
            self._frameOverlay.move(w-w//4, 3)
        elif y<h//4:
            self._frameOverlay.show()
            self._frameOverlay.resize(w,h//4)
            self._frameOverlay.move(0, 3)
        elif y>h*3//4:
            self._frameOverlay.show()
            self._frameOverlay.resize(w,h//4)
            self._frameOverlay.move(0, 3+h-h//4)
        else:
            self._frameOverlay.hide()
        return True

    def dropEvent(self, evt) -> bool:
        self._frameOverlay.hide()
        x,y = evt.x, evt.y
        ret = True
        data = evt.data()
        tb = data.tabButton()
        tw = data.tabWidget()
        if y<3:
            ret = super().dropEvent(evt)
        else:
            w,h = self.size()
            h-=3
            y-=3
            index  = tw._tabBar._tabButtons.index(tb)
            widget = tw._tabWidgets[index]

            def _processDrop(index, orientation, offset):
                tw.removeTab(index)
                splitter = self.parentWidget()
                index = splitter.indexOf(self)
                if splitter.orientation() != orientation:
                    splitter.replaceWidget(index, splitter := TTkSplitter(orientation=orientation))
                    splitter.addWidget(self)
                    index=offset
                splitter.insertWidget(index+offset, kt:=KodeTab())
                kt.addTab(widget,tb.text())
            if x<w//4:
                _processDrop(index, TTkK.HORIZONTAL, 0)
            elif x>w*3//4:
                _processDrop(index, TTkK.HORIZONTAL, 1)
            elif y<h//4:
                _processDrop(index, TTkK.VERTICAL, 0)
            elif y>h*3//4:
                _processDrop(index, TTkK.VERTICAL, 1)
            else:
                ret = super().dropEvent(evt)

        # Remove the widget and/or all the cascade empty splitters
        if not tw._tabWidgets:
            widget = tw
            splitter = widget.parentWidget()
            while splitter.count() == 1:
                widget = splitter
                splitter = widget.parentWidget()
            splitter.removeWidget(widget)

        return ret


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    TTkLog.use_default_file_logging()
    TTkTheme.loadTheme(TTkTheme.NERD)

    root = TTk(title="ttkode")
    layout = TTkGridLayout()
    if args.f:
        root.setLayout(layout)
        container = root
        border = False
    else:
        container = TTkWindow(parent=root,pos=(0,0), size=(100,40), title="pyTermTk Showcase", border=True, layout=layout)
        border = True

    splitter = TTkSplitter(parent=container)
    splitter.addWidget(fileTree:=TTkFileTree(path='.'), 15)

    hSplitter = TTkSplitter(parent=splitter,  orientation=TTkK.HORIZONTAL)
    kt = KodeTab(parent=hSplitter)

    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#008800", modifier=TTkColorGradient(increment=-6)), title="uno"),"uno")
    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#880000", modifier=TTkColorGradient(increment=-6)), title="due"),"due")
    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#000088", modifier=TTkColorGradient(increment=-6)), title="tre"),"tre")
    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#888800", modifier=TTkColorGradient(increment=-6)), title="quattro"),"quattro")
    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#008888", modifier=TTkColorGradient(increment=-6)), title="cinque"),"cinque")
    kt.addTab(_KolorFrame(fillColor=TTkColor.bg("#880088", modifier=TTkColorGradient(increment=-6)), title="sei"),"sei")

    root.mainloop()

if __name__ == "__main__":
    main()